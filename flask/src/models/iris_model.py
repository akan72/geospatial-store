from sklearn.linear_model import LinearRegression
import seaborn as sns
import pandas as pd
import pickle

def train_iris_model(): 
    """ Trains our Iris Model. 

    Initial un-tuned function to train and serialize a Linear Regression
    model to predict petal_length given petal_width for the `Iris` dataset.
    Serialized models are stored in .pkl format within the `models` directory.

    """
    iris = sns.load_dataset('iris')

    X = iris.petal_width.as_matrix(columns=None).reshape(-1, 1)
    
    lm = LinearRegression()
    model = lm.fit(X, iris.petal_length)

    pickle.dump(model, open('models/iris_model.pkl', 'wb'))

def predict_length(petal_width: int=0)-> float:
    """ Predict petal_length given petal_width. 

    This function loads the serialized `Iris` petal_length prediction model,
    and then predicts the petal_length given the petal_width that is passed. 
    Used within views.py to servee the prediction results.

    Args:
        petal_width [int]: Petal length input by user
    
    Returns:
        float: Petal_length predicted by our linear model.

    """

    lm = pickle.load(open('models/iris_model.pkl', 'rb'))
    
    return lm.predict(pd.DataFrame({'petal_width': [petal_width]}))