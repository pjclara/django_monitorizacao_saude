<template>
    <v-container>
        <div class="d-flex flex-column">
            <v-col class="d-flex align-center">
                <v-card class="patient-card pa-2" variant="outlined">
                    <v-card-text>
                        <v-row>
                            <v-col class="d-flex justify-center align-center" v-if="!smAndDown">
                                <img src="/userAnoon.png" width="120px" height="120px" alt="userStockPhoto">
                            </v-col>
                            <v-col class="d-flex flex-column justify-space-between">
                                <div class="d-flex justify-center my-2" v-if="smAndDown">
                                    <img src="/userAnoon.png" width="120px" height="120px" alt="userStockPhoto">
                                </div>
                                <div>
                                    <span class="text-h6 font-weight-bold">{{ $t('name') }}: </span>
                                    <span class="text-h6">{{ identifier?.nome }}</span>
                                </div>
                                <div class="mt-2">
                                    <span class="text-h6 font-weight-bold">{{ $t('age') }}: </span>
                                    <span class="text-h6">{{ identifier?.age }}</span>
                                </div>
                                <div class="mt-2">
                                    <span class="text-h6 font-weight-bold">{{ $t('sns') }}: </span>
                                    <span class="text-h6">{{ identifier?.sns }}</span>
                                </div>
                                <div class="mt-2">
                                    <span class="text-h6 font-weight-bold">{{ $t('Gender') }}: </span>
                                    <span class="text-h6">{{ identifier?.genero }}</span>
                                </div>
                                <div class="mt-2">
                                    <span class="text-h6 font-weight-bold">{{ $t('Phone') }}: </span>
                                    <span class="text-h6">{{ identifier?.telefone }}</span>
                                </div>
                                <v-row no-gutters justify="space-between" v-if="!isPatient">
                                    <v-btn color="blue-darken-3" size="small" width="100px" class="mt-2"
                                        @click="voltar">{{ $t("Return") }}</v-btn>
                                    <v-btn color="green" size="small" width="100px" class="mt-2"
                                        @click="callPatient">{{ $t("Call") }}</v-btn>
                                    <v-btn color="blue" size="small" width="100px" class="mt-2"
                                        @click="edit(patient?.sns)">{{ $t("Edit") }}</v-btn>
                                </v-row>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-col>
            <v-col class="pa-2">
                <v-card>
                    <v-tabs v-model="tab">
                        <v-tab value="devices" class="tab-border mr-1">
                            <span class="text-blue">
                                Devices of the patient
                            </span>
                        </v-tab>
                        <v-tab value="vitals" class="tab-border mr-1">
                            <span class="text-blue">
                                Vital Signs
                            </span>
                        </v-tab>
                        <v-tab value="estatistics" class="tab-border mr-1">
                            <span class="text-blue">
                                Estatistics
                            </span>
                        </v-tab>
                        <v-tab value="notifications" class="tab-border">
                            <span class="text-blue">
                                Notifications
                            </span>
                        </v-tab>
                        <v-tab value="history" class="tab-border">
                            <span class="text-blue">
                                History
                            </span>
                        </v-tab>
                    </v-tabs>
                    <v-card-text class="flex-grow-1">
                        <v-window v-model="tab">
                            <v-window-item value="devices">
                                <div v-for="(device, index) in decicesList">
                                    <v-card class="border-md border-info" elevation="16">
                                        <v-card-title>
                                            <h3>{{ device.modelo }}</h3>
                                        </v-card-title>
                                        <v-card-text>
                                            <p>{{ device.descricao }} - {{ device.numeroSerie }}</p>

                                        </v-card-text>
                                            <v-btn color="secondary" @click="deleteDevice(index)">Delete device</v-btn>
                                    </v-card>
                                </div>
                            </v-window-item>

                            <v-window-item value="vitals">
                                <v-row no-gutters>
                                    <v-col v-for="(sinal, index) in lastVitalValues" :key="index" cols="12" sm="4">
                                        <v-sheet class="ma-2">
                                            <v-card class="border-md border-info">
                                                <v-card-title>
                                                    <h4>{{ sinal.nome }} ({{ sinal.modelo }})</h4>
                                                    <v-btn color="secondary"
                                                        @click="deleteSinal(sinal.sinal_idx, sinal.dispositivo_idx)">
                                                        Delete sinal
                                                        
                                                    </v-btn>
                                                </v-card-title>
                                                <v-card-text class="d-flex flex-wrap">
                                                    <v-row no-gutters class="w-100 justify-center"
                                                        v-if="sinal.valor?.valor">
                                                        <p v-if="sinal.min <= sinal.valor.valor && sinal.max >= sinal.valor.valor"
                                                            class="text-h6 text-green">{{
                                                                sinal.valor.valor }}</p>
                                                        <p v-else class="text-h6 text-red">{{ sinal.valor.valor }} {{
                                                            sinal.unidade }}</p>
                                                    </v-row>
                                                    <v-row v-else no-gutters class="w-100 justify-center">
                                                        <p class="text-h6 text-center">{{ $t('Without data') }}</p>
                                                    </v-row>
                                                    <v-row no-gutters class="w-100 justify-space-between">
                                                        <p class="w-50 text-center">Min: {{ sinal.min }} {{
                                                            sinal.unidade }}</p>
                                                        <p class="w-50 text-center">Max: {{ sinal.max }} {{
                                                            sinal.unidade }}</p>
                                                    </v-row>
                                                </v-card-text>
                                            </v-card>
                                        </v-sheet>
                                    </v-col>
                                </v-row>
                            </v-window-item>

                            <v-window-item value="estatistics">
                                <div v-if="!smAndDown">
                                    <div>
                                        <v-select v-model="deviceId" :items="decicesList" item-title="modelo"
                                            item-value="id" label="Choose a Device" return-object>
                                        </v-select>
                                    </div>
                                    <div>
                                        <v-btn v-for="(sinalVital, index) in sinaisVitais"
                                            :color="sinal == index ? 'green' : 'primary'" class="ma-2" :key="index"
                                            @click="atualizarGrafico(index)">{{
                                                sinalVital.nome }}</v-btn>
                                    </div>
                                    <div v-if="deviceId != null">
                                        <Line id="my-chart-id" :options="chartOptions" :data="formattedChartData" />
                                    </div>
                                </div>
                                <div v-else>
                                    <p class="text-center text-h5">{{ $t('OnlyDesktop') }}</p>
                                </div>
                            </v-window-item>

                            <v-window-item value="notifications">
                                <v-data-table :headers="notificationsHeaders" :items="processedNotifications"
                                    :items-per-page="5" v-if="!smAndDown">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title>{{ $t('notifications') }}</v-toolbar-title>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item="{ item }">
                                        <tr>
                                            <td>{{ item.dispositivo }}</td>
                                            <td>{{ item.sinal }}</td>
                                            <td>{{ item.data }}</td>
                                            <td>{{ item.valor }}</td>
                                            <td>
                                                <v-btn color="blue" @click="read(item.idBotao)">Visto</v-btn>
                                            </td>
                                        </tr>
                                    </template>

                                </v-data-table>
                                <MobileTable v-else :data="processedNotifications"
                                    :keys="['dispositivo', 'sinal', 'data', 'valor', 'idBotao']">
                                </MobileTable>
                            </v-window-item>

                            <v-window-item value="history">
                                <v-data-table :items="historyNotifications" :items-per-page="5" v-if="!smAndDown">
                                    <template v-slot:top>
                                        <v-toolbar flat>
                                            <v-toolbar-title>{{ $t('notifications') }}</v-toolbar-title>
                                        </v-toolbar>
                                    </template>
                                    <template v-slot:item="{ item }">
                                        <tr>
                                            <td>{{ item.dispositivo }}</td>
                                            <td>{{ item.sinal }}</td>
                                            <td>{{ item.data }}</td>
                                            <td>{{ item.valor }}</td>
                                        </tr>
                                    </template>
                                </v-data-table>
                                <MobileTable v-else :data="historyNotifications"
                                    :keys="['dispositivo', 'sinal', 'data', 'valor']"></MobileTable>
                            </v-window-item>
                        </v-window>
                    </v-card-text>
                </v-card>
            </v-col>
        </div>
    </v-container>
