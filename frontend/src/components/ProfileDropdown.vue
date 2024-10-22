<script setup lang="ts">
import { useRouter } from 'vue-router';
import { useProfile } from 'stores/profile-store';
import { useJwtStore } from 'stores/jwt-store.js';
import { onMounted, ref } from 'vue';
import { Profile } from 'src/shared.types';

const profile = ref<Profile>(null);

const router = useRouter();
const profileStore = useProfile();
const jwtStore = useJwtStore();

onMounted(() => {
  profile.value = profileStore.profile;
});

const logout = () => {
  jwtStore.removeToken();
  profileStore.remove()
  router.push('/login');
};
</script>

<template>
  <div class="q-pa-md flex flex-center">
    <q-btn-dropdown
      color="primary"
      :label="'Привіт, ' + (profile?.username || 'Guest') + ' !!!'"
      glossy
      class="text-h5"
      no-caps
      content-class="bg-secondary"
      style="min-height: 60px; min-width: 200px;"
    >
      <q-list>
        <q-item clickable v-close-popup @click="logout">
          <q-item-section avatar>
            <q-icon name="exit_to_app" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Logout</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </q-btn-dropdown>
  </div>
</template>

<style scoped></style>
