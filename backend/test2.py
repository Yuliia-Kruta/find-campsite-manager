import pyodbc
from pymongo import MongoClient
import certifi
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import base64

"""Initilises Flask app and enables CORS"""
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

last_retrieved_booking = 0

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

connection_to_head_office = connect_to_head_office_sql_db()

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

def get_next_booking(cursor):
    """Retrieves the next booking from the Head Office SQL database."""
    global last_retrieved_booking
    last_retrieved_booking += 1
    cursor.execute(f"""SELECT * FROM camping.booking WHERE booking_id ={last_retrieved_booking}""")
    return cursor.fetchone()

def extract_booking_details(row):
    """Extracts and formats booking details from SQL booking table from Head Office db."""
    booking_id = row[0]
    customer_id = row[1]
    booking_date = row[2].strftime('%Y-%m-%d')
    arrival_date = row[3].strftime('%Y-%m-%d')
    campground_id = row[4]
    campsite_size = row[5]
    num_campsites = row[6]
    
    return booking_id, customer_id, booking_date, arrival_date, campground_id, campsite_size, num_campsites

def find_available_campsites(campsite_size_needed, num_sites_needed, arrival_date):
    """Finds available campsites for a given arrival date, size and number of campsites needed."""
    available_campsites = []
    suitable_campsites = list(campsites_col.find({"site_size": campsite_size_needed}, {'_id':0}))
    
    for site in suitable_campsites:
        if arrival_date in site['available_dates']:
            available_campsites.append(site)
        if len(available_campsites) == num_sites_needed:
            break
    
    return available_campsites if len(available_campsites) == num_sites_needed else None

def get_customer(customer_id, cursor):
    cursor.execute(f"""SELECT * FROM camping.customers WHERE customer_id ={customer_id}""")
    row = cursor.fetchone()
    if row:
        return extract_customer_details(row)
    return None

def extract_customer_details(row):
    """Extracts and formats customer details from SQL customers table from Head Office db."""
    return {
        "customer_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "phone": row[3],
        "address": row[4],
        "post_code": row[5]
    }

def calculate_total_cost(available_campsites):
    """Calculates the total cost based of the chosen campsites."""
    total_cost = 0
    for site in available_campsites:
        rate = site.get("daily_rate")
        total_cost += rate
    return total_cost

def create_pdf(confirmation_details):
    """Creates a booking confirmation."""
    buffer = io.BytesIO()
    
    # Create a PDF canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Write the confirmation details to the PDF
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)
    for line in confirmation_details.splitlines():
        text.textLine(line)
    c.drawText(text)
    
    # Finish up the PDF
    c.showPage()
    c.save()
    
    # Move to the beginning of the StringIO buffer
    buffer.seek(0)
    
    return buffer.getvalue()

def prepare_booking_document(booking_id, campground_id, customer, available_campsites, booking_date, arrival_date):
    """Prepares a booking document."""
    
    total_cost = calculate_total_cost(available_campsites)
    departure_date = datetime.strptime(arrival_date, "%Y-%m-%d")+timedelta(days=7)

    booked_campsites = [
        {
            "site_number": campsite["site_number"],
            "site_size": campsite["site_size"],
            "daily_rate": campsite["daily_rate"]
        }
        for campsite in available_campsites
    ] 
    
    confirmation_details = f"""
    Booking Confirmation
    -------------------------
    Booking ID: {booking_id}
    Booking Date: {booking_date}

    Customer:
    name: {customer['first_name']} {customer['last_name']}
    phone: {customer['phone']}
    address: {customer['address']}, {customer['post_code']}
    
    Arrival Date: {arrival_date}
    Departure Date: {departure_date}
    Number of Campsites: {len(booked_campsites)}
    Campsites Booked: {booked_campsites}
    
    Total Cost: ${total_cost}
    -------------------------
    Thank you for booking with us!
    """
   
    pdf_data = create_pdf(confirmation_details)
    pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')  

    return {
        "booking_id": booking_id,
        "campground_id": campground_id,
        "customer": customer,
        "booked_campsites": booked_campsites,
        "booking_date": booking_date,
        "arrival_date": arrival_date,
        "total_cost": total_cost,
        "confirmation_details": pdf_base64
    }

def update_campsite_availability(available_campsites, arrival_date):
    """Updates the availability of booked campsites."""
    for site in available_campsites:
        campsites_col.update_one(
            {"site_number": site["site_number"]},
            {"$pull": {"available_dates": arrival_date}}
        )

@app.get('/get-booking')
def get_booking():
    global last_retrieved_booking
    cursor = connection_to_head_office.cursor()
    print("Before getting booking")
    booking = get_next_booking(cursor)
    print("After getting booking")
    if not booking:
        return jsonify({"error": "No new bookings found."}), 404

    booking_id, customer_id, booking_date, arrival_date, campground_id, campsite_size, num_campsites = extract_booking_details(booking)
    campground_id = "1160780"

    available_campsites = find_available_campsites(campsite_size, num_campsites, arrival_date)
    
    if not available_campsites:
        return jsonify({"error": "No suitable campsites available for this booking."}), 400
    
    customer = get_customer(customer_id, cursor)

    booking_document = prepare_booking_document(booking_id, campground_id, customer, available_campsites, booking_date, arrival_date)
    bookings_col.insert_one(booking_document)

    
    update_campsite_availability(available_campsites, arrival_date)

    last_retrieved_booking = booking_id
    booking_document_for_json = {key: booking_document[key] for key in booking_document if key != "_id"}

    return jsonify(booking_document_for_json), 200

"""To check if Flask is up"""
@app.route('/')
def flask():
    return 'Flask server is up!'

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
  app.run(debug=True)