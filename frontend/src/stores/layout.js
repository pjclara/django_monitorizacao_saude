import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useLayoutStore = defineStore('layout', () => {
    const showSidebar = ref(false)

    const toggleSidebar = () => {
        showSidebar.value = !showSidebar.value;
     }
    return { showSidebar, toggleSidebar }
})
