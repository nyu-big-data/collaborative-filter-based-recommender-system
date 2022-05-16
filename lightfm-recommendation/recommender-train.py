from lightfm import LightFM
from lightfm.data import Dataset
from lightfm.evaluation import precision_at_k,auc_score,recall_at_k
from lightfm.cross_validation import random_train_test_split
from lightfm.datasets import fetch_movielens
from scipy.sparse import csr_matrix
import pandas as pd

movielens = fetch_movielens()

def prepare_dataset(size_type):
    # Loading  csv file
    ratingsDF = pd.read_csv('{}/ratings.csv'.format(size_type) ,usecols=['userId', 'movieId','rating'])
    ratings = ratingsDF.to_dict('records')
    
    dataset = Dataset()
    dataset.fit((x['userId'] for x in ratings), (x['movieId'] for x in ratings))
    
    num_users, num_items = dataset.interactions_shape()
    print('Num users: {}, num_items {}.'.format(num_users, num_items))

    # building  interaction matrix between userId and movieId
    dataRating = ((x['userId'], x['movieId'],x['rating']) for x in ratings) 
    print(dataRating)
    (interactions, weights) = dataset.build_interactions(dataRating)
    
    # # Creating a sparse matrix
    # interactions = csr_matrix((ratingsArr, (userIds, movieIds)))
    # spliting the interaction into test and train
    train,test = random_train_test_split(interactions,test_percentage=0.25)    
    interactions = {
        'train':train,
        'test':test
    }
    # print(repr(interactions))
    return movielens

def train_model(data):
    # Instantiate and train the model
    model = LightFM(loss='warp')
    model.fit(data['train'], epochs=30, num_threads=2)
    # print(type(data))
    return model

def evaluate_model(model,data):
    # Evaluate the trained model
    train_precision = precision_at_k(model, data['train'], k=10).mean()
    test_precision = precision_at_k(model, data['test'], k=10).mean()

    train_auc = auc_score(model, data['train']).mean()
    test_auc = auc_score(model, data['test']).mean()

    train_recall = recall_at_k(model, data['train']).mean()
    test_recall = recall_at_k(model, data['test']).mean()


    print('Precision: train %.2f, test %.2f.' % (train_precision, test_precision))
    print('AUC: train %.2f, test %.2f.' % (train_auc, test_auc))



if __name__ == "__main__":

    size_type = 'ml-latest-small'
    data = prepare_dataset(size_type)
    model = train_model(data)
    print(data['train'])
    evaluate_model(model,data)