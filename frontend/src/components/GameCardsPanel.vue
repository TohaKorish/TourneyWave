<script setup lang="ts">

import { onMounted, ref } from 'vue';
import { Game } from 'src/shared.types';
import { useFetch } from 'src/composables/fetch';
import { useRouter } from 'vue-router';

const router = useRouter();

const games = ref<Game[]>();

onMounted(async () => {
  const data = await useFetch('GET', '/api/games?size=5')

  games.value = data.items

});

const handleCardClick = (id: number) => {
  router.push('/matches?filterId=' + id)

}


</script>

<template>
  <div class="q-pa-md">
    <div class="q-gutter-x-md row">
      <q-card
        @click="handleCardClick((g.id))"
        class="my-card col"
        v-for="g in games"
        :key="g.id">
        <q-img
          :src="g.image"
          class="q-card__media fit-cover"
          style="height: 500px;">
          <div class="absolute-bottom text-subtitle2 text-center"> {{ g.name }}</div>
        </q-img>
      </q-card>
    </div>
  </div>
</template>


<style scoped></style>
