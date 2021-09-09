# Flask-Container-Frame数据库初始化
mysql -uroot -pxuan89948632 -e "CREATE USER 'fcf'@'%' IDENTIFIED BY 'fcf89948632';"
mysql -uroot -pxuan89948632 -e "CREATE DATABASE IF NOT EXISTS fcf DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;"
mysql -uroot -pxuan89948632 -e "GRANT ALL PRIVILEGES ON fcf.* TO 'fcf'@'%';"
mysql -uroot -pxuan89948632 -e "FLUSH PRIVILEGES;"

# huobi数据库初始化
mysql -uroot -pxuan89948632 -e "CREATE USER 'huobi'@'%' IDENTIFIED BY 'huobi89948632';"
mysql -uroot -pxuan89948632 -e "CREATE DATABASE IF NOT EXISTS Huobi DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8mb4_general_ci;"
mysql -uroot -pxuan89948632 -e "GRANT ALL PRIVILEGES ON Huobi.* TO 'huobi'@'%';"
mysql -uroot -pxuan89948632 -e "FLUSH PRIVILEGES;"

# 