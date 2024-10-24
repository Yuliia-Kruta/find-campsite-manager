function SummariesTab({ summaries }) {
  return (
    <div className="summaries-tab">
      {summaries.length > 0 ? (
        <table>
          <thead>
            <th>Summary Id</th>
            <th>Summary Date</th>
            <th>Total Bookings</th>
            <th>Total Sales</th>
          </thead>
          <tbody>
          {summaries.map(summary => (
            <tr>
              <td>id</td>
              <td>{summary.summary_date}</td>
              <td>{summary.total_bookings}</td>
              <td>{summary.total_sales}</td>

            </tr>
          ))}
          </tbody>
        </table>
      ) : (
        <p>No summaries available yet.</p>
      )}
    </div>
  );
}

export default SummariesTab;
