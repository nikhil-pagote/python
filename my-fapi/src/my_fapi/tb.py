from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    delete,
    insert,
    inspect,
    select,
    text,
    update,
)
from sqlalchemy.exc import InvalidRequestError

from my_fapi.db import engine, validate_identifier

metadata = MetaData()

TYPE_MAP = {
    "int": Integer,
    "float": Float,
    "str": String,
    "bool": Boolean,
}


class ColumnDef(BaseModel):
    name: str
    type: str
    primary_key: bool = False
    nullable: bool = True


class TableCreate(BaseModel):
    table_name: str
    columns: list[ColumnDef]


class TableAlter(BaseModel):
    action: str  # "add_column" | "drop_column" | "rename_column" | "change_type"
    column: str
    new_name: str | None = None
    type: str | None = None
    nullable: bool = True


class RowQuery(BaseModel):
    filter: dict


class RowUpdateByFilter(BaseModel):
    filter: dict
    values: dict


def _load_table(table_name: str) -> Table:
    if table_name not in metadata.tables:
        try:
            metadata.reflect(bind=engine, only=[table_name])
        except InvalidRequestError:
            pass
    if table_name not in metadata.tables:
        raise HTTPException(404, f"Table '{table_name}' not found")
    return metadata.tables[table_name]


def _primary_key_column(table: Table) -> Column:
    pk_columns = list(table.primary_key.columns)
    if not pk_columns:
        raise HTTPException(400, f"Table '{table.name}' has no primary key")
    return pk_columns[0]


def _apply_filter(stmt, table: Table, filter: dict):
    for col, val in filter.items():
        if col not in table.columns:
            raise HTTPException(
                422, f"Column '{col}' not found in table '{table.name}'"
            )
        stmt = stmt.where(table.c[col] == val)
    return stmt


def list_tables() -> list[str]:
    return inspect(engine).get_table_names()


def create_table(payload: TableCreate) -> dict:
    validate_identifier(payload.table_name, "table name")
    if inspect(engine).has_table(payload.table_name):
        raise HTTPException(400, f"Table '{payload.table_name}' already exists")

    columns = []
    for col in payload.columns:
        validate_identifier(col.name, "column name")
        if col.type not in TYPE_MAP:
            raise HTTPException(422, f"Unsupported column type: '{col.type}'")
        columns.append(
            Column(
                col.name,
                TYPE_MAP[col.type],
                primary_key=col.primary_key,
                nullable=col.nullable,
            )
        )

    table = Table(payload.table_name, metadata, *columns)
    table.create(engine)
    return {"message": f"Table '{payload.table_name}' created"}


def alter_table(table_name: str, payload: TableAlter) -> dict:
    table = _load_table(table_name)
    validate_identifier(payload.column, "column name")

    if payload.action == "add_column":
        if payload.column in table.columns:
            raise HTTPException(400, f"Column '{payload.column}' already exists")
        if payload.type not in TYPE_MAP:
            raise HTTPException(422, f"Unsupported column type: '{payload.type}'")
        col_type = TYPE_MAP[payload.type]().compile(dialect=engine.dialect)
        null_clause = "" if payload.nullable else " NOT NULL"
        with engine.begin() as conn:
            conn.execute(
                text(
                    f'ALTER TABLE "{table_name}" ADD COLUMN "{payload.column}" {col_type}{null_clause}'
                )
            )

    elif payload.action == "drop_column":
        if payload.column not in table.columns:
            raise HTTPException(404, f"Column '{payload.column}' not found")
        with engine.begin() as conn:
            conn.execute(
                text(f'ALTER TABLE "{table_name}" DROP COLUMN "{payload.column}"')
            )

    elif payload.action == "rename_column":
        if payload.column not in table.columns:
            raise HTTPException(404, f"Column '{payload.column}' not found")
        if not payload.new_name:
            raise HTTPException(422, "new_name is required for rename_column")
        validate_identifier(payload.new_name, "column name")
        with engine.begin() as conn:
            conn.execute(
                text(
                    f'ALTER TABLE "{table_name}" RENAME COLUMN "{payload.column}" TO "{payload.new_name}"'
                )
            )

    elif payload.action == "change_type":
        if payload.column not in table.columns:
            raise HTTPException(404, f"Column '{payload.column}' not found")
        if payload.type not in TYPE_MAP:
            raise HTTPException(422, f"Unsupported column type: '{payload.type}'")
        col_type = TYPE_MAP[payload.type]().compile(dialect=engine.dialect)
        with engine.begin() as conn:
            conn.execute(
                text(
                    f'ALTER TABLE "{table_name}" ALTER COLUMN "{payload.column}" TYPE {col_type}'
                )
            )

    else:
        raise HTTPException(422, f"Unsupported action: '{payload.action}'")

    metadata.remove(table)
    return {"message": f"Table '{table_name}' altered ({payload.action})"}


def delete_table(table_name: str) -> dict:
    table = _load_table(table_name)
    table.drop(engine)
    metadata.remove(table)
    return {"message": f"Table '{table_name}' deleted"}


def create_row(table_name: str, row: dict) -> dict:
    table = _load_table(table_name)
    with engine.begin() as conn:
        conn.execute(insert(table).values(**row))
    return {"message": "Row inserted"}


def list_rows(table_name: str) -> list[dict]:
    table = _load_table(table_name)
    with engine.connect() as conn:
        result = conn.execute(select(table))
        return [dict(r._mapping) for r in result]


def get_row(table_name: str, row_id: str) -> dict:
    table = _load_table(table_name)
    pk = _primary_key_column(table)
    with engine.connect() as conn:
        result = conn.execute(
            select(table).where(pk == pk.type.python_type(row_id))
        ).first()
    if result is None:
        raise HTTPException(404, "Row not found")
    return dict(result._mapping)


def update_row(table_name: str, row_id: str, row: dict) -> dict:
    table = _load_table(table_name)
    pk = _primary_key_column(table)
    with engine.begin() as conn:
        result = conn.execute(
            update(table).where(pk == pk.type.python_type(row_id)).values(**row)
        )
    if result.rowcount == 0:
        raise HTTPException(404, "Row not found")
    return {"message": "Row updated"}


def delete_row(table_name: str, row_id: str) -> dict:
    table = _load_table(table_name)
    pk = _primary_key_column(table)
    with engine.begin() as conn:
        result = conn.execute(delete(table).where(pk == pk.type.python_type(row_id)))
    if result.rowcount == 0:
        raise HTTPException(404, "Row not found")
    return {"message": "Row deleted"}


def query_rows(table_name: str, filter: dict) -> list[dict]:
    table = _load_table(table_name)
    stmt = _apply_filter(select(table), table, filter)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        return [dict(r._mapping) for r in result]


def update_rows_by_filter(table_name: str, filter: dict, values: dict) -> dict:
    if not filter:
        raise HTTPException(422, "filter must not be empty")
    table = _load_table(table_name)
    stmt = _apply_filter(update(table), table, filter).values(**values)
    with engine.begin() as conn:
        result = conn.execute(stmt)
    return {"message": f"{result.rowcount} row(s) updated"}


def delete_rows_by_filter(table_name: str, filter: dict) -> dict:
    if not filter:
        raise HTTPException(422, "filter must not be empty")
    table = _load_table(table_name)
    stmt = _apply_filter(delete(table), table, filter)
    with engine.begin() as conn:
        result = conn.execute(stmt)
    return {"message": f"{result.rowcount} row(s) deleted"}
