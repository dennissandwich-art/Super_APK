"""
NTRLI SuperAPK - Monitoring & Analytics Module
Performance monitoring and usage analytics
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path

try:
    from modules.ai_core import AI_CONSOLE
except ImportError:
    from ai_core import AI_CONSOLE

ANALYTICS_DIR = "/sdcard/superapk_analytics"
PERFORMANCE_DB = "/sdcard/superapk_performance.json"

class MonitoringManager:
    """
    Application monitoring and analytics
    - Performance tracking
    - Usage analytics
    - Error tracking
    - Custom events
    """

    def __init__(self, ai_console=None):
        self.ai_console = ai_console
        self.performance_metrics = self._load_metrics()
        self.session_start = time.time()
        self.session_events = []
        self._ensure_analytics_dir()
        self.log("MonitoringManager initialized")

    def log(self, msg, level="INFO"):
        """Enhanced logging"""
        if self.ai_console:
            self.ai_console.log(f"[MONITORING] {msg}", level)
        else:
            print(f"[MONITORING] {msg}")

    def _ensure_analytics_dir(self):
        """Ensure analytics directory exists"""
        try:
            Path(ANALYTICS_DIR).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.log(f"Error creating analytics dir: {e}", "ERROR")

    def _load_metrics(self):
        """Load performance metrics"""
        try:
            if os.path.exists(PERFORMANCE_DB):
                with open(PERFORMANCE_DB, "r") as f:
                    return json.load(f)
            return {
                "app_launches": 0,
                "total_session_time": 0,
                "screen_views": {},
                "api_calls": {},
                "errors": [],
                "events": []
            }
        except Exception as e:
            self.log(f"Error loading metrics: {e}", "ERROR")
            return {}

    def _save_metrics(self):
        """Save performance metrics"""
        try:
            Path(PERFORMANCE_DB).parent.mkdir(parents=True, exist_ok=True)
            with open(PERFORMANCE_DB, "w") as f:
                json.dump(self.performance_metrics, f, indent=2)
        except Exception as e:
            self.log(f"Error saving metrics: {e}", "ERROR")

    # ========== SESSION TRACKING ==========

    def track_app_launch(self):
        """Track app launch"""
        self.performance_metrics["app_launches"] = self.performance_metrics.get("app_launches", 0) + 1
        self._save_metrics()
        self.log(f"App launch #{self.performance_metrics['app_launches']}")

    def track_app_close(self):
        """Track app close and session duration"""
        session_duration = time.time() - self.session_start
        self.performance_metrics["total_session_time"] = \
            self.performance_metrics.get("total_session_time", 0) + session_duration

        self._save_session_events()
        self._save_metrics()

        self.log(f"Session ended: {session_duration:.2f}s")

    def _save_session_events(self):
        """Save session events to file"""
        try:
            session_file = os.path.join(
                ANALYTICS_DIR,
                f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )

            session_data = {
                "session_start": datetime.fromtimestamp(self.session_start).isoformat(),
                "session_duration": time.time() - self.session_start,
                "events": self.session_events
            }

            with open(session_file, "w") as f:
                json.dump(session_data, f, indent=2)

            self.log(f"Session saved: {len(self.session_events)} events")

        except Exception as e:
            self.log(f"Error saving session: {e}", "ERROR")

    # ========== SCREEN TRACKING ==========

    def track_screen_view(self, screen_name):
        """Track screen view"""
        if "screen_views" not in self.performance_metrics:
            self.performance_metrics["screen_views"] = {}

        views = self.performance_metrics["screen_views"].get(screen_name, 0)
        self.performance_metrics["screen_views"][screen_name] = views + 1

        self._track_event("screen_view", {"screen": screen_name})
        self._save_metrics()

        self.log(f"Screen view: {screen_name}")

    # ========== API TRACKING ==========

    def track_api_call(self, api_name, duration_ms, success=True):
        """Track API call performance"""
        if "api_calls" not in self.performance_metrics:
            self.performance_metrics["api_calls"] = {}

        if api_name not in self.performance_metrics["api_calls"]:
            self.performance_metrics["api_calls"][api_name] = {
                "count": 0,
                "total_duration": 0,
                "successes": 0,
                "failures": 0
            }

        api_stats = self.performance_metrics["api_calls"][api_name]
        api_stats["count"] += 1
        api_stats["total_duration"] += duration_ms

        if success:
            api_stats["successes"] += 1
        else:
            api_stats["failures"] += 1

        self._save_metrics()

        self.log(f"API call: {api_name} - {duration_ms:.2f}ms - {'OK' if success else 'FAIL'}")

    def measure_api_call(self, api_name):
        """Context manager for measuring API call duration"""
        class APICallTimer:
            def __init__(timer_self, monitoring_manager):
                timer_self.monitoring = monitoring_manager
                timer_self.start_time = None
                timer_self.success = True

            def __enter__(timer_self):
                timer_self.start_time = time.time()
                return timer_self

            def __exit__(timer_self, exc_type, exc_val, exc_tb):
                duration_ms = (time.time() - timer_self.start_time) * 1000
                timer_self.success = exc_type is None
                timer_self.monitoring.track_api_call(api_name, duration_ms, timer_self.success)
                return False

        return APICallTimer(self)

    # ========== ERROR TRACKING ==========

    def track_error(self, error_type, error_message, context=None):
        """Track error"""
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_message,
            "context": context or {}
        }

        if "errors" not in self.performance_metrics:
            self.performance_metrics["errors"] = []

        self.performance_metrics["errors"].append(error_entry)

        # Keep only recent errors (last 100)
        self.performance_metrics["errors"] = self.performance_metrics["errors"][-100:]

        self._save_metrics()

        self.log(f"Error tracked: {error_type} - {error_message}", "ERROR")

    # ========== EVENT TRACKING ==========

    def track_event(self, event_name, properties=None):
        """Track custom event"""
        self._track_event(event_name, properties)
        self._save_metrics()

    def _track_event(self, event_name, properties=None):
        """Internal event tracking"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "name": event_name,
            "properties": properties or {}
        }

        # Add to session events
        self.session_events.append(event)

        # Add to global events (keep last 1000)
        if "events" not in self.performance_metrics:
            self.performance_metrics["events"] = []

        self.performance_metrics["events"].append(event)
        self.performance_metrics["events"] = self.performance_metrics["events"][-1000:]

        self.log(f"Event: {event_name}")

    # ========== PERFORMANCE MEASUREMENT ==========

    def measure_performance(self, operation_name):
        """Context manager for measuring operation performance"""
        class PerformanceTimer:
            def __init__(timer_self, monitoring_manager):
                timer_self.monitoring = monitoring_manager
                timer_self.start_time = None

            def __enter__(timer_self):
                timer_self.start_time = time.time()
                return timer_self

            def __exit__(timer_self, exc_type, exc_val, exc_tb):
                duration_ms = (time.time() - timer_self.start_time) * 1000
                timer_self.monitoring.track_event(
                    "performance",
                    {
                        "operation": operation_name,
                        "duration_ms": duration_ms,
                        "success": exc_type is None
                    }
                )
                return False

        return PerformanceTimer(self)

    # ========== ANALYTICS REPORTING ==========

    def get_analytics_summary(self):
        """Get analytics summary"""
        total_session_time = self.performance_metrics.get("total_session_time", 0)
        app_launches = self.performance_metrics.get("app_launches", 0)

        avg_session_time = total_session_time / app_launches if app_launches > 0 else 0

        # Calculate API performance
        api_stats = {}
        for api_name, stats in self.performance_metrics.get("api_calls", {}).items():
            if stats["count"] > 0:
                api_stats[api_name] = {
                    "calls": stats["count"],
                    "avg_duration": stats["total_duration"] / stats["count"],
                    "success_rate": stats["successes"] / stats["count"] * 100
                }

        summary = {
            "app_launches": app_launches,
            "total_session_time": total_session_time,
            "avg_session_time": avg_session_time,
            "screen_views": self.performance_metrics.get("screen_views", {}),
            "api_performance": api_stats,
            "total_errors": len(self.performance_metrics.get("errors", [])),
            "total_events": len(self.performance_metrics.get("events", []))
        }

        return summary

    def export_analytics(self, export_type="summary"):
        """Export analytics data"""
        if export_type == "summary":
            return self.get_analytics_summary()
        elif export_type == "full":
            return self.performance_metrics
        elif export_type == "session":
            return {
                "session_start": datetime.fromtimestamp(self.session_start).isoformat(),
                "session_duration": time.time() - self.session_start,
                "events": self.session_events
            }
        else:
            return {}
