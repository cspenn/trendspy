"""
Enhanced session management with cookie persistence and browser-like headers.

Copyright (C) 2025 Trust Insights
Based on trendspy (MIT License) by sdil87

License: MIT
"""

import pickle
import logging
import random
import requests
import time
from pathlib import Path

from .tls_session import TLSImpersonationSession
from .browser_profiles import get_random_profile

logger = logging.getLogger(__name__)

# User-Agent pool with current browsers (November 2025)
# Phase 1.1: User-Agent Rotation for anti-detection
USER_AGENTS = [
    # Chrome 131 (November 2025 - CURRENT)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Chrome 130
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # Firefox 132
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    # Safari 18 (macOS only)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    # Edge 131
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
]


class SessionManager:
    """
    Manages HTTP sessions with cookie persistence and browser emulation.

    Features:
    - Persists cookies across runs
    - Browser-like headers to avoid detection
    - Automatic session refresh
    - Session save/load from disk

    Args:
        session_file: Path to session pickle file (default: .trendspy_session.pkl)
        persist_cookies: Whether to save/load cookies (default: True)
        use_tls_impersonation: Use curl_cffi for TLS fingerprint impersonation (default: True)
        tls_browser: Browser to impersonate (chrome131, chrome130, firefox132, etc.)

    Example:
        >>> manager = SessionManager()
        >>> session = manager.get_session()
        >>> # ... use session for requests ...
        >>> manager.save_session()  # Persist for next run
    """

    def __init__(
        self,
        session_file: str = ".trendspy_session.pkl",
        persist_cookies: bool = True,
        use_tls_impersonation: bool = True,
        tls_browser: str = "chrome131",
        use_browser_profiles: bool = True,
        session_warmup: bool = True,
    ):
        self.session_file = Path(session_file)
        self.persist_cookies = persist_cookies
        self.use_tls_impersonation = use_tls_impersonation
        self.tls_browser = tls_browser
        self.use_browser_profiles = use_browser_profiles
        self.session_warmup = session_warmup
        self.session = self._load_or_create_session()

        logger.info(
            f"SessionManager initialized "
            f"(persist_cookies={persist_cookies}, "
            f"use_tls_impersonation={use_tls_impersonation}, "
            f"tls_browser={tls_browser}, "
            f"use_browser_profiles={use_browser_profiles}, "
            f"session_warmup={session_warmup}, "
            f"file={session_file})"
        )

    def _load_or_create_session(self) -> requests.Session:
        """
        Load existing session from disk or create new one.

        Returns:
            requests.Session object
        """
        if self.persist_cookies and self.session_file.exists():
            try:
                with open(self.session_file, "rb") as f:
                    session = pickle.load(f)
                    logger.info(
                        f"Loaded existing session from {self.session_file} "
                        f"with {len(session.cookies)} cookies"
                    )
                    return session
            except Exception as e:
                logger.warning(
                    f"Failed to load session from {self.session_file}: {e}. "
                    f"Creating new session."
                )

        return self._create_session()

    def _create_session(self):
        """
        Create new session with browser-like headers.

        Headers mimic a real browser to avoid bot detection.
        Phase 1.1: Randomly selects User-Agent from pool for anti-fingerprinting.
        Phase 2: Uses TLS impersonation if enabled to avoid TLS fingerprinting.
        Phase 3: Uses coherent browser profiles if enabled.

        Returns:
            New session (either TLSImpersonationSession or requests.Session)
        """
        # Phase 2: Use TLS impersonation if enabled
        if self.use_tls_impersonation:
            session = TLSImpersonationSession(browser=self.tls_browser)
            logger.info(
                f"Created TLS impersonation session " f"(browser={self.tls_browser})"
            )
        else:
            session = requests.Session()
            logger.info("Created standard requests session")

        # Phase 3.1: Use coherent browser profiles if enabled
        if self.use_browser_profiles:
            # Get a random coherent profile (UA + all Client Hints)
            profile_headers = get_random_profile()

            # Base headers (same for all browsers)
            base_headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://trends.google.com/",
                "Origin": "https://trends.google.com",
                "DNT": "1",  # Do Not Track
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            }

            # Merge profile headers (includes UA and Client Hints) with base
            headers = {**base_headers, **profile_headers}

            ua_preview = headers.get("User-Agent", "Unknown")[:60]
            logger.info(f"Using coherent browser profile: {ua_preview}...")

        else:
            # Phase 1.1: Legacy - Randomly select User-Agent from pool
            selected_ua = random.choice(USER_AGENTS)

            # Browser-like headers (old method)
            headers = {
                "User-Agent": selected_ua,
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Referer": "https://trends.google.com/",
                "Origin": "https://trends.google.com",
                "DNT": "1",  # Do Not Track
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="131", "Google Chrome";v="131"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"macOS"',
            }

            logger.info(f"Using legacy UA rotation: {selected_ua[:50]}...")

        # Update headers (works for both TLSImpersonationSession and requests.Session)
        if hasattr(session, "headers"):
            if isinstance(session.headers, dict):
                session.headers.update(headers)
            else:
                session.headers = headers
        else:
            session.headers = headers

        return session

    def save_session(self) -> bool:
        """
        Persist current session to disk.

        Returns:
            True if saved successfully, False otherwise
        """
        if not self.persist_cookies:
            return False

        try:
            with open(self.session_file, "wb") as f:
                pickle.dump(self.session, f)

            logger.info(
                f"Saved session to {self.session_file} "
                f"({len(self.session.cookies)} cookies)"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to save session: {e}")
            return False

    def get_session(self) -> requests.Session:
        """
        Get current session object.

        Returns:
            requests.Session instance
        """
        return self.session

    def refresh_session(self) -> requests.Session:
        """
        Create fresh session (clears cookies and headers).

        Useful when switching IPs or after being blocked.

        Returns:
            New requests.Session instance
        """
        logger.info("Refreshing session (clearing cookies)")
        self.session = self._create_session()
        return self.session

    def clear_saved_session(self) -> bool:
        """
        Delete saved session file.

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if self.session_file.exists():
                self.session_file.unlink()
                logger.info(f"Deleted saved session file: {self.session_file}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete session file: {e}")
            return False

    def warmup_session(self) -> bool:
        """
        Phase 3.2: Warm up session with human-like browsing behavior.

        Visits Google Trends pages in a natural sequence before making API calls.
        This mimics real user behavior - no human jumps straight to API endpoints.

        Sequence:
        1. Visit homepage (random delay 0.5-1.5s)
        2. Visit explore page (random delay 1.0-2.5s)
        3. Visit trending searches (random delay 0.8-2.0s)

        Returns:
            True if warmup successful, False if errors occurred
        """
        if not self.session_warmup:
            logger.debug("Session warmup disabled, skipping")
            return True

        logger.info("Starting session warmup (human-like browsing)")

        try:
            # Step 1: Visit homepage
            delay = random.uniform(0.5, 1.5)
            logger.debug(f"Warmup step 1/3: Homepage (delay {delay:.2f}s)")
            time.sleep(delay)

            response1 = self.session.get("https://trends.google.com/trends/")
            logger.debug(f"Homepage response: {response1.status_code}")

            # Step 2: Visit explore page
            delay = random.uniform(1.0, 2.5)
            logger.debug(f"Warmup step 2/3: Explore page (delay {delay:.2f}s)")
            time.sleep(delay)

            response2 = self.session.get("https://trends.google.com/trends/explore")
            logger.debug(f"Explore response: {response2.status_code}")

            # Step 3: Visit trending searches
            delay = random.uniform(0.8, 2.0)
            logger.debug(f"Warmup step 3/3: Trending searches (delay {delay:.2f}s)")
            time.sleep(delay)

            response3 = self.session.get(
                "https://trends.google.com/trends/trendingsearches/daily?geo=US"
            )
            logger.debug(f"Trending response: {response3.status_code}")

            logger.info(
                f"Session warmup complete "
                f"(responses: {response1.status_code}, {response2.status_code}, {response3.status_code})"
            )
            return True

        except Exception as e:
            logger.warning(f"Session warmup failed (non-critical): {e}")
            # Don't fail - warmup is optional enhancement
            return False
