<script setup lang="ts">
import { useRouter } from 'vue-router';
import GameCardsPanel from 'components/GameCardsPanel.vue';
import { useProfile } from 'stores/profile-store';
import { onMounted, ref } from 'vue';
import { useFetch } from 'src/composables/fetch';

const router = useRouter();

const handleShowAllGames = () => {
  router.push('/matches');
};

const profileStore = useProfile();

type Row = {
  name: string;
  image: string;
  rating: number;
};

const columns = ref([
  { name: 'image', label: 'Image', align: 'left', field: 'image' },
  { name: 'name', label: 'Game Name', align: 'left', field: 'name' },
  { name: 'rating', label: 'Rating', align: 'center', field: 'rating' },
]);

const playerGames = ref<Row[]>([]);

onMounted(async () => {

  const profile = await useFetch('GET', '/api/users/me');

  const rows = profile.userGames.map((ug) => {
    const row: Row = {
      name: ug.game.name,
      image: ug.game.image,
      rating: ug.rating,
    };
    return row;
  });
  playerGames.value = rows;
});
</script>

<template>
  <q-page class="q-pa-lg">
    <GameCardsPanel />

    <div class="flex justify-center">
      <q-btn
        label="Show all games"
        @click="handleShowAllGames"
        class="q-mt-md"
        color="primary"
      />
    </div>

    <q-page class="q-pa-md">
      <q-table
        :rows="playerGames"
        :columns="columns"
        row-key="name"
        flat
        dense
        hide-pagination
        square
        class="custom-table"
      >
        <template v-slot:body-cell-image="props">
          <q-img :src="props.row.image" style="width: 50px; height: 50px; border-radius: 5px;" />
        </template>
      </q-table>
    </q-page>
  </q-page>
</template>

<style scoped>
.custom-table {
  background-color: var(--q-dark-page-bg); /* Match your dark theme background */
  color: white; /* Ensures readability */
}

.q-table__title, .q-table__cell {
  color: inherit; /* Matches with the rest of your page's text color */
}
</style>
