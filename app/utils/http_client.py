from typing import Any, Dict, Optional

import requests


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
    Args:
        method: HTTP method (GET, POST, etc.)
        url: Full URL to request
        params: Query parameters
        data: Form data
        json: JSON body
        headers: HTTP headers
        timeout: Timeout in seconds
    Returns:
        Response JSON or error dict
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
    except requests.RequestException as e:
        return {"error": "Request failed", "details": str(e)}
