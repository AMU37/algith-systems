const CACHE_NAME = 'alghith-v1';
const ASSETS = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/images/logo.png',
    '/static/manifest.json'
];

self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', (e) => {
    if (e.request.method !== 'GET') return;
    e.respondWith(
        caches.match(e.request).then((cached) =>
            fetch(e.request).then((response) => {
                caches.open(CACHE_NAME).then((cache) => cache.put(e.request, response.clone()));
                return response;
            }).catch(() => cached)
        )
    );
});
