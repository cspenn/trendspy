"""
Free Tor proxy rotation for IP diversity.

Copyright (C) 2025 Trust Insights

Provides free IP rotation using the Tor network.
Requires: tor installed (brew install tor on macOS)

License: MIT
"""

import logging
import time
import requests
from typing import Optional

try:
    from stem import Signal
    from stem.control import Controller

    STEM_AVAILABLE = True
except ImportError:
    STEM_AVAILABLE = False

logger = logging.getLogger(__name__)


class TorProxyRotator:
    """
    Rotate IP addresses using Tor network (FREE).

    Prerequisites:
        - Install Tor: brew install tor (macOS) or apt install tor (Linux)
        - Install stem: pip install stem
        - Start Tor: tor (or configure as service)

    Args:
        tor_port: Tor SOCKS5 proxy port (default: 9050)
        control_port: Tor control port (default: 9051)
        password: Tor control password (optional)

    Example:
        >>> tor = TorProxyRotator()
        >>> proxy_config = tor.get_proxy_config()
        >>>
        >>> # Use with requests
        >>> response = requests.get(url, proxies=proxy_config)
        >>>
        >>> # Rotate to new IP
        >>> tor.rotate_ip()
        >>> current_ip = tor.get_current_ip()
    """

    def __init__(
        self,
        tor_port: int = 9050,
        control_port: int = 9051,
        password: Optional[str] = None,
    ):
        if not STEM_AVAILABLE:
            raise ImportError(
                "stem library not installed. " "Install with: pip install stem"
            )

        self.tor_port = tor_port
        self.control_port = control_port
        self.password = password

        self.proxy_config = {
            "http": f"socks5://127.0.0.1:{tor_port}",
            "https": f"socks5://127.0.0.1:{tor_port}",
        }

        # Test connection
        self._test_connection()

        logger.info(
            f"TorProxyRotator initialized (port={tor_port}, "
            f"control_port={control_port})"
        )

    def _test_connection(self) -> None:
        """
        Test Tor connection.

        Raises:
            ConnectionError: If can't connect to Tor
        """
        try:
            # Try to get current IP
            ip = self.get_current_ip()
            if ip:
                logger.info(f"Tor connection successful. Current exit IP: {ip}")
            else:
                raise ConnectionError("Could not determine exit IP")
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to Tor proxy on port {self.tor_port}. "
                f"Make sure Tor is running. Error: {e}"
            )

    def rotate_ip(self) -> bool:
        """
        Request new Tor circuit (new exit IP).

        Returns:
            True if rotation successful, False otherwise
        """
        try:
            with Controller.from_port(port=self.control_port) as controller:
                # Authenticate
                if self.password:
                    controller.authenticate(password=self.password)
                else:
                    controller.authenticate()

                # Request new circuit
                controller.signal(Signal.NEWNYM)

                # Wait for new circuit
                wait_time = controller.get_newnym_wait()
                if wait_time > 0:
                    logger.debug(f"Waiting {wait_time}s for new Tor circuit")
                    time.sleep(wait_time)

                # Verify new IP
                new_ip = self.get_current_ip()
                logger.info(f"Rotated to new Tor exit IP: {new_ip}")

                return True

        except Exception as e:
            logger.error(f"Failed to rotate Tor IP: {e}")
            return False

    def get_current_ip(self) -> Optional[str]:
        """
        Get current Tor exit node IP address.

        Returns:
            IP address string or None if failed
        """
        try:
            response = requests.get(
                "https://api.ipify.org?format=text",
                proxies=self.proxy_config,
                timeout=10,
            )
            return response.text.strip()
        except Exception as e:
            logger.warning(f"Failed to get current IP: {e}")
            return None

    def get_proxy_config(self) -> dict:
        """
        Get proxy configuration for requests library.

        Returns:
            Dictionary with http/https proxy settings
        """
        return self.proxy_config

    def test_tor_connection(self) -> bool:
        """
        Test if Tor is working.

        Returns:
            True if Tor is accessible, False otherwise
        """
        try:
            ip = self.get_current_ip()
            return ip is not None
        except Exception:
            return False


# Convenience function
def create_tor_proxy(
    tor_port: int = 9050, control_port: int = 9051, password: Optional[str] = None
) -> Optional[TorProxyRotator]:
    """
    Create TorProxyRotator if Tor is available.

    Returns:
        TorProxyRotator instance or None if Tor not available
    """
    try:
        return TorProxyRotator(tor_port, control_port, password)
    except Exception as e:
        logger.warning(f"Tor not available: {e}")
        return None
