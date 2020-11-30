"""
Tested with:
Python 3.7.7
scikit-learn==0.24.2
"""
import json
import joblib

from sklearn import svm
from sklearn import datasets

classes = {"0": "Setosa", "1": "Versicolour", "2": "Virginica" }

clf = svm.SVC(gamma='scale', probability=True)
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)

###
# Export / Store
###

joblib.dump(clf, open("model.joblib", "wb"))
with open("classes.json", "w") as f:
    f.write(json.dumps(classes))
