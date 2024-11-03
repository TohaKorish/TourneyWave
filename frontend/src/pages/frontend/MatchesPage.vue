<script setup lang="ts">
import MatchesList from 'components/matches/MatchesList.vue';
import GamesSelect from 'components/GamesSelect.vue';
import { Game, Status } from 'src/shared.types';
import { ref, watch } from 'vue';
import MatchesForm from 'components/matches/MatchesForm.vue';
import { useRoute, useRouter } from 'vue-router';

const game = ref<Game | null>(null);
const showForm = ref<boolean>(false);

const toggleForm = (): void => {
  showForm.value = !showForm.value;

};

const selectedStatus = ref<Status>({ label: 'All', value: 'all' });

const statusOptions: Status[] = [
  { label: 'All', value: 'all' },
  { label: 'Open', value: 'open' },
  { label: 'Canceled', value: 'canceled' },
  { label: 'Completed', value: 'completed' },
  { label: 'In progress', value: 'In progress' }
];

const route = useRoute();
const router = useRouter();


const handleSelect = async (newGame: Game) => {

  const query = { ...route.query };

  if (newGame) {
    query.filterId = newGame.id;
  } else {
    delete query.filterId;
  }

  await router.replace({ query });

  game.value = newGame;
};

</script>

<template>
  <q-page class="q-pa-lg">
    <div class="row justify-center items-center">
      <GamesSelect class="q-pl-lg q-pb-md" @select-update="handleSelect"/>

      <div class="q-px-lg">
        <div class="text-pink-5 q-mb-sm">
          Status
        </div>
        <q-select
          v-model="selectedStatus"
          :options="statusOptions"
          use-input
          hide-dropdown-icon
          style="width: 250px"
          dark
          color="pink-6"
          standout="bg-blue-grey-9"
          input-style="color: white"
          menu-style="background-color: #1d1d2d"
          popup-content-style="background-color: #1d1d2d"
          :rules="[val => !!val || 'Status is required']"

        >
          <template v-slot:prepend>
            <q-icon name="filter_list" color="pink-5" />
          </template>
        </q-select>
      </div>
    </div>

    <MatchesList :game-filter="game" :status="selectedStatus"/>

    <MatchesForm :is-showing="showForm" @form-close="toggleForm"/>

    <q-page-sticky position="bottom-right" :offset="[18, 18]">
      <q-btn
        fab
        icon="add"
        color="primary"
        @click="toggleForm"
        size="lg"
        class="shadow-10 q-transition transform hover-scale"
      />
    </q-page-sticky>
  </q-page>
</template>

<style scoped>

</style>
