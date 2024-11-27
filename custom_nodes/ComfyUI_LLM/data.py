import dataclasses
import json
import uuid


@dataclasses.dataclass
class RouteData:
    stop: bool
    conversation_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[dict] = dataclasses.field(default_factory=list)
    query: str = ""

    @classmethod
    def from_json(cls, json_str: str) -> "RouteData":
        data = json.loads(json_str)
        route_data = data.get("route_data", {})

        return cls(
            stop=route_data.get("stop", False),
            conversation_id=route_data.get("conversation_id", str(uuid.uuid4())),
            messages=route_data.get("messages", []),
            query=route_data.get("query", ""),
        )

    def to_json(self) -> str:
        return json.dumps(
            {
                "route_data": {
                    "stop": self.stop,
                    "conversation_id": self.conversation_id,
                    "messages": self.messages,
                    "query": self.query,
                }
            },
            indent=2,
            ensure_ascii=False,
        )
