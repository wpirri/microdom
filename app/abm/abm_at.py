from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id

logger = get_daily_logger()

"""
CREATE TABLE IF NOT EXISTS TB_DOM_AT (
Id integer primary key,
Agenda varchar(128) NOT NULL,
Mes integer DEFAULT 0,
Dia integer DEFAULT 0,
Hora integer DEFAULT 0,
Minuto integer DEFAULT 0,
Dias_Semana varchar(128),
Objeto_Destino integer  DEFAULT 0,        -- Solo uno de los cuatro assign, grupo, Funcion, Variable
Grupo_Destino integer  DEFAULT 0,         -- Solo uno de los cuatro assign, grupo, Funcion, Variable
Variable_Destino integer  DEFAULT 0,        -- Solo uno de los cuatro assign, grupo, Funcion, Variable
Evento integer DEFAULT 0,               -- Evento a enviar 0=Nada 1=On 2=Off 3=Switch 4=Pulso a Objeto o Grupo. Si no Variable = Enviar
Parametro_Evento integer DEFAULT 0,     -- Se pasa si es Variable o Funcion
Condicion_Variable integer DEFAULT 0,             -- Condiciona el evento
Condicion_Igualdad integer DEFAULT 0,             -- ==, >, <
Condicion_Valor integer DEFAULT 0,                -- Valor de condicion
Ultimo_Mes integer DEFAULT 0,
Ultimo_Dia integer DEFAULT 0,
Ultima_Hora integer DEFAULT 0,
Ultimo_Minuto integer DEFAULT 0,
Flags integer DEFAULT 0,
FOREIGN KEY(Objeto_Destino) REFERENCES TB_DOM_ASSIGN(Id),
FOREIGN KEY(Grupo_Destino) REFERENCES TB_DOM_GROUP(Id),
FOREIGN KEY(Variable_Destino) REFERENCES TB_DOM_FLAG(Id),
UNIQUE INDEX idx_at_id (Id)
);
"""

def get_task_list():
    query = """SELECT TASK.Id, Agenda, ASS.Objeto 
        FROM TB_DOM_AT AS TASK, TB_DOM_ASSIGN AS ASS 
        WHERE TASK.Objeto_Destino = ASS.Id 
        ORDER BY Agenda, ASS.Objeto ASC;
        """
    query_result = mysql_query(query);
    return {"error": 0, "message": "Ok", "response": query_result}

def get_task_list_all():
    query_result = mysql_query("SELECT * FROM TB_DOM_AT")
    return {"error": 0, "message": "Ok", "response": query_result}

def get_task(id):
    query_result = mysql_query(f"SELECT * FROM TB_DOM_AT WHERE Id = {id}")
    return {"error": 0, "message": "Ok", "response": query_result}

def add_task(data):
    next_id = mysql_next_id('TB_DOM_AT')
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
    query = f"INSERT INTO TB_DOM_AT ({campos_str}) VALUES ({valores_str})"

    #logger.info(f"[add_task] Insertando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok", "Id": next_id}

def update_task(data):
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
    query = f"UPDATE TB_DOM_AT SET {campos_valores_str} WHERE Id = {Id}"

    #logger.info(f"[update_task] Actualizando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}

def delete_task(Id):
    if not Id:
        return {"error": 1, "message": "Id es requerido"}

    query = f"DELETE FROM TB_DOM_AT WHERE Id = {Id}"
    #logger.info(f"[delete_task] Eliminando: {query}")
    mysql_execute(query)
    return {"error": 0, "message": "Ok"}
