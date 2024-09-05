<template>
    <v-container>
        <v-col class="d-flex flex-column">
            <v-row>
                <v-col :class="['d-flex justify-start', {'justify-center': smAndDown}]" cols="12" sm="4">
                    <v-btn color="indigo-darken-3" @click="voltarPainel"><v-icon class="mr-2">mdi-home</v-icon>{{
                        $t('Dashboard') }}</v-btn>
                </v-col>
                <v-col class="text-h4 text-center font-weight-bold text-deep-purple-darken-4" cols="12" sm="4">{{
                    $t('UsersListing')
                }}
                </v-col>
                <v-col :class="['d-flex justify-end', {'justify-center': smAndDown}]" cols="12" sm="4">
                    <v-btn color="indigo-darken-3" elevated to="/create-user">
                        <v-icon color="white" class="mr-2">mdi-plus</v-icon> {{ $t('CreateUser') }}
                    </v-btn>
                </v-col>
            </v-row>
            <v-row no-gutters justify="center" class="mt-2">
                <v-data-table :headers="headers" :items="users" :items-per-page="5" :search="search" class="elevation-1"
                    v-if="!smAndDown">
                    <template v-slot:headers>
                        <tr>
                            <th v-for="header in headers" :key="header.title" class="text-center">{{ $t(header.title) }}
                            </th>
                        </tr>
                    </template>
                    <template v-slot:top>
                        <v-toolbar flat>
                            <v-col cols="12" class="d-flex justify-end align-center">
                                <div class="search-container">
                                    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" height="24"
                                        viewBox="0 96 960 960" width="24" fill="#888">
                                        <path
                                            d="M796 936 536 676q-28 24-62 36.5T400 725q-95 0-161.5-66.5T172 496q0-95 66.5-161.5T400 268q95 0 161.5 66.5T628 496q0 36-12.5 70T580 628l260 260-44 48Zm-396-292q66 0 112-46t46-112q0-66-46-112t-112-46q-66 0-112 46t-46 112q0 66 46 112t112 46Z" />
                                    </svg>
                                    <input type="search" class="search-input" :placeholder="$t('Search for users')"
                                        v-model="search">
                                </div>
                            </v-col>
                        </v-toolbar>
                    </template>
                    <template v-slot:item.taxpayer_number="{ item }">
                        <span v-if="!item.taxpayer_number || item.taxpayer_number == '0'">-----</span>
                        <span v-else>{{ item.taxpayer_number }}</span>
                    </template>
                    <template v-slot:item.health_number="{ item }">
                        <span v-if="!item.health_number || item.health_number == '0'">-----</span>
                        <span v-else>{{ item.health_number }}</span>
                    </template>
                    <template v-slot:item.is_active="{ item }">
                        <v-icon v-if="item.is_active" class="green">mdi-check-circle</v-icon>
                        <v-icon v-else class="red">mdi-close-circle</v-icon>
                    </template>
                    <template v-slot:item.actions="{ item }">
                        <v-icon @click="editItem(item)">mdi-pencil</v-icon>
                    </template>
                </v-data-table>

                <MobileTable v-else class="justify-center" :data="users" :keys="['id', 'name', 'email', 'active', 'actions']"
                    :isUser="true">
                </MobileTable>
            </v-row>

        </v-col>
    </v-container>
</template>

<script setup>
import MobileTable from '@/components/table/MobileTable.vue';

import { onMounted, ref } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import { useUsersStore } from '@/stores/users';
import { useRouter } from 'vue-router';
import { useDisplay } from 'vuetify'
const { smAndDown } = useDisplay()
const loaderStore = useLoaderStore();

const headers = ref([
    { title: 'Name', key: 'full_name' },
    { title: 'Email', key: 'email' },
    { title: 'Taxpayer number', key: 'taxpayer_number' },
    { title: 'Health number', key: 'health_number' },
    { title: 'Mobile phone', key: 'mobile_phone' },
    { title: 'Type user', key: 'type_user' },
    { title: 'Active', key: 'is_active' },
    { title: 'Actions', key: 'actions', sortable: false }
])


const users = ref([]);

const router = useRouter();

const voltarPainel = () => {
    router.push({ name: 'HomeAdmin' })
}

onMounted(async () => {
    loaderStore.setLoading(true);
    if (useUsersStore().users.length == 0) {
        users.value = await useUsersStore().fetchUsers();
    } else {
        users.value = useUsersStore().users;
    }
    users.value = users.value.map(user => {
        return {...user, name: user.full_name, active: user.is_active}
    })
    loaderStore.setLoading(false);
});

const search = ref(null)

const editItem = (item) => {
    router.push({ name: 'EditUser', params: { id: item.id } })
}
</script>

<style scoped>
.search-container {
    position: relative;
    display: inline-block;
}

.search-icon {
    position: absolute;
    top: 50%;
    left: 10px;
    transform: translateY(-50%);
    pointer-events: none;
}

.search-input {
    width: 100%;
    padding: 10px 10px 10px 40px;
    border-radius: 20px;
    border: 1px solid #ccc;
    outline: none;
    background-color: aliceblue;
}

.search-input:focus {
    border-color: #007BFF;
}
</style>