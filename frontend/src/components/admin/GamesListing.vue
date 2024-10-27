<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';
import { Game } from 'src/shared.types';
import { useFetch } from 'src/composables/fetch';

const columns = ref([
  { name: 'id', required: true, label: 'Id', align: 'left', field: 'id' },
  { name: 'name', required: true, label: 'Name', align: 'left', field: 'name' },
  { name: 'Participant number', align: 'left', label: 'Participant number', field: 'participantCount',
    format: (val, row) => `${val.join('/')}`,
  },
  { name: 'image', align: 'left', label: 'Image', field: 'image' },
]);

const rows = ref<Game[]>([]);
const pagination = ref({ page: 1, rowsPerPage: 5 });

const handleRequest = async (update) => {
  pagination.value.page = update.pagination.page;
  pagination.value.rowsPerPage = update.pagination.rowsPerPage;

  await fetchGames();

};

async function fetchGames() {

  const size = pagination.value.rowsPerPage;
  const page = pagination.value.page;

  const data = await useFetch('GET', `/api/games?size=${size}&page=${page}`);
  rows.value = data.items

  pagination.value.rowsNumber = data.total;
}

onMounted(async () => {
  await fetchGames();
})

const router = useRouter()

const selected = ref([]);

const showDeleteConfirm = ref<boolean>(false);


const handleEdit = () => {
  if (! selected.value.length) {
    Notify.create({
      message: 'No game selected !',
      position: 'top',
    })

    return
  }

  const selectedId = selected.value.pop().id;

  router.push(`/admin/games/edit/${selectedId}`)
}


const handleDelete = () => {

  if (! selected.value.length) {
    Notify.create({
      message: 'No game selected !',
        position: 'top',
    })

    return
  }

  showDeleteConfirm.value = ! showDeleteConfirm.value

}

const handleDeleteConfirm = async () => {
  const game: Game = selected.value.pop()

  await useFetch('DELETE', `/api/games/${game.id}`).then( async () => {
    Notify.create({
      message: 'Game deleted !',
      color: 'positive',
      position: 'top',
    })

    await fetchGames();
    }
  ).catch((err) => {
    Notify.create({
      message: err.message,
      color: 'warning',
      position: 'top',
    })
  });


}


const handleNew = () => {
  router.push(`/admin/games/new`);
}

</script>

<template>
  <div>
    <div class="row justify-between q-ma-md">
      <div class="row justify-around">
        <q-btn class="q-mr-md" label="Edit" color="primary" @click="handleEdit"/>
        <q-btn label="Delete" color="primary" @click="handleDelete"/>
      </div>
      <div>
        <q-btn label="New" color="primary" @click="handleNew"/>
      </div>
    </div>


    <q-dialog v-model="showDeleteConfirm" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="primary" text-color="white" />
          <span class="q-ml-sm">Are you sure, you want to delete the game</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn flat label="Sure" color="primary" v-close-popup @click="handleDeleteConfirm" />
        </q-card-actions>
      </q-card>
    </q-dialog>

    <q-table
      @request="handleRequest"
      :rows="rows"
      :columns="columns"
      v-model:pagination="pagination"
      row-key="id"
      selection="single"
      v-model:selected="selected"
      flat
      bordered
      class="my-sticky-header-table"
    >
      <template v-slot:body-cell-image="props">
        <q-td :props="props">
          <div>
            <img :src="props.row.image" style="max-width: 50px" />
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<style scoped></style>
