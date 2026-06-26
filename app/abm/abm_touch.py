from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
CREATE TABLE IF NOT EXISTS TB_DOM_TOUCH (
Dispositivo integer,
Pantalla integer,
Boton integer,
Evento integer DEFAULT 0,                -- 0=Nada 1=On 2=Off 3=Switch 4=Pulso 10=Config 11=Home 12=Prev 13=Next
Objeto integer DEFAULT 0,
X integer DEFAULT 0,
Y integer DEFAULT 0,
W integer DEFAULT 0,
H integer DEFAULT 0,
Redondo integer DEFAULT 0,
Texto varchar(16),
Icono varchar(16),
Color_pantalla integer DEFAULT 0,
Color_borde integer DEFAULT 0,
Color_fondo integer DEFAULT 0,
Color_texto integer DEFAULT 0,
Orientacion integer DEFAULT 0,
UNIQUE INDEX idx_touch_id (Dispositivo,Pantalla,Boton),
FOREIGN KEY(Dispositivo) REFERENCES TB_DOM_PERIF(Id),
FOREIGN KEY(Objeto) REFERENCES TB_DOM_ASSIGN(Id)
);

"""

def get_touch_list(id, pantalla):
    if id:
        if pantalla:
            query =  ("SELECT T.Boton, T.Boton AS Nro, T.Texto, Evento, A.Objeto "
                "FROM TB_DOM_TOUCH AS T, TB_DOM_ASSIGN AS A "
                "WHERE T.Objeto = A.Id "
                f"AND T.Dispositivo = {id} AND T.Pantalla = {pantalla} "
                "ORDER BY Boton;")
        else:
            query = ("SELECT Pantalla, Pantalla AS Nro, COUNT(*) AS Botones "
                "FROM TB_DOM_TOUCH "
                f"WHERE Dispositivo = {id} "
                "GROUP BY Pantalla ORDER BY Pantalla;")
    else:
        query = """SELECT Id, Dispositivo, Direccion_IP, Estado "
            "FROM TB_DOM_PERIF "
            "WHERE Id > 0 AND Tipo = 5 "
            "ORDER BY Dispositivo ASC;"""
    query_result = mysql_query(query);
    return {"error": 0, "message": "Ok", "response": query_result}  

def get_touch_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_TOUCH")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_touch(id, pantalla, boton):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_TOUCH WHERE Dispositivo = {id} AND Pantalla = {pantalla} AND Boton = {boton};")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_touch(data):
    next_id = mysql_next_id('TB_DOM_TOUCH')
    if next_id in (None, ''):
        next_id = 1
    data['Id'] = next_id

    campos = []
    valores = []
    for key, value in data.items():
        campos.append(key)
        if isinstance(value, str):
            escaped_value = value.replace("'", "''")
            valores.append(f"'{escaped_value}'")
        else:
            valores.append(str(value))

    campos_str = ', '.join(campos)
    valores_str = ', '.join(valores)
    query = f"INSERT INTO TB_DOM_TOUCH ({campos_str}) VALUES ({valores_str})"

    #logger.info(f"[add_touch] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_touch(data):
    Id = data.get('Id')
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    campos_valores = []
    for key, value in data.items():
        if key == 'Id':
            continue
        if isinstance(value, str):
            escaped_value = value.replace("'", "''")
            campos_valores.append(f"{key} = '{escaped_value}'")
        else:
            campos_valores.append(f"{key} = {value}")

    campos_valores_str = ', '.join(campos_valores)
    query = f"UPDATE TB_DOM_TOUCH SET {campos_valores_str} WHERE Id = {Id}"

    #logger.info(f"[update_touch] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_touch(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_TOUCH WHERE Id = {Id}"
    #logger.info(f"[delete_touch] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}
