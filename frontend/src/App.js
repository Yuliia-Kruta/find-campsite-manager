


/*function App() {


  const [error, setError] = useState("");
  const [message, setMessage] = useState("")

  const handleGetBooking = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/get-booking');
      setBookings(prevBookings => [response.data.booking, ...prevBookings]);
      setMessage(response.data.message);
    } catch (error) {
      console.log(error.response.data)
      setError(error.response?.data?.error || "Error processing the booking");
    }
  };


export default App;*/

import Main from "./components/Main";


function App() {

  /*useEffect(() => {
    // Fetch the most recent bookings on component mount
    axios.get('/api/recent_bookings')
      .then(response => {
        setBookings(response.data.bookings);
        setSummaries(response.data.summaries); // Get initial summaries as well
      })
      .catch(error => {
        console.error("Error fetching initial data!", error);
      });
  }, []);*/

  

  return (
    <div className="App">
      <Main />
    </div>
  );
}

export default App;
