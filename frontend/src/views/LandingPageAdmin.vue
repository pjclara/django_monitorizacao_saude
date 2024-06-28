<template>
  <v-container style="margin-top: 50px;" fluid>
    <v-row>
      <v-col cols="12" sm="12" class="mt-n4 text-center">
        <div>{{ $t('dashboard') }}</div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4">
        <v-card color="#B49239" theme="dark" class="rounded-xl" height="150">
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
        <v-card color="#C78987" theme="dark" class="rounded-xl" height="150">
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

const user = useUsersStore().user

const loaderStore = useLoaderStore();

onMounted(() => {
  fetchDataFromApi();
  getUsers();
});

const roles = ref([]);

const users = ref([]);

const fetchDataFromApi = async () => {
  try {
    loaderStore.setLoading(true);
    const response = await fetch(window.URL + '/api/get_groups/');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();

    roles.value = data;

  } catch (error) {
    console.error(error);
  }
  loaderStore.setLoading(false);
};

const getUsers = async () => {
    loaderStore.setLoading(true);
    const response = await fetch(window.URL + '/api/users/')
    if (response.status !== 200) {
        console.log("Error: ", response)
        return
    } else {
        const data = await response.json()
        users.value = data
        console.log("Success: ", data)
    }
    loaderStore.setLoading(false);
}



</script>