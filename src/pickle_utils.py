import pickle


def save_to_pickle(obj, path):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)
        
        
def read_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
