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
deployment.samples(ndarray=[X[0]])
deployment.deploy(
    summary="Automatic deployment from sklearn-deploy.py",
    activate=True
)

print("v{} successfuly deployed.".format(deployment.version()))
