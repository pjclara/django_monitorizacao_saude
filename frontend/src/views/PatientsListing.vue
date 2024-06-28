<template>
    <v-container>
        <!-- DESKTOP -->
        <v-col v-if="!smAndDown">
            <!-- <v-row no-gutters justify="center" class="mb-2">
                <h3>{{ $t('PatientsListing') }}</h3>
            </v-row> -->
            <v-text-field v-model="search" label="Procurar Pacientes" class="mb-4" outlined></v-text-field>
            <v-data-table :headers="headers" :items="patientsList" v-model:expanded="expanded" :search="search"
                :mobile="smAndDown" item-value="sns">
                <template v-slot:top>
                    <v-toolbar flat>
                        <v-col cols="3">
                            <v-toolbar-title>{{ $t('PatientsListing') }}</v-toolbar-title>
                        </v-col>
                        <v-divider class="mx-4" inset vertical></v-divider>
                        <v-col cols="5" class="d-flex justify-center pt-8">
                            <v-checkbox v-model="showMonitoredPatients"
                                label="Show Patients being monitored"></v-checkbox>
                        </v-col>
                        <v-divider class="mx-4" inset vertical></v-divider>
                        <v-col cols="3">
                            <v-btn class="mb-2" color="primary" dark to="/create-patient">
                                {{ $t('CreatePatient') }}
                            </v-btn>
                        </v-col>
                    </v-toolbar>
                </template>
                <template v-slot:item.dispositivos="{ item }">
                    <v-row v-for="(dispositivo, indexSinal) in item.dispositivos" :key="indexSinal" class="my-1">
                        <v-col>
                            <v-chip color="success" v-if="dispositivo.ativo">{{ dispositivo.modelo }}:
                                On</v-chip><v-chip color="primary" v-else>{{ dispositivo.modelo }}: Off</v-chip>
                        </v-col>
                        <v-col>
                            <v-row v-for="(sinalVital, index) in dispositivo.sinaisVitais" :key="index">

                                <v-col>
                                    <v-chip class="mr-2" :disabled="disabled" v-if="item"
                                        @click="activate(item, indexSinal, index, loopAtivo)"
                                        :color="sinalVital.ativo ? 'success' : 'primary'">
                                        <v-tooltip :text="sinalVital.tipo" activator="parent" />
                                        <span v-if="sinalVital.tipo == 'Temperatura'">
                                            <img src="/temperatura.png" alt="" width="20px" height="20px">
                                        </span>
                                        <span v-else-if="sinalVital.tipo == 'Saturação Oxigênio'">
                                            <img src="/oxigenio.png" alt="" width="20px" height="20px">
                                        </span>
                                        <span v-else>
                                            <img src="/heart_beat.png" alt="" width="20px" height="20px">
                                        </span>
                                        <span v-if="sinalVital.ativo">On</span><span v-else>Off</span>
                                    </v-chip>
                                </v-col>
                                <v-col>
                                    <v-chip :color="hasAlertSignal(sinalVital) ? 'red' : 'success'">
                                        <span>
                                            <span v-if="hasAlertSignal(sinalVital)" class="cursor-pointer"
                                                @click="redirectNotifications(item, hasAlertSignal(sinalVital), dispositivo)">Alert</span>
                                            <span v-else>No Alert</span>
                                        </span>
                                    </v-chip>
                                </v-col>
                            </v-row>
                        </v-col>
                    </v-row>
                </template>
                <template v-slot:item.dataNascimento="{ item }">
                    {{ formatDate(item.dataNascimento) }}
                </template>
                <template v-slot:item.actions="{ item }">
                    <v-icon :disabled="disabled" @click="viewItem(item)" class="mr-10">mdi-eye</v-icon>
                    <v-icon :disabled="disabled" @click="editItem(item)">mdi-pencil</v-icon>
                </template>
            </v-data-table>
        </v-col>
        <!-- MOBILE -->
        <v-col v-else>
            <v-row no-gutters justify="center" class="mb-2">
                <div class="text-h4 text-center text-center">{{ $t('PatientsListing') }}</div>
                <v-btn class="my-3" color="primary" dark to="/create-patient">
                    {{ $t('CreatePatient') }}
                </v-btn>
                <v-checkbox v-model="showMonitoredPatients" label="Show Patients being monitored"></v-checkbox>
            </v-row>
            <v-card v-for="(patient, index) in patientsList" :key="index" class="d-flex my-2">
                <v-col cols="12" class="align-center">
                    <div v-for="(header, i) in headers" :key="i" class="d-flex mb-2">
                        <v-row no-gutters class="w-50 align-center">
                            <span class="font-weight-bold">{{ header.title }}</span>
                        </v-row>
                        <v-row no-gutters class="w-50 justify-center">
                            <div v-if="header.key === 'dispositivos'">
                                <div v-for="(dispositivo, indexSinal) in patient.dispositivos" :key="indexSinal"
                                    class="d-flex flex-column my-1 pa-2 mobile-item-border align-center">
                                    <span class="font-weight-bold"> {{ dispositivo.modelo }} </span>
                                    <v-row v-for="(sinalVital, index) in dispositivo.sinaisVitais" :key="index"
                                        class="my-3 mx-1">
                                        <v-chip :disabled="disabled"
                                            @click="activate(item, indexSinal, index, loopAtivo)"
                                            :color="sinalVital.ativo ? 'success' : 'primary'">
                                            <v-tooltip :text="sinalVital.tipo" activator="parent" />
                                            <span v-if="sinalVital.tipo == 'Temperatura'">
                                                <img src="/temperatura.png" alt="" width="20px" height="20px">
                                            </span>
                                            <span v-else-if="sinalVital.tipo == 'Saturação Oxigênio'">
                                                <img src="/oxigenio.png" alt="" width="20px" height="20px">
                                            </span>
                                            <span v-else>
                                                <img src="/heart_beat.png" alt="" width="20px" height="20px">
                                            </span>
                                            <span v-if="sinalVital.ativo">On</span><span v-else>Off</span>
                                        </v-chip>
                                        <v-chip :color="hasAlertSignal(sinalVital) ? 'red' : 'success'">
                                            <span>
                                                <span v-if="hasAlertSignal(sinalVital)"
                                                    @click="redirectNotifications(patient, hasAlertSignal(sinalVital), dispositivo)">Alert</span>
                                                <span v-else>No Alert</span>
                                            </span>
                                        </v-chip>
                                    </v-row>
                                </div>
                            </div>
                            <div v-else-if="header.key === 'dataNascimento'">
                                {{ formatDate(patient.dataNascimento) }}
                            </div>
                            <div v-else-if="header.key === 'actions'"
                                class="d-flex w-100 justify-space-evenly pa-3 mobile-item-border">
                                <v-icon :disabled="disabled" @click="viewItem(patient)" class="mr-10">mdi-eye</v-icon>
                                <v-icon :disabled="disabled" @click="editItem(patient)">mdi-pencil</v-icon>
                            </div>
                            <div v-else>
                                {{ patient[header.key] }}
                            </div>
                        </v-row>
                    </div>
                </v-col>
            </v-card>
        </v-col>
    </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { differenceInYears } from 'date-fns';
