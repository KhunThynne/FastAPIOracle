from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData, select
from database import Base, engine, get_db

app = FastAPI()

metadata = MetaData()

# Define table structure
table = Table(
    'table', metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('name', String, index=True),
    Column('description', String),
)

metadata.create_all(bind=engine)


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    query = select([table])
    result = db.execute(query).fetchall()
    return result


@app.post("/items/")
def create_item(name: str, description: str, db: Session = Depends(get_db)):
    insert_stmt = table.insert().values(name=name, description=description)
    db.execute(insert_stmt)
    db.commit()
    return {"message": "Item created successfully"}
