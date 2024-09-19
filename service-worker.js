'use strict';

const CACHE_NAME = 'my-app-static-cache-v7';
const DATA_CACHE_NAME = 'my-app-data-cache-v7';

const FILES_TO_CACHE = [
    '/',
    '/index.html',
    '/history/index.html',
    '/listings/index.html',
    '/images/icons/favicon.ico',
    '/images/icons/github.svg',
    '/images/icons/linkedin.svg',
    '/images/icons/email.svg',
    '/images/icons/treemap.jpeg',
    '/images/icons/scatter.jpeg',
    '/images/icons/bar.jpeg',
    '/scripts/install.js',
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
    if (evt.request.url.includes('/data/iss/history/engines/stock/totals/boards/MRKT/') || evt.request.url.includes('/history/')) {
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
