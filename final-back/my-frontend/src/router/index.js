import { createRouter, createWebHistory } from 'vue-router'
import FlightList from '../components/FlightList.vue'
import FlightDetails from '../components/FlightDetails.vue'
import LoginPage from '../components/LoginPage.vue'
import RegisterPage from '../components/RegisterPage.vue'
import AirportDetails from '../components/AirportDetails.vue'
import FlightBookingPage from '../components/FlightBookingPage.vue'
import ProfilePage from '../components/ProfilePage.vue'
import BookingConfirmation from '../components/BookingConfirmation.vue'
import BookingDetails from '../components/BookingDetails.vue'
import ManageBooking from '../components/ManageBooking.vue'
import { isAuthenticated } from '../utils/auth.js';
import AdminUserBookingsPage from '../components/AdminUserBookingsPage.vue'
import NotFound from '../components/NotFound.vue'

const routes = [
  { path: '/', name: 'Home', component: FlightList },
  { path: '/flights/:id', name: 'FlightDetails', component: FlightDetails },
  { path: '/login', name: 'LoginPage', component: LoginPage},
  { path: '/register', name: 'RegisterPage', component: RegisterPage},
  { path: '/airport/:id', name: 'AirportDetails', component: AirportDetails},
  { path: '/booking/:id', name: 'FlightBookingPage', component: FlightBookingPage},
  { path: '/profile', name: 'ProfilePage', component: ProfilePage},
  { path: '/booking-confirmation/:id', name:"BookingConfirmation", component: BookingConfirmation},
  { path: '/manage-booking', name:"ManageBooking", component: ManageBooking},
  { path: '/booking-details/:code', name:"BookingDetails", component: BookingDetails},
  { path: '/admin/bookings/:userId', name: 'AdminUserBookingsPage', component: AdminUserBookingsPage, 
    props: route => ({
    userId: route.params.userId,
  })},
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound},
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const publicPages = ['/login', '/register', '/login/', '/register/'];
  const authRequired = publicPages.includes(to.path);

  if (authRequired && isAuthenticated()) {
    return next('/');
  }

  next();
});

export default router
