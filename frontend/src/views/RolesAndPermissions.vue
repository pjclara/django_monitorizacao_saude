<template>
    <v-container>
        <v-row>
            <v-col cols="6">
                <h2>{{ $t('RolesAndPermissions') }}</h2>
            </v-col>
            <v-col cols="6">
                <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line
                    hide-details></v-text-field>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-data-table :headers="headersRoles" :items="roles" :search="search" :items-per-page="5"
                    class="elevation-1">
                    <template v-slot:item.actions="{ item }">
                        <v-icon small @click="editRole(item.id)">mdi-pencil</v-icon>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import { useRouter } from 'vue-router';

const loaderStore = useLoaderStore();

const router = useRouter()

const headersRoles = ref([
    { text: 'ID', value: 'id' },
    { text: 'Name', value: 'name' },
    { text: 'Permissions', value: 'permissions.name' },
    { text: 'Actions', value: 'actions', sortable: false },
])

const search = ref('')

const roles = ref([])

const getRoles = async () => {
    loaderStore.setLoading(true);
    try {
        const response = await fetch(window.URL + '/api/get_groups/');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        roles.value = data
        console.log('roles.value: ', roles.value)
    } catch (error) {
        console.error(error)
    }
    loaderStore.setLoading(false);
}

const editRole = (id) => {
    router.push({ name: 'RolesAndPermissionsEdit', params: { id: id } })
}

const addRole = () => {
    router.push({ name: 'AddRole' })
}

onMounted(() => {
    getRoles();
})

</script>