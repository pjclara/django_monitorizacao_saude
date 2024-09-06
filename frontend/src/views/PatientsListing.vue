<template>
    <v-container>
        <!-- DESKTOP -->
        <div v-if="!smAndDown">
            <v-row>
                <v-col class="d-flex justify-start" cols="12" sm="4">
                    <v-btn color="indigo-darken-3" @click="voltarPainel"><v-icon class="mr-2">mdi-home</v-icon>{{
                        $t('Dashboard') }}</v-btn>
                </v-col>
                <v-col class="text-h4 text-center font-weight-bold text-deep-purple-darken-4" cols="12" sm="4">{{
                    $t('PatientsListing')
                    }}
                </v-col>
                <v-col class="d-flex justify-end" cols="12" sm="4">
                    <v-btn color="indigo-darken-3" elevated to="/create-patient">
                        <v-icon color="white" class="mr-2">mdi-plus</v-icon>{{ $t('AddPatient') }}
                    </v-btn>
                </v-col>
            </v-row>
            <v-row>
                <v-data-table :headers="headers" :items="patientsList" v-model:expanded="expanded" :search="search"
                    :mobile="smAndDown" item-value="sns" class="custom_table_class">
                    <template v-slot:headers>
                        <tr>
                            <th v-for="header in headers" :key="header.title" class="text-center">{{ $t(header.title) }}
                            </th>
                        </tr>
                    </template>
                    <template v-slot:top>
                        <v-toolbar flat style="background-color: #425C5A; color: white;">
                            <v-col cols="3">
                                <v-toolbar-title>{{ $t('PatientsListing') }}</v-toolbar-title>
                            </v-col>
                            <v-divider class="mx-4" inset vertical></v-divider>
                            <v-col cols="5" class="d-flex justify-center pt-8">
                                <v-checkbox v-model="showMonitoredPatients"
                                    :label="$t('Show Patients being monitored')"></v-checkbox>
                            </v-col>
                            <v-divider class="mx-4" inset vertical></v-divider>
                            <v-col cols="3" class="d-flex justify-center align-center">
                                <div class="search-container">
                                    <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" height="24"
                                        viewBox="0 96 960 960" width="24" fill="#888">
                                        <path
                                            d="M796 936 536 676q-28 24-62 36.5T400 725q-95 0-161.5-66.5T172 496q0-95 66.5-161.5T400 268q95 0 161.5 66.5T628 496q0 36-12.5 70T580 628l260 260-44 48Zm-396-292q66 0 112-46t46-112q0-66-46-112t-112-46q-66 0-112 46t-46 112q0 66 46 112t112 46Z" />
                                    </svg>
                                    <input type="search" class="search-input" :placeholder="$t('Search for Patients')"
                                        v-model="search">
                                </div>
                            </v-col>
                        </v-toolbar>
                    </template>
                    <template v-slot:item.dispositivos="{ item }">
                        <v-row v-for="(dispositivo, indexSinal) in item.dispositivos" :key="indexSinal" class="my-1">
                            <v-col cols="4">
                                <v-chip color="success" v-if="dispositivo.ativo">{{ dispositivo.modelo }}
                                    On</v-chip><v-chip color="primary" v-else>{{ dispositivo.modelo }}: Off</v-chip>
                            </v-col>
                            <v-col>
                                <v-row v-for="(sinalVital, index) in dispositivo.sinaisVitais" :key="index">
                                    <v-col>
                                        <v-btn @click="startGenerateData(item, indexSinal, index)"
                                            v-if="!getStartValue(item.sns, indexSinal, index)" color="primary"
                                            width="150px">
                                            <span v-if="sinalVital.tipo == 'Temperatura'">
                                                <img class="rounded p-2" src="/temperatura.png" alt="" width="20px"
                                                    height="20px">
                                            </span>
                                            <span v-else-if="sinalVital.tipo == 'Saturação Oxigênio'">
                                                <img class="rounded p-2" src="/oxigenio.png" alt="" width="20px"
                                                    height="20px">
                                            </span>
                                            <span v-else>
                                                <img class="rounded p-2" src="/heart_beat.png" alt="" width="20px"
                                                    height="20px">
                                            </span>
                                            <span class="ml-2">{{ $t("Activate") }}</span>
                                        </v-btn>
                                        <v-btn @click="stopGeneratingData(item, indexSinal, index)"
                                            v-if="getStartValue(item.sns, indexSinal, index)" color="secondary"
                                            width="150px">
                                            <span v-if="sinalVital.tipo == 'Temperatura'">
                                                <img class="rounded p-2" src="/temperatura.png" alt="" width="20px"
                                                    height="20px">
                                            </span>
                                            <span v-else-if="sinalVital.tipo == 'Saturação Oxigênio'">
                                                <img class="rounded p-2" src="/oxigenio.png" alt="" width="20px"
                                                    height="20px">
                                            </span>
                                            <span v-else>
                                                <img class="rounded p-2" src="/heart_beat.png" alt="" width="20px"
                                                    height="20px">
                                            </span>
                                            <span class="ml-2">{{ $t("Deactivate") }}</span>
                                        </v-btn>
                                    </v-col>
                                    <v-col>
                                        <v-chip :color="hasAlertSignal(sinalVital) ? 'red' : 'success'">
                                            <span>
                                                <span v-if="hasAlertSignal(sinalVital)" class="cursor-pointer"
                                                    @click="redirectNotifications(item, hasAlertSignal(sinalVital), dispositivo)">{{
                                                        $t('Alert') }}</span>
                                                <span v-else>{{ $t('No Alert') }}</span>
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
            </v-row>
        </div>
        <!-- MOBILE -->
        <div v-else>
            <v-row>
                <v-col class="d-flex justify-center" cols="12" sm="4">
                    <v-btn color="indigo-darken-3" @click="voltarPainel"><v-icon class="mr-2">mdi-home</v-icon>{{
                        $t('dashboard') }}</v-btn>
                </v-col>
                <v-col class="text-h4 text-center font-weight-bold text-deep-purple-darken-4" cols="12" sm="4">{{
                    $t('PatientsListing')
                    }}
                </v-col>
                <v-col class="d-flex justify-center" cols="12" sm="4">
                    <v-btn color="indigo-darken-3" elevated to="/create-patient">
                        <v-icon color="white" class="mr-2">mdi-plus</v-icon>{{ $t('AddPatient') }}
                    </v-btn>
                </v-col>
            </v-row>
            <v-row no-gutters justify="center" class="mb-2">
                <v-col cols="12" class="d-flex justify-center align-center">
                    <v-checkbox v-model="showMonitoredPatients">
                        <template v-slot:label>
                            <span style="font-size: 12px">{{ $t('Show Patients being monitored') }}</span>
                        </template>
                    </v-checkbox>
                </v-col>
            </v-row>
            <v-row no-gutters>
                <v-col cols="12" v-for="(patient, index) in patientsList" :key="index">
                    <v-card class="d-flex flex-column my-2 pa-10 mobile-card">
                        <v-row class="d-flex justify-space-between align-center border  border-lg mb-1 rounded-lg pa-1">
                            <span class="font-weight-bold">
                                {{ $t('Name') }} :
                            </span>
                            <span>
                                {{ patient.nome }}
                            </span>
                        </v-row>
                        <v-row class="d-flex justify-space-between border mb-1 border-lg rounded-lg pa-1">
                            <span class="font-weight-bold">
                                {{ $t('Health number') }}:
                            </span>
                            <span>
                                {{ patient.sns }}
                            </span>
                        </v-row>
                        <v-row class="d-flex justify-space-between align-center border border-lg mb-1 rounded-lg pa-1">
                            <span class="font-weight-bold">
                                {{ $t('Age') }}:
                            </span>
                            <span>
                                {{ formatDate(patient.dataNascimento) }} {{ $t('years') }}
                            </span>
                        </v-row>

                        <v-row v-for="(dispositivo, indexSinal) in patient?.dispositivos" :key="indexSinal" class="border border-lg mb-1">

                            <v-col class="d-flex justify-center" cols="12">
                                <span class="font-weight-bold">{{ $t('Model') }}: </span>
                                <span> {{ dispositivo.modelo }} </span>
                            </v-col>

                            <v-col v-for="(sinalVital, index) in dispositivo.sinaisVitais" :key="index"
                                class="my-3 mx-1 d-flex justify-center border border-lg mb-1 rounded-xl">
                                <v-chip :disabled="disabled" @click="generateData(patient, indexSinal, index)"
                                    :color="sinalVital.ativo ? 'success' : 'primary'">
                                    <v-tooltip :text="sinalVital.tipo" activator="parent" />
                                    <span v-if="sinalVital.tipo == 'Temperatura'">
                                        <img class="" src="/temperatura.png" alt="" width="20px" height="20px">
                                    </span>
                                    <span v-else-if="sinalVital.tipo == 'Saturação Oxigênio'">
                                        <img class="" src="/oxigenio.png" alt="" width="20px" height="20px">
                                    </span>
                                    <span v-else>
                                        <img src="/heart_beat.png" alt="" width="20px" height="20px">
                                    </span>
                                    <span v-if="sinalVital.ativo">On</span>
                                    
                                    <span v-else>Off</span>
                                </v-chip>
                                <v-chip :color="hasAlertSignal(sinalVital) ? 'red' : 'success'">
                                    <span>
                                        <span v-if="hasAlertSignal(sinalVital)"
                                            @click="redirectNotifications(patient, hasAlertSignal(sinalVital), dispositivo)">Alert</span>
                                        <span v-else>No Alert</span>
                                    </span>
                                </v-chip>
                            </v-col>
                        </v-row>
                        <v-row class="d-flex justify-center align-center border mb-2">
                            <span class="mr-2">
                                <v-icon :disabled="disabled" @click="editItem(patient)">mdi-pencil</v-icon>
                            </span>
                            <span>
                                <v-icon :disabled="disabled" @click="viewItem(patient)">mdi-eye</v-icon>
                            </span>
                        </v-row>
                    </v-card>
                </v-col>
            </v-row>
        </div>
    </v-container>

