import logging
import sqlite3
import time
from contextlib import closing

from fastapi import FastAPI, Request

# Task 5 - basic monitoring: log method, endpoint and status (no sensitive values)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("devsecops-lab07")

app = FastAPI()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration_ms = round((time.time() - start) * 1000, 1)
    # Log method, path and status only - never the query values (no sensitive data).
    logger.info(
        "method=%s path=%s status=%s duration_ms=%s",
        request.method, request.url.path, response.status_code, duration_ms,
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/search")
def search(name: str):
    with closing(sqlite3.connect(":memory:")) as conn:
        conn.execute("CREATE TABLE students (name TEXT)")
        conn.executemany(
            "INSERT INTO students VALUES (?)",
            [("Alice",), ("O'Neil",)]
        )
        # FIX (CWE-89): parameterized query separates data from SQL instructions.
        rows = conn.execute(
            "SELECT name FROM students WHERE name = ?",
            (name,)
        ).fetchall()
        return {"students": [row[0] for row in rows]}
