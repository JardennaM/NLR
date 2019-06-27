import mysql.connector


# function for creating a database
def create_database_if_not_exists(database_name, username, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="%s"%username,
            passwd="%s"%password,
            database="%s"%database_name
        )

        return db

    except:
        mydb = mysql.connector.connect(
            host="localhost",
            user="%s"%username,
            passwd="%s"%password
            )
        mycursor = mydb.cursor()

        mycursor.execute("CREATE DATABASE %s"%database_name)
        db = mysql.connector.connect(
            host="localhost",
            user="%s"%username,
            passwd="%s"%password,
            database="%s"%database_name
        )

        return db

def create_phase_table(database):
    """
    Function for creating the phases table within the c_uas database
    Parameters:
    database (string): SQL mycursor
    Returns:
    The phase table within the c_uas database
    """

    database.cursor().execute("CREATE TABLE phases (id INT AUTO_INCREMENT PRIMARY KEY, phase TEXT)")



def create_manufacturers_table(database):
    """
    Function for creating the manufacturers table within the c_uas database_name
    Parameters:
    database (string): SQL mycursor
    Returns:
    The maunfacturers table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE manufacturers (id INT AUTO_INCREMENT PRIMARY KEY, manufacturer TEXT)")


def create_systems_table(database):
    """
    Function for creating the systems table within the c_uas database_name
    Parameters:
    database (string): SQL mycursor
    Returns:
    The systems table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE systems (id INT AUTO_INCREMENT PRIMARY KEY, man_id INT, parent_id INT, system TEXT)")


def create_information_table(database):
    """
    Function for creating the information table within the c_uas
    Parameters:
    database (string): SQL mycursor
    Returns:
    The information table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE information (id INT AUTO_INCREMENT PRIMARY KEY, sys_id INT, phase_id INT, URL TEXT, information_keywords TEXT, text TEXT)")



def initiate_db(database_name, username, password):
    """
    Function for initiating a database, and creating the initiate_db_tables
    Parameters:
    database_name (string): name of the database_name
    Returns:
    Database and tables
    """

    db = create_database_if_not_exists(database_name, username, password)

    try:
    create_phase_table(db)
    create_manufacturers_table(db)
    create_systems_table(db)
    create_information_table(db)

    insert_in_phases(db, "detection")
    insert_in_phases(db, "classification")
    insert_in_phases(db, "intervention")

def insert_in_phases(database, phase_name):
    """
    Function for inserting rows in the phases table
    Parameters:
    database (string): SQL cursor
    phase_name (string): name of the phases
    Returns:
    Boolean True or False
    """
    try:
        text = '"'
        database.cursor().execute("INSERT INTO phases (phase) VALUES (' %s ')" %phase_name)
        database.commit()

        return True
    except:
        return False

def insert_in_manufacturers(database, manufacturer_name):
    """
    Function for inserting rows in the phases table
    Parameters:
    database (string): SQL cursor
    manufacturer_name (string): name of the manufacturer
    Returns:
    Boolean True or False
    """

    
    database.cursor().execute("INSERT INTO manufacturers (manufacturer) VALUES ('%s') "%manufacturer_name)
    database.commit()
    database.cursor().execute("SELECT id FROM manufacturers WHERE manufacturer='%s'"%manufacturer_name)
    myresult = database.cursor().fetchall()
    return myresult
    

        # return False

def insert_in_systems(database, man_id, name, parent_id=None):
    """
    Function for inserting rows in the phase table
    Parameters:
    database (string): SQL cursor
    man_id (INT): manufacturers
    parent_id (INT): parental system
    system_name (string): name of the system
    Returns:
    Boolean True or False
    """
    try:
        database.cursor().execute("INSERT INTO systems (manucaturer_id, name, parent_id) VALUES ('%d', '%s', '%d') "% (man_id, name, parent_id))
        database.commit()

        return True
    except:

        return False


def insert_in_information(database, sys_id, phase_id, URL, information_keywords, text):
    """
    Function for inserting rows in the phase table
    Parameters:
    database (string): SQL cursor
    sys_id (INT): id of the system in question
    phase_id (INT): id of the phase in
    URL (string): URL where the information in this row is extracted from
    information_keywords (string): keywords and extracted information found at the website
    text (string): alinea where the information is found
    Returns:
    Boolean True or False
    """
    try:
        database.cursor().execute("INSERT INTO information (sys_id, phase_id, URL, information_keywords, text) VALUES ('%s', '%s', '%s', '%s', '%s') " % (sys_id, phase_id, URL, information_keywords, text))
        database.commit()

        return True
    except:

        return False