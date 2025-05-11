<template>
    <header>
      <div v-if="showPromoBanner" class="promo-banner">
          🎉 Welcome! Here’s your promo code: <strong>{{ promoCode }}</strong>
      </div>
      <div class="container header-content">
        <div class="logo">
          <router-link to="/">SkyJourney Airways</router-link>
        </div>
        
        <div class="header-buttons">
          <!-- Display a welcome message when the user is logged in -->
          <span v-if="username" class="welcome-msg">Welcome, {{ username }}</span>

          <!-- Profile and Manage Booking links only visible when user is logged in -->
          <router-link v-if="username" to="/profile" class="btn btn-outline">Profile</router-link>
          <router-link v-if="username" to="/manage-booking" class="btn btn-outline">Manage My Booking</router-link>

          <!-- Login/Register links for non-logged-in users -->
          <div v-else class="log-container">
            <router-link to="/login" class="btn btn-primary">Login</router-link>
            <router-link to="/register" class="btn btn-outline-primary">Register</router-link>
          </div>

          <!-- Logout button for logged-in users -->
          <button v-if="username" @click="logout" class="btn btn-outline-danger">Logout</button>
        </div>
      </div>
    </header>
  </template>
  <script>
  import axios from 'axios';

  export default {
    name: 'Navbar',
    data() {
      return {
        username: null,
        promoCode: null,
        showPromoBanner: false,
      };
    },
    mounted() {
      const accessToken = localStorage.getItem('auth_token');
      //   console.log(accessToken);
      if (accessToken) {
        fetch('http://127.0.0.1:8000/api/auth/profile/', {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.username) {
              this.username = data.username;
            }
          })
          .catch((error) => {
            console.error('Error fetching user profile:', error);
          });
      }
      axios.get('http://127.0.0.1:8000/api/promo-code/', { withCredentials: true })
      .then(response => {
        const token = localStorage.getItem("auth_token");
        // console.log(response)
        if (response.data.promo_code && !token) {
          this.promoCode = response.data.promo_code;
          localStorage.setItem('promo_code', response.data.promo_code)
          this.showPromoBanner = true;
          setTimeout(() => { this.showPromoBanner = false; }, 5000);
        }
      })
      .catch(error => {
        console.error('Error fetching promo code:', error);
      });
    },
    methods: {
      logout() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
  
        // this.$router.push('/');
        window.location.href = '/';
  
        this.username = null;
      }
    }
  };
  </script>
  
 

<style scoped>
.promo-banner {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg, #ff9800, #ff5722);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  font-size: 1rem;
  animation: slideIn 0.5s ease, fadeOut 1s ease 4s forwards;
}

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes fadeOut {
  to { opacity: 0; transform: translateX(100%); }
}
header {
    background-color: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    padding: 15px 0;
    margin-bottom: 30px;
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
}

.logo {
    font-size: 24px;
    font-weight: bold;
    color: #1174FD;
}

.header-buttons {
    display: flex;
    align-items: center;
    gap: 10px;
}

.welcome-msg {
    font-size: 1rem;
    font-weight: 600;
    color: #007bff;
    background-color: #e6f0ff;
    padding: 6px 12px;
    border-radius: 8px;
    margin-right: 10px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    display: inline-block;
}

/* Buttons */
.btn {
    display: inline-block;
    background-color: #1174FD;
    color: white;
    padding: 10px 15px;
    border-radius: 4px;
    text-decoration: none;
    border: none;
    cursor: pointer;
    font-size: 16px;
    transition: all 0.3s ease;
}

.btn:hover {
    background-color: #0d5bc7;
    text-decoration: none;
    color: white;
}

.btn-outline {
    background: transparent;
    border: 2px solid #333;
    color: #333;
}

.btn-outline:hover {
    background-color: #333;
    color: #fff;
}

.btn-outline-primary {
    background: transparent;
    border: 2px solid #1174FD;
    color: #1174FD;
}

.log-container {
    display: flex;
    gap: 16px;
}

.btn-outline-primary:hover {
    background-color: #1174FD;
    color: #fff;
}

.btn-outline-danger {
    background: transparent;
    border: 2px solid #dc3545;
    color: #dc3545;
}

.btn-outline-danger:hover {
    background-color: #dc3545;
    color: #fff;
}
</style>