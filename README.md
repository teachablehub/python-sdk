# About

Deployment, Prediction, and Management API interactions of TeachableHub Machine-Learning Deployment Platform via Python.

# Usage

## Deploy a model

You can integrate this SDK in your training logic, Jupyter notebook during experimentation, or your CI/CD system during the production environment. This SDK is also applicable for deploying existing models from your model registry or storage.

```python
from teachablehub.deployments.sklearn import TeachableDeployment

# ... training logic here ...

deployment = TeachableDeployment(
    teachable="user/teachable",
    environment="production",
    deploy_key="your-deploy-key-here",
)

deployment.model(clf)
deployment.deploy(
    summary="Automatic deployment from our CI via sklearn-deploy.py",
    activate=True
)
```

### Other deployment examples
We have prepared a couple of simple and advanced examples to show you some standard ways to integrate the TeachableHub platform very easily inside your training process. Also, there are ideas on how you can deploy your already trained and stored models to TeachableHub.

In the advanced examples, you will find some excellent tips and tricks on sharing knowledge between the training environment and the deployments via the Context API or creating and enforcing Features Schema with Validation to make your Model Serving API more understandable and secure.

Take a look at the examples here:

- [Ludwig example](https://github.com/teachablehub/python-sdk/blob/master/examples/ludwig-train-deploy.py)
- [Deploy existing model example](https://github.com/teachablehub/python-sdk/blob/master/examples/deploy-existing.py)
- [Deploy advanced example](https://github.com/teachablehub/python-sdk/blob/master/examples/sklearn-train-deploy-advanced.py)
- [Sklearn Regression Advanced Example](https://github.com/teachablehub/python-sdk/blob/master/examples/sklearn-train-deploy-regression-advanced.py)

## Make predictions

### Simple ndarray predictions

```python
from teachablehub.clients import TeachableHubPredictAPI

teachable = TeachableHubPredictAPI(
    teachable="user/teachable",
    environment="production",
    serving_key="your-serving-key-here"
)

predictions = teachable.predict([[0.03, 0.05, -0.002, -0.01, 0.04, 0.01, 0.08, -0.04, 0.005, -0.1]])
print(predictions)
````

### Advanced predictions with Features Validation

```python
from teachablehub.clients import TeachableHubPredictAPI

teachable = TeachableHubPredictAPI(
    teachable="user/teachable",
    environment="production",
    serving_key="your-serving-key-here"
)

features = {
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
}

predictions = teachable.predict(features, order='desc', limit=10, threshold=0.5)
print(predictions)
````

# Supported Tools & Frameworks

- [Uber's Luwdig](https://github.com/ludwig-ai/ludwig) - Ludwig is a toolbox on top of TensorFlow that allows to train and evaluate deep learning models without the need to write code.
- [scikit-learn](https://scikit-learn.org/stable/) - Machine Learning in Python
- [Google's Teachablemachine](https://teachablemachine.withgoogle.com/) Image Classification


# Requirements

- Python 3.7.7+ (probably could work with Python 3.4+ as well.)
- Create a teachable here: `https://app.teachablehub.com/create`
- Create a deploy key here: `https://app.teachablehub.com/<user>/<teachable>/settings/deploy-keys`
- Create a Serving key here: `https://app.teachablehub.com/<user>/<teachable>/settings/serving-keys`

# Installation

from source

```sh
git clone https://github.com/teachablehub/python-sdk.git
cd python-sdk
python setup.py install
```


with pip

```sh
pip install teachablehub
```

# Contributing

Thanks for looking at this section. We're open to any cool ideas, so if you have one and are willing to share - fork the repo, apply changes and open a pull request. :)

# Copyright

Copyright (c) 2021 CloudStrap AD. See LICENSE for further details.
