"""Utility functions for interacting with dapla-team-api."""
import logging
from typing import Any
from typing import Dict

import requests
from returns.result import Failure
from returns.result import Result
from returns.result import Success

from dapla_team_cli.auth.services.get_token import get_token


logger = logging.getLogger("dpteam")


def get_resource(
    endpoint: str,
) -> Result[Dict[str, Any], str]:
    """Get a given resource (Team/Group/User/a list) from the API."""
    token = get_token()

    try:
        response = requests.get(
            endpoint,
            headers={
                "Authorization": f"Bearer {token}",
            },
            timeout=10,
        )
    except requests.RequestException as e:
        logger.debug("exception thrown in get_resource accessing %s, exception: %s", endpoint, str(e))
        return Failure("Something went wrong trying to access the API")

    if response.status_code != 200:
        logger.debug(
            "get_resource got status code %s accessing %s | Reason: %s | Response body: %s",
            response.status_code,
            endpoint,
            response.reason,
            response.content.decode("utf-8"),
        )
        return Failure(f"Error trying to access {endpoint}: {response.status_code} {response.reason}")

    return Success(response.json())
