import logging

from fastapi import Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

logger = logging.getLogger("rate_limit")


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(
        "Rate limit superado - IP: %s, Path: %s",
        request.client.host if request.client else "unknown",
        request.url.path,
    )
    return _rate_limit_exceeded_handler(request, exc)


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],
    swallow_errors=True,
)


def setup_rate_limiting(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
