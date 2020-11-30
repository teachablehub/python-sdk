import os
import json
import shutil
import tempfile
import random
import string
import numpy

from abc import ABC
from json import JSONEncoder


from teachablehub import config
from teachablehub.clients import TeachableHubAPI

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class NotDeployedModelError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class BaseDeployment(ABC):
    def __init__(self, teachable=None, environment=None, deploy_key=None, api_key=None, token=None, **kwargs):

        self.teachable = config.teachable
        if teachable:
            self.teachable = teachable

        self.owner, self.teachable_name = self.teachable.split('/')

        self.environment = config.environment
        if environment:
            self.environment = environment

        self._deploy_key = config.deploy_key
        if deploy_key:
            self._deploy_key = deploy_key

        self._api_key = config.api_key
        if api_key:
            self._api_key = api_key

        self._user_token = config.user_token
        if token:
            self._user_token = token

        base_url = kwargs.get('base_url', None)
        if not base_url:
            base_url = config.base_url

        auth_method = {}

        if self._deploy_key:
            auth_method['deploy_key'] = self._deploy_key
        elif self._api_key:
            auth_method['api_key'] = self._api_key
        else:
            auth_method['token'] = self._user_token

        self._th = TeachableHubAPI(
            base_url = base_url,
            **auth_method,
        )

        self._api = self._th.teachable(self.teachable)

        self._deployment_id = None
        self._paths_to_be_deleted = []
        self._archived_model_path = None

        self._environment_id = self._get_environment_id(environment)

        self._deployment_data = {
            "framework": self.framework,
            "environment": self._environment_id
        }

        version = kwargs.get('version', None)
        if version:
            self._version = int(version)
            self._retrieve_existing_deployment()

        # this is used where we can get the schema from the model
        # like in the ludwig for example
        self._auto_schema = True

    def _get_environment_id(self, environment_name):
        all_envs = self._api.get_all_environments()
        for env in all_envs:
            if env['name'] == environment_name:
                return env['id']

    def _retrieve_existing_deployment(self):
        r = self._api.get_deployment_by_env_id_and_version(self._environment_id, self._version)
        data = r.json()
        if len(data) == 1:
            self._deployment_data = data[0]
            self._deployment_id = data[0]['uuid']
            self._version = data[0]['version']
            return self._deployment_data
        else:
            raise AssertionError("The deployment with this version and environment should be only one.")
        return self._deployment_data

    def _unique_name(self):
        length = 16
        letters_and_digits = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
        return result_str

    def _unique_tmp_dir_path(self):
        tmp_dir = self._tmp_dir()
        unique_name = self._unique_name()
        return "{}/{}".format(tmp_dir, unique_name)

    def _tmp_dir(self):
        return tempfile.gettempdir()

    def _add_zip_dir(self, zip, path):
        """zipper"""
        for root, _, files in os.walk(path):
            for file_found in files:
                abs_path = root+'/'+file_found
                zip.write(abs_path, file_found)

    def _add_zip_file(self, zip, filename):
        dir, base_filename = os.path.split(filename)
        os.chdir(dir)
        zip.write(base_filename)

    def _should_delete(self, path):
        self._paths_to_be_deleted.append(path)

    def samples(self, ndarray=None, features=None):
        samples = None

        if not ndarray is None or not features is None:
            samples = {}
            if not ndarray is None:
                samples['ndarray'] = ndarray

            if not features is None:
                samples['features'] = features

        self._deployment_data['samples'] = json.dumps(samples, cls=NumpyArrayEncoder)
        return self

    def context(self, context):
        self._deployment_data['context'] = json.dumps(context)
        return self

    def classes(self, classes):
        self._deployment_data['classes'] = json.dumps(classes)
        return self

    def schema(self, schema):
        self._deployment_data['schema'] = json.dumps(schema)
        self._auto_schema = False
        return self

    def model(self, model):
        raise NotImplementedError(".model() must be overridden.")

    def deploy(self, summary, description=None, *args, **kwargs):
        model_fin = open(self._model_zip_path, 'rb')
        self._deployment_data['summary'] = summary

        if description:
            self._deployment_data['description'] = description

        activate = kwargs.get('activate', False)
        if activate:
            self._deployment_data['activate'] = True

        data = self._api.create_deployment(data = self._deployment_data, model=model_fin)
        if data.get('uuid', False):
            self._deployment_data = data
            self._deployment_id = data['uuid']
            self._version = data['version']

            for this_path in self._paths_to_be_deleted:
                shutil.rmtree(this_path)

        run_tests = kwargs.get('run_tests', False)
        if run_tests:
            raise NotImplementedError("Running tests during deployment will be implemented soon.")

        return self

    def successful(self):
        return bool(self._deployment_data.get('uuid', None))

    def reload(self):
        return self._retrieve_existing_deployment()

    def verified(self, reload=False):
        if reload:
            self.reload()
        return bool(self._deployment_data.get('status', {}).get('state') == "verified")

    def object(self):
        return self._deployment_data

    def activate(self):
        if self._deployment_id:
            return self._api.activate_deployment(self._deployment_id)
        else:
            raise NotDeployedModelError(message="Model should be deployed first, then can be activated.")

        return False

    def rollback(self, version):
        response = self._api.rollback_deployment_version(self._environment_id, int(version))
        if response.ok:
            data = response.json()
            self._deployment_data = data
            self._deployment_id = data['uuid']
            return data
        return False


    def version(self):
        return self._deployment_data.get('version', None)
