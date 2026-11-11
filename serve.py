#!/usr/bin/env python3
"""Run the Cookiepocalypse planner locally with automatic saving to ./saves.

    python3 serve.py            # http://localhost:8000
    python3 serve.py 8080       # another port

The app saves your plan to saves/state.json about a second after each change,
and keeps one backup per day in saves/backups/ (the last 30 days). The saves
folder is in .gitignore, so it never goes to GitHub. Only this computer can
reach the server: it listens on 127.0.0.1.
"""
import datetime
import http.server
import json
import os
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SAVES = ROOT / "saves"
STATE = SAVES / "state.json"
BACKUPS = SAVES / "backups"
KEEP_BACKUPS = 30
MAX_BYTES = 20 * 1024 * 1024
LOCK = threading.Lock()


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def _json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/state":
            with LOCK:
                if not STATE.exists():
                    return self._json(200, {"app": "cookiepocalypse", "exists": False})
                saved = json.loads(STATE.read_text(encoding="utf-8"))
            return self._json(200, {"app": "cookiepocalypse", "exists": True, **saved})
        if self.path.split("?")[0].startswith("/saves"):
            return self._json(404, {"error": "not found"})
        if self.path.split("?")[0] == "/seed.json":  # the app's starter data lives in data/
            self.path = "/data/seed.json"
        return super().do_GET()

    def do_PUT(self):
        if self.path.split("?")[0] != "/api/state":
            return self._json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        if not 0 < length <= MAX_BYTES:
            return self._json(413, {"error": "too large"})
        raw = self.rfile.read(length).decode("utf-8")
        try:
            json.loads(raw)  # must be a valid plan
        except ValueError:
            return self._json(400, {"error": "not JSON"})
        saved_at = datetime.datetime.now().isoformat(timespec="seconds")
        record = json.dumps({"savedAt": saved_at, "json": raw})
        with LOCK:
            SAVES.mkdir(exist_ok=True)
            BACKUPS.mkdir(exist_ok=True)
            tmp = STATE.with_suffix(".tmp")
            tmp.write_text(record, encoding="utf-8")
            os.replace(tmp, STATE)
            daily = BACKUPS / f"state-{datetime.date.today().isoformat()}.json"
            daily.write_text(record, encoding="utf-8")
            for old in sorted(BACKUPS.glob("state-*.json"))[:-KEEP_BACKUPS]:
                old.unlink()
        return self._json(200, {"ok": True, "savedAt": saved_at})

    do_POST = do_PUT

    def log_message(self, fmt, *args):
        try:
            msg = fmt % args
        except (TypeError, ValueError):
            msg = str(fmt)
        if "/api/state" not in msg:  # autosaves would flood the console
            super().log_message("%s", msg)


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    url = f"http://localhost:{port}/index.html"
    print(f"Cookiepocalypse planner: {url}\nSaving to {STATE}\nCtrl+C to stop.")
    threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
