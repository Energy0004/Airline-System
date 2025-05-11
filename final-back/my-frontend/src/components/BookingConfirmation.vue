    <template>
        <div class="confirmation-page">
        <div class="card">
            <i class="fas fa-check-circle success-icon"></i>
            <h1>Booking Confirmed! <span class="checkmark">✅</span></h1>
            <p class="subtitle">Thank you for booking with SkyJourney Airways.</p>
            <p class="info-text">Your booking code is:</p>
            <div class="booking-code">{{ booking.booking_code }}</div>
            <p class="small-text">Please save this code to manage your booking.</p>
    
            <div class="actions">
            <button @click="goHome" class="btn btn-home">Return to Homepage</button>
            <button @click="viewBooking" class="btn btn-details">View Booking Details</button>
            </div>
        </div>
        </div>
    </template>
    
    <script>
    import axios from 'axios';

    export default {
        data() {
        return {
            booking: {
            confirmationCode: '',
            },
            loading: true,
            error: null,
        };
        },
        mounted() {
            this.fetchBookingDetails();
        },
        methods: {
        fetchBookingDetails() {
            const token = localStorage.getItem('auth_token');
            const bookingId = this.$route.params.id;
            axios
            .get(`http://127.0.0.1:8000/api/booking-confirmation/${bookingId}`,{
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            })
            .then(response => {
                this.booking = response.data;
                this.loading = false;
            })
            .catch(error => {
                this.error = 'Failed to load booking details.';
                this.loading = false;
                console.error('Error fetching booking:', error);
            });
        },
        goHome() {
            this.$router.push('/');
        },
        viewBooking() {
            this.$router.push(`/booking-details/${this.booking.booking_code}`);
        },
        },
    };
    </script>
  
  <style scoped>
  .confirmation-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #74ebd5, #acb6e5);
    padding: 20px;
  }
  
  .card {
    background: #fff;
    border-radius: 20px;
    padding: 40px;
    max-width: 500px;
    text-align: center;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    animation: fadeIn 0.6s ease;
  }
  
  .success-icon {
    font-size: 60px;
    color: #28a745;
    margin-bottom: 15px;
  }
  
  h1 {
    font-size: 28px;
    margin-bottom: 10px;
    color: #333;
  }
  
  .subtitle {
    font-size: 16px;
    color: #555;
    margin-bottom: 20px;
  }
  
  .info-text {
    font-size: 18px;
    color: #333;
    margin-bottom: 10px;
  }
  
  .booking-code {
    font-size: 32px;
    font-weight: bold;
    background: #f0f4f8;
    padding: 15px 25px;
    border-radius: 12px;
    color: #007bff;
    display: inline-block;
    margin-bottom: 10px;
    letter-spacing: 1.5px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }
  
  .small-text {
    font-size: 14px;
    color: #777;
    margin-bottom: 25px;
  }
  
  .actions {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  
  .btn {
    padding: 12px 20px;
    font-size: 16px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
  }
  
  .btn-home {
    background: #007bff;
    color: white;
  }
  
  .btn-home:hover {
    background: #0056b3;
  }
  
  .btn-details {
    background: #28a745;
    color: white;
  }
  
  .btn-details:hover {
    background: #1e7e34;
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
  
  @media (min-width: 480px) {
    .actions {
      flex-direction: row;
    }
    .btn {
      width: auto;
      min-width: 180px;
    }
  }
  </style>
  