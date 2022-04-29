import getpass

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

def baseline_popularity_model(spark,netID,size_type,damping_factor):
    schema = 'userId INT, movieId INT, rating FLOAT, timestamp INT, title STRING'
    ratingsTrain = spark.read.parquet(f'hdfs:/user/{netID}/movielens/{size_type}/train.parquet', header=True, schema=schema)
    itemRatings = ratingsTrain.groupby('movieId','title').agg((F.sum('rating')/(F.count('rating')+damping_factor)).alias('pRatings'))
    calculatedRatings = ratingsTrain.join(itemRatings, ratingsTrain.movieId == itemRatings.movieId, "left")
    calculateMetrics(calculatedRatings) 

def baseline_popularity_model_v2(spark,netID,size_type,damping_factor_global,damping_factor_item,damping_factor_user):
    # Implementing R = u + bi + bu (popularity model)
    schema = 'userId INT, movieId INT, rating FLOAT , timestamp INT, title STRING'
    ratingsTrain = spark.read.parquet(f'hdfs:/user/{netID}/movielens/{size_type}/train.parquet', header=True, schema=schema)
    ratingsTest = spark.read.parquet(f'hdfs:/user/{netID}/movielens/{size_type}/test.parquet', header=True, schema=schema)
    global_ratings = ratingsTrain.agg((F.sum('rating')/(F.count('rating')+damping_factor_global)).alias('global_ratings')).first()['global_ratings']
    movie_bias = ratingsTrain.groupby('movieId').agg((F.sum(ratingsTrain.rating - global_ratings)/(F.count('rating')+damping_factor_item)).alias('movieRatings'))
    calculatedRatings = ratingsTrain.join(movie_bias, ratingsTrain.movieId == movie_bias.movieId, "left")
    user_bias = calculatedRatings.groupby('userId')\
                                 .agg((F.sum(ratingsTrain.rating - global_ratings - calculatedRatings.movieRatings)/(F.count('rating')+damping_factor_user))\
                                 .alias('userRatings'))
    calculatedRatings = calculatedRatings.join(user_bias, calculatedRatings.userId == user_bias.userId, "left")
    calculatedRatings = calculatedRatings.withColumn('pRatings', global_ratings + calculatedRatings.movieRatings + calculatedRatings.userRatings)
    calculateMetrics(calculatedRatings) 
    
def calculateMetrics(ratingsDF):
    combinedDF = ratingsDF.withColumn("Diff", ratingsDF.rating - ratingsDF.pRatings)
    combinedDF = combinedDF.withColumn("RMSE", F.pow(combinedDF.Diff, F.lit(2)))\
                           .withColumn("MAE", F.abs(combinedDF.Diff))
    combinedDF.select(F.sqrt(F.avg(F.col("RMSE"))).alias("RMSE"),\
                      F.avg(F.col("MAE")).alias("MAE"))\
                      .show()

if __name__ == "__main__":
    spark = SparkSession.builder.appName("Baseline-Popularity-GRP33").getOrCreate()
    netID = getpass.getuser()
    size_type = 'ml-latest-small'
    damping_factor = 5
    baseline_popularity_model(spark,netID,size_type, damping_factor)
    baseline_popularity_model_v2(spark,netID,size_type, damping_factor, damping_factor, damping_factor)
    spark.stop()
