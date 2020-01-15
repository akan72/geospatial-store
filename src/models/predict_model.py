from sklearn.linear_model import LinearRegression
import seaborn as sns
import pandas as pd

iris = sns.load_dataset('iris')

X = iris.petal_width.as_matrix(columns=None).reshape(-1, 1)

lm = LinearRegression()
model = lm.fit(X, iris.petal_length)

def predict_length(petal_width: int=0):
    return lm.predict(pd.DataFrame({'petal_width':[petal_width]}))