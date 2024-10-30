<script setup lang="ts">
import MatchesList from 'components/matches/MatchesList.vue';
import GamesSelect from 'components/GamesSelect.vue';
import { Game } from 'src/shared.types';
import { ref } from 'vue';

const game = ref<Game | null>(null);

const handleSelect = (newGame: Game) => {
  game.value = newGame;
};

</script>

<template>
  <q-page class="q-pa-lg">
    <GamesSelect @select-update="handleSelect"/>

    <MatchesList :game-filter="game"/>
  </q-page>
</template>

<style scoped>

</style>