</template>
<script setup>
import MobileTable from '@/components/table/MobileTable.vue';
import { ref, onMounted, watch, computed } from 'vue';
import { Line } from 'vue-chartjs'
import { useRoute, useRouter } from 'vue-router';
import { differenceInYears } from 'date-fns';
import { toast } from 'vue3-toastify';
import { format, compareDesc } from 'date-fns'
import { useUsersStore } from '@/stores/users'
import {
    Chart as ChartJS, CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import { useDisplay } from 'vuetify'
const { smAndDown } = useDisplay()

import { useLoaderStore } from '@/stores/loader'

const loaderStore = useLoaderStore();

ChartJS.register(CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend)


const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    type: 'line',
    backgroundColor: 'rgba(75, 192, 192, 0.2)',
    borderColor: 'rgba(75, 192, 192, 1)',
    borderWidth: 1,
    responsive: true,
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

const router = useRouter();

const props = defineProps(['alert'])

const isPatient = computed(() => {
    return useUsersStore().user?.groups.includes('paciente') ? true : false
});

const sinal = ref(0);

const voltar = () => {
    router.go(-1);
};

// variables

const tab = ref(null);
const patient = ref([]);

const patientSns = useRoute().params.patientSns;
const deviceId = ref(null);

const sinaisVitais = computed(() => {
    if (!deviceId.value) {
        return [];
    }
    return patient.value.dispositivos.find(device => device.numeroSerie === deviceId.value.numeroSerie).sinaisVitais.map(sinal => {
        return { nome: sinal.tipo }
    });
});

const lastVitalValues = computed(() => {
    const values = patient.value.dispositivos.map((dispositivo, dispositivo_idx) => dispositivo.sinaisVitais.map((sinal, sinal_idx) => {
        return {
            dispositivo_idx: dispositivo_idx,
            sinal_idx: sinal_idx,
            modelo: dispositivo.modelo, nome: sinal.tipo, max: sinal.maximo, min: sinal.minimo, unidade: sinal.unidade, valor: sinal.valores[sinal.valores.length - 1]
        }
    }))
    return values.flat()
})

const identifier = computed(() => {
    if (!patient.value) {
        return [];
    }
    const data = {
        nome: patient.value.nome,
        age: differenceInYears(new Date(), new Date(patient.value.dataNascimento)),
        sns: patient.value.sns,
        telefone: patient.value.telefone,
        genero: patient.value.genero
    }
    return data;
});

const decicesList = computed(() => {
    if (!patient.value) {
        return [];
    }
    return patient.value.dispositivos?.map(device => {
        return {
            modelo: device.modelo,
            descricao: device.descricao,
            numeroSerie: device.numeroSerie,
            fabricante: device.fabricante
        }
    });
});


onMounted(async () => {
    await fetchPatientData();
    await fetchNotifications();
    try {
        const ws = new WebSocket('ws://' + useLoaderStore().url + '/ws/pacient/room' + patientSns + '/');
        ws.onopen = () => {
            console.log('Connected to the websocket server')
        }
        ws.onmessage = (event) => {
            fetchPatientData();
            fetchNotifications();
        }
    }
    catch (error) {
        console.error('Error:', error);
    }
    if (router.currentRoute.value.query.notifications) {
        tab.value = 'notifications';
    }
    if (router.currentRoute.value.query.estatistics && router.currentRoute.value.query.modelo) {
        tab.value = 'estatistics';
        deviceId.value = decicesList.value.find(device => device.modelo === router.currentRoute.value.query.modelo);

    }
});

const callPatient = () => {
    window.location.href = `tel:${patient?.value?.telefone}`;
}

const notificationsHeaders = ref([
    { title: 'Dispositivo', key: 'dispositivo' },
    { title: 'Sinal', key: 'sinal' },
    { title: 'Data', key: 'data' },
    { title: 'Valor', key: 'valor' },
    { title: 'Actions', key: 'idBotao', sortable: false }
])


// get patient data from api
const fetchPatientData = async () => {
    try {
        loaderStore.setLoading(true);

        const response = await fetch(window.URL + '/api/documentos/buscar_por_sns/' + patientSns + '/');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        patient.value = await response.json();
    } catch (error) {
        console.error(error);
    }
    loaderStore.setLoading(false);

};


// chart data

const chartData = ref({
    labels: [],
    datasets: []
});

const clean = () => {
    if (chartData.value) {
        chartData.value = {
            labels: [],
            datasets: []
        };
    }
};

const formattedChartData = computed(() => {
    clean();
    const device = patient.value.dispositivos.find(device => device.numeroSerie === deviceId.value.numeroSerie);
    if (!device) {
        return chartData.value;
    }
    const colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'pink', 'brown', 'gray', 'black'];
    const data = {
        label: device.sinaisVitais[sinal.value].tipo + "(" + device.sinaisVitais[0].unidade + ")",
        data: device.sinaisVitais[sinal.value].valores.slice(-30).map(entry => entry.valor),
        fill: false,
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.5,
        pointBackgroundColor: device.sinaisVitais[sinal.value].valores.slice(-30).map(entry => {
            if (entry.valor < device.sinaisVitais[sinal.value].minimo || entry.valor > device.sinaisVitais[sinal.value].maximo) {
                return 'red';
            }
            return 'blue';
        })

    }

    chartData.value.datasets.push(data);
    chartData.value.labels = device.sinaisVitais[0].valores.slice(-30).map(entry => new Date(entry.data).toLocaleTimeString());

    return chartData.value;

});

