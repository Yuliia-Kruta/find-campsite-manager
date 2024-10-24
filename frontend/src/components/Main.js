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
    }, [])

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
