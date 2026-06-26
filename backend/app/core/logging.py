import json
import logging
import sys
from datetime import datetime
from typing import Any


def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    def log_auth_attempt(self, username: str, success: bool, ip: str, user_agent: str):
        self.logger.info(json.dumps({
            "event": "auth_attempt",
            "username": username,
            "success": success,
            "ip": ip,
            "user_agent": user_agent,
            "timestamp": datetime.utcnow().isoformat()
        }))
    
    def log_api_access(self, user_id: int, endpoint: str, method: str, ip: str):
        self.logger.info(json.dumps({
            "event": "api_access",
            "user_id": user_id,
            "endpoint": endpoint,
            "method": method,
            "ip": ip,
            "timestamp": datetime.utcnow().isoformat()
        }))
    
    def log_security_event(self, event_type: str, details: dict[str, Any]):
        self.logger.warning(json.dumps({
            "event": "security_event",
            "type": event_type,
            "details": details,
            "timestamp": datetime.utcnow().isoformat()
        }))


security_logger = SecurityLogger()