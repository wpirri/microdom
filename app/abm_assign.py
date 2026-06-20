from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
CREATE TABLE IF NOT EXISTS TB_DOM_ASSIGN (
Id integer primary key,
Objeto varchar(128) NOT NULL,               -- Nombre para identificarlo en el sistema
Dispositivo integer NOT NULL,               -- Discpositivo - Id de TB_DOM_PERIF
Port varchar(128) NOT NULL,                 -- Nombre con el que se identifica en el dispositivo
Tipo integer NOT NULL,                      -- 0=Output, 1=Input, 2=Analog, 3=Output Alarma, 4=Input Alarma, 5=Output Pulse/Analog_Mult_Div_Valor=Pulse Param, 6=Periferico
Estado integer DEFAULT 0,                   -- 1 / 0 para digitales 0 a n para analogicos
Estado_HW integer DEFAULT 0,                -- Estado reportado por el HW
Perif_Data varchar(128),
Icono_Apagado varchar(32),
Icono_Encendido varchar(32),
Grupo_Visual integer DEFAULT 0,             -- 0=Ninguno 1=Alarma 2=Iluminación 3=Puertas 4=Climatización 5=Cámaras 6=Riego
Planta integer DEFAULT 0,
Cord_x integer DEFAULT 0,
Cord_y integer DEFAULT 0,
Coeficiente integer DEFAULT 0,              -- 1=Coeficiente Positivo, -1=Coeficiente Negativo  - rc = Coeficiente * ( (Analog_Mult_Div)?Estado/Analog_Mult_Div_Valor:Estado*Analog_Mult_Div_Valor )
Analog_Mult_Div integer DEFAULT 0,          -- 0=Multiplicar por valor, 1=Dividir por valor
Analog_Mult_Div_Valor integer DEFAULT 1,    -- Parámetro para coeficiente si Tipo=2, Tiempo si Tipo=5
Actualizar integer DEFAULT 0,                   -- Enviar update de config al HW por este PORT
Flags integer DEFAULT 0,
FOREIGN KEY(Dispositivo) REFERENCES TB_DOM_PERIF(Id),
FOREIGN KEY(Grupo_Visual) REFERENCES TB_DOM_GRUPO_VISUAL(Id),
UNIQUE INDEX idx_assign_id (Id)
);
"""

def get_assign_list():
    query = """SELECT ASS.Id, ASS.Objeto, HW.Dispositivo, ASS.Port, ASS.Tipo 
                FROM TB_DOM_ASSIGN AS ASS, TB_DOM_PERIF AS HW 
                WHERE ASS.Dispositivo = HW.Id 
                ORDER BY ASS.Objeto ASC;"""
    query_result = mysql_query(query);
    return {"error": 0, "message": "Ok", "response": query_result}

def get_assign_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_ASSIGN")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_assign(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_ASSIGN WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_assign(data):
    next_id = mysql_next_id('TB_DOM_ASSIGN')
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
    query = f"INSERT INTO TB_DOM_ASSIGN ({campos_str}) VALUES ({valores_str})"

    logger.info(f"[add_assign] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_assign(data):
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
    query = f"UPDATE TB_DOM_ASSIGN SET {campos_valores_str} WHERE Id = {Id}"

    logger.info(f"[update_assign] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_assign(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_ASSIGN WHERE Id = {Id}"
    logger.info(f"[delete_assign] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}
