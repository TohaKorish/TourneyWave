<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useFetch } from 'src/composables/fetch';
import { Notify } from 'quasar';
import { useRoute, useRouter } from 'vue-router';
import { Game } from 'src/shared.types';

const router = useRouter();

const isImageChanged = ref<boolean>(false);

const gameName = ref<string>('');
const image = ref();
const gameId = ref<number>(0);
const preview = ref<{ url: string; name: string } | null>(null);

const participantCount = ref<number[]>([]);
const participantOptions = ref<number[]>([2, 3, 4, 5, 7]);

const route = useRoute();

onMounted(async () => {
  const isEdit = route.path.includes('games/edit');

  if (isEdit) {
    const id = route.params.id;

    try {
      const game: Game = await useFetch('GET', '/api/games/' + id);

      gameName.value = game.name;
      gameId.value = game.id;
      participantCount.value = game.participantCount;

      const response = await fetch(game.image);

      if (response.ok) {
        const blob = await response.blob();
        image.value = new File([blob], 'current_image.jpg', {
          type: blob.type,
        });

        preview.value = {
          url: URL.createObjectURL(blob),
          name: 'current_image.jpg',
        };
      } else {
        image.value = null;
        preview.value = null;
      }
    } catch (err) {
      console.log(err);
      if (err instanceof TypeError) {
        Notify.create({
          message: 'Can not read the image',
          color: 'warning',
          position: 'top',
        });
        image.value = null;
        preview.value = null;
        return;
      }

      router.push({ name: 'not-found' });
      return;
    }
  }
});

const triggerFileUpload = () => {
  const fileInput = document.querySelector('input[type="file"]');
  fileInput?.click();
};

const onFileChange = (event) => {
  isImageChanged.value = true;

  const file = event.target.files[0];

  console.log(image.value);

  if (preview.value) {
    URL.revokeObjectURL(preview.value.url);
  }

  if (file) {
    preview.value = {
      url: URL.createObjectURL(file),
      name: file.name,
    };
  } else {
    image.value = null;
    preview.value = null;
  }
};

const onSubmit = async () => {
  const isEdit = route.path.includes('games/edit');
  console.log(gameId.value);
  let imageUrl = preview.value.url;

  try {
    if (!isEdit || isImageChanged.value) {
      // Sending image to server
      const formData = new FormData();
      formData.append('image', image.value);

      const imageResponse = await fetch('/api/images', {
        body: formData,
        method: 'POST',
      });

      imageUrl = (await imageResponse.json()).url;
    }

    // Sending game data to server
    const method = isEdit ? 'PUT' : 'POST';
    const body = {
      name: gameName.value,
      image: imageUrl,
      participant_count: participantCount.value,
    };

    let url = '/api/games';

    if (isEdit) {
      body.id = gameId.value;
      url = `${url}/${gameId.value}`;
    }

    await useFetch(method, url, body);

    // Notify success and navigate
    Notify.create({
      message: 'Success !',
      color: 'positive',
      position: 'top',
    });
    router.push('/admin/games');
  } catch (error) {
    // Notify errors
    const errorMessage = error.message || 'Failed to create image!';
    Notify.create({
      message: errorMessage,
      color: 'warning',
      position: 'top',
    });
  }
};
</script>

<template>
  <q-card style="min-width: 400px">
    <q-card-section>
      <div class="text-h6">Game</div>
    </q-card-section>

    <q-card-section>
      <q-form @submit="onSubmit" ref="formRef">
        <q-input
          filled
          v-model="gameName"
          label="Name"
          :rules="[(val) => !!val || 'Name is required']"
          required
          class="q-mb-md"
        />

        <q-file
          v-model="image"
          label="Upload Image(s)"
          @input="onFileChange"
          :rules="[(val) => val || 'Image is required']"
          required
          accept="image/*"
          class="q-mb-md q-mt-md"
          style="
            border: 1px dashed #ccc;
            border-radius: 4px;
            background: #f9f9f9;
          "
        >
          <template v-slot:append>
            <q-btn
              color="primary"
              label="Browse"
              class="q-ml-xs"
              @click.stop="triggerFileUpload"
            />
          </template>

          <template v-slot:hint>
            <div class="text-grey">
              Drag & drop your image files here or click "Browse" to select.
            </div>
          </template>
        </q-file>

        <div v-if="preview" class="q-mt-md">
          <img
            :src="preview.url"
            :alt="preview.name"
            style="
              max-width: 100%;
              max-height: 200px;
              border: 1px solid #ddd;
              border-radius: 4px;
            "
          />
          <div class="text-caption q-mt-xs">{{ preview.name }}</div>
        </div>

        <q-select
          filled
          v-model="participantCount"
          :options="participantOptions"
          label="Participant Count"
          multiple
          :rules="[
            (val) => val.length > 0 || 'Select at least one participant',
          ]"
          required
          class="q-mb-md q-mt-lg"
        />

        <q-card-actions class="flex-center">
          <q-btn type="submit" label="Submit" color="primary" />
        </q-card-actions>
      </q-form>
    </q-card-section>
  </q-card>
</template>

<style scoped></style>
