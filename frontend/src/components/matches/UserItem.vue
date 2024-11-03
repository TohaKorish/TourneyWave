<script setup lang="ts">
import { Player } from 'src/shared.types';
import { computed } from 'vue';
import { useProfile } from 'stores/profile-store';

const props = defineProps<{
  player: Player
}>();

const profileStore = useProfile();

const getRating = (player: Player): number => {
  console.log(player);
  if (!player.userGames) {
    return 100;
  }

  if (player.userGames.length == 0) {
    return 100;
  }

  return player.userGames[0].rating;
};

const isCurrentUser = computed(() => {
  return profileStore.profile.id == props.player.id;
});
</script>

<template>
  <q-item-section>
    <q-item-label :class="{ 'text-primary': isCurrentUser }" lines="5">
      <span class="text-bold">{{ props.player.username }}</span> <span class="text-white q-pl-lg">rating: {{getRating(props.player)}}</span>
    </q-item-label>
  </q-item-section>
</template>

<style scoped>
</style>
