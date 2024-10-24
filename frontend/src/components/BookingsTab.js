import { useState } from "react";
import BookingDetailsModal from "./BookingDetailsModal";

function BookingsTab({ bookings }) {

  const [selectedBooking, setSelectedBooking] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = (booking) => {
    setSelectedBooking(booking);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedBooking(null);
  };

  return (
    <div className="bookings-tab">
      {bookings.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Booking ID</th>
              <th>Booking Date</th>
              <th>Customer Name</th>
              <th>Booking Details</th>
              <th>Booking Confirmation</th>
            </tr>
          </thead>
          <tbody>
            {bookings.map(booking => (
              <tr key={booking.booking_id}>
                <td>{booking.booking_id}</td>
                <td>{booking.booking_date}</td>
                <td>{booking.customer.first_name} {booking.customer.last_name}</td>
                <td>
                  <button className="view-booking-btn" onClick={() => openModal(booking)}>
                    View Booking Details
                  </button>
                </td>
                <td>
                  <a href={`/api/customer_confirmation/${booking.id}`} target="_blank" rel="noopener noreferrer">
                    View Booking Confirmation
                  </a>
                </td>
              </tr>
            ))}

          </tbody>
        </table>)
        : (
          <p>No bookings present yet.</p>
        )}
      {isModalOpen && (
        <BookingDetailsModal booking={selectedBooking} onClose={closeModal} />
      )}
    </div>
  );
}

export default BookingsTab;