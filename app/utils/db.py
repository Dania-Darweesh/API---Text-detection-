
from datetime import datetime
import psycopg2
import hashlib





connection = None
cursor = None

def connect_DB():
    global connection
    connection = psycopg2.connect(user="root",
                                  password="root",
                                  host="128.199.62.224",
                                  port="5432",
                                  database="ocr")
def disconnect_DB():
    global cursor
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

def insert_admin_DB( username:str , password:str , email='' ) :
    try:
        global connection , cursor
        connect_DB()
        cursor = connection.cursor()

        postgres_insert_query = """insert into users (username , password , email) values ( %s , %s , %s);"""
        record_to_insert = (username , hashlib.md5(password.encode()).hexdigest() , email)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        if (connection):
            print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        disconnect_DB()

def insert_into_DB( image_name :str , image:bytearray , ocr_text = '' , datetime = datetime.utcnow()  ):
    try:
        global connection , cursor
        connect_DB()
        cursor = connection.cursor()

        postgres_insert_query = """insert into events (image_name , image , text , date_time) values (%s , %s , %s , %s);"""
        record_to_insert = ( image_name, image , ocr_text , datetime)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error:
        if (connection):
            print("Failed to insert record into mobile table", error)

    finally:
        # closing database connection.
        disconnect_DB()

def cmd_DB ( query  , fetch = False) :

    try:
        global connection , cursor
        connect_DB()
        cursor = connection.cursor()
        # Print PostgreSQL Connection properties
        #print ( connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute(query)

        final_res = {}

        if (fetch == False):
            return 'done cmd'

        rows = cursor.fetchall()

        i = 0

        for row in rows:
            i = i+1
            final_res.update( {i:row[0]})

        return (final_res)

    except (Exception, psycopg2.Error) as error :
        return ("Error while connecting to PostgreSQL", error)

    finally:
        #closing database connection.
        disconnect_DB()

def check_admin( username ='' , password = ''):

    try:
        global connection , cursor
        connect_DB()
        cursor = connection.cursor()

        postgres_query = """select * from users where username= %s and password= %s """
        Values = (username,  hashlib.md5(password.encode()).hexdigest() )
        cursor.execute(postgres_query, Values)

        rows = cursor.fetchall()

        for row in rows:
            return True

        return False

    except (Exception, psycopg2.Error) as error :
        return ("Error while connecting to PostgreSQL", error)

    finally:
        #closing database connection.
        disconnect_DB()



#insert_into_DB()
#insert_admin_DB('admin','admin')
