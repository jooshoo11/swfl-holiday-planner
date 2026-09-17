// Service Worker for SWFL Holiday & Festivities Planner
const CACHE_NAME = 'swfl-holidays-v4';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './events.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-512-maskable.png',
  './icons/apple-touch-icon.png'
];

// Install Event - Pre-cache critical assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event - Clean up previous cache versions
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Stale-While-Revalidate strategy with Offline Fallback
self.addEventListener('fetch', event => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  // Ignore chrome-extension or external analytics if any
  const url = new URL(event.request.url);
  
  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      // Fetch fresh from network in background to update cache
      const fetchPromise = fetch(event.request).then(networkResponse => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      }).catch(() => {
        // Network failed (offline)
        // If offline and request is for page navigation, return cached root or index.html
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });

      // Return cached version immediately if found, else wait for network
      return cachedResponse || fetchPromise;
    })
  );
});
