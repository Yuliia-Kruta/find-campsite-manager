import pyodbc
from pymongo import MongoClient
import certifi
from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
import base64
from dotenv import load_dotenv  

load_dotenv()

"""Initilises Flask app and enables CORS"""
app = Flask(__name__)
CORS(app) 

last_retrieved_booking = 0
last_retrieved_booking_date = "2024-08-15"
total_bookings_today = 0
total_sales_today = 0

def connect_to_head_office_sql_db():
  """Connects to the Head Office Azure SQL database."""
  try:
    server = os.getenv("CAMPING_SERVER")
    database = os.getenv("CAMPING_DB_NAME")
    username = os.getenv("CAMPING_USERNAME")
    password = os.getenv("CAMPING_PASSWORD")
    driver= '{ODBC Driver 18 for SQL Server}'

    connection_string = 'Driver='+driver+';Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';PWD='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    connection = pyodbc.connect(connection_string)
    return connection
  
  except Exception as e:
    raise Exception(f"Error connecting to Head Office SQL database: {e}")


def connect_to_campground_nosql_db():
  """Connects to the Campground Azure NoSQL Document database."""
  try:
    username = os.getenv("CAMPGROUND_USERNAME")
    password = os.getenv("CAMPGROUND_PASSWORD")
    url = os.getenv("CAMPGROUND_URL")
    db_name = os.getenv("CAMPGROUND_DB_NAME")

    uri = f'mongodb://{username}:{password}@{url}?ssl=true&retrywrites=false&replicaSet=globaldb&maxIdleTimeMS=120000&appName=@{username}@'
    mongo_client = MongoClient(uri, tlsCAFile=certifi.where())
    campground_db = mongo_client[db_name]
    return campground_db
  
  except Exception as e:
    raise Exception(f"Error connecting to Campground MongoDB: {e}")

def connect_to_campground_sql_db():
  """Connects to the Campground Azure SQL database."""
  try:
    server = os.getenv("SUMMARIES_SERVER")
    database = os.getenv("SUMMARIES_DB_NAME")
    username = os.getenv("SUMMARIES_USERNAME")
    password = os.getenv("SUMMARIES_PASSWORD")
    driver= '{ODBC Driver 18 for SQL Server}'

    connection_string = 'Driver='+driver+';Server=tcp:'+server+',1433;Database='+database+';Uid='+username+';PWD='+password+';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    connection = pyodbc.connect(connection_string)
    return connection
  
  except Exception as e:
      raise Exception(f"Error connecting to Campground SQL database: {e}")
  

"""Initilises connections"""
try:
    connection_to_head_office = connect_to_head_office_sql_db()
    campground_db = connect_to_campground_nosql_db()
    campsites_col = campground_db["campsites"]
    bookings_col = campground_db["bookings"] 
    connection_to_summary_db = connect_to_campground_sql_db()
except Exception as e:
    print(f"Database connection error: {e}")
        
def populate_campsites():
    """Populates campsites collection with data."""
    if campsites_col is None:
        print("No MongoDB collection available for campsites.")
        return
    
    num_campsites = 90
    start_available_date = datetime.strptime('2024-10-05', '%Y-%m-%d')
    end_available_date = datetime.strptime('2024-11-30', '%Y-%m-%d')
    saturdays = []
    # Listing all Saturdays for the 2 month period
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

def create_summary_table():
    """Creates a new table in the Campground SQL db for storing summaries."""
    cursor = connection_to_summary_db.cursor()
    cursor.execute("""
        IF OBJECT_ID('summaries', 'U') IS NOT NULL
        DROP TABLE summaries;
    """)
    cursor.execute(f"""CREATE TABLE summaries (summary_id int IDENTITY(1,1) PRIMARY KEY, summary_date date NULL, total_bookings int NULL, total_sales decimal(10, 2) NULL)""")
    connection_to_summary_db.commit()


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
    if campsites_col is None:
        print("Campsites collection is not initialised.")
        return None
    
    available_campsites = []
    suitable_campsites = list(campsites_col.find({"site_size": campsite_size_needed}, {'_id':0}))
    
    for site in suitable_campsites:
        if arrival_date in site['available_dates']:
            available_campsites.append(site)
        if len(available_campsites) == num_sites_needed:
            break
    return available_campsites if len(available_campsites) == num_sites_needed else None

