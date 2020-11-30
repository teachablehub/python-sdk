"""
Tested with:
Python 3.7.7
scikit-learn==0.24.2
"""

###
# Requirements
# 1. First you need to create a teachable here: https://app.teachablehub.com/create
# 2. Create Deploy and Serving keys
# https://app.teachablehub.com/<user>/<teachable>/settings/deploy-keys
# https://app.teachablehub.com/<user>/<teachable>/settings/serving-keys
###

# training packages
from sklearn import svm
from sklearn import datasets

# deployment packages
from teachablehub.deployments.sklearn import TeachableDeployment
from teachablehub.clients import TeachableHubPredictAPI

# environment info
import platform
from sklearn import __version__ as sklearn_version

###
# Training
###

clf = svm.SVC(gamma='scale', probability=True)
iris = datasets.load_iris()
X, y = iris.data, iris.target
clf.fit(X, y)

###
# Deployment
###

deployment = TeachableDeployment(
    teachable="user/teachable",
    environment="production",
    deploy_key="your-deploy-key-here",
)

deployment.model(clf)

# The API will use these classes in the predictions
deployment.classes({"0": "Setosa", "1": "Versicolour", "2": "Virginica" })

# HTTP Request schema + validation
deployment.schema({
    "features": {
        "sepal_length": {"type": "float"},
        "sepal_width": {"type": "float"},
        "petal_length": {"type": "float"},
        "petal_width": {"type": "float"},
    },
    "ndarray": [[
        "sepal_length",
        "sepal_width",
        "petal_length",
        "petal_width",
    ]]
})

# Deployment validations and tests.
# Better documentation examples. Model Validation after deployment, Predictman examples.
deployment.samples(
    ndarray=[X[0]],
    features={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2 }
)

# Easly tracking of changes, version of the training data or environment where the deployment was made.
deployment.context({
    "branch": "dev",
    "commit": "9e91a9d16eecf9e44935788ea777549de4377408",
    "dataset_version": "777549de4377408",
    "training_params": {},
    "scikit-learn": sklearn_version,
    "python": platform.python_version(),
    "local_hostname": platform.node(),
    "os_info": platform.version()
})

deployment.deploy(
    summary="Automatic deployment from {}".format(platform.node())
)

deployment.activate()

print("v{} successfuly deployed.".format(deployment.version()))

# ###
# # Predict
# ###

teachable = TeachableHubPredictAPI(
    teachable="user/teachable",
    environment="production",
    serving_key="your-serving-key-here"
)

# predict with ndarray
# predictions = teachable.predict([[0.1,0.2,0.3,0.4]])

# predict with features
predictions = teachable.predict({
        "sepal_length": 0.1,
        "sepal_width": 0.2,
        "petal_length": 0.3,
        "petal_width": 0.4,
    })

print(predictions)

"""
Result:

[{
  "className": "Setosa",
  "probability": 0.97862075
}, {
  "className": "Versicolour",
  "probability": 0.01342416
}, {
  "className": "Virginica",
  "probability": 0.00795509
}]
"""
