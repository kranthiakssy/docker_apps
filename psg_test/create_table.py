import psycopg2
import datetime

try:
    connect_str = "dbname='exampledb' user='docker1' host='localhost' " + \
                  "password='bhel@123'"
    # use our connection values to establish a connection
    conn = psycopg2.connect(connect_str)
    # create a psycopg2 cursor that can execute queries
    cursor = conn.cursor()
    # create a new table with a single column called "name"
    # cursor.execute("""CREATE TABLE tutorials (name char(40));""")
    cursor.execute("""CREATE TABLE plant_data (time_index timestamp without time zone NOT NULL, 
                        variable1 double precision,
                        variable2 double precision,
                        variable3 double precision,
                        variable4 double precision);""")
    # Insert data into table
    # cursor.execute("INSERT INTO tutorials VALUES('pasagadugula')")
    # cursor.execute("insert into plant_data (time_index,variable1,variable2,variable3,variable4) values(%s,%s,%s,%s,%s)",
    #                 (datetime.datetime.now(),15,33,44,74))
    # conn.commit()
    # run a SELECT statement - no data in there, but we can try it
    # cursor.execute("""SELECT * from plant_data""")
    # cursor.execute("""DROP TABLE plant_data""")
    conn.commit() # <--- makes sure the change is shown in the database
    # rows = cursor.fetchall()
    # print(rows)
    cursor.close()
    conn.close()
except Exception as e:
    print("Uh oh, can't connect. Invalid dbname, user or password?")
    print(e)