const atualizarGrafico = (index) => {
    clean();

    console.log(index);

    sinal.value = index;


};

const edit = (sns) => {
    router.push({ name: 'PatientEdit', params: { patientSns: sns } });
};

const notificacoes = computed(() => {
    if (!patient.value) {
        return [];
    }
    const notificacoes = [];
    patient.value.dispositivos.forEach(device => {
        device.sinaisVitais.forEach(sign => {
            sign.valores.forEach(value => {
                if (value.valor < sign.minimo || value.valor > sign.maximo)
                    notificacoes.push({
                        dispositivo: device.modelo,
                        sinalVital: sign.tipo,
                        valor: value.valor,
                        data: new Date(value.data).toLocaleString('pt-PT', { timeZone: 'UTC' })
                    });
            });
        });
    });
    return notificacoes;
});

const notificacoesData = ref([]);
const dataTeste = ref([]);

const fetchNotifications = async () => {
    try {
        const response = await fetch(window.URL + '/api/listar_notificacoes/' + patientSns + '/');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        const data = await response.json();
        // explode data by device, vital sign and value

        dataTeste.value = data;
        data.forEach(notification => {
            if (notification.read)
                return;
            let parts = notification.message.split(',');
            notificacoesData.value.push({
                dispositivo: patient.value.dispositivos[parseInt(parts[0].split(':')[1])].modelo,
                sinal: patient.value.dispositivos[parseInt(parts[0].split(':')[1])].sinaisVitais[parseInt(parts[1].split(':')[1])].tipo,
                valor: patient.value.dispositivos[parseInt(parts[0].split(':')[1])].sinaisVitais[parseInt(parts[1].split(':')[1])].valores[parseInt(parts[2].split(':')[1])] ? patient.value.dispositivos[parseInt(parts[0].split(':')[1])].sinaisVitais[parseInt(parts[1].split(':')[1])].valores[parseInt(parts[2].split(':')[1])].valor : 'No value',
                read: notification.read
            });
        });
    } catch (error) {
        console.error(error);
    }
};

