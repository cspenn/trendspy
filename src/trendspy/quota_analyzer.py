# start src/trendspy/quota_analyzer.py
"""
Quota Window Detection and Prediction

Analyzes success/failure patterns to detect Google's quota reset windows
and predict when quotas will reset.

This helps optimize wait times by:
- Learning quota patterns from historical data
- Predicting next reset time
- Avoiding wasteful waiting
"""

import time
import logging
from typing import Optional, Dict, Deque
from collections import deque
import numpy as np

logger = logging.getLogger(__name__)


class QuotaAnalyzer:
    """
    Analyzes request patterns to detect quota windows and predict resets.

    Tracks timestamps of successes and failures to identify patterns in
    Google's quota enforcement.

    Example:
        >>> analyzer = QuotaAnalyzer()
        >>> analyzer.record_result(success=True, timestamp=time.time())
        >>> reset_time = analyzer.predict_next_reset()
    """

    def __init__(self, history_size: int = 1000):
        """
        Initialize quota analyzer.

        Args:
            history_size: Number of historical results to track
        """
        self.history_size = history_size
        self.success_timestamps: Deque[float] = deque(maxlen=history_size)
        self.failure_timestamps: Deque[float] = deque(maxlen=history_size)
        self.detected_window: Optional[float] = None  # Detected quota window in seconds

        logger.info(f"QuotaAnalyzer initialized (history_size={history_size})")

    def record_result(self, success: bool, timestamp: Optional[float] = None):
        """
        Record a request result with timestamp.

        Args:
            success: Whether request succeeded
            timestamp: Unix timestamp (uses current time if None)
        """
        if timestamp is None:
            timestamp = time.time()

        if success:
            self.success_timestamps.append(timestamp)
        else:
            self.failure_timestamps.append(timestamp)

    def detect_quota_window(self) -> Optional[float]:
        """
        Analyze success patterns to detect quota reset window.

        Looks for modal (most common) interval between consecutive successes,
        which indicates the quota reset period.

        Returns:
            Detected quota window in seconds, or None if insufficient data
        """
        if len(self.success_timestamps) < 10:
            logger.debug("Insufficient data for quota window detection")
            return None

        # Calculate time deltas between consecutive successes
        timestamps = sorted(self.success_timestamps)
        deltas = np.diff(timestamps)

        # Filter outliers (>1 hour likely indicates breaks, not quota)
        deltas = deltas[deltas < 3600]

        if len(deltas) < 5:
            logger.debug("Insufficient valid deltas for detection")
            return None

        # Find modal interval using histogram
        try:
            hist, bins = np.histogram(deltas, bins=20)
            modal_index = np.argmax(hist)
            modal_window = (bins[modal_index] + bins[modal_index + 1]) / 2

            self.detected_window = modal_window
            logger.info(
                f"Detected quota window: {modal_window:.1f}s ({modal_window/60:.1f}m)"
            )
            return modal_window

        except Exception as e:
            logger.warning(f"Error detecting quota window: {e}")
            return None

    def predict_next_reset(self) -> Optional[float]:
        """
        Predict when quota will next reset based on detected pattern.

        Returns:
            Predicted Unix timestamp of next reset, or None if cannot predict
        """
        if not self.failure_timestamps:
            logger.debug("No failures recorded, cannot predict reset")
            return None

        # Detect window if not already done
        if self.detected_window is None:
            window = self.detect_quota_window()
            if window is None:
                return None
        else:
            window = self.detected_window

        # Use last failure time as reference
        last_failure = max(self.failure_timestamps)
        predicted_reset = last_failure + window

        logger.debug(
            f"Predicted reset in {predicted_reset - time.time():.0f}s "
            f"(at {time.strftime('%H:%M:%S', time.localtime(predicted_reset))})"
        )

        return predicted_reset

    def should_wait_for_reset(self, wait_threshold: float = 300) -> bool:
        """
        Determine if it's worth waiting for quota reset.

        Args:
            wait_threshold: Maximum seconds worth waiting (default: 5 minutes)

        Returns:
            True if should wait, False if should proceed/retry now
        """
        predicted = self.predict_next_reset()
        if predicted is None:
            return False

        wait_time = predicted - time.time()

        if wait_time <= 0:
            logger.info("Predicted reset time has passed, proceeding")
            return False

        if wait_time > wait_threshold:
            logger.info(f"Reset in {wait_time:.0f}s (>{wait_threshold}s), not waiting")
            return False

        logger.info(f"Waiting {wait_time:.0f}s for predicted quota reset")
        return True

    def get_stats(self) -> Dict:
        """
        Get quota analyzer statistics.

        Returns:
            Dict with stats about detected patterns
        """
        return {
            "total_successes": len(self.success_timestamps),
            "total_failures": len(self.failure_timestamps),
            "detected_window_seconds": self.detected_window,
            "detected_window_minutes": self.detected_window / 60
            if self.detected_window is not None
            else None,
            "predicted_next_reset": self.predict_next_reset(),
        }

    def reset(self):
        """Clear all historical data."""
        self.success_timestamps.clear()
        self.failure_timestamps.clear()
        self.detected_window = None
        logger.info("QuotaAnalyzer reset")


# end src/trendspy/quota_analyzer.py
