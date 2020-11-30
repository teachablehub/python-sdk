import os

# Base
base_url = os.environ.get('TH_BASE_URL','https://api.teachablehub.com/v1/')
serving_base_url = os.environ.get('TH_SERVING_BASE_URL','https://serve.teachablehub.com/v1/')

# Auth
api_key = os.environ.get('TH_API_KEY', None)
deploy_key = os.environ.get('TH_DEPLOY_KEY', None)
user_token = os.environ.get('TH_USER_TOKEN', None)
serving_key = os.environ.get('TH_SERVING_KEY', None)

# Env
teachable = os.environ.get('TH_TEACHABLE', None)
environment = os.environ.get('TH_ENVIRONMENT', "production")
