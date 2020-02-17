from sklearn.linear_model import LinearRegression
import seaborn as sns
import pandas as pd
import pickle

def train_iris_model():
    iris = sns.load_dataset('iris')

    X = iris.petal_width.as_matrix(columns=None).reshape(-1, 1)
    
    lm = LinearRegression()
    model = lm.fit(X, iris.petal_length)

    pickle.dump(model, open('models/iris_model.pkl', 'wb'))

def predict_length(petal_width: int=0)-> float:
    lm = pickle.load(open('models/iris_model.pkl', 'rb'))
    
    return lm.predict(pd.DataFrame({'petal_width':[petal_width]}))