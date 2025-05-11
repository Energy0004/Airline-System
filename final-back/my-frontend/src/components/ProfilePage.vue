<script>
  import axios from 'axios';
  import { jwtDecode } from 'jwt-decode';
  import { format } from 'date-fns';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

  
  export default {
    name: 'Profile',
    components: { FontAwesomeIcon },
    data() {
        return {
            isAdmin: false,
            user: { username: '', email: '', password: '' },
            showDeleteModal: false,
            selectedUserToDelete: null,
            showToastUpdated: false,
            showToastDeleted: false,
            showToastCreated: false,
            bookings: [],
            users: [],
            selectedUser: null,
            userBookings: [],
            newUser: { username: '', email: '', password: '', isAdmin: false },
            passwordForm: { new_password: '', confirm_password: '' }, 
            showModal: false,
            showEditModal: false,
            updateUserErrors: null,  
            updatePasswordErrors: null,
            passwordChangedSuccess: false,
        };
    },
    mounted() {
        const token = localStorage.getItem('auth_token');
        if (token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            try {
                const decoded = jwtDecode(token);
                console.log(decoded)
                this.isAdmin = decoded.isAdmin || false;

                this.user.username = decoded.username || '';
                this.user.email = decoded.email || '';
            } catch (e) {
                console.error('Invalid token:', e);
            }
        }

        this.fetchUserData();
        if (this.isAdmin) {
            this.fetchAllUsers();
        }
    },
    computed: {
        isLoggedIn() {
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
        formatDate(dateString) {
            const date = new Date(dateString);
            return format(date, 'MMMM d, yyyy h:mm a'); // May 7, 2025 12:09 AM
        },
      fetchUserData() {
        axios.get('http://127.0.0.1:8000/api/my_bookings/')
          .then(response => {
            this.bookings = response.data;
          })
          .catch(error => {
            console.error('Error fetching bookings:', error);
          });
      },
      updateUser() {
        this.updateUserErrors = null; // сбрасываем ошибки
        const token = localStorage.getItem('auth_token');
        axios.put('http://127.0.0.1:8000/api/users/update/me/', {
          username: this.user.username,
          email: this.user.email
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(() => {
          this.showToastUpdated = true;
          setTimeout(() => this.showToastUpdated = false, 4000);
        })
        .catch(error => {
          if (error.response && error.response.data) {
            this.updateUserErrors = Object.values(error.response.data).flat();
          } else {
            this.updateUserErrors = ['Unexpected error occurred'];
          }
        });
      },
      updatePassword() {
        this.updatePasswordErrors = null;
        const token = localStorage.getItem('auth_token');
        axios.put('http://127.0.0.1:8000/api/users/change-password/', {
          new_password: this.passwordForm.new_password,
          confirm_password: this.passwordForm.confirm_password
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(() => {
          this.passwordChangedSuccess = true;
          this.passwordForm.new_password = '';
          this.passwordForm.confirm_password = '';

          this.passwordChangedSuccess = true;
          setTimeout(() => { this.passwordChangedSuccess = false }, 3000);
        })
        .catch(error => {
          if (error.response && error.response.data) {
            this.updatePasswordErrors = Object.values(error.response.data).flat();
          } else {
            this.updatePasswordErrors = ['Unexpected error occurred'];
          }
        });
      },
      deleteUser() {
        const token = localStorage.getItem("auth_token");

        axios.delete('http://127.0.0.1:8000/api/users/delete/me/', {
          headers: { Authorization: `Bearer ${token}` }
        })
          .then(() => {
            localStorage.removeItem("auth_token");
            localStorage.removeItem("user");
            window.location.href = '/login';
          })
          .catch(error => {
            console.error('Error deleting account:', error);
            alert('Failed to delete account.');
          });

        this.showModal = false;
      },
      fetchAllUsers() {
        axios.get('http://127.0.0.1:8000/api/admin/users')
          .then(response => {
            this.users = response.data;
          })
          .catch(error => {
            console.error('Error fetching users:', error);
          });
      },
      selectUserForEdit(user) {
        this.selectedUser = { ...user };
        this.showEditModal = true;
      },
      closeEditModal() {
        this.showEditModal = false;
        this.updateUserErrors = ''
      },
      updateSelectedUser() {
        axios.put(`http://127.0.0.1:8000/api/admin/users/${this.selectedUser.id}/`, this.selectedUser)
          .then(() => {
            this.showToastUpdated = true;
            setTimeout(() => this.showToastUpdated = false, 4000);
            this.fetchAllUsers();
            this.selectedUser = null;
            this.showEditModal = false;
            this.updateUserErrors = ''
          })
          .catch(error => {
            console.error('Error updating user:', error.response.data.username);
            this.updateUserErrors = Object.values(error.response.data).flat();
          });
      },
      openDeleteModal(user) {
        this.selectedUserToDelete = user;
        this.showDeleteModal = true;
      },
      closeDeleteModal() {
        this.showDeleteModal = false;
        this.selectedUserToDelete = null;
      },
      confirmDeleteUser() {
        axios.delete(`http://127.0.0.1:8000/api/admin/users/${this.selectedUserToDelete.id}/`)
          .then(() => {
            this.showToastDeleted = true;
            setTimeout(() => this.showToastDeleted = false, 4000);
            this.fetchAllUsers();
            this.closeDeleteModal();
          })
          .catch(error => {
            console.error('Error deleting user:', error);
          });
      },
      createUser() {
        axios.post('http://127.0.0.1:8000/api/admin/users/', this.newUser)
          .then(() => {
            this.showToastCreated = true;
            setTimeout(() => this.showToastCreated = false, 4000);
            this.fetchAllUsers();
            this.newUser = { username: '', email: '', password: '', isAdmin: false };
            this.updateUserErrors = '';
          })
          .catch(error => {
            console.error('Error creating user:', error);
            this.updateUserErrors = Object.values(error.response.data).flat();
          });
      },
    }
  };
  </script>

<template>
  <div class="container">
    <div class="content-card">
      <h1>👤 Profile</h1>

      <!-- Unauthenticated User -->
      <div v-if="!isLoggedIn" class="error-msg">
        ❌ You need to log in to view this page. <router-link to="/login">Login here</router-link>.
      </div>

      <!-- Authenticated User -->
      <div v-else-if="isLoggedIn">
        <!-- Non-Admin Section -->
        <div v-if="!isAdmin">
          <h2>✏️ Your Information</h2>

          <!-- Показываем ошибки -->
          <p v-if="updateUserErrors" class="error-message">
            <span v-for="(msg, index) in updateUserErrors" :key="index">{{ msg }}<br /></span>
          </p>

          <form @submit.prevent="updateUser" class="user-form">
            <label>
              Username:
              <input v-model="user.username" required placeholder="Enter username" />
            </label>
            <label>
              Email:
              <input v-model="user.email" type="email" required placeholder="Enter email" />
            </label>
            <button type="submit" class="btn submit-btn">Update Profile</button>
          </form>

          <hr>

          <h2>🔑 Change Password</h2>

          <p v-if="updatePasswordErrors" class="error-message">
            <span v-for="(msg, index) in updatePasswordErrors" :key="index">{{ msg }}<br /></span>
          </p>

          <form @submit.prevent="updatePassword" class="password-form">
            <label>
              New Password:
              <input v-model="passwordForm.new_password" type="password" required placeholder="Enter new password" />
            </label>
            <label>
              Confirm Password:
              <input v-model="passwordForm.confirm_password" type="password" required placeholder="Confirm new password" />
            </label>
            <button type="submit" class="btn submit-btn">Change Password</button>
          </form>

          <!-- Delete button -->
          <button @click="showModal = true" class="btn btn-danger">🗑️ Delete Account</button>

          <!-- Success Popup -->
          <div v-if="passwordChangedSuccess" class="popup-overlay">
          <div class="popup-content">
              <h3>✅ Password Changed Successfully!</h3>
              <button @click="passwordChangedSuccess = false">Close</button>
            </div>
          </div>

          <!-- Modal -->
          <div v-if="showModal" class="modal-overlay">
            <div class="modal-box">
              <h2 class="modal-title">⚠️ Confirm Deletion</h2>
              <p class="modal-message">
                Are you sure you want to delete your account? <br />
                <strong>This action cannot be undone.</strong>
              </p>
              <div class="modal-buttons">
                <button @click="deleteUser" class="btn-confirm">Yes, Delete</button>
                <button @click="showModal = false" class="btn-cancel">Cancel</button>
              </div>
            </div>
          </div>

          <h2>🛫 Your Bookings</h2>
          <div v-if="bookings.length" class="bookings-list">
            <table>
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
                    <router-link :to="{ name: 'FlightDetails', params: { id: booking.flight.id } }" class="btn btn-info">View Flight</router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else>No bookings found.</p>
        </div>

        <!-- Admin Section -->
        <div v-else>
          <h2>👥 Manage Users</h2>
          <div class="users-list">
            <table>
              <thead>
                <tr>
                  <th>Username</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.username }}</td>
                  <td>{{ user.email }}</td>
                  <td>{{ user.is_staff ? "Admin" : "User" }}</td>
                  <td v-if="!user.is_staff">
                    <!-- Edit Icon -->
                    <button @click="selectUserForEdit(user)" class="icon-btn">
                      <font-awesome-icon icon="pen" />
                    </button>
                    <!-- Delete Icon -->
                    <!-- <button @click="deleteSelectedUser(user.id)" class="icon-btn danger">
                      <font-awesome-icon icon="trash" />
                    </button> -->
                    <button @click="openDeleteModal(user)" class="icon-btn danger">
                      <font-awesome-icon icon="trash" />
                    </button>
                    <!-- View Bookings Icon (router-link) -->
                    <router-link
                      :to="{ name: 'AdminUserBookingsPage', params: { userId: user.id }, query: { username: user.username } }"
                      class="icon-btn info"
                    >
                      <font-awesome-icon icon="book" />
                    </router-link>
                  </td>
                  <td v-else></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Edit User Modal -->
          <div v-if="showEditModal" class="modal-overlay">
            <div class="modal">
              <p v-if="updateUserErrors" class="error-message">
                <span v-for="(msg, index) in updateUserErrors" :key="index">{{ msg }}<br /></span>
              </p>
              <h3>✏️ Edit User: {{ selectedUser.username }}</h3>
              <form @submit.prevent="updateSelectedUser" class="user-form">
                <label>
                  Username:
                  <input v-model="selectedUser.username" required placeholder="Enter username" />
                </label>
                <label>
                  Email:
                  <input v-model="selectedUser.email" type="email" required placeholder="Enter email" />
                </label>
                <label>
                  Password:
                  <input v-model="selectedUser.password" type="password" placeholder="Enter new password" />
                </label>
                <div class="modal-buttons">
                  <button type="submit" class="btn submit-btn">Update User</button>
                  <button @click="closeEditModal" type="button" id="cancel-btn">Cancel</button>
                </div>
              </form>
            </div>
          </div>

          <!-- Delete Confirmation Modal -->
          <div v-if="showDeleteModal" class="delete-modal-overlay">
            <div class="delete-modal-box">
              <h2>🗑️ Confirm Delete</h2>
              <p>Are you sure you want to delete user <strong>{{ selectedUserToDelete.username }}</strong>?</p>
              <div class="delete-modal-actions">
                <button @click="confirmDeleteUser" class="delete-modal-confirm-btn">
                  <font-awesome-icon icon="trash" /> Yes, Delete
                </button>
                <button @click="closeDeleteModal" id="delete-modal-cancel-btn">
                  <font-awesome-icon icon="times" /> Cancel
                </button>
              </div>
            </div>
          </div>

          <h3>➕ Create New User</h3>
          <p v-if="updateUserErrors" class="error-message">
            <span v-for="(msg, index) in updateUserErrors" :key="index">{{ msg }}<br /></span>
          </p>
          <form @submit.prevent="createUser" class="user-form">
            <label>
              Username:
              <input v-model="newUser.username" required placeholder="Enter username" />
            </label>
            <label>
              Email:
              <input v-model="newUser.email" type="email" required placeholder="Enter email" />
            </label>
            <label>
              Password:
              <input v-model="newUser.password" type="password" autocomplete="new-password" required placeholder="Enter password" />
            </label>
            <button type="submit" class="btn submit-btn">Create User</button>
          </form>
        </div>
        <div v-if="showToastUpdated" class="toast">
          ✅ User updated successfully!
        </div>
        <div v-if="showToastDeleted" class="toast">
          ✅ User deleted successfully!
        </div>
        <div v-if="showToastCreated" class="toast">
          ✅ User created successfully!
        </div>
      </div>
    </div>
  </div>
  </template>

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

.toast {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: #4caf50;
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  opacity: 0;
  animation: fadeInOut 4s forwards;
  font-size: 1rem;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(20px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(20px); }
}

#cancel-btn {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  background: #f44336; /* Red color */
  color: white;
  border: none;
  border-radius: 6px;
  margin-top: 15px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

#cancel-btn:hover {
  background: #d32f2f;
  transform: scale(1.02);
}
table {
  width: 100%;
  border-collapse: collapse;
}
th, td {
  padding: 0.8rem;
  border: 1px solid #ccc;
}

/* Icon button styling */
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  margin: 0 0.3rem;
}
.icon-btn.danger {
  color: red;
}
.icon-btn.info {
  color: #007bff;
}

/* Modal styling */
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
  min-width: 300px;
}
.modal-buttons {
  margin-top: 1rem;
  display: flex;
  justify-content: space-between;
}
.popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.popup-content {
  background: white;
  padding: 20px 30px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.popup-content h3 {
  margin-bottom: 15px;
}

.popup-content button {
  background: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.popup-content button:hover {
  background: #45a049;
}

.container {
  max-width: 800px;
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
  margin-bottom: 24px;
}

h2 {
  font-size: 22px;
  color: var(--primary);
  margin: 20px 0 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--gray);
}

h3 {
  font-size: 20px;
  color: var(--primary);
  margin: 15px 0 10px;
}

.user-form, .password-form {
  background-color: var(--gray-light);
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--primary);
  position: relative;
}

