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
    links = spark.read.csv(f'{data_path}links.csv',header=True,schema='movieId INT, imdbId STRING, tmdbId STRING')
    movies = spark.read.csv(f'{data_path}movies.csv',header=True,schema='movieId INT, title STRING, genres STRING')
    ratings = spark.read.csv(f'{data_path}ratings.csv',header=True,schema='userId INT,movieId INT,rating FLOAT, timestamp INT')
    tags = spark.read.csv(f'{data_path}tags.csv',header=True,schema='userId INT,movieId INT,tag STRING')



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

    df = spark.sql('SELECT rt.*,mov.title FROM ratings rt JOIN movies mov ON rt.movieId=mov.movieId')
    df.repartition(10,'timestamp')
    df.sort('timestamp')
    print(df.head())
    (training, test) = df.randomSplit([0.8, 0.2])
    # training.write.parquet('training.parquet')
    # val.write.parquet('val.parquet')
    # test.write.parquet('test.parquet')
    training.write.csv('training.csv')
    test.write.csv('testing.csv')

 
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('Recommender-DataLoader-GRP33').getOrCreate()

    process_movie_data(spark)
