"""
Tested with:
Python 3.7.7
scikit-learn==0.24.2

https://scikit-learn.org/0.23/auto_examples/feature_selection/plot_select_from_model_diabetes.html
"""

###
# Requirements
# 1. First you need to create a teachable here: https://app.teachablehub.com/create
# 2. Create Deploy and Serving keys
# https://app.teachablehub.com/<user>/<teachable>/settings/deploy-keys
# https://app.teachablehub.com/<user>/<teachable>/settings/serving-keys
###

# training packages
from sklearn.linear_model import LinearRegression
from sklearn import datasets
from sklearn.model_selection import train_test_split

# deployment packages
from teachablehub.deployments.sklearn import TeachableDeployment
from teachablehub.clients import TeachableHubPredictAPI

# environment info
import platform
from sklearn import __version__ as sklearn_version

###
# Training
###

diabetes = datasets.load_diabetes() # load data
X_train, X_test, y_train, y_test = train_test_split(diabetes.data, diabetes.target, test_size=0.2, random_state=0)

model = LinearRegression()
model.fit(X_train, y_train)

###
# Deployment
###

deployment = TeachableDeployment(
    teachable="user/teachable",
    environment="production",
    deploy_key="your-deploy-key-here",
)

deployment.model(model)

# HTTP Request schema + validation
deployment.schema({
    "features": {
        "age": {"type": "float", "max": 0.1, "min": -0.1},
        "sex": {"type": "float", "max": 0.1, "min": -0.1},
        "bmi": {"type": "float", "max": 0.1, "min": -0.1},
        "bp":  {"type": "float", "max": 0.1, "min": -0.1},
        "s1":  {
            "type": "float",
            "max": 0.1,
            "min": -0.1,
            "help": "What is this feature about, where we can get it. how to prepare it, how to generate it?",
        },
        "s2":  {"type": "float", "max": 0.1, "min": -0.1},
        "s3":  {"type": "float", "max": 0.1, "min": -0.1},
        "s4":  {"type": "float", "max": 0.1, "min": -0.1},
        "s5":  {"type": "float", "max": 0.1, "min": -0.1},
        "s6":  {"type": "float", "max": 0.1, "min": -0.1},

    },
    "ndarray": [["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]]
})

deployment.samples(
    ndarray=X_train[0],
    features={
        "age": 0.01264814,
        "sex": 0.05068012,
        "bmi": 0.00241654,
        "bp": 0.05630106,
        "s1": 0.02732605,
        "s2": 0.01716188,
        "s3": 0.04127682,
        "s4": -0.03949338,
        "s5": 0.00371174,
        "s6": 0.07348023
    }
)

deployment.context({
    "script": "deploy-regression-advanced.py",
    "scikit-learn": sklearn_version,
    "python": platform.python_version(),
    "local_hostname": platform.node(),
    "os_info": platform.version()
})

deployment.deploy(
    summary="Automatic deployment from {}".format(platform.node()),
    activate=True
)

print("v{} successfuly deployed.".format(deployment.version()))

###
# Predict
###

teachable = TeachableHubPredictAPI(
    teachable="user/teachable",
    environment="production",
    serving_key="your-serving-key-here"
)

# predict with ndarray
# predictions = teachable.predict([[0.03, 0.05, -0.002, -0.01, 0.04, 0.01, 0.08, -0.04, 0.005, -0.1]])

# predict with features
predictions = teachable.predict({
        "age": 0.03,
        "sex": 0.05,
        "bmi": -0.002,
        "bp": -0.01,
        "s1": 0.04,
        "s2": 0.01,
        "s3": 0.08,
        "s4": -0.04,
        "s5": 0.005,
        "s6": -0.1
    })

print(predictions)

"""
Result:
[
    106.38885834176024
]

"""
