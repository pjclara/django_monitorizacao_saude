<template>
    <v-container>
        <v-col class="d-flex flex-column">
            <v-text-field
                v-model="search"
                :label="$t('Search')"
                class="mb-4"
                outlined
            ></v-text-field>
            <v-data-table :headers="headers" :items="users" :items-per-page="5" :search="search" class="elevation-1" v-if="!smAndDown">
                <template v-slot:headers >
                    <tr>
                        <th v-for="header in headers" :key="header.title" class="text-left">{{ $t(header.title) }}</th>
                    </tr>

                </template>
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-toolbar-title>{{ $t('UsersListing') }}</v-toolbar-title>
                        <v-divider class="mx-4" inset vertical></v-divider>
                        <v-btn class="mb-2" color="primary" dark to="/create-user">
                            {{ $t('CreateUser') }}
                        </v-btn>
                    </v-toolbar>
                </template>
                <template v-slot:item.is_active="{ item }">
                    <v-icon v-if="item.is_active" class="green">mdi-check-circle</v-icon>
                    <v-icon v-else class="red">mdi-close-circle</v-icon>
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon @click="editItem(item)">mdi-pencil</v-icon>
                </template>
            </v-data-table>
            <MobileTable v-else :data="users" :keys="['id', 'username', 'email', 'is_active', 'actions']" :isUser="true"></MobileTable>
        </v-col>
    </v-container>
</template>

<script setup>
import MobileTable from '@/components/table/MobileTable.vue';

import { onMounted, ref } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import router from '@/router';
import { useDisplay } from 'vuetify'
const { smAndDown } = useDisplay()
const loaderStore = useLoaderStore();

const headers = ref([
    { title: 'Name', key: 'full_name' },
    { title: 'Email', key: 'email' },
    { title: 'Taxpayer number', key: 'taxpayer_number'},
    { title: 'Health number', key: 'health_number'},
    { title: 'Mobile phone', key: 'mobile_phone' },
    { title: 'Type user', key: 'type_user' },
    { title: 'Active', key: 'is_active' },
    { title: 'Actions', key: 'actions', sortable: false }
])

const users = ref([])

const search = ref(null)

onMounted(() => {
    getUsers()
})

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

const editItem = (item) => {
    router.push({ name: 'EditUser', params: { id: item.id } })
}
</script>