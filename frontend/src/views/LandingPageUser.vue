<template>
  <v-container style="margin-top: 50px;" fluid>
    <v-row>
      <v-col cols="12" sm="12" class="mt-n4 text-center">
        <div class="text-h4 text-center">{{ $t('dashboard') }}</div>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4">
        <v-card color="#B49239" theme="dark" class="rounded-xl" height="150">
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-h5 mt-10">
                {{ $t('pacients') }}
              </v-card-title>

              <v-card-subtitle>{{ patients.length }}</v-card-subtitle>
            </div>
            <v-img src="patient.png" class="mr-4 mt-5" width="100" height="100" absolute></v-img>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card color="#C78987" theme="dark" class="rounded-xl" height="150">
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-h5 mt-10">
                {{ $t('devices') }}
              </v-card-title>

              <v-card-subtitle>
                Total: {{ devives?.length }} <br>
                Activos:{{ countDevicesActives }}
              </v-card-subtitle>
            </div>
            <v-img src="smartwatch.png" class="mr-4 mt-5" width="100" height="100" absolute></v-img>
          </div>
        </v-card>
      </v-col>
      <v-col cols="12" sm="4">
        <v-card color="#425C5A" theme="dark" class="rounded-xl" height="150">
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-h5 mt-10">
                {{ $t('sinalVital') }}
              </v-card-title>
              <v-card-subtitle>
                Total: {{ vitalSigns?.length }} <br>
                {{ $t('notifications') }}: {{ valueNotRead }}
              </v-card-subtitle>
            </div>
            <v-img src="pulse.png" class="mr-4 mt-5" width="100" height="100" absolute></v-img>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="data in patientsWithDevicesActives" v-if="patientsWithDevicesActives.length > 0">
        <Line id="id_w" :data="data" :options="chartOptions" />
      </v-col>
      <v-col v-else>
        <v-card color="#425C5A" theme="dark" class="rounded-xl" height="150">
          <div class="d-flex flex-no-wrap justify-space-between">
            <div>
              <v-card-title class="text-h5 mt-10">
                {{ $t('No active devices') }}
              </v-card-title>
            </div>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

</template>

<script setup>
import { computed, onMounted, ref } from 'vue';
import { useLoaderStore } from '@/stores/loader'
import { useUsersStore } from '@/stores/users';
import { Line } from 'vue-chartjs';
import {
  Chart as ChartJS, CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

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
  responsive: true,
  scales: {
    y: {
      beginAtZero: true
    }
  }
};
const user = useUsersStore().user

const loaderStore = useLoaderStore();

onMounted(() => {
  fetchDataFromApi();
});

const patients = ref([]);

const fetchDataFromApi = async () => {
  try {
    loaderStore.setLoading(true);
    const response = await fetch(window.URL + '/api/patients/listar_documentos_com_profissionais/' + user.user_id + '/');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    const data = await response.json();

    patients.value = data;

  } catch (error) {
    console.error(error);
  }
  loaderStore.setLoading(false);
};

const devives = computed(() => {
  const dispositivos = ref([]);
  patients.value.forEach((patient) => {
    patient.dispositivos.forEach((dispositivo) => {
      if (!dispositivos.value.includes(dispositivo)) {
        dispositivos.value.push(dispositivo);
      }
    });
  });
  return dispositivos.value;
});

const vitalSigns = computed(() => {
  const sinaisVitais = ref([]);
  patients.value.forEach((patient) => {
    patient.dispositivos.forEach((dispositivo) => {
      dispositivo.sinaisVitais.forEach((sinalVital) => {
        sinalVital.valores.forEach((valor) => {
          if (!sinaisVitais.value.includes(valor)) {
            sinaisVitais.value.push(valor);
          }
        });
      });
    });
  });
  return sinaisVitais.value;
});
const dadosPacientes = ref([]);
const valueNotRead = computed(() => {
  let count = 0;
  patients.value.forEach((patient) => {
    patient.dispositivos.forEach((dispositivo) => {
      dispositivo.sinaisVitais.forEach((sinalVital) => {
        sinalVital.valores.forEach((valor) => {
          if (valor.alerta === true) {
            dadosPacientes.value.push({
              nome: patient.nome,
              sns: patient.sns,
              dispositivo: dispositivo.modelo,
              sinalVital: sinalVital.tipo,
              valor: valor.valor,
              data: valor.data,

            });
            count++;
          }
        });
      });
    });
  });
  // os 5 mais recentes por data from dadosPacientes
  dadosPacientes.value.sort((a, b) => {
    return new Date(b.data) - new Date(a.data);
  });
  dadosPacientes.value = dadosPacientes.value.slice(0, 5);

  return count;
});

// count all devices actives
const countDevicesActives = computed(() => {
  let count = 0;
  patients.value.forEach((patient) => {
    patient.dispositivos.forEach((dispositivo) => {
      if (dispositivo.ativo) {
        count++;
      }
    });
  });
  return count;
});

// get all patients with devices actives
const patientsWithDevicesActives = computed(() => {
  const dataForGraph = [];
  patients.value.forEach((patient) => {
    try {
        const ws = new WebSocket('ws://' + useLoaderStore().url + '/ws/pacient/room' + patient.sns + '/');
        ws.onopen = () => {
            console.log('Connected to the websocket server')
        }
        ws.onmessage = (event) => {
          fetchDataFromApi();
        }
    } catch (error) {
        console.error(error);
    }
    patient.dispositivos.forEach((dispositivo) => {
      if (dispositivo.ativo) {
        dispositivo.sinaisVitais.forEach((sinalVital) => {
          if (sinalVital.ativo === false) {
            return;
          }
          dataForGraph.push({
              labels: sinalVital.valores.slice(-30).map(entry => new Date(entry.data).toLocaleTimeString()),
              datasets: [
                {
                  label: sinalVital.tipo,
                  backgroundColor: 'rgba(75, 192, 192, 0.2)',
                  borderColor: 'rgba(75, 192, 192, 1)',
                  borderWidth: 1,
                  data: sinalVital.valores.slice(-30).map(entry => entry.valor)
                }
              ]
            });
        });
      }
    });
  });
  return dataForGraph
});




</script>