import datetime
import time
import random
import psycopg2
import uuid
""" Data format:
(1, 1.01, "clothes", 435, "PP", datetime.time(12, 10, 30), "Mall", "Unknown", 124.99,
"NA", "SHOES", "MEN", "20pieces", True, 256, "Mall", datetime.time(8, 0, 0),
"Local", "Foot", "NA", "Lacoste", "AsRequired", datetime.time(7, 4, 5), "Who Knows")
"""

"""Create Schema :-
https://www.postgresql.org/docs/9.3/static/sql-createschema.html

Create table under schema:-
    CREATE TABLE myschema.mytable
"""

"""
Generate uuid
>>> import uuid
>>> uid = uuid.uuid4()
>>> uid.hex
'df008b2e24f947b1b873c94d8a3f2201'
"""
class product(object):

    conn_string = "";

    def __init__(self):
        self.conn_string = "host='mentorica.czdfre5hbvcb.ap-southeast-1.rds.amazonaws.com' dbname='devretailgear' " \
                           "user='mentorica' password='M3nt0r1c4'";

        # Hardcoding dummy data
        self.dummyData = [[1, 2, 3, 4, 2, 1, 3],
                          ["A","B","C","D","E","F","G"],
                          ["8a8083895ec63a2f015ec63a6ea10000","8a8083895ec63a2f015ec63a6ea10000","8a8083895ec63a2f015ec63a6ea10000","8a8083895ec63a2f015ec63a6ea10000","8a8083895ee51d33015ee53f307a0000","8a8083895ee51d33015ee53f307a0000","8a8083895ee51d33015ee53f307a0000"],
                          ["PP", "Prasanna", "Pawar", "John", "Jack", "Mentorica", "Mediacorp"],
                          [datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')],
                          ["Mall", "Mall1","Mall2","Mall3", "Mall4", "Mall5", "Mall6"],
                          ["Unknown1", "Unknown2", "Unknown3", "Unknown4", "Unknown5", "Unknown6", "Unknown7"],
                          ["123.66", "45.32", "99.99", "799.99", "899.99", "90.5", "100.99"],
                          ["NA","NA","NA","NA","NA","NA","NA"],
                          ["Shoes", "Jacket", "Short dress", "Plastic", "Paperbag", "vest", "Bag"],
                          ["MEN","LADIES"],
                          [20,9,8,4,2,5,6],
                          [True, False],
                          ["141","142","143","144","145","146","147"],
                          ["Mall", "Mall1", "Mall2", "Mall3", "Mall4", "Mall5", "Mall6"],
                          [datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')],
                          ["Local", "Global", "International", "Exotic", "Obsolete", "Traditional", "Hippy"],
                          ["A", "B", "C", "D", "E", "F", "G"],
                          ["NA", "NA", "NA", "NA", "NA", "NA", "NA"],
                          ["Lacoste","Prada","Adidas","Armani","Nike","AirJordan","H&M"],
                          ["AsRequired", "AsRequired", "AsRequired", "AsRequired", "AsRequired", "AsRequired", "AsRequired"],
                          [datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')],
                          ["Who Knows", "Who Knows", "Who Knows", "Who Knows", "Who Knows", "Who Knows",
                           "Who Knows"]]

    def feedData(self):
        cursor, query_statement, conn = self.initDB()
        print(" Feeding data Started");
        print(self.dummyData)

        for i in range(0, 151, 1):
            data = [0 for idx in range(0, 24, 1)]
            print (data)
            uid = uuid.uuid4();
            data[0] = uid.hex;
	    print(data[0])
            #data[0] = i+1;
            for j in range(0,23,1):
                if j == 4 or j == 15 or j == 21:
                    data[j+1] = self.dummyData[j][0]
                else:
                    if j == 12 or j == 10:
                        data[j+1] = self.dummyData[j][random.randint(0, 1)]
                    else:
                        print(j)
                        data[j+1] = self.dummyData[j][random.randint(0, 6)]
            feed_data = tuple(data)
            """feed_data = (data[0],data[1],data[2],data[3],data[4],data[5],data[6],
                         data[7],data[8],data[9],data[10],data[11],data[12],data[13],
                         data[14],data[15],data[16],data[17],data[18],data[19],data[20],
                         data[21],data[22])"""
            try:
            #Execute query for pos_product table.
		print(feed_data)
		cursor.execute(query_statement, feed_data)
		conn.commit()
            except:
        	print( "Feeding data failed which means Query execution failed. ")
        print(" Finished feeding data")

    def initDB(self):
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % (self.conn_string))

        # get a connection, if a connect cannot be made an exception will be raised here
        conn = psycopg2.connect(self.conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        cursor = conn.cursor()
        print("Connected!\n")

        # Postgres does not have autocommit
        # Set auto commit to true
        conn.set_isolation_level(0)
        # Prepare query for pos_product table
        query_statement = "INSERT INTO public.pos_product (id, version, category, company_id," \
                          " create_by, created_at, datasource, default_barcode, default_price, " \
                          "default_sku, description, gender, inventory, is_active, pos_id," \
                          " product_type, published_at, published_scope, subcategory, tags, " \
                          "title, update_by, updated_at, vendor)" \
                          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                          "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";  # Use %s for integer too, %s is placeholder

        return cursor, query_statement, conn

def main():
    print("Starting feeding data")
    to_feed = product()
    to_feed.feedData()

if __name__ == "__main__":
    main()

