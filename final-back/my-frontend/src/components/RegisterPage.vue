<template>
  <div class="container">
    <div class="content-card">
      <h1>Register</h1>
      <!-- Error message -->
      <!-- <p v-if="error" class="error">{{ error }}</p> -->
      <p v-for="(err, index) in error" :key="index" class="error">{{ err }}</p>

      <form @submit.prevent="submitForm">
        <!-- Username -->
        <div class="form-group">
          <label for="username">Username</label>
          <input placeholder="Enter your username" type="text" id="username" v-model="username" required />
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email">Email</label>
          <input placeholder="Enter your email" type="email" id="email" v-model="email" required />
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>
          <input placeholder="Enter your password" type="password" id="password" v-model="password" required />
        </div>

        <!-- Confirm Password -->
        <div class="form-group">
          <label for="confirmPassword">Confirm Password</label>
          <input placeholder="Repeat your password" type="password" id="confirmPassword" v-model="confirmPassword" required />
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn btn-primary">Register</button>
      </form>

      <div class="action-buttons">
        <router-link to="/login" class="btn btn-secondary">
          Already have an account? Login here
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: "RegisterPage",
    data() {
      return {
        username: "",
        email: "",
        password: "",
        confirmPassword: "",
        error: null,
      };
    },
    methods: {
      async submitForm() {
        if (this.password !== this.confirmPassword) {
          this.error = ["Passwords do not match!"];
          return;
        }
  
        const formData = {
          username: this.username,
          email: this.email,
          password: this.password,
          second_password: this.confirmPassword,
        };
  
        try {
          const response = await fetch("http://127.0.0.1:8000/api/auth/register/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(formData),
          });
  
          const data = await response.json();
          console.log(data)
          if (response.status === 201) {
            if (data.tokens && data.tokens.access) {
              localStorage.setItem('auth_token', data.tokens.access);
              localStorage.setItem('user', JSON.stringify(data.user));
              window.location.href = '/';
            } else {
              this.error = ["Token not received from server. Please try again."];
            }
          } else {
            this.error = data.password || data.email || data.username || ["Registration failed. Please try again."];
          }
        } catch (err) {
          this.error = ["An error occurred. Please try again."];
          console.error(err);
        }
      },
    },
  };
  </script>
    

<style scoped>
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
