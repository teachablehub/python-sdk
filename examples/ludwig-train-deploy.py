"""
Tested with:
Python 3.7.7
ludwig==0.2.2.8
tensorflow==1.15.3
"""

###
# Requirements
# 1. First you need to create a teachable here: https://app.teachablehub.com/create
# 2. Create Deploy and Serving keys
# https://app.teachablehub.com/<user>/<teachable>/settings/deploy-keys
# https://app.teachablehub.com/<user>/<teachable>/settings/serving-keys
###

# training packages
from ludwig.api import LudwigModel

# deployment packages
from teachablehub.deployments.ludwig import TeachableDeployment
from teachablehub.clients import TeachableHubPredictAPI

# environment info
import platform
from ludwig.globals import LUDWIG_VERSION

###
# Training
###

"""
  If you have an existing model, you don't need to train every time
  when you want to do a deployment

  ludwig_model = LudwigModel.load("./existing_models/ludwig_bbc_text")
"""

ludwig_config = {
  "input_features": [
    {
      "name": "text",
      "type": "text",
      "level": "word",
      "representation": "sparse",
      "encoder": "embed",
      "preprocessing": {
        "lowercase": True,
        "word_most_common": 1000,
        "word_format": "lemmatize_filter"
      }
    }
  ],
  "training": {
    "epochs": 50
  },
  "output_features": [
    {
      "type": "category",
      "name": "category"
    }
  ]
}

ludwig_model = LudwigModel(ludwig_config)

dataset_path = "./examples_data/ludwig/bbc-text.csv"
train_stats, _, _  = ludwig_model.train(data_csv=dataset_path)

###
# Deployment
###

deployment = TeachableDeployment(
    teachable="user/teachable",
    environment="production",
    deploy_key="your-deploy-key-here",
)

deployment.model(ludwig_model)

deployment.samples(
    features={
      "text": "wilkinson fit to face edinburgh england captain jonny wilkinson will make his long-awaited return from injury against edinburgh on saturday.  wilkinson  who has not played since injuring his bicep on 17 october  took part in full-contact training with newcastle falcons on wednesday. and the 25-year-old fly-half will start saturday s heineken cup match at murrayfield on the bench. but newcastle director of rugby rob andrew said:  he s fine and we hope to get him into the game at some stage.  the 25-year-old missed england s autumn internationals after aggravating the haematoma in his upper right arm against saracens. he was subsequently replaced as england captain by full-back jason robinson. sale s charlie hodgson took over the number 10 shirt in the internationals against canada  south africa and australia. wilkinson s year has been disrupted by injury as his muscle problem followed eight months on the sidelines with a shoulder injury sustained in the world cup final."
    }
)

deployment.context({
    "branch": "main",
    "commit": "9e91a9d16eecf9e44935788ea777549de4377408",
    "dataset_path": dataset_path,
    "ludwig": LUDWIG_VERSION,
    "python": platform.python_version(),
    "local_hostname": platform.node(),
    "os_info": platform.version()

})

deployment.deploy(
    summary="Initial ludwig deployment",
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

predictions = teachable.predict({
    "text": "wilkinson fit to face edinburgh england captain jonny wilkinson will make his long-awaited return from injury against edinburgh on saturday.  wilkinson  who has not played since injuring his bicep on 17 october  took part in full-contact training with newcastle falcons on wednesday. and the 25-year-old fly-half will start saturday s heineken cup match at murrayfield on the bench. but newcastle director of rugby rob andrew said:  he s fine and we hope to get him into the game at some stage.  the 25-year-old missed england s autumn internationals after aggravating the haematoma in his upper right arm against saracens. he was subsequently replaced as england captain by full-back jason robinson. sale s charlie hodgson took over the number 10 shirt in the internationals against canada  south africa and australia. wilkinson s year has been disrupted by injury as his muscle problem followed eight months on the sidelines with a shoulder injury sustained in the world cup final."
})

print(predictions)

"""
Result:

[
    {
      "className": "sport",
      "probability": 0.8740168809890747
    },
    {
      "className": "entertainment",
      "probability": 0.05120284482836723
    },
    {
      "className": "politics",
      "probability": 0.030961833894252777
    },
    {
      "className": "business",
      "probability": 0.030350320041179657
    },
    {
      "className": "tech",
      "probability": 0.012785467319190502
    },
    {
      "className": "unknown",
      "probability": 0.000682628364302218
    }
]
"""
