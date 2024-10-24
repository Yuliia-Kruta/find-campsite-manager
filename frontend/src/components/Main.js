import { useState, useEffect } from "react";
import axios from 'axios';
import BookingsTab from './BookingsTab';
import SummariesTab from './SummariesTab';

const Main = () => {
    
    const [bookings, setBookings] = useState([]);
    const [summaries, setSummaries] = useState([]);
    const [activeTab, setActiveTab] = useState('bookings');
    const [error, setError] = useState("");
    const [message, setMessage] = useState("")


    const handleGetBooking = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/get-booking');
            setBookings(prevBookings => [response.data.booking, ...prevBookings]);
            setMessage(response.data.message);
            if (response.data.summary) {
                setSummaries(prevSummaries => [response.data.summary, ...prevSummaries]);
            }
        } catch (error) {
            console.log(error.response.data)
            setError(error.response?.data?.error || "Error processing the booking");
        }
    };

    useEffect(() => {
        axios.get('http://127.0.0.1:5000/fetch-from-db')
          .then(response => {
            setBookings(response.data.bookings);
            setSummaries(response.data.summaries); 
          })
          .catch(error => {
            setError(error.response?.data?.error || "Error fetching initial data");
            console.error("Error fetching initial data", error);
          });
      }, [])//Add errors and messages to screen

    return (
        <div className="wrapper">
            {error && <p style={{ color: 'red' }}>{error}</p>}
            {message && <p style={{ color: 'green' }}>{message}</p>}
            <button className="get-booking-btn" onClick={handleGetBooking}>Get the Booking</button>
            <div className="info">
                <div className="tabs">
                    <button onClick={() => setActiveTab('bookings')} className={activeTab === 'bookings' ? 'active' : ''}>Bookings</button>
                    <button onClick={() => setActiveTab('summaries')} className={activeTab === 'summaries' ? 'active' : ''}>Summaries</button>
                </div>
                {activeTab === 'bookings' ? (
                    <BookingsTab bookings={bookings} />
                ) : (
                    <SummariesTab summaries={summaries} />
                )}
                
            </div>
        </div>
    );
}

export default Main;

/*
{activeTab === 'bookings' ? (
                    <BookingsTab bookings={bookings} />
                ) : (
                    <SummariesTab summaries={summaries} />
                )}
*/










/*
        const [bookings, setBookings] = useState([
            {
                "booking_id": 1, "customer": {
                    "customer_id": 1,
                    "first_name": "Olena",
                    "last_name": "Kruta",
                    "phone": "0414 05 9239",
                    "address": "SKfjfejlfjjff St ejowqjfoijevn",
                    "post_code": "4456"
                }, "booked_campsites": [
                    {
                        "site_number": 1,
                        "site_size": "Small",
                        "daily_rate": 60
                    },
                    {
                        "site_number": 2,
                        "site_size": "Small",
                        "daily_rate": 60
                    }
                ], "booking_date": "2024-08-15", "arrival_date": "2024-05-10", "total_cost": "250$", "confirmation_details": "ConfirmationTralala"
            },
    
            {
                "booking_id": 2, "customer": {
                    "customer_id": 2,
                    "first_name": "Lusha",
                    "last_name": "Kruta",
                    "phone": "0414 05 9239",
                    "address": "SKfjfejlfjjff St ejowqjfoijevn",
                    "post_code": "4456"
                }, "booked_campsites": [
                    {
                        "site_number": 3,
                        "site_size": "Small",
                        "daily_rate": 60
                    },
                    {
                        "site_number": 4,
                        "site_size": "Small",
                        "daily_rate": 60
                    }
                ], "booking_date": "2024-08-15", "arrival_date": "2024-05-10", "total_cost": "250$", "confirmation_details": "ConfirmationTralala"
            },
        ]);
    
        const [summaries, setSummaries] = useState([
            { "summary_date": "2024-10-05", "total_bookings": 2, "total_sales": "1000$" },
            { "summary_date": "2024-10-04", "total_bookings": 5, "total_sales": "2004$" }
        ]);*/