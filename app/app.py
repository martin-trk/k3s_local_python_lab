from __future__ import annotations

import json
import os
from dataclasses import dataclass
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import RLock
from typing import Any, Dict, Optional, Type

JSONDict = Dict[str, Any]

@dataclass(frozen=True)
class ConfigEntry:
    name: str
    value: str

    def to_dict(self) -> JSONDict:
        return {"name": self.name, "value": self.value}


class ConfigStore:
    def __init__(self) -> None:
        self._store: Dict[str, str] = {}
        self._lock = RLock()

    def get(self, name: str) -> Optional[str]:
        with self._lock:
            return self._store.get(name)

    def set(self, entry: ConfigEntry) -> None:
        with self._lock:
            self._store[entry.name] = entry.value

    def delete(self, name: str) -> bool:
        with self._lock:
            if name in self._store:
                del self._store[name]
                return True
            return False


class APIRequestHandler(BaseHTTPRequestHandler):
    config_store = ConfigStore()
    version = "1.0.0"

    def _send_json(self, code: int, payload: JSONDict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> Optional[JSONDict]:
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length == 0:
            return None

        raw_body = self.rfile.read(content_length)
        try:
            return json.loads(raw_body)
        except json.JSONDecodeError:
            return None

    def _config_name(self) -> Optional[str]:
        if not self.path.startswith("/config/"):
            return None
        return self.path.removeprefix("/config/")

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return

        if self.path == "/version":
            self._send_json(200, {"version": self.version})
            return

        if self.path == "/env":
            self._send_json(200, {"environment": os.getenv("ENVIRONMENT", "")})
            return

        config_name = self._config_name()
        if config_name is not None:
            if not config_name:
                self._send_json(400, {"error": "name is required"})
                return

            stored_value = self.config_store.get(config_name)
            if stored_value is None:
                self._send_json(404, {"error": "config not found"})
                return

            self._send_json(200, ConfigEntry(config_name, stored_value).to_dict())
            return

        self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/config":
            self._send_json(404, {"error": "not found"})
            return

        payload = self._read_json()
        if not payload:
            self._send_json(400, {"error": "invalid JSON"})
            return

        name = payload.get("name")
        value = payload.get("value")
        if not isinstance(name, str) or not name:
            self._send_json(400, {"error": "name is required"})
            return
        if not isinstance(value, str):
            self._send_json(400, {"error": "value must be a string"})
            return

        entry = ConfigEntry(name=name, value=value)
        self.config_store.set(entry)
        self._send_json(200, entry.to_dict())

    def do_DELETE(self) -> None:
        config_name = self._config_name()
        if config_name is None:
            self._send_json(404, {"error": "not found"})
            return

        if not config_name:
            self._send_json(400, {"error": "name is required"})
            return

        deleted = self.config_store.delete(config_name)
        if not deleted:
            self._send_json(404, {"error": "config not found"})
            return

        self._send_json(200, {"deleted": True})

    def log_message(self, format: str, *args: Any) -> None:
        return


@dataclass(frozen=True)
class AppConfig:
    host: str = ""
    port: int = 8080

    @classmethod
    def from_env(cls) -> AppConfig:
        return cls(host="", port=int(os.getenv("PORT", "8080")))


def run(server_class: Type[HTTPServer] = HTTPServer, handler_class: Type[APIRequestHandler] = APIRequestHandler) -> None:
    config = AppConfig.from_env()
    server_address = (config.host, config.port)
    server = server_class(server_address, handler_class)
    print(f"Starting server on http://127.0.0.1:{config.port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
