#!/bin/sh
# Cabacera
echo "#!/bin/sh" > microdom-install.sh
# Archivo de configuracion
echo "sudo sh -c 'echo REMOTE_HOST=witchblade.com.ar > /etc/microdom.conf'" >> microdom-install.sh
echo "sudo sh -c 'echo REMOTE_PORT=443 >> /etc/microdom.conf'" >> microdom-install.sh
echo "sudo sh -c 'echo REMOTE_PROTO=https >> /etc/microdom.conf'" >> microdom-install.sh
# Directorios
echo "sudo sh -c 'mkdir -p /var/lib/microdom/html'" >> microdom-install.sh
echo "sudo sh -c 'mkdir -p /var/lib/microdom/download'" >> microdom-install.sh
echo "sudo sh -c 'chmod 0777 /var/lib/microdom/download'" >> microdom-install.sh
# SCripts de actualizacion
for script in microdom-update-firmware.sh microdom-update-service.sh microdom-update-web.sh; do
    echo "" >> microdom-install.sh
    echo "cat << 'EOF' > $script" >> microdom-install.sh
    cat "$script" >> microdom-install.sh
    echo "" >> microdom-install.sh
    echo "EOF" >> microdom-install.sh
    echo "chmod +x $script" >> microdom-install.sh
done
#
# TODO: Mofificar el script de servicios con la IP correcta para el acceso al a base de datos
#
# Script de creación de Base de datos y datos iniciales
echo "" >> microdom-install.sh
echo "cat << 'EOF' > create_mysql_db.sql" >> microdom-install.sh
cat "../db/create_mysql_db.sql" >> microdom-install.sh
echo "" >> microdom-install.sh
echo "EOF" >> microdom-install.sh
#
echo "" >> microdom-install.sh
echo "cat << 'EOF' > init_mysql_db.sql" >> microdom-install.sh
cat "../db/init_mysql_db.sql" >> microdom-install.sh
echo "" >> microdom-install.sh
echo "EOF" >> microdom-install.sh
#
# TODO: modificar la configuracion de MySQL para que escuche en la interface de red
#
# Ejecuciones
#
echo "" >> microdom-install.sh
echo "sudo sh -c 'mysql < create_mysql_db.sql'" >> microdom-install.sh
echo "sudo sh -c 'mysql < init_mysql_db.sql'" >> microdom-install.sh
#
echo "" >> microdom-install.sh
echo "./microdom-update-firmware.sh" >> microdom-install.sh
echo "./microdom-update-web.sh" >> microdom-install.sh
echo "./microdom-update-service.sh" >> microdom-install.sh
#
# TODO: Agregar la configuración de APACHE













chmod +x microdom-install.sh