def get_customer(customer_id, cursor):
    """Retrieves a customer record from Head Office db based on customer ID."""
    cursor.execute(f"""SELECT * FROM camping.customers WHERE customer_id ={customer_id}""")
    row = cursor.fetchone()
    if row:
        return extract_customer_details(row)
    return None

def extract_customer_details(row):
    """Extracts customer details from retrieved record."""
    return {
        "customer_id": row[0],
        "first_name": row[1],
        "last_name": row[2],
        "phone": row[3],
        "address": row[4],
        "post_code": row[5]
    }

def calculate_total_cost(available_campsites):
    """Calculates the total cost based on the chosen campsites' daily rates."""
    total_cost = 0
    for site in available_campsites:
        rate = site.get("daily_rate")
        rate *= 7 # customers stay for 7 nights
        total_cost += rate
    return total_cost

def create_pdf(confirmation_details):
    """Creates a booking confirmation."""
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    text = c.beginText(40, 750)
    text.setFont("Helvetica", 12)
    for line in confirmation_details.splitlines():
        text.textLine(line)
    c.drawText(text)
    
    c.showPage()
    c.save()
    buffer.seek(0)
    
    return buffer.getvalue()

def prepare_booking_document(booking_id, campground_id, customer, available_campsites, booking_date, arrival_date):
    """Prepares a booking document."""
    total_cost = calculate_total_cost(available_campsites)
    departure_date = (datetime.strptime(arrival_date, "%Y-%m-%d")+timedelta(days=7)).strftime("%Y-%m-%d")

    booked_campsites = [
        {
            "site_number": campsite["site_number"],
            "site_size": campsite["site_size"],
            "daily_rate": campsite["daily_rate"]
        }
        for campsite in available_campsites
    ] 
    # Formatted string for campsites
    campsites_info = "\n\n".join([
    f"        Site Number: {site['site_number']},\n"
    f"        Size: {site['site_size']},\n"
    f"        Daily Rate: {site['daily_rate']}$"
    for site in booked_campsites
])
    
    confirmation_details = f"""
    Booking Confirmation
    ------------------------------------------
    Booking ID: {booking_id}
    Booking Date: {booking_date}

    Customer:
        name: {customer['first_name']} {customer['last_name']}
        phone: {customer['phone']}
        address: {customer['address']}, {customer['post_code']}
    
    Arrival Date: {arrival_date}
    Departure Date: {departure_date}
    
    Number of Campsites: {len(booked_campsites)}
    Campsites Booked: 
    
{campsites_info}
    
    Total Cost: {total_cost}$
    ------------------------------------------
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
        site_number = site["site_number"]
        campsites_col.update_one(
            {"site_number": site_number},
            {"$pull": {"available_dates": arrival_date}}
        )
        print(f"Campsite {site_number} availability updated.")

def send_daily_summary_to_head_office(cursor_head_office, campground_id, booking_date, total_bookings_today, total_sales_today):
    """Stores the summary of the Campground's #1160780 bookings for the day in Head Office SQL db."""
    try:
        query = """
        INSERT INTO camping.summary(campground_id, summary_date, total_sales, total_bookings)
        VALUES (?, ?, ?, ?)
        """
        cursor_head_office.execute(query, (campground_id, booking_date, total_sales_today, total_bookings_today))
        connection_to_head_office.commit()
        print(f"Daily summary for {booking_date} stored in Head Office db successfully.")
    except Exception as e:
        print(f"Error storing daily summary in Head Office db: {e}")

