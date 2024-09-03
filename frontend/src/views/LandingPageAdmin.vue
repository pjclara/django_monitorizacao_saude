<template>
  <v-container style="margin-top: 50px;" fluid>
    <v-row>
      <v-col cols="12" sm="12" class="mt-n4 text-center">
        <div class="text-h4">{{ $t('dashboard') }}</div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4">
        <v-card color="#B49239" theme="dark" class="rounded-xl" height="150" @click="goToUsers">
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-h5 mt-10">
                {{ $t('Users') }}
              </v-card-title>

              <v-card-subtitle>{{ users.length }}</v-card-subtitle>
            </div>
            <v-img src="patient.png" class="mr-4 mt-5" width="100" height="100" absolute></v-img>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card color="#C78987" theme="dark" class="rounded-xl" height="150" @click="goToRoles">
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-h5 mt-10">
                {{ $t('RolesAndPermissions') }}
              </v-card-title>

              <v-card-subtitle>
                {{ roles?.length }}
              </v-card-subtitle>
            </div>
          </div>
        </v-card>
      </v-col>

    </v-row>

  </v-container>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useLoaderStore } from '@/stores/loader'
import { useUsersStore } from '@/stores/users';
import { useRouter } from 'vue-router';

const loaderStore = useLoaderStore();

onMounted(() => {
  loaderStore.setLoading(true);
  getUsers();
  getRoles();
  loaderStore.setLoading(false);
});
const router = useRouter();
const roles = ref([]);

const users = ref([]);

const goToUsers = () => {
  router.push({ name: 'EmployeesListing' });
};

const getUsers = async () => {  
  useUsersStore().fetchUsers()
    .then((response) => {
      users.value = response;
    })
    .catch((error) => {
      console.error(error);
    });
}

const getRoles = async () => {
  useUsersStore().fetchRoles()
    .then((response) => {
      roles.value = response;
    })
    .catch((error) => {
      console.error(error);
    });
}

const goToRoles = () => {
  router.push({ name: 'RolesAndPermissions' });
};



</script>