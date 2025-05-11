<template>
    <div class="container">
      <div class="content-card">
        <h1>🔍 Manage Booking</h1>

        <div v-if="!isAuthenticated" class="error-msg">
        ❌ You need to log in to view this page. <router-link to="/login">Login here</router-link>.
        </div>
        <div v-else-if="isAuthenticated">
          <!-- Booking Code Input Form -->
          <div v-if="!booking" class="booking-form">
            <h2>Enter Your Booking Code</h2>
            <form @submit.prevent="fetchBooking">
              <label>
                Booking Code:
                <input v-model="bookingCode" type="text" required placeholder="Enter your booking code" />
              </label>
              <button type="submit" class="btn submit-btn" :disabled="loading">
                {{ loading ? 'Searching...' : 'Search Booking' }}
              </button>
            </form>
          </div>
    
          <!-- Error Message -->
          <div v-if="error" class="error-msg">❌ {{ error }}</div>
    
          <!-- Loading Indicator -->
          <div v-if="loading" class="loading-msg">⏳ Loading booking details...</div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
import axios from 'axios';
import { isAuthenticated } from '../utils/auth.js';

export default {
  name: 'ManageBooking',
  data() {
    return {
      bookingCode: '',
      loading: false,
      error: null,
    };
  },
  computed:{
    isAuthenticated
  },
  methods: {
    fetchBooking() {
      if (!this.bookingCode.trim()) {
        this.error = 'Please enter a booking code.';
        return;
      }
      this.loading = true;
      this.error = null;
      const token = localStorage.getItem("auth_token");
      console.log('Submitting booking code:', this.bookingCode);

      axios.post(
        `http://127.0.0.1:8000/api/manage-booking/`,
        { code: this.bookingCode },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      .then(() => {
        this.loading = false;
        this.$router.push({
          name: 'BookingDetails',
          params: { code: this.bookingCode }
        });
      })
      .catch(error => {
        this.error = 'Booking not found or invalid code. Please try again.';
        this.loading = false;
        console.error('Error fetching booking:', error);
      });
    },
    printPage() {
      window.print();
    },
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
  
  .booking-form {
    background-color: var(--gray-light);
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 20px;
  }
  
  .booking-form label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    color: var(--dark);
  }
  
  .booking-form input {
    width: 100%;
    padding: 10px;
    border: 1px solid var(--gray);
    border-radius: 6px;
    font-size: 16px;
    transition: border-color 0.3s ease;
  }
  
  .booking-form input:focus {
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
    margin-top: 15px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .submit-btn:hover {
    background-color: var(--primary-dark);
  }
  
  .submit-btn:disabled {
    background-color: var(--gray);
    cursor: not-allowed;
  }
  
  .booking-details {
    margin-top: 20px;
  }
  
  .booking-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
  }
  
  .booking-detail-card {
    background-color: white;
    border: 1px solid var(--gray);
    border-radius: 6px;
    padding: 15px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    opacity: 0;
    animation: fadeIn 0.5s ease-in-out forwards;
  }
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  
  .detail-header {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
  }
  
  .detail-header i {
    margin-right: 10px;
    color: var(--primary);
    font-size: 18px;
  }
  
  .detail-header h3 {
    font-size: 16px;
    color: var(--dark);
    margin: 0;
  }
  
  .booking-detail-card p {
    font-size: 16px;
    color: var(--dark);
    margin: 0;
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
  
  .loading-msg {
    margin-top: 20px;
    padding: 15px;
    background-color: var(--gray-light);
    color: var(--dark);
    border-radius: 6px;
    font-size: 16px;
    text-align: center;
  }
  
  .action-buttons {
    margin-top: 20px;
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
  
  @media print {
    .booking-form, .error-msg, .loading-msg, .action-buttons {
      display: none;
    }
    .booking-details {
      margin-top: 0;
    }
  }
  </style>