import pyodbc

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

def show_records(connection, mytable):
    """Shows all the records for a given table."""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + mytable)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

connectionToHeadOffice = connect_to_head_office_sql_db()

show_records(connectionToHeadOffice, "camping.booking")

