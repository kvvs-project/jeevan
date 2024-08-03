// Name of the cache
const CACHE_NAME = 'jeevan-cache-v1';

// Files to cache
const urlsToCache = [
  '/',
  '/static/js/home.js',
  '/static/manifest.json',
  '/static/favicon.ico',
  '/static/favicon-16x16.png',
  '/static/favicon-32x32.png',
  '/static/android-chrome-192x192.png',
  '/static/android-chrome-512x512.png',
  '/static/img/misc/jeevan.webp'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('Opened cache');
      return cache.addAll(urlsToCache);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) {
        return response;
      }
      return fetch(event.request);
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.filter((cacheName) => cacheName !== CACHE_NAME).map((cacheName) => {
          return caches.delete(cacheName);
        })
      );
    })
  );
});
