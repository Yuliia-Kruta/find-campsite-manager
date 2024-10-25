function SummariesTab({ summaries }) {
  return (
    <div className="summaries-tab">
      {summaries.length > 0 ? (
        <table>
          <thead>
            <th>Summary ID</th>
            <th>Summary Date</th>
            <th>Total Bookings</th>
            <th>Total Sales (AUD)</th>
          </thead>
          <tbody>
            {summaries.map((summary, index) => (
              <tr key={index}>
                <td>{summary.summary_id || summaries.length}</td>
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
