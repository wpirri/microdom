#!/bin/sh

DBHOST=192.168.10.32
DBNAME=DB_DOMPIWEB
DBUSER=dompi_web
DBPASSWORD=dompi_web

FECHA=`date +%y%m%d%H%M%S`
BACKUP_PATH="/tmp"
INFILE=dump_mysql_db.sql


echo "Obteniendo sistema..."
set -x
SYSTEM_KEY=`echo "SELECT System_Key FROM DB_DOMPIWEB.TB_DOM_CONFIG ORDER BY Id DESC LIMIT 1;" | /usr/bin/mysql -h $DBHOST -u $DBUSER -p$DBPASSWORD -D $DBNAME -N -r --skip-ssl`
set +x
if [ "X${SYSTEM_KEY}" = "X" ]; then
    echo ""
    echo "ERROR: No se pudo obtener el Nombre del sistema"
    exit 1
fi
echo "        Sistema: ${SYSTEM_KEY}"
FILE="backup-mysql-${DBNAME}-${SYSTEM_KEY}-${FECHA}.sql"
OUTFILE="${BACKUP_PATH}/${FILE}"

mkdir -p $BACKUP_PATH

echo "Generando ${OUTFILE} ..."

echo "-- #### Backup creado el ${FECHA}" > "${OUTFILE}"
echo "-- ####" >> "${OUTFILE}"
echo "-- ####CREATE DATABASE ${DBNAME};" >> "${OUTFILE}"
echo "-- ####CREATE USER 'dompi_web'@'%' IDENTIFIED BY 'dompi_web';" >> "${OUTFILE}"
echo "-- ####GRANT SELECT, INSERT, UPDATE, DELETE ON DB_DOMPIWEB.* TO 'dompi_web'@'%' WITH GRANT OPTION;" >> "${OUTFILE}"
echo "-- ####FLUSH PRIVILEGES;" >> "${OUTFILE}"
echo "-- ####" >> "${OUTFILE}"
echo "USE ${DBNAME};" >> "${OUTFILE}"
echo "-- ####" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_TOUCH;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_AUTO;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_AT;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_EVENT;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_CAMARA;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_ALARM_SALIDA;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_ALARM_ZONA;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_ALARM_PARTICION;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_FLAG;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_GROUP;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_ASSIGN;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_GRUPO_VISUAL;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_PERIF;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_USER;" >> "${OUTFILE}"
echo "DELETE FROM TB_DOM_CONFIG;" >> "${OUTFILE}"
echo "-- ####" >> "${OUTFILE}"

/usr/bin/mysql -h $DBHOST -u $DBUSER -p$DBPASSWORD -D $DBNAME -N -r --skip-ssl < "${INFILE}" >> "${OUTFILE}"

sed -i 's/\t//g' "${OUTFILE}"
sed -i 's/NULL//g' "${OUTFILE}"
sed -i 's/,,/,NULL,/g' "${OUTFILE}"
