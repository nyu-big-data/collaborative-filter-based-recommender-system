import getpass

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql import Row
from pyspark.sql.window import Window
from pyspark.ml.evaluation import RankingEvaluator

def baseline_popularity_model(spark,netID,size_type,damping_factor):
    schema = 'userId INT, movieId INT, rating FLOAT, timestamp INT, title STRING'
    ratingsTrain = spark.read.parquet(f'hdfs:/user/{netID}/movielens/{size_type}/train.parquet', header=True, schema=schema)
    finalRatings = (ratingsTrain.select('userId').distinct()).crossJoin(ratingsTrain.select('movieId').distinct())
    itemRatings = ratingsTrain.groupby('movieId').agg((F.sum('rating')/(F.count('rating')+damping_factor)).alias('pRatings'))
    finalRatings = finalRatings.join(itemRatings, ['movieId'], "left")\
                               .select("userId", "movieId", "pRatings")
    return finalRatings

def baseline_popularity_model_v2(spark,netID,size_type,damping_factor_global,damping_factor_item,damping_factor_user):
    # Implementing R = u + bi + bu (popularity model)
    schema = 'userId INT, movieId INT, rating FLOAT, timestamp INT, title STRING'
    ratingsTrain = spark.read.parquet(f'hdfs:/user/{netID}/movielens/{size_type}/train.parquet', header=True, schema=schema)
    finalRatings = (ratingsTrain.select('userId').distinct()).crossJoin(ratingsTrain.select('movieId').distinct())
    global_ratings = ratingsTrain.agg((F.sum('rating')/(F.count('rating')+damping_factor_global)).alias('global_ratings')).first()['global_ratings']
    movie_bias = ratingsTrain.groupby('movieId').agg((F.sum(ratingsTrain.rating - global_ratings)/(F.count('rating')+damping_factor_item))\
                             .alias('movieRatings')).select(F.col("movieId").alias("movieId_mod"), F.col("movieRatings"))
    ratingsTrain = ratingsTrain.join(movie_bias, ratingsTrain.movieId == movie_bias.movieId_mod, "left")\
                               .select("userId", "movieId", "rating", "movieRatings")
    user_bias = ratingsTrain.groupby('userId').agg((F.sum(ratingsTrain.rating - global_ratings - ratingsTrain.movieRatings)/(F.count('rating')+damping_factor_user))\
                            .alias('userRatings')).select(F.col("userId").alias("userId_mod"), F.col("userRatings"))
    finalRatings = finalRatings.join(movie_bias, finalRatings.movieId == movie_bias.movieId_mod, "left")\
                               .join(user_bias, finalRatings.userId == user_bias.userId_mod, "left")\
                               .select("userId", "movieId", "userRatings", "movieRatings")\
                               .withColumn('pRatings', global_ratings + F.col("movieRatings") + F.col("userRatings"))\
                               .select("userId", "movieId", "pRatings")
    return finalRatings

def runEval(spark, netID, size_type, evalFileName, finalRatings, metrics):
    schema = 'userId INT, movieId INT, rating FLOAT, timestamp INT, title STRING'
    ratingsVal = spark.read.parquet(evalFileName, header=True, schema=schema)\
                           .join(finalRatings, ["userId", "movieId"], "inner")\
                           .select("userId", "movieId", "rating", "pRatings")
    nonRankingMetrics = calculateMetrics(ratingsVal)
    finalRatings = finalRatings.withColumn("rank", F.dense_rank().over(Window.partitionBy("userId").orderBy(F.desc("pRatings"))))\
                               .filter(F.col("rank") <= 100)\
                               .orderBy(F.asc("rank"))\
                               .groupBy("userId").agg(F.collect_list("movieId").alias('predictions'))\
                               .withColumn("predictions", F.col("predictions").cast("array<double>"))\
                               .select("userId", "predictions")
    ratingsVal = ratingsVal.select("userId", "movieId", "rating")\
                           .withColumn("rank", F.dense_rank().over(Window.partitionBy("userId").orderBy(F.desc("rating"))))\
                           .filter(F.col("rank") <= 100)\
                           .orderBy(F.asc("rank"))\
                           .groupBy("userId").agg(F.collect_list("movieId").alias('labels'))\
                           .withColumn("labels", F.col("labels").cast("array<double>"))\
                           .select("userId", "labels")
    validationRatings = ratingsVal.join(finalRatings, ["userId"], "inner")\
                                  .select("userId", "predictions", "labels")
    calculated_metrics = dict().fromkeys(metrics)
    for metric in metrics:
        evaluator = RankingEvaluator(predictionCol="predictions", labelCol="labels", metricName=metric, k=100)
        calculated_metrics[metric] = evaluator.evaluate(validationRatings)
    calculated_metrics.update(nonRankingMetrics)
    return calculated_metrics
    
def calculateMetrics(finalRatings):
    metrics = finalRatings.withColumn("Diff", finalRatings.rating - finalRatings.pRatings)\
                          .withColumn("RMSE", F.pow(F.col("Diff"), F.lit(2)))\
                          .withColumn("MAE", F.abs(F.col("Diff")))\
                          .select(F.sqrt(F.avg(F.col("RMSE"))).alias("RMSE"),\
                                  F.avg(F.col("MAE")).alias("MAE"))\
                          .first()
    return {"RMSE" : metrics["RMSE"], "MAE" : metrics["MAE"]}

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Baseline-Popularity-GRP33").getOrCreate()
    netID = getpass.getuser()
    size_types = ['ml-latest-small', 'ml-latest']
    metrics = ["meanAveragePrecisionAtK", "precisionAtK", "ndcgAtK", "recallAtK"]
    damping_factor = 100
    for size_type in size_types:
        val_file = f'hdfs:/user/{netID}/movielens/{size_type}/val.parquet'
        test_file = f'hdfs:/user/{netID}/movielens/{size_type}/test.parquet'
        # Using Basic Model with no User and Item Bias
        finalRatings = baseline_popularity_model(spark, netID, size_type, damping_factor)
        metrics_values_val = runEval(spark, netID, size_type, val_file, finalRatings, metrics)
        metrics_values_test = runEval(spark, netID, size_type, test_file, finalRatings, metrics)
        metrics_values_val["dataset"] = "val"
        metrics_values_test["dataset"] = "test"
        metricsDF = spark.createDataFrame(Row(**x) for x in [metrics_values_val, metrics_values_test])
        metricsDF.write.mode("overwrite").option("header",True).csv(f'hdfs:/user/{netID}/movielens/{size_type}/metrics-basic.csv')
        # Using Enhanced Model with User and Item Bias
        finalRatings = baseline_popularity_model_v2(spark, netID, size_type, damping_factor, damping_factor, damping_factor)
        metrics_values_val = runEval(spark, netID, size_type, val_file, finalRatings, metrics)
        metrics_values_test = runEval(spark, netID, size_type, test_file, finalRatings, metrics)
        metrics_values_val["dataset"] = "val"
        metrics_values_test["dataset"] = "test"
        metricsDF = spark.createDataFrame(Row(**x) for x in [metrics_values_val, metrics_values_test])
        metricsDF.write.mode("overwrite").option("header",True).csv(f'hdfs:/user/{netID}/movielens/{size_type}/metrics-enhanced.csv')
    spark.stop()
