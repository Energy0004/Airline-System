<template>
  <div class="container">
    <h1>📋 Bookings for {{ username }}</h1>

    <div v-if="bookings.length === 0">
      <p>No bookings found for this user.</p>
    </div>

    <table v-else class="table">
      <thead>
        <tr>
            <th>Booking Code</th>
            <th>Flight</th>
            <th>Date</th>
            <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="booking in bookings" :key="booking.id">
            <td>{{ booking.booking_code }}</td>
            <td>{{ booking.flight.origin.code }} → {{ booking.flight.destination.code }}</td>
            <td>{{ formatDate(booking.created_at) }}</td>
            <td>
                <button @click="openDeleteModal(booking)" class="icon-btn danger">
                    <font-awesome-icon icon="trash" />
                </button>
            </td>
        </tr>
      </tbody>
    </table>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="delete-modal-overlay">
      <div class="delete-modal-box">
        <h2>🗑️ Confirm Delete</h2>
        <p>Are you sure you want to delete booking #<strong>{{ selectedBooking.id}}</strong>?</p>
        <div class="delete-modal-actions">
          <button @click="confirmDelete" class="delete-modal-confirm-btn">
            <font-awesome-icon icon="trash" /> Yes, Delete
          </button>
          <button @click="closeDeleteModal" id="delete-modal-cancel-btn">
            <font-awesome-icon icon="times" /> Cancel
          </button>
        </div>
      </div>
    </div>
    <br>
    <router-link to="/profile" class="btn">← Back to User List</router-link>
  </div>
</template>

<script>
import axios from 'axios';
import { format } from 'date-fns';

export default {
  name: 'AdminUserBookingsPage',
  props: ['userId'],
  data() {
    return {
      bookings: [],
      showEditModal: false,
      showDeleteModal: false,
      selectedBooking: null,
    };
  },
  methods: {
    formatDate(dateString) {
        const date = new Date(dateString);
        return format(date, 'MMMM d, yyyy h:mm a'); // May 7, 2025 12:09 AM
    },
    fetchBookings() {
      const userId = this.$route.params.userId;
      axios
        .get(`http://127.0.0.1:8000/api/admin/bookings/user/${userId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('auth_token')}` },
        })
        .then((res) => {
          this.bookings = res.data;
        
        })
        .catch((err) => {
          console.error('Failed to load bookings:', err);
        });
    },
    openDeleteModal(booking) {
      this.selectedBooking = booking;
      this.showDeleteModal = true;
    },
    closeDeleteModal() {
      this.showDeleteModal = false;
    },
    confirmDelete() {
      axios
        .delete(`http://127.0.0.1:8000/api/admin/bookings/${this.selectedBooking.id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('auth_token')}` },
        })
        .then(() => {
          this.fetchBookings();
          this.closeDeleteModal();
        })
        .catch((err) => {
          console.error('Failed to delete booking:', err);
        });
    },
  },
  mounted() {
    this.fetchBookings();
  },
  computed:{
    username() {
        return this.$route.query.username;
    }
  }
};
</script>

<style scoped>
.delete-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: grid;
  place-items: center;
  z-index: 2000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.delete-modal-box {
  background: #fff;
  padding: 2rem 2.5rem;
  border-radius: 20px;
  width: 350px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
  text-align: center;
  animation: scaleIn 0.3s ease;
}

@keyframes scaleIn {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.delete-modal-box h2 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.delete-modal-box p {
  font-size: 1rem;
  color: #555;
  margin-bottom: 1.5rem;
}

.delete-modal-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.delete-modal-confirm-btn {
  background: linear-gradient(135deg, #ff4e50, #f44336);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.delete-modal-confirm-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.4);
}

#delete-modal-cancel-btn {
  background: #ddd;
  color: #333;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s ease, transform 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

#delete-modal-cancel-btn:hover {
  background: #ccc;
  transform: translateY(-2px);
}
.table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.8rem;
  border: 1px solid #ccc;
}
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
}
.icon-btn.danger {
  color: red;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
}
</style>
