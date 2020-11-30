from teachablehub import config
from uplink import (
    post,
    retry,
    args,
    Query,
    Body,
    json,
    response_handler
)
from .base import BaseTeachableHubConsumer, raise_for_status
from .errors import MissingTeachableError

import numpy as np
from json import loads, dumps, JSONEncoder

class NumpyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

@retry(
    # Retry on 503 response status code or any exception.
    when=retry.when.status(503) | retry.when.raises(Exception),
    # Stop after 10 attempts or when backoff exceeds 30 seconds.
    stop=retry.stop.after_attempt(10) | retry.stop.after_delay(30),
    # Use exponential backoff with added randomness.
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@response_handler(raise_for_status)
class TeachableHubPredictAPI(BaseTeachableHubConsumer):
    def __init__(self, serving_key=None, **kwargs):

        base_url = kwargs.get('base_url', config.serving_base_url)

        teachable = kwargs.get('teachable', None)
        if teachable is None:
            raise MissingTeachableError

        self._base_url = "{}/{}/".format(base_url, teachable)

        self._serving_key = config.serving_key
        if serving_key:
            self._serving_key = serving_key

        self._environment = kwargs.get('environment', 'production')
        self._version = kwargs.get('version', None)


        super(TeachableHubPredictAPI, self).__init__(base_url=self._base_url, serving_key=self._serving_key)

    @json
    @args(Body, Query, Query, Query, Query, Query,)
    @post("predict/")
    def request_cloud_prediction(self, payload, environment, version, order, limit, threshold):
        """Get all public teachables"""

    def predict(self, ndarray_or_features, **kwargs):
        payload = {}
        if isinstance(ndarray_or_features, list) or isinstance(ndarray_or_features, np.ndarray):
            # ndarray prediction
            payload['ndarray'] = loads(dumps(ndarray_or_features, cls=NumpyEncoder))
        elif type(ndarray_or_features) is dict:
            # features
            payload['features'] = [ndarray_or_features]
        else:
            raise NotImplementedError

        order = kwargs.get('order', 'desc')
        limit = kwargs.get('limit', -1)
        threshold = kwargs.get('threshold', 0.0)

        payload['context'] = kwargs.get('context', None)


        r = self.request_cloud_prediction(payload, self._environment, self._version, order, limit, threshold)
        return r.json()['predictions']

