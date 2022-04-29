import getpass

from pyspark.sql import SparkSession
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator


# from pyspark.sql import Row

def train_model(spark, netID,size_type, latentRanks, regularizationParams):
    schema = 'userId INT, movieId INT, rating FLOAT , timestamp INT, title STRING'
    ratingsTrain = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True ,schema=schema)
    
    
    # Build the recommendation model using ALS on the training data
    # Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
    als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating", nonnegative = True, implicitPrefs = False, coldStartStrategy="drop")
    # model = als.fit(ratingsTrain)

    # Add hyperparameters and their respective values to param_grid
    param_grid = ParamGridBuilder().addGrid(als.rank, latentRanks).addGrid(als.regParam, regularizationParams).build()

    # Define evaluator as RMSE 
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction") 
    
    # Build cross validation using CrossValidator
    cv = CrossValidator(estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=5)

    #Fit cross validator to the training dataset
    model = cv.fit(ratingsTrain)

    #fetch the best model
    best_model = model.bestModel

    print("Best Model - Rank:",best_model._java_obj.parent().getRank(), " RegParam:",best_model._java_obj.parent().getRegParam())
    # best_model.save("./models/")
    
    return best_model,evaluator



def evaluate_test_pred(model,evaluator):
    schema = 'userId INT, movieId INT, rating FLOAT , timestamp INT, title STRING'
    ratingsTest = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True),schema=schema)

    test_pred = model.transform(ratingsTest)
    rmse = evaluator.evaluate(test_pred)
    print(rmse)
    return rmse,test_pred




if __name__ == "__main__":
    spark = SparkSession.builder.appName("Recommender-Model-GRP33").getOrCreate()

    regularizationParams = [.01, .05, .1, .15]
    latentRanks = [10, 50, 100, 150]
    netID = getpass.getuser()
    size_type = 'ml-latest-small'
    model,evaluator = train_model(spark, netID,size_type, latentRanks, regularizationParams)

    evaluate_test_pred(model,evaluator)


    # Generate top 10 movie recommendations for each user
    userRecs = model.recommendForAllUsers(10)
    # Generate top 10 user recommendations for each movie
    movieRecs = model.recommendForAllItems(10)

    # Generate top 10 movie recommendations for a specified set of users
    # users = ratings.select(als.getUserCol()).distinct().limit(3)
    # userSubsetRecs = model.recommendForUserSubset(users, 10)
    # Generate top 10 user recommendations for a specified set of movies
    # movies = ratings.select(als.getItemCol()).distinct().limit(3)
    # movieSubSetRecs = model.recommendForItemSubset(movies, 10)
    # $example off$
    userRecs.show()
    movieRecs.show()
    # userSubsetRecs.show()
    # movieSubSetRecs.show()

    spark.stop()