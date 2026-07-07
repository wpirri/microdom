from app.log_utils import get_daily_logger
from app.mysql_utils import mysql_execute, mysql_query, mysql_next_id
from fastapi.responses import Response

logger = get_daily_logger()


def get_touch_download_list(ip_adddr):
    """
    Devuelve una respuesta HTTP que representa un archivo de texto para descarga.
    El archivo contendrá tres líneas con el texto "texto de prueba" y se
    enviará como adjunto con el nombre `lista.txt`.
    """
    content = "# Lista de descargas\n"
    content += f"# para: {ip_adddr}\n"
    content += "download.bmp\n"
    content += "extract.bmp\n"
    content += "gear.bmp\n"
    content += "home.bmp\n"
    content += "key.bmp\n"
    content += "lamp1.bmp\n"
    content += "network.bmp\n"
    content += "next.bmp\n"
    content += "offline.bmp\n"
    content += "power.bmp\n"
    content += "prev.bmp\n"
    content += "restart.bmp\n"
    content += "wifi.bmp\n"
    content += "wifi1.bmp\n"
    content += "config.csv\n"
    content += "offline.csv\n"
    content += "screen0.csv\n"
    content += "screen1.csv\n"
    content += "screen2.csv\n"
    content += "screen3.csv\n"

    headers = {"Content-Disposition": "attachment; filename=lista.txt"}
    return Response(content=content, media_type="text/plain", headers=headers)

def get_touch_download_screen(ip_adddr, screen_nro):
    """
    Devuelve una respuesta HTTP que representa un archivo de texto CSV para descarga.
    El archivo contendrá tres líneas con el texto "texto de prueba" y se
    enviará como adjunto con el nombre `screenx.csv'.
    """

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

    query = f"SELECT T.Redondo, T.Evento, A.Objeto, T.X, T.Y, T.W, T.H, T.Color_Fondo, T.Color_Borde, T.Color_Etiqueta, T.Icono, T.Orientacion "
    query += f"FROM TB_DOM_TB_DOM_PERIF AS P, TB_DOM_TOUCH AS T, TB_DOM_ASSIGN AS A "
    query += f"WHERE P.Id = T.Dispositivo AND A.Id = T.Objeto  AND P.Direccion_IP = {ip_adddr} AND T.Pantalla = {screen_nro} "
    query += "ORDER BY Id ASC"

    query_result = mysql_query(query)
    if query_result:
        for i in range(0, len(query_result)):
            if query_result[i]['Redondo'] == 1:
                content += f"BOTON_REDONDO,"
            else:
                content += f"BOTON_CUADRADO,"

            content += f"{query_result[i]['Etiqueta']},"

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
            content += f"{query_result[i]['Color_Fondo']},{query_result[i]['Color_Borde']},{query_result[i]['Color_Etiqueta']},"
            content += f"{query_result[i]['Icono']},{query_result[i]['Orientacion']}\n"

    headers = {"Content-Disposition": f"attachment; filename=screen{screen_nro}.csv"}
    return Response(content=content, media_type="text/plain", headers=headers)
