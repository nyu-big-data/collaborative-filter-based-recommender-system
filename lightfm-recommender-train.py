from lightfm import LightFM
from lightfm.data import Dataset
from lightfm.evaluation import precision_at_k,auc_score,recall_at_k,reciprocal_rank
from lightfm.cross_validation import random_train_test_split
import scipy.sparse as sp
import pandas as pd
import numpy as np

from scipy import stats
from sklearn.model_selection import KFold, RandomizedSearchCV

from utils import nested_dict_to_csv

import time

ROOT_DIR = ''#'/scratch/work/courses/DSGA1004-2021/movielens/'
SEED = 42

def build_interaction_matrix(shape, data, min_rating=0.0):

    mat = sp.lil_matrix(shape, dtype=np.int32)

    for dt in data:
        rating = min_rating
        if dt['rating'] >= min_rating:
            rating = dt['rating']
        
        mat[dt['userId'], dt['movieId']] = rating

    return mat.tocoo()

def prepare_dataset(size_type):
    # Loading  csv file
    ratingsDF = pd.read_csv('{}{}/ratings.csv'.format(ROOT_DIR,size_type) ,usecols=['userId', 'movieId','rating'])
    ratings = ratingsDF.to_dict('records')
    
    num_users = ratingsDF['userId'].max() + 1
    num_items = ratingsDF['movieId'].max() + 1
    
    print('Num users: {}, num_items {}.'.format(num_users, num_items))

    # building  interaction matrix between userId and movieId with ratings
    interaction_mat = build_interaction_matrix((num_users, num_items),ratings)
    
    # spliting the interaction into test and train
    train,test = random_train_test_split(interaction_mat,test_percentage=0.25)    
    interactions = {
        'train':train,
        'test':test
    }
    return interactions

def train_model(data,hyperparams):
    # Instantiate and train the model
    model = LightFM(**hyperparams)
    model.fit(data['train'], epochs=30, num_threads=8)
    # print(type(data))
    return model

def evaluate_model(model,data):
    # Evaluate the trained model
    metrics = {
        'precision_at_k': {
            'train':precision_at_k(model, data['train'], k=100).mean(),
            'test':precision_at_k(model, data['test'], k=100).mean()
        },
        'auc_score':{
            'train':auc_score(model, data['train']).mean(),
            'test':auc_score(model, data['test']).mean()
        },
        'recall_at_k':{
            'train':recall_at_k(model, data['train'],k=100).mean(),
            'test':recall_at_k(model, data['test'],k=100).mean(),
        },
        'reciprocal_rank':{
            'train':reciprocal_rank(model, data['train']).mean(),
            'test':reciprocal_rank(model, data['test']).mean()
        }
    }
    return metrics

def cv_sklearn_hyperparameter_tuning(data):

    model = LightFM(loss="warp", random_state=SEED)

    # Set distributions for hyperparameters
    randint = stats.randint(low=1, high=65)
    randint.random_state = SEED
    gamma = stats.gamma(a=1.2, loc=0, scale=0.13)
    gamma.random_state = SEED
    distr = {"no_components": randint, "learning_rate": gamma, "loss":["bpr", "warp", "warp-kos","logistic"]}


    # Custom score function
    def scorer(est, x, y=None):
        return precision_at_k(est, x).mean()

    # Dummy custom CV to ensure shape preservation.
    class CV(KFold):
        def split(self, X, y=None, groups=None):
            idx = np.arange(X.shape[0])
            for _ in range(self.n_splits):
                yield idx, idx

    cv = CV(n_splits=5, shuffle=True, random_state=SEED)
    search = RandomizedSearchCV(
        estimator=model,
        param_distributions=distr,
        n_iter=10,
        scoring=scorer,
        random_state=SEED,
        cv=cv,
        n_jobs=8
    )
    search.fit(data['train'])
    return search.best_params_



def train(size_type):
    data = prepare_dataset(size_type)

    hyperparams = cv_sklearn_hyperparameter_tuning(data)
    print(hyperparams)
    # hyperparams = {'learning_rate': 0.18410595411209124, 'loss': 'bpr', 'no_components': 21}
    model = train_model(data,hyperparams)
    # print(data['train'])
    performance_metrics = evaluate_model(model,data)
    print(performance_metrics)
    return performance_metrics

if __name__ == "__main__":
    
    size_types = ['ml-latest','ml-latest-small']
    performance_metrics = {}
    for size_type in size_types:
        start_time = time.time()
        performance_metrics[size_type] = train(size_type)
        print("Lightfm Dataset Size: {}, Time: {} seconds".format(size_type, (time.time() - start_time)))
    
    nested_dict_to_csv(performance_metrics,['Dataset','Metric Name','EvaluationSet','Value'],'lightfm')
    
    