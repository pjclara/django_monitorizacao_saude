<template>
    <v-list style="background-color: inherit;">
        <v-list-item v-for="(item, index) in paginatedData" :key="index" class="mb-2">
            <v-row v-for="(key, i) in keys" :key="i">
                <!-- Esquerda -->
                <div style="width: 35%;">
                    <v-col class="d-flex align-center">
                        <p class="font-weight-bold">{{ capitalizeFirstLetter(key) }}</p>
                    </v-col>
                </div>

                <!-- Direita -->
                <v-col class="d-flex justify-center" v-if="key === 'idBotao'">
                    <v-btn color="blue" size="small" @click="read(item.id)">Visto</v-btn>
                </v-col>
                <v-col class="d-flex justify-center" v-else-if="key==='is_active'"> 
                    <v-icon v-if="item.is_active" class="green">mdi-check-circle</v-icon>
                    <v-icon v-else class="red">mdi-close-circle</v-icon>
                </v-col>
                <v-col class="d-flex justify-center" v-else-if="key==='actions'"> 
                    <v-btn v-if="isUser" color="blue" size="small" @click="editUser(item)">{{ $t('EditUser') }}</v-btn>
                </v-col>
                <v-col class="d-flex justify-center" style="line-break: anywhere;" v-else> 
                    <p>{{ item[key] }}</p>
                </v-col>
            </v-row>
        </v-list-item>
    </v-list>
    <v-pagination
      v-model:page="currentPage"
      :length="totalPages"
      circle
    ></v-pagination>
</template>

<script setup>
import {ref,computed} from 'vue'
import router from '@/router';


const props = defineProps(['data', 'keys', 'isUser'])

const itemsPerPage = ref(5);
const currentPage = ref(1);

const totalPages = computed(() => {
    return Math.ceil(props.data.length / itemsPerPage.value);
});

const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return props.data.slice(start, end);
});

function capitalizeFirstLetter(string) {
    if (string.length === 0) {
        return string;
    }
    return string.charAt(0).toUpperCase() + string.slice(1);
}

const editUser = (item) => {
    router.push({ name: 'EditUser', params: { id: item.id } })
}

</script>

<style scoped>

.v-list-item{
    padding: 1rem !important;
    border: 2px solid blue;
    border-radius: 6px;
}

</style>