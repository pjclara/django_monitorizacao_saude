<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-card>
                    <v-card-title>
                        <h3>{{ $t('EditRole') }}</h3>
                    </v-card-title>
                    <v-card-text>
                        <v-form>
                            <v-row>
                                <v-col cols="12">
                                    <v-text-field v-model="role.name" label="Name" required></v-text-field>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <v-select v-model="role.permissions" :items="permissions" item-title="name" item-value="id" label="Permissions"
                                        multiple required></v-select>
                                </v-col>
                            </v-row>
                            <v-row>
                                <v-col cols="12">
                                    <v-btn @click="updateRole" color="primary">{{ $t('Save') }}</v-btn>
                                </v-col>
                            </v-row>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12">
                <v-card>
                    <v-card-title>
                        <h3>{{ $t('Permissions') }}</h3>
                    </v-card-title>
                    <v-card-text>
                        <v-data-table :headers="headers" :items="permissions" :items-per-page="5" class="elevation-1">
                            <template v-slot:top>
                                <v-toolbar flat>
                                    <v-toolbar-title>
                                        {{ $t('Permissions') }}
                                        <v-btn color="primary" @click="openDialogCreate">{{ $t('CreatePermission') }}</v-btn>
                                    </v-toolbar-title>
                                    <v-divider class="mx-4" inset vertical></v-divider>
                                    <v-spacer></v-spacer>
                                    <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line
                                        hide-details></v-text-field>
                                </v-toolbar>
                            </template>
                            <template v-slot:item.actions="{ item }">
                                <v-icon small @click="editPermission(item)">mdi-pencil</v-icon>
                                <v-icon small @click="deletePermission(item)">mdi-delete</v-icon>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
        <v-dialog v-model="dialog" max-width="500px">
            <v-card>
                <v-card-title>
                    <span class="headline">{{ $t('EditPermission') }}</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field v-model="permission.name" label="Name" required></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDialog">{{ $t('Close') }}</v-btn>
                    <v-btn color="blue darken-1" text @click="updatePermission">{{ $t('Save') }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>

        <v-dialog v-model="dialogCreate" max-width="500px">
            <v-card>
                <v-card-title>
                    <span class="headline">{{ $t('CreatePermission') }}</span>
                </v-card-title>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12">
                                <v-text-field v-model="permission.name" label="Name" required></v-text-field>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="closeDialogCreate">{{ $t('Close') }}</v-btn>
                    <v-btn color="blue darken-1" text @click="createPermission">{{ $t('Save') }}</v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>


    </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

const headers = [
    { title: 'Name', value: 'name' },
    { title: 'Actions', value: 'actions', sortable: false }
]

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const dialog = ref(false)

const role = ref({
    name: '',
    permissions: []
})

const permission = ref({
    name: ''
})

const search = ref('')

onMounted(() => {
    getRole()
    getPermissions()
})

const permissions = ref([])

const dialogCreate = ref(false)

const openDialogCreate = () => {
    dialogCreate.value = true
}

const closeDialogCreate = () => {
    dialogCreate.value = false
}

const editPermission = (item) => {
    permission.value = { ...item }
    dialog.value = true
}

const createPermission = async () => {
    try {
        const response = await fetch(window.URL + '/api/create_permission/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(permission.value)
        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        closeDialogCreate()
        getPermissions()
    } catch (error) {
        console.error(error)
    }
}

const updatePermission = async () => {
    try {
        const response = await fetch(window.URL + '/api/get_permission/' + permission.value.id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(permission.value)
        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        closeDialog()
        getPermissions()
    } catch (error) {
        console.error(error)
    }
}

const getPermissions = async () => {
    try {
        const response = await fetch(window.URL + '/api/get_permissions/');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        permissions.value = data
    } catch (error) {
        console.error(error)
    }
}

const getRole = async () => {
    try {
        const response = await fetch(window.URL + '/api/get_group/' + route.params.id + '/');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json()
        role.value = data
    } catch (error) {
        console.error(error)
    }
}

const updateRole = async () => {
    try {
        const response = await fetch(window.URL + '/api/get_group/' + route.params.id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(role.value)
        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        router.push('/roles-and-permissions')
    } catch (error) {
        console.error(error)
    }
}

</script>