<script setup>
import { ref } from 'vue';
import { Notify } from 'quasar';
import { useRouter } from 'vue-router';
import { useFetch } from 'src/composables/fetch';

const username = ref('');
const email = ref('');
const password = ref('');
const passwordConfirmation = ref('');

const router = useRouter();

const onSubmit = async () => {
  if (username.value && email.value && password.value && passwordConfirmation.value) {
    if (password.value !== passwordConfirmation.value) {
      Notify.create({
        message: 'Passwords do not match',
        color: 'negative',
        position: 'top',
      });
      return;
    }

    try {

      await useFetch("POST", "/api/users", {
        username: username.value,
        email: email.value,
        password: password.value,
      })

      await router.push("/login");

      Notify.create({
        message: 'Successfully registered',
        color: 'positive',
        position: 'top',
      });
    } catch (err) {
      Notify.create({
        message: err.message || 'Registration failed',
        color: 'negative',
        position: 'top',
      });
    }
  }
};
</script>

<template>
    <q-card
      dark
      bordered
      class="q-pa-lg q-mt-lg"
      style="max-width: 600px; min-width: 400px;"
    >
      <q-card-section class="text-center">
        <div class="text-h6 text-primary q-mb-md">Register</div>
      </q-card-section>

      <q-card-section>
        <q-form @submit="onSubmit" class="q-gutter-md">
          <!-- Username Input -->
          <q-input
            v-model="username"
            label="Username"
            bg-color="dark"
            filled
            lazy-rules
            :rules="[(val) => !!val || 'Username is required']"
            dark
            color="primary"
          >
            <template v-slot:prepend>
              <q-icon name="person" color="primary" />
            </template>
          </q-input>

          <!-- Email Input -->
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

          <!-- Password Input -->
          <q-input
            v-model="password"
            type="password"
            label="Password"
            bg-color="dark"
            filled
            lazy-rules
            :rules="[
              (val) => !!val || 'Password is required',
              (val) => val.length >= 6 || 'Password must be at least 6 characters long'
            ]"
            dark
            color="primary"
          >
            <template v-slot:prepend>
              <q-icon name="lock" color="primary" />
            </template>
          </q-input>

          <!-- Password Confirmation Input -->
          <q-input
            v-model="passwordConfirmation"
            type="password"
            label="Confirm Password"
            bg-color="dark"
            filled
            lazy-rules
            :rules="[(val) => !!val || 'Password confirmation is required']"
            dark
            color="primary"
          >
            <template v-slot:prepend>
              <q-icon name="lock" color="primary" />
            </template>
          </q-input>

          <!-- Register Button -->
          <div class="row justify-center q-mt-lg">
            <q-btn
              type="submit"
              label="Register"
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
</template>

<style scoped></style>
