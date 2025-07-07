from typing import Any, Literal

OBJECT = dict[str, Any]
AcceptedValue = str | int | float | bool | None
JSON = dict[str, AcceptedValue | OBJECT | list[AcceptedValue | OBJECT]]
Methods = Literal["GET", "POST", "PUT", "DELETE"]