</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { differenceInYears } from 'date-fns';
import { useRouter } from 'vue-router';
import { useUsersStore } from '@/stores/users';
import { useDisplay } from 'vuetify'
import { useVitalSignsStore } from '@/stores/vitalSigns'
import { usePatientsStore } from '@/stores/patients';

const { smAndDown } = useDisplay()

const user = useUsersStore().user

const router = useRouter();

const expanded = ref([]);

const disabled = ref(useVitalSignsStore().disabled);

const showMonitoredPatients = ref(false);

const search = ref(null)

const headers = ref([
    { title: 'Name', key: 'nome', width: '20%', align: 'center' },
    { title: 'Health number', key: 'sns', width: '10%', align: 'center' },
    { title: 'Age', key: 'dataNascimento', width: '5%', align: 'center' },
    //email
    { title: 'email', key: 'email', width: '10%', align: 'center' },
    { title: 'devices', key: 'dispositivos', width: '45%', align: 'center' },
    { title: 'Actions', key: 'actions', sortable: false, width: '10%', align: 'center' },
]);

onMounted(() => {
    if (usePatientsStore().patients.length === 0)
        usePatientsStore().fetchPatients(user.user_id);

});

const patientsList = computed(() => {
    return showMonitoredPatients.value ? usePatientsStore().patients.filter(patient => patient.dispositivos.some(dispositivo => dispositivo.ativo)) : usePatientsStore().patients;
})

