# And pyspark.sql to get the spark session
from pyspark.sql import SparkSession
import pyspark.sql.functions as func

def process_movie_data(spark):
    '''Loads MovieLens data, processes them into dataframe and divide into train,test and validation testset
    Parameters
    ----------
    spark : SparkSession object
    '''
    data_path = '/scratch/work/courses/DSGA1004-2021/movielens/ml-latest-small/'
    # Load the data into DataFrame
    links = spark.read.csv(f'{data_path}links.csv',header=True,schema='movieId STRING, imdbId STRING, tmdbId STRING')
    movies = spark.read.csv(f'{data_path}movies.csv',header=True,schema='movieId STRING, title STRING, genres STRING')
    ratings = spark.read.csv(f'{data_path}ratings.csv',header=True,schema='userId STRING,movieId STRING,rating FLOAT, timestamp STRING')
    tags = spark.read.csv(f'{data_path}tags.csv',header=True,schema='userId STRING,movieId STRING,tag STRING, timestamp STRING')



    print('Printing links schema')
    links.printSchema()
    print('Printing movies schema')
    movies.printSchema()
    print('Printing ratings schema')
    ratings.printSchema()
    print('Printing tags schema')
    tags.printSchema()
    
    # creating temp view for running sql query
    links.createOrReplaceTempView('links')
    movies.createOrReplaceTempView('movies')
    ratings.createOrReplaceTempView('ratings')
    tags.createOrReplaceTempView('tags')

    df = spark.sql('SELECT rt.userId,rt.movieId,mov.title,rt.rating FROM ratings rt JOIN movies mov ON rt.movieId=mov.movieId')
    (training, val, test) = df.randomSplit([0.6, 0.2, 0.2])
    # training.write.parquet('training.parquet')
    # val.write.parquet('val.parquet')
    # test.write.parquet('test.parquet')
    training.write.csv('training.csv')
    val.write.csv('val.csv')
    test.write.csv('test.csv')

 
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('Recommender-DataLoader-GRP33').getOrCreate()

    process_movie_data(spark)
