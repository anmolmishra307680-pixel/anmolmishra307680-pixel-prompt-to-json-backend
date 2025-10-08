"""Sentry error monitoring configuration"""

import os
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

def init_sentry():
    """Initialize Sentry error monitoring"""
    sentry_dsn = os.getenv("SENTRY_DSN")
    
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            environment=os.getenv("SENTRY_ENVIRONMENT", "development"),
            traces_sample_rate=0.1,
            profiles_sample_rate=0.1,
            integrations=[
                FastApiIntegration(auto_enabling_integrations=True),
                SqlalchemyIntegration(),
            ],
            attach_stacktrace=True,
            send_default_pii=False,
        )
        print(f"[OK] Sentry monitoring enabled for {os.getenv('SENTRY_ENVIRONMENT', 'development')}")
        return True
    else:
        print("[WARN] SENTRY_DSN not configured, error monitoring disabled")
        return False

def capture_exception(error: Exception, extra_data: dict = None):
    """Capture exception with Sentry"""
    try:
        if extra_data:
            sentry_sdk.set_extra("additional_data", extra_data)
        sentry_sdk.capture_exception(error)
    except Exception as e:
        print(f"[ERROR] Failed to capture exception with Sentry: {e}")

def capture_message(message: str, level: str = "info"):
    """Capture message with Sentry"""
    try:
        sentry_sdk.capture_message(message, level=level)
    except Exception as e:
        print(f"[ERROR] Failed to capture message with Sentry: {e}")