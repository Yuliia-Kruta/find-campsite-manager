import { useState } from "react";
import BookingDetailsModal from "./BookingDetailsModal";

function BookingsTab({ bookings }) {

  const [selectedBooking, setSelectedBooking] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const openModal = (booking) => {
    setSelectedBooking(booking);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedBooking(null);
  };

  const openBookingConfirmation = (confirmationDetails) => {
    const pdfData = `data:application/pdf;base64,${confirmationDetails}`;
    const newWindow = window.open();
      if (newWindow) {
        newWindow.document.write(`
          <!DOCTYPE html>
          <html lang="en">
            <head>
              <title>Booking Confirmation</title>
              <style>
                body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; }
                iframe { width: 100%; height: 100%; border: none; }
              </style>
            </head>
            <body>
              <iframe src="${pdfData}" width="100%" height="100%" style="border:none;"></iframe>
            </body>
          </html>
        `);
        newWindow.document.close(); 
      }
  };

  const filteredBookings = bookings.filter((booking) =>
    `${booking.customer.first_name} ${booking.customer.last_name}`
      .toLowerCase()
      .includes(searchQuery.toLowerCase())
  );

  return (
    <div className="bookings-tab">
      <input
        type="text"
        placeholder="Search by customer name"
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)} 
        className="search-input"
      />
      {filteredBookings.length > 0 ? (
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
            {filteredBookings.map(booking => (
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
                  <button className="view-pdf-btn"
                    onClick={() =>
                      openBookingConfirmation(booking.confirmation_details)
                    }
                  >
                    View Booking Confirmation
                  </button>
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