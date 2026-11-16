import { createRouter, createWebHistory } from 'vue-router'
import Login from '../Pages/Login.vue'
import Dashboard from '../Pages/Dashboard.vue'
import Index from '../Pages/Index.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'index',
      component: Index
      // No meta.layout -> renders without AppLayout in App.vue
    },
    {
      path: '/login',
      name: 'login',
      component: Login
      // No meta.layout -> renders without AppLayout in App.vue
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: Dashboard,
      meta: { 
        layout: 'AppLayout', 
        title: 'Dashboard' 
      }
    },
    {
      path: '/create-request',
      name: 'create-request',
      component: () => import('../Pages/CreateRequest.vue'),
      meta: { 
        layout: 'AppLayout', 
        title: 'New Requests' 
      }
    },
    {
      path: '/my-requests',
      name: 'my-requests',
      component: () => import('../Pages/MyRequests.vue'),
      meta: { 
        layout: 'AppLayout', 
        title: 'My Requests' 
      }
    },
    {
      path: '/assignments',
      name: 'assignments',
      component: () => import('../Pages/Assignment.vue'),
      meta: { 
        layout: 'AppLayout', 
        title: 'My Requests' 
      }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../Pages/Admin.vue'),
      meta: { 
        layout: 'AppLayout', 
        title: 'Admin' 
      }
    },
    {
      path: '/admin/create-user',
      name: 'create-user',
      component: () => import('../Pages/UserFormPage.vue'),
      meta: { 
        layout: 'AppLayout', 
        title: 'Create User' 
      }
    },
    {
      path: '/admin/:id/edit-user',
      name: 'edit-user',
      component: () => import('../Pages/UserFormPage.vue'),
      props: true,
      meta: { 
        layout: 'AppLayout', 
        title: 'Update User' 
      }
    },
    {
      path: '/admin/create-vehicle',
      name: 'create-vehicle',
      component: () => import('../Pages/VehicleFormPage.vue'),
      meta: { 
        layout: 'AppLayout', 
        title: 'Create Vehicle' 
      }
    },
    {
      path: '/admin/:id/edit-vehicle',
      name: 'edit-vehicle',
      component: () => import('../Pages/VehicleFormPage.vue'),
      props: true,
      meta: { 
        layout: 'AppLayout', 
        title: 'Update Vehicle' 
      }
    }
  ]
})

export default router
