"""
Tested with:
Python 3.7.7
scikit-learn==0.24.2

https://scikit-learn.org/0.23/auto_examples/feature_selection/plot_select_from_model_diabetes.html
"""

import joblib

from sklearn.linear_model import LinearRegression
from sklearn import datasets
from sklearn.model_selection import train_test_split


diabetes = datasets.load_diabetes() # load data
X_train, X_test, y_train, y_test = train_test_split(diabetes.data, diabetes.target, test_size=0.2, random_state=0)

model = LinearRegression()
model.fit(X_train, y_train)

print("Model Score:", model.score(X_test, y_test))

###
# Export / Store
###

joblib.dump(model, open("model.joblib", "wb"))
