<template>
  <div class="content-card">
    <h1>{{ airport.city_name }} ({{ airport.code }}) Airport</h1>

    <div class="airport-info">
      <!-- Departures Section -->
      <div v-if="departures.length" class="departures">
        <h2>Departures</h2>
        <table>
          <thead>
            <tr>
              <th>Destination</th>
              <th>Duration</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="flight in departures" :key="flight.id">
              <td>
                <router-link :to="`/airport/${flight.destination.id}`" class="table-link">
                  {{ flight.destination.city_name }} ({{ flight.destination.code }})
                </router-link>
              </td>
              <td>{{ flight.duration }} minutes</td>
              <td>
                <router-link :to="{ name: 'FlightDetails', params: { id: flight.id } }" class="btn">
                  View Flight
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No departures from this airport.</p>

      <!-- Arrivals Section -->
      <div v-if="arrivals.length" class="arrivals">
        <h2>Arrivals</h2>
        <table>
          <thead>
            <tr>
              <th>Origin</th>
              <th>Duration</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="flight in arrivals" :key="flight.id">
              <td>
                <router-link :to="`/airport/${flight.origin.id}`" class="table-link">
                  {{ flight.origin.city_name }} ({{ flight.origin.code }})
                </router-link>
              </td>
              <td>{{ flight.duration }} minutes</td>
              <td>
                <router-link :to="{ name: 'FlightDetails', params: { id: flight.id } }" class="btn">
                  View Flight
                </router-link>              
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else>No arrivals to this airport.</p>
    </div>

    <!-- Action Buttons -->
    <div class="action-buttons">
      <router-link to="/" class="btn btn-secondary">Return to Homepage</router-link>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AirportInfo",
  data() {
    return {
      airport: "",
      departures: [],
      arrivals: [],
    };
  },
  methods: {
    fetchAirportData() {
      const airportId = this.$route.params.id;
      axios
        .get(`http://127.0.0.1:8000/api/airports/${airportId}/`)
        .then((response) => {
          this.airport = response.data.airport;
          this.departures = response.data.departures;
          this.arrivals = response.data.arrivals;
        })
        .catch((error) => {
          console.error("Error fetching airport data:", error);
        });
    },
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler() {
        this.fetchAirportData();
      },
    },
  },
};
</script>


<style>
:root {
  --primary: #1174fd;
  --primary-dark: #0d5bc7;
  --secondary: #34c759;
  --gray-light: #f8f9fa;
  --gray: #e9ecef;
  --dark: #343a40;
  --danger: #dc3545;
}

.content-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 30px;
  margin-bottom: 30px;
}

h1 {
  font-size: 28px;
  margin-bottom: 20px;
  color: var(--dark);
  font-weight: 600;
}

h2 {
  font-size: 22px;
  color: var(--dark);
  margin-bottom: 15px;
  font-weight: 500;
}

.airport-info {
  margin-bottom: 30px;
}

.departures,
.arrivals {
  margin-bottom: 40px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}

th,
td {
  padding: 12px 15px; /* Consistent padding */
  text-align: center; /* Center text in cells */
  border-bottom: 1px solid var(--gray);
  vertical-align: middle; /* Ensures vertical centering */
  line-height: 1.5;
}

th {
  background-color: var(--primary);
  color: white;
  font-weight: 600;
  text-align: center; /* Center header text */
}

tr:hover {
  background-color: var(--gray-light);
}

.table-link {
  color: var(--primary);
  text-decoration: none;
  transition: all 0.3s ease;
}

.table-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

.btn {
  display: inline-block;
  background-color: var(--primary);
  color: white;
  padding: 6px 10px; /* Reduced padding for better fit */
  border-radius: 4px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 13px; /* Slightly smaller font for compactness */
  line-height: 1.5;
  transition: all 0.3s ease;
  white-space: nowrap; /* Prevents button text from wrapping */
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

.action-buttons {
  margin-top: 30px;
  display: flex;
  gap: 15px;
  justify-content: center; /* Centers the action buttons */
}
</style>