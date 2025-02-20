from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time

LOG_FILE = 'logs/log.txt'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    text: str

def get_db_connection():
    while True:
        try:
            return psycopg2.connect(
                host="db",
                database="shopping",
                user="postgres",
                password="postgres",
                cursor_factory=RealDictCursor
            )
        except psycopg2.OperationalError:
            print("Waiting for database...")
            time.sleep(1)

conn = None
cursor = None

@app.on_event("startup")
async def startup():
    global conn, cursor
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id SERIAL PRIMARY KEY,
            text VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()

@app.on_event("shutdown")
async def shutdown():
    if cursor:
        cursor.close()
    if conn:
        conn.close()

@app.get("/items")
def read_items():
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return items

@app.post("/items")
def create_item(item: Item):
    cursor.execute("INSERT INTO items (text) VALUES (%s) RETURNING *", (item.text,))
    new_item = cursor.fetchone()
    conn.commit()

    with open(LOG_FILE, 'a') as f:
        f.write(f'Created item {item.text}\n')


    return new_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    cursor.execute("DELETE FROM items WHERE id = %s RETURNING *", (item_id,))
    deleted_item = cursor.fetchone()
    if deleted_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    conn.commit()

    with open(LOG_FILE, 'a') as f:
        f.write(f'Deleted item with id {item_id}\n')

    return {"message": "Item deleted"}

