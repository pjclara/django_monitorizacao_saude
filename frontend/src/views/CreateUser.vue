<template>
  <v-container>
    <v-row class="d-flex my-2 justify-center">
      <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">{{ $t('CreateUser') }}</div>
    </v-row>
    <v-form v-model="isFormValid" @input="validationStatus">
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field v-model="user.full_name" label="Name" :rules="full_name_rules" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
          <v-text-field v-model="user.email" label="Email" :rules="email_rules" required></v-text-field>
        </v-col>
        <!-- <v-col cols="12" sm="4">
          <v-text-field v-model="user.password" label="Password" :rules="password_rules" required></v-text-field>
        </v-col> -->
      </v-row>
      <v-row>
        <v-col cols="12" sm="3" v-if="user.type_user == 'paciente'">
          <v-text-field v-model="user.health_number" label="Health number" :rules="health_number_rules"
            required></v-text-field>
        </v-col>
        <v-col cols="12" sm="3" v-if="user.type_user != 'paciente'">
          <v-text-field v-model="user.taxpayer_number" label="Taxpayer number" :rules="taxpayer_number"
            required></v-text-field>
        </v-col>
        <v-col cols="12" sm="3">
          <v-text-field v-model="user.mobile_phone" label="Mobile phone" :rules="mobile_phone_rules"
            required></v-text-field>
        </v-col>
        <v-col cols="12" sm="3" v-if="isAdmin">
          <v-select v-model="user.type_user" :items="typeUser" label="Type user" :rules="type_user_rules"
            required></v-select>
        </v-col>

        <v-col cols="12" sm="3" v-if="isAdmin">
          <v-select v-model="user.role" :items="roles" label="Role" :rules="role_rules" required></v-select>
        </v-col>
        <v-col v-if="user.role == 'add new role'">
          <v-text-field v-model="new_role" label="New role"></v-text-field>
        </v-col>
      </v-row>
    </v-form>
    <v-row class="d-flex my-2 justify-space-between">
      <v-btn @click="cancel" color="blue-darken-3"><v-icon class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t('Return')
        }}</v-btn>
      <v-btn :disabled="!isFormValid" @click="criarUser" color="indigo-darken-3"><v-icon
          class="mr-2">mdi-content-save</v-icon>{{ $t('Save') }}</v-btn>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import { useUsersStore } from '@/stores/users'
import { toast } from 'vue3-toastify';
import { useRouter } from 'vue-router';
const loaderStore = useLoaderStore();

const user = ref({
  full_name: '',
  email: '',
  password: 'test',
  health_number: 0,
  taxpayer_number: 0,
  mobile_phone: '',
  type_user: '',
  role: '',
  is_active: true,
  is_staff: false
})

const roles = ref([])

const new_role = ref('')

const router = useRouter()

const isFormValid = ref(false)

const validationStatus = ref(false)

const isAdmin = computed(() => {
  return useUsersStore().user?.groups.includes('admin') ? true : false
});


const typeUser = ref(['profissional', 'paciente', 'admin'])

onMounted(() => {
  getRoles()
})

const getRoles = async () => {
  loaderStore.setLoading(true);
  useUsersStore().fetchRoles()
    .then((response) => {
      response.forEach(role => {
        roles.value.push(role.name)
      })
    })
    .catch((error) => {
      console.error(error);
    });
  loaderStore.setLoading(false);
}

const criarUser = async () => {
  console.log(user.value)
  //return
  try {
    if (user.value.role == 'add new role') {
      user.value.role = new_role.value
    }
    const response = await fetch(window.URL + '/api/users/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(user.value)
    })
    if (response.status !== 201) {
      const error = await response.json()
      toast.error(error.error)
      return
    }
    toast.success('User created successfully')
    router.push({ name: 'EmployeesListing' })
  } catch (error) {
    console.error(error)
    toast.error('Error creating user')
  }
}

const cancel = () => {
  // go to the previous page
  router.go(-1)
}

// validation rules

const full_name_rules = [
  v => !!v || 'Name is required',
  v => (v && v.length <= 50) || 'Name must be less than 50 characters',
]

const email_rules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'E-mail must be valid',
]

// const password_rules = [
//   v => !!v || 'Password is required',
//   v => (v && v.length >= 8) || 'Password must be at least 8 characters',
// ]

const health_number_rules = [
  v => !!v || 'Health number is required',
  v => (v && v.length <= 9) || 'Health number must be less than 9 characters',
]

const taxpayer_number = [
  v => !!v || 'Taxpayer number is required',
  v => (v && v.length <= 9) || 'Taxpayer number must be less than 9 characters',
]

const mobile_phone_rules = [
  v => !!v || 'Mobile phone is required',
  v => (v && v.length <= 9) || 'Mobile phone must be less than 9 characters',
]

const type_user_rules = [
  v => !!v || 'Type user is required',
]

const role_rules = [
  v => !!v || 'Role is required',
]


</script>
