<template>
  <div>
    <Navbar />
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
import Navbar from './components/Navbar.vue';

export default {
  components: {
    Navbar,
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

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  margin-bottom: 20px;
}

th,
td {
  padding: 12px 15px;
  text-align: center; /* Center text in cells */
  border-bottom: 1px solid var(--gray);
  vertical-align: middle; /* Ensures vertical centering */
  line-height: 1.5;
}

th {
  background-color: var(--primary);
  color: white;
  font-weight: 500;
  text-align: center; /* Center header text */
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
  justify-content: center; /* Centers the action buttons */
}
</style>