<template>
  <div class="container">
    <div class="content-card">
      <h1>Login</h1>

      <!-- Error message -->
      <p v-if="error" class="error">{{ error }}</p>

      <!-- Login Form -->
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Enter your username"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            placeholder="Enter your password"
            required
          />
        </div>

        <button type="submit" class="btn" :disabled="loading">
          <span v-if="loading">Logging in...</span>
          <span v-else>Login</span>
        </button>
      </form>

      <div class="action-buttons">
        <router-link to="/register" class="btn btn-secondary">
          Don't have an account? Register here
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  
  export default {
    name: 'LoginPage',
    data() {
      return {
        username: '',
        password: '',
        loading: false,
        error: null,
      };
    },
    methods: {
      handleLogin() {
        this.loading = true;
        this.error = null;

        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
  
        // Send login request with username, and password
        axios
          .post('http://127.0.0.1:8000/api/auth/login/', {
            username: this.username,
            password: this.password,
          })
          .then((response) => {
            // Assuming the response contains 'tokens' with access token
            const { tokens } = response.data;
            // console.log(tokens)
            
            // Store the token in localStorage or sessionStorage
            localStorage.setItem('auth_token', tokens.access);  // You can use sessionStorage instead of localStorage if needed
            
            // Optional: Store the user information for later use (optional)
            localStorage.setItem('user', JSON.stringify(response.data.user));
  
            // Redirect to the homepage or dashboard after successful login
            // this.$router.push({ name: 'Home' }); // Or any other route you want to redirect to
            window.location.href = '/'
          })
          .catch((error) => {
            console.error('Error during login:', error);
            this.error = 'Invalid username, or password. Please try again.';
          })
          .finally(() => {
            this.loading = false;
          });
      },
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
  max-width: 450px;
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
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 14px;
  color: var(--dark);
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid var(--gray);
  border-radius: 4px;
  font-size: 16px;
}

input:focus {
  outline: none;
  border-color: var(--primary);
}

.btn {
  display: inline-block;
  background-color: var(--primary);
  color: white;
  padding: 10px 15px;
  border-radius: 4px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
  transition: all 0.3s ease;
}

.btn:hover {
  background-color: var(--primary-dark);
}

.btn:disabled {
  background-color: var(--gray);
  cursor: not-allowed;
}

.btn-secondary {
  background-color: var(--secondary);
}

.btn-secondary:hover {
  background-color: #2aa84a;
}

.error {
  color: var(--danger);
  margin-top: 1rem;
  text-align: center;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}
</style>
