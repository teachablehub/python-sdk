from .base import BaseDeployment

from zipfile import ZipFile, ZIP_DEFLATED
from os import makedirs

class TeachableDeployment(BaseDeployment):
    framework = 'ludwig'

    def model(self, model):

        tmp_path = self._unique_tmp_dir_path()
        makedirs(tmp_path)
        exported_model_path = "{}/".format(tmp_path)
        zip_path = "{}/{}.zip".format(self._tmp_dir(), self._unique_name())
        model.save(exported_model_path)

        with ZipFile(zip_path, 'w', ZIP_DEFLATED, allowZip64=True) as zip:
            self._add_zip_dir(zip, exported_model_path)

        self._model_zip_path = zip_path
        self._should_delete(tmp_path)

        types_map = {
            "category": "string",
            "numerical": "number",
            "text": "string",
            "binary": "int",
            "date": "date",
        }

        if self._auto_schema:
            _schema = {"features": {}, "ndarray": None}
            for f in model.model_definition['input_features']:
                _schema['features'][f['name']] = {"type": types_map.get(f['type'], "string")}
            self.schema(_schema)

        self.classes({"0": "unknown"})
