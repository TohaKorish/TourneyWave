<template>
  <router-view />
</template>

<script lang="ts">
import { defineComponent, onMounted } from 'vue';
import { useJwtStore } from 'stores/jwt-store.js';


export default defineComponent({
  name: 'App'
});
</script>
