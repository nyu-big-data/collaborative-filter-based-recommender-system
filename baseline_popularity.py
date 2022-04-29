import getpass

from pyspark.sql import SparkSession
from pyspark.sql.functions import count,sum


def baseline_popularity_model(spark,netID,size_type,damping_factor):
    schema = 'userId INT, movieId INT, rating FLOAT , timestamp INT, title STRING'
    ratingsTrain = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True ,schema=schema)
    ratingsTest = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/training.csv' ,header=True)

    ratingsTrain.groupby('movieId','title').agg((sum('rating')/(count('rating')+damping_factor)).alias('pRatings')).show()


if __name__ == "__main__":
    spark = SparkSession.builder.appName("Baseline-Popularityå-GRP33").getOrCreate()

    netID = getpass.getuser()
    size_type = 'ml-latest-small'
    damping_factor = 5
    baseline_popularity_model(spark,netID,size_type, damping_factor)

    spark.stop()