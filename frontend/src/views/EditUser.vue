<template>
  <v-container>
    <v-row class="d-flex my-2 justify-center">
      <v-col cols="12" sm="12">
        <div class="text-h4 text-center font-weight-bold text-deep-purple-darken-4">{{ $t('EditUser') }}</div>
      </v-col>
    </v-row>
    <v-form v-model="isFormValid" @input="validationStatus" class="border-dashed pa-4">
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field v-model="user.full_name" label="Name" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
          <v-text-field v-model="user.email" label="Email" required></v-text-field>
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
      <v-btn :disabled="!isFormValid" @click="cancel" color="blue-darken-3"><v-icon
          class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t('Return') }}</v-btn>
      <v-btn v-if="isAdmin" :disabled="!isFormValid" @click="deleteUser" color="red"><v-icon
          class="mr-2">mdi-trash-can</v-icon>{{ $t('Delete')
        }}</v-btn>
      <v-btn :disabled="!isFormValid" @click="updateUser" color="indigo-darken-3"><v-icon
          class="mr-2">mdi-content-save</v-icon>{{ $t('Save') }}</v-btn>
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

onMounted(async () => {
  loaderStore.setLoading(true);
  if (useUsersStore().groups.length === 0) {
    useUsersStore().fetchRoles()
      .then((response) => {
        const groups = useUsersStore().groups;
        groups.forEach(group => {
          roles.value.push(group.name)
        });
      })
      .catch((error) => {
        console.error(error);
      });
  } else {
    const groups = useUsersStore().groups;
    groups.forEach(group => {
      roles.value.push(group.name)
    });
  }
  useUsersStore().fetchUserData(3)
  const data = await useUsersStore().fetchUserData(userId)

  user.value.email = data.email
  user.value.full_name = data.full_name
  user.value.health_number = data.health_number
  user.value.mobile_phone = data.mobile_phone
  user.value.taxpayer_number = data.taxpayer_number
  user.value.type_user = data.type_user
  user.value.role = data.groups[0]
  user.value.is_active = data.is_active
  user.value.is_staff = data.is_staff

  loaderStore.setLoading(false);

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
  if (!user.value.full_name || !user.value.email || !user.value.mobile_phone || !user.value.type_user || !user.value.role) {
    toast.error('All fields are required')
    return
  }
  loaderStore.setLoading(true);
  try {
    const response = await fetch(window.URL + '/api/users/' + userId + '/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer ' + localStorage.getItem('token')
      },
      body: JSON.stringify(user.value)
    })
    if (response.status !== 200) {

      const error = await response.json()
      toast.error(error.error)
      return
    }
    toast.success('User updated successfully')

  } catch (error) {
    console.error(error)
    toast.error('Error updating user')
  }
  loaderStore.setLoading(false);
}

const fetchUserData = () => {
  loaderStore.setLoading(true);
  user.value = useUsersStore().fetchUserData(userId)
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
