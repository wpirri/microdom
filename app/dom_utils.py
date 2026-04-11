from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query

logger = get_daily_logger()

"""
        CREATE TABLE IF NOT EXISTS TB_DOM_PERIF (
            Id integer primary key,
            MAC varchar(16) NOT NULL,                       -- MAC Address
            Dispositivo varchar(128) NOT NULL,
            Tipo integer DEFAULT 0,                         -- 0=Ninguno, 1=Wifi 2=RBPi 3=DSC 4=Garnet
            Estado integer DEFAULT 0,                       -- 0=Offline
            Direccion_IP varchar(16) DEFAULT "0.0.0.0",
            Ultimo_Ok integer DEFAULT 0,
            Usar_Https integer DEFAULT 0,
            Habilitar_Wiegand integer DEFAULT 0,
            Update_Firmware integer DEFAULT 0,
            Update_WiFi integer DEFAULT 0,
            Update_Config integer DEFAULT 0,
            Informacion varchar(1024),
            UNIQUE INDEX idx_perif_id (Id),
            UNIQUE INDEX idx_perif_mac (MAC)
        );

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

        CREATE TABLE IF NOT EXISTS TB_DOM_FLAG (
        Id integer primary key,
        Variable varchar(128) NOT NULL,
        Valor integer DEFAULT 0,
        UNIQUE INDEX idx_flag_id (Id)
        );

        CREATE TABLE IF NOT EXISTS TB_DOM_EVENT (
        Id integer primary key,
        Evento varchar(128) NOT NULL,
        Objeto_Origen integer DEFAULT 0,
        Objeto_Destino integer  DEFAULT 0,      -- Solo uno de los cinco assign, grupo, Funcion, Particion, Variable
        Grupo_Destino integer  DEFAULT 0,       -- Solo uno de los cinco assign, grupo, Funcion, Particion, Variable
        Particion_Destino integer  DEFAULT 0,   -- Solo uno de los cinco assign, grupo, Funcion, Particion, Variable
        Variable_Destino integer  DEFAULT 0,    -- Solo uno de los cinco assign, grupo, Funcion, Particion, Variable
        ON_a_OFF integer DEFAULT 0,
        OFF_a_ON integer DEFAULT 0,
        Enviar integer DEFAULT 0,               -- Evento a enviar 
                                                --      0=Nada 
                                                --      1=On 
                                                --      2=Off 
                                                --      3=Switch 
                                                --      4=Pulso a Objeto o Grupo. Si no Variable = Enviar
        Parametro_Evento integer DEFAULT 0,     -- Se pasa si es Variable o Funcion
        Condicion_Variable integer DEFAULT 0,             -- Condiciona el evento
        Condicion_Igualdad integer DEFAULT 0,             -- 0 ==, 1 >, 2 <
        Condicion_Valor integer DEFAULT 0,                -- Valor de condicion
        Filtro_Repeticion integer DEFAULT 0,              -- Segundos para ignorar repeticiones
        Ultimo_Evento  integer DEFAULT 0,
        Flags integer DEFAULT 0,
        FOREIGN KEY(Objeto_Origen) REFERENCES TB_DOM_ASSIGN(Id),
        FOREIGN KEY(Objeto_Destino) REFERENCES TB_DOM_ASSIGN(Id),
        FOREIGN KEY(Grupo_Destino) REFERENCES TB_DOM_GROUP(Id),
        FOREIGN KEY(Particion_Destino) REFERENCES TB_DOM_ALARM_PARTICION(Id),
        FOREIGN KEY(Variable_Destino) REFERENCES TB_DOM_FLAG(Id),
        UNIQUE INDEX idx_event_id (Id)
        );

"""
def change_assign_by_id(id, accion, parametro=0):
    if accion == 1:
        logger.info(f"[change_assign_by_id] Encender: {id}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = 1 WHERE Id = {id}")
    elif accion == 2:
        logger.info(f"[change_assign_by_id] Apagar: {id}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = 0 WHERE Id = {id}")
    elif accion == 3:
        logger.info(f"[change_assign_by_id] Alternar: {id}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = (1 - Estado) WHERE Id = {id}")
    elif accion == 4:
        logger.info(f"[change_assign_by_id] Pulso de: {parametro}s a: {id}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = (1 + {parametro}) WHERE Id = {id}")
    else:
        logger.warning(f"change_assign_by_id: acción desconocida {accion} para Id={id}")

def change_assign_by_name(name, accion, parametro=0):
    if accion == 1:
        logger.info(f"[change_assign_by_name] Encender: {name}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = 1 WHERE Objeto = '{name}'")
    elif accion == 2:
        logger.info(f"[change_assign_by_name] Apagar: {name}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = 0 WHERE Objeto = '{name}'")
    elif accion == 3:
        logger.info(f"[change_assign_by_name] Alternar: {name}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = (1 - Estado) WHERE Objeto = '{name}'")
    elif accion == 4:
        logger.info(f"[change_assign_by_name] Pulso de: {parametro}s a: {name}")
        mysql_execute(f"UPDATE TB_DOM_ASSIGN SET Estado = (1 + {parametro}) WHERE Objeto = '{name}'")
    else:
        logger.warning(f"change_assign_by_name: acción desconocida {accion} para Objeto={name}")

def change_group_by_id(id, accion):
    estado = 0

    return estado

