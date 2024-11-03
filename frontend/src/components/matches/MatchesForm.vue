<script setup lang="ts">
import { ref, watch } from 'vue';
import GamesSelect from 'components/GamesSelect.vue';
import { Game } from 'src/shared.types';
import { useProfile } from 'stores/profile-store';
import { useFetch } from 'src/composables/fetch';
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';

interface Props {
  isShowing: boolean;
}

const game = ref<Game | null>(null);
const playersNumber = ref<number>(null);
const connectionKey = ref<string>('');
const connectionDescription = ref<string>('');
const streamUrl = ref<string>('');
const startDate = ref<string>('');
const startTime = ref<string>('');

const emit = defineEmits(['form-close']);
const props = defineProps<Props>();
const toggled = ref<boolean>(false);

const showOtherFields = ref<boolean>(false);

const handleClose = (): void => {
  emit('form-close');
};

watch(
  () => props.isShowing,
  (newValue) => {
    toggled.value = newValue;
  }
);

watch(toggled, (newValue) => {
  if (!newValue) handleClose();
});

const handleGameSelect = (newGame: Game): void => {
  showOtherFields.value = true;
  game.value = newGame;
};

const getFullDateTime = (): string => {
  if (!startDate.value || !startTime.value) return '';
  return `${startDate.value}T${startTime.value}`;
};

const profileStore = useProfile();

const router = useRouter();

const submitForm = (): void => {
  const fullDateTime = getFullDateTime();
  const now = new Date();
  const tenMinutesFromNow = new Date(now.getTime() + 10 * 60000);

  if (new Date(fullDateTime) < tenMinutesFromNow) {
    Notify.create({
      message: 'The game must be created at least for 10 minutes in advance',
      position: 'top',
      color: 'negative',
    });
    return;
  }

  const body = {
    game_id: game.value?.id,
    datetime: fullDateTime,
    connection_description: connectionDescription.value,
    connection_key: connectionKey.value,
    stream_url: streamUrl.value,
    players_number: playersNumber.value,
    owner_id: profileStore.profile.id,
  };

  useFetch('POST', '/api/matches', body)
    .then((response) => {
      Notify.create({
        message: 'Success',
        position: 'top',
        color: 'positive',
      });


      game.value = null;
      playersNumber.value = null;
      connectionKey.value = '';
      connectionDescription.value = '';
      streamUrl.value = '';
      startDate.value= '';
      startTime.value = '';

      router.push(`/matches/${response.id}`);
    })
    .catch((err) => {
      Notify.create({
        message: err.message,
        position: 'top',
        color: 'negative',
      });
    });
};
</script>

<template>
  <q-dialog v-model="toggled">
    <q-card class="bg-blue-grey-10" style="width: 450px; max-width: 90vw">
      <form @submit.prevent="submitForm" ref="formRef">
        <q-card-section class="row items-center q-pb-none">
          <div class="text-h6 text-pink-5">Create Match</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup color="pink-5" />
        </q-card-section>

        <q-card-section>
          <GamesSelect @select-update="handleGameSelect" />
        </q-card-section>

        <q-card-section v-if="showOtherFields">
          <q-select
            v-model="playersNumber"
            :options="game?.participantCount"
            label="Players in Team *"
            dark
            color="pink-6"
            standout="bg-dark"
            class="q-mb-md"
            popup-content-style="background-color: #1d1d2d"
            :rules="[(val) => !!val || 'Players count is required']"
            error-message="Please select players count"
            bottom-slots
          >
            <template v-slot:error>
              <div class="text-negative">Players count is required</div>
            </template>
          </q-select>

          <div class="row q-col-gutter-md">
            <div class="col-12 col-sm-6">
              <q-input
                v-model="startDate"
                label="Start Date *"
                dark
                color="pink-6"
                standout="bg-blue-grey-9"
                class="q-mb-md"
                :rules="[(val) => !!val || 'Start date is required']"
                bottom-slots
              >
                <template v-slot:error>
                  <div class="text-negative">Start date is required</div>
                </template>
                <template v-slot:append>
                  <q-icon name="event" color="pink-5">
                    <q-popup-proxy
                      cover
                      transition-show="scale"
                      transition-hide="scale"
                    >
                      <q-date
                        v-model="startDate"
                        mask="YYYY-MM-DD"
                        color="pink-5"
                        dark
                        minimal
                      >
                        <div class="row items-center justify-end q-gutter-sm">
                          <q-btn
                            label="Close"
                            color="pink-5"
                            flat
                            v-close-popup
                          />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
            <div class="col-12 col-sm-6">
              <q-input
                v-model="startTime"
                label="Start Time *"
                dark
                color="pink-6"
                standout="bg-blue-grey-9"
                class="q-mb-md"
                :rules="[(val) => !!val || 'Start time is required']"
                bottom-slots
              >
                <template v-slot:error>
                  <div class="text-negative">Start time is required</div>
                </template>
                <template v-slot:append>
                  <q-icon name="schedule" color="pink-5">
                    <q-popup-proxy
                      cover
                      transition-show="scale"
                      transition-hide="scale"
                    >
                      <q-time
                        v-model="startTime"
                        mask="HH:mm"
                        format24h
                        color="pink-5"
                        dark
                      >
                        <div class="row items-center justify-end q-gutter-sm">
                          <q-btn
                            label="Close"
                            color="pink-5"
                            flat
                            v-close-popup
                          />
                        </div>
                      </q-time>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
          </div>

          <q-input
            v-model="connectionKey"
            label="Connection Key *"
            maxlength="255"
            dark
            color="pink-6"
            standout="bg-blue-grey-9"
            class="q-mb-md"
            :rules="[(val) => !!val || 'Connection key is required']"
            bottom-slots
          >
            <template v-slot:error>
              <div class="text-negative">Connection key is required</div>
            </template>
          </q-input>

          <q-input
            v-model="connectionDescription"
            type="textarea"
            label="Connection Description"
            maxlength="500"
            autogrow
            dark
            color="pink-6"
            standout="bg-blue-grey-9"
            class="q-mb-md"
            hint="Additional information about the connection"
            :rules="[(val) => !!val || 'Connection Description is required']"
          />

          <q-input
            v-model="streamUrl"
            label="Stream URL (optional)"
            maxlength="255"
            dark
            color="pink-6"
            standout="bg-blue-grey-9"
            class="q-mb-md"
            hint="Link to stream if available"
          />
        </q-card-section>

        <q-card-section class="text-center">
          <q-btn
            type="submit"
            color="pink-5"
            label="CREATE"
            class="q-px-xl q-py-sm text-bold"
          />
        </q-card-section>
      </form>
    </q-card>
  </q-dialog>
</template>

<style scoped>
.q-field--standout.q-field--dark.q-field--highlighted >>> .q-field__control {
  background-color: #383c42 !important;
}

.q-field--standout.q-field--dark.q-field--highlighted >>> .q-field__native {
  color: white !important;
}
</style>