const processedNotifications = computed(() => {
    if (!dataTeste.value.length) {
        return []
    }

    return dataTeste.value
        .filter(notification => notification.read === false)
        .sort((a, b) => compareDesc(new Date(a.created_at), new Date(b.created_at)))
        .map(notification => {
            let parts = notification.message.split(',');
            let dispositivoIdx = parseInt(parts[0].split(':')[1].trim());
            let sinalIdx = parseInt(parts[1].split(':')[1].trim());
            let valorIdx = parseInt(parts[2].split(':')[1].trim());
            return {
                dispositivo: patient.value.dispositivos[dispositivoIdx].modelo,
                sinal: patient.value.dispositivos[dispositivoIdx].sinaisVitais[sinalIdx].tipo,
                data: format(new Date(notification.created_at), 'dd-MM-yyyy - HH:mm:ss'),
                valor: patient.value.dispositivos[dispositivoIdx].sinaisVitais[sinalIdx].valores[valorIdx].valor,
                idBotao: notification._id
            };
        });
});


const historyNotifications = computed(() => {
    return dataTeste.value
        .filter(notification => notification.read === true)
        .sort((a, b) => compareDesc(new Date(a.created_at), new Date(b.created_at)))
        .map(notification => {
            let parts = notification.message.split(',');
            let dispositivoIdx = parseInt(parts[0].split(':')[1].trim());
            let sinalIdx = parseInt(parts[1].split(':')[1].trim());
            let valorIdx = parseInt(parts[2].split(':')[1].trim());
            return {
                dispositivo: patient.value.dispositivos[dispositivoIdx].modelo,
                sinal: patient.value.dispositivos[dispositivoIdx].sinaisVitais[sinalIdx].tipo,
                data: format(new Date(notification.created_at), 'dd-MM-yyyy - HH:mm:ss'),
                valor: patient.value.dispositivos[dispositivoIdx].sinaisVitais[sinalIdx].valores[valorIdx].valor
            };
        });
});

