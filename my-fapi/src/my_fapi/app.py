from fastapi import FastAPI

from my_fapi import db, tb

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from my-fapi-Nikhil!"}


# --- Databases ---


@app.get("/databases")
def list_databases():
    return db.list_databases()


@app.post("/databases")
def create_database(payload: db.DatabaseCreate):
    return db.create_database(payload)


@app.delete("/databases/{db_name}")
def delete_database(db_name: str):
    return db.delete_database(db_name)


# --- Tables ---


@app.get("/tables")
def list_tables():
    return tb.list_tables()


@app.post("/tables")
def create_table(payload: tb.TableCreate):
    return tb.create_table(payload)


@app.put("/tables/{table_name}")
def alter_table(table_name: str, payload: tb.TableAlter):
    return tb.alter_table(table_name, payload)


@app.delete("/tables/{table_name}")
def delete_table(table_name: str):
    return tb.delete_table(table_name)


# --- Rows ---


@app.post("/tables/{table_name}/rows")
def create_row(table_name: str, row: dict):
    return tb.create_row(table_name, row)


@app.get("/tables/{table_name}/rows")
def list_rows(table_name: str):
    return tb.list_rows(table_name)


# Registered before /rows/{row_id} so a literal "query" path segment
# matches these routes first, rather than being swallowed by {row_id}.
@app.post("/tables/{table_name}/rows/query")
def query_rows(table_name: str, payload: tb.RowQuery):
    return tb.query_rows(table_name, payload.filter)


@app.put("/tables/{table_name}/rows/query")
def update_rows_by_filter(table_name: str, payload: tb.RowUpdateByFilter):
    return tb.update_rows_by_filter(table_name, payload.filter, payload.values)


@app.delete("/tables/{table_name}/rows/query")
def delete_rows_by_filter(table_name: str, payload: tb.RowQuery):
    return tb.delete_rows_by_filter(table_name, payload.filter)


@app.get("/tables/{table_name}/rows/{row_id}")
def get_row(table_name: str, row_id: str):
    return tb.get_row(table_name, row_id)


@app.put("/tables/{table_name}/rows/{row_id}")
def update_row(table_name: str, row_id: str, row: dict):
    return tb.update_row(table_name, row_id, row)


@app.delete("/tables/{table_name}/rows/{row_id}")
def delete_row(table_name: str, row_id: str):
    return tb.delete_row(table_name, row_id)
