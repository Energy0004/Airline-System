<template>
  <div class="not-found-container">
    <h1>🚫 404 - Page Not Found</h1>
    <p>Oops! The page you're looking for doesn't exist.</p>
    <router-link to="/" class="home-link">Go back home</router-link>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
};
</script>

<style scoped>
.not-found-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  text-align: center;
  padding: 2rem;
  background: #f9f9f9;
}

.not-found-container h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #ff5252;
}

.not-found-container p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #666;
}

.home-link {
  display: inline-block;
  padding: 0.8rem 1.5rem;
  background-color: #1976d2;
  color: white;
  border-radius: 8px;
  text-decoration: none;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.home-link:hover {
  background-color: #1565c0;
}
</style>