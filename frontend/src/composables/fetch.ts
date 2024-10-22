import { useJwtStore } from 'stores/jwt-store.js';

export async function useFetch(
  method: string,
  url: string,
  body: any | null = null
) {
  const headers: any = {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  };

  const jwtStore = useJwtStore();

  if (jwtStore.token) {
    headers['Authorization'] = 'Bearer ' + jwtStore.token;
  }

  const init: any = {
    headers: headers,
    method: method,
  };

  if (body) {
    init['body'] = JSON.stringify(body);
  }

  const resp = await fetch(url, init);

  const responseBody = await resp.json();

  if (!resp.ok) {
    throw Error(responseBody.detail);
  }

  return responseBody;
}
