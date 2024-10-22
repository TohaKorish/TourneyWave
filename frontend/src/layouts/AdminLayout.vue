<script setup lang="ts">
import { computed, ref } from 'vue';
import EssentialLink from 'components/EssentialLink.vue';
import ProfileDropdown from 'components/ProfileDropdown.vue';
import { useJwtStore } from 'stores/jwt-store.js';


const leftDrawerOpen = ref(false)

const jwtStore = useJwtStore();
const isAuthenticated = computed(() => jwtStore.isAuthenticated);

const linksList = [

  {
    title: 'Tab1',
    caption: 'Tab1',
    icon: 'dashboard',
    link: '/'
  },
  {
    title: 'Tab2',
    caption: 'Tab2',
    icon: 'list',
    link: '/sessions'
  }
];

const toggleLeftDrawer = () => {
  leftDrawerOpen.value = !leftDrawerOpen.value
}

</script>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated >
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="toggleLeftDrawer"
        />

        <q-toolbar-title >
          TourneyWave
        </q-toolbar-title>
        <ProfileDropdown v-if="isAuthenticated"></ProfileDropdown>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
      <q-list>
        <q-item-label
          header
        >
          Essential Links
        </q-item-label>

        <EssentialLink
          @close-toggle="toggleLeftDrawer"
          v-for="link in linksList"
          :key="link.title"
          v-bind="link"
        />
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>


