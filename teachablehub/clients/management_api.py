from uplink import (
    Body,
    Part,
    Field,
    Query,
    args,
    get,
    post,
    multipart,
    returns,
    json,
    retry,
    response_handler
)

from .base import BaseTeachableHubConsumer, raise_for_status

@retry(
    # Retry on 503 response status code or any exception.
    when=retry.when.status(503) | retry.when.raises(Exception),
    # Stop after 10 attempts or when backoff exceeds 30 seconds.
    stop=retry.stop.after_attempt(10) | retry.stop.after_delay(30),
    # Use exponential backoff with added randomness.
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@response_handler(raise_for_status)
class TeachableConsumer(BaseTeachableHubConsumer):

    @returns.json
    @get("")
    def get_teachable(self):
        """get the teachable"""

    ## Deployments

    @multipart
    @returns.json
    @post("deployments/")
    def create_deployment(self, data: Body, model: Part):
       """create new deployment."""

    @returns.json
    @get("deployments/")
    def get_all_deployments(self):
       """get the deployment."""

    @returns.json
    @get("environments/")
    def get_all_environments(self):
       """get all the environments in this teachable."""

    @returns.json
    @get("deployments/{deployment_id}/")
    def get_deployment(self, deployment_id):
       """get the deployment."""

    @args(Query, Query)
    @get("deployments/")
    def get_deployment_by_env_and_version(self, environment, version):
       """get the deployment."""

    @args(Query, Query)
    @get("deployments/")
    def get_deployment_by_env_id_and_version(self, environment_id, version):
       """get the deployment."""

    @returns.json
    @post("deployments/{deployment_id}/activate/")
    def activate_deployment(self, deployment_id):
       """activate deployment."""

    @returns.json
    @post("deployments/{deployment_id}/rollback/")
    def rollback_deployment(self, deployment_id):
       """activate deployment."""

    @json
    @args(Field, Field)
    @post("deployments/rollback-version/")
    def rollback_deployment_version(self, environment, version):
       """activate deployment."""


@retry(
    # Retry on 503 response status code or any exception.
    when=retry.when.status(503) | retry.when.raises(Exception),
    # Stop after 10 attempts or when backoff exceeds 30 seconds.
    stop=retry.stop.after_attempt(10) | retry.stop.after_delay(30),
    # Use exponential backoff with added randomness.
    backoff=retry.backoff.jittered(multiplier=0.5)
)
@response_handler(raise_for_status)
class TeachableHubAPI(BaseTeachableHubConsumer):
    ## Users
    @returns.json
    @get("users/me/")
    def whoami(self):
        """Get my user."""

    @returns.json
    @get("users/me/teachables/")
    def get_user_teachables(self):
        """Get my teachables."""

    ## Teachables

    @returns.json
    @get("teachables/")
    def get_all_public_teachables(self):
        """Get all public teachables"""

    def teachable(self, teachable_full_name):
        """Get my teachables."""
        base_url = "{}teachables/{}/".format(self._base_url, teachable_full_name)

        instance = TeachableConsumer(
            base_url = base_url,
            auth = self._th_auth
        )
        return instance
