import json
import os
import sqlite3
from pathlib import Path
from typing import Optional

from .models import Snippet


def get_db_path() -> Path:
    if "SNIP_DB_PATH" in os.environ:
        return Path(os.environ["SNIP_DB_PATH"])
    return Path.home() / ".quicksnip" / "snippets.db"


class Database:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or get_db_path()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS snippets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT DEFAULT '',
                    language TEXT DEFAULT '',
                    code TEXT NOT NULL,
                    tags TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

    def add_snippet(self, snippet: Snippet) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO snippets (name, description, language, code, tags) VALUES (?, ?, ?, ?, ?)",
                (snippet.name, snippet.description, snippet.language, snippet.code, ",".join(snippet.tags)),
            )
            return cursor.lastrowid

    def get_snippet(self, name: str) -> Optional[Snippet]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute("SELECT * FROM snippets WHERE name = ?", (name,)).fetchone()
            return self._row_to_snippet(row) if row else None

    def search_snippets(self, query: str = "", language: str = "", tag: str = "") -> list[Snippet]:
        with sqlite3.connect(self.db_path) as conn:
            sql = "SELECT * FROM snippets WHERE 1=1"
            params: list = []
            if query:
                sql += " AND (name LIKE ? OR description LIKE ? OR code LIKE ?)"
                params.extend([f"%{query}%", f"%{query}%", f"%{query}%"])
            if language:
                sql += " AND language = ?"
                params.append(language)
            if tag:
                sql += " AND tags LIKE ?"
                params.append(f"%{tag}%")
            sql += " ORDER BY name"
            rows = conn.execute(sql, params).fetchall()
            return [self._row_to_snippet(row) for row in rows]

    def list_snippets(self) -> list[Snippet]:
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute("SELECT * FROM snippets ORDER BY name").fetchall()
            return [self._row_to_snippet(row) for row in rows]

    def delete_snippet(self, name: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("DELETE FROM snippets WHERE name = ?", (name,))
            return cursor.rowcount > 0

    def update_snippet(self, name: str, snippet: Snippet) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "UPDATE snippets SET name=?, description=?, language=?, code=?, tags=?, updated_at=CURRENT_TIMESTAMP WHERE name=?",
                (snippet.name, snippet.description, snippet.language, snippet.code, ",".join(snippet.tags), name),
            )
            return cursor.rowcount > 0

    def export_json(self) -> str:
        snippets = self.list_snippets()
        data = [
            {
                "name": s.name,
                "description": s.description,
                "language": s.language,
                "code": s.code,
                "tags": s.tags,
            }
            for s in snippets
        ]
        return json.dumps(data, indent=2)

    def import_json(self, json_str: str) -> int:
        data = json.loads(json_str)
        count = 0
        for item in data:
            snippet = Snippet(
                id=None,
                name=item["name"],
                description=item.get("description", ""),
                language=item.get("language", ""),
                code=item["code"],
                tags=item.get("tags", []),
            )
            try:
                self.add_snippet(snippet)
                count += 1
            except sqlite3.IntegrityError:
                pass
        return count

    def _row_to_snippet(self, row) -> Snippet:
        return Snippet(
            id=row[0],
            name=row[1],
            description=row[2],
            language=row[3],
            code=row[4],
            tags=row[5].split(",") if row[5] else [],
            created_at=row[6],
            updated_at=row[7],
        )
