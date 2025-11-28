"""
Self-Tuning Configuration Optimizer

Automatically adjusts rate limiting parameters based on observed performance.
Learns optimal settings over time and adapts to Google API changes.

Features:
- Records performance history (config + results)
- Identifies best-performing configurations
- Provides tuning suggestions
- Automatic adjustment based on success rate
"""

import json
import logging
from typing import Dict, Optional, List
from pathlib import Path
import statistics

logger = logging.getLogger(__name__)


class ConfigTuner:
    """
    Automatically tunes configuration parameters based on performance.

    Tracks performance metrics for different configurations and suggests
    optimal settings.

    Example:
        >>> tuner = ConfigTuner()
        >>> tuner.record_session(
        >>>     config={'base_delay': 15},
        >>>     success_rate=92.5,
        >>>     avg_response_time=2.1
        >>> )
        >>> suggestion = tuner.auto_tune()
    """

    def __init__(self, history_file: str = ".config_tuning_history.json"):
        """
        Initialize config tuner.

        Args:
            history_file: Path to save tuning history
        """
        self.history_file = Path(history_file)
        self.performance_history: List[Dict[str, float]] = []

        # Load existing history if available
        self._load_history()

        logger.info(f"ConfigTuner initialized (history_file={history_file})")

    def _load_history(self):
        """Load performance history from file."""
        try:
            if self.history_file.exists():
                with open(self.history_file, "r") as f:
                    self.performance_history = json.load(f)
                logger.info(
                    f"Loaded {len(self.performance_history)} historical sessions"
                )
        except Exception as e:
            logger.warning(f"Could not load tuning history: {e}")
            self.performance_history = []

    def _save_history(self):
        """Save performance history to file."""
        try:
            with open(self.history_file, "w") as f:
                json.dump(self.performance_history, f, indent=2)
            logger.debug("Saved tuning history")
        except Exception as e:
            logger.error(f"Could not save tuning history: {e}")

    def record_session(
        self,
        config: Dict,
        success_rate: float,
        avg_response_time: float,
        requests_total: int = 0,
    ):
        """
        Record performance for a configuration.

        Args:
            config: Configuration used (dict with base_delay, requests_per_hour, etc.)
            success_rate: Success rate percentage (0-100)
            avg_response_time: Average response time in seconds
            requests_total: Total requests made
        """
        session_record = {
            "base_delay": config.get("base_delay", 15),
            "requests_per_hour": config.get("requests_per_hour", 150),
            "success_rate": success_rate,
            "response_time": avg_response_time,
            "requests_total": requests_total,
        }

        self.performance_history.append(session_record)
        self._save_history()

        logger.info(
            f"Recorded session: delay={session_record['base_delay']}s, "
            f"success_rate={success_rate:.1f}%, "
            f"response_time={avg_response_time:.2f}s"
        )

    def suggest_optimal_config(self, min_success_rate: float = 85.0) -> Optional[Dict]:
        """
        Find best-performing configuration from history.

        Args:
            min_success_rate: Minimum acceptable success rate

        Returns:
            Dict with suggested configuration, or None if insufficient data
        """
        if len(self.performance_history) < 3:
            logger.info("Insufficient history for suggestions (need ≥3 sessions)")
            return None

        # Filter to acceptable success rates
        acceptable = [
            s for s in self.performance_history if s["success_rate"] >= min_success_rate
        ]

        if not acceptable:
            logger.warning("No sessions met minimum success rate threshold")
            return None

        # Find best by success rate, then by speed
        best = max(acceptable, key=lambda x: (x["success_rate"], -x["response_time"]))

        suggestion = {
            "base_delay": best["base_delay"],
            "requests_per_hour": best["requests_per_hour"],
            "expected_success_rate": best["success_rate"],
            "expected_response_time": best["response_time"],
        }

        logger.info(
            f"Suggested config: delay={best['base_delay']}s "
            f"(success_rate={best['success_rate']:.1f}%)"
        )

        return suggestion

    def auto_tune(self) -> Optional[Dict]:
        """
        Automatically suggest configuration adjustments.

        Returns:
            Dict with tuning adjustments, or None if no change needed
        """
        if len(self.performance_history) < 5:
            logger.debug("Need more history for auto-tuning (≥5 sessions)")
            return None

        # Analyze recent performance (last 10 sessions)
        recent = self.performance_history[-10:]
        avg_success = statistics.mean([s["success_rate"] for s in recent])

        # Current config (assume latest)
        current_delay = recent[-1]["base_delay"]

        adjustment = None

        if avg_success < 80:
            # Poor performance - increase delays
            new_delay = current_delay + 2
            adjustment = {
                "base_delay": new_delay,
                "reason": f"Low success rate ({avg_success:.1f}%) - increasing delays",
            }
            logger.info(
                f"Auto-tune: {current_delay}s → {new_delay}s (low success rate)"
            )

        elif avg_success > 95 and current_delay > 5:
            # Excellent performance - try speeding up
            new_delay = max(5, current_delay - 1)
            adjustment = {
                "base_delay": new_delay,
                "reason": f"High success rate ({avg_success:.1f}%) - decreasing delays",
            }
            logger.info(
                f"Auto-tune: {current_delay}s → {new_delay}s (high success rate)"
            )

        else:
            logger.debug(f"No adjustment needed (success_rate={avg_success:.1f}%)")

        return adjustment

    def get_stats(self) -> Dict:
        """
        Get tuning statistics.

        Returns:
            Dict with stats about tuning history
        """
        if not self.performance_history:
            return {
                "total_sessions": 0,
                "avg_success_rate": 0,
                "best_success_rate": 0,
            }

        success_rates = [s["success_rate"] for s in self.performance_history]

        return {
            "total_sessions": len(self.performance_history),
            "avg_success_rate": statistics.mean(success_rates),
            "best_success_rate": max(success_rates),
            "worst_success_rate": min(success_rates),
            "recent_avg": statistics.mean(
                [s["success_rate"] for s in self.performance_history[-10:]]
            ),
        }

    def reset(self):
        """Clear tuning history."""
        self.performance_history = []
        self._save_history()
        logger.info("ConfigTuner history cleared")
