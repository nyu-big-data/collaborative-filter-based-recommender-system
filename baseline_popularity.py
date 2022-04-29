import getpass

from pyspark.sql import SparkSession
from pyspark.sql.functions import count,sum


def baseline_popularity_model(spark,netID,size_type,damping_factor):
    schema = 'userId INT, movieId INT, rating FLOAT , timestamp INT, title STRING'
    ratingsTrain = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True ,schema=schema)
    ratingsTest = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True)

    ratingsTrain.groupby('movieId','title').agg((sum('rating')/(count('rating')+damping_factor)).alias('pRatings')).show()

def baseline_popularity_model_v2(spark,netID,size_type,damping_factor_global,damping_factor_item):
    # Implementing R = u + bi + bu (popularity model)

    schema = 'userId INT, movieId INT, rating FLOAT , timestamp INT, title STRING'
    ratingsTrain = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True ,schema=schema)
    ratingsTest = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True)
    
    # global_ratings = ratingsTrain.agg((sum('rating')/(count('rating')+damping_factor_global)).alias('global_ratings')).first()['global_ratings']
    # ratingsTrain.groupby('movieId').agg(((sum('rating')- global_ratings)/(count('rating')+damping_factor_item)).alias('movieRatings')).show()
    # ratingsTrain.groupby('userId').agg()
    
if __name__ == "__main__":
    spark = SparkSession.builder.appName("Baseline-Popularityå-GRP33").getOrCreate()

    netID = getpass.getuser()
    size_type = 'ml-latest-small'
    damping_factor = 5
    baseline_popularity_model(spark,netID,size_type, damping_factor)

    spark.stop()