const hasAlertSignal = (sinalVital) => {
    if (sinalVital.valores.length == 0) {
        return false;
    }
    return sinalVital.valores?.some(sinal => sinal.alerta && !sinal.lida);

}

const startGenerateData = (patient, indexSinal, index) => {
    patient.dispositivos[indexSinal].sinaisVitais[index].ativo = true
    patient.dispositivos[indexSinal].ativo = patient.dispositivos[indexSinal].sinaisVitais.some(
        (sinal) => sinal.ativo
    )
    useVitalSignsStore().startGenerateData(patient, indexSinal, index);
    useVitalSignsStore().updateStart(patient.sns, indexSinal, index, true);

}

const stopGeneratingData = async (patient, indexSinal, index) => {
    patient.dispositivos[indexSinal].sinaisVitais[index].ativo = false
    patient.dispositivos[indexSinal].ativo = patient.dispositivos[indexSinal].sinaisVitais.some(
        (sinal) => sinal.ativo
    )
    useVitalSignsStore().stopGeneratingData(patient, indexSinal, index);
    useVitalSignsStore().updateStart(patient.sns, indexSinal, index, false);
}

const voltarPainel = () => {
    router.push({ name: 'HomeUser' });
}

const generateData = async (patient, indexSinal, index) => {
    const start = getStartValue(patient.sns, indexSinal, index);
    if(start){
        stopGeneratingData(patient, indexSinal, index);
        return;
    }
    startGenerateData(patient, indexSinal, index);
}


const formatDate = (date) => {
    const dob = new Date(date);
    const diff = differenceInYears(new Date(), dob);
    return diff;
};


const getStartValue = (sns, indexSinal, index) => {
    const start = useVitalSignsStore().start;

    const value = start.find((item) => item.patient === sns && item.indexSinal === indexSinal && item.index === index);

    return value ? value.start : false;
}

const viewItem = (item) => {
    // redirect to patient profile
    router.push({ name: 'PatientProfile', params: { patientSns: item.sns } });
}

const editItem = (item) => {
    // redirect to patient profile
    router.push({ name: 'PatientEdit', params: { patientSns: item.sns } });
}

const redirectNotifications = (item, hasAlert, dispositivo) => {
    router.push({ name: 'PatientProfile', params: { patientSns: item.sns }, query: { notifications: hasAlert, modelo: dispositivo.modelo } });
}
</script>

<style>
.mobile-item-border {
    border: 1px solid lightblue;
    border-radius: 10px;
}

.v-container .v-toolbar__content {
    background-color: #006400;
    color: #E0E0E0;
}

.v-data-table-footer {
    background-color: white;
}
</style>
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