import { useRouter } from 'vue-router';
import { useLoaderStore } from '@/stores/loader'
import { useUsersStore } from '@/stores/users';
import { useDisplay } from 'vuetify'
const { smAndDown } = useDisplay()
import { toast } from 'vue3-toastify';

const user = useUsersStore().user

const loaderStore = useLoaderStore();

const router = useRouter();

const loopAtivo = ref(false);

const expanded = ref([]);

const patients = ref([])

const disabled = ref(false);

const showMonitoredPatients = ref(true);

const search = ref(null)

const patientsList = computed(() => {
    return showMonitoredPatients.value ? patients.value.filter(patient => patient.dispositivos.some(dispositivo => dispositivo.ativo)) : patients.value;
})

const hasAlertSignal = (sinalVital) => {
    if (sinalVital.valores.length == 0) {
        return false;
    }

    const isRead = sinalVital.valores[sinalVital.valores.length - 1].lida ? false : true;
    // return !sinalVital.values?.some(sinal => sinal.alerta);

    return isRead
}
const desativarSinal = async (patient, indexSinal, index) => {
    patient.dispositivos[indexSinal].sinaisVitais[index].ativo = false;
    patient.dispositivos[indexSinal].ativo = patient.dispositivos[indexSinal].sinaisVitais.some(sinal => sinal.ativo);
    const response = await fetch(window.URL + `/api/documentos/desativar_sinal_vital/${patient.sns}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                "dispositivo_idx": indexSinal,
                "sinal_idx": index
            }
        ),
    });
    if (!response.ok) {
        throw new Error('Failed to fetch data');
    }
    toast.success('Data creation stopped');
    disabled.value = false;
}

const ativarSinal = async (patient, indexSinal, index) => {
    patient.dispositivos[indexSinal].sinaisVitais[index].ativo = true;
    patient.dispositivos[indexSinal].ativo = patient.dispositivos[indexSinal].sinaisVitais.some(sinal => sinal.ativo);
    const response = await fetch(window.URL + `/api/documentos/ativar_sinal_vital/${patient.sns}/`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(
            {
                "dispositivo_idx": indexSinal,
                "sinal_idx": index,
                "data" : new Date().toISOString()
            }
        ),
    });
    if (!response.ok) {
        throw new Error('Failed to fetch data');
    }
    toast.success('Data creation stopped');
    disabled.value = false;
}

const activate = async (patient, indexSinal, index, loop) => {
    if (patient.dispositivos[indexSinal].sinaisVitais[index].ativo) {
        await desativarSinal(patient, indexSinal, index);
    } else {
        await ativarSinal(patient, indexSinal, index);
    }
}



/*


const activate = async (patient, indexSinal, index, loop) => {
    console.log(patient);
    patient.dispositivos[indexSinal].sinaisVitais[index].ativo = !patient.dispositivos[indexSinal].sinaisVitais[index].ativo;
    patient.dispositivos[indexSinal].ativo = patient.dispositivos[indexSinal].sinaisVitais.some(sinal => sinal.ativo);
    if (patient.dispositivos[indexSinal].sinaisVitais[index].ativo) {
        toast.info('Data creation started');
    } else {
        disabled.value = true;
        const response = await fetch(window.URL + `/api/documentos/atualizar_documento_por_sns/${patient.sns}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(patient),
        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        toast.success('Data creation stopped');
        disabled.value = false;
    }
    const max = patient.dispositivos[indexSinal].sinaisVitais[index].maximo + patient.dispositivos[indexSinal].sinaisVitais[index].maximo * 0.2;
    const min = patient.dispositivos[indexSinal].sinaisVitais[index].minimo - patient.dispositivos[indexSinal].sinaisVitais[index].minimo * 0.2;
    console.log(max, min);
    while (patient.dispositivos[indexSinal].sinaisVitais[index].ativo) {
        const random = Math.floor(Math.random() * (max - min + 1) + min);
        patient.dispositivos[indexSinal].sinaisVitais[index].valores.push(
            {
                "valor": Math.floor(Math.random() * (max - min + 1) + min),
                "data": new Date().toISOString()
            });
        const response = await fetch(window.URL + `/api/documentos/atualizar_documento_por_sns/${patient.sns}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(patient),
        });
        // sleep for 5 seconds
        await sleep(5000);
    }
}
    */

const sleep = (ms) => {
    return new Promise(resolve => setTimeout(resolve, ms));
};

const headers = ref([
    { title: 'Name', key: 'nome', width: '20%', align: 'center' },
    { title: 'SNS', key: 'sns', width: '10%', align: 'center' },
    { title: 'Age', key: 'dataNascimento', width: '10%', align: 'center' },
    { title: 'Dispositivos', key: 'dispositivos', width: '45%', align: 'center' },
    { title: 'Actions', key: 'actions', sortable: false, width: '15%', align: 'center' },
]);

onMounted(() => {
    fetchDataFromApi();
});

const formatDate = (date) => {
    const dob = new Date(date);
    const diff = differenceInYears(new Date(), dob);
    return diff + ' years';
};

const fetchDataFromApi = async () => {
    try {
        loaderStore.setLoading(true);
        const response = await fetch(window.URL + '/api/patients/listar_documentos_com_profissionais/' + user.user_id + '/');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        patients.value = data;
        console.log(data);

    } catch (error) {
        console.error(error);
    }
    loaderStore.setLoading(false);
};

const viewItem = (item) => {
    // redirect to patient profile
    router.push({ name: 'PatientProfile', params: { patientSns: item.sns } });
}

const editItem = (item) => {
    // redirect to patient profile
    router.push({ name: 'PatientEdit', params: { patientSns: item.sns } });
}

const redirectNotifications = (item, hasAlert, dispositivo) => {
    router.push({ name: 'PatientProfile', params: { patientSns: item.sns }, query: { estatistics: hasAlert, modelo: dispositivo.modelo } });
}
</script>

<style scoped>
.mobile-item-border {
    border: 1px solid lightblue;
    border-radius: 10px;
}
</style>
