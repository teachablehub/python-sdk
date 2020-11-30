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

# HTTP Request schema + validation + help sections
"""
Important this example only demonstrates the advanced use of the Schema Validation
the explained requirements are based on the information from:
 - https://scikit-learn.org/stable/datasets/toy_dataset.html#diabetes-dataset
 - https://www4.stat.ncsu.edu/~boos/var.select/diabetes.tab.txt

 The actual predictions with the current toy data set probably wont be correct.
"""
deployment.schema({
    "features": {
        "age": {
            "type": "integer",
            "max": 120,
            "min": 1,
            "help": "age in years",
        },
        "sex": {
            "type": "integer",
            "allowed": [1, 2],
            "help": "sex as integer, 1 for Male and 2 for Femail.",
        },
        "bmi": {
            "type": "float",
            "max": 50,
            "min": 0,
            "help": "body mass index",
        },
        "bp":  {
            "type": "number",
            "max": 180.0,
            "min": 30.0,
            "help": "average blood pressure",
        },
        "s1":  {
            "type": "integer",
            "max": 300,
            "min": 0,
            "help": "tc, total serum cholesterol",
        },
        "s2":  {
            "type": "float",
            "max": 250,
            "min": 0,
            "help": "ldl, low-density lipoproteins",
        },
        "s3":  {
            "type": "integer",
            "max": 100,
            "min": 30,
            "help": "hdl, high-density lipoproteins",
        },
        "s4":  {
            "type": "float",
            "max": 10,
            "min": 1,
            "help": "tch, total cholesterol / HDL",
        },
        "s5":  {
            "type": "float",
            "max": 6.0,
            "min": 4.0,
            "help": "ltg, possibly log of serum triglycerides level",
        },
        "s6":  {
            "type": "number",
            "max": 150,
            "min": 0,
            "help": "glu, blood sugar level",
        },

    },
    "ndarray": [["age", "sex", "bmi", "bp", "s1", "s2", "s3", "s4", "s5", "s6"]]
})

deployment.samples(
    ndarray=[[59, 2, 32.1, 101, 157, 93.2, 38, 4, 4.8598, 87]],
    features={
        "age": 59,
        "sex": 2,
        "bmi": 32.1,
        "bp": 101,
        "s1": 157,
        "s2": 93.2,
        "s3": 38,
        "s4": 4,
        "s5": 4.8598,
        "s6": 87
    }
)

deployment.deploy(
    summary="Automatic deployment from {}".format(platform.node()),
    activate=True
)

print("v{} successfuly deployed.".format(deployment.version()))
