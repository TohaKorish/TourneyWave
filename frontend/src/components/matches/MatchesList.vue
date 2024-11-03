<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { Game, Match, Status } from 'src/shared.types';
import { useFetch } from 'src/composables/fetch';

import { getStatusColor } from 'src/utils/utils';

import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
import { useRouter } from 'vue-router';

dayjs.extend(relativeTime);

const router = useRouter();


interface Props {
  gameFilter: Game | null;
  status: Status;
}

const props = defineProps<Props>();

const toRelDate = (date: Date) => {
  const start = dayjs(date);
  const now = dayjs();

  return start.from(now, true);
};

const formatedStartTime = (startDate: string) => {
  const alreadyStarted = Date.parse(startDate) < Date.now();

  return alreadyStarted
    ? 'already started'
    : `starts in ${toRelDate(startDate)}`;
};

const matches = ref<Match[]>([]);
const page = ref(1);
const loading = ref(false);
const hasMorePages = ref(true);

const fetchMatches = async (pageNum: number) => {
  if (!hasMorePages.value) return;

  loading.value = true;
  let url = props.gameFilter
    ? `/api/matches?size=20&page=${pageNum}&game_id=${props.gameFilter.id}`
    : `/api/matches?size=20&page=${pageNum}`;

  url = props.status.value == 'all' ? url : url + `&status=${props.status.value}`

  try {
    const data = await useFetch('GET', url);

    if (pageNum === 1) {
      matches.value = data.items;
    } else {
      matches.value = [...matches.value, ...data.items];
    }

    hasMorePages.value = data.items.length === 20;
  } catch (error) {
    console.error('Error fetching matches:', error);
  } finally {
    loading.value = false;
  }
};

const onLoad = async (index: number, done: () => void) => {
  page.value++;
  await fetchMatches(page.value);
  done();
};

// Reset pagination when filter changes
watch(
  [() => props.gameFilter, () => props.status],
  async () => {
    page.value = 1;
    hasMorePages.value = true;
    await fetchMatches(1);
  },
  { deep: true }
);


onMounted(async () => {
  await fetchMatches(1);
});

const handleJoin = (id: number) => {
  router.push(`/matches/${id}`);
};

</script>

<template>
  <q-page>
    <div class="q-pa-md flex justify-center">
      <q-list bordered class="rounded-borders" style="max-width: 800px">
        <q-infinite-scroll @load="onLoad" :disable="!hasMorePages">
          <q-item
            v-for="match in matches"
            :key="match.id"
            class="bg-blue-grey-10 q-mb-md"
            style="min-width: 600px"
          >
            <q-item-section
              class="q-mr-md"
              avatar
              top
              style="
                width: 60px;
                height: 60px;
                overflow: hidden;
                position: relative;
              "
            >
              <img
                :src="match.game.image"
                alt=""
                style="
                  width: 100%;
                  height: 100%;
                  object-fit: cover;
                  position: absolute;
                  top: 0;
                  left: 0;
                "
              />
            </q-item-section>

            <q-item-section top>
              <q-item-label lines="1" class="text-primary">
                <span class="text-weight-medium">{{ match.game.name }}</span>
                <span>
                  - {{ `${match.playersNumber} vs ${match.playersNumber}` }}</span
                >
                <span :class="[getStatusColor(match.status), 'q-ml-md']">
                  {{ match.status }}
                </span>
              </q-item-label>
              <q-item-label caption lines="1" class="text-grey-6">
                {{ formatedStartTime(match.datetime) }}
              </q-item-label>

              <q-item-label
                lines="1"
                class="q-mt-xs text-body2 text-weight-bold text-primary text-uppercase"
              >
                <span @click="handleJoin(match.id)" class="cursor-pointer">Join</span>
              </q-item-label>
            </q-item-section>

            <q-item-section side top>
              <q-item-label lines="1" class="text-primary text-right">
                {{ match.totalTeamsMembers }} / {{ match.totalPlayers }}
              </q-item-label>
            </q-item-section>
          </q-item>

          <template v-slot:loading>
            <div class="row justify-center q-my-md">
              <q-spinner-dots color="primary" size="40px" />
            </div>
          </template>
        </q-infinite-scroll>

        <div v-if="!hasMorePages" class="text-center q-pa-md text-grey-6">
          No more matches to load
        </div>

        <q-separator spaced />
      </q-list>
    </div>
  </q-page>
</template>
