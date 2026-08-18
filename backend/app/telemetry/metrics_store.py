import time
from typing import List, Dict, Any

class TelemetryMetricsStore:
    """
    Records performance telemetry, latency stats, resolution rates, and quality trends.
    """
    def __init__(self):
        self.latencies_ms: List[float] = [180.0, 240.0, 310.0, 195.0, 220.0]
        self.total_queries: int = 5
        self.grounded_answers: int = 4
        self.escalations_triggered: int = 1
        self.redactions_count: int = 0
        self.blocked_injections: int = 0

    def record_query_metric(
        self,
        latency_ms: float,
        is_grounded: bool,
        is_escalated: bool,
        had_redaction: bool = False,
    ):
        self.latencies_ms.append(latency_ms)
        self.total_queries += 1
        if is_grounded:
            self.grounded_answers += 1
        if is_escalated:
            self.escalations_triggered += 1
        if had_redaction:
            self.redactions_count += 1

    def get_summary(self) -> Dict[str, Any]:
        lats = sorted(self.latencies_ms) if self.latencies_ms else [0.0]
        p50 = lats[int(len(lats) * 0.50)]
        p95 = lats[int(len(lats) * 0.95)] if len(lats) > 1 else lats[0]

        res_rate = (self.grounded_answers / max(1, self.total_queries)) * 100.0

        return {
            "total_queries": self.total_queries,
            "grounded_answers": self.grounded_answers,
            "escalations_triggered": self.escalations_triggered,
            "resolution_rate_percent": round(res_rate, 1),
            "p50_latency_ms": round(p50, 1),
            "p95_latency_ms": round(p95, 1),
            "redactions_count": self.redactions_count,
            "blocked_injections": self.blocked_injections,
        }

metrics_store = TelemetryMetricsStore()