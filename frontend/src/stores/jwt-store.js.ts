import { defineStore } from 'pinia';
import { Profile } from 'src/shared.types';
import { useFetch } from 'src/composables/fetch';
import { jwtDecode } from 'jwt-decode';

export const useJwtStore = defineStore('jwt', {
  state: () => ({
    token: localStorage.getItem('token') ?? '',
  }),
  getters: {
    isAuthenticated: (state): boolean => {
      return state.token !== '';
    },
    isAdmin: (state): boolean => {
      if (state.token === '') {
        return false;
      }
      const { role } = jwtDecode(state.token);

      if (role == 'user') {
        return false;
      }

      return true;

    },

    isValid: (state): boolean => {
      if (!state.token) {
        return true;
      }

      const { exp } = jwtDecode(state.token);

      if (!exp) {
        return true;
      }
      const currentTime = Date.now() / 1000;

      return exp > currentTime;
    },
  },

  actions: {
    async fetchJwt(email: string, password: string): Promise<void> {
      const body = { email: email, password: password };

      const { access_token } = await useFetch('POST', '/api/auth/login', body);
      localStorage.setItem('token', access_token);
      this.token = access_token;
    },
    removeToken() {
      localStorage.setItem('token', '');
      this.token = '';
    },
  },
});
