import getpass

# And pyspark.sql to get the spark session
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

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
    
    (trainUserIds, valUserIds, testUserIds) = df.select('userId').distinct().randomSplit([0.6, 0.2, 0.2])
    trainUserIds = [x.userId for x in trainUserIds.collect()]
    trainUserIds_broadcast = spark.sparkContext.broadcast(trainUserIds)
    valUserIds = [x.userId for x in valUserIds.collect()]
    valUserIds_broadcast = spark.sparkContext.broadcast(valUserIds)
    testUserIds = [x.userId for x in testUserIds.collect()]
    testUserIds_broadcast = spark.sparkContext.broadcast(testUserIds)
    val = df.filter(F.col('userId').isin(valUserIds_broadcast.value))
    test = df.filter(F.col('userId').isin(testUserIds_broadcast.value))
    train = df.filter(F.col('userId').isin(trainUserIds_broadcast.value))
    val.select('userId').distinct().show()
    test.select('userId').distinct().show()
    (val_few_interactions,_) = val.randomSplit([0.6, 0.4])
    (test_few_interactions,_) = test.randomSplit([0.6, 0.4])
    train = train.union(val_few_interactions).union(test_few_interactions)
    train.write.mode('overwrite').parquet(f'hdfs:/user/{netID}/movielens/{size_type}/train.parquet')
    val.write.mode('overwrite').parquet(f'hdfs:/user/{netID}/movielens/{size_type}/val.parquet')
    test.write.mode('overwrite').parquet(f'hdfs:/user/{netID}/movielens/{size_type}/test.parquet')
 
if __name__ == "__main__":

    # Create the spark session object
    spark = SparkSession.builder.appName('Recommender-DataLoader-GRP33').getOrCreate()

    netID = getpass.getuser()

    process_movie_data(spark, 'ml-latest-small', netID)
    process_movie_data(spark, 'ml-latest', netID)

    spark.stop()
