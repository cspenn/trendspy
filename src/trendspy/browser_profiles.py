"""
Browser Profiles for Anti-Detection

This module provides coherent browser profiles that ensure all headers
(User-Agent, Client Hints, etc.) are consistent and realistic.

Google analyzes header coherence - mismatches between User-Agent and
Client Hints (like Chrome 120 claiming to be on macOS 10.15.7, which
is impossible) are red flags for automation.

Each profile includes:
- User-Agent string
- All 7 Client Hint headers (Sec-CH-UA-*)
- Version consistency across all headers
- Realistic OS/architecture combinations
"""

import random
from typing import Dict

# Chrome 131 Profiles (November 2025 - CURRENT)
CHROME_131_MACOS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Sec-CH-UA": '"Chromium";v="131", "Not_A Brand";v="24", "Google Chrome";v="131"',
    "Sec-CH-UA-Platform": '"macOS"',
    "Sec-CH-UA-Platform-Version": '"14.2.0"',
    "Sec-CH-UA-Arch": '"arm64"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Bitness": '"64"',
    "Sec-CH-UA-Model": '""',
}

CHROME_131_WINDOWS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Sec-CH-UA": '"Chromium";v="131", "Not_A Brand";v="24", "Google Chrome";v="131"',
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-CH-UA-Platform-Version": '"15.0.0"',
    "Sec-CH-UA-Arch": '"x86"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Bitness": '"64"',
    "Sec-CH-UA-Model": '""',
}

# Chrome 130 Profiles (October 2025)
CHROME_130_MACOS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Sec-CH-UA": '"Chromium";v="130", "Not_A Brand";v="24", "Google Chrome";v="130"',
    "Sec-CH-UA-Platform": '"macOS"',
    "Sec-CH-UA-Platform-Version": '"14.1.0"',
    "Sec-CH-UA-Arch": '"arm64"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Bitness": '"64"',
    "Sec-CH-UA-Model": '""',
}

CHROME_130_WINDOWS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Sec-CH-UA": '"Chromium";v="130", "Not_A Brand";v="24", "Google Chrome";v="130"',
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-CH-UA-Platform-Version": '"15.0.0"',
    "Sec-CH-UA-Arch": '"x86"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Bitness": '"64"',
    "Sec-CH-UA-Model": '""',
}

# Firefox 132 Profiles (November 2025)
# Note: Firefox doesn't send Client Hints by default
FIREFOX_132_MACOS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
    # Firefox doesn't send Sec-CH-UA headers
}

FIREFOX_132_WINDOWS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    # Firefox doesn't send Sec-CH-UA headers
}

# Safari 18 Profile (macOS only)
# Note: Safari doesn't send Client Hints
SAFARI_18_MACOS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15",
    # Safari doesn't send Sec-CH-UA headers
}

# Edge 131 Profile (follows Chrome)
EDGE_131_WINDOWS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Sec-CH-UA": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-CH-UA-Platform-Version": '"15.0.0"',
    "Sec-CH-UA-Arch": '"x86"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Bitness": '"64"',
    "Sec-CH-UA-Model": '""',
}

# Aggregate all profiles
BROWSER_PROFILES = {
    "chrome131_macos": CHROME_131_MACOS,
    "chrome131_windows": CHROME_131_WINDOWS,
    "chrome130_macos": CHROME_130_MACOS,
    "chrome130_windows": CHROME_130_WINDOWS,
    "firefox132_macos": FIREFOX_132_MACOS,
    "firefox132_windows": FIREFOX_132_WINDOWS,
    "safari18_macos": SAFARI_18_MACOS,
    "edge131_windows": EDGE_131_WINDOWS,
}

# Weighted selection (prefer current browsers)
PROFILE_WEIGHTS = {
    "chrome131_macos": 25,  # Most common, current
    "chrome131_windows": 25,  # Most common, current
    "chrome130_macos": 15,  # Recent, still widely used
    "chrome130_windows": 15,  # Recent, still widely used
    "firefox132_macos": 5,  # Less common but realistic
    "firefox132_windows": 5,  # Less common but realistic
    "safari18_macos": 5,  # macOS only, less common
    "edge131_windows": 5,  # Less common but realistic
}


def get_random_profile() -> Dict[str, str]:
    """
    Get a random browser profile with weighted selection.

    Weights favor current Chrome versions (131) over older ones,
    and Chrome over Firefox/Safari/Edge (matching real-world distribution).

    Returns:
        Dict with User-Agent and Client Hints headers
    """
    profile_names = list(PROFILE_WEIGHTS.keys())
    weights = list(PROFILE_WEIGHTS.values())

    selected_name = random.choices(profile_names, weights=weights, k=1)[0]
    return BROWSER_PROFILES[selected_name].copy()


def get_profile_by_name(name: str) -> Dict[str, str]:
    """
    Get a specific browser profile by name.

    Args:
        name: Profile name (e.g., 'chrome131_macos', 'firefox132_windows')

    Returns:
        Dict with User-Agent and Client Hints headers

    Raises:
        KeyError: If profile name doesn't exist
    """
    if name not in BROWSER_PROFILES:
        raise KeyError(
            f"Profile '{name}' not found. Available profiles: "
            f"{', '.join(BROWSER_PROFILES.keys())}"
        )
    return BROWSER_PROFILES[name].copy()


def get_chrome_profiles_only() -> Dict[str, str]:
    """
    Get a random Chrome profile (any version, any OS).

    Useful when you specifically want Chrome behavior.

    Returns:
        Dict with User-Agent and Client Hints headers
    """
    chrome_names = [
        "chrome131_macos",
        "chrome131_windows",
        "chrome130_macos",
        "chrome130_windows",
    ]
    selected_name = random.choice(chrome_names)
    return BROWSER_PROFILES[selected_name].copy()


def list_available_profiles() -> list:
    """
    List all available browser profile names.

    Returns:
        List of profile name strings
    """
    return list(BROWSER_PROFILES.keys())


# For backward compatibility
def get_coherent_headers() -> Dict[str, str]:
    """
    Alias for get_random_profile() for backward compatibility.

    Returns:
        Dict with User-Agent and Client Hints headers
    """
    return get_random_profile()
