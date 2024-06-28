<template>
    <v-navigation-drawer v-model="showSidebar" class="d-flex flex-column">
        <v-list>
            <v-spacer class="spacer mx-2 mt-2" />

            <v-list-item class="d-flex justify-center my-5">
                <v-btn variant="outlined" @click="changeRoute('Home')">
                    {{ $t('home') }}
                </v-btn>
            </v-list-item>
            <v-spacer class="spacer mx-2" />
            <v-list-item class="d-flex justify-center my-5">
                <v-btn variant="outlined" @click="changeRoute('EmployeesListing')">
                    {{ $t('staffManagement') }}
                </v-btn>
            </v-list-item>

            <!-- <v-list-item class="d-flex justify-center my-5">
                <v-btn variant="outlined">
                    {{ $t('pacientsManagement') }}
                </v-btn>
            </v-list-item> -->

            <v-spacer class="spacer mx-2" />

            <v-list-item class="d-flex justify-center my-5">
                <v-btn variant="outlined" @click="changeRoute('PatientsListing')">
                    {{ $t('pacients') }}
                </v-btn>
            </v-list-item>

            <v-spacer class="spacer mx-2" />
            <!-- 
            <v-list-item class="d-flex justify-center my-5">
                <v-btn variant="outlined">
                    {{ $t('overallStatistics') }}
                </v-btn>
            </v-list-item> -->
        </v-list>
        <template v-slot:append>
            <v-list>
                <v-spacer class="spacer mx-2 my-4" />

                <v-list-item class="d-flex justify-center my-5" v-if="isLogged">
                    <v-btn variant="outlined" @click="changeRoute('MyProfile')">
                        {{ $t('profileSettings') }}
                    </v-btn>
                </v-list-item>
                <v-list-item class="d-flex justify-center my-5" v-if="isLogged">
                    <v-btn variant="outlined" @click="logOut()">
                        {{ $t('logOut') }}
                    </v-btn>
                </v-list-item>
                <v-list-item class="d-flex justify-center my-5" v-if="!isLogged">
                    <v-btn variant="outlined" @click="changeRoute('login')">
                        {{ $t('logIn') }}
                    </v-btn>
                </v-list-item>

                <v-spacer class="spacer mx-2 my-4" />

                <v-list-item class="d-flex justify-center">
                    <v-btn variant="outlined" class="mr-2" @click="changeLocale('PT')">
                        <img height="32" src="/portugal-48.png" />
                    </v-btn>
                    <v-btn variant="outlined" @click="changeLocale('EN')">
                        <img height="32" src="/united-kingdom-48.png" />
                    </v-btn>
                </v-list-item>
            </v-list>
        </template>
    </v-navigation-drawer>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia'
import { useLayoutStore } from '@/stores/layout'
import { useUsersStore } from '@/stores/users'
import { useI18n } from 'vue-i18n'

const router = useRouter();
const layoutStore = useLayoutStore()
const usersStore = useUsersStore()

const showSidebar = storeToRefs(layoutStore).showSidebar;
const isLogged = storeToRefs(usersStore).isLogged;

let { locale } = useI18n()

function changeLocale(language) {
    locale.value = language
}

const changeRoute = (routeName) => {
    router.push({ name: routeName });
}


const logOut = () => {
    usersStore.user = null;
    usersStore.isLogged = false
    router.push({ name: 'login' });
}
</script>

<style scoped>
.spacer {
    border-bottom: 2px solid grey;
}

.v-btn--variant-outlined {
    border: thin solid skyblue;
}
</style>