def store_daily_summary(cursor_summary_db, cursor_head_office, daily_summary_details, campground_id):
    """Stores the summary of the bookings for the day in Campground SQL db."""
    try:
        summary_date = daily_summary_details["summary_date"]
        total_bookings = daily_summary_details["total_bookings"]
        total_sales = daily_summary_details["total_sales"]
        query = """
        INSERT INTO summaries(summary_date, total_bookings, total_sales)
        VALUES (?, ?, ?)
        """
        cursor_summary_db.execute(query, (summary_date, total_bookings, total_sales))
        connection_to_summary_db.commit()
        print(f"Daily summary for {summary_date} stored in Campground summary db successfully.")
        send_daily_summary_to_head_office(cursor_head_office, campground_id, summary_date, total_bookings, total_sales)
    except Exception as e:
        print(f"Error storing daily summary: {e}")

"""Endpoint to fetch and process the booking"""
@app.post('/get-booking')
def get_booking():
    try:
        global last_retrieved_booking, last_retrieved_booking_date, total_bookings_today, total_sales_today
        daily_summary_details = None
        cursor_head_office = connection_to_head_office.cursor()
        cursor_summary_db = connection_to_summary_db.cursor()

        booking = get_next_booking(cursor_head_office)
        if not booking:
            return jsonify({"message": "No new bookings found."}), 404

        booking_id, customer_id, booking_date, arrival_date, campground_id, campsite_size, num_campsites = extract_booking_details(booking)
        campground_id = "1160780"

        #Triggers creating the summary
        if booking_date!=last_retrieved_booking_date:
            daily_summary_details = {"summary_date":last_retrieved_booking_date, "total_bookings":total_bookings_today, "total_sales":f"{total_sales_today:.2f}"}
            store_daily_summary(cursor_summary_db, cursor_head_office, daily_summary_details, campground_id)
            last_retrieved_booking_date=booking_date
            total_bookings_today=0
            total_sales_today=0

        available_campsites = find_available_campsites(campsite_size, num_campsites, arrival_date)
        if not available_campsites:
            return jsonify({"error": "No suitable campsites available for this booking."}), 400
        
        customer = get_customer(customer_id, cursor_head_office)
        if not customer:
            return jsonify({"error": "Customer not found."}), 404

        booking_document = prepare_booking_document(booking_id, campground_id, customer, available_campsites, booking_date, arrival_date)

        if bookings_col is not None:
            bookings_col.insert_one(booking_document)
        
        total_bookings_today+=1
        total_sales_today+=booking_document["total_cost"]
        
        update_campsite_availability(available_campsites, arrival_date)

        last_retrieved_booking = booking_id
        booking_document_for_json = {key: booking_document[key] for key in booking_document if key != "_id"}
        
        return jsonify({'message': 'Booking was processed successfully', 'booking' : booking_document_for_json, 'summary':daily_summary_details}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""Endpoint to fetch existing in databases bookings and summaries"""
@app.get('/fetch-from-db')
def get_existing_data():
    try:
        bookings = bookings_col.find()
        existing_bookings = []
        for booking in bookings:
            prepared_booking = {key: booking[key] for key in booking if key != "_id"}
            existing_bookings.insert(0, prepared_booking)
        
        cursor_summary = connection_to_summary_db.cursor()
        cursor_summary.execute("SELECT * FROM dbo.summaries")
        existing_summaries = cursor_summary.fetchall()
        #Prepare summaries to be json serialisable
        columns = [column[0] for column in cursor_summary.description]
        prepared_summaries = []
        for row in existing_summaries:
            row_dict = dict(zip(columns, row))
            row_dict['summary_date'] = row_dict['summary_date'].strftime('%Y-%m-%d')
            prepared_summaries.insert(0, row_dict)
 
        return jsonify({'message': 'Existing bookings and summaries retrieved successfully', 'bookings': existing_bookings, 'summaries': prepared_summaries}), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500


"""To check if Flask is up"""
@app.route('/')
def flask():
    return 'Flask server is up!'

if __name__ == '__main__':
  if campsites_col.count_documents({}) == 0:
     populate_campsites()
  create_summary_table()
  app.run(debug=True)
