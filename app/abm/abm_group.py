from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
from app.abm.abm_assign import change_assign_by_id

logger = get_daily_logger()

"""
CREATE TABLE IF NOT EXISTS TB_DOM_GROUP (
Id integer primary key,
Grupo varchar(128) NOT NULL,
Listado_Objetos varchar(256),       -- Id de assign separados por , (comas)
Estado integer DEFAULT 0,            -- Define el estado que deben tener los objetos del grupo
Icono_Apagado varchar(32),
Icono_Encendido varchar(32),
Grupo_Visual integer DEFAULT 0,             -- 0=Ninguno 1=Alarma 2=Iluminación 3=Puertas 4=Climatización 5=Cámaras 6=Riego
Planta integer DEFAULT 0,
Cord_x integer DEFAULT 0,
Cord_y integer DEFAULT 0,
Actualizar integer DEFAULT 0,
UNIQUE INDEX idx_group_id (Id)
);
"""

def get_group_list():
    query_result = mysql_query("SELECT Id, Grupo FROM TB_DOM_GROUP ORDER BY Grupo ASC;");
    return {"error": 0, "message": "Ok", "response": query_result}

def get_group_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_GROUP")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_group(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_GROUP WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_group(data):
    next_id = mysql_next_id('TB_DOM_GROUP')
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
    query = f"INSERT INTO TB_DOM_GROUP ({campos_str}) VALUES ({valores_str})"

    #logger.info(f"[add_group] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_group(data):
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
    query = f"UPDATE TB_DOM_GROUP SET {campos_valores_str} WHERE Id = {Id}"

    #logger.info(f"[update_group] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_group(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_GROUP WHERE Id = {Id}"
    #logger.info(f"[delete_group] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def change_group_by_id(id, accion, parametro=0):
    query_result = mysql_query(f"SELECT Estado, Listado_Objetos FROM TB_DOM_GROUP WHERE Id = {id};");
    estado_grupo = query_result[0]['Estado']
    objetos = query_result[0]['Listado_Objetos'].split(",")

    if accion == 1:
        logger.info(f"[change_group_by_id] Encender: {id}")
        estado_grupo = 1
    elif accion == 2:
        logger.info(f"[change_group_by_id] Apagar: {id}")
        estado_grupo = 0
    elif accion == 3:
        logger.info(f"[change_group_by_id] Alternar: {id}")
        estado_grupo = 1 - estado_grupo
    elif accion == 4:
        logger.info(f"[change_group_by_id] Pulso de: {parametro}s a: {id} - NO IMPLEMENTADO")

    else:
        logger.warning(f"change_group_by_id: acción desconocida {accion} para Id={id}")

    for obj in objetos:
        if obj:
            if estado_grupo == 1:
                logger.info(f"[change_group_by_id] Encender: {obj}")
                change_assign_by_id(obj, 1)
            elif estado_grupo == 0:
                logger.info(f"[change_group_by_id] Apagar: {obj}")
                change_assign_by_id(obj, 2)

    mysql_execute(f"UPDATE TB_DOM_GROUP SET Estado = {estado_grupo} WHERE Id = {id};")

    return len(objetos)
