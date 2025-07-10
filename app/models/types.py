from typing import Any, Literal

OBJECT = dict[str, Any]
AcceptedValue = str | int | float | bool | None
JSON = dict[str, AcceptedValue | OBJECT | list[AcceptedValue | OBJECT]]
Methods = Literal["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
PropsHeaders: list[str] = ["CSP", "STRICT_TRANSPORT_SECURITY", "PERMISSION_POLICY", "REFERRER_POLICY", "X_CONTENT_TYPE_OPTIONS", "X_FRAME_OPTIONS"]
RequiredCsp: list[str] = ["default-src", "script-src", "style-src", "img-src", "font-src", "worker-src", "connect-src"]
Pattern = r"^(?!0)\d+/(second|minute|hour|day|month|year)$"
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
