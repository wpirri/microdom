from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
from app.abm.abm_assign import change_assign_by_id
from app.abm.abm_group import change_group_by_id

logger = get_daily_logger()

def check_io_event(mac, io, status):
    logger.info(f"[check_io_event] EVENTO: HW: {mac} Port: {io} Status: {status}")
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
        if query_result[i]['Objeto_Destino']:
            logger.info(f"[check_io_event] ACCION: Enviar: {query_result[i]['Enviar']} a Objeto: {query_result[i]['Objeto_Destino']}")
            change_assign_by_id(query_result[i]['Objeto_Destino'], query_result[i]['Enviar'], query_result[i]['Parametro_Evento'])
            pass
        if query_result[i]['Grupo_Destino']:
            logger.info(f"[check_io_event] ACCION: Enviar: {query_result[i]['Enviar']} a Grupo: {query_result[i]['Grupo_Destino']}")
            change_group_by_id(query_result[i]['Grupo_Destino'], query_result[i]['Enviar'], query_result[i]['Parametro_Evento'])
            pass
        if query_result[i]['Particion_Destino']:
            logger.info(f"[check_io_event] ACCION: Enviar: {query_result[i]['Enviar']} a Particion: {query_result[i]['Particion_Destino']}")
            # TODO: Procesar evento para partición
            pass
        if query_result[i]['Variable_Destino']:
            logger.info(f"[check_io_event] ACCION: Enviar: {query_result[i]['Enviar']} a Variable: {query_result[i]['Variable_Destino']}")
            # TODO: Procesar evento para variable
            pass


    return query_result

def analyze_event(mac, changes, io1, io2, io3, io4, io5, io6, io7, io8, out1, out2, out3, out4, out5, out6, out7, out8):
    if changes != None:
        #logger.info(f"[analyze_event] MAC: {mac} Cambios: {changes}")
        for i in range(1, 9):
            if f"IO{i}" in changes:
                check_io_event(mac, f"IO{i}", eval(f"io{i}"))
            if f"OUT{i}" in changes:
                check_io_event(mac, f"OUT{i}", eval(f"out{i}"))

def get_hw_io_status(hw_mac_addr):
    resp = "error=0&message=Ok"

    query_result = mysql_query(f"SELECT Port, Estado, Tipo FROM TB_DOM_ASSIGN WHERE (Tipo = 0 OR Tipo = 3 OR Tipo = 5) AND Dispositivo = (SELECT Id FROM TB_DOM_PERIF WHERE MAC = '{hw_mac_addr}')")
    if query_result:
        resp += "&" + "&".join([f"{item['Port']}={item['Estado']}" for item in query_result])
        return resp
    else:
        return "error=0&message=Ok"

def get_hw_update_data(hw_mac_addr):
    resp = ""
    query_result = mysql_query(f"SELECT Tipo, Update_Firmware, Update_WiFi, Update_Config FROM TB_DOM_PERIF WHERE MAC = '{hw_mac_addr}'")
    if query_result:
        if query_result[0]['Update_Firmware'] == 1:
            logger.info(f"Solicitando actualizacion de firmware a: {hw_mac_addr}")
            resp = "&update=firmware"
            mysql_execute(f"UPDATE TB_DOM_PERIF SET Update_Firmware = 0 WHERE MAC = '{hw_mac_addr}'")
        elif query_result[0]['Update_WiFi'] == 1:
            logger.info(f"Solicitando actualizacion de WiFi a: {hw_mac_addr}")
            config_result = mysql_query("SELECT * FROM TB_DOM_CONFIG ORDER BY Id DESC LIMIT 1;")
            if config_result:
                config = config_result[0]
                resp += f"&ap1={config.get('Wifi_AP1', '')}"
                resp += f"&ap1p={config.get('Wifi_AP1_Pass', '')}"
                resp += f"&ap2={config.get('Wifi_AP2', '')}"
                resp += f"&ap2p={config.get('Wifi_AP2_Pass', '')}"
                resp += f"&ce1={config.get('Home_Host_1_Address', '')}"
                resp += f"&ce2={config.get('Home_Host_2_Address', '')}"
                #
                if query_result[0]['Tipo'] == 1:
                    resp += f"&rep=1"
                elif query_result[0]['Tipo'] == 5:
                    resp += f"&rep={config.get('Wifi_Report', '')}"
                #
                resp += f"&path={config.get('Rqst_Path', '')}"
            mysql_execute(f"UPDATE TB_DOM_PERIF SET Update_WiFi = 0 WHERE MAC = '{hw_mac_addr}'")
        elif query_result[0]['Update_Config'] == 1:
            logger.info(f"Solicitando actualizacion de configuracion de I/O a: {hw_mac_addr}")
            config_result = mysql_query(f"SELECT A.Port, A.Tipo FROM TB_DOM_ASSIGN AS A, TB_DOM_PERIF AS P WHERE A.Dispositivo = P.Id AND P.MAC = '{hw_mac_addr}';")
            if config_result:
                for item in config_result:
                    tipo = "x"
                    if item['Tipo'] == 0 or item['Tipo'] == 3 or item['Tipo'] == 5:
                        tipo = "o"
                    elif item['Tipo'] == 1 or item['Tipo'] == 4:
                        tipo = "i"
                    elif item['Tipo'] == 3:
                        tipo = "a"
                    if tipo != "x":
                        resp += f"&cfg{item['Port']}={tipo}"
            mysql_execute(f"UPDATE TB_DOM_PERIF SET Update_Config = 0 WHERE MAC = '{hw_mac_addr}'")
    return resp

def get_assign_status_id(id, planta):
    if id:
        query_result = mysql_query(f"SELECT Id, Objeto, Port, Icono_Apagado, Icono_Encendido, Estado, Tipo, Perif_Data, Analog_Mult_Div_Valor FROM TB_DOM_ASSIGN WHERE Id = {id};")
    else:
        if planta:
            query_result = mysql_query(f"SELECT Id, Objeto, Port, Icono_Apagado, Icono_Encendido, Estado, Tipo, Perif_Data, Analog_Mult_Div_Valor FROM TB_DOM_ASSIGN WHERE Planta = {planta};")
        else:  
            query_result = mysql_query("SELECT Id, Objeto, Port, Icono_Apagado, Icono_Encendido, Estado, Tipo, Perif_Data, Analog_Mult_Div_Valor FROM TB_DOM_ASSIGN")
    return {"error": 0, "message": "Ok", "response": query_result if query_result else []}
    
def get_assign_info_id(id, planta):
    if id:
        query_result = mysql_query(f"SELECT Id,Objeto,Tipo,Icono_Apagado,Icono_Encendido,Grupo_Visual,Planta,Cord_x,Cord_y FROM TB_DOM_ASSIGN WHERE Id = {id};")
    else:
        if planta:
            query_result = mysql_query(f"SELECT Id,Objeto,Tipo,Icono_Apagado,Icono_Encendido,Grupo_Visual,Planta,Cord_x,Cord_y FROM TB_DOM_ASSIGN WHERE Planta = {planta};")
        else:
            query_result = mysql_query("SELECT Id,Objeto,Tipo,Icono_Apagado,Icono_Encendido,Grupo_Visual,Planta,Cord_x,Cord_y FROM TB_DOM_ASSIGN;")

    return {"error": 0, "message": "Ok", "response": query_result if query_result else []}
