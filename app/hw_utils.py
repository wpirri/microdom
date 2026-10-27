import asyncio
import time
import threading
from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
from fastapi.responses import Response

logger = get_daily_logger()

tabla_perif = []
_tabla_perif_lock = threading.Lock()

def init_hw_status():
    mysql_execute("UPDATE TB_DOM_PERIF SET Estado = 0;")
    with _tabla_perif_lock:
        tabla_perif.clear()

def check_hw(mac_addr, ip_address, info):
    # Verificar si el periférico ya existe
    if mac_addr != None:
        query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE MAC = '{mac_addr}'")
    else:
        query_result = mysql_query(f"SELECT * FROM TB_DOM_PERIF WHERE Direccion_IP = '{ip_address}'")

    if query_result:
        ahora = int(time.time())
        mac_key = (mac_addr if mac_addr is not None else query_result[0]["MAC"]).upper()
        Dispositivo = query_result[0]['Dispositivo']
        cambiar_estado = False

        with _tabla_perif_lock:
            perif = next((p for p in tabla_perif if p["MAC"] == mac_key), None)
            if perif is None:
                perif = {"MAC": mac_key, "Dispositivo": Dispositivo, "Ultimo_Ok": ahora, "Estado": 1}
                tabla_perif.append(perif)
                cambiar_estado = True
            else:
                perif["Dispositivo"] = Dispositivo
                perif["Ultimo_Ok"] = ahora
                if perif["Estado"] == 0 or query_result[0]["Estado"] == 0:
                    perif["Estado"] = 1
                    cambiar_estado = True

        if cambiar_estado:
            logger.info(f"HW: {query_result[0]['Dispositivo']} OFFLINE -> ONLINE")
            # Actualizar el periférico existente solo al cambiar de estado
            mysql_execute(f"UPDATE TB_DOM_PERIF SET Direccion_IP = '{ip_address}', Estado = 1, Informacion = '{info}' WHERE MAC = '{mac_key}'")

        return query_result[0]['Dispositivo'] 
    else:
        # HW no existe
        return None

def check_perif_timeout():
    ahora = int(time.time())

    with _tabla_perif_lock:
        for perif in tabla_perif:
            if perif["Estado"] != 0 and perif["Ultimo_Ok"] < (ahora - 30):
                perif["Estado"] = 0
                logger.info(f"HW: {perif['Dispositivo']} ONLINE -> OFFLINE")
                mysql_execute(f"UPDATE TB_DOM_PERIF SET Estado = 0 WHERE MAC = '{perif['MAC']}';")


async def hw_worker_loop():
    while True:
        await asyncio.sleep(10)
        await asyncio.to_thread(check_perif_timeout)

def get_touch_download_list(ip_adddr):
    """
    Devuelve una respuesta HTTP que representa un archivo de texto para descarga.
    El archivo contendrá tres líneas con el texto "texto de prueba" y se
    enviará como adjunto con el nombre `lista.txt`.
    """
    max_screen = -1
    query_result = mysql_query(f"SELECT MAX( T.Pantalla ) FROM TB_DOM_PERIF AS P, TB_DOM_TOUCH AS T WHERE P.Id = T.Dispositivo AND P.Direccion_IP = '{ip_adddr}'")
    if query_result and query_result[0] and query_result[0]['MAX( T.Pantalla )'] is not None:
        max_screen = query_result[0]['MAX( T.Pantalla )']

    content = "# Lista de descargas\n"
    content += f"# para: {ip_adddr}\n"
    #content += "/download/download.bmp\n"
    #content += "/download/extract.bmp\n"
    #content += "/download/gear.bmp\n"
    #content += "/download/home.bmp\n"
    #content += "/download/key.bmp\n"
    #content += "/download/lamp1.bmp\n"
    #content += "/download/network.bmp\n"
    #content += "/download/next.bmp\n"
    #content += "/download/offline.bmp\n"
    #content += "/download/power.bmp\n"
    #content += "/download/prev.bmp\n"
    #content += "/download/restart.bmp\n"
    #content += "/download/wifi.bmp\n"
    #content += "/download/wifi1.bmp\n"
    #content += "/download/config.csv\n"
    #content += "/download/offline.csv\n"
    for screen in range(0, max_screen + 1):
        content += f"/hw/hwconfig?screen={screen}\n"

    headers = {"Content-Disposition": "attachment; filename=download.lst"}
    return Response(content=content, media_type="text/plain", headers=headers)

