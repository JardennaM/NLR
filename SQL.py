import mysql.connector


# function for creating a database
def create_database_if_not_exists(database_name):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="%s"%database_name
        )
        print("database already exists")

        return db

    except:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root"
            )
        mycursor = mydb.cursor()
        print("database created!")
        mycursor.execute("CREATE DATABASE %s"%database_name)


        return mydb

def create_phase_table(database):
    """
    Function for creating the phases table within the c_uas database

    Parameters:
    database (string): SQL mycursor

    Returns:
    The phase table within the c_uas database

    """

    database.cursor().execute("CREATE TABLE phases (id INT AUTO_INCREMENT PRIMARY KEY, phase TEXT)")

    print("Phases table created!")

def create_manufacturers_table(database):
    """
    Function for creating the manufacturers table within the c_uas database_name

    Parameters:
    database (string): SQL mycursor

    Returns:
    The maunfacturers table within the c_uas database

    """
    database.cursor().execute("CREATE TABLE manufacturers (id INT AUTO_INCREMENT PRIMARY KEY, manufacturer TEXT)")

    print("Manufacturers table created!")

def create_systems_table(database):
    """
    Function for creating the systems table within the c_uas database_name

    Parameters:
    database (string): SQL mycursor

    Returns:
    The systems table within the c_uas database

    """
    database.cursor().execute("CREATE TABLE systems (id INT AUTO_INCREMENT PRIMARY KEY, man_id INT, parent_id INT, system TEXT)")

    print("Systems table created!")

def create_information_table(database):
    """
    Function for creatnig the information table within the c_uas

    Parameters:
    database (string): SQL mycursor

    Returns:
    The information table within the c_uas database

    """
    database.cursor().execute("CREATE TABLE information (id INT AUTO_INCREMENT PRIMARY KEY, man_id INT, sys_id INT, phase_id INT, URL VARCHAR(255), information TEXT)")

    print("Information table created!")


def initiate_db_tables(database_name):
    db = create_database_if_not_exists(database_name)
    create_phase_table(db)
    create_manufacturers_table(db)
    create_systems_table(db)
    create_information_table(db)

    print("Database initiated and phase, manufacturers, systems and information table created!")





def insert_in_phases(name):
    """
    def some function

    """
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="c_uas"
    )

    mycursor = mydb.cursor()


    txt = "INSERT INTO {} ({}) VALUES ({}) "
    input = txt.format(table_name, column_names, data)

    mycursor.execute(input)

    mydb.commit()

    print("name inserted.")
