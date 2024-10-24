import { useState } from "react";
import axios from 'axios';
import BookingsTab from './BookingsTab';
import SummariesTab from './SummariesTab';

const Main = () => {

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
    ]);
    const [activeTab, setActiveTab] = useState('bookings');
    const [error, setError] = useState("");
    const [message, setMessage] = useState("")

    const handleGetBooking = () => {
        axios.post('/api/get_booking')
            .then(response => {
                if (response.data.success) {
                    setBookings(prevBookings => [response.data.booking, ...prevBookings]);
                    // If a summary is created, fetch the latest summaries
                    if (response.data.new_summary) {
                        setSummaries(prevSummaries => [response.data.new_summary, ...prevSummaries]);
                    }
                } else {
                    alert(response.data.message); // Handle error message
                }
            })
            .catch(error => {
                console.error("Error processing the booking!", error);
            });
    };

    return (
        <div className="container">
            <button className="get-booking-btn" onClick={handleGetBooking}>Get the Booking</button>
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

    );
}

export default Main;