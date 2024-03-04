'use strict';

const CACHE_NAME = 'my-app-static-cache-v1';
const DATA_CACHE_NAME = 'my-app-data-cache-v1';

const FILES_TO_CACHE = [
    '/moex/',
    '/moex/index.html',
    '/moex/images/favicon.ico',
    '/moex/scripts/main.js',
    '/moex/scripts/install.js',
    'https://code.jquery.com/jquery-3.7.1.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.29.1/plotly.min.js'
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
    if (evt.request.url.includes('https://ruslanbay.github.io/moex/data/')) {
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
