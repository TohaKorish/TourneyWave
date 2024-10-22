import { boot } from 'quasar/wrappers';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import { Roulette } from 'vue3-roulette';

export default boot(({ app }): void => {
  app.component('app-roulette', Roulette);
});