.user-form label, .password-form label {
  display: block;
  margin-bottom: 15px;
  font-weight: 600;
  color: var(--dark);
}

.user-form input, .password-form input {
  width: 100%;
  padding: 10px;
  border: 1px solid var(--gray);
  border-radius: 6px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.user-form input:focus, .password-form input:focus {
  border-color: var(--primary);
  outline: none;
}

.user-form::before {
  content: '👤';
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 20px;
}

.user-form label {
  padding-left: 40px;
}

.password-form::before {
  content: '🔒';
  position: absolute;
  top: 10px;
  left: 10px;
  font-size: 20px;
}

.password-form label {
  padding-left: 40px;
}

.bookings-list, .users-list {
  margin-top: 20px;
  background-color: var(--gray-light);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--primary);
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  padding: 12px 15px;
  text-align: center;
  border-bottom: 1px solid var(--gray);
  vertical-align: middle;
}

th {
  background-color: var(--primary);
  color: white;
  font-weight: 600;
}

tr:hover {
  background-color: #e6f0ff;
}

.btn {
  display: inline-block;
  padding: 8px 15px;
  border-radius: 6px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn:hover {
  transform: scale(1.02);
}

.btn-primary {
  background-color: var(--primary);
  color: white;
}

.btn-primary:hover {
  background-color: var(--primary-dark);
}

.btn-danger {
  background-color: var(--danger);
  color: white;
  margin: 15px 0;
}

.btn-danger:hover {
  background-color: #c82333;
}

.btn-info {
  background-color: #17a2b8;
  color: white;
}

.btn-info:hover {
  background-color: #138496;
}

.submit-btn {
  width: 100%;
  padding: 12px 20px;
  font-size: 16px;
  background-color: var(--primary);
  color: white;
  border-radius: 6px;
  margin-top: 15px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.submit-btn:hover {
  background-color: var(--primary-dark);
  transform: scale(1.02);
}

.error-message {
  color: #721c24;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 15px;
  font-size: 14px;
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

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(30, 30, 30, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-box {
  background: #fff;
  padding: 40px;
  border-radius: 16px;
  border: 1px solid var(--primary);
  width: 90%;
  max-width: 420px;
  text-align: center;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.modal-title {
  font-size: 1.8rem;
  margin-bottom: 15px;
  color: var(--primary);
}

.modal-message {
  font-size: 1rem;
  color: #555;
  margin-bottom: 30px;
}

.modal-buttons {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}

.btn-confirm {
  flex: 1;
  background: #e74c3c;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}

.btn-confirm:hover {
  background: #c0392b;
  transform: scale(1.02);
}

.btn-cancel {
  flex: 1;
  background: #95a5a6;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease, transform 0.2s ease;
}

.btn-cancel:hover {
  background: #7f8c8d;
  transform: scale(1.02);
}
</style>