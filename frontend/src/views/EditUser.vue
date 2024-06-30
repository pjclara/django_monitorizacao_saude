<template>
  <v-container>
    <div v-if="showSuccess" class="success-message">
      {{ $t('SuccessYourActionWasCompleted') }}
    </div>
    <div v-if="showErrors" class="error-message">
      {{ $t('ErrorYourActionWasNotCompleted') }}

    </div>
    <v-row class="d-flex my-2 justify-center">
      <v-col cols="12" sm="8">
        <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">{{ $t('EditUser') }}</div>
      </v-col>
      <v-col cols="12" sm="4" v-if="isAdmin"><v-btn @click="usersList">{{ $t('UsersListing') }}</v-btn></v-col>

    </v-row>
    <v-form v-model="isFormValid" @input="validationStatus">
      <v-row>
        <v-col cols="12" sm="4">
          <v-text-field v-model="user.full_name" label="Name" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field v-model="user.email" label="Email" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="4">
          <v-text-field v-model="user.password" label="Password" required></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="3" v-if="user.type_user != 'profissional'">
          <v-text-field v-model="user.health_number" label="Health number" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="3" v-if="user.type_user == 'profissional'">
          <v-text-field v-model="user.taxpayer_number" label="Taxpayer number" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="3">
          <v-text-field v-model="user.mobile_phone" label="Mobile phone" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="3" v-if="isAdmin">
          <v-select v-model="user.type_user" :items="typeUser" label="Type user" required></v-select>
        </v-col>

        <v-col cols="12" sm="3" v-if="isAdmin">
          <v-select v-model="user.role" :items="roles" label="Role" required></v-select>
        </v-col>
      </v-row>
    </v-form>
    <v-row class="d-flex my-2 justify-space-between">
      <v-btn :disabled="!isFormValid" @click="cancel" color="lightdark">{{ $t('Return') }}</v-btn>
      <v-btn v-if="isAdmin" :disabled="!isFormValid" @click="deleteUser" color="indigo-darken-3">{{ $t('Delete') }}</v-btn>
      <v-btn :disabled="!isFormValid" @click="updateUser" color="indigo-darken-3">{{ $t('Save') }}</v-btn>
    </v-row>
  </v-container>

</template>

<script setup>
import router from '@/router';
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router';
import { useLoaderStore } from '@/stores/loader'
import { useUsersStore } from '@/stores/users';
import { toast } from 'vue3-toastify';


const isAdmin = computed(() => {
  return useUsersStore().user?.groups.includes('admin') ? true : false
});

const loaderStore = useLoaderStore();

const showSuccess = ref(false)
const showErrors = ref(false)

const userId = useRoute().params.id

const roles = ref([])

const typeUser = ref(['profissional', 'paciente', 'admin'])

const user = ref({
  full_name: '',
  email: '',
  health_number: 0,
  password: '',
  mobile_phone: '',
  taxpayer_number: 0,
  type_user: '',
  role: '',
  is_active: true,
  is_staff: false
})

const form = ref(null)

onMounted(() => {
  fetchUserData(),
    fetchRolesFromApi()
})

const isFormValid = ref(false)

const validationStatus = ref(false)

const cancel = () => {
  // go to the previous page
  router.go(-1)
}

const password = ref('')

const updateUser = async () => {

  // all fields are required
  if (!user.value.full_name || !user.value.email || !user.value.password || !user.value.mobile_phone || !user.value.type_user || !user.value.role) {
    toast.error('All fields are required')
    return
  }
  loaderStore.setLoading(true);
  try {
    const response = await fetch(window.URL + '/api/users/' + userId + '/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(user.value)
    })
    if (response.status !== 200) {
      toast.error('Error updating user')
      return
    }
    toast.success('User updated successfully')

  } catch (error) {
    console.error(error)
    toast.error('Error updating user')
  }
  loaderStore.setLoading(false);
}

const fetchUserData = async () => {
  loaderStore.setLoading(true);
  try {
    const response = await fetch(window.URL + '/api/users/' + userId + '/');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const userData = await response.json();
    user.value.email = userData.email;
    user.value.health_number = userData.health_number ? userData.health_number : 0;
    user.value.mobile_phone = userData.mobile_phone;
    user.value.taxpayer_number = userData.taxpayer_number? userData.taxpayer_number : 0;
    user.value.type_user = userData.type_user;
    user.value.full_name = userData.full_name;
    user.value.is_active = userData.is_active;
    user.value.is_staff = userData.is_staff;
    user.value.role = userData.groups[0];

  } catch (error) {
    console.error(error);
    toast.error('Error fetching user data');
  }
  loaderStore.setLoading(false);
};

const fetchRolesFromApi = async () => {
  try {
    loaderStore.setLoading(true);
    const response = await fetch(window.URL + '/api/get_groups/');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();
    for (let i = 0; i < data.length; i++) {
      roles.value.push(data[i].name)
    }
  } catch (error) {
    console.error(error);
  }
  loaderStore.setLoading(false);
};

const deleteUser = async () => {
  try {
    const response = await fetch(window.URL + '/api/users/', {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: user.value.email }),
    });

    if (response.ok) {
      const data = await response.json();
      alert(data.message || 'User deleted successfully');
      cancel();
    } else {
      const errorData = await response.json();
      alert(errorData.error || 'Error deleting user');
    }
  } catch (error) {
    alert('Network error');
  }
};

const usersList = () => {
  router.push({ name: 'EmployeesListing' })
}




</script>
