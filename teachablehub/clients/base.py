# import http.client
# http.client.HTTPConnection.debuglevel = 1

from uplink import (
    Consumer,
    response_handler,
)

from uplink.auth import ApiTokenHeader

from teachablehub import config

from .errors import UnsuccessfulRequestError, UnauthorizedError, NoThAuthMethodError

def raise_for_status(response):
    """Checks whether or not the response was successful."""
    status_code = response.status_code

    if 200 <= status_code < 300:
        # Pass through the response.
        return response

    if status_code == 401:
        raise UnauthorizedError()

    # raise for all 4xx and 5xx
    if status_code >= 400:
        raise UnsuccessfulRequestError(status_code, response.text, "{} - {} - {}".format(status_code, response.url, response.text))

    return response

class BaseTeachableHubConsumer(Consumer):
    """A Python Client for the TeachbaleHub API."""

    def __init__(self, token=None, api_key=None, deploy_key=None, serving_key=None, **kwargs):
        # if not region or type(region) is not Region:
        #     raise ValueError("Invalid value supplied for Region.")

        base_url = kwargs.get('base_url', None)
        if not base_url:
            base_url = config.base_url

        self._base_url = base_url

        self._th_auth = None

        if kwargs.get('auth', None):
            self._th_auth = kwargs['auth']
        else:
            if token:
                self._th_auth = ApiTokenHeader("Authorization", "Token {}".format(token))

            if api_key:
                self._th_auth = ApiTokenHeader("Authorization", "Api-Key {}".format(api_key))

            if deploy_key:
                self._th_auth = ApiTokenHeader("Authorization", "Deploy-Key {}".format(deploy_key))

            if serving_key:
                self._th_auth = ApiTokenHeader("X-Serving-Key", serving_key)

        if self._th_auth is None:
            raise NoThAuthMethodError()

        super(BaseTeachableHubConsumer, self).__init__(base_url=base_url, auth=self._th_auth)

        self.session.headers["User-Agent"] = kwargs.get('user_agent', "th.py:{}".format('0.0.1'))
