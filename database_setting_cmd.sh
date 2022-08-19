#!/bin/bash

echo "Please enter root user MySQL password!"
echo "Note: password will be hidden when typing"
read -s rootpasswd

echo "[DB] Creating ..."
mysql -uroot -p${rootpasswd} -e "CREATE DATABASE ably /*\!40100 DEFAULT CHARACTER SET utf8 */;"
mysql -uroot -p${rootpasswd} -e "CREATE DATABASE test_ably /*\!40100 DEFAULT CHARACTER SET utf8 */;"
echo "[DB] Created !"

echo "[USER] Creating ..."
mysql -uroot -p${rootpasswd} -e "CREATE USER ably_backend@localhost IDENTIFIED BY 'dp2qmfflWkd!';"
mysql -uroot -p${rootpasswd} -e "CREATE USER test_ably_backend@localhost IDENTIFIED BY 'testdp2qmfflWkd!';"

echo "[USER] Granting ALL privileges ..."
mysql -uroot -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON ably.* TO ably_backend@localhost;"
mysql -uroot -p${rootpasswd} -e "GRANT ALL PRIVILEGES ON test_ably.* TO test_ably_backend@localhost;"
mysql -uroot -p${rootpasswd} -e "FLUSH PRIVILEGES;"
echo "[USER] Created !"

echo "[TABLE] Starting ..."
mysql -uroot -p${rootpasswd} ably < ably_table_schema.sql
mysql -uroot -p${rootpasswd} test_ably < ably_table_schema.sql
echo "[TABLE] Done !"

echo "MySQL Setting Done !"

exit

fi