def change_partition_by_id(id, accion):
    estado = 0

    return estado

def change_flag_by_id(id, accion):
    estado = 0

    return estado

def check_hw(mac_addr, ip_address, info):
    # Verificar si el periférico ya existe
    if mac_addr != None:
        query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE MAC = '{mac_addr}'")
    else:
        query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE Direccion_IP = '{ip_address}'")

    if query_result:
        if query_result[0]["Estado"] == 0:
            logger.info(f"HW: {query_result[0]['Dispositivo']} OFFLINE -> ONLINE")
        # Actualizar el periférico existente
        mysql_execute(f"UPDATE TB_DOM_PERIF SET Direccion_IP = '{ip_address}', Ultimo_Ok = UNIX_TIMESTAMP(), Estado = 1, Informacion = '{info}' WHERE MAC = '{mac_addr}'")
        return query_result[0]['Id'] 
    else:
        # HW no existe
        return None

def check_io_event(mac, io, status):
    logger.info(f"[check_io_event] MAC: {mac} IO: {io} Status: {status}")
    cambio = "OFF_a_ON" if str(status) == "1" else "ON_a_OFF"
    query = (
        "SELECT EV.Enviar, EV.Objeto_Destino, EV.Grupo_Destino, EV.Particion_Destino, "
        "EV.Variable_Destino, EV.Parametro_Evento "
        "FROM TB_DOM_PERIF AS HW "
        "JOIN TB_DOM_ASSIGN AS ASS ON HW.Id = ASS.Dispositivo "
        "JOIN TB_DOM_EVENT AS EV ON ASS.Id = EV.Objeto_Origen "
        f"WHERE EV.{cambio} = 1 AND ASS.Port = %s AND HW.MAC = %s;"
    )
    query_result = mysql_query(query, (io, mac))

    if not query_result:
        return None

    for i in range(0, len(query_result)):
        logger.info(f"[check_io_event] Evento: {i} - Accion: {query_result[i]['Objeto_Destino']}, {query_result[i]['Enviar']}")
        # TODO: procesar cada evento según EV.Enviar, Objeto_Destino, Grupo_Destino, etc.
        if query_result[i]['Objeto_Destino']:
            change_assign_by_id(query_result[i]['Objeto_Destino'], query_result[i]['Enviar'])
            pass
        if query_result[i]['Grupo_Destino']:
            # Procesar evento para grupo
            pass
        if query_result[i]['Particion_Destino']:
            # Procesar evento para partición
            pass
        if query_result[i]['Variable_Destino']:
            # Procesar evento para variable
            pass


    return query_result

def analyze_event(mac, changes, io1, io2, io3, io4, io5, io6, io7, io8, out1, out2, out3, out4, out5, out6, out7, out8):
    if changes != None:
        logger.info(f"[analyze_event] MAC: {mac} Cambios: {changes}")
        for i in range(1, 9):
            if f"IO{i}" in changes:
                check_io_event(mac, f"IO{i}", eval(f"io{i}"))
            if f"OUT{i}" in changes:
                check_io_event(mac, f"OUT{i}", eval(f"out{i}"))

def get_hw_io_status(hw_mac_addr):
    resp = "error=0&message=Ok"

    query_result = mysql_query(f"SELECT Port, Estado FROM TB_DOM_ASSIGN WHERE Dispositivo = (SELECT Id FROM TB_DOM_PERIF WHERE MAC = '{hw_mac_addr}')")
    if query_result:
        resp += "&" + "&".join([f"{item['Port']}={item['Estado']}" for item in query_result])
        return {resp}
    else:
        return {"error=0&message=Ok"}


def get_assign_status():
    query_result = mysql_query("SELECT Id, Objeto, Port, Icono_Apagado, Icono_Encendido, Estado, Tipo, Perif_Data FROM TB_DOM_ASSIGN")
    if query_result:
        return {
            "error": 0,
            "message": "Ok",
            "response": query_result if query_result else [] ,
        }
    else:
        return {"error": 0, "message": "Ok", "response": []}
    
def get_assign_info_id(id, planta):
    if id:
        query_result = mysql_query(f"SELECT Id,Objeto,Tipo,Icono_Apagado,Icono_Encendido,Grupo_Visual,Planta,Cord_x,Cord_y FROM TB_DOM_ASSIGN WHERE Id = {id};")
    else:
        if planta:
            query_result = mysql_query(f"SELECT Id,Objeto,Tipo,Icono_Apagado,Icono_Encendido,Grupo_Visual,Planta,Cord_x,Cord_y FROM TB_DOM_ASSIGN WHERE Planta = {planta};")
        else:
            query_result = mysql_query("SELECT Id,Objeto,Tipo,Icono_Apagado,Icono_Encendido,Grupo_Visual,Planta,Cord_x,Cord_y FROM TB_DOM_ASSIGN;")

    if query_result:
        return {
            "error": 0,
            "message": "Ok",
            "response": query_result if query_result else [] ,
        }
    else:
        return {"error": 0, "message": "Ok", "response": []}

def get_sys_config():
    query_result = mysql_query("SELECT * FROM TB_DOM_CONFIG ORDER BY Id DESC LIMIT 1;")
    if query_result:
        return {
            "error": 0,
            "message": "Ok",
            "response": query_result[0],
        }
    else:
        return {"error": 0, "message": "Ok", "response": {}}
