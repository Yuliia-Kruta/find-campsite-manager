function BookingsTab({ bookings }) {
  return (
    <div className="bookings-tab">
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
            <tr>
              <td>{booking.booking_id}</td>
              <td>{booking.booking_date}</td>
              <td>{booking.customer.first_name} {booking.customer.last_name}</td>
              <td>
                <a href=''>
                  View Booking Details
                </a>
              </td>
              <td>
                <a href={`/api/customer_confirmation/${booking.id}`} target="_blank" rel="noopener noreferrer">
                  View Booking Confirmation
                </a>
              </td>
            </tr>
          ))}

        </tbody>
      </table>
    </div>
  );
}

export default BookingsTab;

/*
{bookings.map(booking => (
            <BookingRow key={booking.id} booking={booking} />
          ))}

*/