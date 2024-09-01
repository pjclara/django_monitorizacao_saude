<template>
    <v-container>
        <v-row no-gutters>
            <v-col cols="12" align="center">
                <p class="text-h5 my-4"> {{ $t("passwordRecovery") }}</p>
                <v-col :cols="smAndDown ? '12' : '6'">
                    <v-text-field label="Email" color="primary" v-model="email" />
                </v-col>
                <v-btn :disabled="!email" @click="passwordRecovery">{{ $t("recover") }}</v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useLoaderStore } from '@/stores/loader'
import { useRouter } from 'vue-router';
import { useDisplay } from 'vuetify'
import { toast } from 'vue3-toastify';

const { smAndDown } = useDisplay()

const router = useRouter();

const loaderStore = useLoaderStore();

const email = ref(null)

const passwordRecovery = async () => {
    loaderStore.setLoading(true);
    try {
        const response = await fetch(window.URL + '/api/password_recovery/' + email.value + '/');
        if (!response.ok) {
            toast.error('Failed to fetch data');
            throw new Error('Failed to fetch data');
        } else {
            console.log("response ok : ", response)
            toast.success('Email Sent');
        }
    } catch (error) {
        console.error(error);
    }
    loaderStore.setLoading(false);
    // pause for 2 seconds
    await new Promise(r => setTimeout(r, 2000));
    router.push({ name: 'login' });
};
</script>