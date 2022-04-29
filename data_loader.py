import getpass

# And pyspark.sql to get the spark session
from pyspark.sql import SparkSession
import pyspark.sql.functions as func

def process_movie_data(spark,size_type,netID):
    '''Loads MovieLens data, processes them into dataframe and divide into train,test and validation testset
    Parameters
    ----------
    spark : SparkSession object
    '''
    # Load the data into DataFrame
    movies = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/movies.csv' ,header=True,schema='movieId INT, title STRING, genres STRING')
    ratings = spark.read.csv(f'hdfs:/user/{netID}/movielens/{size_type}/ratings.csv', header=True, schema='userId INT, movieId INT, rating FLOAT, timestamp INT')

    # print('Printing movies schema')
    movies.printSchema()
    # print('Printing ratings schema')
    ratings.printSchema()
    
    # creating temp view for running sql query
    movies.createOrReplaceTempView('movies')
    ratings.createOrReplaceTempView('ratings')

    df = spark.sql('SELECT rt.*, mov.title FROM ratings rt JOIN movies mov ON rt.movieId=mov.movieId')
    df.sort('timestamp')
    df.repartition(10,'timestamp')
    
    (train, test) = df.randomSplit([0.8, 0.2])
    train.write.mode('overwrite').parquet(f'hdfs:/user/{netID}/movielens/{size_type}/train.parquet')
    test.write.mode('overwrite').parquet(f'hdfs:/user/{netID}/movielens/{size_type}/test.parquet')
 
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('Recommender-DataLoader-GRP33').getOrCreate()

    netID = getpass.getuser()

    process_movie_data(spark, 'ml-latest-small', netID)

    spark.stop()
