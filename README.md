# reIMS
## REHAU Inventory Management System
<details>
  <summary>Install deps</summary>
  
```
pip --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org  --trusted-host piwheels.org install -r requirements.txt
sudo apt-get update
sudo apt-get install postgresql
sudo apt-get install python3-kivy
sudo apt-get install python3-psycopg2
```
</details>

<details>
  <summary>Setup DB</summary>
  
```
sudo su postgres
createuser pi -P --interactive
psql
CREATE DATABASE pi;
exit
exit
psql
CREATE DATABASE reims;
```
</details>

<details>
  <summary>Create DB table</summary>
  
```sql
CREATE TABLE IF NOT EXISTS cords (
    item VARCHAR (255) PRIMARY KEY,
    amount INT NOT NULL,
    connector VARCHAR (255) NOT NULL,
    color VARCHAR (255) NOT NULL,
    type VARCHAR (255) NOT NULL,
    length INT NOT NULL,
    class VARCHAR (255) NOT NULL,
    mode VARCHAR (255)
);
```
</details>

<details>
  <summary>Export DB Table</summary>
  
```sql
COPY cords TO '/home/pi/reIMS/table.csv' DELIMITER ',' CSV HEADER;
```
</details>

<details>
  <summary>Import DB Table</summary>
  
```sql
COPY cords(item,amount,connector,color,type,length,class,mode)
FROM '/home/pi/reIMS/table.csv' DELIMITER ',' CSV HEADER;
```
</details>

<details>
  <summary>List DB entries</summary>
  
```sql
SELECT * FROM cords;
```
</details>

<details>
  <summary>Remote DB</summary>
  
```
sudo nano /etc/postgresql/13/main/pg_hba.conf
```
```
host    all             all              0.0.0.0/0                       trust
host    all             all              ::/0                            trust
```
```
sudo nano /etc/postgresql/13/main/postgresql.conf
```
```
listen_addresses = '*'
```
```
sudo /etc/init.d/postgresql restart
```
</details>
