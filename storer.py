import mysql.connector

def create_main_categories_table(database):
    """
    Function for creating the main_categories table within the c_uas database
    Parameters:
    database (string): SQL mycursor
    Returns:
    The phase table within the c_uas database
    """

    database.cursor().execute("CREATE TABLE main_categories (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

def create_manufacturers_table(database):
    """
    Function for creating the manufacturers table within the c_uas database_name
    Parameters:
    database (string): SQL mycursor
    Returns:
    The maunfacturers table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE manufacturers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

def create_systems_table(database):
    """
    Function for creating the systems table within the c_uas database_name
    Parameters:
    database (string): SQL mycursor
    Returns:
    The systems table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE systems (id INT AUTO_INCREMENT PRIMARY KEY, manufacturer_id INT, parent_id INT, name VARCHAR(255))")

def create_sub_categories_table(database):
    """
    Function for creating the sub categories table within the c_uas database_name
    Parameters:
    database (string): SQL mycursor
    Returns:
    The sub categories table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE sub_categories (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))")

def create_information_table(database):
    """
    Function for creating the information table within the c_uas
    Parameters:
    database (string): SQL mycursor
    Returns:
    The information table within the c_uas database
    """
    database.cursor().execute("CREATE TABLE information (id INT AUTO_INCREMENT PRIMARY KEY, system_id INT, main_category_id INT, sub_category VARCHAR(255), keywords TEXT, url VARCHAR(255), context TEXT, reliability INT)")

def create_database(username, password, database_name):
    mydb = mysql.connector.connect(
      host="localhost",
      user="%s"%username,
      passwd="%s"%password
    )

    mycursor = mydb.cursor()
    mycursor.execute("SHOW DATABASES LIKE '%s'"%database_name)
    databases = [list(db)[0] for db in mycursor]

    if databases == []:
        mycursor.execute("CREATE DATABASE %s"%database_name)
    db = mysql.connector.connect(
        host="localhost",
        user="%s"%username,
        passwd="%s"%password,
        database="%s"%database_name
    )
    return db
        
def add_tables(mydb):
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    tables = [list(table)[0] for table in mycursor]
    
    if 'main_categories' not in tables:
        create_main_categories_table(mydb)
    if 'sub_categories' not in tables:
        create_sub_categories_table(mydb)
    if 'manufacturers' not in tables:
        create_manufacturers_table(mydb)
    if 'systems' not in tables:
        create_systems_table(mydb)
    if 'information' not in tables:
        create_information_table(mydb)

def insert_in_main_categories(database, main_category_name):
    """
    Function for inserting rows in the phases table
    Parameters:
    database (string): SQL cursor
    phase_name (string): name of the phases
    Returns:
    Boolean True or False
    """
    mycursor = database.cursor()
    mycursor.execute("SELECT * FROM main_categories WHERE name = '%s'"%main_category_name)
    ids = [identifier[0] for identifier in mycursor]
    if ids == []:
        mycursor.execute("INSERT INTO main_categories (name) VALUES ('%s')"%main_category_name)
        database.commit()
        return mycursor.lastrowid
    else:
        return ids[0]


def insert_in_sub_categories(database, sub_category_name):
    """
    Function for inserting rows in the sub_categories table
    Parameters:
    database (string): SQL cursor
    phase_name (string): name of the phases
    Returns:
    Boolean True or False
    """
    mycursor = database.cursor()
    mycursor.execute("INSERT INTO sub_categories (name) VALUES ('%s')"%sub_category_name)
    database.commit()
    return mycursor.lastrowid
    
def insert_in_manufacturers(database, manufacturer_name):
    """
    Function for inserting rows in the phases table
    Parameters:
    database (string): SQL cursor
    manufacturer_name (string): name of the manufacturer
    Returns:
    Boolean True or False
    """
    mycursor = database.cursor()
    mycursor.execute("INSERT INTO manufacturers (name) VALUES ('%s') "%manufacturer_name)
    database.commit()
    return mycursor.lastrowid

def insert_in_systems(database, man_id, name, parent_id=0):
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
    mycursor = database.cursor()
    mycursor.execute("INSERT INTO systems (manufacturer_id, name, parent_id) VALUES ('%d', '%s', '%d') "% (man_id, name, parent_id))
    database.commit()
    return mycursor.lastrowid

def insert_in_information(database, sys_id, main_category_id, sub_category, keywords, url, context, reliability=1):
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
        mycursor = database.cursor()
        mycursor.execute("INSERT INTO information (system_id, main_category_id, sub_category, keywords, url, context, reliability) VALUES ('%d', '%d', '%s', '%s', '%s', '%s', '%d') " % (sys_id, main_category_id, sub_category, keywords, url, context, reliability))
        database.commit()
        return mycursor.lastrowid
    except:
        return False

       