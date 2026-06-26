from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
-- Sistema de riego
-- Calefaccion
-- Aire acondicionado
-- Fotocelula
CREATE TABLE IF NOT EXISTS TB_DOM_AUTO (
Id integer primary key,
Objeto varchar(128) NOT NULL,               -- Nombre para identificarlo en el sistema
Tipo integer default 0,                     -- 0 = Riego 1 = Calefaccion 2 = Aire acondicionado 3 = Fotocelula
Objeto_Sensor integer default 0,             -- Discpositivo - Id de input de TB_DOM_ASSIGN
Objeto_Salida integer default 0,             -- Discpositivo - Id de TB_DOM_ASSIGN
Grupo_Salida integer default 0,              -- Grupo - Id de TB_DOM_GROUP
Particion_Salida integer default 0,          -- Particion - Id de TB_DOM_ALARM_PARTICION
Variable_Salida integer default 0,           -- Variable - Id de TB_DOM_FLAG
Parametro_Evento integer default 0,         -- Se pasa si es Variable o Funcion
Min_Sensor integer DEFAULT 0,
Enviar_Min integer default 0,               -- Accion a enviar al pasar el minimo
Max_Sensor integer DEFAULT 0,
Enviar_Max integer default 0,               -- Accion a enviar al pasar el màximo
Hora_Inicio integer DEFAULT 0,
Minuto_Inicio integer DEFAULT 0,
Hora_Fin integer DEFAULT 0,
Minuto_Fin integer DEFAULT 0,
Dias_Semana varchar(128),                   -- Lu,Ma,Mi,Ju,Vi,Sa,Do
Condicion_Variable integer DEFAULT 0,       -- Condiciona el evento
Condicion_Igualdad integer DEFAULT 0,       -- ==, >, <
Condicion_Valor integer DEFAULT 0,          -- Valor de condicion
Estado integer DEFAULT 0,                   -- 0= Salida apagada 1= Salida encendida
Habilitado integer DEFAULT 1,               -- 0=Apagado 1=Automatico 2=Encendido
Icono_Apagado varchar(32),
Icono_Encendido varchar(32),
Icono_Auto varchar(32),
Grupo_Visual integer DEFAULT 0,             -- 0=Ninguno 1=Alarma 2=Iluminación 3=Puertas 4=Climatización 5=Cámaras 6=Riego
Planta integer DEFAULT 0,
Cord_x integer DEFAULT 0,
Cord_y integer DEFAULT 0,
Actualizar integer DEFAULT 0,
Flags integer DEFAULT 0,
FOREIGN KEY(Objeto_Salida) REFERENCES TB_DOM_ASSIGN(Id),
FOREIGN KEY(Grupo_Salida) REFERENCES TB_DOM_GROUP(Id),
FOREIGN KEY(Particion_Salida) REFERENCES TB_DOM_ALARM_PARTICION(Id),
FOREIGN KEY(Variable_Salida) REFERENCES TB_DOM_FLAG(Id),
FOREIGN KEY(Objeto_Sensor) REFERENCES TB_DOM_ASSIGN(Id),
FOREIGN KEY(Grupo_Visual) REFERENCES TB_DOM_GRUPO_VISUAL(Id),
UNIQUE INDEX idx_auto_id (Id)
);
"""

"""
SELECT AU.Id AS Id, AU.Objeto AS Nombre, AU.Habilitado AS Control, AU.Estado AS Estado 
FROM TB_DOM_AUTO AS AU, TB_DOM_ASSIGN AS ASS 
WHERE (AU.Objeto_Salida = ASS.Id AND AU.Id = 0) OR 
(AU.Objeto_Salida = ASS.Id AND AU.Tipo = {tipo}) 
ORDER BY AU.Objeto ASC;

SELECT AU.Id AS Id, AU.Objeto AS Nombre, AU.Habilitado AS Control, AU.Estado AS Estado 
FROM TB_DOM_AUTO AS AU, TB_DOM_ASSIGN AS ASS 
WHERE (AU.Objeto_Salida = ASS.Id AND AU.Id = 0) OR 
(AU.Objeto_Salida = ASS.Id) 
ORDER BY AU.Objeto ASC;
"""

def get_auto_list(tipo):
    if tipo:
        query = ("SELECT AU.Id AS Id, AU.Objeto AS Nombre, AU.Habilitado AS Control, AU.Estado AS Estado "
            "FROM TB_DOM_AUTO AS AU, TB_DOM_ASSIGN AS ASS "
            "WHERE (AU.Objeto_Salida = ASS.Id AND AU.Id = 0) OR "
            f"(AU.Objeto_Salida = ASS.Id AND AU.Tipo = {tipo}) "
            "ORDER BY AU.Objeto ASC;")
    else:
        query = """SELECT AU.Id AS Id, AU.Objeto AS Nombre, AU.Habilitado AS Control, AU.Estado AS Estado 
            FROM TB_DOM_AUTO AS AU, TB_DOM_ASSIGN AS ASS 
            WHERE (AU.Objeto_Salida = ASS.Id AND AU.Id = 0) OR 
            AU.Objeto_Salida = ASS.Id 
            ORDER BY AU.Objeto ASC;
            """
    query_result = mysql_query(query);
    return {"error": 0, "message": "Ok", "response": query_result}  

def get_auto_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_AUTO")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_auto(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_AUTO WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_auto(data):
    next_id = mysql_next_id('TB_DOM_AUTO')
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
    query = f"INSERT INTO TB_DOM_AUTO ({campos_str}) VALUES ({valores_str})"

    #logger.info(f"[add_auto] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_auto(data):
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
    query = f"UPDATE TB_DOM_AUTO SET {campos_valores_str} WHERE Id = {Id}"

    #logger.info(f"[update_auto] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_auto(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_AUTO WHERE Id = {Id}"
    #logger.info(f"[delete_auto] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}
