import dataclasses
import json
import uuid


@dataclasses.dataclass
class RouteData:
    stop: bool
    conversation_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[dict] = dataclasses.field(default_factory=list)
    query: str = ""
    variables: dict = dataclasses.field(default_factory=dict)
    prev_node_type: str = ""
    prev_node_id: str = ""

    @classmethod
    def from_json(cls, json_str: str) -> "RouteData":
        data = json.loads(json_str)
        route_data = data.get("route_data", {})

        return cls(
            stop=route_data.get("stop", False),
            conversation_id=route_data.get("conversation_id", str(uuid.uuid4())),
            messages=route_data.get("messages", []),
            query=route_data.get("query", ""),
            variables=route_data.get("variables", {}),
            prev_node_id=route_data.get("prev_node_id", ""),
            prev_node_type=route_data.get("prev_node_type", ""),
        )

    def to_json(self) -> str:
        return json.dumps(
            {
                "route_data": {
                    "stop": self.stop,
                    "conversation_id": self.conversation_id,
                    "messages": self.messages,
                    "query": self.query,
                    "variables": self.variables,
                    "prev_node_id": self.prev_node_id,
                    "prev_node_type": self.prev_node_type,
                }
            },
            indent=2,
            ensure_ascii=False,
        )


def get_node_id(node_id: str | None = None) -> str:
    return node_id if node_id else str(uuid.uuid4())


def is_stopped(route_data: RouteData) -> bool:
    if route_data.stop:
        return True
    return False
