'use strict';

const CACHE_NAME = 'my-app-static-cache-v23';
const DATA_CACHE_NAME = 'my-app-data-cache-v23';

const FILES_TO_CACHE = [
    '/moex/',
    '/moex/css/style.css',
    '/moex/index.html',
    '/moex/images/icons/favicon.ico',
    '/moex/images/icons/github.svg',
    '/moex/images/icons/linkedin.svg',
    '/moex/scripts/main.js',
    'https://cdn.jsdelivr.net/npm/jquery/dist/jquery.min.js',
    'https://cdn.jsdelivr.net/npm/d3/dist/d3.min.js',
    'https://cdn.jsdelivr.net/npm/plotly.js/dist/plotly.min.js'
];

self.addEventListener('install', async (evt) => {
    evt.waitUntil(
        caches.open(CACHE_NAME).then(async (cache) => {
            try {
                await cache.addAll(FILES_TO_CACHE);
            } catch (error) {
                console.error('Failed to cache files:', error);
            }
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', (evt) => {
    evt.waitUntil(
        caches.keys().then((keyList) => {
            return Promise.all(keyList.map((key) => {
                if (key !== CACHE_NAME && key !== DATA_CACHE_NAME) {
                    return caches.delete(key);
                }
            }));
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (evt) => {
    if (evt.request.url.includes('/moex/data/iss')) {
        evt.respondWith(
            caches.open(DATA_CACHE_NAME).then(async (cache) => {
                try {
                    const response = await fetch(evt.request);
                    if (response.status === 200) {
                        cache.put(evt.request.url, response.clone());
                    }
                    return response;
                } catch (error) {
                    const cachedResponse = await cache.match(evt.request);
                    if (cachedResponse) {
                        return cachedResponse;
                    }
                    console.error('Failed to fetch data:', error);
                }
            })
        );
        return;
    }
    evt.respondWith(
        caches.open(CACHE_NAME).then(async (cache) => {
            const response = await cache.match(evt.request);
            return response || fetch(evt.request);
        })
    );
});
