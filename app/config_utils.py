
def get_config_value(filename, param_name):
    """
    Lee un archivo de configuración estilo KEY=VALUE y devuelve el valor
    del parámetro solicitado. Ignora líneas vacías y comentarios (#).
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                # Ignorar comentarios y líneas vacías
                if not line or line.startswith("#"):
                    continue

                # Separar clave y valor
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if key == param_name:
                        return value if value != "" else None

        # Si no se encontró el parámetro
        return None

    except FileNotFoundError:
        raise FileNotFoundError(f"El archivo '{filename}' no existe.")
    