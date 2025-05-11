<template>
    <div class="container">
      <div class="content-card">
        <h1>✈️ Flight Details</h1>
  
        <div v-if="loading" class="loading-msg">
          Loading flight details...
        </div>
        <p v-if="error" class="error">{{ error }}</p>
  
        <div v-if="flight" class="flight-info">
          <div class="route">
            <span class="from">
              <strong>From:</strong> {{ flight.origin.city_name }} ({{ flight.origin.code }})
            </span>
            <span class="arrow">→</span>
            <span class="to">
              <strong>To:</strong> {{ flight.destination.city_name }} ({{ flight.destination.code }})
            </span>
          </div>
  
          <div class="detail-row">
            <strong>Duration:</strong>
            <span>{{ flight.duration }} minutes</span>
          </div>
  
          <div class="detail-row">
            <strong>Capacity:</strong>
            <span>{{ flight.capacity }} passengers</span>
          </div>
  
          <div v-if="flight.passengers && flight.passengers.length" class="passengers-list">
                <h3>🧑‍✈️ Passengers on this flight:</h3>
                <ul>
                <li v-for="(passenger, index) in flight.passengers" :key="index">
                    <div class="passenger-info">
                    <div class="avatar">{{ passenger.name[0] }}</div>
                    <div>
                        <div class="name">{{ passenger.name }}</div>
                        <div class="email">{{ passenger.email }}</div>
                    </div>
                    </div>
                </li>
                </ul>
            </div>
          <div v-else class="no-passengers">
            <p>No passengers have booked this flight yet.</p>
          </div>
        </div>
  
        <div class="action-buttons">
          <router-link to="/" class="btn btn-secondary">
            ← Back to All Flights
          </router-link>
  
          <router-link v-if="isAuthenticated && flight" :to="`/booking/${flight.id}`" class="btn btn-primary">
            Book This Flight
          </router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'FlightDetails',
    data() {
      return {
        flight: null,
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
      fetchFlightDetails() {
        this.loading = true;
        this.error = null;
  
        const flightId = this.$route.params.id;
        axios
          .get(`http://127.0.0.1:8000/api/flights/${flightId}/`)
          .then((response) => {
            this.flight = response.data;
          })
          .catch((error) => {
            console.error('Error fetching flight details:', error);
            this.error = 'Failed to load flight details.';
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
    mounted() {
      this.fetchFlightDetails();
    },
  };
  </script>
  
  <style scoped>
  h1 {
    font-size: 24px;
    margin-bottom: 20px;
    color: var(--dark);
  }
  
  .loading-msg {
    font-size: 16px;
    color: #6c757d;
    padding: 15px;
    background-color: var(--gray-light);
    border-radius: 4px;
    margin-bottom: 15px;
    text-align: center;
  }
  
  .flight-info {
    margin-top: 20px;
  }
  
  .route {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    font-size: 18px;
    margin-bottom: 20px;
    background-color: var(--gray-light);
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }
  
  .arrow {
    font-size: 24px;
    color: var(--primary);
  }
  
  .detail-row {
    display: flex;
    justify-content: space-between;
    background-color: #f8f9fa;
    padding: 12px 20px;
    margin-bottom: 10px;
    border-radius: 6px;
    border: 1px solid var(--gray);
    font-size: 16px;
  }
  
  .passengers-list {
  background-color: white;
  border: 1px solid var(--gray);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin-top: 20px;
}

.passengers-list h3 {
  font-size: 20px;
  color: var(--primary);
  margin-bottom: 15px;
}

.passengers-list ul {
  list-style: none;
  padding: 0;
}

.passengers-list li {
  padding: 10px 0;
  border-bottom: 1px solid var(--gray);
}

.passengers-list li:last-child {
  border-bottom: none;
}

.passengers-list li:hover {
  background-color: var(--gray-light);
}

.passenger-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  margin-right: 15px;
}

.name {
  font-weight: 600;
  font-size: 16px;
  color: var(--dark);
}

.email {
  color: #6c757d;
  font-size: 14px;
}
  
  .no-passengers {
    margin-top: 20px;
    font-style: italic;
    color: #888;
  }
  
  .action-buttons {
    margin-top: 30px;
    display: flex;
    justify-content: space-between;
    gap: 15px;
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
    line-height: 1.5;
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
  </style>  