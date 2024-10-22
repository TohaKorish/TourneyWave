import { boot } from 'quasar/wrappers';
import { useJwtStore } from 'stores/jwt-store.js';

export default boot((): void => {

  const jwtStore = useJwtStore();

  if (! jwtStore.isValid) {
    jwtStore.removeToken();
  }

});
