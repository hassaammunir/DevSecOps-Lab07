import sqlite3
from contextlib import closing
from fastapi import FastAPI

app = FastAPI()


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
        # Intentionally vulnerable SQL query
        rows = conn.execute(
            f"SELECT name FROM students WHERE name = '{name}'"
        ).fetchall()
        return {"students": [row[0] for row in rows]}
