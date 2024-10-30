<script setup lang="ts">
import {  useRouter } from 'vue-router';
import GameCardsPanel from 'components/GameCardsPanel.vue';

const router = useRouter();

</script>

<template>
  <q-page class="q-pa-lg">
    <GameCardsPanel/>
  </q-page>
</template>
