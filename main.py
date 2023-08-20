# main.py

from fastapi import FastAPI, HTTPException
import pyodbc
from pydantic import BaseModel


server = 'erikauin'
database = 'DBTec'
username = 'sa'
password = 'Erikauin123*'

#database connection
connection_string = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection = pyodbc.connect(connection_string)


# --------------------------------
app = FastAPI()

class ArticuloDetalle(BaseModel):
    descripcion: str
    precio: float

class Articulo(ArticuloDetalle):
    id: int
    descripcion: str
    precio: float

def get_articulo_by_id(articulo_id: int):
    cursor = connection.cursor()
    cursor.execute("EXEC GetArticulo @id = ?", (articulo_id) )
    row = cursor.fetchone()
    if row:
        return Articulo(id=row.id, descripcion=row.descripcion, precio=(row.precio+7))
    return None

# FastAPI obtener un articulo por ID
@app.get("/articulos/{articulo_id}")
async def get_articulo(articulo_id: int):
    articulo = get_articulo_by_id(articulo_id)
    if articulo:
        return articulo
    else:
    #raise HTTPException(status_code=404, detail="Articulo no encontrado")    
        return {"errorcode":2, "mensaje":"Articulo no encontrado"}


def insertar_articulo(articulo: ArticuloDetalle): 
    cursor = connection.cursor()
    cursor.execute("EXEC InsertArticulo @Descripcion=?, @Precio=?", articulo.descripcion, articulo.precio)
    row = cursor.fetchone()
    cursor.commit()
    if row:
        return {"id":row.id}
    

# Insertar un articulo
@app.post("/articulos")
async def insertar_articulo_post(articulo: ArticuloDetalle):
    resultado = insertar_articulo(articulo)
    if resultado:
        return resultado
    else:
    #raise HTTPException(status_code=400, detail="Articulo no insertado")
        return {"errorcode":1, "mensaje":"Articulo no insertado"}

# obtener todos los articulos
@app.get("/articulos")
async def obtener_articulos():
    cursor = connection.cursor()
    cursor.execute("EXEC GetArticulos")
    rows = cursor.fetchall()
    #articulos = [{"id": row.id, "descripcion": row.descripcion, "precio": row.precio} for row in rows]
    articulos = [Articulo(id=row.id, descripcion=row.descripcion, precio=(row.precio+3)) for row in rows]
    return articulos


# -----------------------------------

#uvicorn main:app --host 127.0.0.1 --port 8050
#http://127.0.0.1:8050/articulos
#http://127.0.0.1:8050/articulos/2
#http://127.0.0.1:8050/articulos POST: {"descripcion":"articulo 5","precio":2350}

