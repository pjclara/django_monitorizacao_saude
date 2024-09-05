<template>
    <v-container v-if="!smAndDown">
        <v-row>
            <v-col class="d-flex justify-start" cols="12" sm="4">
                <v-btn color="indigo-darken-3" @click="voltarListaUtilizadores"><v-icon
                        class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t("Return")
                    }}</v-btn>
            </v-col>
            <v-col class="text-h4 text-center font-weight-bold text-deep-purple-darken-4" cols="12" sm="4">{{
                $t('Roles')
                }}
            </v-col>
            <v-col class="d-flex justify-end" cols="12" sm="4">
                <v-btn color="indigo-darken-3" elevated @click="openDialogCreate"><v-icon color="white"
                        class="mr-2">mdi-plus</v-icon>{{ $t('CreateRole') }}</v-btn>
            </v-col>
        </v-row>

        <v-row justify="center" no-gutters style="margin-top: 20px;">
            <v-col cols="9">
                <v-data-table :headers="headersRoles" :items="roles" :search="search" :items-per-page="5"
                    class="elevation-1">
                    <template v-slot:top>
                        <v-toolbar flat style="background-color: #425C5A; color: white;">
                            <v-col cols="9">
                                <v-toolbar-title>{{ $t('RolesListing') }}</v-toolbar-title>
                            </v-col>
                            <v-col cols="3" class="d-flex justify-center align-center">
                                <div class="search-container">
                                    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" height="24"
                                        viewBox="0 96 960 960" width="24" fill="#888">
                                        <path
                                            d="M796 936 536 676q-28 24-62 36.5T400 725q-95 0-161.5-66.5T172 496q0-95 66.5-161.5T400 268q95 0 161.5 66.5T628 496q0 36-12.5 70T580 628l260 260-44 48Zm-396-292q66 0 112-46t46-112q0-66-46-112t-112-46q-66 0-112 46t-46 112q0 66 46 112t112 46Z" />
                                    </svg>
                                    <input type="search" class="search-input" :placeholder="$t('Search for roles')"
                                        v-model="search">
                                </div>
                            </v-col>
                        </v-toolbar>
                    </template>
                    <template v-slot:item.actions="{ item }">
                        <v-icon small @click="editRole(item)">mdi-pencil</v-icon>
                    </template>
                </v-data-table>
            </v-col>
        </v-row>
    </v-container>
    <v-container v-else>
        <div>
            <v-col class="d-flex justify-center" cols="12" sm="4">
                <v-btn color="indigo-darken-3" @click="voltarListaUtilizadores"><v-icon
                        class="mr-2">mdi-keyboard-backspace</v-icon>{{ $t("Return")
                    }}</v-btn>
            </v-col>
            <v-col class="text-h4 text-center font-weight-bold text-deep-purple-darken-4" cols="12" sm="4">{{
                $t('Roles')
                }}
            </v-col>
            <v-col class="d-flex justify-center" cols="12" sm="4">
                <v-btn color="indigo-darken-3" elevated @click="openDialogCreate"><v-icon color="white"
                        class="mr-2">mdi-plus</v-icon>{{ $t('CreateRole') }}</v-btn>
            </v-col>
        </div>
        <MobileTable class="justify-center" :data="roles" :keys="['id', 'name', 'Actions']" @roleEdit="editRole(item)"/>
    </v-container>

    <v-dialog v-model="dialogCreate" max-width="500px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ $t('CreateRole') }}</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="role.name" label="Name" required></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDialogCreate">{{ $t('Close') }}</v-btn>
                <v-btn color="blue darken-1" text @click="createRole">{{ $t('Save') }}</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog v-model="dialogEdit" max-width="500px">
        <v-card>
            <v-card-title>
                <span class="headline">{{ $t('EditRole') }}</span>
            </v-card-title>
            <v-card-text>
                <v-container>
                    <v-row>
                        <v-col cols="12">
                            <v-text-field v-model="role.name" label="Name" required></v-text-field>
                        </v-col>
                    </v-row>
                </v-container>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDialogEdit">{{ $t('Close') }}</v-btn>
                <v-btn color="blue darken-1" text @click="updateRole">{{ $t('Save') }}</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>


</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import { useRouter } from 'vue-router';
import { toast } from 'vue3-toastify';
const loaderStore = useLoaderStore();
import { useDisplay } from 'vuetify'
const { smAndDown } = useDisplay()
import MobileTable from '@/components/table/MobileTable.vue';

const router = useRouter()

const headersRoles = ref([
    { title: 'ID', value: 'id' },
    { title: 'Name', value: 'name' },
    { title: 'Actions', value: 'actions', sortable: false },
])

const search = ref('')

const roles = ref([])

const dialogCreate = ref(false)

const dialogEdit = ref(false)

const openDialogCreate = () => {
    dialogCreate.value = true
    role.value = {
        name: ''
    }
}

const closeDialogCreate = () => {
    dialogCreate.value = false
}

const closeDialogEdit = () => {
    dialogEdit.value = false
}

const role = ref({
    name: ''
})

const editRole = (item) => {
    role.value = { ...item }
    dialogEdit.value = true
}

const createRole = async () => {
    loaderStore.setLoading(true);
    // name not empty
    if (!role.value.name) {
        loaderStore.setLoading(false);
        toast.error('Name is required')
        return
    }
    // check if role already exists
    for (let i = 0; i < roles.value.length; i++) {
        if (roles.value[i].name === role.value.name) {
            loaderStore.setLoading(false);
            toast.error('Role already exists')
            return
        }
    }

    try {
        const response = await fetch(window.URL + '/api/create_group/',
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ` + localStorage.getItem('token')
                },
                body: JSON.stringify(role.value)
            }
        );
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        console.log('data: ', data)
        toast.success('Role created')
        getRoles()
        closeDialogCreate()
    } catch (error) {
        console.error(error)
    }
    loaderStore.setLoading(false);
}

const updateRole = async () => {
    loaderStore.setLoading(true);
    if (!role.value.name) {
        loaderStore.setLoading(false);
        toast.error('Name is required')
        return
    }
    // check if role already exists
    for (let i = 0; i < roles.value.length; i++) {
        if (roles.value[i].name === role.value.name && roles.value[i].id !== role.value.id) {
            loaderStore.setLoading(false);
            toast.error('Role already exists')
            return
        }
    }
    try {
        const response = await fetch(window.URL + '/api/get_group/' + role.value.id + '/',
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ` + localStorage.getItem('token')
                },
                body: JSON.stringify(role.value)
            }
        );
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        console.log('data: ', data)
        toast.success('Role updated')
        getRoles()
        closeDialogEdit()
    } catch (error) {
        console.error(error)
    }
    loaderStore.setLoading(false);
}

const getRoles = async () => {
    loaderStore.setLoading(true);
    try {
        const response = await fetch(window.URL + '/api/get_groups/',
            {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ` + localStorage.getItem('token')
                }
            }
        );
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

const voltarListaUtilizadores = () => {
    router.push({ name: 'EmployeesListing' });
}

onMounted(() => {
    getRoles();
})

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