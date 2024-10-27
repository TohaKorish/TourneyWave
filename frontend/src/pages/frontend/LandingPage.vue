<script setup lang="ts">
import {ref} from 'vue';

const slide = ref(0);

const images = [
  {
    src: 'https://as1.ftcdn.net/v2/jpg/06/03/15/94/1000_F_603159435_kuk9zQwvLt3Ypp3hLATtH80za0hwc8A5.jpg',
    title: 'Game 1'
  },
  {src: 'https://cdn.akamai.steamstatic.com/apps/dota2/images/dota2_social.jpg', title: 'Game 2'},
  {
    src: 'https://cmsassets.rgpub.io/sanity/images/dsfx7636/news/0dd9058c623268e044399d7433371d89041a47b3-3440x1020.jpg?auto=format&fit=fill&q=80&h=1020',
    title: 'Game 3'
  },
  {
    src: 'https://images.squarespace-cdn.com/content/v1/58af450eb3db2b0582612f1d/1693267823655-3711YY46XXOD5WADE9VB/Ev8RQYqXMAAqwGj.jpeg?format=1000w',
    title: 'Game 4'
  },
  {
    src: 'https://images.squarespace-cdn.com/content/v1/58af450eb3db2b0582612f1d/1693267823655-3711YY46XXOD5WADE9VB/Ev8RQYqXMAAqwGj.jpeg?format=1000w',
    title: 'Game 5'
  }
];
</script>

<template>
  <q-page-container>
    <q-page class="q-mx-xl">

      <q-card flat bordered class="bg-blue-grey-10 q-my-lg q-pa-md">
        <q-card-section class="q-pb-none">
          <div class="text-h5 text-bold text-primary">
            Welcome to TourneyWave
          </div>
        </q-card-section>
        <q-card-section>
          <p class="text-subtitle1 text-grey-3">
            At TourneyWave, we organize online gaming tournaments across a variety of games.
            Our tournaments are designed for gamers of all skill levels, whether you're a seasoned pro
            or a passionate newcomer looking to make your mark. Compete with the best and claim your victory!
          </p>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="bg-blue-grey-10 q-my-lg q-pa-md">
        <q-card-section class="q-pb-none">
          <div class="text-h5 text-bold text-primary">
            Explore Popular Games
          </div>
        </q-card-section>
        <q-card-section>
          <q-carousel
            animated
            swipeable
            navigation
            padding
            height="400px"
            class="bg-dark"
            v-model="slide"
            arrows
            infinite
          >
            <q-carousel-slide v-for="(image, index) in images" :key="index" :name="index" :img-src="image.src">
              <div class="absolute-bottom text-h5 text-center text-bold text-white bg-black bg-opacity-50 q-pa-md">
                {{ image.title }}
              </div>
            </q-carousel-slide>
          </q-carousel>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="bg-blue-grey-10 q-my-lg q-pa-md">
        <q-card-section class="q-pb-none">
          <div class="text-h5 text-bold text-primary">
            Our Goal
          </div>
        </q-card-section>
        <q-card-section>
          <p class="text-subtitle1 text-grey-3">
            Our mission is to revolutionize the way online gaming matches and tournaments are organized,
            making it seamless, engaging, and accessible for all players. At TourneyWave, we provide a platform
            where gamers can not only find and join tournaments effortlessly but also connect with like-minded
            teammates who share their passion and competitive spirit.
          </p>
        </q-card-section>
      </q-card>

      <q-card flat bordered class="bg-blue-grey-10 q-my-lg q-pa-md">
        <q-card-section class="q-pb-none">
          <div class="text-h5 text-bold text-primary">
            Join Our Community
          </div>
        </q-card-section>
        <q-card-section class="q-gutter-md">
          <p class="text-subtitle1 text-grey-3">
            Be part of a rapidly growing community of passionate gamers at TourneyWave! Whether you're a casual player
            or a dedicated esports enthusiast, our platform connects you with others who share your love for gaming.
            Form teams, collaborate with skilled players, and build strategies to take on challenging opponents across
            a wide range of game genres.
          </p>
          <img
            src="https://thehornetonline.com/wp-content/uploads/2024/03/cbc14-twitch-gaming-event-.jpeg"
            style="width: 100%; height: auto; object-fit: cover; border-radius: 8px;"
            alt="Gaming Event"
          />
        </q-card-section>
      </q-card>

    </q-page>
  </q-page-container>
</template>

<style scoped>

</style>
