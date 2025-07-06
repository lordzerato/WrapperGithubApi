from typing import Any

JSON = dict[str, Any]
AcceptedValue = str | int | float | bool | None
GraphQLVariables = dict[str, AcceptedValue | JSON | list[AcceptedValue | JSON]] | None