def get_touch_download_screen(ip_adddr, screen_nro):
    """
    Devuelve una respuesta HTTP que representa un archivo de texto CSV para descarga.
    El archivo contendrá tres líneas con el texto "texto de prueba" y se
    enviará como adjunto con el nombre `screenx.csv'.
    """

    try:
        screen_nro = int(screen_nro)
    except (TypeError, ValueError):
        logger.error(f"get_touch_download_screen: screen_nro {screen_nro} inválido")
        return Response(content=f"Error: screen_nro {screen_nro} inválido", media_type="text/plain")

    if screen_nro < 0 or screen_nro > 9:
        logger.error(f"get_touch_download_screen: screen_nro {screen_nro} fuera de rango")
        return Response(content=f"Error: screen_nro {screen_nro} fuera de rango", media_type="text/plain")

    content = f"## Archivo: screen{screen_nro}.csv\n"
    content += "## Creado: 2026/07/01 23:26:22\n"
    content += "#\n"
    content += "# FONDO,[color]\n"
    content += "# BOTON_CUADRADO,[etiqueta],[comando:objeto],[x],[y],[w],[h],[color fondo],[color borde],[color etiqueta],[icono],[orientacion]\n"
    content += "# BOTON_REDONDO,[etiqueta],[comando:objeto],[x],[y],[w],[h],[color fondo],[color borde],[color etiqueta],[icono],[orientacion]\n"
    content += "#\n"
    content += "# etiqueta: Texto que aparece en el botón (opcopnal)\n"
    content += "# comando: SWITCH, PULSE, CONFIG, HOME, NEXT, PREV\n"
    content += "# objeto: \n"
    content += "# x: posición X de la esquina superior derecha del botón\n"
    content += "# y: posición Y de la esquina superior derecha del botón\n"
    content += "# w: Ancho del botón\n"
    content += "# h: altura del botón\n"
    content += "# color fondo: 0 a 65535\n"
    content += "# color borde: 0 a 65535\n"
    content += "# color etiqueta: 0 a 65535\n"
    content += "# icono: archivo BMP de 48x48 pixel (opcopnal)\n"
    content += "# orientacion: 0 = Horizontal, 1 = Vertical\n"
    content += "#\n"

    query = f"SELECT T.Redondo, T.Evento, A.Objeto, T.Texto, T.X, T.Y, T.W, T.H, T.Color_pantalla, T.Color_Fondo, T.Color_Borde, T.Color_Texto, T.Icono, T.Orientacion "
    query += f"FROM TB_DOM_PERIF AS P, TB_DOM_TOUCH AS T, TB_DOM_ASSIGN AS A "
    query += f"WHERE P.Id = T.Dispositivo AND A.Id = T.Objeto  AND P.Direccion_IP = '{ip_adddr}' AND T.Pantalla = {screen_nro} "
    query += "ORDER BY T.Boton ASC"

    #logger.info(f"get_touch_download_screen: query: {query}")

    query_result = mysql_query(query)
    if query_result:
        for i in range(0, len(query_result)):
            if i == 0:
                content += f"FONDO,{query_result[i]['Color_pantalla']}\n"

            if query_result[i]['Redondo'] == 1:
                content += f"BOTON_REDONDO,"
            else:
                content += f"BOTON_CUADRADO,"

            content += f"{query_result[i]['Texto']},"

            if query_result[i]['Evento'] == 1:
                content += f"ON:"
            elif query_result[i]['Evento'] == 2:
                content += f"OFF:"
            elif query_result[i]['Evento'] == 3:
                content += f"SWITCH:"
            elif query_result[i]['Evento'] == 4:
                content += f"PULSO:"
            elif query_result[i]['Evento'] == 10:
                content += f"CONFIG:"
            elif query_result[i]['Evento'] == 11:
                content += f"HOME:"
            elif query_result[i]['Evento'] == 12:
                content += f"PREV:"
            elif query_result[i]['Evento'] == 13:
                content += f"NEXT:"

            content += f"{query_result[i]['Objeto']},{query_result[i]['X']},{query_result[i]['Y']},{query_result[i]['W']},{query_result[i]['H']},"
            content += f"{query_result[i]['Color_Fondo']},{query_result[i]['Color_Borde']},{query_result[i]['Color_Texto']},"
            content += f"{query_result[i]['Icono']},{query_result[i]['Orientacion']}\n"

    headers = {"Content-Disposition": f"attachment; filename=screen{screen_nro}.csv"}
    return Response(content=content, media_type="text/plain", headers=headers)

def add_invalid_hardware(mac):
    mysql_execute(
        f"INSERT INTO TB_DOM_INVALID_PERIF (MAC, Ultimo) VALUES ('{mac}', UNIX_TIMESTAMP()) "
        f"ON DUPLICATE KEY UPDATE Ultimo = UNIX_TIMESTAMP()"
    )
    logger.info(f"HW: {mac} desconocido")
