<template>
    <v-card variant="outlined" color="surface-variant">
        <v-card-title> 
            <v-row>
                <v-col cols="6">
                    <h2> {{ $t('Pacient') }} (dinamico)</h2>
                </v-col>
                <v-col cols="6" class="text-end">
                    <v-chip color="blue" variant="outlined" label>
                        <span> 3 {{ $t('daysAgo') }} (dinamico)</span>
                    </v-chip>
                </v-col>
            </v-row>
        </v-card-title>
        <v-card-text class="mt-4">
            <h3>
                Test message with the problem (dinamico)
            </h3>
        </v-card-text>
        <v-card-actions class="justify-end">
            <v-btn variant="outlined" color="blue-darken-4">
                {{ $t('viewProfile') }}
            </v-btn>
        </v-card-actions>
    </v-card>
</template>

<script setup>

</script>

<style scoped>

</style>