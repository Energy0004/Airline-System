<template>
    <div class="container">
      <div class="content-card">
        <h1>📄 Booking Details</h1>
  
        <!-- Loading spinner -->
        <div v-if="loading" class="loading-msg">⏳ Loading booking details...</div>
  
        <!-- Error message -->
        <div v-if="errorMsg" class="error-msg">❌ {{ errorMsg }}</div>
  
        <!-- Booking info -->
        <div v-if="booking" class="booking-info">
          <h2>✈️ Flight Information</h2>
          <div class="info-card">
            <p><strong>From:</strong> {{ booking.flight.origin.city_name }} ({{ booking.flight.origin.code }})</p>
            <p><strong>To:</strong> {{ booking.flight.destination.city_name }} ({{ booking.flight.destination.code }})</p>
            <p><strong>Duration:</strong> {{ booking.flight.duration }} minutes</p>
          </div>
  
          <h2>🧍 Passenger Information</h2>
          <div class="info-card">
            <p><strong>Username:</strong> {{ booking.passenger.name }}</p>
            <p><strong>Email:</strong> {{ booking.passenger.email }}</p>
          </div>
  
          <h2>🔖 Booking Information</h2>
          <div class="info-card">
            <p><strong>Booking Code:</strong> {{ booking.booking_code }}</p>
            <p><strong>Booked At:</strong> {{ formatDate(booking.created_at) }}</p>
          </div>
        </div>
  
        <div class="action-buttons">
          <router-link to="/" class="btn btn-secondary">← Back to Home</router-link>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { format } from 'date-fns';

  export default {
    name: 'BookingDetails',
    data() {
      return {
        booking: null,
        loading: true,
        errorMsg: '',
      };
    },
    methods: {
        formatDate(dateString) {
            const date = new Date(dateString);
            return format(date, 'MMMM d, yyyy h:mm a');
        },
      fetchBooking() {
        const token = localStorage.getItem("auth_token");
        const bookingCode = this.$route.params.code;
        console.log("Here is the booking code:", bookingCode);
        axios
          .get(`http://127.0.0.1:8000/api/bookings/${bookingCode}/`, {
            headers: {
                Authorization: `Bearer ${token}`
            },
          })
          .then((response) => {
            this.booking = response.data;
          })
          .catch((error) => {
            console.error('Error fetching booking:', error);
            if (error.response && error.response.status === 404) {
              this.errorMsg = 'Booking not found. Please check your code.';
            } else {
              this.errorMsg = 'Failed to load booking. Please try again.';
            }
          })
          .finally(() => {
            this.loading = false;
          });
      },
    },
    mounted() {
      this.fetchBooking();
    },
  };
  </script>
  
  <style scoped>
  .container {
    max-width: 700px;
    margin: 0 auto;
    padding: 20px;
  }
  
  .content-card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 30px;
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
    margin-top: 20px;
    margin-bottom: 10px;
  }
  
  .info-card {
    background-color: var(--gray-light);
    padding: 15px 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    margin-bottom: 20px;
  }
  
  .info-card p {
    margin: 8px 0;
    font-size: 16px;
    color: var(--dark);
  }
  
  .loading-msg,
  .error-msg {
    margin-top: 20px;
    padding: 15px;
    border-radius: 6px;
    font-size: 16px;
    text-align: center;
  }
  
  .loading-msg {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
  }
  
  .error-msg {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
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