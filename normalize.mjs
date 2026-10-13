// Node.js 20+. Keep RAPIDAPI_KEY in your server environment.
export const HOST = 'crm-lead-hygiene-api.p.rapidapi.com';
export const contact = {name:'  Ana   Maria  ',email:'ana@example.COM ',phone:'020 7946 0018',country:'gb',website:'Example.com/?utm_source=crm'};
export async function call(path, body, key = process.env.RAPIDAPI_KEY, transport = fetch) {
  if (!key) throw new Error('Set RAPIDAPI_KEY to your own subscribed RapidAPI application key.');
  const response = await transport(`https://${HOST}${path}`, {
    method:'POST', headers:{'Content-Type':'application/json','X-RapidAPI-Key':key,'X-RapidAPI-Host':HOST},
    body:JSON.stringify(body), signal:AbortSignal.timeout(15000)
  });
  const data = await response.json();
  if (!response.ok) throw new Error(`HTTP ${response.status}: ${data.error?.code ?? data.message ?? 'Request failed'}`);
  return data;
}
if (process.argv[1]?.endsWith('normalize.mjs')) console.log(JSON.stringify(await call('/v1/contact/normalize',contact),null,2));
