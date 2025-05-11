<template>
    <div class="container">
      <div class="content-card">
        <h1>🛫 Book Flight</h1>
  
        <!-- Redirect message if guest -->
        <div v-if="!isAuthenticated" class="error-msg">
          ❌ You must be logged in to book a flight. <router-link to="/login">Login here</router-link>.
        </div>
  
        <!-- Flight info -->
        <div v-if="flight" class="flight-info">
          <div class="route">
            <span>🛫 <strong>From:</strong> {{ flight.origin.city_name }} ({{ flight.origin.code }})</span>
            <span class="arrow">→</span>
            <span>🛬 <strong>To:</strong> {{ flight.destination.city_name }} ({{ flight.destination.code }})</span>
          </div>
          <p>⏱️ <strong>Duration:</strong> {{ flight.duration }} minutes</p>
          <p>👥 <strong>Capacity:</strong> {{ flight.capacity }} passengers</p>
        </div>
  
        <!-- Booking form -->          
        <form v-if="isAuthenticated" @submit.prevent="submitBooking" class="booking-form">
          <h2>Passenger Details</h2>
          <div v-if="errorMsg" class="error-msg">❌ {{ errorMsg }}</div>
          <br>
          <div class="passenger-card">
            <label>
              Username:
              <input v-model="passenger.username" required placeholder="Enter username" />
            </label>
            <label>
              Email:
              <input type="email" v-model="passenger.email" required placeholder="Enter email address" />
            </label>
          </div>
  
          <button type="submit" class="btn submit-btn" :disabled="loading">
            {{ loading ? 'Booking...' : 'Confirm Booking' }}
          </button>
        </form>
  
        <!-- Success/Error messages -->
        <!-- <div v-if="successMsg" class="success-msg">✅ {{ successMsg }}</div>
        <div v-if="errorMsg" class="error-msg">❌ {{ errorMsg }}</div>
   -->
        <div class="action-buttons">
          <router-link to="/" class="btn btn-secondary">← Back to Home</router-link>
        </div>
      </div>
    </div>
  </template>

<script>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';

export default {
  name: 'BookFlight',
  data() {
    return {
      flight: null,
      passenger: {
        username: '',
        email: ''
      },
      loading: false,
      successMsg: '',
      errorMsg: '',
    };
  },
  computed: {
    isAuthenticated() {
      const token = localStorage.getItem('auth_token');
      if (!token) return false;

      try {
        const decoded = jwtDecode(token);
        if (!decoded || !decoded.exp) return false;
        const now = Date.now() / 1000;
        return decoded.exp > now;
      } catch (e) {
        console.error('Invalid token:', e);
        return false;
      }
    }
  },
  methods: {
    fetchFlightDetails() {
      const flightId = this.$route.params.id;
      axios
        .get(`http://127.0.0.1:8000/api/flights/${flightId}/`)
        .then((response) => {
          this.flight = response.data;
        })
        .catch((error) => {
          console.error('Error fetching flight:', error);
        });
    },
    submitBooking() {
        this.loading = true;
        // this.successMsg = '';
        // this.errorMsg = '';

        const token = localStorage.getItem('auth_token');
        const flightId = this.$route.params.id;

        axios
            .post(`http://127.0.0.1:8000/api/bookings/`,{
                flight_id: flightId,
                username: this.passenger.username,
                email: this.passenger.email,
            },{
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
            )
            .then((response) => {
            const bookingId = response.data.id;

            this.$router.push(`/booking-confirmation/${bookingId}`);
            })
            .catch((error) => {
                console.error('Booking error:', error);
                if (error.response && error.response.data) {
                    const errorData = error.response.data;
                    this.errorMsg = errorData.error || errorData.detail || 'Booking failed. Please try again.';
                } else {
                    this.errorMsg = 'Booking failed. Please try again.';
                }
            })
            .finally(() => {
                this.loading = false;
            });
        }
  },
  mounted() {
    this.fetchFlightDetails();
  },
};
</script>
  
  <style scoped>
  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .content-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 20px;
  }
  
  h1 {
    font-size: 28px;
    color: var(--dark);
    text-align: center;
    margin-bottom: 25px;
  }
  
  h2 {
    font-size: 22px;
    color: var(--primary);
    margin: 20px 0 15px;
  }
  
  .flight-info {
    background-color: var(--gray-light);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 25px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  .route {
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    margin-bottom: 15px;
  }
  
  .arrow {
    font-size: 26px;
    color: var(--primary);
  }
  
  .flight-info p {
    font-size: 16px;
    margin: 8px 0;
    color: var(--dark);
  }
  
  .booking-form {
    margin-top: 20px;
  }
  
  .passenger-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid var(--gray);
    margin-bottom: 20px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }
  
  label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    color: var(--dark);
  }
  
  input {
    width: 100%;
    padding: 10px;
    border: 1px solid var(--gray);
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.3s ease;
  }
  
  input:focus {
    border-color: var(--primary);
    outline: none;
  }
  
  .submit-btn {
    width: 100%;
    padding: 12px 20px;
    font-size: 16px;
    background-color: var(--primary);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-top: 20px;
  }
  
  .submit-btn:hover {
    background-color: var(--primary-dark);
  }
  
  .submit-btn:disabled {
    background-color: var(--gray);
    cursor: not-allowed;
  }
  
  .success-msg {
    margin-top: 20px;
    padding: 15px;
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 6px;
    font-size: 16px;
  }
  
  .error-msg {
    margin-top: 20px;
    padding: 15px;
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 6px;
    font-size: 16px;
  }
  
  .action-buttons {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    gap: 15px;
  }
  
  .btn-secondary {
    background-color: var(--secondary);
    color: white;
    padding: 10px 20px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 14px;
    transition: background-color 0.3s ease;
  }
  
  .btn-secondary:hover {
    background-color: #2aa84a;
  }
  </style>