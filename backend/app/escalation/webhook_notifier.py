import hmac
import hashlib
import json
import time
from typing import Dict, Any, Optional
import httpx

class WebhookNotifier:
    """
    Sends cryptographically signed webhook notifications on support escalations.
    """
    def __init__(self, secret: str = "anchor_webhook_secret_key_2026"):
        self.secret = secret

    def sign_payload(self, payload: Dict[str, Any], timestamp: int) -> str:
        data = f"{timestamp}.{json.dumps(payload, sort_keys=True)}"
        return hmac.new(self.secret.encode(), data.encode(), hashlib.sha256).hexdigest()

    async def dispatch(self, webhook_url: str, event_type: str, data: Dict[str, Any]) -> bool:
        ts = int(time.time())
        payload = {
            "event": event_type,
            "timestamp": ts,
            "data": data,
        }
        signature = self.sign_payload(payload, ts)
        headers = {
            "Content-Type": "application/json",
            "X-Anchor-Signature": signature,
            "X-Anchor-Timestamp": str(ts),
        }

        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                res = await client.post(webhook_url, json=payload, headers=headers)
                return res.status_code in (200, 201, 202, 204)
            except Exception:
                return False

webhook_notifier = WebhookNotifier()