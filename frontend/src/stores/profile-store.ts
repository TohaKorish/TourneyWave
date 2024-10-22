import { defineStore } from 'pinia';
import { useFetch } from 'src/composables/fetch';
import { Profile } from 'src/shared.types';

export const useProfile = defineStore('profile', {
  state: () => ({
    profile: JSON.parse(localStorage.getItem('profile')) || null,
  }),
  actions: {
    async fetchMe() {
      useFetch("GET", "/api/users/me").then((user) => {
        this.profile = user;
        const profileString = JSON.stringify(user)
        localStorage.setItem('profile', profileString)

      })
    },
    remove() {
      localStorage.removeItem('profile');
      this.profile = null;
    }
  }
});
