import { boot } from 'quasar/wrappers';
import Vue3GoogleLogin from 'vue3-google-login';

export default boot(({ app }): void => {
  const options = {
    clientId: process.env.VUE_APP_GOOGLE_API
  };

  app.use(Vue3GoogleLogin, options);
});
