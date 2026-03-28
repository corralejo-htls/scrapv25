
===  BookingScraper Celery Worker  ===


 -------------- worker@HOUSE v5.4.0 (opalescent)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0 2026-03-28 12:18:33
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         bookingscraper:0x24af6e30590
- ** ---------- .> transport:   redis://localhost:6379/0
- ** ---------- .> results:     redis://localhost:6379/1
- *** --- * --- .> concurrency: 1 (solo)
-- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
--- ***** -----
 -------------- [queues]
                .> default          exchange=default(direct) key=default
                .> maintenance      exchange=maintenance(direct) key=maintenance
                .> monitoring       exchange=monitoring(direct) key=monitoring

[tasks]
  . tasks.collect_system_metrics
  . tasks.ensure_log_partitions
  . tasks.purge_old_debug_html
  . tasks.reset_stale_processing_urls
  . tasks.scrape_pending_urls

[2026-03-28 12:18:36,026: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-28 12:18:40,114: INFO/MainProcess] mingle: searching for neighbors
[2026-03-28 12:18:47,240: INFO/MainProcess] mingle: all alone
[2026-03-28 12:18:55,416: INFO/MainProcess] worker@HOUSE ready.
[2026-03-28 12:19:09,618: INFO/MainProcess] Task tasks.scrape_pending_urls[da71fbcd-5c85-4f0b-9284-5aa5c4dea65c] received
[2026-03-28 12:19:11,795: INFO/MainProcess] Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5
[2026-03-28 12:19:11,975: INFO/MainProcess] Task tasks.scrape_pending_urls[da71fbcd-5c85-4f0b-9284-5aa5c4dea65c] succeeded in 2.356046799919568s: {'status': 'idle', 'pending': 0}
[2026-03-28 12:19:33,483: INFO/MainProcess] Task tasks.scrape_pending_urls[29fc30d2-f9f2-46d3-acac-cf965656a9a0] received
[2026-03-28 12:19:33,488: INFO/MainProcess] Task tasks.scrape_pending_urls[29fc30d2-f9f2-46d3-acac-cf965656a9a0] succeeded in 0.0050360000459477305s: {'status': 'idle', 'pending': 0}
[2026-03-28 12:20:03,483: INFO/MainProcess] Task tasks.scrape_pending_urls[7f0b0b3b-c60b-4dbc-b087-6c1af7733741] received
[2026-03-28 12:20:03,488: INFO/MainProcess] Task tasks.scrape_pending_urls[7f0b0b3b-c60b-4dbc-b087-6c1af7733741] succeeded in 0.004073099931702018s: {'status': 'idle', 'pending': 0}
[2026-03-28 12:20:33,484: INFO/MainProcess] Task tasks.scrape_pending_urls[e129043f-f0f0-42f9-a111-41209e52ebb4] received
[2026-03-28 12:20:35,500: INFO/MainProcess] scrape_pending_urls: starting auto-batch, pending=13
[2026-03-28 12:20:36,171: INFO/MainProcess] VPN: original IP = 45.141.123.241
[2026-03-28 12:20:36,844: INFO/MainProcess] VPN: home country detected = FR
[2026-03-28 12:20:36,846: INFO/MainProcess] NordVPNManager initialised | interactive=False | original_ip=45.141.123.241 | home_country=FR
[2026-03-28 12:20:36,846: INFO/MainProcess] ScraperService INIT | VPN_ENABLED=True | HEADLESS_BROWSER=False | workers=2 | languages=en,es,de,it,fr,pt | vpn_interval=50s | vpn_countries=Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden
[2026-03-28 12:20:36,877: INFO/MainProcess] VPN: excluding home country FR from pool — remaining: ES,DE,NL,IT,CA,SE
[2026-03-28 12:20:36,878: INFO/MainProcess] VPN: connecting to Italy (IT)...
[2026-03-28 12:20:58,542: INFO/MainProcess] VPN connected to Italy — IP: 185.81.127.237
[2026-03-28 12:20:58,542: INFO/MainProcess] VPN connected OK before batch start.
[2026-03-28 12:20:58,544: INFO/MainProcess] Dispatching batch: urls=13 workers=2
[2026-03-28 12:20:58,545: INFO/MainProcess] Redis connection pool created: max_connections=20
[2026-03-28 12:21:03,521: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:03,539: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:16,712: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:21,319: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:31,732: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:34,424: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:37,933: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:38,606: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:47,312: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:47,312: INFO/MainProcess] CloudScraper failed for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd/en — trying Selenium.
[2026-03-28 12:21:47,579: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:21:50,836: INFO/MainProcess] Selenium: Brave started
[2026-03-28 12:21:55,701: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:22:19,935: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-28 12:22:19,935: INFO/MainProcess] CloudScraper failed for e5698a41-3ffa-4d1d-90fa-854ec5619d99/en — trying Selenium.
[2026-03-28 12:24:19,128: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 12:24:21,351: INFO/MainProcess] Gallery: 137 images loaded after scroll
[2026-03-28 12:24:25,038: INFO/MainProcess] Gallery: 144 unique image URLs extracted
[2026-03-28 12:24:25,177: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 12:24:25,178: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 12:24:52,054: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd
[2026-03-28 12:25:00,343: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 2870ebb8-c213-4354-83ec-a3e9ed555664
[2026-03-28 12:25:00,344: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 2870ebb8-c213-4354-83ec-a3e9ed555664
[2026-03-28 12:25:00,353: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd lang=en: SUCCESS
[2026-03-28 12:25:03,122: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-28 12:25:13,165: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-28 12:25:17,846: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-28 12:25:30,488: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-28 12:25:36,683: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-28 12:25:48,069: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-28 12:25:48,069: INFO/MainProcess] CloudScraper failed for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd/es — trying Selenium.
[2026-03-28 12:27:14,070: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 12:27:16,020: INFO/MainProcess] Gallery: 131 images loaded after scroll
[2026-03-28 12:27:19,791: INFO/MainProcess] Gallery: 138 unique image URLs extracted
[2026-03-28 12:27:19,965: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 12:27:19,966: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 12:27:46,967: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for e5698a41-3ffa-4d1d-90fa-854ec5619d99
[2026-03-28 12:27:57,497: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel bf559f6a-9be3-4832-a430-6d3d51b91722
[2026-03-28 12:27:57,497: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel bf559f6a-9be3-4832-a430-6d3d51b91722
[2026-03-28 12:27:57,503: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99 lang=en: SUCCESS
[2026-03-28 12:28:00,217: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-28 12:28:10,278: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-28 12:28:15,079: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-28 12:28:28,417: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-28 12:28:35,041: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-28 12:29:05,060: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd lang=es: SUCCESS
[2026-03-28 12:29:07,802: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-28 12:29:14,722: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-28 12:29:14,723: INFO/MainProcess] CloudScraper failed for e5698a41-3ffa-4d1d-90fa-854ec5619d99/es — trying Selenium.
[2026-03-28 12:29:17,751: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-28 12:29:22,669: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-28 12:29:31,979: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-28 12:29:38,180: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-28 12:29:49,376: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-28 12:29:49,377: INFO/MainProcess] CloudScraper failed for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd/de — trying Selenium.
[2026-03-28 12:30:33,507: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99 lang=es: SUCCESS
[2026-03-28 12:30:36,314: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-28 12:30:45,822: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-28 12:30:50,569: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-28 12:31:04,343: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-28 12:31:10,528: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-28 12:31:24,468: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-28 12:31:24,469: INFO/MainProcess] CloudScraper failed for e5698a41-3ffa-4d1d-90fa-854ec5619d99/de — trying Selenium.
[2026-03-28 12:31:51,368: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd lang=de: SUCCESS
[2026-03-28 12:31:54,188: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-28 12:32:08,520: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-28 12:32:13,285: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-28 12:32:23,326: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-28 12:32:29,495: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-28 12:32:40,909: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-28 12:32:40,909: INFO/MainProcess] CloudScraper failed for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd/it — trying Selenium.
[2026-03-28 12:33:08,658: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99 lang=de: SUCCESS
[2026-03-28 12:33:11,507: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-28 12:33:34,397: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-28 12:33:39,206: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-28 12:33:47,768: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-28 12:33:54,111: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-28 12:34:08,863: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-28 12:34:08,863: INFO/MainProcess] CloudScraper failed for e5698a41-3ffa-4d1d-90fa-854ec5619d99/it — trying Selenium.
[2026-03-28 12:34:39,731: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd lang=it: SUCCESS
[2026-03-28 12:34:42,462: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-28 12:34:57,327: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-28 12:35:02,162: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-28 12:35:12,602: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-28 12:35:18,971: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-28 12:35:33,712: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-28 12:35:33,712: INFO/MainProcess] CloudScraper failed for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd/fr — trying Selenium.
[2026-03-28 12:35:57,454: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99 lang=it: SUCCESS
[2026-03-28 12:36:00,267: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-28 12:36:14,551: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-28 12:36:19,416: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-28 12:36:30,188: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-28 12:36:36,359: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-28 12:36:50,639: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-28 12:36:50,640: INFO/MainProcess] CloudScraper failed for e5698a41-3ffa-4d1d-90fa-854ec5619d99/fr — trying Selenium.
[2026-03-28 12:37:15,482: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd lang=fr: SUCCESS
[2026-03-28 12:37:18,185: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:37:27,526: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:37:32,266: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:37:41,004: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:37:47,194: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:37:58,573: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:37:58,573: INFO/MainProcess] CloudScraper failed for e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd/pt — trying Selenium.
[2026-03-28 12:38:35,119: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99 lang=fr: SUCCESS
[2026-03-28 12:38:37,814: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:38:47,285: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:38:52,133: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:39:04,031: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:39:10,241: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:39:23,918: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-28 12:39:23,918: INFO/MainProcess] CloudScraper failed for e5698a41-3ffa-4d1d-90fa-854ec5619d99/pt — trying Selenium.
[2026-03-28 12:40:06,552: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd lang=pt: SUCCESS
[2026-03-28 12:40:06,555: INFO/MainProcess] URL e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 12:40:09,475: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-28 12:40:20,349: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-28 12:40:25,225: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-28 12:40:37,415: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-28 12:40:43,604: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-28 12:40:55,634: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-28 12:40:55,635: INFO/MainProcess] CloudScraper failed for 9196f2c9-d95b-459e-922b-299a2970a88f/en — trying Selenium.
[2026-03-28 12:41:24,010: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99 lang=pt: SUCCESS
[2026-03-28 12:41:24,013: INFO/MainProcess] URL e5698a41-3ffa-4d1d-90fa-854ec5619d99: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 12:41:26,869: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-28 12:41:37,332: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-28 12:41:42,156: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-28 12:41:51,231: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-28 12:41:57,422: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-28 12:42:11,267: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-28 12:42:11,267: INFO/MainProcess] CloudScraper failed for e0b37fd7-b906-4e5c-a3fd-1ba839138900/en — trying Selenium.
[2026-03-28 12:43:42,916: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 12:43:44,823: INFO/MainProcess] Gallery: 87 images loaded after scroll
[2026-03-28 12:43:47,151: INFO/MainProcess] Gallery: 94 unique image URLs extracted
[2026-03-28 12:43:47,288: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 12:43:47,289: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 12:44:13,510: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 9196f2c9-d95b-459e-922b-299a2970a88f
[2026-03-28 12:44:22,311: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 5adb942b-63a5-4867-a58a-905bcfd722ff
[2026-03-28 12:44:22,311: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 5adb942b-63a5-4867-a58a-905bcfd722ff
[2026-03-28 12:44:22,317: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f lang=en: SUCCESS
[2026-03-28 12:44:25,346: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-28 12:44:38,542: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-28 12:44:43,338: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-28 12:44:52,705: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-28 12:44:58,881: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-28 12:45:07,703: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-28 12:45:07,704: INFO/MainProcess] CloudScraper failed for 9196f2c9-d95b-459e-922b-299a2970a88f/es — trying Selenium.
[2026-03-28 12:46:35,615: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 12:46:38,050: INFO/MainProcess] Gallery: 266 images loaded after scroll
[2026-03-28 12:46:43,794: INFO/MainProcess] Gallery: 273 unique image URLs extracted
[2026-03-28 12:46:43,967: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 12:46:43,970: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 12:47:11,520: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for e0b37fd7-b906-4e5c-a3fd-1ba839138900
[2026-03-28 12:47:21,539: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 84ab8779-b752-4112-9aa2-ddff56ef9901
[2026-03-28 12:47:21,540: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 84ab8779-b752-4112-9aa2-ddff56ef9901
[2026-03-28 12:47:21,547: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900 lang=en: SUCCESS
[2026-03-28 12:47:24,288: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-28 12:47:32,711: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-28 12:47:37,608: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-28 12:47:49,981: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-28 12:47:56,172: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-28 12:48:09,963: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-28 12:48:09,963: INFO/MainProcess] CloudScraper failed for e0b37fd7-b906-4e5c-a3fd-1ba839138900/es — trying Selenium.
[2026-03-28 12:48:30,022: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f lang=es: SUCCESS
[2026-03-28 12:48:32,820: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-28 12:48:44,691: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-28 12:48:49,541: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-28 12:48:59,993: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-28 12:49:06,183: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-28 12:49:19,714: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-28 12:49:19,714: INFO/MainProcess] CloudScraper failed for 9196f2c9-d95b-459e-922b-299a2970a88f/de — trying Selenium.
[2026-03-28 12:49:49,439: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900 lang=es: SUCCESS
[2026-03-28 12:49:52,338: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-28 12:50:05,479: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-28 12:50:10,428: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-28 12:50:23,846: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-28 12:50:30,038: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-28 12:50:43,685: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-28 12:50:43,685: INFO/MainProcess] CloudScraper failed for e0b37fd7-b906-4e5c-a3fd-1ba839138900/de — trying Selenium.
[2026-03-28 12:51:08,991: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f lang=de: SUCCESS
[2026-03-28 12:51:11,668: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-28 12:51:23,591: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-28 12:51:28,339: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-28 12:51:38,118: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-28 12:51:44,298: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-28 12:51:53,655: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-28 12:51:53,655: INFO/MainProcess] CloudScraper failed for 9196f2c9-d95b-459e-922b-299a2970a88f/it — trying Selenium.
[2026-03-28 12:52:43,291: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900 lang=de: SUCCESS
[2026-03-28 12:52:46,039: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-28 12:53:00,103: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-28 12:53:04,955: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-28 12:53:15,538: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-28 12:53:21,733: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-28 12:53:35,152: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-28 12:53:35,153: INFO/MainProcess] CloudScraper failed for e0b37fd7-b906-4e5c-a3fd-1ba839138900/it — trying Selenium.
[2026-03-28 12:54:02,022: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f lang=it: SUCCESS
[2026-03-28 12:54:04,746: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-28 12:54:38,219: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-28 12:54:43,022: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-28 12:54:53,641: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-28 12:54:59,879: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-28 12:55:08,491: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-28 12:55:08,491: INFO/MainProcess] CloudScraper failed for 9196f2c9-d95b-459e-922b-299a2970a88f/fr — trying Selenium.
[2026-03-28 12:55:20,888: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900 lang=it: SUCCESS
[2026-03-28 12:55:23,683: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-28 12:55:35,695: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-28 12:55:40,555: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-28 12:56:14,473: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-28 12:56:20,621: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-28 12:56:39,866: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f lang=fr: SUCCESS
[2026-03-28 12:56:42,672: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-28 12:56:48,669: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-28 12:56:48,669: INFO/MainProcess] CloudScraper failed for e0b37fd7-b906-4e5c-a3fd-1ba839138900/fr — trying Selenium.
[2026-03-28 12:56:51,481: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-28 12:56:56,388: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-28 12:57:05,545: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-28 12:57:11,769: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-28 12:57:20,932: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-28 12:57:20,933: INFO/MainProcess] CloudScraper failed for 9196f2c9-d95b-459e-922b-299a2970a88f/pt — trying Selenium.
[2026-03-28 12:58:08,761: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900 lang=fr: SUCCESS
[2026-03-28 12:58:11,549: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-28 12:58:37,150: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-28 12:58:42,019: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-28 12:58:54,561: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-28 12:59:00,749: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-28 12:59:09,444: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-28 12:59:09,444: INFO/MainProcess] CloudScraper failed for e0b37fd7-b906-4e5c-a3fd-1ba839138900/pt — trying Selenium.
[2026-03-28 12:59:26,100: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f lang=pt: SUCCESS
[2026-03-28 12:59:26,103: INFO/MainProcess] URL 9196f2c9-d95b-459e-922b-299a2970a88f: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 12:59:28,954: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-28 12:59:40,960: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-28 12:59:45,754: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-28 12:59:55,272: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-28 13:00:01,472: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-28 13:00:15,898: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-28 13:00:15,898: INFO/MainProcess] CloudScraper failed for aeb8a08c-a894-4b14-873b-4eb3c85b49c1/en — trying Selenium.
[2026-03-28 13:00:43,102: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900 lang=pt: SUCCESS
[2026-03-28 13:00:43,105: INFO/MainProcess] URL e0b37fd7-b906-4e5c-a3fd-1ba839138900: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 13:00:45,986: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-28 13:00:58,378: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-28 13:01:03,184: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-28 13:01:11,514: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-28 13:01:17,725: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-28 13:01:31,742: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-28 13:01:31,742: INFO/MainProcess] CloudScraper failed for e448865f-1a25-45bc-9d74-d01a35b9a9f9/en — trying Selenium.
[2026-03-28 13:03:19,713: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 13:03:21,653: INFO/MainProcess] Gallery: 118 images loaded after scroll
[2026-03-28 13:03:25,487: INFO/MainProcess] Gallery: 125 unique image URLs extracted
[2026-03-28 13:03:25,730: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 13:03:25,731: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 13:03:53,504: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for aeb8a08c-a894-4b14-873b-4eb3c85b49c1
[2026-03-28 13:04:07,678: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel e4027c19-7afe-41c3-b589-5132ed6cbf0a
[2026-03-28 13:04:07,679: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel e4027c19-7afe-41c3-b589-5132ed6cbf0a
[2026-03-28 13:04:07,685: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1 lang=en: SUCCESS
[2026-03-28 13:04:10,504: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-28 13:04:22,995: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-28 13:04:27,792: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-28 13:04:49,447: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-28 13:04:55,638: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-28 13:05:05,412: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-28 13:05:05,412: INFO/MainProcess] CloudScraper failed for aeb8a08c-a894-4b14-873b-4eb3c85b49c1/es — trying Selenium.
[2026-03-28 13:06:15,092: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 13:06:17,003: INFO/MainProcess] Gallery: 24 images loaded after scroll
[2026-03-28 13:06:18,170: INFO/MainProcess] Gallery: 31 unique image URLs extracted
[2026-03-28 13:06:18,290: INFO/MainProcess] hotelPhotos JS: 24 photos extracted from page source
[2026-03-28 13:06:18,290: INFO/MainProcess] Gallery: 24 photos with full metadata (hotelPhotos JS)
[2026-03-28 13:06:44,958: INFO/MainProcess] Photos: 24 rich photo records (hotelPhotos JS) for e448865f-1a25-45bc-9d74-d01a35b9a9f9
[2026-03-28 13:06:50,160: INFO/MainProcess] download_photo_batch: 72/72 photo-files saved for hotel dbde9052-3144-4b52-aaab-67afeb3ce049
[2026-03-28 13:06:50,160: INFO/MainProcess] ImageDownloader (photo_batch): 72/24 photos saved for hotel dbde9052-3144-4b52-aaab-67afeb3ce049
[2026-03-28 13:06:50,166: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9 lang=en: SUCCESS
[2026-03-28 13:06:53,226: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-28 13:07:05,221: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-28 13:07:11,077: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-28 13:07:23,942: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-28 13:07:30,147: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-28 13:07:41,032: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-28 13:07:41,033: INFO/MainProcess] CloudScraper failed for e448865f-1a25-45bc-9d74-d01a35b9a9f9/es — trying Selenium.
[2026-03-28 13:08:03,325: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1 lang=es: SUCCESS
[2026-03-28 13:08:06,065: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-28 13:08:16,200: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-28 13:08:20,891: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-28 13:08:51,473: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-28 13:08:57,601: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-28 13:09:21,434: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-28 13:09:21,435: INFO/MainProcess] CloudScraper failed for aeb8a08c-a894-4b14-873b-4eb3c85b49c1/de — trying Selenium.
[2026-03-28 13:09:21,969: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9 lang=es: SUCCESS
[2026-03-28 13:09:24,823: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-28 13:09:39,260: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-28 13:09:44,025: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-28 13:09:58,371: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-28 13:10:04,560: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-28 13:10:12,670: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-28 13:10:12,670: INFO/MainProcess] CloudScraper failed for e448865f-1a25-45bc-9d74-d01a35b9a9f9/de — trying Selenium.
[2026-03-28 13:10:41,042: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1 lang=de: SUCCESS
[2026-03-28 13:10:43,692: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-28 13:11:12,174: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-28 13:11:17,072: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-28 13:11:46,065: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-28 13:11:52,200: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-28 13:12:11,791: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9 lang=de: SUCCESS
[2026-03-28 13:12:14,546: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-28 13:12:16,272: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-28 13:12:16,273: INFO/MainProcess] CloudScraper failed for aeb8a08c-a894-4b14-873b-4eb3c85b49c1/it — trying Selenium.
[2026-03-28 13:12:29,466: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-28 13:12:34,175: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-28 13:12:43,471: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-28 13:12:49,665: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-28 13:13:03,366: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-28 13:13:03,366: INFO/MainProcess] CloudScraper failed for e448865f-1a25-45bc-9d74-d01a35b9a9f9/it — trying Selenium.
[2026-03-28 13:13:34,307: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1 lang=it: SUCCESS
[2026-03-28 13:13:37,141: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-28 13:13:59,077: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-28 13:14:03,919: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-28 13:14:16,764: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-28 13:14:22,990: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-28 13:14:37,503: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-28 13:14:37,503: INFO/MainProcess] CloudScraper failed for aeb8a08c-a894-4b14-873b-4eb3c85b49c1/fr — trying Selenium.
[2026-03-28 13:14:51,326: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9 lang=it: SUCCESS
[2026-03-28 13:14:54,103: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-28 13:15:22,720: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-28 13:15:27,525: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-28 13:15:37,198: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-28 13:15:43,392: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-28 13:15:53,451: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-28 13:15:53,451: INFO/MainProcess] CloudScraper failed for e448865f-1a25-45bc-9d74-d01a35b9a9f9/fr — trying Selenium.
[2026-03-28 13:16:10,461: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1 lang=fr: SUCCESS
[2026-03-28 13:16:13,186: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-28 13:16:27,633: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-28 13:16:32,434: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-28 13:16:44,070: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-28 13:16:50,265: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-28 13:17:00,122: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-28 13:17:00,123: INFO/MainProcess] CloudScraper failed for aeb8a08c-a894-4b14-873b-4eb3c85b49c1/pt — trying Selenium.
[2026-03-28 13:17:43,022: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9 lang=fr: SUCCESS
[2026-03-28 13:17:45,765: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-28 13:18:09,373: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-28 13:18:14,246: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-28 13:18:23,526: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-28 13:18:29,715: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-28 13:19:01,398: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-28 13:19:01,428: INFO/MainProcess] CloudScraper failed for e448865f-1a25-45bc-9d74-d01a35b9a9f9/pt — trying Selenium.
[2026-03-28 13:19:01,817: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1 lang=pt: SUCCESS
[2026-03-28 13:19:01,820: INFO/MainProcess] URL aeb8a08c-a894-4b14-873b-4eb3c85b49c1: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 13:19:04,621: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-28 13:19:36,399: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-28 13:19:41,141: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-28 13:19:55,585: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-28 13:20:01,776: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-28 13:20:14,338: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-28 13:20:14,339: INFO/MainProcess] CloudScraper failed for d7704d4b-a617-4f66-8424-21c14805159d/en — trying Selenium.
[2026-03-28 13:20:20,846: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9 lang=pt: SUCCESS
[2026-03-28 13:20:20,849: INFO/MainProcess] URL e448865f-1a25-45bc-9d74-d01a35b9a9f9: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 13:20:23,671: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:20:33,158: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:20:37,823: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:21:14,594: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:21:20,774: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:21:55,904: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:21:55,904: INFO/MainProcess] CloudScraper failed for a12bc041-5341-4f6c-bce9-338f023b7fb8/en — trying Selenium.
[2026-03-28 13:22:41,107: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 13:22:43,055: INFO/MainProcess] Gallery: 144 images loaded after scroll
[2026-03-28 13:22:47,220: INFO/MainProcess] Gallery: 151 unique image URLs extracted
[2026-03-28 13:22:47,363: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 13:22:47,364: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 13:23:14,270: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for d7704d4b-a617-4f66-8424-21c14805159d
[2026-03-28 13:23:23,552: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 9df04de8-65a5-4166-b504-e8a0c4bb16a6
[2026-03-28 13:23:23,552: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 9df04de8-65a5-4166-b504-e8a0c4bb16a6
[2026-03-28 13:23:23,559: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d lang=en: SUCCESS
[2026-03-28 13:23:26,382: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-28 13:24:01,502: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-28 13:24:06,298: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-28 13:24:18,475: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-28 13:24:24,673: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-28 13:24:33,481: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-28 13:24:33,483: INFO/MainProcess] CloudScraper failed for d7704d4b-a617-4f66-8424-21c14805159d/es — trying Selenium.
[2026-03-28 13:24:33,788: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-28 13:24:43,857: INFO/MainProcess] Selenium retry 2 -- waiting 12s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:26:10,795: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-28 13:26:20,395: INFO/MainProcess] Selenium retry 3 -- waiting 30s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:28:05,074: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-28 13:28:05,074: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:28:05,076: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure a12bc041-5341-4f6c-bce9-338f023b7fb8/en
[2026-03-28 13:28:05,076: INFO/MainProcess] VPN: rotating (current=IT)...
[2026-03-28 13:28:06,063: INFO/MainProcess] VPN disconnected.
[2026-03-28 13:28:11,064: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-28 13:28:31,046: INFO/MainProcess] VPN connected to Sweden — IP: 31.40.213.220
[2026-03-28 13:28:31,046: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-28 13:28:31,048: INFO/MainProcess] VPN rotated — retrying a12bc041-5341-4f6c-bce9-338f023b7fb8/en with CloudScraper.
[2026-03-28 13:28:33,953: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:28:42,998: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:28:42,998: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-28 13:29:24,105: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d lang=es: SUCCESS
[2026-03-28 13:29:26,986: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-28 13:29:39,494: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-28 13:29:44,315: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-28 13:29:59,124: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-28 13:30:05,405: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-28 13:30:16,228: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-28 13:30:16,229: INFO/MainProcess] CloudScraper failed for d7704d4b-a617-4f66-8424-21c14805159d/de — trying Selenium.
[2026-03-28 13:30:42,949: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-28 13:30:57,738: INFO/MainProcess] Selenium retry 2 -- waiting 14s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:32:26,374: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-28 13:32:40,918: INFO/MainProcess] Selenium retry 3 -- waiting 32s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:34:28,312: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-28 13:34:28,313: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-28 13:34:28,339: WARNING/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 lang=en: FAILED
[2026-03-28 13:34:31,098: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-28 13:34:40,594: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-28 13:34:45,418: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-28 13:34:59,438: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-28 13:35:05,662: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-28 13:35:14,329: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-28 13:35:14,329: INFO/MainProcess] CloudScraper failed for a12bc041-5341-4f6c-bce9-338f023b7fb8/es — trying Selenium.
[2026-03-28 13:35:46,604: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d lang=de: SUCCESS
[2026-03-28 13:35:49,602: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-28 13:36:02,455: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-28 13:36:07,370: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-28 13:36:18,425: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-28 13:36:24,641: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-28 13:36:36,147: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-28 13:36:36,147: INFO/MainProcess] CloudScraper failed for d7704d4b-a617-4f66-8424-21c14805159d/it — trying Selenium.
[2026-03-28 13:37:03,803: INFO/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 lang=es: SUCCESS
[2026-03-28 13:37:06,639: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:37:17,513: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:37:22,459: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:37:36,887: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:37:43,105: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:37:57,199: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:37:57,199: INFO/MainProcess] CloudScraper failed for a12bc041-5341-4f6c-bce9-338f023b7fb8/de — trying Selenium.
[2026-03-28 13:38:34,692: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d lang=it: SUCCESS
[2026-03-28 13:38:37,564: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-28 13:38:48,480: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-28 13:38:53,224: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-28 13:39:05,175: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-28 13:39:11,426: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-28 13:39:25,075: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-28 13:39:25,076: INFO/MainProcess] CloudScraper failed for d7704d4b-a617-4f66-8424-21c14805159d/fr — trying Selenium.
[2026-03-28 13:39:51,707: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-28 13:40:06,249: INFO/MainProcess] Selenium retry 2 -- waiting 24s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:41:45,096: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-28 13:41:58,754: INFO/MainProcess] Selenium retry 3 -- waiting 28s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:43:41,935: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-28 13:43:41,936: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:43:41,937: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure a12bc041-5341-4f6c-bce9-338f023b7fb8/de
[2026-03-28 13:43:41,938: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-28 13:43:42,898: INFO/MainProcess] VPN disconnected.
[2026-03-28 13:43:47,899: INFO/MainProcess] VPN: connecting to Italy (IT)...
[2026-03-28 13:44:06,821: INFO/MainProcess] VPN connected to Italy — IP: 194.34.233.22
[2026-03-28 13:44:06,821: INFO/MainProcess] VPN rotation successful → Italy
[2026-03-28 13:44:06,823: INFO/MainProcess] VPN rotated — retrying a12bc041-5341-4f6c-bce9-338f023b7fb8/de with CloudScraper.
[2026-03-28 13:44:09,717: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:44:22,912: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:44:22,912: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-28 13:45:00,584: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d lang=fr: SUCCESS
[2026-03-28 13:45:03,425: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-28 13:45:35,146: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-28 13:45:40,015: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-28 13:45:51,279: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-28 13:45:57,460: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-28 13:46:12,147: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-28 13:46:12,147: INFO/MainProcess] CloudScraper failed for d7704d4b-a617-4f66-8424-21c14805159d/pt — trying Selenium.
[2026-03-28 13:46:20,093: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-28 13:46:31,161: INFO/MainProcess] Selenium retry 2 -- waiting 15s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:48:00,860: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-28 13:48:14,966: INFO/MainProcess] Selenium retry 3 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:49:52,776: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-28 13:49:52,776: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-28 13:49:52,801: WARNING/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 lang=de: FAILED
[2026-03-28 13:49:55,579: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:50:04,063: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:50:08,846: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:50:17,100: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:50:23,283: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:50:36,101: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:50:36,103: INFO/MainProcess] CloudScraper failed for a12bc041-5341-4f6c-bce9-338f023b7fb8/it — trying Selenium.
[2026-03-28 13:51:10,665: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d lang=pt: SUCCESS
[2026-03-28 13:51:10,667: INFO/MainProcess] URL d7704d4b-a617-4f66-8424-21c14805159d: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 13:51:13,392: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-28 13:51:24,399: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-28 13:51:29,198: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-28 13:51:39,941: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-28 13:51:46,136: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-28 13:52:00,725: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-28 13:52:00,726: INFO/MainProcess] CloudScraper failed for 0d3a7d06-2d69-4d0b-8e03-2b794358977e/en — trying Selenium.
[2026-03-28 13:52:29,882: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-28 13:52:40,567: INFO/MainProcess] Selenium retry 2 -- waiting 12s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:54:07,376: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-28 13:54:16,491: INFO/MainProcess] Selenium retry 3 -- waiting 34s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:56:05,112: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-28 13:56:05,112: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:56:05,114: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure a12bc041-5341-4f6c-bce9-338f023b7fb8/it
[2026-03-28 13:56:05,114: INFO/MainProcess] VPN: rotating (current=IT)...
[2026-03-28 13:56:08,976: INFO/MainProcess] VPN disconnected.
[2026-03-28 13:56:13,976: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-28 13:56:34,002: INFO/MainProcess] VPN connected to Sweden — IP: 193.46.242.152
[2026-03-28 13:56:34,002: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-28 13:56:34,004: INFO/MainProcess] VPN rotated — retrying a12bc041-5341-4f6c-bce9-338f023b7fb8/it with CloudScraper.
[2026-03-28 13:56:36,932: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:56:47,274: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 13:56:47,275: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-28 13:58:24,784: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 13:58:26,714: INFO/MainProcess] Gallery: 113 images loaded after scroll
[2026-03-28 13:58:30,400: INFO/MainProcess] Gallery: 120 unique image URLs extracted
[2026-03-28 13:58:30,533: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 13:58:30,533: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 13:58:58,545: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 0d3a7d06-2d69-4d0b-8e03-2b794358977e
[2026-03-28 13:59:07,641: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel a865bc46-4262-4a41-8235-6d49456c65d9
[2026-03-28 13:59:07,642: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel a865bc46-4262-4a41-8235-6d49456c65d9
[2026-03-28 13:59:07,649: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e lang=en: SUCCESS
[2026-03-28 13:59:10,607: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-28 13:59:25,245: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-28 13:59:30,222: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-28 13:59:45,081: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-28 13:59:51,283: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-28 14:00:04,977: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-28 14:00:04,977: INFO/MainProcess] CloudScraper failed for 0d3a7d06-2d69-4d0b-8e03-2b794358977e/es — trying Selenium.
[2026-03-28 14:00:16,516: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-28 14:00:24,657: INFO/MainProcess] Selenium retry 2 -- waiting 21s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 14:02:00,269: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-28 14:02:14,412: INFO/MainProcess] Selenium retry 3 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 14:03:49,662: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-28 14:03:49,663: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-28 14:03:49,674: WARNING/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 lang=it: FAILED
[2026-03-28 14:03:52,399: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:04:04,718: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:04:09,932: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:04:24,007: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:04:30,228: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:04:44,402: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:04:44,403: INFO/MainProcess] CloudScraper failed for a12bc041-5341-4f6c-bce9-338f023b7fb8/fr — trying Selenium.
[2026-03-28 14:05:07,445: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e lang=es: SUCCESS
[2026-03-28 14:05:10,283: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-28 14:05:23,455: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-28 14:05:28,381: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-28 14:05:37,373: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-28 14:05:43,602: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-28 14:05:52,155: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-28 14:05:52,156: INFO/MainProcess] CloudScraper failed for 0d3a7d06-2d69-4d0b-8e03-2b794358977e/de — trying Selenium.
[2026-03-28 14:06:25,217: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-28 14:06:38,227: INFO/MainProcess] Selenium retry 2 -- waiting 14s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:08:06,808: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-28 14:08:18,146: INFO/MainProcess] Selenium retry 3 -- waiting 25s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:09:57,825: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-28 14:09:57,825: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:09:57,827: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure a12bc041-5341-4f6c-bce9-338f023b7fb8/fr
[2026-03-28 14:09:57,827: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-28 14:09:58,786: INFO/MainProcess] VPN disconnected.
[2026-03-28 14:10:03,787: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-28 14:10:22,770: INFO/MainProcess] VPN connected to Germany — IP: 91.214.65.5
[2026-03-28 14:10:22,771: INFO/MainProcess] VPN rotation successful → Germany
[2026-03-28 14:10:22,772: INFO/MainProcess] VPN rotated — retrying a12bc041-5341-4f6c-bce9-338f023b7fb8/fr with CloudScraper.
[2026-03-28 14:10:25,485: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:10:37,189: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:10:37,189: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-28 14:11:17,524: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e lang=de: SUCCESS
[2026-03-28 14:11:20,439: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-28 14:11:30,378: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-28 14:11:35,209: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-28 14:11:47,868: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-28 14:11:54,039: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-28 14:12:03,810: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-28 14:12:03,811: INFO/MainProcess] CloudScraper failed for 0d3a7d06-2d69-4d0b-8e03-2b794358977e/it — trying Selenium.
[2026-03-28 14:12:33,757: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-28 14:12:48,118: INFO/MainProcess] Selenium retry 2 -- waiting 21s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:14:23,840: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-28 14:14:37,634: INFO/MainProcess] Selenium retry 3 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:16:12,566: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-28 14:16:12,567: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-28 14:16:12,575: WARNING/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 lang=fr: FAILED
[2026-03-28 14:16:15,381: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:16:30,021: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:16:34,889: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:16:48,489: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:16:54,663: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:17:05,824: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:17:05,824: INFO/MainProcess] CloudScraper failed for a12bc041-5341-4f6c-bce9-338f023b7fb8/pt — trying Selenium.
[2026-03-28 14:17:29,911: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e lang=it: SUCCESS
[2026-03-28 14:17:32,611: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-28 14:18:08,956: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-28 14:18:13,738: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-28 14:18:37,041: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-28 14:18:43,235: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-28 14:18:47,941: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-28 14:19:01,593: INFO/MainProcess] Selenium retry 2 -- waiting 13s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:19:07,530: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-28 14:19:07,531: INFO/MainProcess] CloudScraper failed for 0d3a7d06-2d69-4d0b-8e03-2b794358977e/fr — trying Selenium.
[2026-03-28 14:20:29,909: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-28 14:20:40,618: INFO/MainProcess] Selenium retry 3 -- waiting 19s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:22:14,228: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-28 14:22:14,229: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:22:14,230: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure a12bc041-5341-4f6c-bce9-338f023b7fb8/pt
[2026-03-28 14:22:14,231: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-28 14:22:15,249: INFO/MainProcess] VPN disconnected.
[2026-03-28 14:22:20,249: INFO/MainProcess] VPN: connecting to Canada (CA)...
[2026-03-28 14:22:39,393: INFO/MainProcess] VPN connected to Canada — IP: 212.15.86.247
[2026-03-28 14:22:39,393: INFO/MainProcess] VPN rotation successful → Canada
[2026-03-28 14:22:39,395: INFO/MainProcess] VPN rotated — retrying a12bc041-5341-4f6c-bce9-338f023b7fb8/pt with CloudScraper.
[2026-03-28 14:22:42,399: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:22:50,899: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:22:50,899: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-28 14:23:32,898: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e lang=fr: SUCCESS
[2026-03-28 14:23:35,845: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:23:45,396: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:23:50,364: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:24:03,852: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:24:10,035: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:24:21,976: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:24:21,977: INFO/MainProcess] CloudScraper failed for 0d3a7d06-2d69-4d0b-8e03-2b794358977e/pt — trying Selenium.
[2026-03-28 14:24:51,038: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-28 14:24:59,566: INFO/MainProcess] Selenium retry 2 -- waiting 19s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:26:34,369: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-28 14:26:48,319: INFO/MainProcess] Selenium retry 3 -- waiting 18s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:28:22,883: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-28 14:28:22,884: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-28 14:28:22,946: WARNING/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 lang=pt: FAILED
[2026-03-28 14:28:22,948: WARNING/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8: PARTIAL — Incomplete: 1/6 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr', 'pt']
[2026-03-28 14:28:22,953: INFO/MainProcess] URL a12bc041-5341-4f6c-bce9-338f023b7fb8 marked incomplete — data PRESERVED. ok=['es'] fail=['en', 'de', 'it', 'fr', 'pt']
[2026-03-28 14:28:25,808: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-28 14:28:37,479: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-28 14:28:42,385: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-28 14:28:52,871: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-28 14:28:59,051: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-28 14:29:11,687: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-28 14:29:11,688: INFO/MainProcess] CloudScraper failed for 4a47abd4-e587-4091-b770-2a0ad9280e15/en — trying Selenium.
[2026-03-28 14:29:42,033: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e lang=pt: SUCCESS
[2026-03-28 14:29:42,036: INFO/MainProcess] URL 0d3a7d06-2d69-4d0b-8e03-2b794358977e: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 14:29:45,033: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-28 14:29:53,991: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-28 14:29:58,901: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-28 14:30:09,097: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-28 14:30:15,276: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-28 14:30:24,954: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-28 14:30:24,954: INFO/MainProcess] CloudScraper failed for 73e168e3-06d5-4615-9a3b-45fb836b4d15/en — trying Selenium.
[2026-03-28 14:32:04,402: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 14:32:06,484: INFO/MainProcess] Gallery: 40 images loaded after scroll
[2026-03-28 14:32:08,792: INFO/MainProcess] Gallery: 47 unique image URLs extracted
[2026-03-28 14:32:08,916: INFO/MainProcess] hotelPhotos JS: 40 photos extracted from page source
[2026-03-28 14:32:08,917: INFO/MainProcess] Gallery: 40 photos with full metadata (hotelPhotos JS)
[2026-03-28 14:32:35,436: INFO/MainProcess] Photos: 40 rich photo records (hotelPhotos JS) for 4a47abd4-e587-4091-b770-2a0ad9280e15
[2026-03-28 14:32:56,290: INFO/MainProcess] download_photo_batch: 120/120 photo-files saved for hotel 6560ba78-a55a-484f-a55f-7bde6b8113e4
[2026-03-28 14:32:56,290: INFO/MainProcess] ImageDownloader (photo_batch): 120/40 photos saved for hotel 6560ba78-a55a-484f-a55f-7bde6b8113e4
[2026-03-28 14:32:56,296: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15 lang=en: SUCCESS
[2026-03-28 14:32:59,552: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-28 14:33:14,349: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-28 14:33:19,504: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-28 14:33:32,058: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-28 14:33:38,237: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-28 14:33:47,236: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-28 14:33:47,237: INFO/MainProcess] CloudScraper failed for 4a47abd4-e587-4091-b770-2a0ad9280e15/es — trying Selenium.
[2026-03-28 14:34:58,529: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 14:35:00,598: INFO/MainProcess] Gallery: 57 images loaded after scroll
[2026-03-28 14:35:02,332: INFO/MainProcess] Gallery: 64 unique image URLs extracted
[2026-03-28 14:35:02,450: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 14:35:02,452: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 14:35:28,599: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 73e168e3-06d5-4615-9a3b-45fb836b4d15
[2026-03-28 14:35:47,468: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 5857a320-7410-4ac0-88a1-f6284957718c
[2026-03-28 14:35:47,468: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 5857a320-7410-4ac0-88a1-f6284957718c
[2026-03-28 14:35:47,472: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15 lang=en: SUCCESS
[2026-03-28 14:35:50,589: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-28 14:36:00,471: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-28 14:36:05,573: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-28 14:36:19,377: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-28 14:36:25,558: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-28 14:36:36,885: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-28 14:36:36,885: INFO/MainProcess] CloudScraper failed for 73e168e3-06d5-4615-9a3b-45fb836b4d15/es — trying Selenium.
[2026-03-28 14:36:49,537: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15 lang=es: SUCCESS
[2026-03-28 14:36:52,657: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-28 14:37:01,286: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-28 14:37:06,345: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-28 14:37:15,201: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-28 14:37:21,379: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-28 14:37:36,149: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-28 14:37:36,149: INFO/MainProcess] CloudScraper failed for 4a47abd4-e587-4091-b770-2a0ad9280e15/de — trying Selenium.
[2026-03-28 14:38:07,515: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15 lang=es: SUCCESS
[2026-03-28 14:38:10,398: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:38:22,603: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:38:27,684: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:38:41,341: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:38:47,520: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:39:00,733: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:39:00,733: INFO/MainProcess] CloudScraper failed for 73e168e3-06d5-4615-9a3b-45fb836b4d15/de — trying Selenium.
[2026-03-28 14:39:26,490: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15 lang=de: SUCCESS
[2026-03-28 14:39:29,365: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-28 14:39:39,532: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-28 14:39:44,436: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-28 14:39:56,947: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-28 14:40:03,123: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-28 14:40:18,092: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-28 14:40:18,093: INFO/MainProcess] CloudScraper failed for 4a47abd4-e587-4091-b770-2a0ad9280e15/it — trying Selenium.
[2026-03-28 14:41:12,869: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-28 14:41:12,869: INFO/MainProcess] Selenium retry 2 -- waiting 19s -- https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-28 14:42:48,493: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15 lang=de: SUCCESS
[2026-03-28 14:42:51,384: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-28 14:43:03,037: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-28 14:43:07,923: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-28 14:43:19,630: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-28 14:43:25,807: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-28 14:43:37,667: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-28 14:43:37,668: INFO/MainProcess] CloudScraper failed for 73e168e3-06d5-4615-9a3b-45fb836b4d15/it — trying Selenium.
[2026-03-28 14:44:07,551: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15 lang=it: SUCCESS
[2026-03-28 14:44:10,436: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:44:20,189: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:44:25,592: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:44:39,134: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:44:45,313: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:44:55,640: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:44:55,640: INFO/MainProcess] CloudScraper failed for 4a47abd4-e587-4091-b770-2a0ad9280e15/fr — trying Selenium.
[2026-03-28 14:45:28,446: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15 lang=it: SUCCESS
[2026-03-28 14:45:31,407: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-28 14:45:39,856: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-28 14:45:44,805: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-28 14:45:58,167: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-28 14:46:04,344: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-28 14:46:19,316: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-28 14:46:19,317: INFO/MainProcess] CloudScraper failed for 73e168e3-06d5-4615-9a3b-45fb836b4d15/fr — trying Selenium.
[2026-03-28 14:47:15,086: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-28 14:47:15,087: INFO/MainProcess] Selenium retry 2 -- waiting 22s -- https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-28 14:48:52,965: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15 lang=fr: SUCCESS
[2026-03-28 14:48:55,858: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:49:04,883: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:49:09,841: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:49:17,894: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:49:24,071: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:49:33,162: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-28 14:49:33,162: INFO/MainProcess] CloudScraper failed for 4a47abd4-e587-4091-b770-2a0ad9280e15/pt — trying Selenium.
[2026-03-28 14:50:13,586: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15 lang=fr: SUCCESS
[2026-03-28 14:50:16,625: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:50:26,129: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:50:31,071: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:50:39,953: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:50:46,130: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:50:55,544: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:50:55,544: INFO/MainProcess] CloudScraper failed for 73e168e3-06d5-4615-9a3b-45fb836b4d15/pt — trying Selenium.
[2026-03-28 14:51:34,488: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15 lang=pt: SUCCESS
[2026-03-28 14:51:34,491: INFO/MainProcess] URL 4a47abd4-e587-4091-b770-2a0ad9280e15: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 14:51:37,546: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-28 14:51:46,539: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-28 14:51:51,381: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-28 14:52:00,019: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-28 14:52:06,196: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-28 14:52:15,015: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-28 14:52:15,015: INFO/MainProcess] CloudScraper failed for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583/en — trying Selenium.
[2026-03-28 14:53:21,262: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-28 14:53:21,262: INFO/MainProcess] Selenium retry 2 -- waiting 22s -- https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-28 14:54:59,756: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15 lang=pt: SUCCESS
[2026-03-28 14:54:59,760: INFO/MainProcess] URL 73e168e3-06d5-4615-9a3b-45fb836b4d15: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 14:55:02,711: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-28 14:55:13,841: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-28 14:55:18,768: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-28 14:55:27,609: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-28 14:55:33,797: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-28 14:55:46,111: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-28 14:55:46,112: INFO/MainProcess] CloudScraper failed for 85572d7b-3d83-4e48-ae2d-fd478ff660f2/en — trying Selenium.
[2026-03-28 14:57:20,671: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 14:57:22,704: INFO/MainProcess] Gallery: 70 images loaded after scroll
[2026-03-28 14:57:25,810: INFO/MainProcess] Gallery: 77 unique image URLs extracted
[2026-03-28 14:57:25,968: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-28 14:57:25,968: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-28 14:57:52,781: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583
[2026-03-28 14:58:19,493: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 4b90cce1-5bdb-4729-95d4-4b615e91039a
[2026-03-28 14:58:19,493: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 4b90cce1-5bdb-4729-95d4-4b615e91039a
[2026-03-28 14:58:19,499: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583 lang=en: SUCCESS
[2026-03-28 14:58:22,538: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-28 14:58:32,182: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-28 14:58:37,063: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-28 14:58:49,561: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-28 14:58:55,738: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-28 14:59:07,776: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-28 14:59:07,776: INFO/MainProcess] CloudScraper failed for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583/es — trying Selenium.
[2026-03-28 15:00:14,702: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-28 15:00:16,650: INFO/MainProcess] Gallery: 34 images loaded after scroll
[2026-03-28 15:00:18,979: INFO/MainProcess] Gallery: 41 unique image URLs extracted
[2026-03-28 15:00:19,095: INFO/MainProcess] hotelPhotos JS: 34 photos extracted from page source
[2026-03-28 15:00:19,095: INFO/MainProcess] Gallery: 34 photos with full metadata (hotelPhotos JS)
[2026-03-28 15:00:46,723: INFO/MainProcess] Photos: 34 rich photo records (hotelPhotos JS) for 85572d7b-3d83-4e48-ae2d-fd478ff660f2
[2026-03-28 15:01:05,724: INFO/MainProcess] download_photo_batch: 102/102 photo-files saved for hotel c4722e81-935d-4491-b237-e78a41c3100a
[2026-03-28 15:01:05,724: INFO/MainProcess] ImageDownloader (photo_batch): 102/34 photos saved for hotel c4722e81-935d-4491-b237-e78a41c3100a
[2026-03-28 15:01:05,730: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2 lang=en: SUCCESS
[2026-03-28 15:01:08,858: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-28 15:01:19,003: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-28 15:01:24,052: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-28 15:01:36,799: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-28 15:01:42,976: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-28 15:01:53,530: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-28 15:01:53,531: INFO/MainProcess] CloudScraper failed for 85572d7b-3d83-4e48-ae2d-fd478ff660f2/es — trying Selenium.
[2026-03-28 15:02:05,500: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583 lang=es: SUCCESS
[2026-03-28 15:02:08,572: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-28 15:02:22,516: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-28 15:02:27,553: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-28 15:02:40,878: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-28 15:02:47,056: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-28 15:02:55,936: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-28 15:02:55,937: INFO/MainProcess] CloudScraper failed for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583/de — trying Selenium.
[2026-03-28 15:03:25,186: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2 lang=es: SUCCESS
[2026-03-28 15:03:28,048: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:03:40,504: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:03:45,571: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:03:58,182: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:04:04,360: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:04:17,488: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:04:17,488: INFO/MainProcess] CloudScraper failed for 85572d7b-3d83-4e48-ae2d-fd478ff660f2/de — trying Selenium.
[2026-03-28 15:04:48,461: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583 lang=de: SUCCESS
[2026-03-28 15:04:51,348: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-28 15:05:04,053: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-28 15:05:09,082: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-28 15:05:22,039: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-28 15:05:28,220: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-28 15:05:36,522: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-28 15:05:36,523: INFO/MainProcess] CloudScraper failed for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583/it — trying Selenium.
[2026-03-28 15:06:35,221: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-28 15:06:35,222: INFO/MainProcess] Selenium retry 2 -- waiting 23s -- https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-28 15:08:14,348: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2 lang=de: SUCCESS
[2026-03-28 15:08:17,388: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-28 15:08:31,945: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-28 15:08:37,021: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-28 15:08:48,350: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-28 15:08:54,529: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-28 15:09:05,686: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-28 15:09:05,686: INFO/MainProcess] CloudScraper failed for 85572d7b-3d83-4e48-ae2d-fd478ff660f2/it — trying Selenium.
[2026-03-28 15:09:34,952: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583 lang=it: SUCCESS
[2026-03-28 15:09:37,821: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:09:50,610: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:09:55,715: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:10:04,152: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:10:10,334: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:10:19,942: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:10:19,943: INFO/MainProcess] CloudScraper failed for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583/fr — trying Selenium.
[2026-03-28 15:10:54,682: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2 lang=it: SUCCESS
[2026-03-28 15:10:57,609: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-28 15:11:11,076: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-28 15:11:16,303: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-28 15:11:29,663: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-28 15:11:35,847: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-28 15:11:44,809: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-28 15:11:44,810: INFO/MainProcess] CloudScraper failed for 85572d7b-3d83-4e48-ae2d-fd478ff660f2/fr — trying Selenium.
[2026-03-28 15:12:40,012: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-28 15:12:40,012: INFO/MainProcess] Selenium retry 2 -- waiting 13s -- https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-28 15:14:09,724: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583 lang=fr: SUCCESS
[2026-03-28 15:14:12,695: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-28 15:14:21,928: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-28 15:14:26,820: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-28 15:14:41,281: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-28 15:14:47,462: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-28 15:14:59,971: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-28 15:14:59,971: INFO/MainProcess] CloudScraper failed for 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583/pt — trying Selenium.
[2026-03-28 15:15:27,755: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2 lang=fr: SUCCESS
[2026-03-28 15:15:30,701: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:15:41,771: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:15:46,653: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:16:01,347: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:16:07,528: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:16:22,081: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:16:22,082: INFO/MainProcess] CloudScraper failed for 85572d7b-3d83-4e48-ae2d-fd478ff660f2/pt — trying Selenium.
[2026-03-28 15:16:47,042: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583 lang=pt: SUCCESS
[2026-03-28 15:16:47,045: INFO/MainProcess] URL 5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 15:18:33,439: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-28 15:18:33,439: INFO/MainProcess] Selenium retry 2 -- waiting 16s -- https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-28 15:20:05,850: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2 lang=pt: SUCCESS
[2026-03-28 15:20:05,852: INFO/MainProcess] URL 85572d7b-3d83-4e48-ae2d-fd478ff660f2: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-28 15:20:08,126: INFO/MainProcess] Selenium browser closed after batch completion.
[2026-03-28 15:20:08,126: INFO/MainProcess] scrape_pending_urls: batch complete — {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-28 15:20:08,129: INFO/MainProcess] Task tasks.scrape_pending_urls[e129043f-f0f0-42f9-a111-41209e52ebb4] succeeded in 10774.644343000022s: {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-28 15:20:08,438: INFO/MainProcess] Task tasks.collect_system_metrics[6cfaebea-4f77-4e83-8ce9-15f503e71180] received
[2026-03-28 15:20:08,963: INFO/MainProcess] Task tasks.collect_system_metrics[6cfaebea-4f77-4e83-8ce9-15f503e71180] succeeded in 0.523852999904193s: {'cpu': 14.6, 'memory': 45.5}
[2026-03-28 15:20:08,965: INFO/MainProcess] Task tasks.purge_old_debug_html[1b977034-23a2-45c2-9ebe-d10e73d72964] received
[2026-03-28 15:20:08,967: INFO/MainProcess] Task tasks.purge_old_debug_html[1b977034-23a2-45c2-9ebe-d10e73d72964] succeeded in 0.0018534999107941985s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-28 15:20:08,970: INFO/MainProcess] Task tasks.scrape_pending_urls[97f33f78-d642-4b12-b8d3-4d1e8584da62] received
[2026-03-28 15:20:08,974: INFO/MainProcess] Task tasks.scrape_pending_urls[97f33f78-d642-4b12-b8d3-4d1e8584da62] succeeded in 0.003731600008904934s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:08,976: INFO/MainProcess] Task tasks.collect_system_metrics[9ece01a8-acc6-4d5b-a903-f667a4d6c661] received
[2026-03-28 15:20:09,496: INFO/MainProcess] Task tasks.collect_system_metrics[9ece01a8-acc6-4d5b-a903-f667a4d6c661] succeeded in 0.519616000005044s: {'cpu': 13.2, 'memory': 45.3}
[2026-03-28 15:20:09,498: INFO/MainProcess] Task tasks.reset_stale_processing_urls[1bf5b6a3-cd5d-4fbc-89c6-e2501867cee0] received
[2026-03-28 15:20:09,503: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:20:09,504: INFO/MainProcess] Task tasks.reset_stale_processing_urls[1bf5b6a3-cd5d-4fbc-89c6-e2501867cee0] succeeded in 0.005576499970629811s: {'reset': 0}
[2026-03-28 15:20:09,506: INFO/MainProcess] Task tasks.scrape_pending_urls[7bb39cda-3cbd-476e-9bbe-7c2981727cc5] received
[2026-03-28 15:20:09,511: INFO/MainProcess] Task tasks.scrape_pending_urls[7bb39cda-3cbd-476e-9bbe-7c2981727cc5] succeeded in 0.004262300091795623s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:09,513: INFO/MainProcess] Task tasks.collect_system_metrics[7355693d-2579-473b-8f77-a92f4be7e735] received
[2026-03-28 15:20:10,030: INFO/MainProcess] Task tasks.collect_system_metrics[7355693d-2579-473b-8f77-a92f4be7e735] succeeded in 0.5168457999825478s: {'cpu': 14.7, 'memory': 45.4}
[2026-03-28 15:20:10,032: INFO/MainProcess] Task tasks.reset_stale_processing_urls[16e77976-7b67-460d-bf8e-5b905ae2883c] received
[2026-03-28 15:20:10,035: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:20:10,036: INFO/MainProcess] Task tasks.reset_stale_processing_urls[16e77976-7b67-460d-bf8e-5b905ae2883c] succeeded in 0.0035264999605715275s: {'reset': 0}
[2026-03-28 15:20:10,038: INFO/MainProcess] Task tasks.scrape_pending_urls[516fe1ac-9ae0-4a6a-97be-0cf05e94828d] received
[2026-03-28 15:20:10,050: INFO/MainProcess] Task tasks.scrape_pending_urls[516fe1ac-9ae0-4a6a-97be-0cf05e94828d] succeeded in 0.011705899960361421s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:10,054: INFO/MainProcess] Task tasks.collect_system_metrics[bb0e7753-9a04-49ac-a376-7f7b84e8003d] received
[2026-03-28 15:20:10,569: INFO/MainProcess] Task tasks.collect_system_metrics[bb0e7753-9a04-49ac-a376-7f7b84e8003d] succeeded in 0.5147417000262067s: {'cpu': 8.0, 'memory': 45.4}
[2026-03-28 15:20:10,572: INFO/MainProcess] Task tasks.purge_old_debug_html[08e68c9a-0169-498b-b06f-bce434f9bbfc] received
[2026-03-28 15:20:10,574: INFO/MainProcess] Task tasks.purge_old_debug_html[08e68c9a-0169-498b-b06f-bce434f9bbfc] succeeded in 0.001518900040537119s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-28 15:20:10,575: INFO/MainProcess] Task tasks.scrape_pending_urls[f3612327-9758-462e-a696-1e4f785d8d57] received
[2026-03-28 15:20:10,579: INFO/MainProcess] Task tasks.scrape_pending_urls[f3612327-9758-462e-a696-1e4f785d8d57] succeeded in 0.003113199956715107s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:10,581: INFO/MainProcess] Task tasks.collect_system_metrics[d1d33ef9-711f-4904-9989-13312e201107] received
[2026-03-28 15:20:11,098: INFO/MainProcess] Task tasks.collect_system_metrics[d1d33ef9-711f-4904-9989-13312e201107] succeeded in 0.5172763000009581s: {'cpu': 5.2, 'memory': 45.4}
[2026-03-28 15:20:11,101: INFO/MainProcess] Task tasks.reset_stale_processing_urls[91913a6a-6229-4061-a912-d5c5fe2518cd] received
[2026-03-28 15:20:11,103: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:20:11,104: INFO/MainProcess] Task tasks.reset_stale_processing_urls[91913a6a-6229-4061-a912-d5c5fe2518cd] succeeded in 0.0035277000861242414s: {'reset': 0}
[2026-03-28 15:20:11,106: INFO/MainProcess] Task tasks.scrape_pending_urls[d885c2ec-4e5a-4c36-a976-8cd4e250e864] received
[2026-03-28 15:20:11,111: INFO/MainProcess] Task tasks.scrape_pending_urls[d885c2ec-4e5a-4c36-a976-8cd4e250e864] succeeded in 0.004211399937048554s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:11,113: INFO/MainProcess] Task tasks.collect_system_metrics[6bca26f6-4de8-48d2-8db0-53a6143c12d3] received
[2026-03-28 15:20:11,631: INFO/MainProcess] Task tasks.collect_system_metrics[6bca26f6-4de8-48d2-8db0-53a6143c12d3] succeeded in 0.5174143000040203s: {'cpu': 6.4, 'memory': 45.4}
[2026-03-28 15:20:11,633: INFO/MainProcess] Task tasks.reset_stale_processing_urls[a78154b4-ae3a-4e58-b15e-1edfc91aa1d9] received
[2026-03-28 15:20:11,636: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:20:11,637: INFO/MainProcess] Task tasks.reset_stale_processing_urls[a78154b4-ae3a-4e58-b15e-1edfc91aa1d9] succeeded in 0.0036622999468818307s: {'reset': 0}
[2026-03-28 15:20:11,639: INFO/MainProcess] Task tasks.scrape_pending_urls[1d634a1c-b362-4e4b-a967-80ea0a5aa56b] received
[2026-03-28 15:20:11,642: INFO/MainProcess] Task tasks.scrape_pending_urls[1d634a1c-b362-4e4b-a967-80ea0a5aa56b] succeeded in 0.0029142999555915594s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:11,644: INFO/MainProcess] Task tasks.collect_system_metrics[9383b2de-d9c0-4553-ad19-ccaf29280d81] received
[2026-03-28 15:20:12,151: INFO/MainProcess] Task tasks.collect_system_metrics[9383b2de-d9c0-4553-ad19-ccaf29280d81] succeeded in 0.5062881000339985s: {'cpu': 7.1, 'memory': 45.4}
[2026-03-28 15:20:12,153: INFO/MainProcess] Task tasks.purge_old_debug_html[1144ac06-8ecc-4fdf-a343-91b8d772edce] received
[2026-03-28 15:20:12,155: INFO/MainProcess] Task tasks.purge_old_debug_html[1144ac06-8ecc-4fdf-a343-91b8d772edce] succeeded in 0.0021144000347703695s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-28 15:20:12,158: INFO/MainProcess] Task tasks.scrape_pending_urls[02731f67-2adb-471f-8187-9459a51a9e6b] received
[2026-03-28 15:20:12,161: INFO/MainProcess] Task tasks.scrape_pending_urls[02731f67-2adb-471f-8187-9459a51a9e6b] succeeded in 0.003230700036510825s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:12,163: INFO/MainProcess] Task tasks.collect_system_metrics[42267d51-3b40-4238-b533-3b58302291bd] received
[2026-03-28 15:20:12,681: INFO/MainProcess] Task tasks.collect_system_metrics[42267d51-3b40-4238-b533-3b58302291bd] succeeded in 0.5177823000121862s: {'cpu': 9.1, 'memory': 45.4}
[2026-03-28 15:20:12,684: INFO/MainProcess] Task tasks.reset_stale_processing_urls[09f932b2-d7de-4923-b44e-ab696370eb4e] received
[2026-03-28 15:20:12,687: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:20:12,688: INFO/MainProcess] Task tasks.reset_stale_processing_urls[09f932b2-d7de-4923-b44e-ab696370eb4e] succeeded in 0.003961700014770031s: {'reset': 0}
[2026-03-28 15:20:12,690: INFO/MainProcess] Task tasks.scrape_pending_urls[6d9d2a84-20dc-4d31-a5b3-ec0f01618a24] received
[2026-03-28 15:20:12,694: INFO/MainProcess] Task tasks.scrape_pending_urls[6d9d2a84-20dc-4d31-a5b3-ec0f01618a24] succeeded in 0.0036322999512776732s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:12,697: INFO/MainProcess] Task tasks.collect_system_metrics[2c6a1195-6bca-413f-b1a8-25791ab4085b] received
[2026-03-28 15:20:13,213: INFO/MainProcess] Task tasks.collect_system_metrics[2c6a1195-6bca-413f-b1a8-25791ab4085b] succeeded in 0.5164317999733612s: {'cpu': 2.4, 'memory': 45.4}
[2026-03-28 15:20:13,216: INFO/MainProcess] Task tasks.reset_stale_processing_urls[909924fe-1797-4853-8d44-d2a0e2b3e309] received
[2026-03-28 15:20:13,218: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:20:13,220: INFO/MainProcess] Task tasks.reset_stale_processing_urls[909924fe-1797-4853-8d44-d2a0e2b3e309] succeeded in 0.003692900063470006s: {'reset': 0}
[2026-03-28 15:20:13,222: INFO/MainProcess] Task tasks.scrape_pending_urls[d333a17e-d698-49d0-88a1-640ddea5dde4] received
[2026-03-28 15:20:13,226: INFO/MainProcess] Task tasks.scrape_pending_urls[d333a17e-d698-49d0-88a1-640ddea5dde4] succeeded in 0.0036512999795377254s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:13,228: INFO/MainProcess] Task tasks.collect_system_metrics[7865a778-a24d-4f09-a39b-29fbb725218f] received
[2026-03-28 15:20:13,745: INFO/MainProcess] Task tasks.collect_system_metrics[7865a778-a24d-4f09-a39b-29fbb725218f] succeeded in 0.5171529999934137s: {'cpu': 4.4, 'memory': 45.4}
[2026-03-28 15:20:13,748: INFO/MainProcess] Task tasks.scrape_pending_urls[09eb7357-26d7-4747-8cad-6db2bb6b21a8] received
[2026-03-28 15:20:13,752: INFO/MainProcess] Task tasks.scrape_pending_urls[09eb7357-26d7-4747-8cad-6db2bb6b21a8] succeeded in 0.0038641999708488584s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:13,754: INFO/MainProcess] Task tasks.collect_system_metrics[1459c412-fe4b-4e15-ad9d-4867b6e85b17] received
[2026-03-28 15:20:14,272: INFO/MainProcess] Task tasks.collect_system_metrics[1459c412-fe4b-4e15-ad9d-4867b6e85b17] succeeded in 0.5173483999678865s: {'cpu': 7.1, 'memory': 45.4}
[2026-03-28 15:20:14,274: INFO/MainProcess] Task tasks.scrape_pending_urls[eec06d6a-7c68-4c03-9593-7e08f60c180a] received
[2026-03-28 15:20:14,278: INFO/MainProcess] Task tasks.scrape_pending_urls[eec06d6a-7c68-4c03-9593-7e08f60c180a] succeeded in 0.003274100017733872s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:14,280: INFO/MainProcess] Task tasks.collect_system_metrics[8c60104f-a56c-4907-bc4f-34ac55ae365e] received
[2026-03-28 15:20:14,798: INFO/MainProcess] Task tasks.collect_system_metrics[8c60104f-a56c-4907-bc4f-34ac55ae365e] succeeded in 0.517547499970533s: {'cpu': 16.0, 'memory': 45.4}
[2026-03-28 15:20:14,801: INFO/MainProcess] Task tasks.scrape_pending_urls[a7cae58f-efdc-45f0-b181-7740d5fb8511] received
[2026-03-28 15:20:14,804: INFO/MainProcess] Task tasks.scrape_pending_urls[a7cae58f-efdc-45f0-b181-7740d5fb8511] succeeded in 0.003320200019516051s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:14,806: INFO/MainProcess] Task tasks.collect_system_metrics[47fa42bd-edd5-49a7-88ab-09022eff14cb] received
[2026-03-28 15:20:15,316: INFO/MainProcess] Task tasks.collect_system_metrics[47fa42bd-edd5-49a7-88ab-09022eff14cb] succeeded in 0.5089406999759376s: {'cpu': 4.7, 'memory': 45.5}
[2026-03-28 15:20:15,318: INFO/MainProcess] Task tasks.scrape_pending_urls[9dc2c326-7997-48b7-bb4f-95ed4321b391] received
[2026-03-28 15:20:15,321: INFO/MainProcess] Task tasks.scrape_pending_urls[9dc2c326-7997-48b7-bb4f-95ed4321b391] succeeded in 0.0030412001069635153s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:15,323: INFO/MainProcess] Task tasks.collect_system_metrics[d5b5954e-ebda-4d14-8e8d-4ed4bc01841f] received
[2026-03-28 15:20:15,841: INFO/MainProcess] Task tasks.collect_system_metrics[d5b5954e-ebda-4d14-8e8d-4ed4bc01841f] succeeded in 0.517554400023073s: {'cpu': 13.6, 'memory': 45.5}
[2026-03-28 15:20:15,843: INFO/MainProcess] Task tasks.scrape_pending_urls[83c5927a-ca8f-43fa-9b70-77b4cb013fda] received
[2026-03-28 15:20:15,848: INFO/MainProcess] Task tasks.scrape_pending_urls[83c5927a-ca8f-43fa-9b70-77b4cb013fda] succeeded in 0.0036732000298798084s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:15,850: INFO/MainProcess] Task tasks.collect_system_metrics[0973e77e-86ab-4cba-805b-2423a64a35da] received
[2026-03-28 15:20:16,367: INFO/MainProcess] Task tasks.collect_system_metrics[0973e77e-86ab-4cba-805b-2423a64a35da] succeeded in 0.5170201000291854s: {'cpu': 29.3, 'memory': 45.5}
[2026-03-28 15:20:16,369: INFO/MainProcess] Task tasks.scrape_pending_urls[e4206722-44fb-44b9-8f8b-6295fe87f09a] received
[2026-03-28 15:20:16,373: INFO/MainProcess] Task tasks.scrape_pending_urls[e4206722-44fb-44b9-8f8b-6295fe87f09a] succeeded in 0.003598199924454093s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:16,375: INFO/MainProcess] Task tasks.collect_system_metrics[88fbd320-a590-4975-bbde-d88115a5ed15] received
[2026-03-28 15:20:16,892: INFO/MainProcess] Task tasks.collect_system_metrics[88fbd320-a590-4975-bbde-d88115a5ed15] succeeded in 0.5170307999942452s: {'cpu': 18.9, 'memory': 45.5}
[2026-03-28 15:20:16,894: INFO/MainProcess] Task tasks.scrape_pending_urls[f0a4af7b-bec1-428e-8588-b6aef55e0d8a] received
[2026-03-28 15:20:16,898: INFO/MainProcess] Task tasks.scrape_pending_urls[f0a4af7b-bec1-428e-8588-b6aef55e0d8a] succeeded in 0.0035435999743640423s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:16,900: INFO/MainProcess] Task tasks.collect_system_metrics[3f3ac0d5-6418-4609-8fdb-1ae1e023e3e8] received
[2026-03-28 15:20:17,417: INFO/MainProcess] Task tasks.collect_system_metrics[3f3ac0d5-6418-4609-8fdb-1ae1e023e3e8] succeeded in 0.516554499976337s: {'cpu': 7.0, 'memory': 45.5}
[2026-03-28 15:20:17,419: INFO/MainProcess] Task tasks.scrape_pending_urls[f7b73c8b-dbca-4bc4-b543-08029407dc2c] received
[2026-03-28 15:20:17,422: INFO/MainProcess] Task tasks.scrape_pending_urls[f7b73c8b-dbca-4bc4-b543-08029407dc2c] succeeded in 0.0028539999620988965s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:17,424: INFO/MainProcess] Task tasks.collect_system_metrics[5de7964b-d6e9-4d5d-a4c3-0510fb7b70ae] received
[2026-03-28 15:20:17,942: INFO/MainProcess] Task tasks.collect_system_metrics[5de7964b-d6e9-4d5d-a4c3-0510fb7b70ae] succeeded in 0.5176899000070989s: {'cpu': 3.1, 'memory': 45.5}
[2026-03-28 15:20:17,944: INFO/MainProcess] Task tasks.scrape_pending_urls[561e0e92-9a66-4560-a8a7-d10af24edcc6] received
[2026-03-28 15:20:17,948: INFO/MainProcess] Task tasks.scrape_pending_urls[561e0e92-9a66-4560-a8a7-d10af24edcc6] succeeded in 0.0032808000687509775s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:17,950: INFO/MainProcess] Task tasks.collect_system_metrics[a815eeb4-4283-4d0c-995c-33c2734e4604] received
[2026-03-28 15:20:18,467: INFO/MainProcess] Task tasks.collect_system_metrics[a815eeb4-4283-4d0c-995c-33c2734e4604] succeeded in 0.5172801000298932s: {'cpu': 5.4, 'memory': 45.5}
[2026-03-28 15:20:18,469: INFO/MainProcess] Task tasks.scrape_pending_urls[807ec09b-5f85-47d4-896a-19330d5d5d9a] received
[2026-03-28 15:20:18,473: INFO/MainProcess] Task tasks.scrape_pending_urls[807ec09b-5f85-47d4-896a-19330d5d5d9a] succeeded in 0.0028435999993234873s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:18,474: INFO/MainProcess] Task tasks.collect_system_metrics[81eff3ea-4689-4c6a-a5f5-40015d9b3aed] received
[2026-03-28 15:20:18,981: INFO/MainProcess] Task tasks.collect_system_metrics[81eff3ea-4689-4c6a-a5f5-40015d9b3aed] succeeded in 0.5062274999218062s: {'cpu': 9.9, 'memory': 45.5}
[2026-03-28 15:20:18,983: INFO/MainProcess] Task tasks.scrape_pending_urls[f17fa6ab-850f-4d80-8ef1-af77909c9556] received
[2026-03-28 15:20:18,987: INFO/MainProcess] Task tasks.scrape_pending_urls[f17fa6ab-850f-4d80-8ef1-af77909c9556] succeeded in 0.003223499981686473s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:18,989: INFO/MainProcess] Task tasks.collect_system_metrics[caadba80-2ef8-4449-b24b-59a3cc430b5c] received
[2026-03-28 15:20:19,507: INFO/MainProcess] Task tasks.collect_system_metrics[caadba80-2ef8-4449-b24b-59a3cc430b5c] succeeded in 0.5175507999956608s: {'cpu': 11.6, 'memory': 45.5}
[2026-03-28 15:20:19,509: INFO/MainProcess] Task tasks.scrape_pending_urls[26bdc70c-d35f-4c6a-848c-4dc59ae07ce9] received
[2026-03-28 15:20:19,513: INFO/MainProcess] Task tasks.scrape_pending_urls[26bdc70c-d35f-4c6a-848c-4dc59ae07ce9] succeeded in 0.003249499946832657s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:19,515: INFO/MainProcess] Task tasks.collect_system_metrics[d00cf76c-04a7-459f-927e-e004d6983eb3] received
[2026-03-28 15:20:20,032: INFO/MainProcess] Task tasks.collect_system_metrics[d00cf76c-04a7-459f-927e-e004d6983eb3] succeeded in 0.5166439999593422s: {'cpu': 7.0, 'memory': 45.6}
[2026-03-28 15:20:20,034: INFO/MainProcess] Task tasks.scrape_pending_urls[de0ecf91-21f0-457b-9b15-f315291df0bc] received
[2026-03-28 15:20:20,038: INFO/MainProcess] Task tasks.scrape_pending_urls[de0ecf91-21f0-457b-9b15-f315291df0bc] succeeded in 0.0034260000102221966s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:20,040: INFO/MainProcess] Task tasks.collect_system_metrics[75ceae27-7147-4efc-a1a4-4d9774f32bea] received
[2026-03-28 15:20:20,558: INFO/MainProcess] Task tasks.collect_system_metrics[75ceae27-7147-4efc-a1a4-4d9774f32bea] succeeded in 0.5181126999668777s: {'cpu': 7.6, 'memory': 45.6}
[2026-03-28 15:20:20,561: INFO/MainProcess] Task tasks.scrape_pending_urls[48f815a8-beeb-4465-a6be-3de7535a9fc2] received
[2026-03-28 15:20:20,565: INFO/MainProcess] Task tasks.scrape_pending_urls[48f815a8-beeb-4465-a6be-3de7535a9fc2] succeeded in 0.003331500105559826s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:20,567: INFO/MainProcess] Task tasks.collect_system_metrics[1d86ea48-3c64-45e9-8afc-07a2c3339aa1] received
[2026-03-28 15:20:21,084: INFO/MainProcess] Task tasks.collect_system_metrics[1d86ea48-3c64-45e9-8afc-07a2c3339aa1] succeeded in 0.5171502000885084s: {'cpu': 9.0, 'memory': 45.5}
[2026-03-28 15:20:21,086: INFO/MainProcess] Task tasks.scrape_pending_urls[aa3ae01f-8295-4275-b688-bf9192f1b3b8] received
[2026-03-28 15:20:21,090: INFO/MainProcess] Task tasks.scrape_pending_urls[aa3ae01f-8295-4275-b688-bf9192f1b3b8] succeeded in 0.0034645000705495477s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:21,092: INFO/MainProcess] Task tasks.collect_system_metrics[49a46109-2e3a-404f-ac09-42f021d9680b] received
[2026-03-28 15:20:21,609: INFO/MainProcess] Task tasks.collect_system_metrics[49a46109-2e3a-404f-ac09-42f021d9680b] succeeded in 0.5168822000268847s: {'cpu': 5.8, 'memory': 45.5}
[2026-03-28 15:20:21,612: INFO/MainProcess] Task tasks.scrape_pending_urls[5af982f0-1301-43ce-803c-ef3e1bd85ce3] received
[2026-03-28 15:20:21,615: INFO/MainProcess] Task tasks.scrape_pending_urls[5af982f0-1301-43ce-803c-ef3e1bd85ce3] succeeded in 0.00316770002245903s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:21,617: INFO/MainProcess] Task tasks.collect_system_metrics[3a5ad213-233a-4989-9658-586186528ea2] received
[2026-03-28 15:20:22,127: INFO/MainProcess] Task tasks.collect_system_metrics[3a5ad213-233a-4989-9658-586186528ea2] succeeded in 0.5093786999350414s: {'cpu': 7.9, 'memory': 45.5}
[2026-03-28 15:20:22,129: INFO/MainProcess] Task tasks.scrape_pending_urls[49aef953-e45a-4912-b5bc-8cbcbfaf77c6] received
[2026-03-28 15:20:22,132: INFO/MainProcess] Task tasks.scrape_pending_urls[49aef953-e45a-4912-b5bc-8cbcbfaf77c6] succeeded in 0.002856900100596249s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:22,134: INFO/MainProcess] Task tasks.collect_system_metrics[ac9836b6-edfe-4d5d-abc9-ca1e6d207562] received
[2026-03-28 15:20:22,652: INFO/MainProcess] Task tasks.collect_system_metrics[ac9836b6-edfe-4d5d-abc9-ca1e6d207562] succeeded in 0.517199800000526s: {'cpu': 2.8, 'memory': 45.5}
[2026-03-28 15:20:22,654: INFO/MainProcess] Task tasks.scrape_pending_urls[58d2fd18-6f1a-490d-9bee-84f8d0be4241] received
[2026-03-28 15:20:22,658: INFO/MainProcess] Task tasks.scrape_pending_urls[58d2fd18-6f1a-490d-9bee-84f8d0be4241] succeeded in 0.0034302999265491962s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:22,660: INFO/MainProcess] Task tasks.collect_system_metrics[a56d27df-e283-4efe-84df-1f89a5ea15ab] received
[2026-03-28 15:20:23,177: INFO/MainProcess] Task tasks.collect_system_metrics[a56d27df-e283-4efe-84df-1f89a5ea15ab] succeeded in 0.5172891000984237s: {'cpu': 11.6, 'memory': 45.5}
[2026-03-28 15:20:23,180: INFO/MainProcess] Task tasks.scrape_pending_urls[f18096a5-8114-48cf-825b-2b56c57757f5] received
[2026-03-28 15:20:23,184: INFO/MainProcess] Task tasks.scrape_pending_urls[f18096a5-8114-48cf-825b-2b56c57757f5] succeeded in 0.003409500000998378s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:23,186: INFO/MainProcess] Task tasks.collect_system_metrics[20f58194-649a-46cb-8cf2-fa7bb0505455] received
[2026-03-28 15:20:23,703: INFO/MainProcess] Task tasks.collect_system_metrics[20f58194-649a-46cb-8cf2-fa7bb0505455] succeeded in 0.5171841999981552s: {'cpu': 4.3, 'memory': 45.5}
[2026-03-28 15:20:23,706: INFO/MainProcess] Task tasks.scrape_pending_urls[3e1b8d35-a93f-4e32-bd83-df9c0d0f283d] received
[2026-03-28 15:20:23,709: INFO/MainProcess] Task tasks.scrape_pending_urls[3e1b8d35-a93f-4e32-bd83-df9c0d0f283d] succeeded in 0.0030703000957146287s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:23,711: INFO/MainProcess] Task tasks.collect_system_metrics[ceedc198-7224-4102-82a3-e9a33b4a21e2] received
[2026-03-28 15:20:24,229: INFO/MainProcess] Task tasks.collect_system_metrics[ceedc198-7224-4102-82a3-e9a33b4a21e2] succeeded in 0.5171887000324205s: {'cpu': 5.8, 'memory': 45.5}
[2026-03-28 15:20:24,231: INFO/MainProcess] Task tasks.scrape_pending_urls[e40f58b9-dbe1-4f17-89ee-d7cd19758a7b] received
[2026-03-28 15:20:24,235: INFO/MainProcess] Task tasks.scrape_pending_urls[e40f58b9-dbe1-4f17-89ee-d7cd19758a7b] succeeded in 0.003282099962234497s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:24,236: INFO/MainProcess] Task tasks.collect_system_metrics[cedf020c-3618-4674-a97f-54c91b6640fb] received
[2026-03-28 15:20:24,753: INFO/MainProcess] Task tasks.collect_system_metrics[cedf020c-3618-4674-a97f-54c91b6640fb] succeeded in 0.5159531000535935s: {'cpu': 14.3, 'memory': 45.6}
[2026-03-28 15:20:24,755: INFO/MainProcess] Task tasks.scrape_pending_urls[a9f35e93-f9a6-42ca-84cb-6bd09db7b512] received
[2026-03-28 15:20:24,758: INFO/MainProcess] Task tasks.scrape_pending_urls[a9f35e93-f9a6-42ca-84cb-6bd09db7b512] succeeded in 0.002753900014795363s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:24,760: INFO/MainProcess] Task tasks.collect_system_metrics[aae5a141-943b-4e5a-9e7d-e926c19724fb] received
[2026-03-28 15:20:25,277: INFO/MainProcess] Task tasks.collect_system_metrics[aae5a141-943b-4e5a-9e7d-e926c19724fb] succeeded in 0.5167551999911666s: {'cpu': 2.8, 'memory': 45.5}
[2026-03-28 15:20:25,279: INFO/MainProcess] Task tasks.scrape_pending_urls[83701041-47b0-4ccb-8a94-8ad096fbe4a8] received
[2026-03-28 15:20:25,283: INFO/MainProcess] Task tasks.scrape_pending_urls[83701041-47b0-4ccb-8a94-8ad096fbe4a8] succeeded in 0.0035340000176802278s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:25,285: INFO/MainProcess] Task tasks.collect_system_metrics[736dc8a0-734d-49ba-92a1-6bfb5752b6e2] received
[2026-03-28 15:20:25,802: INFO/MainProcess] Task tasks.collect_system_metrics[736dc8a0-734d-49ba-92a1-6bfb5752b6e2] succeeded in 0.5166364000178874s: {'cpu': 10.5, 'memory': 45.6}
[2026-03-28 15:20:25,804: INFO/MainProcess] Task tasks.scrape_pending_urls[85d0a136-4c36-402f-a522-e751763a5ab6] received
[2026-03-28 15:20:25,807: INFO/MainProcess] Task tasks.scrape_pending_urls[85d0a136-4c36-402f-a522-e751763a5ab6] succeeded in 0.002773699932731688s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:25,809: INFO/MainProcess] Task tasks.collect_system_metrics[74ffc0df-36dc-4730-8c5b-2c9d14b3e16a] received
[2026-03-28 15:20:26,326: INFO/MainProcess] Task tasks.collect_system_metrics[74ffc0df-36dc-4730-8c5b-2c9d14b3e16a] succeeded in 0.5163460999028757s: {'cpu': 6.2, 'memory': 45.6}
[2026-03-28 15:20:26,328: INFO/MainProcess] Task tasks.scrape_pending_urls[0575a3b7-eafc-4073-a918-e721de4410a5] received
[2026-03-28 15:20:26,332: INFO/MainProcess] Task tasks.scrape_pending_urls[0575a3b7-eafc-4073-a918-e721de4410a5] succeeded in 0.0029829000122845173s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:26,333: INFO/MainProcess] Task tasks.collect_system_metrics[65dd14fe-2f60-4042-9213-304a00e18684] received
[2026-03-28 15:20:26,850: INFO/MainProcess] Task tasks.collect_system_metrics[65dd14fe-2f60-4042-9213-304a00e18684] succeeded in 0.5167444000253454s: {'cpu': 5.9, 'memory': 45.6}
[2026-03-28 15:20:26,853: INFO/MainProcess] Task tasks.scrape_pending_urls[15e96d6b-ae87-4b65-91c9-7099e791c5e4] received
[2026-03-28 15:20:26,856: INFO/MainProcess] Task tasks.scrape_pending_urls[15e96d6b-ae87-4b65-91c9-7099e791c5e4] succeeded in 0.0028855999698862433s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:26,858: INFO/MainProcess] Task tasks.collect_system_metrics[95ca5a60-7275-4a3f-825d-3cba6fe48dd0] received
[2026-03-28 15:20:27,375: INFO/MainProcess] Task tasks.collect_system_metrics[95ca5a60-7275-4a3f-825d-3cba6fe48dd0] succeeded in 0.5169825999764726s: {'cpu': 8.9, 'memory': 45.6}
[2026-03-28 15:20:27,377: INFO/MainProcess] Task tasks.scrape_pending_urls[20ebaf24-dbad-4fcc-813b-4c937e8a38f6] received
[2026-03-28 15:20:27,381: INFO/MainProcess] Task tasks.scrape_pending_urls[20ebaf24-dbad-4fcc-813b-4c937e8a38f6] succeeded in 0.0033016999950632453s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,383: INFO/MainProcess] Task tasks.scrape_pending_urls[31bfa234-7af1-43c6-822b-d27e27398003] received
[2026-03-28 15:20:27,387: INFO/MainProcess] Task tasks.scrape_pending_urls[31bfa234-7af1-43c6-822b-d27e27398003] succeeded in 0.004142999998293817s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,389: INFO/MainProcess] Task tasks.scrape_pending_urls[685bef70-41eb-45ba-aa98-2988865aef98] received
[2026-03-28 15:20:27,392: INFO/MainProcess] Task tasks.scrape_pending_urls[685bef70-41eb-45ba-aa98-2988865aef98] succeeded in 0.002708100015297532s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,393: INFO/MainProcess] Task tasks.scrape_pending_urls[76b1b392-e962-4c8f-85a7-4d1fb2df6be5] received
[2026-03-28 15:20:27,396: INFO/MainProcess] Task tasks.scrape_pending_urls[76b1b392-e962-4c8f-85a7-4d1fb2df6be5] succeeded in 0.002621099934913218s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,398: INFO/MainProcess] Task tasks.scrape_pending_urls[01d72b75-2374-4b51-aff6-24d142da566d] received
[2026-03-28 15:20:27,402: INFO/MainProcess] Task tasks.scrape_pending_urls[01d72b75-2374-4b51-aff6-24d142da566d] succeeded in 0.003919599927030504s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,404: INFO/MainProcess] Task tasks.scrape_pending_urls[144210cb-3c79-467d-adf9-64ee507ab324] received
[2026-03-28 15:20:27,408: INFO/MainProcess] Task tasks.scrape_pending_urls[144210cb-3c79-467d-adf9-64ee507ab324] succeeded in 0.0032260000007227063s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,409: INFO/MainProcess] Task tasks.scrape_pending_urls[e0ca77e6-9875-442c-b102-1d79804bc874] received
[2026-03-28 15:20:27,413: INFO/MainProcess] Task tasks.scrape_pending_urls[e0ca77e6-9875-442c-b102-1d79804bc874] succeeded in 0.00313510000705719s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,415: INFO/MainProcess] Task tasks.scrape_pending_urls[9e7a307a-b3f5-40b3-a255-3c226db33503] received
[2026-03-28 15:20:27,420: INFO/MainProcess] Task tasks.scrape_pending_urls[9e7a307a-b3f5-40b3-a255-3c226db33503] succeeded in 0.004634600016288459s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,421: INFO/MainProcess] Task tasks.scrape_pending_urls[70e19ef9-1532-4fc8-ba0a-4b02438305ac] received
[2026-03-28 15:20:27,424: INFO/MainProcess] Task tasks.scrape_pending_urls[70e19ef9-1532-4fc8-ba0a-4b02438305ac] succeeded in 0.0026688999496400356s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,426: INFO/MainProcess] Task tasks.scrape_pending_urls[188ca497-9e53-4db8-ad08-a3cb479b4ed8] received
[2026-03-28 15:20:27,429: INFO/MainProcess] Task tasks.scrape_pending_urls[188ca497-9e53-4db8-ad08-a3cb479b4ed8] succeeded in 0.0027269000420346856s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,432: INFO/MainProcess] Task tasks.scrape_pending_urls[eac1dca8-48d1-415b-b9b2-4e4b9ab30fc8] received
[2026-03-28 15:20:27,436: INFO/MainProcess] Task tasks.scrape_pending_urls[eac1dca8-48d1-415b-b9b2-4e4b9ab30fc8] succeeded in 0.003136300016194582s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,438: INFO/MainProcess] Task tasks.scrape_pending_urls[b5add8fa-c050-4148-922b-be113052e483] received
[2026-03-28 15:20:27,441: INFO/MainProcess] Task tasks.scrape_pending_urls[b5add8fa-c050-4148-922b-be113052e483] succeeded in 0.0027729999274015427s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,443: INFO/MainProcess] Task tasks.scrape_pending_urls[44e13539-e0f5-49a9-a101-6cdccb8ddfd3] received
[2026-03-28 15:20:27,446: INFO/MainProcess] Task tasks.scrape_pending_urls[44e13539-e0f5-49a9-a101-6cdccb8ddfd3] succeeded in 0.0026786000235006213s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,448: INFO/MainProcess] Task tasks.scrape_pending_urls[aa814ac2-cc53-4136-9bb1-915550ac0cdf] received
[2026-03-28 15:20:27,451: INFO/MainProcess] Task tasks.scrape_pending_urls[aa814ac2-cc53-4136-9bb1-915550ac0cdf] succeeded in 0.0032463000388816s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,453: INFO/MainProcess] Task tasks.scrape_pending_urls[b20907c9-be5f-4666-9d29-ef7a9dcb433a] received
[2026-03-28 15:20:27,456: INFO/MainProcess] Task tasks.scrape_pending_urls[b20907c9-be5f-4666-9d29-ef7a9dcb433a] succeeded in 0.0024341000244021416s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,457: INFO/MainProcess] Task tasks.scrape_pending_urls[39562fd4-880e-4739-9db7-83f955e23960] received
[2026-03-28 15:20:27,460: INFO/MainProcess] Task tasks.scrape_pending_urls[39562fd4-880e-4739-9db7-83f955e23960] succeeded in 0.0023482999531552196s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,461: INFO/MainProcess] Task tasks.scrape_pending_urls[22d434ea-9abd-4023-b58b-96e6cba51d5b] received
[2026-03-28 15:20:27,465: INFO/MainProcess] Task tasks.scrape_pending_urls[22d434ea-9abd-4023-b58b-96e6cba51d5b] succeeded in 0.003923699958249927s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,467: INFO/MainProcess] Task tasks.scrape_pending_urls[ec617078-fa6e-44bc-bbe6-395eaae2cfba] received
[2026-03-28 15:20:27,470: INFO/MainProcess] Task tasks.scrape_pending_urls[ec617078-fa6e-44bc-bbe6-395eaae2cfba] succeeded in 0.0027837000088766217s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,472: INFO/MainProcess] Task tasks.scrape_pending_urls[f0e11790-8f89-4909-ba5f-7c61d4acce12] received
[2026-03-28 15:20:27,475: INFO/MainProcess] Task tasks.scrape_pending_urls[f0e11790-8f89-4909-ba5f-7c61d4acce12] succeeded in 0.0023110000183805823s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,476: INFO/MainProcess] Task tasks.scrape_pending_urls[c104b103-cf69-4369-9332-6b5b97f623d7] received
[2026-03-28 15:20:27,478: INFO/MainProcess] Task tasks.scrape_pending_urls[c104b103-cf69-4369-9332-6b5b97f623d7] succeeded in 0.002256999956443906s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,481: INFO/MainProcess] Task tasks.scrape_pending_urls[9c1f7b1a-8106-43f0-b247-cdd8d0026b07] received
[2026-03-28 15:20:27,484: INFO/MainProcess] Task tasks.scrape_pending_urls[9c1f7b1a-8106-43f0-b247-cdd8d0026b07] succeeded in 0.0026368999388068914s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,485: INFO/MainProcess] Task tasks.scrape_pending_urls[e5b7a35e-e966-4f1a-bda5-5978f4db1209] received
[2026-03-28 15:20:27,488: INFO/MainProcess] Task tasks.scrape_pending_urls[e5b7a35e-e966-4f1a-bda5-5978f4db1209] succeeded in 0.002318299957551062s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,489: INFO/MainProcess] Task tasks.scrape_pending_urls[512e31e0-290b-4c5b-9b8e-df11bd9ff798] received
[2026-03-28 15:20:27,492: INFO/MainProcess] Task tasks.scrape_pending_urls[512e31e0-290b-4c5b-9b8e-df11bd9ff798] succeeded in 0.002314200042746961s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,493: INFO/MainProcess] Task tasks.scrape_pending_urls[bfa9189f-dae4-48eb-8269-4872f41c0905] received
[2026-03-28 15:20:27,497: INFO/MainProcess] Task tasks.scrape_pending_urls[bfa9189f-dae4-48eb-8269-4872f41c0905] succeeded in 0.003939600079320371s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,499: INFO/MainProcess] Task tasks.scrape_pending_urls[88cccea5-bd7a-465b-8593-33fee80241c0] received
[2026-03-28 15:20:27,503: INFO/MainProcess] Task tasks.scrape_pending_urls[88cccea5-bd7a-465b-8593-33fee80241c0] succeeded in 0.002991899964399636s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,504: INFO/MainProcess] Task tasks.scrape_pending_urls[f4cd1bca-bae5-4d88-9cd7-c3fa31ea0788] received
[2026-03-28 15:20:27,507: INFO/MainProcess] Task tasks.scrape_pending_urls[f4cd1bca-bae5-4d88-9cd7-c3fa31ea0788] succeeded in 0.0024082999443635345s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,508: INFO/MainProcess] Task tasks.scrape_pending_urls[598771c3-4fa1-4e00-9cff-d45495ea3ee8] received
[2026-03-28 15:20:27,512: INFO/MainProcess] Task tasks.scrape_pending_urls[598771c3-4fa1-4e00-9cff-d45495ea3ee8] succeeded in 0.0036331999581307173s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,514: INFO/MainProcess] Task tasks.scrape_pending_urls[8c3f941e-5d3d-4728-9d45-c93455b5b9ca] received
[2026-03-28 15:20:27,518: INFO/MainProcess] Task tasks.scrape_pending_urls[8c3f941e-5d3d-4728-9d45-c93455b5b9ca] succeeded in 0.003066500066779554s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,519: INFO/MainProcess] Task tasks.scrape_pending_urls[42d7b86d-ac41-4fbb-b3b3-fea6f9d5c91c] received
[2026-03-28 15:20:27,522: INFO/MainProcess] Task tasks.scrape_pending_urls[42d7b86d-ac41-4fbb-b3b3-fea6f9d5c91c] succeeded in 0.0027667999966070056s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,524: INFO/MainProcess] Task tasks.scrape_pending_urls[81b10007-23b6-497e-8176-1c0f94193cf2] received
[2026-03-28 15:20:27,526: INFO/MainProcess] Task tasks.scrape_pending_urls[81b10007-23b6-497e-8176-1c0f94193cf2] succeeded in 0.002049200003966689s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,529: INFO/MainProcess] Task tasks.scrape_pending_urls[95a2f4c3-f627-4286-9fe2-59d824d0026e] received
[2026-03-28 15:20:27,533: INFO/MainProcess] Task tasks.scrape_pending_urls[95a2f4c3-f627-4286-9fe2-59d824d0026e] succeeded in 0.0033327999990433455s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,534: INFO/MainProcess] Task tasks.scrape_pending_urls[2ba673a7-4245-4c71-ae64-05f79deaffc9] received
[2026-03-28 15:20:27,537: INFO/MainProcess] Task tasks.scrape_pending_urls[2ba673a7-4245-4c71-ae64-05f79deaffc9] succeeded in 0.002190500032156706s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,538: INFO/MainProcess] Task tasks.scrape_pending_urls[93995a9e-20eb-4081-8686-e9a2eaed8b4e] received
[2026-03-28 15:20:27,540: INFO/MainProcess] Task tasks.scrape_pending_urls[93995a9e-20eb-4081-8686-e9a2eaed8b4e] succeeded in 0.002118899952620268s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,542: INFO/MainProcess] Task tasks.scrape_pending_urls[84d644fd-40bb-45f4-853b-2fdbd574069b] received
[2026-03-28 15:20:27,545: INFO/MainProcess] Task tasks.scrape_pending_urls[84d644fd-40bb-45f4-853b-2fdbd574069b] succeeded in 0.0033297999761998653s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,547: INFO/MainProcess] Task tasks.scrape_pending_urls[32ff4c67-07cb-4f09-bd60-3cd92dffdcbb] received
[2026-03-28 15:20:27,550: INFO/MainProcess] Task tasks.scrape_pending_urls[32ff4c67-07cb-4f09-bd60-3cd92dffdcbb] succeeded in 0.0024513000389561057s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,551: INFO/MainProcess] Task tasks.scrape_pending_urls[12078cc7-d845-4003-a06f-77bf9508fc48] received
[2026-03-28 15:20:27,553: INFO/MainProcess] Task tasks.scrape_pending_urls[12078cc7-d845-4003-a06f-77bf9508fc48] succeeded in 0.0021286000264808536s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,555: INFO/MainProcess] Task tasks.scrape_pending_urls[1a418620-5b47-4365-832e-ddab72b35f2b] received
[2026-03-28 15:20:27,557: INFO/MainProcess] Task tasks.scrape_pending_urls[1a418620-5b47-4365-832e-ddab72b35f2b] succeeded in 0.0021025999449193478s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,558: INFO/MainProcess] Task tasks.scrape_pending_urls[d338a63f-9e6b-42e7-8864-2cca8669c574] received
[2026-03-28 15:20:27,562: INFO/MainProcess] Task tasks.scrape_pending_urls[d338a63f-9e6b-42e7-8864-2cca8669c574] succeeded in 0.0024273000890389085s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,563: INFO/MainProcess] Task tasks.scrape_pending_urls[a2604dce-ae2d-42ce-994f-022278dded4a] received
[2026-03-28 15:20:27,566: INFO/MainProcess] Task tasks.scrape_pending_urls[a2604dce-ae2d-42ce-994f-022278dded4a] succeeded in 0.0021370999747887254s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,567: INFO/MainProcess] Task tasks.scrape_pending_urls[c93005cf-c7ac-44b4-9f7a-5f08ace78ab6] received
[2026-03-28 15:20:27,569: INFO/MainProcess] Task tasks.scrape_pending_urls[c93005cf-c7ac-44b4-9f7a-5f08ace78ab6] succeeded in 0.002092299982905388s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,571: INFO/MainProcess] Task tasks.scrape_pending_urls[87ca991f-7868-44bb-8219-4a89fcfea776] received
[2026-03-28 15:20:27,573: INFO/MainProcess] Task tasks.scrape_pending_urls[87ca991f-7868-44bb-8219-4a89fcfea776] succeeded in 0.0020840999204665422s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,574: INFO/MainProcess] Task tasks.scrape_pending_urls[0add9a21-bfdf-4f13-b6af-08450fc341af] received
[2026-03-28 15:20:27,578: INFO/MainProcess] Task tasks.scrape_pending_urls[0add9a21-bfdf-4f13-b6af-08450fc341af] succeeded in 0.003912499989382923s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,580: INFO/MainProcess] Task tasks.scrape_pending_urls[536237dc-da4c-47a2-97ba-c4e1ff6b2327] received
[2026-03-28 15:20:27,583: INFO/MainProcess] Task tasks.scrape_pending_urls[536237dc-da4c-47a2-97ba-c4e1ff6b2327] succeeded in 0.0025170999579131603s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,584: INFO/MainProcess] Task tasks.scrape_pending_urls[66147674-ff83-462d-bf43-8c07ee3a0d51] received
[2026-03-28 15:20:27,587: INFO/MainProcess] Task tasks.scrape_pending_urls[66147674-ff83-462d-bf43-8c07ee3a0d51] succeeded in 0.0027913000667467713s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,589: INFO/MainProcess] Task tasks.scrape_pending_urls[f8736ea0-48d8-4ea1-87cd-d3d45ab537a8] received
[2026-03-28 15:20:27,592: INFO/MainProcess] Task tasks.scrape_pending_urls[f8736ea0-48d8-4ea1-87cd-d3d45ab537a8] succeeded in 0.003232099930755794s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,594: INFO/MainProcess] Task tasks.scrape_pending_urls[f5d5f4f4-e503-4018-a238-cf34f45eb869] received
[2026-03-28 15:20:27,597: INFO/MainProcess] Task tasks.scrape_pending_urls[f5d5f4f4-e503-4018-a238-cf34f45eb869] succeeded in 0.002359599922783673s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,598: INFO/MainProcess] Task tasks.scrape_pending_urls[cb245fac-9e62-43b5-80e4-5d0544e6482c] received
[2026-03-28 15:20:27,601: INFO/MainProcess] Task tasks.scrape_pending_urls[cb245fac-9e62-43b5-80e4-5d0544e6482c] succeeded in 0.002327699912711978s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,602: INFO/MainProcess] Task tasks.scrape_pending_urls[a1894c21-64f7-4f41-a781-6c05711f22f0] received
[2026-03-28 15:20:27,605: INFO/MainProcess] Task tasks.scrape_pending_urls[a1894c21-64f7-4f41-a781-6c05711f22f0] succeeded in 0.002301200060173869s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,607: INFO/MainProcess] Task tasks.scrape_pending_urls[c1ff494d-c02a-4c81-903a-1057fa546246] received
[2026-03-28 15:20:27,610: INFO/MainProcess] Task tasks.scrape_pending_urls[c1ff494d-c02a-4c81-903a-1057fa546246] succeeded in 0.0026675999397411942s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,612: INFO/MainProcess] Task tasks.scrape_pending_urls[e2739637-d588-49c8-80e4-20c7d519764d] received
[2026-03-28 15:20:27,614: INFO/MainProcess] Task tasks.scrape_pending_urls[e2739637-d588-49c8-80e4-20c7d519764d] succeeded in 0.002324800007045269s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,616: INFO/MainProcess] Task tasks.scrape_pending_urls[892f691d-d10a-4a34-b232-6d33e89b5428] received
[2026-03-28 15:20:27,618: INFO/MainProcess] Task tasks.scrape_pending_urls[892f691d-d10a-4a34-b232-6d33e89b5428] succeeded in 0.0022776999976485968s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,620: INFO/MainProcess] Task tasks.scrape_pending_urls[d768a5a1-2c82-427d-bb84-9ba52522b639] received
[2026-03-28 15:20:27,624: INFO/MainProcess] Task tasks.scrape_pending_urls[d768a5a1-2c82-427d-bb84-9ba52522b639] succeeded in 0.003707400057464838s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,626: INFO/MainProcess] Task tasks.scrape_pending_urls[69f0f995-9a68-4767-8712-f55a2e0953b8] received
[2026-03-28 15:20:27,630: INFO/MainProcess] Task tasks.scrape_pending_urls[69f0f995-9a68-4767-8712-f55a2e0953b8] succeeded in 0.0034035000717267394s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,632: INFO/MainProcess] Task tasks.scrape_pending_urls[ad179088-6140-4915-bc05-21d088523059] received
[2026-03-28 15:20:27,636: INFO/MainProcess] Task tasks.scrape_pending_urls[ad179088-6140-4915-bc05-21d088523059] succeeded in 0.0032689999788999557s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,638: INFO/MainProcess] Task tasks.scrape_pending_urls[100bc1c1-7455-495b-aa0c-d2fa0a58d42d] received
[2026-03-28 15:20:27,642: INFO/MainProcess] Task tasks.scrape_pending_urls[100bc1c1-7455-495b-aa0c-d2fa0a58d42d] succeeded in 0.0035389000549912453s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,644: INFO/MainProcess] Task tasks.scrape_pending_urls[f8de1f3d-7e45-49b5-abbd-15e9f2c2a835] received
[2026-03-28 15:20:27,648: INFO/MainProcess] Task tasks.scrape_pending_urls[f8de1f3d-7e45-49b5-abbd-15e9f2c2a835] succeeded in 0.003361099981702864s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,650: INFO/MainProcess] Task tasks.scrape_pending_urls[895e36ae-436b-4676-92b0-75b3cd6ecdb1] received
[2026-03-28 15:20:27,653: INFO/MainProcess] Task tasks.scrape_pending_urls[895e36ae-436b-4676-92b0-75b3cd6ecdb1] succeeded in 0.0035802999045699835s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,656: INFO/MainProcess] Task tasks.scrape_pending_urls[c368b357-73cc-48ad-9407-e553733da208] received
[2026-03-28 15:20:27,660: INFO/MainProcess] Task tasks.scrape_pending_urls[c368b357-73cc-48ad-9407-e553733da208] succeeded in 0.002816300024278462s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,661: INFO/MainProcess] Task tasks.scrape_pending_urls[24841680-e69e-4c3d-8934-96884c32ce0c] received
[2026-03-28 15:20:27,664: INFO/MainProcess] Task tasks.scrape_pending_urls[24841680-e69e-4c3d-8934-96884c32ce0c] succeeded in 0.0026036000344902277s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,665: INFO/MainProcess] Task tasks.scrape_pending_urls[ae5ba4f0-75ea-4726-8c7e-da74617f856a] received
[2026-03-28 15:20:27,668: INFO/MainProcess] Task tasks.scrape_pending_urls[ae5ba4f0-75ea-4726-8c7e-da74617f856a] succeeded in 0.002492200001142919s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,670: INFO/MainProcess] Task tasks.scrape_pending_urls[10574fea-e4ce-4483-8435-a153454272e9] received
[2026-03-28 15:20:27,674: INFO/MainProcess] Task tasks.scrape_pending_urls[10574fea-e4ce-4483-8435-a153454272e9] succeeded in 0.003163300105370581s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,675: INFO/MainProcess] Task tasks.scrape_pending_urls[dbfd37f1-6417-466a-9447-2d20add2159e] received
[2026-03-28 15:20:27,678: INFO/MainProcess] Task tasks.scrape_pending_urls[dbfd37f1-6417-466a-9447-2d20add2159e] succeeded in 0.002468799939379096s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,680: INFO/MainProcess] Task tasks.scrape_pending_urls[d96c492f-8b75-4a54-a67c-bd6441861079] received
[2026-03-28 15:20:27,683: INFO/MainProcess] Task tasks.scrape_pending_urls[d96c492f-8b75-4a54-a67c-bd6441861079] succeeded in 0.002424200065433979s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,684: INFO/MainProcess] Task tasks.scrape_pending_urls[f9c6515d-20b4-4be0-b586-d3cbfaa35345] received
[2026-03-28 15:20:27,688: INFO/MainProcess] Task tasks.scrape_pending_urls[f9c6515d-20b4-4be0-b586-d3cbfaa35345] succeeded in 0.003293600049801171s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,689: INFO/MainProcess] Task tasks.scrape_pending_urls[cf53bfc3-ec35-4f2d-96df-f5e25beef920] received
[2026-03-28 15:20:27,692: INFO/MainProcess] Task tasks.scrape_pending_urls[cf53bfc3-ec35-4f2d-96df-f5e25beef920] succeeded in 0.002344300039112568s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,693: INFO/MainProcess] Task tasks.scrape_pending_urls[cb3b4ed3-16a2-4fad-9998-a52cf3a120c5] received
[2026-03-28 15:20:27,696: INFO/MainProcess] Task tasks.scrape_pending_urls[cb3b4ed3-16a2-4fad-9998-a52cf3a120c5] succeeded in 0.0022995000472292304s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,698: INFO/MainProcess] Task tasks.scrape_pending_urls[face186b-ed19-43e4-ad90-a50aead0fdc3] received
[2026-03-28 15:20:27,700: INFO/MainProcess] Task tasks.scrape_pending_urls[face186b-ed19-43e4-ad90-a50aead0fdc3] succeeded in 0.0024695999454706907s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,703: INFO/MainProcess] Task tasks.scrape_pending_urls[e96c8933-465c-4b6d-a139-66b585b063b2] received
[2026-03-28 15:20:27,706: INFO/MainProcess] Task tasks.scrape_pending_urls[e96c8933-465c-4b6d-a139-66b585b063b2] succeeded in 0.0026681000599637628s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,708: INFO/MainProcess] Task tasks.scrape_pending_urls[598002e1-b8dc-4ff3-b08d-9b34bb387023] received
[2026-03-28 15:20:27,711: INFO/MainProcess] Task tasks.scrape_pending_urls[598002e1-b8dc-4ff3-b08d-9b34bb387023] succeeded in 0.002530299942009151s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,712: INFO/MainProcess] Task tasks.scrape_pending_urls[3234cd48-bc77-4417-96a5-6cd2d234cbcf] received
[2026-03-28 15:20:27,715: INFO/MainProcess] Task tasks.scrape_pending_urls[3234cd48-bc77-4417-96a5-6cd2d234cbcf] succeeded in 0.002453400054946542s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,718: INFO/MainProcess] Task tasks.scrape_pending_urls[7b961a28-5fd9-430b-8aed-b79c1f83d21b] received
[2026-03-28 15:20:27,721: INFO/MainProcess] Task tasks.scrape_pending_urls[7b961a28-5fd9-430b-8aed-b79c1f83d21b] succeeded in 0.0027640999760478735s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,723: INFO/MainProcess] Task tasks.scrape_pending_urls[52d66687-9103-4ac1-82df-9daaf35f61a8] received
[2026-03-28 15:20:27,726: INFO/MainProcess] Task tasks.scrape_pending_urls[52d66687-9103-4ac1-82df-9daaf35f61a8] succeeded in 0.00249810004606843s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,727: INFO/MainProcess] Task tasks.scrape_pending_urls[fa77abf6-9867-47d9-a6c5-6654c18d99f7] received
[2026-03-28 15:20:27,730: INFO/MainProcess] Task tasks.scrape_pending_urls[fa77abf6-9867-47d9-a6c5-6654c18d99f7] succeeded in 0.002449600026011467s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,731: INFO/MainProcess] Task tasks.scrape_pending_urls[1f316209-f479-4a2e-ab93-fe1e0c00aa30] received
[2026-03-28 15:20:27,735: INFO/MainProcess] Task tasks.scrape_pending_urls[1f316209-f479-4a2e-ab93-fe1e0c00aa30] succeeded in 0.0036784999538213015s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,737: INFO/MainProcess] Task tasks.scrape_pending_urls[69621bd1-1308-4fbf-91f8-e3c2249576b9] received
[2026-03-28 15:20:27,740: INFO/MainProcess] Task tasks.scrape_pending_urls[69621bd1-1308-4fbf-91f8-e3c2249576b9] succeeded in 0.002565799979493022s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,742: INFO/MainProcess] Task tasks.scrape_pending_urls[d7e5296e-ce96-47c9-9eba-36fdd159aa34] received
[2026-03-28 15:20:27,744: INFO/MainProcess] Task tasks.scrape_pending_urls[d7e5296e-ce96-47c9-9eba-36fdd159aa34] succeeded in 0.002483600052073598s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,746: INFO/MainProcess] Task tasks.scrape_pending_urls[a8ab3b0e-a24d-4f00-9353-a1974ffe0815] received
[2026-03-28 15:20:27,749: INFO/MainProcess] Task tasks.scrape_pending_urls[a8ab3b0e-a24d-4f00-9353-a1974ffe0815] succeeded in 0.002581499982625246s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,752: INFO/MainProcess] Task tasks.scrape_pending_urls[89f096d6-95cd-4a24-be90-62e808042a4d] received
[2026-03-28 15:20:27,755: INFO/MainProcess] Task tasks.scrape_pending_urls[89f096d6-95cd-4a24-be90-62e808042a4d] succeeded in 0.0030773000326007605s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,757: INFO/MainProcess] Task tasks.scrape_pending_urls[a95303cf-731b-4ee9-a638-c470e1326b1c] received
[2026-03-28 15:20:27,760: INFO/MainProcess] Task tasks.scrape_pending_urls[a95303cf-731b-4ee9-a638-c470e1326b1c] succeeded in 0.002535699983127415s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,761: INFO/MainProcess] Task tasks.scrape_pending_urls[6a397a54-85ea-429c-b081-1856be0755d0] received
[2026-03-28 15:20:27,764: INFO/MainProcess] Task tasks.scrape_pending_urls[6a397a54-85ea-429c-b081-1856be0755d0] succeeded in 0.0025382000021636486s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,766: INFO/MainProcess] Task tasks.scrape_pending_urls[ac7326ac-b92c-4b74-bcd1-cb87773e29ed] received
[2026-03-28 15:20:27,769: INFO/MainProcess] Task tasks.scrape_pending_urls[ac7326ac-b92c-4b74-bcd1-cb87773e29ed] succeeded in 0.0031114000594243407s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,771: INFO/MainProcess] Task tasks.scrape_pending_urls[f86ed692-9e7a-4c34-8785-30f00e471632] received
[2026-03-28 15:20:27,774: INFO/MainProcess] Task tasks.scrape_pending_urls[f86ed692-9e7a-4c34-8785-30f00e471632] succeeded in 0.0026936000213027s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,776: INFO/MainProcess] Task tasks.scrape_pending_urls[d2924bbf-f283-4ed3-b0c3-2ec95fb9eeeb] received
[2026-03-28 15:20:27,778: INFO/MainProcess] Task tasks.scrape_pending_urls[d2924bbf-f283-4ed3-b0c3-2ec95fb9eeeb] succeeded in 0.0024764001136645675s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,780: INFO/MainProcess] Task tasks.scrape_pending_urls[52899450-3ed9-434e-9a86-c9551cbb7527] received
[2026-03-28 15:20:27,784: INFO/MainProcess] Task tasks.scrape_pending_urls[52899450-3ed9-434e-9a86-c9551cbb7527] succeeded in 0.003923800075426698s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,786: INFO/MainProcess] Task tasks.scrape_pending_urls[14035145-a12a-4a85-96f9-cf8a7a4ddb9b] received
[2026-03-28 15:20:27,789: INFO/MainProcess] Task tasks.scrape_pending_urls[14035145-a12a-4a85-96f9-cf8a7a4ddb9b] succeeded in 0.0025243000127375126s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,790: INFO/MainProcess] Task tasks.scrape_pending_urls[29b513ac-d0ba-43fe-bfad-2605239c2efc] received
[2026-03-28 15:20:27,793: INFO/MainProcess] Task tasks.scrape_pending_urls[29b513ac-d0ba-43fe-bfad-2605239c2efc] succeeded in 0.0024710000725463033s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,795: INFO/MainProcess] Task tasks.scrape_pending_urls[8cf50565-dfef-4a6e-bdba-f2ee67bf8bd6] received
[2026-03-28 15:20:27,799: INFO/MainProcess] Task tasks.scrape_pending_urls[8cf50565-dfef-4a6e-bdba-f2ee67bf8bd6] succeeded in 0.0038166999584063888s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,801: INFO/MainProcess] Task tasks.scrape_pending_urls[581dd7e9-7d55-457a-a509-7810405150d8] received
[2026-03-28 15:20:27,804: INFO/MainProcess] Task tasks.scrape_pending_urls[581dd7e9-7d55-457a-a509-7810405150d8] succeeded in 0.0028051999397575855s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,805: INFO/MainProcess] Task tasks.scrape_pending_urls[0d681719-2b37-491c-8442-5f8ef2f77bcd] received
[2026-03-28 15:20:27,808: INFO/MainProcess] Task tasks.scrape_pending_urls[0d681719-2b37-491c-8442-5f8ef2f77bcd] succeeded in 0.002516500069759786s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,810: INFO/MainProcess] Task tasks.scrape_pending_urls[db4ccf90-edd1-4cd5-974f-816ef288a315] received
[2026-03-28 15:20:27,813: INFO/MainProcess] Task tasks.scrape_pending_urls[db4ccf90-edd1-4cd5-974f-816ef288a315] succeeded in 0.003181200008839369s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,815: INFO/MainProcess] Task tasks.scrape_pending_urls[7b2e301f-7e0f-4f9b-9c89-0638c05f91ca] received
[2026-03-28 15:20:27,818: INFO/MainProcess] Task tasks.scrape_pending_urls[7b2e301f-7e0f-4f9b-9c89-0638c05f91ca] succeeded in 0.00266369991004467s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,820: INFO/MainProcess] Task tasks.scrape_pending_urls[93efeb95-366c-4fa8-accd-864bf29020a8] received
[2026-03-28 15:20:27,822: INFO/MainProcess] Task tasks.scrape_pending_urls[93efeb95-366c-4fa8-accd-864bf29020a8] succeeded in 0.0025155000621452928s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,824: INFO/MainProcess] Task tasks.scrape_pending_urls[8de6c3fa-f8b6-4e5d-94ab-4298e2600e90] received
[2026-03-28 15:20:27,827: INFO/MainProcess] Task tasks.scrape_pending_urls[8de6c3fa-f8b6-4e5d-94ab-4298e2600e90] succeeded in 0.0025016999570652843s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,828: INFO/MainProcess] Task tasks.scrape_pending_urls[2e955a67-a482-472b-a589-8edd8e189358] received
[2026-03-28 15:20:27,833: INFO/MainProcess] Task tasks.scrape_pending_urls[2e955a67-a482-472b-a589-8edd8e189358] succeeded in 0.002933699986897409s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,834: INFO/MainProcess] Task tasks.scrape_pending_urls[ca1480d5-dd44-40e8-a3b6-474eda77e5a2] received
[2026-03-28 15:20:27,837: INFO/MainProcess] Task tasks.scrape_pending_urls[ca1480d5-dd44-40e8-a3b6-474eda77e5a2] succeeded in 0.0025423000333830714s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,839: INFO/MainProcess] Task tasks.scrape_pending_urls[595cf45a-6b69-412d-94de-b9867fa42bc2] received
[2026-03-28 15:20:27,842: INFO/MainProcess] Task tasks.scrape_pending_urls[595cf45a-6b69-412d-94de-b9867fa42bc2] succeeded in 0.0025185999693349004s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,843: INFO/MainProcess] Task tasks.scrape_pending_urls[6a443773-58d1-4281-92e6-cbd6c5730eb8] received
[2026-03-28 15:20:27,847: INFO/MainProcess] Task tasks.scrape_pending_urls[6a443773-58d1-4281-92e6-cbd6c5730eb8] succeeded in 0.003588699968531728s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,849: INFO/MainProcess] Task tasks.scrape_pending_urls[1c7d8dd7-ab13-48c4-933b-6a2a975f9ff8] received
[2026-03-28 15:20:27,852: INFO/MainProcess] Task tasks.scrape_pending_urls[1c7d8dd7-ab13-48c4-933b-6a2a975f9ff8] succeeded in 0.0025981999933719635s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,853: INFO/MainProcess] Task tasks.scrape_pending_urls[8e6d4720-22c5-436f-a1e6-1705db051500] received
[2026-03-28 15:20:27,856: INFO/MainProcess] Task tasks.scrape_pending_urls[8e6d4720-22c5-436f-a1e6-1705db051500] succeeded in 0.002544500050134957s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,858: INFO/MainProcess] Task tasks.scrape_pending_urls[47fa6276-fef8-48a4-899d-aeded1638486] received
[2026-03-28 15:20:27,862: INFO/MainProcess] Task tasks.scrape_pending_urls[47fa6276-fef8-48a4-899d-aeded1638486] succeeded in 0.003488000016659498s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,864: INFO/MainProcess] Task tasks.scrape_pending_urls[ea3f30e4-1953-4cea-a118-15e10db0dc83] received
[2026-03-28 15:20:27,868: INFO/MainProcess] Task tasks.scrape_pending_urls[ea3f30e4-1953-4cea-a118-15e10db0dc83] succeeded in 0.0035019998904317617s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,870: INFO/MainProcess] Task tasks.scrape_pending_urls[3c0de013-e462-4236-be61-fe2189b34c4e] received
[2026-03-28 15:20:27,873: INFO/MainProcess] Task tasks.scrape_pending_urls[3c0de013-e462-4236-be61-fe2189b34c4e] succeeded in 0.0032180999405682087s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,875: INFO/MainProcess] Task tasks.scrape_pending_urls[1ee46faf-00ab-482c-b7d4-2bbf546c524c] received
[2026-03-28 15:20:27,879: INFO/MainProcess] Task tasks.scrape_pending_urls[1ee46faf-00ab-482c-b7d4-2bbf546c524c] succeeded in 0.0038732000393792987s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,881: INFO/MainProcess] Task tasks.scrape_pending_urls[22984a0d-af67-4a21-a42d-aea72c11aa4e] received
[2026-03-28 15:20:27,885: INFO/MainProcess] Task tasks.scrape_pending_urls[22984a0d-af67-4a21-a42d-aea72c11aa4e] succeeded in 0.0037802000297233462s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,888: INFO/MainProcess] Task tasks.scrape_pending_urls[7f2ed597-cc5a-4e4a-af1f-0c34f28e82f6] received
[2026-03-28 15:20:27,891: INFO/MainProcess] Task tasks.scrape_pending_urls[7f2ed597-cc5a-4e4a-af1f-0c34f28e82f6] succeeded in 0.0034456999273970723s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,894: INFO/MainProcess] Task tasks.scrape_pending_urls[43952184-6969-4129-9c1f-0cf9b8d36304] received
[2026-03-28 15:20:27,897: INFO/MainProcess] Task tasks.scrape_pending_urls[43952184-6969-4129-9c1f-0cf9b8d36304] succeeded in 0.002913299947977066s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,899: INFO/MainProcess] Task tasks.scrape_pending_urls[061f8e34-9c99-47b4-898d-df5eb30e5d2d] received
[2026-03-28 15:20:27,902: INFO/MainProcess] Task tasks.scrape_pending_urls[061f8e34-9c99-47b4-898d-df5eb30e5d2d] succeeded in 0.0026818999322131276s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,903: INFO/MainProcess] Task tasks.scrape_pending_urls[b073e1c1-0610-4811-8d1b-fa85f49cee9c] received
[2026-03-28 15:20:27,906: INFO/MainProcess] Task tasks.scrape_pending_urls[b073e1c1-0610-4811-8d1b-fa85f49cee9c] succeeded in 0.002611899981275201s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,907: INFO/MainProcess] Task tasks.scrape_pending_urls[66588e22-2b8b-44c2-968c-abad03fed008] received
[2026-03-28 15:20:27,912: INFO/MainProcess] Task tasks.scrape_pending_urls[66588e22-2b8b-44c2-968c-abad03fed008] succeeded in 0.0040336999809369445s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,913: INFO/MainProcess] Task tasks.scrape_pending_urls[2db84a43-0a78-463e-bd23-79a8be59860a] received
[2026-03-28 15:20:27,916: INFO/MainProcess] Task tasks.scrape_pending_urls[2db84a43-0a78-463e-bd23-79a8be59860a] succeeded in 0.002626199973747134s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,918: INFO/MainProcess] Task tasks.scrape_pending_urls[885b29ea-ec85-4ce6-b1d4-a6493150aa27] received
[2026-03-28 15:20:27,920: INFO/MainProcess] Task tasks.scrape_pending_urls[885b29ea-ec85-4ce6-b1d4-a6493150aa27] succeeded in 0.0024967000354081392s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,922: INFO/MainProcess] Task tasks.scrape_pending_urls[80219890-3ef0-4069-addf-97bba8681ba7] received
[2026-03-28 15:20:27,926: INFO/MainProcess] Task tasks.scrape_pending_urls[80219890-3ef0-4069-addf-97bba8681ba7] succeeded in 0.0034666000865399837s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,927: INFO/MainProcess] Task tasks.scrape_pending_urls[82b0b4fe-fd49-4d1e-b69a-28fc30c894e1] received
[2026-03-28 15:20:27,931: INFO/MainProcess] Task tasks.scrape_pending_urls[82b0b4fe-fd49-4d1e-b69a-28fc30c894e1] succeeded in 0.003028100007213652s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,932: INFO/MainProcess] Task tasks.scrape_pending_urls[45efa0f7-a4e1-4144-9fb0-e8425c48dcec] received
[2026-03-28 15:20:27,935: INFO/MainProcess] Task tasks.scrape_pending_urls[45efa0f7-a4e1-4144-9fb0-e8425c48dcec] succeeded in 0.0025813999818637967s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,937: INFO/MainProcess] Task tasks.scrape_pending_urls[491ee3de-2625-4da6-b230-929474c2e5fe] received
[2026-03-28 15:20:27,940: INFO/MainProcess] Task tasks.scrape_pending_urls[491ee3de-2625-4da6-b230-929474c2e5fe] succeeded in 0.002670600078999996s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,942: INFO/MainProcess] Task tasks.scrape_pending_urls[c2eec595-3e80-4425-bd48-049d3a2a1eab] received
[2026-03-28 15:20:27,945: INFO/MainProcess] Task tasks.scrape_pending_urls[c2eec595-3e80-4425-bd48-049d3a2a1eab] succeeded in 0.0026363000506535172s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,947: INFO/MainProcess] Task tasks.scrape_pending_urls[94fce3de-b25e-4eaf-84cb-9856524cc7c8] received
[2026-03-28 15:20:27,950: INFO/MainProcess] Task tasks.scrape_pending_urls[94fce3de-b25e-4eaf-84cb-9856524cc7c8] succeeded in 0.0025032999692484736s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,951: INFO/MainProcess] Task tasks.scrape_pending_urls[70d6dba9-6214-4d89-bb9f-fca8007c6662] received
[2026-03-28 15:20:27,954: INFO/MainProcess] Task tasks.scrape_pending_urls[70d6dba9-6214-4d89-bb9f-fca8007c6662] succeeded in 0.002519400091841817s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,956: INFO/MainProcess] Task tasks.scrape_pending_urls[818979d2-e25a-42bc-968c-ce76e45f8a21] received
[2026-03-28 15:20:27,959: INFO/MainProcess] Task tasks.scrape_pending_urls[818979d2-e25a-42bc-968c-ce76e45f8a21] succeeded in 0.0029456999618560076s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,961: INFO/MainProcess] Task tasks.scrape_pending_urls[8617142f-42e4-410e-bc08-9f1db85ae90b] received
[2026-03-28 15:20:27,964: INFO/MainProcess] Task tasks.scrape_pending_urls[8617142f-42e4-410e-bc08-9f1db85ae90b] succeeded in 0.0025713000213727355s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,965: INFO/MainProcess] Task tasks.scrape_pending_urls[a4fb5a58-6ad1-4892-aa27-e4b22f4f8b5e] received
[2026-03-28 15:20:27,968: INFO/MainProcess] Task tasks.scrape_pending_urls[a4fb5a58-6ad1-4892-aa27-e4b22f4f8b5e] succeeded in 0.002500500064343214s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,970: INFO/MainProcess] Task tasks.scrape_pending_urls[3998c537-bff3-491e-aafd-d5324357be37] received
[2026-03-28 15:20:27,973: INFO/MainProcess] Task tasks.scrape_pending_urls[3998c537-bff3-491e-aafd-d5324357be37] succeeded in 0.003334700013510883s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,975: INFO/MainProcess] Task tasks.scrape_pending_urls[b7a8fd28-0559-41c3-9b2d-034d7fa230ca] received
[2026-03-28 15:20:27,978: INFO/MainProcess] Task tasks.scrape_pending_urls[b7a8fd28-0559-41c3-9b2d-034d7fa230ca] succeeded in 0.0027185999788343906s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,980: INFO/MainProcess] Task tasks.scrape_pending_urls[2bae2b6d-decc-41fa-97f1-b6d0ff31ac2d] received
[2026-03-28 15:20:27,983: INFO/MainProcess] Task tasks.scrape_pending_urls[2bae2b6d-decc-41fa-97f1-b6d0ff31ac2d] succeeded in 0.0025556000182405114s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,984: INFO/MainProcess] Task tasks.scrape_pending_urls[44935e0f-6357-46ad-9f27-e8b25751c51b] received
[2026-03-28 15:20:27,988: INFO/MainProcess] Task tasks.scrape_pending_urls[44935e0f-6357-46ad-9f27-e8b25751c51b] succeeded in 0.0034244999988004565s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,990: INFO/MainProcess] Task tasks.scrape_pending_urls[4e3ebd67-0943-483f-87e5-b263ff4a1a61] received
[2026-03-28 15:20:27,993: INFO/MainProcess] Task tasks.scrape_pending_urls[4e3ebd67-0943-483f-87e5-b263ff4a1a61] succeeded in 0.002647100016474724s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,994: INFO/MainProcess] Task tasks.scrape_pending_urls[b059bb0b-154f-4765-9724-0fa4235503a7] received
[2026-03-28 15:20:27,997: INFO/MainProcess] Task tasks.scrape_pending_urls[b059bb0b-154f-4765-9724-0fa4235503a7] succeeded in 0.0025070999981835485s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:27,998: INFO/MainProcess] Task tasks.scrape_pending_urls[c5698be0-0ca5-4ee0-b673-231bd891350b] received
[2026-03-28 15:20:28,001: INFO/MainProcess] Task tasks.scrape_pending_urls[c5698be0-0ca5-4ee0-b673-231bd891350b] succeeded in 0.002506999997422099s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,003: INFO/MainProcess] Task tasks.scrape_pending_urls[53bdafd1-d838-47d7-9b6a-c781614b9da0] received
[2026-03-28 15:20:28,008: INFO/MainProcess] Task tasks.scrape_pending_urls[53bdafd1-d838-47d7-9b6a-c781614b9da0] succeeded in 0.0033527000341564417s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,010: INFO/MainProcess] Task tasks.scrape_pending_urls[d8548a59-94c7-4a33-a5db-b79d3edae9b9] received
[2026-03-28 15:20:28,012: INFO/MainProcess] Task tasks.scrape_pending_urls[d8548a59-94c7-4a33-a5db-b79d3edae9b9] succeeded in 0.00257060001604259s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,014: INFO/MainProcess] Task tasks.scrape_pending_urls[df01271f-f590-43b1-a38a-2785e68ecb21] received
[2026-03-28 15:20:28,017: INFO/MainProcess] Task tasks.scrape_pending_urls[df01271f-f590-43b1-a38a-2785e68ecb21] succeeded in 0.002500800066627562s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,018: INFO/MainProcess] Task tasks.scrape_pending_urls[63d1936e-d176-4c2b-96d1-585717dcafb7] received
[2026-03-28 15:20:28,022: INFO/MainProcess] Task tasks.scrape_pending_urls[63d1936e-d176-4c2b-96d1-585717dcafb7] succeeded in 0.003496199962683022s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,024: INFO/MainProcess] Task tasks.scrape_pending_urls[60249f32-cd37-4367-ac7d-cf3f58c2dd88] received
[2026-03-28 15:20:28,028: INFO/MainProcess] Task tasks.scrape_pending_urls[60249f32-cd37-4367-ac7d-cf3f58c2dd88] succeeded in 0.0031543999211862683s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,029: INFO/MainProcess] Task tasks.scrape_pending_urls[dc3682c1-ca1d-433f-909c-cafb1a56ae91] received
[2026-03-28 15:20:28,032: INFO/MainProcess] Task tasks.scrape_pending_urls[dc3682c1-ca1d-433f-909c-cafb1a56ae91] succeeded in 0.0027336999773979187s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,034: INFO/MainProcess] Task tasks.scrape_pending_urls[e4f8e43d-44f2-49f4-a162-aab2cd31dd27] received
[2026-03-28 15:20:28,038: INFO/MainProcess] Task tasks.scrape_pending_urls[e4f8e43d-44f2-49f4-a162-aab2cd31dd27] succeeded in 0.003842300036922097s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,039: INFO/MainProcess] Task tasks.scrape_pending_urls[5165d908-391d-41f7-a9f7-6e3a4d5af0d6] received
[2026-03-28 15:20:28,042: INFO/MainProcess] Task tasks.scrape_pending_urls[5165d908-391d-41f7-a9f7-6e3a4d5af0d6] succeeded in 0.0025840000016614795s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,044: INFO/MainProcess] Task tasks.scrape_pending_urls[e309da31-96c0-453a-8f70-653071c0150b] received
[2026-03-28 15:20:28,046: INFO/MainProcess] Task tasks.scrape_pending_urls[e309da31-96c0-453a-8f70-653071c0150b] succeeded in 0.002507800003513694s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,048: INFO/MainProcess] Task tasks.scrape_pending_urls[f92ab866-cb46-40f9-82bc-a12ab1330dbd] received
[2026-03-28 15:20:28,051: INFO/MainProcess] Task tasks.scrape_pending_urls[f92ab866-cb46-40f9-82bc-a12ab1330dbd] succeeded in 0.003060900024138391s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,053: INFO/MainProcess] Task tasks.scrape_pending_urls[f3e3f0f1-8399-4510-bf9f-d98617489975] received
[2026-03-28 15:20:28,057: INFO/MainProcess] Task tasks.scrape_pending_urls[f3e3f0f1-8399-4510-bf9f-d98617489975] succeeded in 0.002911900053732097s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,059: INFO/MainProcess] Task tasks.scrape_pending_urls[8006671e-2170-4fe3-bd4c-0d1b79222c71] received
[2026-03-28 15:20:28,061: INFO/MainProcess] Task tasks.scrape_pending_urls[8006671e-2170-4fe3-bd4c-0d1b79222c71] succeeded in 0.002606299938634038s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,063: INFO/MainProcess] Task tasks.scrape_pending_urls[c641bda7-f0e4-4903-bc63-4a1c305fd16a] received
[2026-03-28 15:20:28,066: INFO/MainProcess] Task tasks.scrape_pending_urls[c641bda7-f0e4-4903-bc63-4a1c305fd16a] succeeded in 0.0026506000431254506s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,068: INFO/MainProcess] Task tasks.scrape_pending_urls[acd7c7e2-39de-4892-ae03-744e900aa49d] received
[2026-03-28 15:20:28,071: INFO/MainProcess] Task tasks.scrape_pending_urls[acd7c7e2-39de-4892-ae03-744e900aa49d] succeeded in 0.00263440003618598s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,073: INFO/MainProcess] Task tasks.scrape_pending_urls[d04a65ad-7740-452d-98fc-90101dcf7e60] received
[2026-03-28 15:20:28,076: INFO/MainProcess] Task tasks.scrape_pending_urls[d04a65ad-7740-452d-98fc-90101dcf7e60] succeeded in 0.002507199998944998s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,077: INFO/MainProcess] Task tasks.scrape_pending_urls[acd61051-3b50-4d96-8cd4-930591f82aca] received
[2026-03-28 15:20:28,080: INFO/MainProcess] Task tasks.scrape_pending_urls[acd61051-3b50-4d96-8cd4-930591f82aca] succeeded in 0.002467100042849779s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,081: INFO/MainProcess] Task tasks.scrape_pending_urls[ee0a6ba3-516a-42ad-8835-f711dc7375cc] received
[2026-03-28 15:20:28,085: INFO/MainProcess] Task tasks.scrape_pending_urls[ee0a6ba3-516a-42ad-8835-f711dc7375cc] succeeded in 0.003675700048916042s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,087: INFO/MainProcess] Task tasks.scrape_pending_urls[07644060-9875-4bb7-a79c-639d30531dad] received
[2026-03-28 15:20:28,090: INFO/MainProcess] Task tasks.scrape_pending_urls[07644060-9875-4bb7-a79c-639d30531dad] succeeded in 0.002546000061556697s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,092: INFO/MainProcess] Task tasks.scrape_pending_urls[b6bc7e1e-eeb8-4a80-9858-7ed99f9e4fd6] received
[2026-03-28 15:20:28,094: INFO/MainProcess] Task tasks.scrape_pending_urls[b6bc7e1e-eeb8-4a80-9858-7ed99f9e4fd6] succeeded in 0.0024905999889597297s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,096: INFO/MainProcess] Task tasks.scrape_pending_urls[17d3c073-10c8-43ca-b6ac-5b1640274cab] received
[2026-03-28 15:20:28,100: INFO/MainProcess] Task tasks.scrape_pending_urls[17d3c073-10c8-43ca-b6ac-5b1640274cab] succeeded in 0.004076300072483718s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,102: INFO/MainProcess] Task tasks.scrape_pending_urls[415ef518-bd83-4cad-ac27-b1d99376e5b6] received
[2026-03-28 15:20:28,105: INFO/MainProcess] Task tasks.scrape_pending_urls[415ef518-bd83-4cad-ac27-b1d99376e5b6] succeeded in 0.0027486999751999974s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,107: INFO/MainProcess] Task tasks.scrape_pending_urls[8cdb91d1-60f2-4799-85ab-4b6297f528e8] received
[2026-03-28 15:20:28,110: INFO/MainProcess] Task tasks.scrape_pending_urls[8cdb91d1-60f2-4799-85ab-4b6297f528e8] succeeded in 0.0031114000594243407s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,112: INFO/MainProcess] Task tasks.scrape_pending_urls[6971b418-a48e-4bac-a005-8fd5573bda00] received
[2026-03-28 15:20:28,117: INFO/MainProcess] Task tasks.scrape_pending_urls[6971b418-a48e-4bac-a005-8fd5573bda00] succeeded in 0.004767999984323978s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,119: INFO/MainProcess] Task tasks.scrape_pending_urls[308df2d1-28d9-4c59-901a-e11d215b1813] received
[2026-03-28 15:20:28,123: INFO/MainProcess] Task tasks.scrape_pending_urls[308df2d1-28d9-4c59-901a-e11d215b1813] succeeded in 0.0032481999369338155s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,124: INFO/MainProcess] Task tasks.scrape_pending_urls[d50d5ffe-be78-4e0f-9f77-81d9011b105f] received
[2026-03-28 15:20:28,128: INFO/MainProcess] Task tasks.scrape_pending_urls[d50d5ffe-be78-4e0f-9f77-81d9011b105f] succeeded in 0.0030712999869138002s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,130: INFO/MainProcess] Task tasks.scrape_pending_urls[dfdbc9f3-0a5f-492f-acd5-f27eb5f2f829] received
[2026-03-28 15:20:28,135: INFO/MainProcess] Task tasks.scrape_pending_urls[dfdbc9f3-0a5f-492f-acd5-f27eb5f2f829] succeeded in 0.0034313000505790114s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,136: INFO/MainProcess] Task tasks.scrape_pending_urls[d372e5a1-3a21-4f7b-83ef-6a0da2db08cc] received
[2026-03-28 15:20:28,139: INFO/MainProcess] Task tasks.scrape_pending_urls[d372e5a1-3a21-4f7b-83ef-6a0da2db08cc] succeeded in 0.002750899991951883s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,141: INFO/MainProcess] Task tasks.scrape_pending_urls[d698834b-73e7-4526-8398-8128d12700b0] received
[2026-03-28 15:20:28,144: INFO/MainProcess] Task tasks.scrape_pending_urls[d698834b-73e7-4526-8398-8128d12700b0] succeeded in 0.0024797000223770738s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,145: INFO/MainProcess] Task tasks.scrape_pending_urls[2667a4bc-8313-4afe-a786-9b5c522d542f] received
[2026-03-28 15:20:28,148: INFO/MainProcess] Task tasks.scrape_pending_urls[2667a4bc-8313-4afe-a786-9b5c522d542f] succeeded in 0.00311300007160753s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,150: INFO/MainProcess] Task tasks.scrape_pending_urls[b8f79186-6740-4cb3-b63e-ec2cb149b2e3] received
[2026-03-28 15:20:28,153: INFO/MainProcess] Task tasks.scrape_pending_urls[b8f79186-6740-4cb3-b63e-ec2cb149b2e3] succeeded in 0.0025978999910876155s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,154: INFO/MainProcess] Task tasks.scrape_pending_urls[e088c896-df86-4eac-82fb-3812b3f5b66d] received
[2026-03-28 15:20:28,157: INFO/MainProcess] Task tasks.scrape_pending_urls[e088c896-df86-4eac-82fb-3812b3f5b66d] succeeded in 0.0026393000734969974s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,159: INFO/MainProcess] Task tasks.scrape_pending_urls[bd329136-3fe8-4212-9c01-9855eaf22188] received
[2026-03-28 15:20:28,162: INFO/MainProcess] Task tasks.scrape_pending_urls[bd329136-3fe8-4212-9c01-9855eaf22188] succeeded in 0.002876600017771125s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,165: INFO/MainProcess] Task tasks.scrape_pending_urls[d92fef1d-6528-4618-acf2-2e5e086f04bb] received
[2026-03-28 15:20:28,168: INFO/MainProcess] Task tasks.scrape_pending_urls[d92fef1d-6528-4618-acf2-2e5e086f04bb] succeeded in 0.002660400001332164s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,170: INFO/MainProcess] Task tasks.scrape_pending_urls[5ddb9b21-2cb8-4bb2-a60a-23ac05c444e4] received
[2026-03-28 15:20:28,172: INFO/MainProcess] Task tasks.scrape_pending_urls[5ddb9b21-2cb8-4bb2-a60a-23ac05c444e4] succeeded in 0.0025360999861732125s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,174: INFO/MainProcess] Task tasks.scrape_pending_urls[de2021d6-8c04-4eda-a488-34d892f9862d] received
[2026-03-28 15:20:28,177: INFO/MainProcess] Task tasks.scrape_pending_urls[de2021d6-8c04-4eda-a488-34d892f9862d] succeeded in 0.002483900054357946s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,179: INFO/MainProcess] Task tasks.scrape_pending_urls[3ff24fc8-8361-40db-a729-5ff98d83e366] received
[2026-03-28 15:20:28,183: INFO/MainProcess] Task tasks.scrape_pending_urls[3ff24fc8-8361-40db-a729-5ff98d83e366] succeeded in 0.002947599976323545s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,185: INFO/MainProcess] Task tasks.scrape_pending_urls[4e1d2cc2-a69b-4d29-b580-321879d0d5aa] received
[2026-03-28 15:20:28,188: INFO/MainProcess] Task tasks.scrape_pending_urls[4e1d2cc2-a69b-4d29-b580-321879d0d5aa] succeeded in 0.0025141999358311296s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,189: INFO/MainProcess] Task tasks.scrape_pending_urls[17104dc7-3f04-47ef-bc24-a2a3106c3f97] received
[2026-03-28 15:20:28,192: INFO/MainProcess] Task tasks.scrape_pending_urls[17104dc7-3f04-47ef-bc24-a2a3106c3f97] succeeded in 0.0024933000095188618s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,194: INFO/MainProcess] Task tasks.scrape_pending_urls[90ff7875-e4c5-4237-93a3-bdcdb4666326] received
[2026-03-28 15:20:28,197: INFO/MainProcess] Task tasks.scrape_pending_urls[90ff7875-e4c5-4237-93a3-bdcdb4666326] succeeded in 0.0027061000000685453s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,199: INFO/MainProcess] Task tasks.scrape_pending_urls[03e0421a-4fed-4b21-bdca-cee93af18fe9] received
[2026-03-28 15:20:28,202: INFO/MainProcess] Task tasks.scrape_pending_urls[03e0421a-4fed-4b21-bdca-cee93af18fe9] succeeded in 0.0024211000418290496s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,203: INFO/MainProcess] Task tasks.scrape_pending_urls[8613af4d-efae-4bff-ad7b-11c6d8064b45] received
[2026-03-28 15:20:28,206: INFO/MainProcess] Task tasks.scrape_pending_urls[8613af4d-efae-4bff-ad7b-11c6d8064b45] succeeded in 0.002557000028900802s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,207: INFO/MainProcess] Task tasks.scrape_pending_urls[6c52d1e1-f558-418d-8431-63d419ffddc0] received
[2026-03-28 15:20:28,211: INFO/MainProcess] Task tasks.scrape_pending_urls[6c52d1e1-f558-418d-8431-63d419ffddc0] succeeded in 0.003783399937674403s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,213: INFO/MainProcess] Task tasks.scrape_pending_urls[5665cec7-daa3-40ab-8bc9-a18ab957fcd1] received
[2026-03-28 15:20:28,217: INFO/MainProcess] Task tasks.scrape_pending_urls[5665cec7-daa3-40ab-8bc9-a18ab957fcd1] succeeded in 0.002824299968779087s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,218: INFO/MainProcess] Task tasks.scrape_pending_urls[8b290e61-203c-47c4-b8b5-f718f35b6ce9] received
[2026-03-28 15:20:28,221: INFO/MainProcess] Task tasks.scrape_pending_urls[8b290e61-203c-47c4-b8b5-f718f35b6ce9] succeeded in 0.0025218999944627285s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,223: INFO/MainProcess] Task tasks.scrape_pending_urls[b1c7089c-4cfd-487e-bdde-ef4dfc1997a1] received
[2026-03-28 15:20:28,226: INFO/MainProcess] Task tasks.scrape_pending_urls[b1c7089c-4cfd-487e-bdde-ef4dfc1997a1] succeeded in 0.003158999956212938s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,228: INFO/MainProcess] Task tasks.scrape_pending_urls[8b485548-43c9-451e-9859-00d0e0e4e8f3] received
[2026-03-28 15:20:28,231: INFO/MainProcess] Task tasks.scrape_pending_urls[8b485548-43c9-451e-9859-00d0e0e4e8f3] succeeded in 0.002635000040754676s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,232: INFO/MainProcess] Task tasks.scrape_pending_urls[c6d7d678-7629-49c2-9c20-04b4a65f1029] received
[2026-03-28 15:20:28,235: INFO/MainProcess] Task tasks.scrape_pending_urls[c6d7d678-7629-49c2-9c20-04b4a65f1029] succeeded in 0.0024404999567195773s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,237: INFO/MainProcess] Task tasks.scrape_pending_urls[3179ad20-1170-4228-9b55-2f12d93f0b72] received
[2026-03-28 15:20:28,239: INFO/MainProcess] Task tasks.scrape_pending_urls[3179ad20-1170-4228-9b55-2f12d93f0b72] succeeded in 0.00248180003836751s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,241: INFO/MainProcess] Task tasks.scrape_pending_urls[10fafc34-471a-4c6b-8064-a823ecf22a4d] received
[2026-03-28 15:20:28,246: INFO/MainProcess] Task tasks.scrape_pending_urls[10fafc34-471a-4c6b-8064-a823ecf22a4d] succeeded in 0.003417799947783351s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,247: INFO/MainProcess] Task tasks.scrape_pending_urls[e0e02d42-576b-4231-8728-5bdf523e3163] received
[2026-03-28 15:20:28,250: INFO/MainProcess] Task tasks.scrape_pending_urls[e0e02d42-576b-4231-8728-5bdf523e3163] succeeded in 0.0025158999487757683s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,252: INFO/MainProcess] Task tasks.scrape_pending_urls[ba9c61d2-feef-460c-ae44-1d9092d1a1db] received
[2026-03-28 15:20:28,255: INFO/MainProcess] Task tasks.scrape_pending_urls[ba9c61d2-feef-460c-ae44-1d9092d1a1db] succeeded in 0.0025131000438705087s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,256: INFO/MainProcess] Task tasks.scrape_pending_urls[d2cb657e-f3f4-4bf7-b9cf-a23ce971c479] received
[2026-03-28 15:20:28,260: INFO/MainProcess] Task tasks.scrape_pending_urls[d2cb657e-f3f4-4bf7-b9cf-a23ce971c479] succeeded in 0.0038084000116214156s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,262: INFO/MainProcess] Task tasks.scrape_pending_urls[1ebd1261-535e-4b04-b02d-5c7b6a88b06c] received
[2026-03-28 15:20:28,265: INFO/MainProcess] Task tasks.scrape_pending_urls[1ebd1261-535e-4b04-b02d-5c7b6a88b06c] succeeded in 0.0025570999132469296s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,266: INFO/MainProcess] Task tasks.scrape_pending_urls[ee20df26-c954-4e5f-bd80-7e66f77cc79f] received
[2026-03-28 15:20:28,269: INFO/MainProcess] Task tasks.scrape_pending_urls[ee20df26-c954-4e5f-bd80-7e66f77cc79f] succeeded in 0.0024766999995335937s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,271: INFO/MainProcess] Task tasks.scrape_pending_urls[8bffcb37-3995-444a-8c87-ce58deb6316c] received
[2026-03-28 15:20:28,275: INFO/MainProcess] Task tasks.scrape_pending_urls[8bffcb37-3995-444a-8c87-ce58deb6316c] succeeded in 0.0039175000274553895s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,277: INFO/MainProcess] Task tasks.scrape_pending_urls[55f7b874-a270-4c6c-ac1a-84e4a89a4a62] received
[2026-03-28 15:20:28,280: INFO/MainProcess] Task tasks.scrape_pending_urls[55f7b874-a270-4c6c-ac1a-84e4a89a4a62] succeeded in 0.003180100000463426s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,282: INFO/MainProcess] Task tasks.scrape_pending_urls[6a728b10-7e56-4680-81f8-2e5de1ada90a] received
[2026-03-28 15:20:28,285: INFO/MainProcess] Task tasks.scrape_pending_urls[6a728b10-7e56-4680-81f8-2e5de1ada90a] succeeded in 0.002640899969264865s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,287: INFO/MainProcess] Task tasks.scrape_pending_urls[fe734bdb-64e1-4224-b0c9-82557b147f9b] received
[2026-03-28 15:20:28,290: INFO/MainProcess] Task tasks.scrape_pending_urls[fe734bdb-64e1-4224-b0c9-82557b147f9b] succeeded in 0.0027677000034600496s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,292: INFO/MainProcess] Task tasks.scrape_pending_urls[82bee31d-4c7e-47c4-98cf-798024262fd7] received
[2026-03-28 15:20:28,295: INFO/MainProcess] Task tasks.scrape_pending_urls[82bee31d-4c7e-47c4-98cf-798024262fd7] succeeded in 0.0031060000183060765s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,297: INFO/MainProcess] Task tasks.scrape_pending_urls[cfb83c69-9217-4384-9f29-993f35baeded] received
[2026-03-28 15:20:28,300: INFO/MainProcess] Task tasks.scrape_pending_urls[cfb83c69-9217-4384-9f29-993f35baeded] succeeded in 0.002574400044977665s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,301: INFO/MainProcess] Task tasks.scrape_pending_urls[f4048dd9-3fe0-4d28-8a96-bc11e2d3b69b] received
[2026-03-28 15:20:28,304: INFO/MainProcess] Task tasks.scrape_pending_urls[f4048dd9-3fe0-4d28-8a96-bc11e2d3b69b] succeeded in 0.00248930009547621s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,307: INFO/MainProcess] Task tasks.scrape_pending_urls[80d84940-553e-46e3-a344-4324b803efec] received
[2026-03-28 15:20:28,310: INFO/MainProcess] Task tasks.scrape_pending_urls[80d84940-553e-46e3-a344-4324b803efec] succeeded in 0.0028042999329045415s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,312: INFO/MainProcess] Task tasks.scrape_pending_urls[d84e988c-9549-42c2-93ae-bedfc525b06f] received
[2026-03-28 15:20:28,315: INFO/MainProcess] Task tasks.scrape_pending_urls[d84e988c-9549-42c2-93ae-bedfc525b06f] succeeded in 0.0026219000574201345s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,316: INFO/MainProcess] Task tasks.scrape_pending_urls[7dde72f7-a8cc-41e4-814b-962890253ed3] received
[2026-03-28 15:20:28,319: INFO/MainProcess] Task tasks.scrape_pending_urls[7dde72f7-a8cc-41e4-814b-962890253ed3] succeeded in 0.002516200067475438s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,322: INFO/MainProcess] Task tasks.scrape_pending_urls[1278efd1-634b-4099-bc52-91e168ee9e84] received
[2026-03-28 15:20:28,325: INFO/MainProcess] Task tasks.scrape_pending_urls[1278efd1-634b-4099-bc52-91e168ee9e84] succeeded in 0.002935800002887845s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,326: INFO/MainProcess] Task tasks.scrape_pending_urls[d2a423ca-37e3-4fba-8a3e-ab98c6b2ee21] received
[2026-03-28 15:20:28,329: INFO/MainProcess] Task tasks.scrape_pending_urls[d2a423ca-37e3-4fba-8a3e-ab98c6b2ee21] succeeded in 0.0026684999465942383s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,331: INFO/MainProcess] Task tasks.scrape_pending_urls[63f87a0b-1262-4c81-99da-1c41e341ce86] received
[2026-03-28 15:20:28,334: INFO/MainProcess] Task tasks.scrape_pending_urls[63f87a0b-1262-4c81-99da-1c41e341ce86] succeeded in 0.002534099970944226s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,335: INFO/MainProcess] Task tasks.scrape_pending_urls[b86c3ac1-6510-4f81-bca2-0306ef13c3df] received
[2026-03-28 15:20:28,339: INFO/MainProcess] Task tasks.scrape_pending_urls[b86c3ac1-6510-4f81-bca2-0306ef13c3df] succeeded in 0.0035476000048220158s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,341: INFO/MainProcess] Task tasks.scrape_pending_urls[b1e8ebfa-6226-4259-a8e6-10b0d4e03b5f] received
[2026-03-28 15:20:28,344: INFO/MainProcess] Task tasks.scrape_pending_urls[b1e8ebfa-6226-4259-a8e6-10b0d4e03b5f] succeeded in 0.003129199962131679s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,346: INFO/MainProcess] Task tasks.scrape_pending_urls[7067c0d3-fc59-4dfa-83f8-fb6a14f4bd19] received
[2026-03-28 15:20:28,349: INFO/MainProcess] Task tasks.scrape_pending_urls[7067c0d3-fc59-4dfa-83f8-fb6a14f4bd19] succeeded in 0.002952300012111664s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,351: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d803f8-989c-48cf-b44a-2eb5b426fe72] received
[2026-03-28 15:20:28,355: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d803f8-989c-48cf-b44a-2eb5b426fe72] succeeded in 0.004288400057703257s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,357: INFO/MainProcess] Task tasks.scrape_pending_urls[9f1e26cf-ff16-44f8-b57b-8b52190e30c4] received
[2026-03-28 15:20:28,361: INFO/MainProcess] Task tasks.scrape_pending_urls[9f1e26cf-ff16-44f8-b57b-8b52190e30c4] succeeded in 0.003030400024726987s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,362: INFO/MainProcess] Task tasks.scrape_pending_urls[e294e464-119f-4aa2-9e89-7622789778a7] received
[2026-03-28 15:20:28,366: INFO/MainProcess] Task tasks.scrape_pending_urls[e294e464-119f-4aa2-9e89-7622789778a7] succeeded in 0.0029143999563530087s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,367: INFO/MainProcess] Task tasks.scrape_pending_urls[ae0003ca-969b-4328-9e49-90c9aa51edfb] received
[2026-03-28 15:20:28,371: INFO/MainProcess] Task tasks.scrape_pending_urls[ae0003ca-969b-4328-9e49-90c9aa51edfb] succeeded in 0.0030061000725254416s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,373: INFO/MainProcess] Task tasks.scrape_pending_urls[119f6ced-bc30-494e-8f14-e55c809f1d78] received
[2026-03-28 15:20:28,376: INFO/MainProcess] Task tasks.scrape_pending_urls[119f6ced-bc30-494e-8f14-e55c809f1d78] succeeded in 0.0028304000152274966s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,377: INFO/MainProcess] Task tasks.scrape_pending_urls[3b2d4d52-e1a2-4a68-8600-ddbc5a79aea7] received
[2026-03-28 15:20:28,380: INFO/MainProcess] Task tasks.scrape_pending_urls[3b2d4d52-e1a2-4a68-8600-ddbc5a79aea7] succeeded in 0.002521199989132583s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,382: INFO/MainProcess] Task tasks.scrape_pending_urls[7ba80464-2486-4d6f-bbaa-5c8f5064bc11] received
[2026-03-28 15:20:28,385: INFO/MainProcess] Task tasks.scrape_pending_urls[7ba80464-2486-4d6f-bbaa-5c8f5064bc11] succeeded in 0.003462999942712486s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,387: INFO/MainProcess] Task tasks.scrape_pending_urls[f961267e-8bd8-421d-b9b9-2fc4a9aee9fd] received
[2026-03-28 15:20:28,390: INFO/MainProcess] Task tasks.scrape_pending_urls[f961267e-8bd8-421d-b9b9-2fc4a9aee9fd] succeeded in 0.0025609000585973263s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,391: INFO/MainProcess] Task tasks.scrape_pending_urls[c3111df8-8ea0-4005-89b0-cb8614be2910] received
[2026-03-28 15:20:28,394: INFO/MainProcess] Task tasks.scrape_pending_urls[c3111df8-8ea0-4005-89b0-cb8614be2910] succeeded in 0.002521799993701279s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,395: INFO/MainProcess] Task tasks.scrape_pending_urls[0dcff3c5-3d56-44ff-a191-f5e1c8c51627] received
[2026-03-28 15:20:28,398: INFO/MainProcess] Task tasks.scrape_pending_urls[0dcff3c5-3d56-44ff-a191-f5e1c8c51627] succeeded in 0.0025180999655276537s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,401: INFO/MainProcess] Task tasks.scrape_pending_urls[562ec24f-833f-4094-8784-f3824e155464] received
[2026-03-28 15:20:28,405: INFO/MainProcess] Task tasks.scrape_pending_urls[562ec24f-833f-4094-8784-f3824e155464] succeeded in 0.002804500050842762s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,406: INFO/MainProcess] Task tasks.scrape_pending_urls[d3c8f02f-7da8-4946-b990-610b12f92aa9] received
[2026-03-28 15:20:28,409: INFO/MainProcess] Task tasks.scrape_pending_urls[d3c8f02f-7da8-4946-b990-610b12f92aa9] succeeded in 0.002608099952340126s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,411: INFO/MainProcess] Task tasks.scrape_pending_urls[e04b954b-53c7-45d4-8e53-2c7c208356b6] received
[2026-03-28 15:20:28,413: INFO/MainProcess] Task tasks.scrape_pending_urls[e04b954b-53c7-45d4-8e53-2c7c208356b6] succeeded in 0.002463800017721951s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,415: INFO/MainProcess] Task tasks.scrape_pending_urls[b809b484-e06b-462f-b863-f002a6364dc2] received
[2026-03-28 15:20:28,420: INFO/MainProcess] Task tasks.scrape_pending_urls[b809b484-e06b-462f-b863-f002a6364dc2] succeeded in 0.0028978000627830625s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,422: INFO/MainProcess] Task tasks.scrape_pending_urls[26314807-c4e0-4f3e-8cdc-ade25dcff656] received
[2026-03-28 15:20:28,424: INFO/MainProcess] Task tasks.scrape_pending_urls[26314807-c4e0-4f3e-8cdc-ade25dcff656] succeeded in 0.0023522000992670655s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,426: INFO/MainProcess] Task tasks.scrape_pending_urls[80c1b5e2-ec02-46a0-abc4-b6caca19b50d] received
[2026-03-28 15:20:28,428: INFO/MainProcess] Task tasks.scrape_pending_urls[80c1b5e2-ec02-46a0-abc4-b6caca19b50d] succeeded in 0.002159199910238385s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,429: INFO/MainProcess] Task tasks.scrape_pending_urls[61afc37a-53c8-4a9f-868b-42ceedfde56b] received
[2026-03-28 15:20:28,433: INFO/MainProcess] Task tasks.scrape_pending_urls[61afc37a-53c8-4a9f-868b-42ceedfde56b] succeeded in 0.0032921999227255583s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,434: INFO/MainProcess] Task tasks.scrape_pending_urls[d411625c-df87-466f-a500-fe2c741206fc] received
[2026-03-28 15:20:28,436: INFO/MainProcess] Task tasks.scrape_pending_urls[d411625c-df87-466f-a500-fe2c741206fc] succeeded in 0.0022122999653220177s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,438: INFO/MainProcess] Task tasks.scrape_pending_urls[e32b3d79-2e20-4d29-8c47-0957637fdebe] received
[2026-03-28 15:20:28,440: INFO/MainProcess] Task tasks.scrape_pending_urls[e32b3d79-2e20-4d29-8c47-0957637fdebe] succeeded in 0.002159500028938055s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,441: INFO/MainProcess] Task tasks.scrape_pending_urls[1ab397c8-6c88-4c8a-9299-8a665e565c65] received
[2026-03-28 15:20:28,443: INFO/MainProcess] Task tasks.scrape_pending_urls[1ab397c8-6c88-4c8a-9299-8a665e565c65] succeeded in 0.002125800005160272s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,445: INFO/MainProcess] Task tasks.scrape_pending_urls[e8f63e39-62fe-4b19-a5fb-9d2b258eea4e] received
[2026-03-28 15:20:28,448: INFO/MainProcess] Task tasks.scrape_pending_urls[e8f63e39-62fe-4b19-a5fb-9d2b258eea4e] succeeded in 0.0034419000148773193s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,450: INFO/MainProcess] Task tasks.scrape_pending_urls[3b5ed5e6-20f6-48a2-a9a5-cf9cf32e2dde] received
[2026-03-28 15:20:28,453: INFO/MainProcess] Task tasks.scrape_pending_urls[3b5ed5e6-20f6-48a2-a9a5-cf9cf32e2dde] succeeded in 0.0026279001031070948s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,454: INFO/MainProcess] Task tasks.scrape_pending_urls[0eee1934-c77e-4d70-9094-43917a86acdd] received
[2026-03-28 15:20:28,456: INFO/MainProcess] Task tasks.scrape_pending_urls[0eee1934-c77e-4d70-9094-43917a86acdd] succeeded in 0.0021652999566867948s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,458: INFO/MainProcess] Task tasks.scrape_pending_urls[f0fd5e96-e622-4245-968a-9c5000ca0a9f] received
[2026-03-28 15:20:28,460: INFO/MainProcess] Task tasks.scrape_pending_urls[f0fd5e96-e622-4245-968a-9c5000ca0a9f] succeeded in 0.0021254000021144748s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,461: INFO/MainProcess] Task tasks.scrape_pending_urls[a043d613-6180-4cd2-b119-8de1517253a9] received
[2026-03-28 15:20:28,464: INFO/MainProcess] Task tasks.scrape_pending_urls[a043d613-6180-4cd2-b119-8de1517253a9] succeeded in 0.0030158000299707055s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,466: INFO/MainProcess] Task tasks.scrape_pending_urls[cc6652b3-608f-473e-8738-33c3ddbc0667] received
[2026-03-28 15:20:28,468: INFO/MainProcess] Task tasks.scrape_pending_urls[cc6652b3-608f-473e-8738-33c3ddbc0667] succeeded in 0.002253200043924153s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,469: INFO/MainProcess] Task tasks.scrape_pending_urls[d2ccafa4-e5f7-4152-802f-b4326283a104] received
[2026-03-28 15:20:28,472: INFO/MainProcess] Task tasks.scrape_pending_urls[d2ccafa4-e5f7-4152-802f-b4326283a104] succeeded in 0.002217500004917383s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,473: INFO/MainProcess] Task tasks.scrape_pending_urls[cbfa653c-b074-42f7-a388-ecdd747c11bf] received
[2026-03-28 15:20:28,475: INFO/MainProcess] Task tasks.scrape_pending_urls[cbfa653c-b074-42f7-a388-ecdd747c11bf] succeeded in 0.002135500079020858s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,477: INFO/MainProcess] Task tasks.scrape_pending_urls[b53f19d6-b98f-43d9-9a5a-c47b84591441] received
[2026-03-28 15:20:28,480: INFO/MainProcess] Task tasks.scrape_pending_urls[b53f19d6-b98f-43d9-9a5a-c47b84591441] succeeded in 0.003367600031197071s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,481: INFO/MainProcess] Task tasks.scrape_pending_urls[78975f3c-dca7-491f-89d1-f2bd4076c5ab] received
[2026-03-28 15:20:28,484: INFO/MainProcess] Task tasks.scrape_pending_urls[78975f3c-dca7-491f-89d1-f2bd4076c5ab] succeeded in 0.0022224999265745282s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,485: INFO/MainProcess] Task tasks.scrape_pending_urls[3af56eeb-26d9-409b-b845-80c30572108a] received
[2026-03-28 15:20:28,488: INFO/MainProcess] Task tasks.scrape_pending_urls[3af56eeb-26d9-409b-b845-80c30572108a] succeeded in 0.0026627000188454986s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,489: INFO/MainProcess] Task tasks.scrape_pending_urls[8811c703-cd6e-4292-b45f-835e1a58035c] received
[2026-03-28 15:20:28,492: INFO/MainProcess] Task tasks.scrape_pending_urls[8811c703-cd6e-4292-b45f-835e1a58035c] succeeded in 0.0022595999762415886s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,493: INFO/MainProcess] Task tasks.scrape_pending_urls[6348ba7d-38b8-48e7-9b9f-b273dc4b3076] received
[2026-03-28 15:20:28,497: INFO/MainProcess] Task tasks.scrape_pending_urls[6348ba7d-38b8-48e7-9b9f-b273dc4b3076] succeeded in 0.0023946999572217464s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,498: INFO/MainProcess] Task tasks.scrape_pending_urls[d419d171-e0c8-4f64-9bb7-db2c9268c3c5] received
[2026-03-28 15:20:28,500: INFO/MainProcess] Task tasks.scrape_pending_urls[d419d171-e0c8-4f64-9bb7-db2c9268c3c5] succeeded in 0.0021500999573618174s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,501: INFO/MainProcess] Task tasks.scrape_pending_urls[cd906b4c-4033-4a81-ba9b-bf1b1b2f9b66] received
[2026-03-28 15:20:28,504: INFO/MainProcess] Task tasks.scrape_pending_urls[cd906b4c-4033-4a81-ba9b-bf1b1b2f9b66] succeeded in 0.002205900033004582s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,505: INFO/MainProcess] Task tasks.scrape_pending_urls[11a0aac9-f081-4203-bb26-9cab67b9869f] received
[2026-03-28 15:20:28,507: INFO/MainProcess] Task tasks.scrape_pending_urls[11a0aac9-f081-4203-bb26-9cab67b9869f] succeeded in 0.0021361999679356813s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,509: INFO/MainProcess] Task tasks.scrape_pending_urls[9b92a18d-c6ec-4031-a8a9-63d7d63196df] received
[2026-03-28 15:20:28,513: INFO/MainProcess] Task tasks.scrape_pending_urls[9b92a18d-c6ec-4031-a8a9-63d7d63196df] succeeded in 0.0037814000388607383s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,514: INFO/MainProcess] Task tasks.scrape_pending_urls[17dec298-73ba-4af1-9d11-d469df04297e] received
[2026-03-28 15:20:28,516: INFO/MainProcess] Task tasks.scrape_pending_urls[17dec298-73ba-4af1-9d11-d469df04297e] succeeded in 0.0020358000183477998s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,518: INFO/MainProcess] Task tasks.scrape_pending_urls[3610d039-8bd8-4d18-91da-08ed958a8891] received
[2026-03-28 15:20:28,520: INFO/MainProcess] Task tasks.scrape_pending_urls[3610d039-8bd8-4d18-91da-08ed958a8891] succeeded in 0.002034400007687509s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,521: INFO/MainProcess] Task tasks.scrape_pending_urls[459f0253-2805-4904-a555-2e5c79c943a9] received
[2026-03-28 15:20:28,523: INFO/MainProcess] Task tasks.scrape_pending_urls[459f0253-2805-4904-a555-2e5c79c943a9] succeeded in 0.0019798000575974584s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,525: INFO/MainProcess] Task tasks.scrape_pending_urls[648bc7ca-2bc6-418a-974c-8b3c9b877995] received
[2026-03-28 15:20:28,530: INFO/MainProcess] Task tasks.scrape_pending_urls[648bc7ca-2bc6-418a-974c-8b3c9b877995] succeeded in 0.0034772000508382916s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,532: INFO/MainProcess] Task tasks.scrape_pending_urls[91733502-b324-46c5-956e-6196dedcc11c] received
[2026-03-28 15:20:28,535: INFO/MainProcess] Task tasks.scrape_pending_urls[91733502-b324-46c5-956e-6196dedcc11c] succeeded in 0.0030436000088229775s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,537: INFO/MainProcess] Task tasks.scrape_pending_urls[95cd253d-c28b-4be0-9da8-f67776171a87] received
[2026-03-28 15:20:28,540: INFO/MainProcess] Task tasks.scrape_pending_urls[95cd253d-c28b-4be0-9da8-f67776171a87] succeeded in 0.0023083999985828996s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,542: INFO/MainProcess] Task tasks.scrape_pending_urls[1c2d4132-61ee-4439-a8ca-0fd3e674fee6] received
[2026-03-28 15:20:28,545: INFO/MainProcess] Task tasks.scrape_pending_urls[1c2d4132-61ee-4439-a8ca-0fd3e674fee6] succeeded in 0.002804199932143092s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,546: INFO/MainProcess] Task tasks.scrape_pending_urls[80fd50ce-3d92-4c86-b91e-e6dacce056bc] received
[2026-03-28 15:20:28,548: INFO/MainProcess] Task tasks.scrape_pending_urls[80fd50ce-3d92-4c86-b91e-e6dacce056bc] succeeded in 0.0021883000154048204s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,550: INFO/MainProcess] Task tasks.scrape_pending_urls[f53b51b1-d238-4c25-a498-76064ef9a0d4] received
[2026-03-28 15:20:28,552: INFO/MainProcess] Task tasks.scrape_pending_urls[f53b51b1-d238-4c25-a498-76064ef9a0d4] succeeded in 0.0022094000596553087s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,553: INFO/MainProcess] Task tasks.scrape_pending_urls[9e32d685-324e-49cd-8c92-afe0a5ef3e06] received
[2026-03-28 15:20:28,556: INFO/MainProcess] Task tasks.scrape_pending_urls[9e32d685-324e-49cd-8c92-afe0a5ef3e06] succeeded in 0.002202299889177084s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,558: INFO/MainProcess] Task tasks.scrape_pending_urls[93861021-1a4c-47d6-9a35-8c1ec03ccd6f] received
[2026-03-28 15:20:28,562: INFO/MainProcess] Task tasks.scrape_pending_urls[93861021-1a4c-47d6-9a35-8c1ec03ccd6f] succeeded in 0.003536500036716461s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,564: INFO/MainProcess] Task tasks.scrape_pending_urls[1f9d8a17-9bf4-4574-9336-fe3aa7f79aec] received
[2026-03-28 15:20:28,567: INFO/MainProcess] Task tasks.scrape_pending_urls[1f9d8a17-9bf4-4574-9336-fe3aa7f79aec] succeeded in 0.0025877999141812325s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,568: INFO/MainProcess] Task tasks.scrape_pending_urls[264c484a-b970-4f1c-a548-4fdeed404b2a] received
[2026-03-28 15:20:28,571: INFO/MainProcess] Task tasks.scrape_pending_urls[264c484a-b970-4f1c-a548-4fdeed404b2a] succeeded in 0.002499000052921474s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,572: INFO/MainProcess] Task tasks.scrape_pending_urls[977f7799-9cfe-450a-be1e-ea9935b10b51] received
[2026-03-28 15:20:28,577: INFO/MainProcess] Task tasks.scrape_pending_urls[977f7799-9cfe-450a-be1e-ea9935b10b51] succeeded in 0.0028615000192075968s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,579: INFO/MainProcess] Task tasks.scrape_pending_urls[0547a28a-751d-4082-9f5b-8049281c3eed] received
[2026-03-28 15:20:28,581: INFO/MainProcess] Task tasks.scrape_pending_urls[0547a28a-751d-4082-9f5b-8049281c3eed] succeeded in 0.0025626999558880925s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,583: INFO/MainProcess] Task tasks.scrape_pending_urls[922bca15-7f69-47f7-8379-4829a860a108] received
[2026-03-28 15:20:28,586: INFO/MainProcess] Task tasks.scrape_pending_urls[922bca15-7f69-47f7-8379-4829a860a108] succeeded in 0.0027808999875560403s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,588: INFO/MainProcess] Task tasks.scrape_pending_urls[9ff8481d-42b8-4893-8d53-92daacf72ede] received
[2026-03-28 15:20:28,593: INFO/MainProcess] Task tasks.scrape_pending_urls[9ff8481d-42b8-4893-8d53-92daacf72ede] succeeded in 0.005053300061263144s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,595: INFO/MainProcess] Task tasks.scrape_pending_urls[d103498f-33b6-4d9a-8155-069a7fc64b82] received
[2026-03-28 15:20:28,599: INFO/MainProcess] Task tasks.scrape_pending_urls[d103498f-33b6-4d9a-8155-069a7fc64b82] succeeded in 0.003212899900972843s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,600: INFO/MainProcess] Task tasks.scrape_pending_urls[5154ccb6-7ec5-4b1f-bc79-ff0b66937cc0] received
[2026-03-28 15:20:28,604: INFO/MainProcess] Task tasks.scrape_pending_urls[5154ccb6-7ec5-4b1f-bc79-ff0b66937cc0] succeeded in 0.002717799972742796s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,605: INFO/MainProcess] Task tasks.scrape_pending_urls[4f72b40a-b426-4dc0-8a95-f87e87ead8eb] received
[2026-03-28 15:20:28,609: INFO/MainProcess] Task tasks.scrape_pending_urls[4f72b40a-b426-4dc0-8a95-f87e87ead8eb] succeeded in 0.0030448000179603696s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,611: INFO/MainProcess] Task tasks.scrape_pending_urls[d56edb34-4344-43a4-881f-a26f17acc80d] received
[2026-03-28 15:20:28,614: INFO/MainProcess] Task tasks.scrape_pending_urls[d56edb34-4344-43a4-881f-a26f17acc80d] succeeded in 0.0026563999708741903s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,615: INFO/MainProcess] Task tasks.scrape_pending_urls[71acebcd-c6ef-41ab-a7d2-8a45522ced29] received
[2026-03-28 15:20:28,617: INFO/MainProcess] Task tasks.scrape_pending_urls[71acebcd-c6ef-41ab-a7d2-8a45522ced29] succeeded in 0.002180499956011772s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,619: INFO/MainProcess] Task tasks.scrape_pending_urls[87181a26-703a-4895-a075-8509c002fd16] received
[2026-03-28 15:20:28,622: INFO/MainProcess] Task tasks.scrape_pending_urls[87181a26-703a-4895-a075-8509c002fd16] succeeded in 0.002889900002628565s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,623: INFO/MainProcess] Task tasks.scrape_pending_urls[563ad9e5-fc3a-48fb-a13b-49f41b49d70e] received
[2026-03-28 15:20:28,626: INFO/MainProcess] Task tasks.scrape_pending_urls[563ad9e5-fc3a-48fb-a13b-49f41b49d70e] succeeded in 0.002242899965494871s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,627: INFO/MainProcess] Task tasks.scrape_pending_urls[36d30557-be61-4cb7-a3cc-17023bc42132] received
[2026-03-28 15:20:28,629: INFO/MainProcess] Task tasks.scrape_pending_urls[36d30557-be61-4cb7-a3cc-17023bc42132] succeeded in 0.002090799971483648s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,630: INFO/MainProcess] Task tasks.scrape_pending_urls[83ad8859-49e5-4fd5-ba30-75e06feb3539] received
[2026-03-28 15:20:28,633: INFO/MainProcess] Task tasks.scrape_pending_urls[83ad8859-49e5-4fd5-ba30-75e06feb3539] succeeded in 0.0021249999990686774s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,634: INFO/MainProcess] Task tasks.scrape_pending_urls[465b7206-c6ea-4e14-b0c6-5bb52f72b9db] received
[2026-03-28 15:20:28,637: INFO/MainProcess] Task tasks.scrape_pending_urls[465b7206-c6ea-4e14-b0c6-5bb52f72b9db] succeeded in 0.0030601000180467963s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,639: INFO/MainProcess] Task tasks.scrape_pending_urls[8a443a28-6226-4809-9f3e-32e146a958b8] received
[2026-03-28 15:20:28,641: INFO/MainProcess] Task tasks.scrape_pending_urls[8a443a28-6226-4809-9f3e-32e146a958b8] succeeded in 0.002267500036396086s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,642: INFO/MainProcess] Task tasks.scrape_pending_urls[f1d7e608-aeb2-406e-a2ab-a7c8db8a3dbd] received
[2026-03-28 15:20:28,645: INFO/MainProcess] Task tasks.scrape_pending_urls[f1d7e608-aeb2-406e-a2ab-a7c8db8a3dbd] succeeded in 0.002075799973681569s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,646: INFO/MainProcess] Task tasks.scrape_pending_urls[2a527b11-5260-4a83-b1d1-108434232c01] received
[2026-03-28 15:20:28,649: INFO/MainProcess] Task tasks.scrape_pending_urls[2a527b11-5260-4a83-b1d1-108434232c01] succeeded in 0.0026234000688418746s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,650: INFO/MainProcess] Task tasks.scrape_pending_urls[c191c07c-c5b1-4ee9-a1f6-a57b8e114491] received
[2026-03-28 15:20:28,653: INFO/MainProcess] Task tasks.scrape_pending_urls[c191c07c-c5b1-4ee9-a1f6-a57b8e114491] succeeded in 0.0028744000010192394s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,655: INFO/MainProcess] Task tasks.scrape_pending_urls[6c75252c-7d45-4fa8-a755-69332abe2556] received
[2026-03-28 15:20:28,657: INFO/MainProcess] Task tasks.scrape_pending_urls[6c75252c-7d45-4fa8-a755-69332abe2556] succeeded in 0.002235200023278594s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,658: INFO/MainProcess] Task tasks.scrape_pending_urls[31589b2b-5c2f-412f-af9a-f3a464be263c] received
[2026-03-28 15:20:28,661: INFO/MainProcess] Task tasks.scrape_pending_urls[31589b2b-5c2f-412f-af9a-f3a464be263c] succeeded in 0.0021235999884083867s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,662: INFO/MainProcess] Task tasks.scrape_pending_urls[8a92f065-f142-4c71-9927-b4b96ad95bda] received
[2026-03-28 15:20:28,664: INFO/MainProcess] Task tasks.scrape_pending_urls[8a92f065-f142-4c71-9927-b4b96ad95bda] succeeded in 0.0020360000198706985s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,665: INFO/MainProcess] Task tasks.scrape_pending_urls[b7416cc8-4d35-402e-b800-df6260869ebf] received
[2026-03-28 15:20:28,668: INFO/MainProcess] Task tasks.scrape_pending_urls[b7416cc8-4d35-402e-b800-df6260869ebf] succeeded in 0.0020222999155521393s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,669: INFO/MainProcess] Task tasks.scrape_pending_urls[b985daf9-1f2c-483e-98fd-71b9575183fb] received
[2026-03-28 15:20:28,672: INFO/MainProcess] Task tasks.scrape_pending_urls[b985daf9-1f2c-483e-98fd-71b9575183fb] succeeded in 0.002335399971343577s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,673: INFO/MainProcess] Task tasks.scrape_pending_urls[f3659760-9a39-4bcb-8524-595e5d441867] received
[2026-03-28 15:20:28,676: INFO/MainProcess] Task tasks.scrape_pending_urls[f3659760-9a39-4bcb-8524-595e5d441867] succeeded in 0.002115699928253889s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,677: INFO/MainProcess] Task tasks.scrape_pending_urls[2a9dbd2e-c5da-42be-9d7a-e26504564b8f] received
[2026-03-28 15:20:28,679: INFO/MainProcess] Task tasks.scrape_pending_urls[2a9dbd2e-c5da-42be-9d7a-e26504564b8f] succeeded in 0.002056900062598288s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,680: INFO/MainProcess] Task tasks.scrape_pending_urls[ce767a6c-2700-4c16-8df1-a0cc0cb377b7] received
[2026-03-28 15:20:28,683: INFO/MainProcess] Task tasks.scrape_pending_urls[ce767a6c-2700-4c16-8df1-a0cc0cb377b7] succeeded in 0.0021220999769866467s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,685: INFO/MainProcess] Task tasks.scrape_pending_urls[b97949ae-c694-40ae-973f-3c064e1ea80e] received
[2026-03-28 15:20:28,688: INFO/MainProcess] Task tasks.scrape_pending_urls[b97949ae-c694-40ae-973f-3c064e1ea80e] succeeded in 0.0023495000787079334s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,689: INFO/MainProcess] Task tasks.scrape_pending_urls[142cd317-f61c-4e0c-be68-c37ebc6a9518] received
[2026-03-28 15:20:28,692: INFO/MainProcess] Task tasks.scrape_pending_urls[142cd317-f61c-4e0c-be68-c37ebc6a9518] succeeded in 0.002146099926903844s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,693: INFO/MainProcess] Task tasks.scrape_pending_urls[f2bb9c52-76db-4da1-8314-1147020e3d6c] received
[2026-03-28 15:20:28,695: INFO/MainProcess] Task tasks.scrape_pending_urls[f2bb9c52-76db-4da1-8314-1147020e3d6c] succeeded in 0.0020471999887377024s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,696: INFO/MainProcess] Task tasks.scrape_pending_urls[f7de7de5-a25e-46b2-8bb7-97df74a0e892] received
[2026-03-28 15:20:28,699: INFO/MainProcess] Task tasks.scrape_pending_urls[f7de7de5-a25e-46b2-8bb7-97df74a0e892] succeeded in 0.0020996000384911895s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,700: INFO/MainProcess] Task tasks.scrape_pending_urls[77ce577c-bf2e-42a5-ba17-68712a6a7c48] received
[2026-03-28 15:20:28,704: INFO/MainProcess] Task tasks.scrape_pending_urls[77ce577c-bf2e-42a5-ba17-68712a6a7c48] succeeded in 0.0027696999022737145s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,705: INFO/MainProcess] Task tasks.scrape_pending_urls[aa833d74-1d67-4b82-bf87-fa344f568b77] received
[2026-03-28 15:20:28,708: INFO/MainProcess] Task tasks.scrape_pending_urls[aa833d74-1d67-4b82-bf87-fa344f568b77] succeeded in 0.002345799934118986s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,709: INFO/MainProcess] Task tasks.scrape_pending_urls[595be90c-633c-47d0-95ba-0ad7a20d6e5b] received
[2026-03-28 15:20:28,712: INFO/MainProcess] Task tasks.scrape_pending_urls[595be90c-633c-47d0-95ba-0ad7a20d6e5b] succeeded in 0.0022881999611854553s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,713: INFO/MainProcess] Task tasks.scrape_pending_urls[4efd32d6-4fcc-44cb-abd1-912aacd1d296] received
[2026-03-28 15:20:28,716: INFO/MainProcess] Task tasks.scrape_pending_urls[4efd32d6-4fcc-44cb-abd1-912aacd1d296] succeeded in 0.0027894999366253614s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,719: INFO/MainProcess] Task tasks.scrape_pending_urls[7acff241-32a7-4a4e-9890-4c169721faa1] received
[2026-03-28 15:20:28,722: INFO/MainProcess] Task tasks.scrape_pending_urls[7acff241-32a7-4a4e-9890-4c169721faa1] succeeded in 0.0026759000029414892s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,723: INFO/MainProcess] Task tasks.scrape_pending_urls[4f046652-aaf9-4e34-bb84-c63cb39795d5] received
[2026-03-28 15:20:28,726: INFO/MainProcess] Task tasks.scrape_pending_urls[4f046652-aaf9-4e34-bb84-c63cb39795d5] succeeded in 0.002466500038281083s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,727: INFO/MainProcess] Task tasks.scrape_pending_urls[6ab62e35-6e1a-4fa1-86da-a131b11f2c68] received
[2026-03-28 15:20:28,730: INFO/MainProcess] Task tasks.scrape_pending_urls[6ab62e35-6e1a-4fa1-86da-a131b11f2c68] succeeded in 0.002330100047402084s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,731: INFO/MainProcess] Task tasks.scrape_pending_urls[8f9bdf26-9ef7-4603-9de5-867f2c812093] received
[2026-03-28 15:20:28,735: INFO/MainProcess] Task tasks.scrape_pending_urls[8f9bdf26-9ef7-4603-9de5-867f2c812093] succeeded in 0.002639499958604574s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,736: INFO/MainProcess] Task tasks.scrape_pending_urls[7d7b5c0d-43fd-4c4b-af5f-3aba6e6c15dc] received
[2026-03-28 15:20:28,739: INFO/MainProcess] Task tasks.scrape_pending_urls[7d7b5c0d-43fd-4c4b-af5f-3aba6e6c15dc] succeeded in 0.0023076001089066267s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,740: INFO/MainProcess] Task tasks.scrape_pending_urls[4003d96b-3f30-4638-98c6-6b7e9a5ca591] received
[2026-03-28 15:20:28,743: INFO/MainProcess] Task tasks.scrape_pending_urls[4003d96b-3f30-4638-98c6-6b7e9a5ca591] succeeded in 0.0022748999763280153s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,744: INFO/MainProcess] Task tasks.scrape_pending_urls[cda0c2f0-0133-479c-94bf-3793fdc4af36] received
[2026-03-28 15:20:28,746: INFO/MainProcess] Task tasks.scrape_pending_urls[cda0c2f0-0133-479c-94bf-3793fdc4af36] succeeded in 0.002256499952636659s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,749: INFO/MainProcess] Task tasks.scrape_pending_urls[d0fe3f05-0cce-43a7-b91e-070eeaa5a9a3] received
[2026-03-28 15:20:28,753: INFO/MainProcess] Task tasks.scrape_pending_urls[d0fe3f05-0cce-43a7-b91e-070eeaa5a9a3] succeeded in 0.00284169998485595s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,754: INFO/MainProcess] Task tasks.scrape_pending_urls[df461e5e-40c4-47ce-9bd1-2c7394c8d004] received
[2026-03-28 15:20:28,757: INFO/MainProcess] Task tasks.scrape_pending_urls[df461e5e-40c4-47ce-9bd1-2c7394c8d004] succeeded in 0.002556400024332106s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,759: INFO/MainProcess] Task tasks.scrape_pending_urls[9e7059b2-84db-425a-aaa3-eb5647dd5271] received
[2026-03-28 15:20:28,762: INFO/MainProcess] Task tasks.scrape_pending_urls[9e7059b2-84db-425a-aaa3-eb5647dd5271] succeeded in 0.003055199980735779s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,764: INFO/MainProcess] Task tasks.scrape_pending_urls[04a5bab9-2d81-4a41-a1a8-4139a73455e0] received
[2026-03-28 15:20:28,767: INFO/MainProcess] Task tasks.scrape_pending_urls[04a5bab9-2d81-4a41-a1a8-4139a73455e0] succeeded in 0.0028223999543115497s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,769: INFO/MainProcess] Task tasks.scrape_pending_urls[71d27e43-e253-457f-ab9d-919169b38897] received
[2026-03-28 15:20:28,772: INFO/MainProcess] Task tasks.scrape_pending_urls[71d27e43-e253-457f-ab9d-919169b38897] succeeded in 0.0026267999783158302s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,773: INFO/MainProcess] Task tasks.scrape_pending_urls[c90199ea-991f-458d-bacc-9c3b69eb9091] received
[2026-03-28 15:20:28,776: INFO/MainProcess] Task tasks.scrape_pending_urls[c90199ea-991f-458d-bacc-9c3b69eb9091] succeeded in 0.0026692000683397055s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,778: INFO/MainProcess] Task tasks.scrape_pending_urls[892792a9-c2c9-4e45-a92e-08d10d1ee219] received
[2026-03-28 15:20:28,782: INFO/MainProcess] Task tasks.scrape_pending_urls[892792a9-c2c9-4e45-a92e-08d10d1ee219] succeeded in 0.0038584000431001186s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,784: INFO/MainProcess] Task tasks.scrape_pending_urls[1a3d6cd3-ffae-4255-92b3-0d8f24bb3a58] received
[2026-03-28 15:20:28,787: INFO/MainProcess] Task tasks.scrape_pending_urls[1a3d6cd3-ffae-4255-92b3-0d8f24bb3a58] succeeded in 0.0029727000510320067s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,789: INFO/MainProcess] Task tasks.scrape_pending_urls[ed5efbbd-3e03-4b56-933d-8af9373bb3ac] received
[2026-03-28 15:20:28,792: INFO/MainProcess] Task tasks.scrape_pending_urls[ed5efbbd-3e03-4b56-933d-8af9373bb3ac] succeeded in 0.002646900014951825s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,793: INFO/MainProcess] Task tasks.scrape_pending_urls[56457e4b-6344-4d20-a522-9721b981d761] received
[2026-03-28 15:20:28,798: INFO/MainProcess] Task tasks.scrape_pending_urls[56457e4b-6344-4d20-a522-9721b981d761] succeeded in 0.003914700006134808s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,800: INFO/MainProcess] Task tasks.scrape_pending_urls[a20194df-a4bc-432b-96aa-10b0c71d5475] received
[2026-03-28 15:20:28,804: INFO/MainProcess] Task tasks.scrape_pending_urls[a20194df-a4bc-432b-96aa-10b0c71d5475] succeeded in 0.003579000011086464s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,805: INFO/MainProcess] Task tasks.scrape_pending_urls[f188b742-f398-481b-a63e-e52192ac513a] received
[2026-03-28 15:20:28,808: INFO/MainProcess] Task tasks.scrape_pending_urls[f188b742-f398-481b-a63e-e52192ac513a] succeeded in 0.002820200053974986s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,810: INFO/MainProcess] Task tasks.scrape_pending_urls[fb54e329-9b27-4354-bee2-ad816589de5a] received
[2026-03-28 15:20:28,815: INFO/MainProcess] Task tasks.scrape_pending_urls[fb54e329-9b27-4354-bee2-ad816589de5a] succeeded in 0.003827699925750494s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,817: INFO/MainProcess] Task tasks.scrape_pending_urls[ac94924b-5f38-4fe9-ba0b-e6a97d9a4307] received
[2026-03-28 15:20:28,820: INFO/MainProcess] Task tasks.scrape_pending_urls[ac94924b-5f38-4fe9-ba0b-e6a97d9a4307] succeeded in 0.0028782000299543142s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,822: INFO/MainProcess] Task tasks.scrape_pending_urls[723088e4-a355-4898-9c55-36cd8a8dc798] received
[2026-03-28 15:20:28,825: INFO/MainProcess] Task tasks.scrape_pending_urls[723088e4-a355-4898-9c55-36cd8a8dc798] succeeded in 0.002703599981032312s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,827: INFO/MainProcess] Task tasks.scrape_pending_urls[c623f217-3eb1-437f-975b-ad248c22e1bd] received
[2026-03-28 15:20:28,831: INFO/MainProcess] Task tasks.scrape_pending_urls[c623f217-3eb1-437f-975b-ad248c22e1bd] succeeded in 0.0028155999025329947s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,832: INFO/MainProcess] Task tasks.scrape_pending_urls[4569a9e7-c657-4271-b79e-3b4c769ff73e] received
[2026-03-28 15:20:28,834: INFO/MainProcess] Task tasks.scrape_pending_urls[4569a9e7-c657-4271-b79e-3b4c769ff73e] succeeded in 0.0021793999476358294s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,836: INFO/MainProcess] Task tasks.scrape_pending_urls[ca76f09e-73af-4156-af7b-5c69a42d930a] received
[2026-03-28 15:20:28,838: INFO/MainProcess] Task tasks.scrape_pending_urls[ca76f09e-73af-4156-af7b-5c69a42d930a] succeeded in 0.002116899937391281s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,839: INFO/MainProcess] Task tasks.scrape_pending_urls[3810e9e5-3b17-4a7e-aadc-08b5f566ea91] received
[2026-03-28 15:20:28,841: INFO/MainProcess] Task tasks.scrape_pending_urls[3810e9e5-3b17-4a7e-aadc-08b5f566ea91] succeeded in 0.002106300089508295s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,843: INFO/MainProcess] Task tasks.scrape_pending_urls[938ab9a8-7855-4943-8b24-88a601bb1565] received
[2026-03-28 15:20:28,847: INFO/MainProcess] Task tasks.scrape_pending_urls[938ab9a8-7855-4943-8b24-88a601bb1565] succeeded in 0.0029915999621152878s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,848: INFO/MainProcess] Task tasks.scrape_pending_urls[7bc12287-c01f-4aa6-aed9-1e26054c7d4e] received
[2026-03-28 15:20:28,851: INFO/MainProcess] Task tasks.scrape_pending_urls[7bc12287-c01f-4aa6-aed9-1e26054c7d4e] succeeded in 0.0021769999293610454s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,852: INFO/MainProcess] Task tasks.scrape_pending_urls[c6d3e35b-4d26-4c57-9fcf-a37a34da987c] received
[2026-03-28 15:20:28,854: INFO/MainProcess] Task tasks.scrape_pending_urls[c6d3e35b-4d26-4c57-9fcf-a37a34da987c] succeeded in 0.0021022999426349998s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,855: INFO/MainProcess] Task tasks.scrape_pending_urls[a7535acc-f0f8-4c9d-89cc-5203d7f1e4f3] received
[2026-03-28 15:20:28,858: INFO/MainProcess] Task tasks.scrape_pending_urls[a7535acc-f0f8-4c9d-89cc-5203d7f1e4f3] succeeded in 0.00212009996175766s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,860: INFO/MainProcess] Task tasks.scrape_pending_urls[5fd26171-454a-492b-83b7-f6d06403b3df] received
[2026-03-28 15:20:28,862: INFO/MainProcess] Task tasks.scrape_pending_urls[5fd26171-454a-492b-83b7-f6d06403b3df] succeeded in 0.0023843999952077866s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,864: INFO/MainProcess] Task tasks.scrape_pending_urls[c2ca212d-9b32-4ec1-aec2-8f9e1dfb9a83] received
[2026-03-28 15:20:28,866: INFO/MainProcess] Task tasks.scrape_pending_urls[c2ca212d-9b32-4ec1-aec2-8f9e1dfb9a83] succeeded in 0.0021386999869719148s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,867: INFO/MainProcess] Task tasks.scrape_pending_urls[2284e089-3be3-46a6-ba20-9e0e611238b1] received
[2026-03-28 15:20:28,870: INFO/MainProcess] Task tasks.scrape_pending_urls[2284e089-3be3-46a6-ba20-9e0e611238b1] succeeded in 0.002104800078086555s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,871: INFO/MainProcess] Task tasks.scrape_pending_urls[fec80fb5-d1df-4458-976f-cac4eb351e19] received
[2026-03-28 15:20:28,873: INFO/MainProcess] Task tasks.scrape_pending_urls[fec80fb5-d1df-4458-976f-cac4eb351e19] succeeded in 0.0020567000610753894s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,874: INFO/MainProcess] Task tasks.scrape_pending_urls[5e2ae82e-fd7c-45b4-ba16-cebd475aa2bb] received
[2026-03-28 15:20:28,878: INFO/MainProcess] Task tasks.scrape_pending_urls[5e2ae82e-fd7c-45b4-ba16-cebd475aa2bb] succeeded in 0.0025645000860095024s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,879: INFO/MainProcess] Task tasks.scrape_pending_urls[d0c93632-00a1-4eda-a3ae-1a45bf0956c8] received
[2026-03-28 15:20:28,882: INFO/MainProcess] Task tasks.scrape_pending_urls[d0c93632-00a1-4eda-a3ae-1a45bf0956c8] succeeded in 0.002127900021150708s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,883: INFO/MainProcess] Task tasks.scrape_pending_urls[23d9fdf7-685b-456c-8883-e631c458dfa9] received
[2026-03-28 15:20:28,886: INFO/MainProcess] Task tasks.scrape_pending_urls[23d9fdf7-685b-456c-8883-e631c458dfa9] succeeded in 0.0025496999733150005s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,887: INFO/MainProcess] Task tasks.scrape_pending_urls[00989ff1-36d5-4048-bc82-8d6c444bc212] received
[2026-03-28 15:20:28,890: INFO/MainProcess] Task tasks.scrape_pending_urls[00989ff1-36d5-4048-bc82-8d6c444bc212] succeeded in 0.0020926999859511852s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,891: INFO/MainProcess] Task tasks.scrape_pending_urls[d03cda56-27d3-4bd1-9b02-5702f687e688] received
[2026-03-28 15:20:28,894: INFO/MainProcess] Task tasks.scrape_pending_urls[d03cda56-27d3-4bd1-9b02-5702f687e688] succeeded in 0.0024379000533372164s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,895: INFO/MainProcess] Task tasks.scrape_pending_urls[aa175299-de9e-4a2d-b1e6-357a66866324] received
[2026-03-28 15:20:28,898: INFO/MainProcess] Task tasks.scrape_pending_urls[aa175299-de9e-4a2d-b1e6-357a66866324] succeeded in 0.0021619999315589666s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,899: INFO/MainProcess] Task tasks.scrape_pending_urls[885d05ff-715a-49f8-b8b8-e12b414d6c7e] received
[2026-03-28 15:20:28,901: INFO/MainProcess] Task tasks.scrape_pending_urls[885d05ff-715a-49f8-b8b8-e12b414d6c7e] succeeded in 0.0021211999701336026s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:28,902: INFO/MainProcess] Task tasks.scrape_pending_urls[1661274d-ae34-47c5-9e07-454f95019703] received
[2026-03-28 15:20:28,905: INFO/MainProcess] Task tasks.scrape_pending_urls[1661274d-ae34-47c5-9e07-454f95019703] succeeded in 0.0020791999995708466s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:20:33,567: INFO/MainProcess] Task tasks.scrape_pending_urls[0e4d09aa-6ffc-432a-8377-89d6ccdcaa8c] received
[2026-03-28 15:20:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[0e4d09aa-6ffc-432a-8377-89d6ccdcaa8c] succeeded in 0.0034401000011712313s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:21:03,567: INFO/MainProcess] Task tasks.scrape_pending_urls[e69bb721-5a65-48b6-9006-8869a7bcc1d9] received
[2026-03-28 15:21:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[e69bb721-5a65-48b6-9006-8869a7bcc1d9] succeeded in 0.0031621999805793166s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:21:33,567: INFO/MainProcess] Task tasks.scrape_pending_urls[455bbf38-85d0-40be-82fe-86c76456dacd] received
[2026-03-28 15:21:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[455bbf38-85d0-40be-82fe-86c76456dacd] succeeded in 0.003387099946849048s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:22:03,567: INFO/MainProcess] Task tasks.scrape_pending_urls[bb932824-1540-4cc9-b9d2-64c36d59e89b] received
[2026-03-28 15:22:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[bb932824-1540-4cc9-b9d2-64c36d59e89b] succeeded in 0.0031271999469026923s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:22:33,567: INFO/MainProcess] Task tasks.scrape_pending_urls[80b78bec-522d-441f-a68d-dd4c99a96b72] received
[2026-03-28 15:22:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[80b78bec-522d-441f-a68d-dd4c99a96b72] succeeded in 0.0033001999836415052s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:23:03,567: INFO/MainProcess] Task tasks.scrape_pending_urls[0fbdacae-fa1b-4876-8f44-9fc24e8511f4] received
[2026-03-28 15:23:03,572: INFO/MainProcess] Task tasks.scrape_pending_urls[0fbdacae-fa1b-4876-8f44-9fc24e8511f4] succeeded in 0.0038797000888735056s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:23:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[49e11d4e-67dc-4f6b-a7b2-9890938a7586] received
[2026-03-28 15:23:34,009: INFO/MainProcess] Task tasks.collect_system_metrics[49e11d4e-67dc-4f6b-a7b2-9890938a7586] succeeded in 0.5173651999793947s: {'cpu': 12.7, 'memory': 45.6}
[2026-03-28 15:23:34,011: INFO/MainProcess] Task tasks.scrape_pending_urls[36da0846-7e3f-4d77-b0fe-3c12c02b1b5c] received
[2026-03-28 15:23:34,085: INFO/MainProcess] Task tasks.scrape_pending_urls[36da0846-7e3f-4d77-b0fe-3c12c02b1b5c] succeeded in 0.074275599909015s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:24:03,567: INFO/MainProcess] Task tasks.scrape_pending_urls[1f83d7fa-ba01-45d5-a783-38fbfe321c7c] received
[2026-03-28 15:24:03,636: INFO/MainProcess] Task tasks.scrape_pending_urls[1f83d7fa-ba01-45d5-a783-38fbfe321c7c] succeeded in 0.06796789995860308s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:24:33,568: INFO/MainProcess] Task tasks.scrape_pending_urls[80e1f95b-aeef-46f6-bd36-ea9381ef62be] received
[2026-03-28 15:24:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[80e1f95b-aeef-46f6-bd36-ea9381ef62be] succeeded in 0.0032502999529242516s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:25:03,567: INFO/MainProcess] Task tasks.scrape_pending_urls[ab0fbb38-e0c2-422c-ba23-51449c1e3456] received
[2026-03-28 15:25:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[ab0fbb38-e0c2-422c-ba23-51449c1e3456] succeeded in 0.003535000025294721s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:25:33,567: INFO/MainProcess] Task tasks.scrape_pending_urls[15cfcfc4-9870-40a4-a533-3f7a18251945] received
[2026-03-28 15:25:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[15cfcfc4-9870-40a4-a533-3f7a18251945] succeeded in 0.0033580000745132565s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:26:03,567: INFO/MainProcess] Task tasks.scrape_pending_urls[5c872a0c-92a9-4d0f-a7be-e4f4d0799110] received
[2026-03-28 15:26:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[5c872a0c-92a9-4d0f-a7be-e4f4d0799110] succeeded in 0.0030321000376716256s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:26:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[b5c3e925-0be1-4a5d-9340-ea882ca39745] received
[2026-03-28 15:26:33,575: INFO/MainProcess] Task tasks.scrape_pending_urls[b5c3e925-0be1-4a5d-9340-ea882ca39745] succeeded in 0.0035221000434830785s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:27:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[d53fd2af-f037-4d03-9178-2dade4937609] received
[2026-03-28 15:27:03,575: INFO/MainProcess] Task tasks.scrape_pending_urls[d53fd2af-f037-4d03-9178-2dade4937609] succeeded in 0.003583699930459261s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:27:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[bdaa1ca9-4590-48bd-8096-ff903810db9e] received
[2026-03-28 15:27:33,574: INFO/MainProcess] Task tasks.scrape_pending_urls[bdaa1ca9-4590-48bd-8096-ff903810db9e] succeeded in 0.003031300031580031s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:28:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[d59528b8-f9bb-46db-957c-f17c3abf6f3d] received
[2026-03-28 15:28:03,575: INFO/MainProcess] Task tasks.scrape_pending_urls[d59528b8-f9bb-46db-957c-f17c3abf6f3d] succeeded in 0.003441200009547174s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:28:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[197baf5f-609c-4d4c-aff1-7bdc19041b4f] received
[2026-03-28 15:28:34,009: INFO/MainProcess] Task tasks.collect_system_metrics[197baf5f-609c-4d4c-aff1-7bdc19041b4f] succeeded in 0.5187020000303164s: {'cpu': 16.3, 'memory': 45.7}
[2026-03-28 15:28:34,011: INFO/MainProcess] Task tasks.scrape_pending_urls[45dacc95-b6f0-4813-9196-3a9fabf48c5f] received
[2026-03-28 15:28:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[45dacc95-b6f0-4813-9196-3a9fabf48c5f] succeeded in 0.003325199941173196s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:29:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[d12c7eb0-a7f9-4af0-9e4d-4cfa3263c82a] received
[2026-03-28 15:29:03,574: INFO/MainProcess] Task tasks.scrape_pending_urls[d12c7eb0-a7f9-4af0-9e4d-4cfa3263c82a] succeeded in 0.003183299908414483s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:29:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[cef39512-902b-4daa-8ebb-ebdbd96426b5] received
[2026-03-28 15:29:33,575: INFO/MainProcess] Task tasks.scrape_pending_urls[cef39512-902b-4daa-8ebb-ebdbd96426b5] succeeded in 0.0034562000073492527s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[cb5235d5-3e8c-443b-8446-20e5c5203ad3] received
[2026-03-28 15:30:00,005: INFO/MainProcess] Task tasks.purge_old_debug_html[cb5235d5-3e8c-443b-8446-20e5c5203ad3] succeeded in 0.0017240999732166529s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-28 15:30:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[cbcc631a-a642-45b5-8ae8-8bd4df3ea425] received
[2026-03-28 15:30:03,641: INFO/MainProcess] Task tasks.scrape_pending_urls[cbcc631a-a642-45b5-8ae8-8bd4df3ea425] succeeded in 0.06962650001514703s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:30:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[bbccae7d-2e71-4bf2-b7b8-11c117345267] received
[2026-03-28 15:30:33,576: INFO/MainProcess] Task tasks.scrape_pending_urls[bbccae7d-2e71-4bf2-b7b8-11c117345267] succeeded in 0.003636999987065792s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:31:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[fcde6f0a-a12f-4db2-9301-54413a3d6687] received
[2026-03-28 15:31:03,575: INFO/MainProcess] Task tasks.scrape_pending_urls[fcde6f0a-a12f-4db2-9301-54413a3d6687] succeeded in 0.0033536999253556132s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:31:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[9ae9efb4-c558-4a05-8821-93ffaee77ffb] received
[2026-03-28 15:31:33,575: INFO/MainProcess] Task tasks.scrape_pending_urls[9ae9efb4-c558-4a05-8821-93ffaee77ffb] succeeded in 0.0033735999604687095s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:32:03,571: INFO/MainProcess] Task tasks.scrape_pending_urls[fdef97a8-2749-4d3a-b396-6b930eaaa8f8] received
[2026-03-28 15:32:03,574: INFO/MainProcess] Task tasks.scrape_pending_urls[fdef97a8-2749-4d3a-b396-6b930eaaa8f8] succeeded in 0.0031027999939396977s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:32:33,571: INFO/MainProcess] Task tasks.scrape_pending_urls[f6a5d11c-cc15-461b-bc14-a0ed314f42aa] received
[2026-03-28 15:32:33,575: INFO/MainProcess] Task tasks.scrape_pending_urls[f6a5d11c-cc15-461b-bc14-a0ed314f42aa] succeeded in 0.003410100005567074s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:33:03,575: INFO/MainProcess] Task tasks.scrape_pending_urls[de001296-1e40-4ec0-b085-f47cc2493229] received
[2026-03-28 15:33:03,580: INFO/MainProcess] Task tasks.scrape_pending_urls[de001296-1e40-4ec0-b085-f47cc2493229] succeeded in 0.0036455000517889857s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:33:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[96baea48-ee38-4850-9ca0-e575a4746bab] received
[2026-03-28 15:33:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[96baea48-ee38-4850-9ca0-e575a4746bab] succeeded in 0.5186157999560237s: {'cpu': 15.5, 'memory': 45.5}
[2026-03-28 15:33:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[a1642db0-e22d-4f14-976a-725ed95f75a6] received
[2026-03-28 15:33:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[a1642db0-e22d-4f14-976a-725ed95f75a6] succeeded in 0.00347869994584471s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:34:03,576: INFO/MainProcess] Task tasks.scrape_pending_urls[e65b7101-60ff-447d-b6c6-b0f5b5b69b8d] received
[2026-03-28 15:34:03,580: INFO/MainProcess] Task tasks.scrape_pending_urls[e65b7101-60ff-447d-b6c6-b0f5b5b69b8d] succeeded in 0.0037675000494346023s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:34:33,575: INFO/MainProcess] Task tasks.scrape_pending_urls[a530e5d6-418d-4933-a0a7-b53be48723b9] received
[2026-03-28 15:34:33,579: INFO/MainProcess] Task tasks.scrape_pending_urls[a530e5d6-418d-4933-a0a7-b53be48723b9] succeeded in 0.0033864000579342246s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:35:03,575: INFO/MainProcess] Task tasks.scrape_pending_urls[f7860f11-8cfd-441d-a33c-440ba534cf4d] received
[2026-03-28 15:35:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[f7860f11-8cfd-441d-a33c-440ba534cf4d] succeeded in 0.003514499985612929s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:35:33,576: INFO/MainProcess] Task tasks.scrape_pending_urls[dff30227-795b-4717-a557-fc5ee2bfe1c8] received
[2026-03-28 15:35:33,580: INFO/MainProcess] Task tasks.scrape_pending_urls[dff30227-795b-4717-a557-fc5ee2bfe1c8] succeeded in 0.0036117000272497535s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:36:03,576: INFO/MainProcess] Task tasks.scrape_pending_urls[785115c3-2f01-47b2-b348-a8f42dc0926d] received
[2026-03-28 15:36:03,580: INFO/MainProcess] Task tasks.scrape_pending_urls[785115c3-2f01-47b2-b348-a8f42dc0926d] succeeded in 0.0036223999923095107s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:36:33,576: INFO/MainProcess] Task tasks.scrape_pending_urls[dde6ef47-ccb9-4304-af5b-cea0eaee2280] received
[2026-03-28 15:36:33,579: INFO/MainProcess] Task tasks.scrape_pending_urls[dde6ef47-ccb9-4304-af5b-cea0eaee2280] succeeded in 0.0032928999280557036s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:37:03,575: INFO/MainProcess] Task tasks.scrape_pending_urls[109b9394-4cf2-436c-93ab-5c6f8533a08f] received
[2026-03-28 15:37:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[109b9394-4cf2-436c-93ab-5c6f8533a08f] succeeded in 0.0034448999213054776s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:37:33,576: INFO/MainProcess] Task tasks.scrape_pending_urls[8f342a73-0dcf-4e9e-9462-606421a79636] received
[2026-03-28 15:37:33,579: INFO/MainProcess] Task tasks.scrape_pending_urls[8f342a73-0dcf-4e9e-9462-606421a79636] succeeded in 0.0034626000560820103s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:38:03,576: INFO/MainProcess] Task tasks.scrape_pending_urls[3533a0c5-7059-4707-9de2-6ddf79aca8a1] received
[2026-03-28 15:38:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[3533a0c5-7059-4707-9de2-6ddf79aca8a1] succeeded in 0.0033862999407574534s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:38:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[aa839c2d-f740-4692-9874-be634205c579] received
[2026-03-28 15:38:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[aa839c2d-f740-4692-9874-be634205c579] succeeded in 0.5194324000040069s: {'cpu': 17.5, 'memory': 45.5}
[2026-03-28 15:38:34,013: INFO/MainProcess] Task tasks.scrape_pending_urls[62e49ea5-495c-41ba-af81-256a47f00839] received
[2026-03-28 15:38:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[62e49ea5-495c-41ba-af81-256a47f00839] succeeded in 0.003339699935168028s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:39:03,576: INFO/MainProcess] Task tasks.scrape_pending_urls[1b168b44-3eb4-4ad7-8c67-725393a2b431] received
[2026-03-28 15:39:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[1b168b44-3eb4-4ad7-8c67-725393a2b431] succeeded in 0.0033032000064849854s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:39:33,579: INFO/MainProcess] Task tasks.scrape_pending_urls[ca3d64b2-1d84-4c9d-9023-207fca5647c7] received
[2026-03-28 15:39:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[ca3d64b2-1d84-4c9d-9023-207fca5647c7] succeeded in 0.003227700013667345s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:40:03,580: INFO/MainProcess] Task tasks.scrape_pending_urls[0ea6c79a-7974-4762-8bc9-bcf99c547453] received
[2026-03-28 15:40:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[0ea6c79a-7974-4762-8bc9-bcf99c547453] succeeded in 0.0033262999495491385s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:40:33,579: INFO/MainProcess] Task tasks.scrape_pending_urls[70f01de0-67e8-45f5-bb5b-57b18e07148f] received
[2026-03-28 15:40:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[70f01de0-67e8-45f5-bb5b-57b18e07148f] succeeded in 0.003306400030851364s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:41:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[bc5d494d-00e8-47ce-8b0c-bf15e19dec70] received
[2026-03-28 15:41:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[bc5d494d-00e8-47ce-8b0c-bf15e19dec70] succeeded in 0.003621599986217916s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:41:33,579: INFO/MainProcess] Task tasks.scrape_pending_urls[49d32b1b-45b1-4245-af65-dcbed327e520] received
[2026-03-28 15:41:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[49d32b1b-45b1-4245-af65-dcbed327e520] succeeded in 0.0031217000214383006s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:42:03,580: INFO/MainProcess] Task tasks.scrape_pending_urls[48f89d6f-3aba-444d-98aa-ecbdad4bb922] received
[2026-03-28 15:42:03,584: INFO/MainProcess] Task tasks.scrape_pending_urls[48f89d6f-3aba-444d-98aa-ecbdad4bb922] succeeded in 0.0034793999511748552s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:42:33,580: INFO/MainProcess] Task tasks.scrape_pending_urls[9885fed0-22fe-4ca8-92e4-9e9a0bc41c4d] received
[2026-03-28 15:42:33,584: INFO/MainProcess] Task tasks.scrape_pending_urls[9885fed0-22fe-4ca8-92e4-9e9a0bc41c4d] succeeded in 0.0036217999877408147s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:43:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[0719c345-a98c-4908-8d3f-bbb866d2181f] received
[2026-03-28 15:43:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[0719c345-a98c-4908-8d3f-bbb866d2181f] succeeded in 0.003145699971355498s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:43:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[08efdc4f-23e8-44f4-a9c9-b591eafbc82e] received
[2026-03-28 15:43:34,007: INFO/MainProcess] Task tasks.collect_system_metrics[08efdc4f-23e8-44f4-a9c9-b591eafbc82e] succeeded in 0.5167685000924394s: {'cpu': 18.7, 'memory': 45.6}
[2026-03-28 15:43:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[3167a0b1-5027-4c46-afb5-8483b7ff437d] received
[2026-03-28 15:43:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[3167a0b1-5027-4c46-afb5-8483b7ff437d] succeeded in 0.0031956000020727515s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:44:03,580: INFO/MainProcess] Task tasks.scrape_pending_urls[fae71b6e-626f-4f2a-a3a4-9fe4958a100c] received
[2026-03-28 15:44:03,584: INFO/MainProcess] Task tasks.scrape_pending_urls[fae71b6e-626f-4f2a-a3a4-9fe4958a100c] succeeded in 0.003442400018684566s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:44:33,580: INFO/MainProcess] Task tasks.scrape_pending_urls[525c967f-d968-4b96-ac36-8706a74a0f51] received
[2026-03-28 15:44:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[525c967f-d968-4b96-ac36-8706a74a0f51] succeeded in 0.003459200030192733s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:45:03,579: INFO/MainProcess] Task tasks.scrape_pending_urls[d4a418d4-0c77-4b97-99e1-4c9ec3bea8ba] received
[2026-03-28 15:45:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[d4a418d4-0c77-4b97-99e1-4c9ec3bea8ba] succeeded in 0.0031026999931782484s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:45:33,580: INFO/MainProcess] Task tasks.scrape_pending_urls[fc2ba841-b886-4e20-85b1-21e708f82e3b] received
[2026-03-28 15:45:33,584: INFO/MainProcess] Task tasks.scrape_pending_urls[fc2ba841-b886-4e20-85b1-21e708f82e3b] succeeded in 0.0034815999679267406s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:46:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[204acb04-042e-46ed-bd7e-55ca9b184ecf] received
[2026-03-28 15:46:03,587: INFO/MainProcess] Task tasks.scrape_pending_urls[204acb04-042e-46ed-bd7e-55ca9b184ecf] succeeded in 0.0035081999376416206s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:46:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[6ac7133d-3476-48ff-8baa-04a0160bc09b] received
[2026-03-28 15:46:33,586: INFO/MainProcess] Task tasks.scrape_pending_urls[6ac7133d-3476-48ff-8baa-04a0160bc09b] succeeded in 0.002993999980390072s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:47:03,584: INFO/MainProcess] Task tasks.scrape_pending_urls[65c161e4-b64e-4ed5-932d-697025fc7f9b] received
[2026-03-28 15:47:03,587: INFO/MainProcess] Task tasks.scrape_pending_urls[65c161e4-b64e-4ed5-932d-697025fc7f9b] succeeded in 0.0032463000388816s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:47:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[9f7fb332-75e5-4fc0-97e7-d15a9de0a610] received
[2026-03-28 15:47:33,587: INFO/MainProcess] Task tasks.scrape_pending_urls[9f7fb332-75e5-4fc0-97e7-d15a9de0a610] succeeded in 0.0032137000234797597s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:48:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[6603d218-d4c1-45ac-9b37-dc6303abea3c] received
[2026-03-28 15:48:03,587: INFO/MainProcess] Task tasks.scrape_pending_urls[6603d218-d4c1-45ac-9b37-dc6303abea3c] succeeded in 0.00346989999525249s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:48:33,479: INFO/MainProcess] Task tasks.reset_stale_processing_urls[dc25bb61-8bee-45c2-8d6f-33ab652b9761] received
[2026-03-28 15:48:33,483: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-28 15:48:33,484: INFO/MainProcess] Task tasks.reset_stale_processing_urls[dc25bb61-8bee-45c2-8d6f-33ab652b9761] succeeded in 0.004379400052130222s: {'reset': 0}
[2026-03-28 15:48:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[c4d3113a-f807-48ce-933c-cfab0b399fa1] received
[2026-03-28 15:48:33,995: INFO/MainProcess] Task tasks.collect_system_metrics[c4d3113a-f807-48ce-933c-cfab0b399fa1] succeeded in 0.5055362000130117s: {'cpu': 21.5, 'memory': 45.5}
[2026-03-28 15:48:33,997: INFO/MainProcess] Task tasks.scrape_pending_urls[dd6b5ef8-94b8-4117-a6cf-f1abadad297e] received
[2026-03-28 15:48:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[dd6b5ef8-94b8-4117-a6cf-f1abadad297e] succeeded in 0.003079200047068298s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:49:03,584: INFO/MainProcess] Task tasks.scrape_pending_urls[21c6455c-d543-41a9-a05c-cacdb5a549b6] received
[2026-03-28 15:49:03,587: INFO/MainProcess] Task tasks.scrape_pending_urls[21c6455c-d543-41a9-a05c-cacdb5a549b6] succeeded in 0.0032277998980134726s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:49:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[689ade40-9769-4595-87ee-9654cd7cfe47] received
[2026-03-28 15:49:33,587: INFO/MainProcess] Task tasks.scrape_pending_urls[689ade40-9769-4595-87ee-9654cd7cfe47] succeeded in 0.0037993999430909753s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:50:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[d70dff4f-679f-4292-8c0f-572b1844c0ff] received
[2026-03-28 15:50:03,588: INFO/MainProcess] Task tasks.scrape_pending_urls[d70dff4f-679f-4292-8c0f-572b1844c0ff] succeeded in 0.004183900076895952s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:50:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[53c1d072-4915-451f-858b-abec32252757] received
[2026-03-28 15:50:33,587: INFO/MainProcess] Task tasks.scrape_pending_urls[53c1d072-4915-451f-858b-abec32252757] succeeded in 0.0031353000085800886s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:51:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[f0ad3047-79f0-48eb-92fd-807753fd7726] received
[2026-03-28 15:51:03,587: INFO/MainProcess] Task tasks.scrape_pending_urls[f0ad3047-79f0-48eb-92fd-807753fd7726] succeeded in 0.003169700037688017s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:51:33,583: INFO/MainProcess] Task tasks.scrape_pending_urls[47a79f34-d5ef-4d24-a874-1aad0d2a53f7] received
[2026-03-28 15:51:33,587: INFO/MainProcess] Task tasks.scrape_pending_urls[47a79f34-d5ef-4d24-a874-1aad0d2a53f7] succeeded in 0.003104300005361438s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:52:03,583: INFO/MainProcess] Task tasks.scrape_pending_urls[3818c54a-ff0e-4cf7-845f-10af2e64984c] received
[2026-03-28 15:52:03,587: INFO/MainProcess] Task tasks.scrape_pending_urls[3818c54a-ff0e-4cf7-845f-10af2e64984c] succeeded in 0.0031435000710189342s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:52:33,588: INFO/MainProcess] Task tasks.scrape_pending_urls[1125511e-f2c9-4e32-958c-d39518ce0563] received
[2026-03-28 15:52:33,592: INFO/MainProcess] Task tasks.scrape_pending_urls[1125511e-f2c9-4e32-958c-d39518ce0563] succeeded in 0.0038711000233888626s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:53:03,588: INFO/MainProcess] Task tasks.scrape_pending_urls[2b99607f-0907-4163-a95a-e129478409a0] received
[2026-03-28 15:53:03,591: INFO/MainProcess] Task tasks.scrape_pending_urls[2b99607f-0907-4163-a95a-e129478409a0] succeeded in 0.00321670004632324s: {'status': 'idle', 'pending': 0}
[2026-03-28 15:53:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[3c7835eb-5e89-4325-8183-437f86899408] received
[2026-03-28 15:53:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[3c7835eb-5e89-4325-8183-437f86899408] succeeded in 0.5188739000586793s: {'cpu': 6.3, 'memory': 47.0}
[2026-03-28 15:53:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[16e0533d-85fc-496e-b75a-13f731e74fdb] received
[2026-03-28 15:53:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[16e0533d-85fc-496e-b75a-13f731e74fdb] succeeded in 0.0032813999569043517s: {'status': 'idle', 'pending': 0}
