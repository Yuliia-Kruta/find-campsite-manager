<h1 align="center">Find Campsite Manager</h1>
<br/>
<img align="center" src="./find-campsite-manager.gif" width="70%" height="auto"/>
<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Project Link: <a target="new" href=update>Live Demo</a>
<br/>
<br/>
<h2>Project description</h2>
<b>Find Campsite Manager</b> is a robust booking management system implemented in the individual campgrounds to streamline the booking process, ensuring efficient handling of reservations and site allocations. <br/><br/>
The application utilises <b>Python</b> for backend processing and database interactions, with <b>Flask</b> serving as the framework for handling HTTP requests. The application’s frontend built with <b>React</b> provides an intuitive and responsive interface for managers to launch the retrieval and processing of bookings from the Head Office, view and search the booking details and summaries, and retrieve customer booking confirmation in pdf format. <br/>
The system architecture includes 2 <b>Azure SQL</b> databases and 1 <b>Azure MongoDB</b> database.

<h2>Features</h2>
<ul>
  <li>Retrieving bookings from Head Office SQL database.</li>
  <li>Preparing and storing booking details in the NoSQL document database. Includes allocation of campsites.</li>
  <li>Storing and managing campground campsites’ information in the NoSQL document database.</li>
  <li>Creating confirmation documents for customers.</li>
  <li>Summarising daily bookings in the table in the local SQL database.</li>
  <li>Sending booking summaries to the Head Office database.</li>
</ul>

<h2>Technologies Used</h2>
<a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>&nbsp;
<a href="https://flask.palletsprojects.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original-wordmark.svg" alt="flask" width="40" height="40"/> </a>&nbsp;
reportlab&nbsp;
<a href="https://azure.microsoft.com/en-in/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/microsoft_azure/microsoft_azure-icon.svg" alt="azure" width="40" height="40"/> </a>&nbsp;
<a href="https://www.mongodb.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/mongodb/mongodb-original-wordmark.svg" alt="mongodb" width="40" height="40"/>&nbsp;
<a href="https://reactjs.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/react/react-original-wordmark.svg" alt="react" width="40" height="40"/> </a>&nbsp;
<a href="https://www.w3schools.com/css/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/css3/css3-original-wordmark.svg" alt="css3" width="40" height="40"/> </a>&nbsp;
<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a>&nbsp;
Axios

<h2>API Endpoints</h2>
<table>
  <thead>
    <tr>
      <th>Endpoint</th>
      <th>Method</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>/get-booking</code></td>
      <td>POST</td>
      <td>Fetches and processes the booking: retrieves booking from Head Office database, finds available campsites that suit booking requirements, retrieves customer details, stores grouped booking information in document database, updates campsite availability, creates and stores daily summary in SQL database.</td>
    </tr>
    <tr/></tr>
    <tr>
      <td><code>/fetch-from-db</code></td>
      <td>POST</td>
      <td>Returns all existing bookings and summaries from the databases.</td>
    </tr>
  </tbody>
</table>

<h2>Database Design</h2>

The management system employs 3 databases hosted on Azure:

1. MongoDB (Cosmos DB) <code>campground_db</code> database. This is a NoSQL document database that contains 2 collections: <b>campsites</b> and <b>bookings</b>.
2. Azure SQL <code>summary</code> database for storing daily booking summaries at each campground.<br/>
<b>Schema:</b><br/>
summaries (<br/>
	  &nbsp;&nbsp;summary_id        	int   IDENTITY(1,1)  PRIMARY KEY,<br/>
	  &nbsp;&nbsp;summary_date	    	date  NULL,<br/>
    &nbsp;&nbsp;total_bookings    	int  NULL,<br/>
	  &nbsp;&nbsp;total_sales           	decimal (10, 2) NULL<br/>
)
3. Azure SQL <code>camping</code> database which acts as Head Office database.

<h2>Getting Started</h2>
To get a local copy up and running, follow these simple steps.

<h3>Prerequisites</h3>
<h5>1. Make sure you have all the following installed:</h5>
- Python 3.x<br/>
- Node.js & npm<br/>
<h5>2. Setup databases in Azure:</h5>
- SQL <code>camping</code> database. The SQL scripts for creating tables and loading sample data can be found in the project directory.<br/>
- Cosmos DB <code>campground_db</code> database with 2 collections: <code>campsites</code> and <code>bookings</code>.<br/>
- SQL <code>summaries</code> database. The schema is provided in the previous section.<br/>

<h3>Installation</h3>
<h5>Clone the repository:</h5>
https://github.com/Yuliia-Kruta/find-campsite-manager.git

<h5>Navigate to the project directory:</h5>
<code>cd find-campsite</code>

<h3>Backend Setup</h3>

<h5>Navigate to the project backend folder:</h5>
<code>cd backend</code>

<h5>Install the backend dependencies:</h5>
<code>pip install -r py_dependencies.txt</code>

<h5>Create a .env file in the backend directory and add all your connection details to all databases:</h5>
CAMPING_SERVER=<br/>
CAMPING_DB_NAME=<br/>
CAMPING_USERNAME=<br/>
CAMPING_PASSWORD=<br/>
CAMPGROUND_USERNAME=<br/>
CAMPGROUND_PASSWORD=<br/>
CAMPGROUND_URL=<br/>
CAMPGROUND_DB_NAME=<br/>
SUMMARIES_SERVER=<br/>
SUMMARIES_DB_NAME=<br/>
SUMMARIES_USERNAME=<br/>
SUMMARIES_PASSWORD=<br/>

<h5>Run the backend:</h5>
<code>python3 app.py</code>

<h3>Frontend Setup</h3>
<h5>Open a new terminal and navigate to the frontend directory:</h5>
<code>cd frontend</code>
<h5>Install the frontend dependencies:</h5>
<code>npm install</code>
<h5>Run the frontend:</h5>
<code>npm start</code>
<br/><br/>
The app will be available at http://localhost:3000.

<h2>Reflection</h2>
This project was created for the uni assignmnet, hence it strictly follows specific task requirements. For it to be more reflective of real-world scenarios, some modifications and improvements should be made, such as getting rid of global variables, adjusting the trigger for daily summaries, making the available dates array for campsites more dynamic, enhancing booking summaries, etc.


<h2>License</h2>
Distributed under the MIT License. See LICENSE for more information.
