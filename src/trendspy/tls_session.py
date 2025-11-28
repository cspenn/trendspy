"""
TLS Impersonation Session Wrapper

This module provides a wrapper around curl_cffi to impersonate real browser
TLS fingerprints. This is critical for avoiding Google's TLS-level blocking.

The standard Python 'requests' library creates a distinctive JA3 fingerprint
that Google can detect and block BEFORE processing HTTP requests, resulting in:
- Empty response headers
- 8+ second timeouts
- Connection-level rejections

By using curl_cffi with browser impersonation, we match real Chrome/Firefox
TLS fingerprints, which dramatically reduces blocking.
"""

import logging
from typing import Any, Union
import requests

try:
    from curl_cffi import requests as curl_requests
    from curl_cffi.requests import Session as CurlSession

    CURL_CFFI_AVAILABLE = True
except ImportError:
    CURL_CFFI_AVAILABLE = False
    curl_requests = None  # type: ignore
    CurlSession = None  # type: ignore

logger = logging.getLogger(__name__)


class TLSImpersonationSession:
    """
    Session that impersonates real browser TLS fingerprints using curl_cffi.

    This wrapper provides get() and post() methods compatible with the
    requests.Session interface, but uses curl_cffi's browser impersonation
    to avoid TLS fingerprint detection.

    Supported browsers:
    - chrome131 (recommended - November 2025)
    - chrome130
    - firefox132
    - safari18
    - edge131

    If curl_cffi is not available, falls back to standard requests library
    with a warning.
    """

    def __init__(self, browser: str = "chrome131"):
        """
        Initialize TLS impersonation session.

        Args:
            browser: Browser to impersonate. Options: chrome131, chrome130,
                    firefox132, safari18, edge131. Default: chrome131
        """
        self.browser = browser

        if not CURL_CFFI_AVAILABLE:
            logger.warning(
                "curl_cffi not available. Falling back to standard requests. "
                "Install with: pip install curl-cffi>=0.7.0"
            )
            self.session: Union[requests.Session, Any] = requests.Session()
            self._using_curl_cffi = False
        else:
            logger.info(f"Creating TLS impersonation session (browser={browser})")
            self.session = curl_requests.Session()  # type: ignore
            self._using_curl_cffi = True

        # Store headers separately (compatible with both session types)
        self.headers: dict = {}

        # Initialize proxies attribute (compatible with requests.Session interface)
        self.proxies: dict = {}

    def get(self, url: str, **kwargs) -> Any:
        """
        Perform GET request with TLS impersonation.

        Args:
            url: URL to request
            **kwargs: Additional arguments passed to session.get()

        Returns:
            Response object
        """
        # Merge instance headers with any passed headers
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"].update(self.headers)

        if self._using_curl_cffi:
            return self.session.get(url, impersonate=self.browser, **kwargs)  # type: ignore
        else:
            return self.session.get(url, **kwargs)

    def post(self, url: str, **kwargs) -> Any:
        """
        Perform POST request with TLS impersonation.

        Args:
            url: URL to request
            **kwargs: Additional arguments passed to session.post()

        Returns:
            Response object
        """
        # Merge instance headers with any passed headers
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"].update(self.headers)

        if self._using_curl_cffi:
            return self.session.post(url, impersonate=self.browser, **kwargs)  # type: ignore
        else:
            return self.session.post(url, **kwargs)

    @property
    def cookies(self):
        """Access session cookies (compatible with both session types)."""
        return self.session.cookies

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, *args):
        """Context manager exit."""
        self.close()
