/* Tripkit service worker.
   Bump CACHE on every release so old cached files are cleared and users get
   the new version. This single line is your "publish a new version" switch. */
const CACHE = "tripkit-v1";

// The app's own files, cached so it loads instantly and works offline.
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/icon-maskable-512.png",
  "./icons/apple-touch-icon.png"
];

// On install: pre-cache the app shell, then take over immediately.
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// On activate: delete any caches from older versions.
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;                       // only cache reads
  const url = new URL(req.url);

  // Never cache the weather/geocoding API — always hit the live network.
  if (url.hostname.endsWith("open-meteo.com")) return;

  // Page loads: network-first (so a returning user sees the latest version
  // when online), falling back to the cached page when offline.
  if (req.mode === "navigate") {
    event.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put("./index.html", copy));
          return res;
        })
        .catch(() => caches.match("./index.html"))
    );
    return;
  }

  // Everything else (icons, fonts, the drag-and-drop library): cache-first,
  // then network — and stash a copy for next time.
  event.respondWith(
    caches.match(req).then(cached =>
      cached || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
        return res;
      }).catch(() => cached)
    )
  );
});
