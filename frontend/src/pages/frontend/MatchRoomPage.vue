<script setup lang="ts">
import UsersList from 'components/matches/UsersList.vue';
import { computed, onMounted, ref } from 'vue';
import { useFetch } from 'src/composables/fetch';
import { useRoute, useRouter } from 'vue-router';
import { Match, Player, Profile } from 'src/shared.types';
import { Notify } from 'quasar';
import { useProfile } from 'stores/profile-store';

const route = useRoute();
const router = useRouter();

const match = ref<Match | null>(null);

onMounted(() => {
  const id = route.params.id;

  useFetch('GET', '/api/matches/' + id)
    .catch(() => router.push({ name: 'not-found' }))
    .then((resp) => {
      match.value = resp;
      console.log(match.value);
      console.log("match.value");
    });
});

const team1 = computed(() => {
  return match.value?.teams[0];
});
const team2 = computed(() => {
  return match.value?.teams[1];
});

const winnerId = computed(() => {
  return match.value?.winnerTeamId;
});

const handlePlayerAdd = (profile: Player, listName: string): void => {
  if (match.value?.winnerTeamId) {
    Notify.create({
      message: 'Game already ended',
      position: 'top',
    });
    return;
  }

  const newTeam = match.value?.teams.find((t) => t.name == listName);
  const oldTeam = match.value?.teams.find((t) => t.name != listName);

  let player = oldTeam?.members.find((member) => member.id == profile.id);

  if (! player) {
    console.log(profile.userGames);
    profile.userGames = profile.userGames.filter((ug) => ug.gameId == match.value?.game.id);
    player = profile;
  }

  newTeam.members.push(player);
  oldTeam.members = oldTeam.members.filter((p) => p.id !== player.id);

  useFetch('PATCH', `/api/matches/join-team/${match.value?.id}`, {
    match_id: match.value?.id,
    team_id: newTeam.id,
    user_id: player.id,
  });
};

const profileStore = useProfile();
const showWinnerForm = ref<boolean>(false);
const handleSelectWinner = (): void => {
  const profile: Profile = profileStore.profile;

  if (profile.id != match.value?.ownerId || profile.role == 'user') {
    Notify.create({
      message: "You are not authorized to select winner.",
      position: 'top'
    });

    return;
  }

  if (match.value?.winnerTeamId || match.value.status != 'in progress') {
    Notify.create({
      message: "Can not assign winner.",
      position: 'top'
    });

    return;
  }

  showWinnerForm.value = !showWinnerForm.value;
};
const winnerOptions = computed(() => {
  return match.value?.teams.map((t) => t.name);
});
const winnerTeam = ref<string>('Team 1');


const handleWinnerSelect = (): void => {
  const team = match.value?.teams.find((t) => t.name == winnerTeam.value);

  const matchId = match.value?.id;
  const teamId = team?.id;

  useFetch('PATCH', `/api/matches/complete/${matchId}/${teamId}`).catch((err) => {
    Notify.create({
      message: err.message,
      position: 'top',
      color: "negative"
    });
  }).then(() => {
    match.value.winnerTeamId = teamId;
  });

};


const formatDate = (date: Date) => {
  return new Date(date).toLocaleString();
};
</script>
<template>
  <q-page>
    <!-- Dark top banner with match info -->
    <div class="match-info-banner q-px-md q-py-sm">
      <div class="row items-center q-gutter-x-md">
        <q-avatar size="45px">
          <q-img :src="match?.game.image" :alt="match?.game.name" />
        </q-avatar>

        <div>
          <div class="text-white text-weight-medium text-h6">
            {{ match?.game.name }}
          </div>
          <div class="row q-gutter-x-md items-center q-mt-xs">
            <q-badge class="text-caption">
              {{ match?.status }}
            </q-badge>
            <div class="row items-center text-grey-5 text-caption">
              <q-icon name="people" size="16px" class="q-mr-xs" />
              {{ match?.totalPlayers }} players
            </div>
            <div class="row items-center text-grey-5 text-caption">
              <q-icon name="event" size="16px" class="q-mr-xs" />
              {{ formatDate(match?.datetime) }}
            </div>
          </div>
        </div>
      </div>

      <div class="q-mt-sm">
        <div class="text-white text-weight-medium">Connection Information</div>
        <div class="text-grey-4 text-caption">
          <div><strong>Key:</strong> {{ match?.connectionKey }}</div>
          <div>
            <strong>Description:</strong> {{ match?.connectionDescription }}
          </div>
          <div v-if="match?.streamUrl">
            <strong>Stream URL:</strong>
            <a :href="match.streamUrl" target="_blank">{{ match.streamUrl }}</a>
          </div>
        </div>
      </div>
    </div>

    <div class="teams-container q-px-md q-mt-md">
      <div class="row justify-between">
        <div class="team-list-width">
          <UsersList
            :isWinner="winnerId == team1?.id"
            :playersNumber="match?.playersNumber"
            @player-add="handlePlayerAdd"
            :list-name="team1?.name"
            :users="team1?.members"
          />
        </div>
        <div class="team-list-width">
          <UsersList
            :isWinner="winnerId == team2?.id"
            :playersNumber="match?.playersNumber"
            @player-add="handlePlayerAdd"
            :list-name="team2?.name"
            :users="team2?.members"
          />
        </div>
      </div>
      <q-btn
        label="Select winner"
        @click="handleSelectWinner"
        class="q-mt-md"
        color="primary"
      />
    </div>

    <q-dialog v-model="showWinnerForm" persistent>
      <q-card style="min-width: 350px" class="bg-blue-grey-10 text-white">
        <q-card-section>
          <div class="text-h6">Who  won the match ?</div>
        </q-card-section>

        <q-card-section class="q-pt-none">
          <q-select
            dense
            label="Choose winner"
            label-color="primary"
            color="primary"
            text-color="white"
            v-model="winnerTeam"
            :options="winnerOptions"
            options-dense
            option-color="grey-9"
            option-bg-color="blue-grey-9"
            popup-content-class="bg-blue-grey-9 text-white"
            @keyup.enter="showWinnerForm = false"
          />
        </q-card-section>

        <q-card-actions align="right" class="text-primary">
          <q-btn flat label="Cancel" v-close-popup />
          <q-btn flat label="Select" v-close-popup @click="handleWinnerSelect" />
        </q-card-actions>
      </q-card>
    </q-dialog>

  </q-page>
</template>

<style scoped>
.match-info-banner {
  background-color: #2a3942;
}

.team-list-width {
  width: 48%; /* Adjust this value to match exact spacing */
}

:deep(.user-list-container) {
  max-width: none;
}

span {
  color: white !important;
}
</style>
