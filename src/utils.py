import numpy as np
import itertools
from datetime import datetime
from lightfm import LightFM
from scipy.sparse import coo_matrix
import pickle


def sample_hyperparameters():
    """
    Yield possible hyperparameter choices.
    """

    while True:
        yield {
            "no_components": np.random.randint(16, 64),
            "learning_schedule": np.random.choice(["adagrad", "adadelta"]),
            "loss": np.random.choice(["bpr", "warp", "warp-kos"]),
            "learning_rate": np.random.exponential(0.05),
            "num_epochs": np.random.randint(5, 30),
        }


def random_search(train, correct: dict, num_samples: int = 20, num_threads: int = -1):
    """
    Sample random hyperparameters, fit a LightFM model, and evaluate it
    on the test set.

    Parameters
    ----------

    train: np.float32 coo_matrix
        Training data.
    correct: dict
        dict with keys as item and val is max score 
    num_samples: int, optional
        Number of hyperparameter choices to evaluate.


    Returns
    ----------

    generator of (auc_score, hyperparameter dict, fitted model)

    """
    best_score = -1
    best_params = {}
    for hyperparams in itertools.islice(sample_hyperparameters(), num_samples):
        start = datetime.now()
        print('hyperparams set:', hyperparams)
        num_epochs = hyperparams.pop("num_epochs")

        model = LightFM(**hyperparams)
        model.fit(train, epochs=num_epochs, num_threads=num_threads)

        recoms = {}
        num_to_recom = 100
        for user in users_to_predict:
            predict = model.predict(
                user, items_to_predict, num_threads=num_threads)
            top_recoms_id = sorted(range(len(predict)),
                                   key=lambda i: predict[i])[-num_to_recom:]
            top_recoms_id.reverse()
            recoms[user_decode[user]] = [item_decode[items_to_predict[i]]
                                         for i in top_recoms_id]

        score = mDCG(correct, recoms)
        print(score)

        hyperparams["num_epochs"] = num_epochs

        end = datetime.now()

        yield (score, hyperparams, model, end - start)
        
        
def DCG(correct: dict, predictions: list):
    """
    Calculate DCG metric for user
    
    Parameters
    ----------

    correct: dict
        dict with keys as item and val is max score 
    predictions: list
        ordered list of recommended items


    Returns
    ----------

    score for user

    """
    score = 0
    intersec = set(correct.keys()).intersection(predictions)
    for i in intersec:
        score += correct[i] / np.log2(predictions.index(i) + 2)
    return score


def mDCG(correct: dict, predictions: dict):
    """
    Calculate mean DCG metric for user all users
    
    Parameters
    ----------

    correct: dict
        dict with keys as user and val as dict with items and scores
    predictions: dict
        dict with users and ordered list of recommended items


    Returns
    ----------

    score for user

    """
    total_sum = 0
    for user in correct:
        total_sum += DCG(correct[user], predictions[user])
    total_num = len(correct)
    return total_sum/total_num
  
        