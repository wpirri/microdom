#!/bin/sh

set -eu

usage() {
	echo "Uso: $0 URL_GITHUB [archivo_destino]" >&2
	echo "URL_GITHUB puede ser un enlace /blob/ o raw.githubusercontent.com." >&2
	exit 2
}

[ "$#" -ge 1 ] && [ "$#" -le 2 ] || usage

source_url=$1
case "$source_url" in
	https://github.com/*/blob/*)
		raw_url=$(printf '%s\n' "$source_url" | sed 's#^https://github.com/#https://raw.githubusercontent.com/#; s#/blob/#/#')
		;;
	https://raw.githubusercontent.com/*)
		raw_url=$source_url
		;;
	*)
		echo "Error: usa un enlace de archivo de github.com/.../blob/... o raw.githubusercontent.com." >&2
		exit 2
		;;
esac

file_path=${raw_url#https://raw.githubusercontent.com/}
file_path=${file_path#*/}
output=${2:-${file_path##*/}}
temp_file=$(mktemp "${output}.tmp.XXXXXX") || {
	echo "Error: no se pudo crear un archivo temporal junto a '$output'." >&2
	exit 1
}

if ! wget -q -O "$temp_file" "$raw_url"; then
	rm -f "$temp_file"
	echo "Error: no se pudo descargar $raw_url" >&2
	echo "Verifica que el repositorio, la rama y la ruta existan y sean públicos." >&2
	exit 1
fi

mv "$temp_file" "$output"
printf 'Descargado: %s\n' "$output"

