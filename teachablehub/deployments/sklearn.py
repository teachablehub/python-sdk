import th_sklearn_json as skljson

from zipfile import ZipFile, ZIP_DEFLATED
from os import makedirs

from .base import BaseDeployment

class TeachableDeployment(BaseDeployment):
    framework = 'sklearn'

    def model(self, model):
        tmp_path = self._unique_tmp_dir_path()
        makedirs(tmp_path)
        exported_model_path = "{}/model.json".format(tmp_path)
        zip_path = "{}/{}.zip".format(self._tmp_dir(), self._unique_name())
        skljson.to_json(model, exported_model_path)

        with ZipFile(zip_path, 'w', ZIP_DEFLATED, allowZip64=True) as zip:
            self._add_zip_file(zip, exported_model_path)

        self._model_zip_path = zip_path
        self._should_delete(tmp_path)

