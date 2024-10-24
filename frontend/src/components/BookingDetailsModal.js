/*import { CloseRounded } from '@mui/icons-material';

const BookingDetailsModal = ({ booking, onClose }) => {
    if (!booking) return null;
    return (
        <div className="modal-container" onClick={onClose}>
            <div className='modal-wrapper'>
                <CloseRounded
                    style={{
                        position: "absolute",
                        top: "10px",
                        right: "20px",
                        cursor: "pointer",
                    }}
                    onClick={onClose}
                />
                <div className="modal-content" onClick={e => e.stopPropagation()}>
                    <h2>Booking Details</h2>
                    <div className='booking-details-section'>
                        <p><strong>Booking ID:</strong> {booking.booking_id}</p>
                        <p><strong>Booking Date:</strong> {booking.booking_date}</p>
                        <ul><strong>Customer:</strong>
                            <li><strong>Customer ID:</strong> {booking.customer.customer_id}</li>
                            <li><strong>First Name:</strong> {booking.customer.first_name}</li>
                            <li><strong>Last Name:</strong> {booking.customer.last_name}</li>
                            <li><strong>Phone:</strong> {booking.customer.phone}</li>
                            <li><strong>Address:</strong> {booking.customer.address}</li>
                            <li><strong>Postcode:</strong> {booking.customer.post_code}</li>
                        </ul>
                        <p><strong>Arrival Date:</strong> {booking.arrival_date}</p>
                        <strong>Booked Campsites:</strong>

                        {booking.booked_campsites.map(site => (
                            <ul key={site.site_number}>
                                <li><strong>Site Number:</strong>{site.site_number}</li>
                                <li><strong>Site Size:</strong>{site.site_size}</li>
                                <li><strong>Daily Rate:</strong>{site.daily_rate}</li>
                            </ul>
                        ))}

                        <p><strong>Total Cost:</strong> {booking.total_cost}</p>
                    </div>
                </div>

            </div>

        </div>
    );
}

export default BookingDetailsModal;
*/
//<p><strong>Number of Campsites:</strong> {booking.booked_campsites.length}</p>

import { CloseRounded } from '@mui/icons-material';

const BookingDetailsModal = ({ booking, onClose }) => {
    if (!booking) return null;

    return (
        <div className="modal-container" onClick={onClose}>
            <div className="modal-wrapper" onClick={e => e.stopPropagation()}>
                <CloseRounded
                    style={{
                        position: "absolute",
                        top: "10px",
                        right: "20px",
                        cursor: "pointer",
                    }}
                    onClick={onClose}
                />
                <div className="modal-content">
                    <h2 className='modal-title'>Booking Details</h2>
                    <div className="booking-details-section">
                        <p><strong>Booking ID:</strong> {booking.booking_id}</p>
                        <p><strong>Booking Date:</strong> {booking.booking_date}</p>
                        
                        <div className="customer-details">
                            <h3>Customer Information</h3>
                            <p><strong>Customer ID:</strong> {booking.customer.customer_id}</p>
                            <p><strong>Name:</strong> {booking.customer.first_name} {booking.customer.last_name}</p>
                            <p><strong>Phone:</strong> {booking.customer.phone}</p>
                            <p><strong>Address:</strong> {booking.customer.address}</p>
                            <p><strong>Postcode:</strong> {booking.customer.post_code}</p>
                        </div>

                        <p><strong>Arrival Date:</strong> {booking.arrival_date}</p>

                        <div className="campsites-section">
                            <h3>Booked Campsites</h3>
                            {booking.booked_campsites.map(site => (
                                <div key={site.site_number} className="campsite-details">
                                    <p><strong>Site Number:</strong> {site.site_number}</p>
                                    <p><strong>Site Size:</strong> {site.site_size}</p>
                                    <p><strong>Daily Rate (AUD):</strong> {site.daily_rate}</p>
                                </div>
                            ))}
                        </div>

                        <p><strong>Total Cost (AUD):</strong> {booking.total_cost}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BookingDetailsModal;
