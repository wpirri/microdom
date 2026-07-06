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
