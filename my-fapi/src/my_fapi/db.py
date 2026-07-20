import re

import psycopg
from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DBAPIError

DATABASE_URL = "postgresql+psycopg://my_fapi:my_fapi@localhost:5432/my_fapi"
ADMIN_DATABASE_URL = "postgresql+psycopg://my_fapi:my_fapi@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)
admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")

_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
_PROTECTED_DATABASES = {"postgres", "my_fapi", "template0", "template1"}


def validate_identifier(name: str, kind: str) -> None:
    if not _IDENTIFIER_RE.match(name):
        raise HTTPException(422, f"Invalid {kind}: '{name}'")


class DatabaseCreate(BaseModel):
    db_name: str


def list_databases() -> list[str]:
    with admin_engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT datname FROM pg_database WHERE datistemplate = false ORDER BY datname"
            )
        )
        return [row[0] for row in result]


def create_database(payload: DatabaseCreate) -> dict:
    validate_identifier(payload.db_name, "database name")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"),
            {"name": payload.db_name},
        ).first()
        if exists:
            raise HTTPException(400, f"Database '{payload.db_name}' already exists")
        conn.execute(text(f'CREATE DATABASE "{payload.db_name}"'))
    return {"message": f"Database '{payload.db_name}' created"}


def delete_database(db_name: str) -> dict:
    validate_identifier(db_name, "database name")
    if db_name in _PROTECTED_DATABASES:
        raise HTTPException(400, f"Cannot delete protected database '{db_name}'")
    with admin_engine.connect() as conn:
        exists = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname = :name"), {"name": db_name}
        ).first()
        if not exists:
            raise HTTPException(404, f"Database '{db_name}' not found")
        try:
            conn.execute(text(f'DROP DATABASE "{db_name}"'))
        except DBAPIError as exc:
            if isinstance(exc.orig, psycopg.errors.ObjectInUse):
                raise HTTPException(
                    409,
                    f"Database '{db_name}' has active connections — close them "
                    "(e.g. disconnect it in pgAdmin) and retry",
                ) from exc
            raise
    return {"message": f"Database '{db_name}' deleted"}
