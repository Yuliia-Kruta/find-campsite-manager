import pyodbc
from pymongo import MongoClient
import certifi
from datetime import datetime, timedelta

def connect_to_head_office_sql_db():
  """Connects to the Head Office Azure SQL database."""
  server = 'ict320-task3.database.windows.net' 
  database = 'camping'
  username = 'ict320-admin'
  password = 'campingPassword!'   
  driver= '{ODBC Driver 18 for SQL Server}'
  
  connection_string = 'Driver='+driver+';Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';PWD='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
  connection = pyodbc.connect(connection_string)
  return connection

def connect_to_campground_nosql_db():
  """Connects to the Campground Azure NoSQL Document database."""
  username = 'ict320-task3-db'
  password = 'Bsrr8WFD1CDFhQxXuFSZKiQjbUEokX1syHWPnXO7kcStKQNq3oVa7eybpxeEy8e5UnolUBIHOCcwACDb7mkUqg=='  
  url = 'ict320-task3-db.mongo.cosmos.azure.com:10255/'
  db_name = 'campground_db'

  uri = f'mongodb://{username}:{password}@{url}?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@{username}@'
  mongo_client = MongoClient(uri, tlsCAFile=certifi.where())
  campground_db = mongo_client[db_name]
  return campground_db




def show_records(connection, mytable):
    """Shows all the records for a given table."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + mytable)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def populate_campsites():
    """Populates campsites collection with data."""
    num_campsites = 90

    start_available_date = datetime.strptime('2024-10-05', '%Y-%m-%d')
    end_available_date = datetime.strptime('2024-11-30', '%Y-%m-%d')
    saturdays = []
    while start_available_date <= end_available_date:
        saturdays.append(start_available_date.strftime('%Y-%m-%d'))
        start_available_date += timedelta(days=7)
    
    campsites = []
    for site_number in range(1, num_campsites + 1):
        if 1 <= site_number <= 30:
            site_size = "Small"
            daily_rate = 50
        elif 31 <= site_number <= 60:
            site_size = "Medium"
            daily_rate = 60
        else:
            site_size = "Large"
            daily_rate = 70

        campsite = {
            "site_number": site_number,
            "site_size": site_size,
            "daily_rate": daily_rate,
            "available_dates": saturdays
        }
        campsites.append(campsite)
        
    campsites_col.insert_many(campsites)
    print(f"{num_campsites} campsites populated successfully!")

connection_to_head_office = connect_to_head_office_sql_db()



# show_records(connection_to_head_office, "camping.booking")


campground_db = connect_to_campground_nosql_db()
campsites_col = campground_db["campsites"]
bookings_col = campground_db["bookings"]

# my_docs = my_col.find({}, {'_id':0})


# Prints all documents in the collection
# for doc in my_docs:
  # print(doc['name'], doc['Semester']) 

if __name__ == '__main__':
  if campsites_col.count_documents({}) == 0:
     populate_campsites()
  