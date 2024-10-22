<script setup>
import { ref } from 'vue';
import { useJwtStore } from 'stores/jwt-store.js';
import { Notify } from 'quasar';
import { useProfile } from 'stores/profile-store';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');

const jwtStore = useJwtStore();
const profileStore = useProfile();
const router = useRouter();

const onSubmit = async () => {
  if (email.value && password.value) {
    jwtStore.fetchJwt(email.value, password.value).then(
      async () => {
        await profileStore.fetchMe();

        const location = jwtStore.isAdmin ? '/admin': '/dashboard'

        await router.push(location);

        Notify.create({
          message: 'Successfully logged in',
          color: 'positive',
          position: 'top',
        });
      },
      (err) => {
        Notify.create({
          message: err.message,
          color: 'negative',
          position: 'top',
        });
      }
    );
  }
};
</script>
<template>
  <q-page class="q-pa-md flex flex-center bg-dark">
    <q-card
      dark
      bordered
      class="q-pa-lg q-mt-lg"
      style="max-width: 600px; min-width: 400px;"
    >
      <q-card-section class="text-center">
        <div class="text-h6 text-primary q-mb-md">Login</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <!-- Email Input Field -->
          <q-input
            v-model="email"
            label="Email"
            bg-color="dark"
            filled
            lazy-rules
            :rules="[
              (val) => !!val || 'Email is required',
              (val) => /.+@.+\..+/.test(val) || 'Enter a valid email',
            ]"
            dark
            color="primary"
          >
            <template v-slot:prepend>
              <q-icon name="email" color="primary" />
            </template>
          </q-input>

          <!-- Password Input Field -->
          <q-input
            v-model="password"
            type="password"
            label="Password"
            bg-color="dark"
            filled
            lazy-rules
            :rules="[(val) => !!val || 'Password is required']"
            dark
            color="primary"
          >
            <template v-slot:prepend>
              <q-icon name="lock" color="primary" />
            </template>
          </q-input>

          <!-- Login Button -->
          <div class="row justify-center q-mt-lg">
            <q-btn
              type="submit"
              label="Login"
              color="primary"
              size="large"
              class="q-px-xl"
              unelevated
              no-caps
            />
          </div>
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>
