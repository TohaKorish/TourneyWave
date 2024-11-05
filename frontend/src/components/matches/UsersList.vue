<script setup lang="ts">
import { Player, Profile, User } from 'src/shared.types';
import UserItem from 'components/matches/UserItem.vue';
import { useProfile } from 'stores/profile-store';
import { Notify } from 'quasar';
import { useFetch } from 'src/composables/fetch';

const props = defineProps<{
  listName: string;
  playersNumber: number;
  selectedUser?: Player | null;
  users: Player[];
  isWinner: boolean;
}>();

const emits = defineEmits(['playerAdd']);

const profileStore = useProfile();

const handleListClick = async (): void => {
  const id = profileStore.profile.id;

  const player = props.users.find((player) => player?.id == id);

  if (player) {
    Notify.create({
      message: 'The player is already in this team',
      position: 'top',
    });

    return;
  }

  if (props.users?.length == props.playersNumber) {
    Notify.create({
      message: 'Team is full',
      position: 'top',
    });
    return;
  }
  const profile: Profile = await useFetch('GET', '/api/users/me');
  emits('playerAdd', profile, props.listName);

};
</script>
<template>
  <div
    @click="handleListClick"
    class="bg-blue-grey-10 rounded-borders cursor-pointer"
  >
    <q-list>
      <q-item-label header class="text-white flex justify-between items-center">
        <div>{{ props.listName }} <span v-if="props.isWinner" class="text-primary">(Winner)</span></div>
        <span class="text-gray-300">{{`${props.users?.length} / ${props.playersNumber}`}}</span>
      </q-item-label>

      <q-item v-for="user in props.users" :key="user.id" class="text-white">
        <UserItem :player="user" />
      </q-item>
    </q-list>
  </div>
</template>
