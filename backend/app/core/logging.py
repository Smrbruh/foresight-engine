import json
import logging
from datetime import datetime
from typing import Any


class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger("security")

    def log_auth_attempt(self, username: str, success: bool, ip: str, user_agent: str):
        self.logger.info(
            json.dumps(
                {
                    "event": "auth_attempt",
                    "username": username,
                    "success": success,
                    "ip": ip,
                    "user_agent": user_agent,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        )

    def log_api_access(self, user_id: int, endpoint: str, method: str, ip: str):
        self.logger.info(
            json.dumps(
                {
                    "event": "api_access",
                    "user_id": user_id,
                    "endpoint": endpoint,
                    "method": method,
                    "ip": ip,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        )

    def log_security_event(self, event_type: str, details: dict[str, Any]):
        self.logger.warning(
            json.dumps(
                {
                    "event": "security_event",
                    "type": event_type,
                    "details": details,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            )
        )


security_logger = SecurityLogger()
