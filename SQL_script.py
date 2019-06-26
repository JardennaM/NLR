import mysql.connector
import SQL

# initiate table
SQL.initiate_db_tables("c_uas")

# cursor
db = SQL.create_database_if_not_exists("c_uas")

SQL.insert_in_manufacturers(db, "Delft Dynamics")
SQL.insert_in_manufacturers(db, "Delft")
SQL.insert_in_systems(db, "1", "2", "DroneCatcher")
SQL.insert_in_information(db, "1", "3", "http://counterdrone.nl", "RF jamming", "This counter drone system uses a sophisticated RF jamming system with a range of up to 2km.")
