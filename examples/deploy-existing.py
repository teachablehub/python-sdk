"""
Tested with:
Python 3.7.7
scikit-learn==0.21.3
"""
###
# Requirements
# 1. First you need to create a teachable here: https://app.teachablehub.com/create
# 2. Create Deploy and Serving keys
# https://app.teachablehub.com/<user>/<teachable>/settings/deploy-keys
# https://app.teachablehub.com/<user>/<teachable>/settings/serving-keys
###

import json
import joblib

# deployment packages
from teachablehub.deployments.sklearn import TeachableDeployment

# environment info
from sklearn import __version__ as sklearn_version
from platform import python_version

###
# Load the existing model and classes
###

clf = joblib.load('./existing_models/sklearn_iris/model.joblib')
classes = json.loads(open('./existing_models/sklearn_iris/classes.json','r').read())

###
# Deployment
###

deployment = TeachableDeployment(
    teachable="user/teachable",
    environment="production",
    deploy_key="your-deploy-key-here",
)

deployment.model(clf)
deployment.classes(classes)

deployment.samples(
    ndarray=[[5.1, 3.5, 1.4, 0.2]],
    features={"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2 }
)

deployment.context({
    "python": python_version(),
    "scikit-learn": sklearn_version,
})

deployment.deploy(
    summary="Initial deploy.",
    description="Deployment of existing sklearn model to TeachableHub.",
    activate=True
)
