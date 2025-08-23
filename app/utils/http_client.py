from typing import Any, Dict, Optional

import requests

from app.utils.exceptions import (
    AppException,
    RequestConnectionError,
    RequestHTTPError,
    RequestTimeoutError,
)


def make_request(
    method: str,
    url: str,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    """
    Generic HTTP request utility.
    """
    try:
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    except requests.Timeout as exc:
        raise RequestTimeoutError(
            "The request timed out", context={"url": url}
        ) from exc

    except requests.ConnectionError as exc:
        raise RequestConnectionError(
            "Failed to connect to the service", context={"url": url}
        ) from exc

    except requests.HTTPError as exc:
        status_code = exc.response.status_code if exc.response else 500
        message = exc.response.text if exc.response else str(exc)
        raise RequestHTTPError(
            detail=message, status_code=status_code, context={"url": url}
        ) from exc

    except Exception as exc:
        # Catch-all wrapped in your base AppException
        raise AppException(
            "Unexpected error in HTTP request",
            code="unexpected_request_error",
            context={"url": url, "error": str(exc)},
        ) from exc
