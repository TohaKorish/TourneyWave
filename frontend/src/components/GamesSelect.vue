<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { Game } from 'src/shared.types';
import { useFetch } from 'src/composables/fetch';
import { useRoute, useRouter } from 'vue-router';
import { debounce } from 'quasar';

const route = useRoute();
const router = useRouter();

const emit = defineEmits(['selectUpdate']);

const selectedOption = ref<Game | null>(null);
const options = ref<Game[]>([]);
const searchTerm = ref('');

watch(selectedOption, async (newOpt, oldOpt) => {
  emit('selectUpdate', newOpt);

  const query = { ...route.query };

  if (newOpt) {
    query.filterId = newOpt.id;
  } else {
    delete query.filterId;
  }

  await router.replace({ query });
});

onMounted(async () => {
  const data = await useFetch('GET', '/api/games?size=5');
  options.value = data.items;
  console.log(options.value);
  console.log("options.value");

  const filterId = route.query.filterId;

  if (filterId) {
    selectedOption.value = options.value.find(
      (option) => option.id === Number(filterId)
    );
  }
});


const fetchOptions = debounce(async (val) => {
  const data = await useFetch('GET', `/api/games?size=5&search=${val}`);
  options.value = data.items;
}, 300);

function filterOptions(val: string, update: () => void) {
  searchTerm.value = val;
  if (val.length >= 2) {
    fetchOptions(val);
  }
  update();
}

</script>

<template>
  <div class="row justify-center">
    <q-select
      v-model="selectedOption"
      :options="options"
      use-input
      clearable
      option-value="value"
      option-label="label"
      hide-dropdown-icon
      @filter="filterOptions"
      style="width: 250px"
      dark
      color="pink-6"
      standout="bg-blue-grey-9"
      input-style="color: white"
      menu-style="background-color: #1d1d2d"
      popup-content-style="background-color: #1d1d2d"
    >
      <template v-slot:prepend>
        <q-icon name="search" color="pink-5" />
      </template>

      <template v-slot:option="scope">
        <q-item v-bind="scope.itemProps">
          <q-item-section avatar>
            <q-avatar size="24px" square>
              <img :src="scope.opt.image" />
            </q-avatar>
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ scope.opt.name }}</q-item-label>
          </q-item-section>
        </q-item>
      </template>

      <template v-slot:selected>
        <div v-if="selectedOption" class="row items-center">
          <q-avatar size="24px" square class="q-mr-sm">
            <img :src="selectedOption.image" />
          </q-avatar>
          {{ selectedOption.name }}
        </div>
      </template>
    </q-select>
  </div>
</template>