const read = async (id) => {
    dataTeste.value.find(notification => notification._id === id).read = true;

    const data = dataTeste.value.find(notification => notification._id === id)
    try {
        const response = await fetch(window.URL + '/api/update_notificacao/' + data._id + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)

        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        else {
            toast.success('Notification read');
        }
    } catch (error) {
        console.error(error);
    }
};

const deleteSinal = async (sinal_idx, dispositivo_idx) => {
    // confirm the deletion
    if (!confirm('Are you sure you want to delete this signal?')) {
        return;
    }
    try {
        const sns = patient.value.sns;
        const response = await fetch(window.URL + '/api/documentos/delete_sinal_vital/' + sns + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dispositivo_idx: dispositivo_idx,
                sinal_idx: sinal_idx
            })

        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        else {
            toast.success('Signal deleted');
            // delete the signal from the local data
            patient.value.dispositivos[dispositivo_idx].sinaisVitais.splice(sinal_idx, 1);
        }
    } catch (error) {
        console.error(error);
    }
};

const deleteDevice = async (index) => {
    // confirm the deletion
    if (!confirm('Are you sure you want to delete this device?')) {
        return;
    }
    try {
        const sns = patient.value.sns;
        const response = await fetch(window.URL + '/api/documentos/delete_device/' + sns + '/', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dispositivo_idx: index
            })

        });
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }
        else {
            toast.success('Device deleted');
            // delete the device from the local data
            patient.value.dispositivos.splice(index, 1);
        }
    } catch (error) {
        console.error(error);
    }
};
</script>

<style scoped>
.tab-border {
    border-bottom: 1px solid #ccc;
}

.patient-card {
    width: 100%;
}
</style>