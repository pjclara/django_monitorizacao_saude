import { createRouter, createWebHistory } from 'vue-router'
import { useUsersStore } from '@/stores/users'
import LoginPage from '@/views/LoginPage.vue'
import PasswordRecovery from '@/views/PasswordRecovery.vue'
import CreatePatient from '@/views/CreatePatient.vue'
import PatientProfile from '@/views/PatientProfile.vue'
import PatientsListing from '@/views/PatientsListing.vue'
import EmployeesListing from '@/views/EmployeesListing.vue'
import PatientEdit from '@/views/PatientEdit.vue'
import CreateUser from '@/views/CreateUser.vue'
import EditUser from '@/views/EditUser.vue'
import LandingPageAdmin from '@/views/LandingPageAdmin.vue'
import LandingPageUser from '@/views/LandingPageUser.vue'
import RolesAndPermissions from '@/views/RolesAndPermissions.vue'
import RolesAndPermissionsEdit from '@/views/RolesAndPermissionsEdit.vue'
import NotFound from '@/views/NotFound.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomeUser',
      component: LandingPageUser
    },
    {
      path: '/admin',
      name: 'HomeAdmin',
      component: LandingPageAdmin
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage
    },
    {
      path: '/create-user',
      name: 'CreateUser',
      component: CreateUser
    },
    {
      path: '/user/:id/edit',
      name: 'EditUser',
      component: EditUser
    },
    {
      path: '/create-patient',
      name: 'CreatePatient',
      component: CreatePatient
    },
    {
      path: '/patients/:patientSns',
      name: 'PatientProfile',
      component: PatientProfile
    },
    {
      path: '/patients/:patientSns/edit',
      name: 'PatientEdit',
      component: PatientEdit
    },
    {
      path: '/usersList',
      name: 'EmployeesListing',
      component: EmployeesListing
    },
    {
      path: '/patients',
      name: 'PatientsListing',
      component: PatientsListing
    },
    {
      path: '/roles-and-permissions',
      name: 'RolesAndPermissions',
      component: RolesAndPermissions
    },
    {
      path: '/roles-and-permissions/:id/edit',
      name: 'RolesAndPermissionsEdit',
      component: RolesAndPermissionsEdit
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/'
    },
    {
      path: '/password-recovery',
      name: 'PasswordRecovery',
      component: PasswordRecovery
    },
    {
      path: '/notFound',
      name: 'NotFound',
      component: () => NotFound
    }
  ]
})

router.beforeEach((to, from, next) => {
  const usersStore = useUsersStore()
  const isLogged = usersStore.isLogged
  if (!isLogged && to.path !== '/login' && to.path !== '/password-recovery') {
    next('/login')
  } else if (isLogged && to.path === '/login') {
    next('/')
  } else {
    next()
  }
})

export default router
