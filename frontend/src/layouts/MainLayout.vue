<script setup>
import { useRouter } from 'vue-router';
import { useJwtStore } from 'stores/jwt-store.js';
import ProfileDropdown from 'components/ProfileDropdown.vue';
import {computed} from "vue";

const router = useRouter()

const handleLoginClick = () => {
  router.push('/login');
}

const handleRegisterClick = () => {
  router.push('/registration');
}

const handleHomeClick = () => {
  router.push('/');
}

const handleToDashboardClick = () => {
  router.push('/dashboard');
}

const jwtStore = useJwtStore();
const isLoggedIn = computed(() => jwtStore.isAuthenticated);
</script>

<template>
  <q-layout class="bg-dark q-pa-none q-ma-none" view="lHh Lpr lFf">
    <q-header class="q-px-md q-py-sm bg-gradient">
      <q-toolbar class="q-gutter-sm items-center">
        <q-btn
          flat
          no-caps
          class="text-h4 text-bold text-primary q-pa-sm"
          @click="handleHomeClick"
        >
          TourneyWave
        </q-btn>

        <q-space />

        <!-- Auth buttons -->
        <div v-if="!isLoggedIn" class="q-gutter-sm">
          <q-btn
            color="primary"
            label="Login"
            no-caps
            size="lg"
            class="q-px-md q-min-width-md"
            @click="handleLoginClick"
          />

          <q-btn
            color="primary"
            label="Register"
            no-caps
            size="lg"
            class="q-px-md q-min-width-md"
            @click="handleRegisterClick"
          />
        </div>



        <div v-if="isLoggedIn" class="q-ml-md self-stretch flex items-center">
          <q-btn
            color="primary"
            label="To dashboard"
            no-caps
            size="lg"
            class="q-px-md q-min-width-md q-mx-md q-pa-md"
            @click="handleToDashboardClick"
          />
          <ProfileDropdown
            class="full-height"
          />
        </div>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer class="bg-gradient q-pa-md">
      <q-toolbar class="justify-center">
        <div class="text-center">
          <q-toolbar-title class="text-caption text-grey-3 q-mb-none">
            &copy; 2024 TourneyWave. All rights reserved.
          </q-toolbar-title>
          <q-btn flat label="Join the wave and rise to the top!" class="text-primary q-mt-xs" />
        </div>
      </q-toolbar>
    </q-footer>
  </q-layout>
</template>

<style>
.bg-gradient {
  background-image: linear-gradient(to right, #374151, #5b21b6);
}
</style>
