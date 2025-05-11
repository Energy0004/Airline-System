
  <template>
    <div class="container">
      <div class="content-card">
        <h1>Available Flights</h1>
        <!-- Loading spinner -->
        <p v-if="loading">Loading flights...</p>
  
        <!-- Error message -->
        <p v-if="error" class="error">{{ error }}</p>
  
        <!-- Flights table -->
        <table v-if="!loading && flights.length > 0">
          <thead>
            <tr>
              <th>Origin</th>
              <th>Destination</th>
              <th>Duration</th>
              <th>Capacity</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="flight in flights" :key="flight.id">
              <td>
                <router-link :to="{ name: 'AirportDetails', params: { id: flight.origin.id } }" class="table-link">
                  {{ flight.origin.city_name }} ({{ flight.origin.code }})
                </router-link>
              </td>
              <td>
                <router-link :to="{ name: 'AirportDetails', params: { id: flight.destination.id } }" class="table-link">
                  {{ flight.destination.city_name }} ({{ flight.destination.code }})
                </router-link>
              </td>
              <td>{{ flight.duration }} min</td>
              <td>{{ flight.capacity }}</td>
              <td>
                <router-link :to="{ name: 'FlightDetails', params: { id: flight.id } }" class="btn">
                  View Details
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
  
        <!-- No flights fallback -->
        <p v-if="!loading && flights.length === 0">
          No flights available at the moment. Please check back later.
        </p>
  
        <div class="action-buttons">
          <router-link v-if="isAuthenticated" :to="`/manage-booking/`" class="btn btn-secondary">
            Manage My Booking
          </router-link>
        </div>
      </div>
    </div>
  </template>

<script>
  import axios from 'axios';
  
  export default {
    name: 'FlightList',
    data() {
      return {
        flights: [],
        loading: false,
        error: null,
      };
    },
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('auth_token');
      }
    },
    methods: {
      fetchFlights() {
        this.loading = true;
        this.error = null;
  
        axios
          .get('http://127.0.0.1:8000/api/flights/')
          .then((response) => {
            this.flights = response.data;
          })
          .catch((error) => {
            console.error('Error fetching flights:', error);
            this.error = 'Failed to load flights. Please try again later.';
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
    mounted() {
      this.fetchFlights();
    },
  };
  </script>

<style scoped>
:root {
    --primary: #1174fd;
    --primary-dark: #0d5bc7;
    --secondary: #34c759;
    --gray-light: #f8f9fa;
    --gray: #e9ecef;
    --dark: #343a40;
    --danger: #dc3545;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background-color: var(--gray-light);
    color: var(--dark);
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

.content-card {
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    padding: 25px;
    margin-bottom: 20px;
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
    color: var(--dark);
}

a {
    color: var(--primary);
    text-decoration: none;
    transition: all 0.3s ease;
}

a:hover {
    color: var(--primary-dark);
    text-decoration: underline;
}

.btn {
    display: inline-block;
    background-color: var(--primary);
    color: white;
    padding: 6px 10px;
    border-radius: 4px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: 13px;
    transition: all 0.3s ease;
    white-space: nowrap;
}

.btn:hover {
    background-color: var(--primary-dark);
    text-decoration: none;
    color: white;
}

.btn-secondary {
    background-color: var(--secondary);
}

.btn-secondary:hover {
    background-color: #2aa84a;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    margin-bottom: 20px;
}

th,
td {
    padding: 12px 15px;
    text-align: center;
    vertical-align: middle;
    border-bottom: 1px solid var(--gray);
}

th {
    background-color: var(--primary);
    color: white;
    font-weight: 500;
}

tr:hover {
    background-color: var(--gray-light);
}

.error {
    color: var(--danger);
    margin-top: 1rem;
}

.action-buttons {
    margin-top: 20px;
    display: flex;
    gap: 10px;
    justify-content: center;
}
</style>