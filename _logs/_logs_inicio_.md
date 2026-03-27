
===  BookingScraper Celery Worker  ===


 -------------- worker@HOUSE v5.4.0 (opalescent)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0 2026-03-26 22:19:45
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         bookingscraper:0x1ede4c58980
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

[2026-03-26 22:19:47,253: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-26 22:19:51,353: INFO/MainProcess] mingle: searching for neighbors
[2026-03-26 22:19:58,490: INFO/MainProcess] mingle: all alone
[2026-03-26 22:20:06,664: INFO/MainProcess] worker@HOUSE ready.
[2026-03-26 22:20:21,690: INFO/MainProcess] Task tasks.scrape_pending_urls[68bde746-1bf7-4899-957e-d7c4f384582c] received
[2026-03-26 22:20:23,862: INFO/MainProcess] Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5
[2026-03-26 22:20:23,975: INFO/MainProcess] Task tasks.scrape_pending_urls[68bde746-1bf7-4899-957e-d7c4f384582c] succeeded in 2.285126999951899s: {'status': 'idle', 'pending': 0}
[2026-03-26 22:20:45,585: INFO/MainProcess] Task tasks.scrape_pending_urls[83158b2d-500f-46e1-8a04-fc27d8542bae] received
[2026-03-26 22:20:47,612: INFO/MainProcess] scrape_pending_urls: starting auto-batch, pending=13
[2026-03-26 22:20:48,440: INFO/MainProcess] VPN: original IP = 45.144.113.254
[2026-03-26 22:20:49,290: INFO/MainProcess] VPN: home country detected = US
[2026-03-26 22:20:49,292: INFO/MainProcess] NordVPNManager initialised | interactive=False | original_ip=45.144.113.254 | home_country=US
[2026-03-26 22:20:49,292: INFO/MainProcess] ScraperService INIT | VPN_ENABLED=True | HEADLESS_BROWSER=False | workers=2 | languages=en,es,de,it,fr | vpn_interval=50s | vpn_countries=Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden
[2026-03-26 22:20:49,306: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-26 22:21:06,937: INFO/MainProcess] VPN connected to Germany — IP: 45.150.175.94
[2026-03-26 22:21:06,938: INFO/MainProcess] VPN connected OK before batch start.
[2026-03-26 22:21:06,939: INFO/MainProcess] Dispatching batch: urls=13 workers=2
[2026-03-26 22:21:06,940: INFO/MainProcess] Redis connection pool created: max_connections=20
[2026-03-26 22:21:11,929: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:11,930: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:25,161: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:26,756: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:29,975: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:30,961: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:38,399: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:45,107: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:54,778: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:56,244: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:21:56,244: INFO/MainProcess] CloudScraper failed for 0be5194c-0489-4065-a156-b1dc20755602/en — trying Selenium.
[2026-03-26 22:21:58,325: INFO/MainProcess] Selenium: Brave started
[2026-03-26 22:22:00,970: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:22:09,438: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-26 22:22:09,438: INFO/MainProcess] CloudScraper failed for 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c/en — trying Selenium.
[2026-03-26 22:24:21,236: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 22:24:23,151: INFO/MainProcess] Gallery: 137 images loaded after scroll
[2026-03-26 22:24:26,688: INFO/MainProcess] Gallery: 144 unique image URLs extracted
[2026-03-26 22:24:26,820: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 22:24:26,821: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 22:24:53,901: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 0be5194c-0489-4065-a156-b1dc20755602
[2026-03-26 22:25:02,058: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 3ca1a55e-c818-432d-817b-77a9924c586a
[2026-03-26 22:25:02,059: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 3ca1a55e-c818-432d-817b-77a9924c586a
[2026-03-26 22:25:02,071: INFO/MainProcess] URL 0be5194c-0489-4065-a156-b1dc20755602 lang=en: SUCCESS
[2026-03-26 22:25:04,930: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-26 22:25:13,474: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-26 22:25:18,125: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-26 22:25:32,563: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-26 22:25:38,746: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-26 22:25:47,725: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-26 22:25:47,725: INFO/MainProcess] CloudScraper failed for 0be5194c-0489-4065-a156-b1dc20755602/es — trying Selenium.
[2026-03-26 22:27:16,001: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 22:27:17,963: INFO/MainProcess] Gallery: 131 images loaded after scroll
[2026-03-26 22:27:21,267: INFO/MainProcess] Gallery: 138 unique image URLs extracted
[2026-03-26 22:27:21,402: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 22:27:21,403: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 22:27:46,742: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c
[2026-03-26 22:27:54,921: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 40ccbc88-add1-4521-92c6-ed2310a7fd3c
[2026-03-26 22:27:54,921: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 40ccbc88-add1-4521-92c6-ed2310a7fd3c
[2026-03-26 22:27:54,930: INFO/MainProcess] URL 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c lang=en: SUCCESS
[2026-03-26 22:27:57,651: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-26 22:28:05,976: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-26 22:28:10,537: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-26 22:28:41,369: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-26 22:28:47,490: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-26 22:29:04,390: INFO/MainProcess] URL 0be5194c-0489-4065-a156-b1dc20755602 lang=es: SUCCESS
[2026-03-26 22:29:07,262: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-26 22:29:13,651: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-26 22:29:13,652: INFO/MainProcess] CloudScraper failed for 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c/es — trying Selenium.
[2026-03-26 22:29:33,070: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-26 22:29:37,715: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-26 22:30:05,108: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-26 22:30:11,247: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-26 22:30:33,129: INFO/MainProcess] URL 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c lang=es: SUCCESS
[2026-03-26 22:30:35,742: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-26 22:30:42,762: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-26 22:30:42,762: INFO/MainProcess] CloudScraper failed for 0be5194c-0489-4065-a156-b1dc20755602/de — trying Selenium.
[2026-03-26 22:30:59,793: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-26 22:31:05,022: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-26 22:31:14,934: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-26 22:31:21,107: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-26 22:31:55,928: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-26 22:31:55,929: INFO/MainProcess] CloudScraper failed for 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c/de — trying Selenium.
[2026-03-26 22:32:00,700: INFO/MainProcess] URL 0be5194c-0489-4065-a156-b1dc20755602 lang=de: SUCCESS
[2026-03-26 22:32:03,496: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-26 22:32:39,009: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-26 22:32:43,791: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-26 22:32:52,452: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-26 22:32:58,642: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-26 22:33:13,165: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-26 22:33:13,166: INFO/MainProcess] CloudScraper failed for 0be5194c-0489-4065-a156-b1dc20755602/it — trying Selenium.
[2026-03-26 22:33:18,138: INFO/MainProcess] URL 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c lang=de: SUCCESS
[2026-03-26 22:33:20,851: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-26 22:33:29,638: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-26 22:33:34,336: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-26 22:33:55,165: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-26 22:34:01,336: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-26 22:34:14,655: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-26 22:34:14,655: INFO/MainProcess] CloudScraper failed for 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c/it — trying Selenium.
[2026-03-26 22:34:35,652: INFO/MainProcess] URL 0be5194c-0489-4065-a156-b1dc20755602 lang=it: SUCCESS
[2026-03-26 22:34:38,326: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-26 22:34:46,843: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-26 22:34:51,656: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-26 22:35:02,033: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-26 22:35:08,242: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-26 22:35:21,295: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-26 22:35:21,295: INFO/MainProcess] CloudScraper failed for 0be5194c-0489-4065-a156-b1dc20755602/fr — trying Selenium.
[2026-03-26 22:36:10,077: INFO/MainProcess] URL 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c lang=it: SUCCESS
[2026-03-26 22:36:12,903: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-26 22:36:25,148: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-26 22:36:29,958: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-26 22:36:39,392: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-26 22:36:45,592: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-26 22:36:59,118: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-26 22:36:59,119: INFO/MainProcess] CloudScraper failed for 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c/fr — trying Selenium.
[2026-03-26 22:37:27,321: INFO/MainProcess] URL 0be5194c-0489-4065-a156-b1dc20755602 lang=fr: SUCCESS
[2026-03-26 22:37:27,324: INFO/MainProcess] URL 0be5194c-0489-4065-a156-b1dc20755602: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 22:37:30,276: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-26 22:37:44,583: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-26 22:37:49,512: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-26 22:38:01,888: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-26 22:38:08,075: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-26 22:38:17,677: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-26 22:38:17,678: INFO/MainProcess] CloudScraper failed for d39b8b6a-6a1e-4801-8f45-3c072aa1488a/en — trying Selenium.
[2026-03-26 22:38:44,367: INFO/MainProcess] URL 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c lang=fr: SUCCESS
[2026-03-26 22:38:44,370: INFO/MainProcess] URL 0c3b1000-ce1f-4a0b-8c0a-6ce4068c445c: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 22:38:47,046: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-26 22:38:58,755: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-26 22:39:03,497: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-26 22:39:17,824: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-26 22:39:23,990: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-26 22:39:34,603: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-26 22:39:34,603: INFO/MainProcess] CloudScraper failed for 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7/en — trying Selenium.
[2026-03-26 22:41:06,089: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 22:41:07,995: INFO/MainProcess] Gallery: 87 images loaded after scroll
[2026-03-26 22:41:10,329: INFO/MainProcess] Gallery: 94 unique image URLs extracted
[2026-03-26 22:41:10,454: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 22:41:10,455: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 22:41:36,012: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for d39b8b6a-6a1e-4801-8f45-3c072aa1488a
[2026-03-26 22:41:43,589: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel fafcca95-621b-4a4d-8498-1f72b8143f9e
[2026-03-26 22:41:43,589: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel fafcca95-621b-4a4d-8498-1f72b8143f9e
[2026-03-26 22:41:43,597: INFO/MainProcess] URL d39b8b6a-6a1e-4801-8f45-3c072aa1488a lang=en: SUCCESS
[2026-03-26 22:41:46,437: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-26 22:42:00,705: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-26 22:42:05,439: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-26 22:42:14,620: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-26 22:42:20,804: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-26 22:42:34,392: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-26 22:42:34,393: INFO/MainProcess] CloudScraper failed for d39b8b6a-6a1e-4801-8f45-3c072aa1488a/es — trying Selenium.
[2026-03-26 22:43:57,331: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 22:43:59,317: INFO/MainProcess] Gallery: 266 images loaded after scroll
[2026-03-26 22:44:04,193: INFO/MainProcess] Gallery: 273 unique image URLs extracted
[2026-03-26 22:44:04,389: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 22:44:04,390: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 22:44:31,586: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7
[2026-03-26 22:44:38,792: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 4973394b-53d3-4a30-b733-4670dc73f622
[2026-03-26 22:44:38,793: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 4973394b-53d3-4a30-b733-4670dc73f622
[2026-03-26 22:44:38,799: INFO/MainProcess] URL 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7 lang=en: SUCCESS
[2026-03-26 22:44:41,649: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-26 22:44:53,336: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-26 22:44:58,163: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-26 22:45:06,677: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-26 22:45:12,842: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-26 22:45:22,526: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-26 22:45:22,527: INFO/MainProcess] CloudScraper failed for 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7/es — trying Selenium.
[2026-03-26 22:45:48,673: INFO/MainProcess] URL d39b8b6a-6a1e-4801-8f45-3c072aa1488a lang=es: SUCCESS
[2026-03-26 22:45:51,309: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-26 22:46:03,902: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-26 22:46:08,591: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-26 22:46:35,666: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-26 22:46:42,006: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-26 22:47:07,382: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-26 22:47:07,383: INFO/MainProcess] CloudScraper failed for d39b8b6a-6a1e-4801-8f45-3c072aa1488a/de — trying Selenium.
[2026-03-26 22:47:08,508: INFO/MainProcess] URL 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7 lang=es: SUCCESS
[2026-03-26 22:47:11,296: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-26 22:47:19,921: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-26 22:47:24,728: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-26 22:47:58,600: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-26 22:48:04,723: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-26 22:48:25,097: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-26 22:48:25,099: INFO/MainProcess] CloudScraper failed for 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7/de — trying Selenium.
[2026-03-26 22:48:27,201: INFO/MainProcess] URL d39b8b6a-6a1e-4801-8f45-3c072aa1488a lang=de: SUCCESS
[2026-03-26 22:48:29,934: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-26 22:48:56,013: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-26 22:49:00,850: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-26 22:49:13,288: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-26 22:49:19,469: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-26 22:49:48,013: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-26 22:49:48,013: INFO/MainProcess] CloudScraper failed for d39b8b6a-6a1e-4801-8f45-3c072aa1488a/it — trying Selenium.
[2026-03-26 22:50:00,277: INFO/MainProcess] URL 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7 lang=de: SUCCESS
[2026-03-26 22:50:02,949: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-26 22:50:35,613: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-26 22:50:40,372: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-26 22:50:51,089: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-26 22:50:57,268: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-26 22:51:06,205: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-26 22:51:06,205: INFO/MainProcess] CloudScraper failed for 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7/it — trying Selenium.
[2026-03-26 22:51:18,412: INFO/MainProcess] URL d39b8b6a-6a1e-4801-8f45-3c072aa1488a lang=it: SUCCESS
[2026-03-26 22:51:21,285: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-26 22:51:35,230: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-26 22:51:40,470: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-26 22:51:54,600: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-26 22:52:00,771: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-26 22:52:11,189: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-26 22:52:11,189: INFO/MainProcess] CloudScraper failed for d39b8b6a-6a1e-4801-8f45-3c072aa1488a/fr — trying Selenium.
[2026-03-26 22:52:35,401: INFO/MainProcess] URL 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7 lang=it: SUCCESS
[2026-03-26 22:52:38,044: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-26 22:52:50,421: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-26 22:52:55,244: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-26 22:53:07,566: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-26 22:53:13,747: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-26 22:53:26,136: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-26 22:53:26,136: INFO/MainProcess] CloudScraper failed for 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7/fr — trying Selenium.
[2026-03-26 22:53:55,122: INFO/MainProcess] URL d39b8b6a-6a1e-4801-8f45-3c072aa1488a lang=fr: SUCCESS
[2026-03-26 22:53:55,126: INFO/MainProcess] URL d39b8b6a-6a1e-4801-8f45-3c072aa1488a: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 22:53:57,896: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-26 22:54:09,097: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-26 22:54:13,751: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-26 22:54:27,800: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-26 22:54:33,979: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-26 22:54:43,678: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-26 22:54:43,678: INFO/MainProcess] CloudScraper failed for d20b76aa-cbc9-4f3e-9331-11d867cc7cb5/en — trying Selenium.
[2026-03-26 22:55:27,919: INFO/MainProcess] URL 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7 lang=fr: SUCCESS
[2026-03-26 22:55:27,922: INFO/MainProcess] URL 6d776ce8-c2d6-4e92-bd3b-a4f64f43c9d7: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 22:55:30,586: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-26 22:55:45,004: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-26 22:55:49,734: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-26 22:56:02,500: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-26 22:56:08,679: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-26 22:56:23,089: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-26 22:56:23,090: INFO/MainProcess] CloudScraper failed for d6327dd0-c60b-40d9-b6fd-51c57132cd56/en — trying Selenium.
[2026-03-26 22:57:48,295: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 22:57:50,230: INFO/MainProcess] Gallery: 118 images loaded after scroll
[2026-03-26 22:57:53,696: INFO/MainProcess] Gallery: 125 unique image URLs extracted
[2026-03-26 22:57:53,900: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 22:57:53,903: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 22:58:22,268: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for d20b76aa-cbc9-4f3e-9331-11d867cc7cb5
[2026-03-26 22:58:29,654: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel ec4f56ab-be1f-486e-a289-6ecf19ff7949
[2026-03-26 22:58:29,654: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel ec4f56ab-be1f-486e-a289-6ecf19ff7949
[2026-03-26 22:58:29,663: INFO/MainProcess] URL d20b76aa-cbc9-4f3e-9331-11d867cc7cb5 lang=en: SUCCESS
[2026-03-26 22:58:32,648: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-26 22:58:41,826: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-26 22:58:46,575: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-26 22:58:57,702: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-26 22:59:04,086: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-26 22:59:13,248: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-26 22:59:13,249: INFO/MainProcess] CloudScraper failed for d20b76aa-cbc9-4f3e-9331-11d867cc7cb5/es — trying Selenium.
[2026-03-26 23:00:42,883: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 23:00:44,782: INFO/MainProcess] Gallery: 24 images loaded after scroll
[2026-03-26 23:00:45,985: INFO/MainProcess] Gallery: 31 unique image URLs extracted
[2026-03-26 23:00:46,106: INFO/MainProcess] hotelPhotos JS: 24 photos extracted from page source
[2026-03-26 23:00:46,106: INFO/MainProcess] Gallery: 24 photos with full metadata (hotelPhotos JS)
[2026-03-26 23:01:12,504: INFO/MainProcess] Photos: 24 rich photo records (hotelPhotos JS) for d6327dd0-c60b-40d9-b6fd-51c57132cd56
[2026-03-26 23:01:16,744: INFO/MainProcess] download_photo_batch: 72/72 photo-files saved for hotel 24580ce1-834c-46df-b0e2-63a982ed51ca
[2026-03-26 23:01:16,745: INFO/MainProcess] ImageDownloader (photo_batch): 72/24 photos saved for hotel 24580ce1-834c-46df-b0e2-63a982ed51ca
[2026-03-26 23:01:16,753: INFO/MainProcess] URL d6327dd0-c60b-40d9-b6fd-51c57132cd56 lang=en: SUCCESS
[2026-03-26 23:01:19,654: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-26 23:01:30,279: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-26 23:01:35,021: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-26 23:02:07,992: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-26 23:02:14,178: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-26 23:02:24,447: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-26 23:02:24,448: INFO/MainProcess] CloudScraper failed for d6327dd0-c60b-40d9-b6fd-51c57132cd56/es — trying Selenium.
[2026-03-26 23:02:32,452: INFO/MainProcess] URL d20b76aa-cbc9-4f3e-9331-11d867cc7cb5 lang=es: SUCCESS
[2026-03-26 23:02:35,238: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-26 23:02:47,940: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-26 23:02:52,674: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-26 23:03:05,915: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-26 23:03:12,087: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-26 23:03:24,869: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-26 23:03:24,869: INFO/MainProcess] CloudScraper failed for d20b76aa-cbc9-4f3e-9331-11d867cc7cb5/de — trying Selenium.
[2026-03-26 23:03:51,029: INFO/MainProcess] URL d6327dd0-c60b-40d9-b6fd-51c57132cd56 lang=es: SUCCESS
[2026-03-26 23:03:53,740: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-26 23:04:03,316: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-26 23:04:08,054: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-26 23:04:19,207: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-26 23:04:25,384: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-26 23:04:36,602: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-26 23:04:36,603: INFO/MainProcess] CloudScraper failed for d6327dd0-c60b-40d9-b6fd-51c57132cd56/de — trying Selenium.
[2026-03-26 23:05:09,726: INFO/MainProcess] URL d20b76aa-cbc9-4f3e-9331-11d867cc7cb5 lang=de: SUCCESS
[2026-03-26 23:05:12,427: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-26 23:05:26,668: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-26 23:05:31,402: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-26 23:05:41,190: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-26 23:05:47,390: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-26 23:06:02,070: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-26 23:06:02,071: INFO/MainProcess] CloudScraper failed for d20b76aa-cbc9-4f3e-9331-11d867cc7cb5/it — trying Selenium.
[2026-03-26 23:06:41,826: INFO/MainProcess] URL d6327dd0-c60b-40d9-b6fd-51c57132cd56 lang=de: SUCCESS
[2026-03-26 23:06:44,464: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-26 23:06:53,362: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-26 23:06:58,044: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-26 23:07:08,298: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-26 23:07:14,477: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-26 23:07:26,125: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-26 23:07:26,125: INFO/MainProcess] CloudScraper failed for d6327dd0-c60b-40d9-b6fd-51c57132cd56/it — trying Selenium.
[2026-03-26 23:07:59,839: INFO/MainProcess] URL d20b76aa-cbc9-4f3e-9331-11d867cc7cb5 lang=it: SUCCESS
[2026-03-26 23:08:02,576: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-26 23:08:23,118: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-26 23:08:27,864: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-26 23:08:40,415: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-26 23:08:46,599: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-26 23:09:00,278: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-26 23:09:00,278: INFO/MainProcess] CloudScraper failed for d20b76aa-cbc9-4f3e-9331-11d867cc7cb5/fr — trying Selenium.
[2026-03-26 23:09:17,148: INFO/MainProcess] URL d6327dd0-c60b-40d9-b6fd-51c57132cd56 lang=it: SUCCESS
[2026-03-26 23:09:19,993: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-26 23:09:32,105: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-26 23:09:36,895: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-26 23:09:48,485: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-26 23:09:54,664: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-26 23:10:08,145: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-26 23:10:08,145: INFO/MainProcess] CloudScraper failed for d6327dd0-c60b-40d9-b6fd-51c57132cd56/fr — trying Selenium.
[2026-03-26 23:10:36,502: INFO/MainProcess] URL d20b76aa-cbc9-4f3e-9331-11d867cc7cb5 lang=fr: SUCCESS
[2026-03-26 23:10:36,505: INFO/MainProcess] URL d20b76aa-cbc9-4f3e-9331-11d867cc7cb5: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 23:10:39,315: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-26 23:10:53,338: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-26 23:10:58,120: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-26 23:11:12,606: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-26 23:11:18,773: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-26 23:11:40,613: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-26 23:11:40,613: INFO/MainProcess] CloudScraper failed for fd466c85-50eb-4099-83b5-1bc3613f80e8/en — trying Selenium.
[2026-03-26 23:12:07,234: INFO/MainProcess] URL d6327dd0-c60b-40d9-b6fd-51c57132cd56 lang=fr: SUCCESS
[2026-03-26 23:12:07,236: INFO/MainProcess] URL d6327dd0-c60b-40d9-b6fd-51c57132cd56: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 23:12:09,974: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:12:20,758: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:12:25,464: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:12:40,249: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:12:46,424: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:12:57,925: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:12:57,926: INFO/MainProcess] CloudScraper failed for 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/en — trying Selenium.
[2026-03-26 23:14:28,099: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 23:14:30,045: INFO/MainProcess] Gallery: 144 images loaded after scroll
[2026-03-26 23:14:33,953: INFO/MainProcess] Gallery: 151 unique image URLs extracted
[2026-03-26 23:14:34,151: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 23:14:34,152: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 23:15:00,315: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for fd466c85-50eb-4099-83b5-1bc3613f80e8
[2026-03-26 23:15:06,672: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 989493c0-934b-4b52-9627-53251cd06957
[2026-03-26 23:15:06,672: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 989493c0-934b-4b52-9627-53251cd06957
[2026-03-26 23:15:06,677: INFO/MainProcess] URL fd466c85-50eb-4099-83b5-1bc3613f80e8 lang=en: SUCCESS
[2026-03-26 23:15:09,730: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-26 23:15:33,588: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-26 23:15:38,341: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-26 23:15:46,813: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-26 23:15:52,968: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-26 23:16:03,139: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-26 23:16:03,140: INFO/MainProcess] CloudScraper failed for fd466c85-50eb-4099-83b5-1bc3613f80e8/es — trying Selenium.
[2026-03-26 23:16:18,672: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-26 23:16:27,952: INFO/MainProcess] Selenium retry 2 -- waiting 24s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:18:06,550: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-26 23:18:18,848: INFO/MainProcess] Selenium retry 3 -- waiting 15s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:19:49,057: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-26 23:19:49,058: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:19:49,060: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/en
[2026-03-26 23:19:49,060: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-26 23:19:50,081: INFO/MainProcess] VPN disconnected.
[2026-03-26 23:19:55,089: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-26 23:20:14,679: INFO/MainProcess] VPN connected to Sweden — IP: 31.40.213.83
[2026-03-26 23:20:14,679: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-26 23:20:14,681: INFO/MainProcess] VPN rotated — retrying 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/en with CloudScraper.
[2026-03-26 23:20:17,648: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:20:27,100: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:20:27,100: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-26 23:21:08,741: INFO/MainProcess] URL fd466c85-50eb-4099-83b5-1bc3613f80e8 lang=es: SUCCESS
[2026-03-26 23:21:11,681: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-26 23:21:23,104: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-26 23:21:27,902: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-26 23:21:37,829: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-26 23:21:44,220: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-26 23:21:52,483: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-26 23:21:52,484: INFO/MainProcess] CloudScraper failed for fd466c85-50eb-4099-83b5-1bc3613f80e8/de — trying Selenium.
[2026-03-26 23:22:25,769: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-26 23:22:35,064: INFO/MainProcess] Selenium retry 2 -- waiting 14s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:24:04,357: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-26 23:24:16,720: INFO/MainProcess] Selenium retry 3 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:25:47,953: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-26 23:25:47,954: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-26 23:25:47,977: WARNING/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033 lang=en: FAILED
[2026-03-26 23:25:50,814: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-26 23:25:59,299: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-26 23:26:04,106: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-26 23:26:14,314: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-26 23:26:20,534: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-26 23:26:31,832: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-26 23:26:31,832: INFO/MainProcess] CloudScraper failed for 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/es — trying Selenium.
[2026-03-26 23:27:05,786: INFO/MainProcess] URL fd466c85-50eb-4099-83b5-1bc3613f80e8 lang=de: SUCCESS
[2026-03-26 23:27:08,510: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-26 23:27:18,970: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-26 23:27:23,728: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-26 23:27:37,919: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-26 23:27:44,158: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-26 23:27:55,541: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-26 23:27:55,541: INFO/MainProcess] CloudScraper failed for fd466c85-50eb-4099-83b5-1bc3613f80e8/it — trying Selenium.
[2026-03-26 23:28:25,225: INFO/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033 lang=es: SUCCESS
[2026-03-26 23:28:27,941: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:28:38,226: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:28:43,002: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:29:05,025: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:29:11,239: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:29:20,752: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:29:20,752: INFO/MainProcess] CloudScraper failed for 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/de — trying Selenium.
[2026-03-26 23:29:57,571: INFO/MainProcess] URL fd466c85-50eb-4099-83b5-1bc3613f80e8 lang=it: SUCCESS
[2026-03-26 23:30:00,540: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-26 23:30:13,336: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-26 23:30:18,171: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-26 23:30:32,172: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-26 23:30:38,385: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-26 23:30:48,056: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-26 23:30:48,057: INFO/MainProcess] CloudScraper failed for fd466c85-50eb-4099-83b5-1bc3613f80e8/fr — trying Selenium.
[2026-03-26 23:31:13,916: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-26 23:31:22,532: INFO/MainProcess] Selenium retry 2 -- waiting 15s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:32:52,426: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-26 23:33:02,001: INFO/MainProcess] Selenium retry 3 -- waiting 22s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:34:39,172: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-26 23:34:39,172: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:34:39,175: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/de
[2026-03-26 23:34:39,176: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-26 23:34:40,190: INFO/MainProcess] VPN disconnected.
[2026-03-26 23:34:45,196: INFO/MainProcess] VPN: connecting to Italy (IT)...
[2026-03-26 23:35:04,252: INFO/MainProcess] VPN connected to Italy — IP: 45.80.28.209
[2026-03-26 23:35:04,252: INFO/MainProcess] VPN rotation successful → Italy
[2026-03-26 23:35:04,254: INFO/MainProcess] VPN rotated — retrying 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/de with CloudScraper.
[2026-03-26 23:35:07,084: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:35:21,208: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:35:21,209: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-26 23:35:58,555: INFO/MainProcess] URL fd466c85-50eb-4099-83b5-1bc3613f80e8 lang=fr: SUCCESS
[2026-03-26 23:35:58,557: INFO/MainProcess] URL fd466c85-50eb-4099-83b5-1bc3613f80e8: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-26 23:36:01,310: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-26 23:36:10,927: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-26 23:36:15,688: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-26 23:36:25,045: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-26 23:36:31,235: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-26 23:36:44,732: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-26 23:36:44,733: INFO/MainProcess] CloudScraper failed for 62026301-65c2-47da-8cb7-bd9f85fee61c/en — trying Selenium.
[2026-03-26 23:37:16,759: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-26 23:37:30,433: INFO/MainProcess] Selenium retry 2 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:39:08,802: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-26 23:39:21,043: INFO/MainProcess] Selenium retry 3 -- waiting 32s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:41:07,780: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-26 23:41:07,780: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-26 23:41:07,808: WARNING/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033 lang=de: FAILED
[2026-03-26 23:41:10,467: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:41:25,294: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:41:30,028: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:41:43,489: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:41:49,663: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:41:59,172: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:41:59,173: INFO/MainProcess] CloudScraper failed for 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/it — trying Selenium.
[2026-03-26 23:43:29,954: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-26 23:43:31,877: INFO/MainProcess] Gallery: 113 images loaded after scroll
[2026-03-26 23:43:35,736: INFO/MainProcess] Gallery: 120 unique image URLs extracted
[2026-03-26 23:43:35,905: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-26 23:43:35,906: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-26 23:44:02,416: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 62026301-65c2-47da-8cb7-bd9f85fee61c
[2026-03-26 23:44:09,643: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 513e9300-05b9-458b-a9d6-31a9294ab02a
[2026-03-26 23:44:09,644: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 513e9300-05b9-458b-a9d6-31a9294ab02a
[2026-03-26 23:44:09,653: INFO/MainProcess] URL 62026301-65c2-47da-8cb7-bd9f85fee61c lang=en: SUCCESS
[2026-03-26 23:44:12,587: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-26 23:44:24,792: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-26 23:44:29,550: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-26 23:44:38,043: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-26 23:44:44,239: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-26 23:44:57,501: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-26 23:44:57,501: INFO/MainProcess] CloudScraper failed for 62026301-65c2-47da-8cb7-bd9f85fee61c/es — trying Selenium.
[2026-03-26 23:45:19,303: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-26 23:45:27,905: INFO/MainProcess] Selenium retry 2 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:47:05,405: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-26 23:47:13,713: INFO/MainProcess] Selenium retry 3 -- waiting 35s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:49:03,555: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-26 23:49:03,556: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:49:03,560: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/it
[2026-03-26 23:49:03,560: INFO/MainProcess] VPN: rotating (current=IT)...
[2026-03-26 23:49:04,485: INFO/MainProcess] VPN disconnected.
[2026-03-26 23:49:09,490: INFO/MainProcess] VPN: connecting to Netherlands (NL)...
[2026-03-26 23:49:28,875: INFO/MainProcess] VPN connected to Netherlands — IP: 193.142.200.86
[2026-03-26 23:49:28,876: INFO/MainProcess] VPN rotation successful → Netherlands
[2026-03-26 23:49:28,877: INFO/MainProcess] VPN rotated — retrying 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/it with CloudScraper.
[2026-03-26 23:49:31,620: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:49:41,721: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:49:41,722: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-26 23:50:22,401: INFO/MainProcess] URL 62026301-65c2-47da-8cb7-bd9f85fee61c lang=es: SUCCESS
[2026-03-26 23:50:25,320: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-26 23:50:35,738: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-26 23:50:40,515: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-26 23:50:50,252: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-26 23:50:56,464: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-26 23:51:06,488: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-26 23:51:06,489: INFO/MainProcess] CloudScraper failed for 62026301-65c2-47da-8cb7-bd9f85fee61c/de — trying Selenium.
[2026-03-26 23:51:39,914: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-26 23:51:49,742: INFO/MainProcess] Selenium retry 2 -- waiting 19s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:53:23,717: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-26 23:53:36,443: INFO/MainProcess] Selenium retry 3 -- waiting 28s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:55:19,547: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-26 23:55:19,548: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-26 23:55:19,571: WARNING/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033 lang=it: FAILED
[2026-03-26 23:55:22,237: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:55:36,364: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:55:41,376: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:55:54,610: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:56:00,802: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:56:13,009: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:56:13,009: INFO/MainProcess] CloudScraper failed for 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/fr — trying Selenium.
[2026-03-26 23:56:38,099: INFO/MainProcess] URL 62026301-65c2-47da-8cb7-bd9f85fee61c lang=de: SUCCESS
[2026-03-26 23:56:40,871: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-26 23:56:53,555: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-26 23:56:58,353: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-26 23:57:07,776: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-26 23:57:13,976: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-26 23:57:23,223: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-26 23:57:23,223: INFO/MainProcess] CloudScraper failed for 62026301-65c2-47da-8cb7-bd9f85fee61c/it — trying Selenium.
[2026-03-26 23:57:55,216: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-26 23:58:08,224: INFO/MainProcess] Selenium retry 2 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-26 23:59:43,410: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-26 23:59:55,869: INFO/MainProcess] Selenium retry 3 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:01:30,380: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 00:01:30,380: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:01:30,383: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/fr
[2026-03-27 00:01:30,383: INFO/MainProcess] VPN: rotating (current=NL)...
[2026-03-27 00:01:31,378: INFO/MainProcess] VPN disconnected.
[2026-03-27 00:01:36,379: INFO/MainProcess] VPN: connecting to Netherlands (NL)...
[2026-03-27 00:01:55,436: INFO/MainProcess] VPN connected to Netherlands — IP: 91.242.248.156
[2026-03-27 00:01:55,436: INFO/MainProcess] VPN rotation successful → Netherlands
[2026-03-27 00:01:55,438: INFO/MainProcess] VPN rotated — retrying 0daaf80d-fe8c-46d1-8d5a-919eef1ed033/fr with CloudScraper.
[2026-03-27 00:01:58,199: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:02:12,804: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:02:12,805: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-27 00:02:48,882: INFO/MainProcess] URL 62026301-65c2-47da-8cb7-bd9f85fee61c lang=it: SUCCESS
[2026-03-27 00:02:51,558: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 00:03:03,191: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 00:03:07,862: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 00:03:20,625: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 00:03:26,790: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 00:03:38,415: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 00:03:38,415: INFO/MainProcess] CloudScraper failed for 62026301-65c2-47da-8cb7-bd9f85fee61c/fr — trying Selenium.
[2026-03-27 00:04:07,458: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 00:04:22,410: INFO/MainProcess] Selenium retry 2 -- waiting 14s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:05:51,497: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 00:06:06,125: INFO/MainProcess] Selenium retry 3 -- waiting 29s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:07:49,553: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 00:07:49,554: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 00:07:49,583: WARNING/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033 lang=fr: FAILED
[2026-03-27 00:07:49,588: WARNING/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033: PARTIAL — Incomplete: 1/5 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr']
[2026-03-27 00:07:49,595: INFO/MainProcess] URL 0daaf80d-fe8c-46d1-8d5a-919eef1ed033 marked incomplete — data PRESERVED. ok=['es'] fail=['en', 'de', 'it', 'fr']
[2026-03-27 00:07:52,368: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 00:08:03,886: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 00:08:08,603: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 00:08:21,383: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 00:08:27,549: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 00:08:38,340: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 00:08:38,340: INFO/MainProcess] CloudScraper failed for 08c34c44-c87f-403a-9262-6f7b5cd2aec2/en — trying Selenium.
[2026-03-27 00:09:07,146: INFO/MainProcess] URL 62026301-65c2-47da-8cb7-bd9f85fee61c lang=fr: SUCCESS
[2026-03-27 00:09:07,148: INFO/MainProcess] URL 62026301-65c2-47da-8cb7-bd9f85fee61c: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-27 00:09:09,881: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 00:09:35,142: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 00:09:39,972: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 00:09:48,865: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 00:09:55,031: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 00:10:09,801: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 00:10:09,801: INFO/MainProcess] CloudScraper failed for 409b9eff-e38f-40e7-a057-f354ae727c55/en — trying Selenium.
[2026-03-27 00:11:28,170: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 00:11:30,061: INFO/MainProcess] Gallery: 40 images loaded after scroll
[2026-03-27 00:11:32,392: INFO/MainProcess] Gallery: 47 unique image URLs extracted
[2026-03-27 00:11:32,541: INFO/MainProcess] hotelPhotos JS: 40 photos extracted from page source
[2026-03-27 00:11:32,545: INFO/MainProcess] Gallery: 40 photos with full metadata (hotelPhotos JS)
[2026-03-27 00:11:58,718: INFO/MainProcess] Photos: 40 rich photo records (hotelPhotos JS) for 08c34c44-c87f-403a-9262-6f7b5cd2aec2
[2026-03-27 00:12:04,944: INFO/MainProcess] download_photo_batch: 120/120 photo-files saved for hotel 7669d683-b5de-434c-9ffa-d712a1c38cd0
[2026-03-27 00:12:04,944: INFO/MainProcess] ImageDownloader (photo_batch): 120/40 photos saved for hotel 7669d683-b5de-434c-9ffa-d712a1c38cd0
[2026-03-27 00:12:04,951: INFO/MainProcess] URL 08c34c44-c87f-403a-9262-6f7b5cd2aec2 lang=en: SUCCESS
[2026-03-27 00:12:07,876: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 00:12:17,157: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 00:12:21,821: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 00:12:33,186: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 00:12:39,582: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 00:12:51,620: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 00:12:51,621: INFO/MainProcess] CloudScraper failed for 08c34c44-c87f-403a-9262-6f7b5cd2aec2/es — trying Selenium.
[2026-03-27 00:14:20,525: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 00:14:22,420: INFO/MainProcess] Gallery: 57 images loaded after scroll
[2026-03-27 00:14:24,162: INFO/MainProcess] Gallery: 64 unique image URLs extracted
[2026-03-27 00:14:24,281: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 00:14:24,281: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 00:14:49,996: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 409b9eff-e38f-40e7-a057-f354ae727c55
[2026-03-27 00:14:56,553: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 8d8fb026-9ce1-4f1e-9fc7-992db5de9197
[2026-03-27 00:14:56,553: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 8d8fb026-9ce1-4f1e-9fc7-992db5de9197
[2026-03-27 00:14:56,559: INFO/MainProcess] URL 409b9eff-e38f-40e7-a057-f354ae727c55 lang=en: SUCCESS
[2026-03-27 00:14:59,463: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 00:15:35,461: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 00:15:40,248: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 00:15:55,158: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 00:16:01,484: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 00:16:08,600: INFO/MainProcess] URL 08c34c44-c87f-403a-9262-6f7b5cd2aec2 lang=es: SUCCESS
[2026-03-27 00:16:11,456: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 00:16:14,190: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 00:16:14,190: INFO/MainProcess] CloudScraper failed for 409b9eff-e38f-40e7-a057-f354ae727c55/es — trying Selenium.
[2026-03-27 00:16:24,596: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 00:16:29,237: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 00:16:39,428: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 00:16:45,603: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 00:16:56,977: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 00:16:56,977: INFO/MainProcess] CloudScraper failed for 08c34c44-c87f-403a-9262-6f7b5cd2aec2/de — trying Selenium.
[2026-03-27 00:17:32,682: INFO/MainProcess] URL 409b9eff-e38f-40e7-a057-f354ae727c55 lang=es: SUCCESS
[2026-03-27 00:17:35,322: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 00:17:49,557: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 00:17:54,309: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 00:18:07,181: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 00:18:13,366: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 00:18:23,383: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 00:18:23,383: INFO/MainProcess] CloudScraper failed for 409b9eff-e38f-40e7-a057-f354ae727c55/de — trying Selenium.
[2026-03-27 00:18:52,169: INFO/MainProcess] URL 08c34c44-c87f-403a-9262-6f7b5cd2aec2 lang=de: SUCCESS
[2026-03-27 00:18:55,200: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 00:19:05,485: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 00:19:10,241: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 00:19:21,770: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 00:19:27,949: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 00:19:41,919: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 00:19:41,920: INFO/MainProcess] CloudScraper failed for 08c34c44-c87f-403a-9262-6f7b5cd2aec2/it — trying Selenium.
[2026-03-27 00:20:23,040: INFO/MainProcess] URL 409b9eff-e38f-40e7-a057-f354ae727c55 lang=de: SUCCESS
[2026-03-27 00:20:25,744: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 00:20:35,770: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 00:20:40,427: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 00:20:53,946: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 00:21:00,113: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 00:21:10,726: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 00:21:10,726: INFO/MainProcess] CloudScraper failed for 409b9eff-e38f-40e7-a057-f354ae727c55/it — trying Selenium.
[2026-03-27 00:21:40,935: INFO/MainProcess] URL 08c34c44-c87f-403a-9262-6f7b5cd2aec2 lang=it: SUCCESS
[2026-03-27 00:21:43,661: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 00:21:51,801: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 00:21:56,506: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 00:22:10,334: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 00:22:16,513: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 00:22:28,541: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 00:22:28,541: INFO/MainProcess] CloudScraper failed for 08c34c44-c87f-403a-9262-6f7b5cd2aec2/fr — trying Selenium.
[2026-03-27 00:22:59,945: INFO/MainProcess] URL 409b9eff-e38f-40e7-a057-f354ae727c55 lang=it: SUCCESS
[2026-03-27 00:23:02,732: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 00:23:16,075: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 00:23:20,859: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 00:23:33,402: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 00:23:39,590: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 00:23:54,368: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 00:23:54,368: INFO/MainProcess] CloudScraper failed for 409b9eff-e38f-40e7-a057-f354ae727c55/fr — trying Selenium.
[2026-03-27 00:24:19,147: INFO/MainProcess] URL 08c34c44-c87f-403a-9262-6f7b5cd2aec2 lang=fr: SUCCESS
[2026-03-27 00:24:19,150: INFO/MainProcess] URL 08c34c44-c87f-403a-9262-6f7b5cd2aec2: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-27 00:24:21,915: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 00:24:32,368: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 00:24:37,083: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 00:24:51,330: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 00:24:57,500: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 00:25:10,755: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 00:25:10,755: INFO/MainProcess] CloudScraper failed for ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2/en — trying Selenium.
[2026-03-27 00:25:50,242: INFO/MainProcess] URL 409b9eff-e38f-40e7-a057-f354ae727c55 lang=fr: SUCCESS
[2026-03-27 00:25:50,245: INFO/MainProcess] URL 409b9eff-e38f-40e7-a057-f354ae727c55: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-27 00:25:52,922: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 00:26:02,845: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 00:26:07,502: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 00:26:28,084: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 00:26:34,260: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 00:26:47,722: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 00:26:47,723: INFO/MainProcess] CloudScraper failed for 99af3a44-1a6f-43ce-aa07-5581ab1ae067/en — trying Selenium.
[2026-03-27 00:28:10,650: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 00:28:12,569: INFO/MainProcess] Gallery: 70 images loaded after scroll
[2026-03-27 00:28:15,315: INFO/MainProcess] Gallery: 77 unique image URLs extracted
[2026-03-27 00:28:15,469: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 00:28:15,471: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 00:28:42,299: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2
[2026-03-27 00:28:50,210: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel e5d83006-9667-493b-be76-b74852056ac9
[2026-03-27 00:28:50,210: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel e5d83006-9667-493b-be76-b74852056ac9
[2026-03-27 00:28:50,225: INFO/MainProcess] URL ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2 lang=en: SUCCESS
[2026-03-27 00:28:53,034: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 00:29:01,848: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 00:29:06,559: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 00:29:17,871: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 00:29:24,052: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 00:29:51,411: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 00:29:51,411: INFO/MainProcess] CloudScraper failed for ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2/es — trying Selenium.
[2026-03-27 00:31:01,580: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 00:31:03,483: INFO/MainProcess] Gallery: 34 images loaded after scroll
[2026-03-27 00:31:05,730: INFO/MainProcess] Gallery: 41 unique image URLs extracted
[2026-03-27 00:31:05,842: INFO/MainProcess] hotelPhotos JS: 34 photos extracted from page source
[2026-03-27 00:31:05,843: INFO/MainProcess] Gallery: 34 photos with full metadata (hotelPhotos JS)
[2026-03-27 00:31:32,521: INFO/MainProcess] Photos: 34 rich photo records (hotelPhotos JS) for 99af3a44-1a6f-43ce-aa07-5581ab1ae067
[2026-03-27 00:31:37,747: INFO/MainProcess] download_photo_batch: 102/102 photo-files saved for hotel 8ee8a530-552b-47bd-81b2-30e90bb901ac
[2026-03-27 00:31:37,747: INFO/MainProcess] ImageDownloader (photo_batch): 102/34 photos saved for hotel 8ee8a530-552b-47bd-81b2-30e90bb901ac
[2026-03-27 00:31:37,752: INFO/MainProcess] URL 99af3a44-1a6f-43ce-aa07-5581ab1ae067 lang=en: SUCCESS
[2026-03-27 00:31:40,611: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 00:31:53,355: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 00:31:58,036: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 00:32:09,609: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 00:32:15,789: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 00:32:29,165: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 00:32:29,166: INFO/MainProcess] CloudScraper failed for 99af3a44-1a6f-43ce-aa07-5581ab1ae067/es — trying Selenium.
[2026-03-27 00:32:51,180: INFO/MainProcess] URL ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2 lang=es: SUCCESS
[2026-03-27 00:32:53,829: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 00:33:08,525: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 00:33:13,351: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 00:33:46,466: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 00:33:52,593: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 00:34:10,067: INFO/MainProcess] URL 99af3a44-1a6f-43ce-aa07-5581ab1ae067 lang=es: SUCCESS
[2026-03-27 00:34:12,765: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 00:34:23,714: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 00:34:23,828: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 00:34:23,829: INFO/MainProcess] CloudScraper failed for ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2/de — trying Selenium.
[2026-03-27 00:34:28,581: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 00:34:40,016: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 00:34:46,184: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 00:34:54,547: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 00:34:54,548: INFO/MainProcess] CloudScraper failed for 99af3a44-1a6f-43ce-aa07-5581ab1ae067/de — trying Selenium.
[2026-03-27 00:35:41,901: INFO/MainProcess] URL ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2 lang=de: SUCCESS
[2026-03-27 00:35:44,611: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 00:36:07,872: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 00:36:12,762: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 00:36:25,143: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 00:36:31,345: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 00:37:00,018: INFO/MainProcess] URL 99af3a44-1a6f-43ce-aa07-5581ab1ae067 lang=de: SUCCESS
[2026-03-27 00:37:01,166: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 00:37:01,167: INFO/MainProcess] CloudScraper failed for ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2/it — trying Selenium.
[2026-03-27 00:37:02,664: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 00:37:12,371: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 00:37:17,188: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 00:37:29,400: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 00:37:35,578: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 00:37:48,753: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 00:37:48,754: INFO/MainProcess] CloudScraper failed for 99af3a44-1a6f-43ce-aa07-5581ab1ae067/it — trying Selenium.
[2026-03-27 00:38:20,658: INFO/MainProcess] URL ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2 lang=it: SUCCESS
[2026-03-27 00:38:23,341: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 00:38:33,073: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 00:38:37,791: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 00:38:50,489: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 00:38:56,673: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 00:39:07,291: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 00:39:07,291: INFO/MainProcess] CloudScraper failed for ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2/fr — trying Selenium.
[2026-03-27 00:39:53,119: INFO/MainProcess] URL 99af3a44-1a6f-43ce-aa07-5581ab1ae067 lang=it: SUCCESS
[2026-03-27 00:39:55,773: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 00:40:04,137: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 00:40:08,806: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 00:40:18,589: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 00:40:24,761: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 00:40:35,678: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 00:40:35,679: INFO/MainProcess] CloudScraper failed for 99af3a44-1a6f-43ce-aa07-5581ab1ae067/fr — trying Selenium.
[2026-03-27 00:41:12,437: INFO/MainProcess] URL ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2 lang=fr: SUCCESS
[2026-03-27 00:41:12,439: INFO/MainProcess] URL ac714704-dc3f-4e4f-9f91-a36d1e4f1cb2: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-27 00:42:30,534: INFO/MainProcess] URL 99af3a44-1a6f-43ce-aa07-5581ab1ae067 lang=fr: SUCCESS
[2026-03-27 00:42:30,536: INFO/MainProcess] URL 99af3a44-1a6f-43ce-aa07-5581ab1ae067: COMPLETE (5/5) langs=['en', 'es', 'de', 'it', 'fr']
[2026-03-27 00:42:32,780: INFO/MainProcess] Selenium browser closed after batch completion.
[2026-03-27 00:42:32,780: INFO/MainProcess] scrape_pending_urls: batch complete — {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-27 00:42:32,783: INFO/MainProcess] Task tasks.scrape_pending_urls[83158b2d-500f-46e1-8a04-fc27d8542bae] succeeded in 8507.197558299988s: {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-27 00:42:32,961: INFO/MainProcess] Task tasks.collect_system_metrics[e446248d-934b-457f-8d2f-847a0c902a9a] received
[2026-03-27 00:42:33,486: INFO/MainProcess] Task tasks.collect_system_metrics[e446248d-934b-457f-8d2f-847a0c902a9a] succeeded in 0.5240124000702053s: {'cpu': 18.3, 'memory': 44.6}
[2026-03-27 00:42:33,488: INFO/MainProcess] Task tasks.purge_old_debug_html[033b5289-e183-4071-9569-69381c63576e] received
[2026-03-27 00:42:33,490: INFO/MainProcess] Task tasks.purge_old_debug_html[033b5289-e183-4071-9569-69381c63576e] succeeded in 0.0017821999499574304s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 00:42:33,492: INFO/MainProcess] Task tasks.scrape_pending_urls[e81231a4-d86a-4340-b1f1-692ef2a3f4a6] received
[2026-03-27 00:42:33,496: INFO/MainProcess] Task tasks.scrape_pending_urls[e81231a4-d86a-4340-b1f1-692ef2a3f4a6] succeeded in 0.003608600003644824s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:33,499: INFO/MainProcess] Task tasks.collect_system_metrics[758e4237-1481-4b8e-bfde-9ff09738a016] received
[2026-03-27 00:42:34,017: INFO/MainProcess] Task tasks.collect_system_metrics[758e4237-1481-4b8e-bfde-9ff09738a016] succeeded in 0.5176269001094624s: {'cpu': 18.9, 'memory': 44.6}
[2026-03-27 00:42:34,019: INFO/MainProcess] Task tasks.reset_stale_processing_urls[431bc868-092c-429e-83cb-7b0b17bcab03] received
[2026-03-27 00:42:34,023: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 00:42:34,024: INFO/MainProcess] Task tasks.reset_stale_processing_urls[431bc868-092c-429e-83cb-7b0b17bcab03] succeeded in 0.005174999940209091s: {'reset': 0}
[2026-03-27 00:42:34,026: INFO/MainProcess] Task tasks.scrape_pending_urls[8e508085-7a7b-42ee-8f37-d53da7100149] received
[2026-03-27 00:42:34,030: INFO/MainProcess] Task tasks.scrape_pending_urls[8e508085-7a7b-42ee-8f37-d53da7100149] succeeded in 0.0030936000403016806s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:34,032: INFO/MainProcess] Task tasks.collect_system_metrics[ecddee34-60fc-4b70-a392-f962bc798e2e] received
[2026-03-27 00:42:34,538: INFO/MainProcess] Task tasks.collect_system_metrics[ecddee34-60fc-4b70-a392-f962bc798e2e] succeeded in 0.5057732999557629s: {'cpu': 10.0, 'memory': 44.5}
[2026-03-27 00:42:34,540: INFO/MainProcess] Task tasks.reset_stale_processing_urls[75974008-3ef2-4403-a1f9-34b8677a9f39] received
[2026-03-27 00:42:34,542: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 00:42:34,543: INFO/MainProcess] Task tasks.reset_stale_processing_urls[75974008-3ef2-4403-a1f9-34b8677a9f39] succeeded in 0.003164399997331202s: {'reset': 0}
[2026-03-27 00:42:34,545: INFO/MainProcess] Task tasks.scrape_pending_urls[66d0ee1c-a76d-4946-9a33-3ace8bdd2e2e] received
[2026-03-27 00:42:34,549: INFO/MainProcess] Task tasks.scrape_pending_urls[66d0ee1c-a76d-4946-9a33-3ace8bdd2e2e] succeeded in 0.0037611000007018447s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:34,560: INFO/MainProcess] Task tasks.collect_system_metrics[c6c11dc9-51a2-4648-a97e-95a3e82eb6e4] received
[2026-03-27 00:42:35,067: INFO/MainProcess] Task tasks.collect_system_metrics[c6c11dc9-51a2-4648-a97e-95a3e82eb6e4] succeeded in 0.5070751999737695s: {'cpu': 14.6, 'memory': 44.7}
[2026-03-27 00:42:35,070: INFO/MainProcess] Task tasks.purge_old_debug_html[1361e6f7-db25-413b-93e4-c49867c7a776] received
[2026-03-27 00:42:35,072: INFO/MainProcess] Task tasks.purge_old_debug_html[1361e6f7-db25-413b-93e4-c49867c7a776] succeeded in 0.0019687999738380313s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 00:42:35,074: INFO/MainProcess] Task tasks.scrape_pending_urls[fd3af4b0-09cf-4db4-bb21-eb4677068421] received
[2026-03-27 00:42:35,078: INFO/MainProcess] Task tasks.scrape_pending_urls[fd3af4b0-09cf-4db4-bb21-eb4677068421] succeeded in 0.0029906999552622437s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:35,079: INFO/MainProcess] Task tasks.collect_system_metrics[be2f0f12-6917-44be-96f6-206910c45425] received
[2026-03-27 00:42:35,599: INFO/MainProcess] Task tasks.collect_system_metrics[be2f0f12-6917-44be-96f6-206910c45425] succeeded in 0.5190052000107244s: {'cpu': 3.5, 'memory': 44.6}
[2026-03-27 00:42:35,601: INFO/MainProcess] Task tasks.reset_stale_processing_urls[05e70a65-9c54-4db0-8b58-439af236cc12] received
[2026-03-27 00:42:35,605: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 00:42:35,606: INFO/MainProcess] Task tasks.reset_stale_processing_urls[05e70a65-9c54-4db0-8b58-439af236cc12] succeeded in 0.004156799986958504s: {'reset': 0}
[2026-03-27 00:42:35,608: INFO/MainProcess] Task tasks.scrape_pending_urls[fee7f9a3-4cf3-4605-b503-34668408ede6] received
[2026-03-27 00:42:35,611: INFO/MainProcess] Task tasks.scrape_pending_urls[fee7f9a3-4cf3-4605-b503-34668408ede6] succeeded in 0.0030207999516278505s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:35,614: INFO/MainProcess] Task tasks.collect_system_metrics[8ee441af-ffc5-432e-9c30-f873c074fab1] received
[2026-03-27 00:42:36,131: INFO/MainProcess] Task tasks.collect_system_metrics[8ee441af-ffc5-432e-9c30-f873c074fab1] succeeded in 0.5173215999966487s: {'cpu': 5.1, 'memory': 44.6}
[2026-03-27 00:42:36,133: INFO/MainProcess] Task tasks.ensure_log_partitions[af9dfafd-6d7d-4a75-8efe-a29748a3d1b3] received
[2026-03-27 00:42:36,145: INFO/MainProcess] Task tasks.ensure_log_partitions[af9dfafd-6d7d-4a75-8efe-a29748a3d1b3] succeeded in 0.011061000055633485s: {'created': [], 'skipped': ['scraping_logs_2026_03', 'scraping_logs_2026_04', 'scraping_logs_2026_05'], 'errors': []}
[2026-03-27 00:42:36,148: INFO/MainProcess] Task tasks.scrape_pending_urls[77b12b68-3850-440e-a6e2-2ed18e16a0c8] received
[2026-03-27 00:42:36,152: INFO/MainProcess] Task tasks.scrape_pending_urls[77b12b68-3850-440e-a6e2-2ed18e16a0c8] succeeded in 0.003601799951866269s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:36,153: INFO/MainProcess] Task tasks.collect_system_metrics[dca78a1f-574b-4fea-bc97-e49e7d1934f4] received
[2026-03-27 00:42:36,671: INFO/MainProcess] Task tasks.collect_system_metrics[dca78a1f-574b-4fea-bc97-e49e7d1934f4] succeeded in 0.5174675999442115s: {'cpu': 0.4, 'memory': 44.6}
[2026-03-27 00:42:36,674: INFO/MainProcess] Task tasks.reset_stale_processing_urls[b231e473-ca2d-4a1b-a360-ba884e960ca0] received
[2026-03-27 00:42:36,676: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 00:42:36,678: INFO/MainProcess] Task tasks.reset_stale_processing_urls[b231e473-ca2d-4a1b-a360-ba884e960ca0] succeeded in 0.0037840999430045485s: {'reset': 0}
[2026-03-27 00:42:36,679: INFO/MainProcess] Task tasks.scrape_pending_urls[3c2bcbcd-6222-46d0-aafe-047f44fdfd9f] received
[2026-03-27 00:42:36,683: INFO/MainProcess] Task tasks.scrape_pending_urls[3c2bcbcd-6222-46d0-aafe-047f44fdfd9f] succeeded in 0.0029990000184625387s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:36,685: INFO/MainProcess] Task tasks.collect_system_metrics[46a65da6-a5bf-4134-88a4-af3a543be007] received
[2026-03-27 00:42:37,200: INFO/MainProcess] Task tasks.collect_system_metrics[46a65da6-a5bf-4134-88a4-af3a543be007] succeeded in 0.5148226000601426s: {'cpu': 4.6, 'memory': 44.6}
[2026-03-27 00:42:37,202: INFO/MainProcess] Task tasks.purge_old_debug_html[4bf5fb91-c816-4dc9-8841-c5da547c0943] received
[2026-03-27 00:42:37,204: INFO/MainProcess] Task tasks.purge_old_debug_html[4bf5fb91-c816-4dc9-8841-c5da547c0943] succeeded in 0.0016568000428378582s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 00:42:37,206: INFO/MainProcess] Task tasks.scrape_pending_urls[9c4ad3b8-4a01-44ca-bbae-242b558e7b33] received
[2026-03-27 00:42:37,209: INFO/MainProcess] Task tasks.scrape_pending_urls[9c4ad3b8-4a01-44ca-bbae-242b558e7b33] succeeded in 0.0028952000429853797s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:37,211: INFO/MainProcess] Task tasks.collect_system_metrics[8bded8f7-db2a-4cb5-af7a-f69f3b824d33] received
[2026-03-27 00:42:37,729: INFO/MainProcess] Task tasks.collect_system_metrics[8bded8f7-db2a-4cb5-af7a-f69f3b824d33] succeeded in 0.5171640000771731s: {'cpu': 4.7, 'memory': 44.6}
[2026-03-27 00:42:37,731: INFO/MainProcess] Task tasks.scrape_pending_urls[0335d3db-e12e-463c-af56-1c791d2ff605] received
[2026-03-27 00:42:37,735: INFO/MainProcess] Task tasks.scrape_pending_urls[0335d3db-e12e-463c-af56-1c791d2ff605] succeeded in 0.003729799995198846s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:37,737: INFO/MainProcess] Task tasks.collect_system_metrics[98ef27b4-7cfb-4a18-b2d2-08694c8b984f] received
[2026-03-27 00:42:38,256: INFO/MainProcess] Task tasks.collect_system_metrics[98ef27b4-7cfb-4a18-b2d2-08694c8b984f] succeeded in 0.5189284000080079s: {'cpu': 12.3, 'memory': 44.7}
[2026-03-27 00:42:38,258: INFO/MainProcess] Task tasks.scrape_pending_urls[c1f4e2fe-f824-4e1e-b7ad-b64d77c638db] received
[2026-03-27 00:42:38,262: INFO/MainProcess] Task tasks.scrape_pending_urls[c1f4e2fe-f824-4e1e-b7ad-b64d77c638db] succeeded in 0.003110199933871627s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:38,264: INFO/MainProcess] Task tasks.collect_system_metrics[98cbaa11-ad8e-4591-8eb5-6f47dfa3b17f] received
[2026-03-27 00:42:38,781: INFO/MainProcess] Task tasks.collect_system_metrics[98cbaa11-ad8e-4591-8eb5-6f47dfa3b17f] succeeded in 0.5168513000244275s: {'cpu': 5.1, 'memory': 44.7}
[2026-03-27 00:42:38,783: INFO/MainProcess] Task tasks.scrape_pending_urls[f68002dc-7d17-4745-aa00-cf8098d3bce4] received
[2026-03-27 00:42:38,787: INFO/MainProcess] Task tasks.scrape_pending_urls[f68002dc-7d17-4745-aa00-cf8098d3bce4] succeeded in 0.0038273000391200185s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:38,789: INFO/MainProcess] Task tasks.collect_system_metrics[91271530-0fdd-45ab-94bf-7fd7dad37fc8] received
[2026-03-27 00:42:39,306: INFO/MainProcess] Task tasks.collect_system_metrics[91271530-0fdd-45ab-94bf-7fd7dad37fc8] succeeded in 0.516601899988018s: {'cpu': 2.3, 'memory': 44.7}
[2026-03-27 00:42:39,308: INFO/MainProcess] Task tasks.scrape_pending_urls[c4d524e2-33c2-41d8-b5fa-d8a3a1b15525] received
[2026-03-27 00:42:39,312: INFO/MainProcess] Task tasks.scrape_pending_urls[c4d524e2-33c2-41d8-b5fa-d8a3a1b15525] succeeded in 0.003484100103378296s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:39,314: INFO/MainProcess] Task tasks.collect_system_metrics[51ee5d81-b8d6-4b1d-ba0b-3216506a3320] received
[2026-03-27 00:42:39,824: INFO/MainProcess] Task tasks.collect_system_metrics[51ee5d81-b8d6-4b1d-ba0b-3216506a3320] succeeded in 0.5094534999225289s: {'cpu': 9.2, 'memory': 44.7}
[2026-03-27 00:42:39,826: INFO/MainProcess] Task tasks.scrape_pending_urls[4eefb977-9973-4ae6-842d-b137dbe4fb3d] received
[2026-03-27 00:42:39,830: INFO/MainProcess] Task tasks.scrape_pending_urls[4eefb977-9973-4ae6-842d-b137dbe4fb3d] succeeded in 0.003518100013025105s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:39,832: INFO/MainProcess] Task tasks.collect_system_metrics[7f7750aa-e514-4f22-84ef-dd8ed1085668] received
[2026-03-27 00:42:40,350: INFO/MainProcess] Task tasks.collect_system_metrics[7f7750aa-e514-4f22-84ef-dd8ed1085668] succeeded in 0.5175079999025911s: {'cpu': 6.7, 'memory': 44.7}
[2026-03-27 00:42:40,352: INFO/MainProcess] Task tasks.scrape_pending_urls[eae6d895-8284-4e0f-ae99-9b51e8469af8] received
[2026-03-27 00:42:40,356: INFO/MainProcess] Task tasks.scrape_pending_urls[eae6d895-8284-4e0f-ae99-9b51e8469af8] succeeded in 0.004015399958007038s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:40,358: INFO/MainProcess] Task tasks.collect_system_metrics[5fa72187-2dbc-4235-a8a3-9af92d58c27b] received
[2026-03-27 00:42:40,864: INFO/MainProcess] Task tasks.collect_system_metrics[5fa72187-2dbc-4235-a8a3-9af92d58c27b] succeeded in 0.5054378999629989s: {'cpu': 3.9, 'memory': 44.7}
[2026-03-27 00:42:40,866: INFO/MainProcess] Task tasks.scrape_pending_urls[dc89856e-0ef6-431d-a7e7-826b7d8fe611] received
[2026-03-27 00:42:40,871: INFO/MainProcess] Task tasks.scrape_pending_urls[dc89856e-0ef6-431d-a7e7-826b7d8fe611] succeeded in 0.004062899970449507s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:40,872: INFO/MainProcess] Task tasks.collect_system_metrics[2322347d-a66b-47c6-8aaf-855efe2d52f8] received
[2026-03-27 00:42:41,390: INFO/MainProcess] Task tasks.collect_system_metrics[2322347d-a66b-47c6-8aaf-855efe2d52f8] succeeded in 0.5172699999529868s: {'cpu': 5.5, 'memory': 44.7}
[2026-03-27 00:42:41,392: INFO/MainProcess] Task tasks.scrape_pending_urls[7a244cda-eeab-452f-9a03-3146e2db00a7] received
[2026-03-27 00:42:41,396: INFO/MainProcess] Task tasks.scrape_pending_urls[7a244cda-eeab-452f-9a03-3146e2db00a7] succeeded in 0.0030270999995991588s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:41,397: INFO/MainProcess] Task tasks.collect_system_metrics[eb3245dc-b97b-44d8-88cb-23f35d4da1df] received
[2026-03-27 00:42:41,914: INFO/MainProcess] Task tasks.collect_system_metrics[eb3245dc-b97b-44d8-88cb-23f35d4da1df] succeeded in 0.5164757000748068s: {'cpu': 0.0, 'memory': 44.7}
[2026-03-27 00:42:41,916: INFO/MainProcess] Task tasks.scrape_pending_urls[9650a424-2b98-4bd2-9b12-a4cb09b29bb9] received
[2026-03-27 00:42:41,920: INFO/MainProcess] Task tasks.scrape_pending_urls[9650a424-2b98-4bd2-9b12-a4cb09b29bb9] succeeded in 0.0033897999674081802s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:41,922: INFO/MainProcess] Task tasks.collect_system_metrics[3c96aeaf-2d78-4954-bbac-c9efef7d6d73] received
[2026-03-27 00:42:42,440: INFO/MainProcess] Task tasks.collect_system_metrics[3c96aeaf-2d78-4954-bbac-c9efef7d6d73] succeeded in 0.5174726000986993s: {'cpu': 4.3, 'memory': 44.7}
[2026-03-27 00:42:42,441: INFO/MainProcess] Task tasks.scrape_pending_urls[086f957c-f2fa-4a19-bbd5-0449cd68090c] received
[2026-03-27 00:42:42,445: INFO/MainProcess] Task tasks.scrape_pending_urls[086f957c-f2fa-4a19-bbd5-0449cd68090c] succeeded in 0.0027329999720677733s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:42,446: INFO/MainProcess] Task tasks.collect_system_metrics[28a18775-e2bb-43da-9e93-0092508aa260] received
[2026-03-27 00:42:42,964: INFO/MainProcess] Task tasks.collect_system_metrics[28a18775-e2bb-43da-9e93-0092508aa260] succeeded in 0.5177778000943363s: {'cpu': 3.5, 'memory': 44.7}
[2026-03-27 00:42:42,967: INFO/MainProcess] Task tasks.scrape_pending_urls[0afd01e7-4a58-4754-ae3b-ea3dde12a781] received
[2026-03-27 00:42:42,970: INFO/MainProcess] Task tasks.scrape_pending_urls[0afd01e7-4a58-4754-ae3b-ea3dde12a781] succeeded in 0.003369900048710406s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:42,972: INFO/MainProcess] Task tasks.collect_system_metrics[9f485e2f-2be8-4ee4-9e9b-a4ba60219d25] received
[2026-03-27 00:42:43,489: INFO/MainProcess] Task tasks.collect_system_metrics[9f485e2f-2be8-4ee4-9e9b-a4ba60219d25] succeeded in 0.5169227999867871s: {'cpu': 6.8, 'memory': 44.7}
[2026-03-27 00:42:43,492: INFO/MainProcess] Task tasks.scrape_pending_urls[19b35f41-a067-459f-a17c-403d0deb60d6] received
[2026-03-27 00:42:43,496: INFO/MainProcess] Task tasks.scrape_pending_urls[19b35f41-a067-459f-a17c-403d0deb60d6] succeeded in 0.003918600035831332s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:43,498: INFO/MainProcess] Task tasks.collect_system_metrics[1d87c131-f11d-4d89-be7a-46fdcf20a980] received
[2026-03-27 00:42:44,016: INFO/MainProcess] Task tasks.collect_system_metrics[1d87c131-f11d-4d89-be7a-46fdcf20a980] succeeded in 0.5170740999747068s: {'cpu': 7.4, 'memory': 44.7}
[2026-03-27 00:42:44,018: INFO/MainProcess] Task tasks.scrape_pending_urls[6d74de97-1acb-4e73-9237-c214d1b3f534] received
[2026-03-27 00:42:44,021: INFO/MainProcess] Task tasks.scrape_pending_urls[6d74de97-1acb-4e73-9237-c214d1b3f534] succeeded in 0.0034666999708861113s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:44,023: INFO/MainProcess] Task tasks.collect_system_metrics[bd582134-1c83-4a2e-915d-c33e7c6dac89] received
[2026-03-27 00:42:44,541: INFO/MainProcess] Task tasks.collect_system_metrics[bd582134-1c83-4a2e-915d-c33e7c6dac89] succeeded in 0.5178132998989895s: {'cpu': 12.1, 'memory': 44.6}
[2026-03-27 00:42:44,544: INFO/MainProcess] Task tasks.scrape_pending_urls[46785800-a673-4bb7-b0a2-a13c78bd0170] received
[2026-03-27 00:42:44,547: INFO/MainProcess] Task tasks.scrape_pending_urls[46785800-a673-4bb7-b0a2-a13c78bd0170] succeeded in 0.0033415000652894378s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:44,549: INFO/MainProcess] Task tasks.collect_system_metrics[264bbca1-f26b-4084-8301-9f321c72da7d] received
[2026-03-27 00:42:45,067: INFO/MainProcess] Task tasks.collect_system_metrics[264bbca1-f26b-4084-8301-9f321c72da7d] succeeded in 0.5169194999616593s: {'cpu': 3.2, 'memory': 44.7}
[2026-03-27 00:42:45,069: INFO/MainProcess] Task tasks.scrape_pending_urls[c91939cf-bca4-4f4e-a7e4-9011fe6cd82d] received
[2026-03-27 00:42:45,072: INFO/MainProcess] Task tasks.scrape_pending_urls[c91939cf-bca4-4f4e-a7e4-9011fe6cd82d] succeeded in 0.0033613000996410847s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:45,074: INFO/MainProcess] Task tasks.collect_system_metrics[9cb07792-8980-4b13-9b26-20162663444d] received
[2026-03-27 00:42:45,592: INFO/MainProcess] Task tasks.collect_system_metrics[9cb07792-8980-4b13-9b26-20162663444d] succeeded in 0.5178234999766573s: {'cpu': 2.3, 'memory': 44.7}
[2026-03-27 00:42:45,594: INFO/MainProcess] Task tasks.scrape_pending_urls[06442b94-ac10-484c-a511-2356c7234793] received
[2026-03-27 00:42:45,598: INFO/MainProcess] Task tasks.scrape_pending_urls[06442b94-ac10-484c-a511-2356c7234793] succeeded in 0.002791200065985322s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[d9c07384-966b-4732-a3c1-f97b536d4fda] received
[2026-03-27 00:42:46,116: INFO/MainProcess] Task tasks.collect_system_metrics[d9c07384-966b-4732-a3c1-f97b536d4fda] succeeded in 0.5165006999159232s: {'cpu': 3.2, 'memory': 44.7}
[2026-03-27 00:42:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[afd98a6b-8638-4bc8-a323-997c05dc7a74] received
[2026-03-27 00:42:46,122: INFO/MainProcess] Task tasks.scrape_pending_urls[afd98a6b-8638-4bc8-a323-997c05dc7a74] succeeded in 0.003700300003401935s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:46,124: INFO/MainProcess] Task tasks.collect_system_metrics[8ba3a043-4b6a-48ac-86ef-652f7203cdc8] received
[2026-03-27 00:42:46,642: INFO/MainProcess] Task tasks.collect_system_metrics[8ba3a043-4b6a-48ac-86ef-652f7203cdc8] succeeded in 0.5172282999847084s: {'cpu': 3.9, 'memory': 44.7}
[2026-03-27 00:42:46,644: INFO/MainProcess] Task tasks.scrape_pending_urls[1c55461d-4de0-494b-8794-4fa7953afcf3] received
[2026-03-27 00:42:46,647: INFO/MainProcess] Task tasks.scrape_pending_urls[1c55461d-4de0-494b-8794-4fa7953afcf3] succeeded in 0.0034204000839963555s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:46,650: INFO/MainProcess] Task tasks.collect_system_metrics[7d854586-0c6e-4c0a-af5d-51c821fda6fd] received
[2026-03-27 00:42:47,168: INFO/MainProcess] Task tasks.collect_system_metrics[7d854586-0c6e-4c0a-af5d-51c821fda6fd] succeeded in 0.5172815000405535s: {'cpu': 10.3, 'memory': 44.7}
[2026-03-27 00:42:47,170: INFO/MainProcess] Task tasks.scrape_pending_urls[4a3b7b86-3cf2-4f56-ae4f-f78c2206eb51] received
[2026-03-27 00:42:47,174: INFO/MainProcess] Task tasks.scrape_pending_urls[4a3b7b86-3cf2-4f56-ae4f-f78c2206eb51] succeeded in 0.003958199988119304s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:47,176: INFO/MainProcess] Task tasks.collect_system_metrics[3f5be5fc-91de-4028-8016-28f8d0c4e61c] received
[2026-03-27 00:42:47,694: INFO/MainProcess] Task tasks.collect_system_metrics[3f5be5fc-91de-4028-8016-28f8d0c4e61c] succeeded in 0.5173647000920027s: {'cpu': 4.7, 'memory': 44.7}
[2026-03-27 00:42:47,696: INFO/MainProcess] Task tasks.scrape_pending_urls[7b0a07b1-824b-4402-9f82-623dd4c19050] received
[2026-03-27 00:42:47,699: INFO/MainProcess] Task tasks.scrape_pending_urls[7b0a07b1-824b-4402-9f82-623dd4c19050] succeeded in 0.0027634999714791775s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:47,701: INFO/MainProcess] Task tasks.scrape_pending_urls[7de37219-1040-40f4-886f-2ea68130b412] received
[2026-03-27 00:42:47,704: INFO/MainProcess] Task tasks.scrape_pending_urls[7de37219-1040-40f4-886f-2ea68130b412] succeeded in 0.0025872999103739858s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:47,705: INFO/MainProcess] Task tasks.scrape_pending_urls[24dc7049-08b3-48e3-88e6-f685219e76d9] received
[2026-03-27 00:42:47,709: INFO/MainProcess] Task tasks.scrape_pending_urls[24dc7049-08b3-48e3-88e6-f685219e76d9] succeeded in 0.003463099943473935s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:47,711: INFO/MainProcess] Task tasks.scrape_pending_urls[5c9f36cc-ae19-40ea-8744-0ad3ca37d9f1] received
[2026-03-27 00:42:47,714: INFO/MainProcess] Task tasks.scrape_pending_urls[5c9f36cc-ae19-40ea-8744-0ad3ca37d9f1] succeeded in 0.002868099953047931s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:47,715: INFO/MainProcess] Task tasks.scrape_pending_urls[e5aece83-4bbc-442b-8cc6-d3850f7cc3ef] received
[2026-03-27 00:42:47,718: INFO/MainProcess] Task tasks.scrape_pending_urls[e5aece83-4bbc-442b-8cc6-d3850f7cc3ef] succeeded in 0.002459999988786876s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:47,719: INFO/MainProcess] Task tasks.scrape_pending_urls[460d8da7-ff03-410b-8ab4-c82bbf7f6971] received
[2026-03-27 00:42:47,722: INFO/MainProcess] Task tasks.scrape_pending_urls[460d8da7-ff03-410b-8ab4-c82bbf7f6971] succeeded in 0.002592999953776598s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,097: INFO/MainProcess] Task tasks.scrape_pending_urls[2c91b2ef-67ac-4304-9b40-f88ad975fb2a] received
[2026-03-27 00:42:48,100: INFO/MainProcess] Task tasks.scrape_pending_urls[2c91b2ef-67ac-4304-9b40-f88ad975fb2a] succeeded in 0.0027774000773206353s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,102: INFO/MainProcess] Task tasks.scrape_pending_urls[f9932286-ea13-4288-99d2-a858dece121d] received
[2026-03-27 00:42:48,106: INFO/MainProcess] Task tasks.scrape_pending_urls[f9932286-ea13-4288-99d2-a858dece121d] succeeded in 0.003738699946552515s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,110: INFO/MainProcess] Task tasks.scrape_pending_urls[eca79914-7e2e-46bd-a174-2d1804626aed] received
[2026-03-27 00:42:48,113: INFO/MainProcess] Task tasks.scrape_pending_urls[eca79914-7e2e-46bd-a174-2d1804626aed] succeeded in 0.0030960000585764647s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,115: INFO/MainProcess] Task tasks.scrape_pending_urls[f24b01b1-3708-4bed-a476-594a56e53503] received
[2026-03-27 00:42:48,118: INFO/MainProcess] Task tasks.scrape_pending_urls[f24b01b1-3708-4bed-a476-594a56e53503] succeeded in 0.002800900023430586s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,120: INFO/MainProcess] Task tasks.scrape_pending_urls[88380741-8960-4470-bcfb-1e058da956f6] received
[2026-03-27 00:42:48,123: INFO/MainProcess] Task tasks.scrape_pending_urls[88380741-8960-4470-bcfb-1e058da956f6] succeeded in 0.0032469999277964234s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,125: INFO/MainProcess] Task tasks.scrape_pending_urls[d76ff2d1-9198-483d-bc09-bf2f29be85d6] received
[2026-03-27 00:42:48,129: INFO/MainProcess] Task tasks.scrape_pending_urls[d76ff2d1-9198-483d-bc09-bf2f29be85d6] succeeded in 0.0033141999738290906s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,131: INFO/MainProcess] Task tasks.scrape_pending_urls[9eb5ea0e-509a-485c-bbc5-463b3e6a0143] received
[2026-03-27 00:42:48,134: INFO/MainProcess] Task tasks.scrape_pending_urls[9eb5ea0e-509a-485c-bbc5-463b3e6a0143] succeeded in 0.0027939999708905816s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,136: INFO/MainProcess] Task tasks.scrape_pending_urls[c7945601-8417-48b3-8e8e-74e902dfc823] received
[2026-03-27 00:42:48,139: INFO/MainProcess] Task tasks.scrape_pending_urls[c7945601-8417-48b3-8e8e-74e902dfc823] succeeded in 0.003384400042705238s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,141: INFO/MainProcess] Task tasks.scrape_pending_urls[58fcc5bb-febf-4d6b-820f-75f7c507948c] received
[2026-03-27 00:42:48,145: INFO/MainProcess] Task tasks.scrape_pending_urls[58fcc5bb-febf-4d6b-820f-75f7c507948c] succeeded in 0.002795599983073771s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,146: INFO/MainProcess] Task tasks.scrape_pending_urls[b1b2633b-4749-459f-a43f-afbdc3745768] received
[2026-03-27 00:42:48,149: INFO/MainProcess] Task tasks.scrape_pending_urls[b1b2633b-4749-459f-a43f-afbdc3745768] succeeded in 0.0026428999844938517s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,151: INFO/MainProcess] Task tasks.scrape_pending_urls[9a1709c3-75ad-40b6-bce8-159ce4908294] received
[2026-03-27 00:42:48,154: INFO/MainProcess] Task tasks.scrape_pending_urls[9a1709c3-75ad-40b6-bce8-159ce4908294] succeeded in 0.0029007999692112207s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,157: INFO/MainProcess] Task tasks.scrape_pending_urls[6f032bb8-e59d-4d51-a1ee-b843d3b78c35] received
[2026-03-27 00:42:48,160: INFO/MainProcess] Task tasks.scrape_pending_urls[6f032bb8-e59d-4d51-a1ee-b843d3b78c35] succeeded in 0.0028362999437376857s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,162: INFO/MainProcess] Task tasks.scrape_pending_urls[b2c9587e-d091-4527-b24f-5bcfa044aee0] received
[2026-03-27 00:42:48,165: INFO/MainProcess] Task tasks.scrape_pending_urls[b2c9587e-d091-4527-b24f-5bcfa044aee0] succeeded in 0.0027127000503242016s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,166: INFO/MainProcess] Task tasks.scrape_pending_urls[33d848b3-3360-4296-9ceb-0d2bcf917771] received
[2026-03-27 00:42:48,169: INFO/MainProcess] Task tasks.scrape_pending_urls[33d848b3-3360-4296-9ceb-0d2bcf917771] succeeded in 0.002382699982263148s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,172: INFO/MainProcess] Task tasks.scrape_pending_urls[4d321bd5-bc0e-46cd-9966-156ad929a93f] received
[2026-03-27 00:42:48,175: INFO/MainProcess] Task tasks.scrape_pending_urls[4d321bd5-bc0e-46cd-9966-156ad929a93f] succeeded in 0.0026866000844165683s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,177: INFO/MainProcess] Task tasks.scrape_pending_urls[2792c873-2825-4c0e-b908-c6f61c4fbd6d] received
[2026-03-27 00:42:48,180: INFO/MainProcess] Task tasks.scrape_pending_urls[2792c873-2825-4c0e-b908-c6f61c4fbd6d] succeeded in 0.0029086999129503965s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,182: INFO/MainProcess] Task tasks.scrape_pending_urls[d5e9c544-5b0f-4bb2-9d4d-103dee350b51] received
[2026-03-27 00:42:48,184: INFO/MainProcess] Task tasks.scrape_pending_urls[d5e9c544-5b0f-4bb2-9d4d-103dee350b51] succeeded in 0.0023551000049337745s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,187: INFO/MainProcess] Task tasks.scrape_pending_urls[93d9c19b-36bf-455c-9979-1d1c72c398d6] received
[2026-03-27 00:42:48,190: INFO/MainProcess] Task tasks.scrape_pending_urls[93d9c19b-36bf-455c-9979-1d1c72c398d6] succeeded in 0.0025658999802544713s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,191: INFO/MainProcess] Task tasks.scrape_pending_urls[b4be5750-d73b-489c-a03e-51fa0d826a01] received
[2026-03-27 00:42:48,194: INFO/MainProcess] Task tasks.scrape_pending_urls[b4be5750-d73b-489c-a03e-51fa0d826a01] succeeded in 0.0023331999545916915s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,195: INFO/MainProcess] Task tasks.scrape_pending_urls[22a7c138-eac6-4dcb-a935-f6a384ea3e3e] received
[2026-03-27 00:42:48,198: INFO/MainProcess] Task tasks.scrape_pending_urls[22a7c138-eac6-4dcb-a935-f6a384ea3e3e] succeeded in 0.002467899932526052s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,200: INFO/MainProcess] Task tasks.scrape_pending_urls[f6fe77af-543f-40d5-a7be-b23f1ec33aa9] received
[2026-03-27 00:42:48,204: INFO/MainProcess] Task tasks.scrape_pending_urls[f6fe77af-543f-40d5-a7be-b23f1ec33aa9] succeeded in 0.003903999924659729s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,206: INFO/MainProcess] Task tasks.scrape_pending_urls[5d722ac7-6f1e-4f09-bd46-1728a9a6a838] received
[2026-03-27 00:42:48,209: INFO/MainProcess] Task tasks.scrape_pending_urls[5d722ac7-6f1e-4f09-bd46-1728a9a6a838] succeeded in 0.0025248000165447593s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,210: INFO/MainProcess] Task tasks.scrape_pending_urls[b297ab49-91f3-45cf-a2fd-0e32f71dbe13] received
[2026-03-27 00:42:48,213: INFO/MainProcess] Task tasks.scrape_pending_urls[b297ab49-91f3-45cf-a2fd-0e32f71dbe13] succeeded in 0.00248030002694577s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,215: INFO/MainProcess] Task tasks.scrape_pending_urls[28b9970f-fc72-4832-8c0f-893a0b9e2db9] received
[2026-03-27 00:42:48,218: INFO/MainProcess] Task tasks.scrape_pending_urls[28b9970f-fc72-4832-8c0f-893a0b9e2db9] succeeded in 0.0028168000280857086s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,219: INFO/MainProcess] Task tasks.scrape_pending_urls[263df7c2-d616-4575-ae39-a3282da66f4e] received
[2026-03-27 00:42:48,223: INFO/MainProcess] Task tasks.scrape_pending_urls[263df7c2-d616-4575-ae39-a3282da66f4e] succeeded in 0.002993699978105724s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,225: INFO/MainProcess] Task tasks.scrape_pending_urls[e3364344-1d3c-4a03-b6ed-78c9ffc30718] received
[2026-03-27 00:42:48,228: INFO/MainProcess] Task tasks.scrape_pending_urls[e3364344-1d3c-4a03-b6ed-78c9ffc30718] succeeded in 0.002638199948705733s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,229: INFO/MainProcess] Task tasks.scrape_pending_urls[41ef66b7-b737-4387-a9db-20c1320c29a6] received
[2026-03-27 00:42:48,232: INFO/MainProcess] Task tasks.scrape_pending_urls[41ef66b7-b737-4387-a9db-20c1320c29a6] succeeded in 0.002468200051225722s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,234: INFO/MainProcess] Task tasks.scrape_pending_urls[e737633a-686f-4c6a-a83f-0ce6d8f32b8d] received
[2026-03-27 00:42:48,237: INFO/MainProcess] Task tasks.scrape_pending_urls[e737633a-686f-4c6a-a83f-0ce6d8f32b8d] succeeded in 0.0026061999378725886s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,239: INFO/MainProcess] Task tasks.scrape_pending_urls[3fd2e6cb-4815-4142-a8c1-ada0c0a3c1b7] received
[2026-03-27 00:42:48,242: INFO/MainProcess] Task tasks.scrape_pending_urls[3fd2e6cb-4815-4142-a8c1-ada0c0a3c1b7] succeeded in 0.0024958999129012227s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,243: INFO/MainProcess] Task tasks.scrape_pending_urls[9f33c764-6d70-491a-a0a5-9af498f3247e] received
[2026-03-27 00:42:48,246: INFO/MainProcess] Task tasks.scrape_pending_urls[9f33c764-6d70-491a-a0a5-9af498f3247e] succeeded in 0.002443999983370304s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,247: INFO/MainProcess] Task tasks.scrape_pending_urls[8b11e99e-d15e-4f8b-ba19-b5a1604d5279] received
[2026-03-27 00:42:48,252: INFO/MainProcess] Task tasks.scrape_pending_urls[8b11e99e-d15e-4f8b-ba19-b5a1604d5279] succeeded in 0.004256699932739139s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,254: INFO/MainProcess] Task tasks.scrape_pending_urls[de59b57e-e0a6-491d-9ef5-e69b0e6d82d2] received
[2026-03-27 00:42:48,257: INFO/MainProcess] Task tasks.scrape_pending_urls[de59b57e-e0a6-491d-9ef5-e69b0e6d82d2] succeeded in 0.0028120999922975898s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,258: INFO/MainProcess] Task tasks.scrape_pending_urls[e405dc9d-a277-4c83-b656-71ff497ba13e] received
[2026-03-27 00:42:48,261: INFO/MainProcess] Task tasks.scrape_pending_urls[e405dc9d-a277-4c83-b656-71ff497ba13e] succeeded in 0.0028204999398440123s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,263: INFO/MainProcess] Task tasks.scrape_pending_urls[2898eb6c-837e-4a24-8815-e222c49bd7e5] received
[2026-03-27 00:42:48,268: INFO/MainProcess] Task tasks.scrape_pending_urls[2898eb6c-837e-4a24-8815-e222c49bd7e5] succeeded in 0.004342200001701713s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,270: INFO/MainProcess] Task tasks.scrape_pending_urls[c0795215-7250-49cf-bf99-d4cddbca66dd] received
[2026-03-27 00:42:48,273: INFO/MainProcess] Task tasks.scrape_pending_urls[c0795215-7250-49cf-bf99-d4cddbca66dd] succeeded in 0.002980199991725385s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,275: INFO/MainProcess] Task tasks.scrape_pending_urls[5809b59e-f9d3-4654-925d-2879fb2afdb7] received
[2026-03-27 00:42:48,278: INFO/MainProcess] Task tasks.scrape_pending_urls[5809b59e-f9d3-4654-925d-2879fb2afdb7] succeeded in 0.0029848000267520547s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,280: INFO/MainProcess] Task tasks.scrape_pending_urls[8d7c57a2-fea7-44e2-bff0-2da5468c36cc] received
[2026-03-27 00:42:48,284: INFO/MainProcess] Task tasks.scrape_pending_urls[8d7c57a2-fea7-44e2-bff0-2da5468c36cc] succeeded in 0.003967700060456991s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,286: INFO/MainProcess] Task tasks.scrape_pending_urls[c0dbe6e5-04c5-46f3-abe4-18e13b2c7752] received
[2026-03-27 00:42:48,290: INFO/MainProcess] Task tasks.scrape_pending_urls[c0dbe6e5-04c5-46f3-abe4-18e13b2c7752] succeeded in 0.0036051999777555466s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,291: INFO/MainProcess] Task tasks.scrape_pending_urls[b7f0231e-2918-4994-884d-3736e430c287] received
[2026-03-27 00:42:48,295: INFO/MainProcess] Task tasks.scrape_pending_urls[b7f0231e-2918-4994-884d-3736e430c287] succeeded in 0.0031422999454662204s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,298: INFO/MainProcess] Task tasks.scrape_pending_urls[cf716dbf-443e-4499-9d71-be1ec1d1f0d0] received
[2026-03-27 00:42:48,303: INFO/MainProcess] Task tasks.scrape_pending_urls[cf716dbf-443e-4499-9d71-be1ec1d1f0d0] succeeded in 0.0036301000509411097s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,304: INFO/MainProcess] Task tasks.scrape_pending_urls[1a977c79-3acb-48e9-b554-0d28e785e0e7] received
[2026-03-27 00:42:48,308: INFO/MainProcess] Task tasks.scrape_pending_urls[1a977c79-3acb-48e9-b554-0d28e785e0e7] succeeded in 0.0029455000767484307s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,309: INFO/MainProcess] Task tasks.scrape_pending_urls[54a7e3df-ee4c-46a5-8338-df4756baccaf] received
[2026-03-27 00:42:48,313: INFO/MainProcess] Task tasks.scrape_pending_urls[54a7e3df-ee4c-46a5-8338-df4756baccaf] succeeded in 0.0030900000128895044s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,316: INFO/MainProcess] Task tasks.scrape_pending_urls[3899d277-c10a-4354-a32f-2aa5e3be19b5] received
[2026-03-27 00:42:48,319: INFO/MainProcess] Task tasks.scrape_pending_urls[3899d277-c10a-4354-a32f-2aa5e3be19b5] succeeded in 0.0035949000157415867s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,321: INFO/MainProcess] Task tasks.scrape_pending_urls[cb64b7fd-f81a-4d53-ae10-061c7c582db1] received
[2026-03-27 00:42:48,325: INFO/MainProcess] Task tasks.scrape_pending_urls[cb64b7fd-f81a-4d53-ae10-061c7c582db1] succeeded in 0.0030169999226927757s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,326: INFO/MainProcess] Task tasks.scrape_pending_urls[5c135a3d-fc60-4c93-bbe6-105b116beeea] received
[2026-03-27 00:42:48,330: INFO/MainProcess] Task tasks.scrape_pending_urls[5c135a3d-fc60-4c93-bbe6-105b116beeea] succeeded in 0.003496199962683022s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,332: INFO/MainProcess] Task tasks.scrape_pending_urls[dc967b8e-f55d-4a6b-bbd3-e4a644b51b54] received
[2026-03-27 00:42:48,334: INFO/MainProcess] Task tasks.scrape_pending_urls[dc967b8e-f55d-4a6b-bbd3-e4a644b51b54] succeeded in 0.002534199971705675s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,336: INFO/MainProcess] Task tasks.scrape_pending_urls[0f93a07c-53dd-4128-a097-4720f0035924] received
[2026-03-27 00:42:48,338: INFO/MainProcess] Task tasks.scrape_pending_urls[0f93a07c-53dd-4128-a097-4720f0035924] succeeded in 0.0023355999728664756s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,340: INFO/MainProcess] Task tasks.scrape_pending_urls[b36ea5de-7830-4940-abfd-51b86e6e53b9] received
[2026-03-27 00:42:48,342: INFO/MainProcess] Task tasks.scrape_pending_urls[b36ea5de-7830-4940-abfd-51b86e6e53b9] succeeded in 0.0023195999674499035s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,344: INFO/MainProcess] Task tasks.scrape_pending_urls[741c91a7-667a-4afa-a89c-0d4f6d8c1e9d] received
[2026-03-27 00:42:48,349: INFO/MainProcess] Task tasks.scrape_pending_urls[741c91a7-667a-4afa-a89c-0d4f6d8c1e9d] succeeded in 0.004774000030010939s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,350: INFO/MainProcess] Task tasks.scrape_pending_urls[96e2a334-c271-4dc4-a0bc-53a347d87764] received
[2026-03-27 00:42:48,353: INFO/MainProcess] Task tasks.scrape_pending_urls[96e2a334-c271-4dc4-a0bc-53a347d87764] succeeded in 0.0026679999427869916s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,355: INFO/MainProcess] Task tasks.scrape_pending_urls[917bd0e0-a414-46d8-9d7c-e2f5bd00a614] received
[2026-03-27 00:42:48,357: INFO/MainProcess] Task tasks.scrape_pending_urls[917bd0e0-a414-46d8-9d7c-e2f5bd00a614] succeeded in 0.00231890007853508s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,359: INFO/MainProcess] Task tasks.scrape_pending_urls[496ada86-1aba-4f4a-a5ed-f97b4a80ad66] received
[2026-03-27 00:42:48,362: INFO/MainProcess] Task tasks.scrape_pending_urls[496ada86-1aba-4f4a-a5ed-f97b4a80ad66] succeeded in 0.0035438999766483903s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,364: INFO/MainProcess] Task tasks.scrape_pending_urls[fee2025c-dbf7-44cc-ac78-80f63a311b9e] received
[2026-03-27 00:42:48,368: INFO/MainProcess] Task tasks.scrape_pending_urls[fee2025c-dbf7-44cc-ac78-80f63a311b9e] succeeded in 0.0033309999853372574s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,370: INFO/MainProcess] Task tasks.scrape_pending_urls[c9359c27-91af-47cf-a3fc-3dc2b0eca1c4] received
[2026-03-27 00:42:48,372: INFO/MainProcess] Task tasks.scrape_pending_urls[c9359c27-91af-47cf-a3fc-3dc2b0eca1c4] succeeded in 0.002435899921692908s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,374: INFO/MainProcess] Task tasks.scrape_pending_urls[0abefcd2-a0a0-4a47-b936-a387f3fc5f1a] received
[2026-03-27 00:42:48,377: INFO/MainProcess] Task tasks.scrape_pending_urls[0abefcd2-a0a0-4a47-b936-a387f3fc5f1a] succeeded in 0.002722000004723668s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,378: INFO/MainProcess] Task tasks.scrape_pending_urls[bd7b4fbe-59da-424c-93d2-d0a46007ef6c] received
[2026-03-27 00:42:48,381: INFO/MainProcess] Task tasks.scrape_pending_urls[bd7b4fbe-59da-424c-93d2-d0a46007ef6c] succeeded in 0.0024525999324396253s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,382: INFO/MainProcess] Task tasks.scrape_pending_urls[b05c9d4d-161f-400d-9e8f-bd73f55bbd92] received
[2026-03-27 00:42:48,385: INFO/MainProcess] Task tasks.scrape_pending_urls[b05c9d4d-161f-400d-9e8f-bd73f55bbd92] succeeded in 0.0023403000086545944s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,386: INFO/MainProcess] Task tasks.scrape_pending_urls[bb708775-b625-4fa5-a428-af2ca67c7893] received
[2026-03-27 00:42:48,389: INFO/MainProcess] Task tasks.scrape_pending_urls[bb708775-b625-4fa5-a428-af2ca67c7893] succeeded in 0.0022371000377461314s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,390: INFO/MainProcess] Task tasks.scrape_pending_urls[cf60b53f-81e4-4e6e-b703-e3486914f4f1] received
[2026-03-27 00:42:48,394: INFO/MainProcess] Task tasks.scrape_pending_urls[cf60b53f-81e4-4e6e-b703-e3486914f4f1] succeeded in 0.0031881999457255006s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,395: INFO/MainProcess] Task tasks.scrape_pending_urls[5f08afed-b098-4637-b3d4-878afacd724f] received
[2026-03-27 00:42:48,398: INFO/MainProcess] Task tasks.scrape_pending_urls[5f08afed-b098-4637-b3d4-878afacd724f] succeeded in 0.0024654000299051404s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,399: INFO/MainProcess] Task tasks.scrape_pending_urls[77398c93-59aa-4edb-b237-0cd54f854ba7] received
[2026-03-27 00:42:48,402: INFO/MainProcess] Task tasks.scrape_pending_urls[77398c93-59aa-4edb-b237-0cd54f854ba7] succeeded in 0.0023212999803945422s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,403: INFO/MainProcess] Task tasks.scrape_pending_urls[f3e9c202-67e5-4128-8f05-b7d47bcecaea] received
[2026-03-27 00:42:48,406: INFO/MainProcess] Task tasks.scrape_pending_urls[f3e9c202-67e5-4128-8f05-b7d47bcecaea] succeeded in 0.00274979998357594s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,408: INFO/MainProcess] Task tasks.scrape_pending_urls[49e309e0-22c7-4bd0-960f-2021e437ab95] received
[2026-03-27 00:42:48,412: INFO/MainProcess] Task tasks.scrape_pending_urls[49e309e0-22c7-4bd0-960f-2021e437ab95] succeeded in 0.0026456000050529838s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,413: INFO/MainProcess] Task tasks.scrape_pending_urls[f96e2118-92a6-4d61-bd2b-d6739485bbdf] received
[2026-03-27 00:42:48,416: INFO/MainProcess] Task tasks.scrape_pending_urls[f96e2118-92a6-4d61-bd2b-d6739485bbdf] succeeded in 0.002338099991902709s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,417: INFO/MainProcess] Task tasks.scrape_pending_urls[85a81333-7e31-42d8-a054-a83b492a4b6b] received
[2026-03-27 00:42:48,420: INFO/MainProcess] Task tasks.scrape_pending_urls[85a81333-7e31-42d8-a054-a83b492a4b6b] succeeded in 0.0022859000600874424s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,421: INFO/MainProcess] Task tasks.scrape_pending_urls[2968e12e-697e-4365-a9de-7e73883dfbc1] received
[2026-03-27 00:42:48,423: INFO/MainProcess] Task tasks.scrape_pending_urls[2968e12e-697e-4365-a9de-7e73883dfbc1] succeeded in 0.002311200019903481s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,426: INFO/MainProcess] Task tasks.scrape_pending_urls[bfcf130c-a527-419e-859a-b876168ae571] received
[2026-03-27 00:42:48,429: INFO/MainProcess] Task tasks.scrape_pending_urls[bfcf130c-a527-419e-859a-b876168ae571] succeeded in 0.002540100016631186s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,430: INFO/MainProcess] Task tasks.scrape_pending_urls[092eb3ee-9c7b-43b7-9e87-347de4900fd3] received
[2026-03-27 00:42:48,433: INFO/MainProcess] Task tasks.scrape_pending_urls[092eb3ee-9c7b-43b7-9e87-347de4900fd3] succeeded in 0.0023736999137327075s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,435: INFO/MainProcess] Task tasks.scrape_pending_urls[f42b9f1a-7f7d-4555-b0b9-da6927b26d58] received
[2026-03-27 00:42:48,437: INFO/MainProcess] Task tasks.scrape_pending_urls[f42b9f1a-7f7d-4555-b0b9-da6927b26d58] succeeded in 0.0024588999804109335s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,439: INFO/MainProcess] Task tasks.scrape_pending_urls[491d61c4-7203-4991-a065-6ebe63e0e48a] received
[2026-03-27 00:42:48,443: INFO/MainProcess] Task tasks.scrape_pending_urls[491d61c4-7203-4991-a065-6ebe63e0e48a] succeeded in 0.003859299933537841s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,445: INFO/MainProcess] Task tasks.scrape_pending_urls[b9adf842-1600-4fd4-8c36-ab57f5f5b56b] received
[2026-03-27 00:42:48,448: INFO/MainProcess] Task tasks.scrape_pending_urls[b9adf842-1600-4fd4-8c36-ab57f5f5b56b] succeeded in 0.0030756000196561217s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,450: INFO/MainProcess] Task tasks.scrape_pending_urls[8a11713b-a644-4ac2-96f2-687cfb18f78e] received
[2026-03-27 00:42:48,452: INFO/MainProcess] Task tasks.scrape_pending_urls[8a11713b-a644-4ac2-96f2-687cfb18f78e] succeeded in 0.0025345999747514725s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,454: INFO/MainProcess] Task tasks.scrape_pending_urls[28e7efb3-9a36-42ce-a042-259ecf8cb49f] received
[2026-03-27 00:42:48,458: INFO/MainProcess] Task tasks.scrape_pending_urls[28e7efb3-9a36-42ce-a042-259ecf8cb49f] succeeded in 0.003406000090762973s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,459: INFO/MainProcess] Task tasks.scrape_pending_urls[ee5a138f-1574-400f-8edf-22453310bba0] received
[2026-03-27 00:42:48,462: INFO/MainProcess] Task tasks.scrape_pending_urls[ee5a138f-1574-400f-8edf-22453310bba0] succeeded in 0.0024975999258458614s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,464: INFO/MainProcess] Task tasks.scrape_pending_urls[4bd7089e-e498-497a-bb0e-041a64fdca9a] received
[2026-03-27 00:42:48,466: INFO/MainProcess] Task tasks.scrape_pending_urls[4bd7089e-e498-497a-bb0e-041a64fdca9a] succeeded in 0.0024334999034181237s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,468: INFO/MainProcess] Task tasks.scrape_pending_urls[a4c10db4-3b00-4feb-9bad-aa3abb240815] received
[2026-03-27 00:42:48,471: INFO/MainProcess] Task tasks.scrape_pending_urls[a4c10db4-3b00-4feb-9bad-aa3abb240815] succeeded in 0.002455799956806004s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,474: INFO/MainProcess] Task tasks.scrape_pending_urls[13f4af07-a5f4-4585-95d6-77a16a13bfb9] received
[2026-03-27 00:42:48,477: INFO/MainProcess] Task tasks.scrape_pending_urls[13f4af07-a5f4-4585-95d6-77a16a13bfb9] succeeded in 0.0026285999920219183s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,479: INFO/MainProcess] Task tasks.scrape_pending_urls[d0b369b8-fce9-487f-888e-10720bb82633] received
[2026-03-27 00:42:48,481: INFO/MainProcess] Task tasks.scrape_pending_urls[d0b369b8-fce9-487f-888e-10720bb82633] succeeded in 0.0023695999989286065s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,483: INFO/MainProcess] Task tasks.scrape_pending_urls[13e1ba1b-8f49-4c3e-81aa-b01692b02fc3] received
[2026-03-27 00:42:48,486: INFO/MainProcess] Task tasks.scrape_pending_urls[13e1ba1b-8f49-4c3e-81aa-b01692b02fc3] succeeded in 0.0024287999840453267s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,487: INFO/MainProcess] Task tasks.scrape_pending_urls[80639905-9448-417b-8de0-b9c3906fdb13] received
[2026-03-27 00:42:48,491: INFO/MainProcess] Task tasks.scrape_pending_urls[80639905-9448-417b-8de0-b9c3906fdb13] succeeded in 0.0030052000656723976s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,493: INFO/MainProcess] Task tasks.scrape_pending_urls[c4cfdb86-7f42-49ee-83e9-67399f23740d] received
[2026-03-27 00:42:48,496: INFO/MainProcess] Task tasks.scrape_pending_urls[c4cfdb86-7f42-49ee-83e9-67399f23740d] succeeded in 0.002889299998059869s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,498: INFO/MainProcess] Task tasks.scrape_pending_urls[f41fe3ce-f138-40ff-9841-6c334eaa5246] received
[2026-03-27 00:42:48,501: INFO/MainProcess] Task tasks.scrape_pending_urls[f41fe3ce-f138-40ff-9841-6c334eaa5246] succeeded in 0.0024712999584153295s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,502: INFO/MainProcess] Task tasks.scrape_pending_urls[f8a8563b-029a-4a40-b025-a22760f46ff3] received
[2026-03-27 00:42:48,506: INFO/MainProcess] Task tasks.scrape_pending_urls[f8a8563b-029a-4a40-b025-a22760f46ff3] succeeded in 0.003554699942469597s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,508: INFO/MainProcess] Task tasks.scrape_pending_urls[00f08bff-8738-439f-a721-1a9e8d01dcb6] received
[2026-03-27 00:42:48,511: INFO/MainProcess] Task tasks.scrape_pending_urls[00f08bff-8738-439f-a721-1a9e8d01dcb6] succeeded in 0.0025438000448048115s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,512: INFO/MainProcess] Task tasks.scrape_pending_urls[651cb104-1abb-497d-b619-4e448c5b49aa] received
[2026-03-27 00:42:48,515: INFO/MainProcess] Task tasks.scrape_pending_urls[651cb104-1abb-497d-b619-4e448c5b49aa] succeeded in 0.00252470001578331s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,516: INFO/MainProcess] Task tasks.scrape_pending_urls[c4da976f-9f92-4320-b680-82a5fdac584a] received
[2026-03-27 00:42:48,519: INFO/MainProcess] Task tasks.scrape_pending_urls[c4da976f-9f92-4320-b680-82a5fdac584a] succeeded in 0.002807699958793819s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,522: INFO/MainProcess] Task tasks.scrape_pending_urls[7e31e5ca-5754-4f23-8970-4bcf28fff5e4] received
[2026-03-27 00:42:48,525: INFO/MainProcess] Task tasks.scrape_pending_urls[7e31e5ca-5754-4f23-8970-4bcf28fff5e4] succeeded in 0.0026424999814480543s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,527: INFO/MainProcess] Task tasks.scrape_pending_urls[88bb5c73-bb10-43d7-b8c3-5b9b5933d54c] received
[2026-03-27 00:42:48,529: INFO/MainProcess] Task tasks.scrape_pending_urls[88bb5c73-bb10-43d7-b8c3-5b9b5933d54c] succeeded in 0.002433300018310547s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,531: INFO/MainProcess] Task tasks.scrape_pending_urls[3c55ede8-cad1-4a91-9632-bc00fe03fe97] received
[2026-03-27 00:42:48,534: INFO/MainProcess] Task tasks.scrape_pending_urls[3c55ede8-cad1-4a91-9632-bc00fe03fe97] succeeded in 0.0024570999667048454s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,536: INFO/MainProcess] Task tasks.scrape_pending_urls[4189088c-d4d3-482b-b5fd-321788a76149] received
[2026-03-27 00:42:48,539: INFO/MainProcess] Task tasks.scrape_pending_urls[4189088c-d4d3-482b-b5fd-321788a76149] succeeded in 0.0033765999833121896s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,541: INFO/MainProcess] Task tasks.scrape_pending_urls[0e97295c-bbde-405d-bd74-b4b33fab5f39] received
[2026-03-27 00:42:48,544: INFO/MainProcess] Task tasks.scrape_pending_urls[0e97295c-bbde-405d-bd74-b4b33fab5f39] succeeded in 0.0024673999287188053s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,545: INFO/MainProcess] Task tasks.scrape_pending_urls[d2e1d1ce-bcad-47ae-b4b6-055ace4bd47b] received
[2026-03-27 00:42:48,548: INFO/MainProcess] Task tasks.scrape_pending_urls[d2e1d1ce-bcad-47ae-b4b6-055ace4bd47b] succeeded in 0.0024933000095188618s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,550: INFO/MainProcess] Task tasks.scrape_pending_urls[dcfbccb6-ad75-4e17-82c5-ae4968f77777] received
[2026-03-27 00:42:48,553: INFO/MainProcess] Task tasks.scrape_pending_urls[dcfbccb6-ad75-4e17-82c5-ae4968f77777] succeeded in 0.0031317000975832343s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,555: INFO/MainProcess] Task tasks.scrape_pending_urls[93d9df65-af9a-4bd5-ac98-c8ea095c6724] received
[2026-03-27 00:42:48,558: INFO/MainProcess] Task tasks.scrape_pending_urls[93d9df65-af9a-4bd5-ac98-c8ea095c6724] succeeded in 0.002534099970944226s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,559: INFO/MainProcess] Task tasks.scrape_pending_urls[ee4ddacf-3564-47e8-9ab8-ea1dafb33281] received
[2026-03-27 00:42:48,562: INFO/MainProcess] Task tasks.scrape_pending_urls[ee4ddacf-3564-47e8-9ab8-ea1dafb33281] succeeded in 0.002484500058926642s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,564: INFO/MainProcess] Task tasks.scrape_pending_urls[52e58791-d7b1-42ff-892e-f34dcbd59f08] received
[2026-03-27 00:42:48,567: INFO/MainProcess] Task tasks.scrape_pending_urls[52e58791-d7b1-42ff-892e-f34dcbd59f08] succeeded in 0.0026050000451505184s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,569: INFO/MainProcess] Task tasks.scrape_pending_urls[1dbc133e-ae91-47be-b5de-0ed2f0c4fc29] received
[2026-03-27 00:42:48,571: INFO/MainProcess] Task tasks.scrape_pending_urls[1dbc133e-ae91-47be-b5de-0ed2f0c4fc29] succeeded in 0.002633600030094385s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,573: INFO/MainProcess] Task tasks.scrape_pending_urls[66413632-2a09-44fa-8914-7b545bae30a7] received
[2026-03-27 00:42:48,576: INFO/MainProcess] Task tasks.scrape_pending_urls[66413632-2a09-44fa-8914-7b545bae30a7] succeeded in 0.00244609999936074s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,577: INFO/MainProcess] Task tasks.scrape_pending_urls[7dcf7a35-f7f4-4a0c-bb1b-a5c376e84a54] received
[2026-03-27 00:42:48,580: INFO/MainProcess] Task tasks.scrape_pending_urls[7dcf7a35-f7f4-4a0c-bb1b-a5c376e84a54] succeeded in 0.0026453000027686357s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,582: INFO/MainProcess] Task tasks.scrape_pending_urls[36107654-f62a-48ac-bfac-02856d7d0582] received
[2026-03-27 00:42:48,587: INFO/MainProcess] Task tasks.scrape_pending_urls[36107654-f62a-48ac-bfac-02856d7d0582] succeeded in 0.0030691000865772367s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,588: INFO/MainProcess] Task tasks.scrape_pending_urls[f7507533-30bf-434e-bbc7-727dc5f3061f] received
[2026-03-27 00:42:48,591: INFO/MainProcess] Task tasks.scrape_pending_urls[f7507533-30bf-434e-bbc7-727dc5f3061f] succeeded in 0.0025334999663755298s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,593: INFO/MainProcess] Task tasks.scrape_pending_urls[34104c5d-5e85-4c25-ae47-c12255cfea1e] received
[2026-03-27 00:42:48,596: INFO/MainProcess] Task tasks.scrape_pending_urls[34104c5d-5e85-4c25-ae47-c12255cfea1e] succeeded in 0.0024763999972492456s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,597: INFO/MainProcess] Task tasks.scrape_pending_urls[ac3c1e36-51a7-405c-86c7-4d865f8bd52f] received
[2026-03-27 00:42:48,601: INFO/MainProcess] Task tasks.scrape_pending_urls[ac3c1e36-51a7-405c-86c7-4d865f8bd52f] succeeded in 0.0035914999898523092s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,603: INFO/MainProcess] Task tasks.scrape_pending_urls[a46a49f5-f5d9-413e-8932-7d9e636013b2] received
[2026-03-27 00:42:48,606: INFO/MainProcess] Task tasks.scrape_pending_urls[a46a49f5-f5d9-413e-8932-7d9e636013b2] succeeded in 0.0026201000437140465s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,607: INFO/MainProcess] Task tasks.scrape_pending_urls[37a65c86-ed1a-4a56-b867-414faf8271e5] received
[2026-03-27 00:42:48,610: INFO/MainProcess] Task tasks.scrape_pending_urls[37a65c86-ed1a-4a56-b867-414faf8271e5] succeeded in 0.002421799930743873s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,612: INFO/MainProcess] Task tasks.scrape_pending_urls[2d729b06-1332-4486-8575-9cc56eabb5ca] received
[2026-03-27 00:42:48,615: INFO/MainProcess] Task tasks.scrape_pending_urls[2d729b06-1332-4486-8575-9cc56eabb5ca] succeeded in 0.0031805000035092235s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,618: INFO/MainProcess] Task tasks.scrape_pending_urls[dae05b36-fd9e-4d99-87b4-1a4ee75458e4] received
[2026-03-27 00:42:48,621: INFO/MainProcess] Task tasks.scrape_pending_urls[dae05b36-fd9e-4d99-87b4-1a4ee75458e4] succeeded in 0.00341970007866621s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,623: INFO/MainProcess] Task tasks.scrape_pending_urls[79b647bf-1ba9-4604-bb5c-a1c33385e3cb] received
[2026-03-27 00:42:48,626: INFO/MainProcess] Task tasks.scrape_pending_urls[79b647bf-1ba9-4604-bb5c-a1c33385e3cb] succeeded in 0.0027103000320494175s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,628: INFO/MainProcess] Task tasks.scrape_pending_urls[6ba30e34-05a6-4a4d-ac0c-15ab914736b6] received
[2026-03-27 00:42:48,631: INFO/MainProcess] Task tasks.scrape_pending_urls[6ba30e34-05a6-4a4d-ac0c-15ab914736b6] succeeded in 0.0027885999297723174s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,633: INFO/MainProcess] Task tasks.scrape_pending_urls[8158864c-2a56-43cc-a713-88bff01b93cb] received
[2026-03-27 00:42:48,636: INFO/MainProcess] Task tasks.scrape_pending_urls[8158864c-2a56-43cc-a713-88bff01b93cb] succeeded in 0.0026357000460848212s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,638: INFO/MainProcess] Task tasks.scrape_pending_urls[1157692d-bb2c-41f2-b584-cfede5203dd4] received
[2026-03-27 00:42:48,640: INFO/MainProcess] Task tasks.scrape_pending_urls[1157692d-bb2c-41f2-b584-cfede5203dd4] succeeded in 0.002365300082601607s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,642: INFO/MainProcess] Task tasks.scrape_pending_urls[ac52db2b-729c-4395-8270-6ea799f0fe1b] received
[2026-03-27 00:42:48,645: INFO/MainProcess] Task tasks.scrape_pending_urls[ac52db2b-729c-4395-8270-6ea799f0fe1b] succeeded in 0.0024473000084981322s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,646: INFO/MainProcess] Task tasks.scrape_pending_urls[af250da6-dae6-4d3d-a2f9-b1d61772c701] received
[2026-03-27 00:42:48,651: INFO/MainProcess] Task tasks.scrape_pending_urls[af250da6-dae6-4d3d-a2f9-b1d61772c701] succeeded in 0.0043363000731915236s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,652: INFO/MainProcess] Task tasks.scrape_pending_urls[b9d2bcd2-e75a-4da3-b693-d1713861d6be] received
[2026-03-27 00:42:48,655: INFO/MainProcess] Task tasks.scrape_pending_urls[b9d2bcd2-e75a-4da3-b693-d1713861d6be] succeeded in 0.0024970999220386147s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,657: INFO/MainProcess] Task tasks.scrape_pending_urls[44d206bc-57c2-421e-a80f-7c0fe1c145bf] received
[2026-03-27 00:42:48,660: INFO/MainProcess] Task tasks.scrape_pending_urls[44d206bc-57c2-421e-a80f-7c0fe1c145bf] succeeded in 0.0024881999706849456s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,661: INFO/MainProcess] Task tasks.scrape_pending_urls[96bb21d2-547a-4932-bf3e-7882eba364da] received
[2026-03-27 00:42:48,665: INFO/MainProcess] Task tasks.scrape_pending_urls[96bb21d2-547a-4932-bf3e-7882eba364da] succeeded in 0.0036005000583827496s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,667: INFO/MainProcess] Task tasks.scrape_pending_urls[f86a2c0d-5a02-4b23-97cb-26570b0ae926] received
[2026-03-27 00:42:48,670: INFO/MainProcess] Task tasks.scrape_pending_urls[f86a2c0d-5a02-4b23-97cb-26570b0ae926] succeeded in 0.0027924999594688416s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,672: INFO/MainProcess] Task tasks.scrape_pending_urls[7014673b-c25c-4a37-a762-34e66e99a56b] received
[2026-03-27 00:42:48,674: INFO/MainProcess] Task tasks.scrape_pending_urls[7014673b-c25c-4a37-a762-34e66e99a56b] succeeded in 0.0025178000796586275s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,676: INFO/MainProcess] Task tasks.scrape_pending_urls[c33ebb94-b727-44bb-9829-989532e1f6d6] received
[2026-03-27 00:42:48,680: INFO/MainProcess] Task tasks.scrape_pending_urls[c33ebb94-b727-44bb-9829-989532e1f6d6] succeeded in 0.00328770000487566s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,681: INFO/MainProcess] Task tasks.scrape_pending_urls[5cea0a05-3421-4038-864b-384cb0978eba] received
[2026-03-27 00:42:48,684: INFO/MainProcess] Task tasks.scrape_pending_urls[5cea0a05-3421-4038-864b-384cb0978eba] succeeded in 0.002634200034663081s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,686: INFO/MainProcess] Task tasks.scrape_pending_urls[e1197797-6e5a-441a-8131-cc8f7fc7e49b] received
[2026-03-27 00:42:48,688: INFO/MainProcess] Task tasks.scrape_pending_urls[e1197797-6e5a-441a-8131-cc8f7fc7e49b] succeeded in 0.00251440005376935s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,690: INFO/MainProcess] Task tasks.scrape_pending_urls[725aea87-597b-4410-8109-ab09ade7a90d] received
[2026-03-27 00:42:48,693: INFO/MainProcess] Task tasks.scrape_pending_urls[725aea87-597b-4410-8109-ab09ade7a90d] succeeded in 0.0024843999417498708s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,695: INFO/MainProcess] Task tasks.scrape_pending_urls[97de1bf2-8c0f-4487-8ed8-fab3aaaa814c] received
[2026-03-27 00:42:48,699: INFO/MainProcess] Task tasks.scrape_pending_urls[97de1bf2-8c0f-4487-8ed8-fab3aaaa814c] succeeded in 0.0030999999726191163s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,700: INFO/MainProcess] Task tasks.scrape_pending_urls[e8d202d5-215d-4f6b-aab6-bbbe5fe9ba8b] received
[2026-03-27 00:42:48,703: INFO/MainProcess] Task tasks.scrape_pending_urls[e8d202d5-215d-4f6b-aab6-bbbe5fe9ba8b] succeeded in 0.002485099947080016s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,705: INFO/MainProcess] Task tasks.scrape_pending_urls[edd867d6-8b3c-4354-af74-c2af02d28ff1] received
[2026-03-27 00:42:48,708: INFO/MainProcess] Task tasks.scrape_pending_urls[edd867d6-8b3c-4354-af74-c2af02d28ff1] succeeded in 0.002557900035753846s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,709: INFO/MainProcess] Task tasks.scrape_pending_urls[55f470af-04bd-43e2-895a-af46cfaae6c4] received
[2026-03-27 00:42:48,714: INFO/MainProcess] Task tasks.scrape_pending_urls[55f470af-04bd-43e2-895a-af46cfaae6c4] succeeded in 0.004072299925610423s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,715: INFO/MainProcess] Task tasks.scrape_pending_urls[0a4b9456-be65-4574-bc48-789915bc8938] received
[2026-03-27 00:42:48,718: INFO/MainProcess] Task tasks.scrape_pending_urls[0a4b9456-be65-4574-bc48-789915bc8938] succeeded in 0.0026092000771313906s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,720: INFO/MainProcess] Task tasks.scrape_pending_urls[2cc28615-3236-4ac2-9bef-c4d413d36720] received
[2026-03-27 00:42:48,723: INFO/MainProcess] Task tasks.scrape_pending_urls[2cc28615-3236-4ac2-9bef-c4d413d36720] succeeded in 0.0025180999655276537s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,724: INFO/MainProcess] Task tasks.scrape_pending_urls[79a67cd7-f477-4d5e-a39a-61a9358a5ff5] received
[2026-03-27 00:42:48,728: INFO/MainProcess] Task tasks.scrape_pending_urls[79a67cd7-f477-4d5e-a39a-61a9358a5ff5] succeeded in 0.0036090000066906214s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,730: INFO/MainProcess] Task tasks.scrape_pending_urls[00901703-cd5c-4133-b68c-b1fb29d60075] received
[2026-03-27 00:42:48,733: INFO/MainProcess] Task tasks.scrape_pending_urls[00901703-cd5c-4133-b68c-b1fb29d60075] succeeded in 0.0026446999981999397s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,734: INFO/MainProcess] Task tasks.scrape_pending_urls[5843634e-05b8-4794-817e-63135bebe51c] received
[2026-03-27 00:42:48,737: INFO/MainProcess] Task tasks.scrape_pending_urls[5843634e-05b8-4794-817e-63135bebe51c] succeeded in 0.002531000063754618s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,739: INFO/MainProcess] Task tasks.scrape_pending_urls[caa95758-387d-4795-b5b3-146dbf783fa1] received
[2026-03-27 00:42:48,742: INFO/MainProcess] Task tasks.scrape_pending_urls[caa95758-387d-4795-b5b3-146dbf783fa1] succeeded in 0.002656599972397089s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,745: INFO/MainProcess] Task tasks.scrape_pending_urls[709c780a-4ee6-4fbc-be66-aa24a0374424] received
[2026-03-27 00:42:48,748: INFO/MainProcess] Task tasks.scrape_pending_urls[709c780a-4ee6-4fbc-be66-aa24a0374424] succeeded in 0.003146299975924194s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,750: INFO/MainProcess] Task tasks.scrape_pending_urls[608336c8-41ab-43ba-8d07-a10847fa0c05] received
[2026-03-27 00:42:48,753: INFO/MainProcess] Task tasks.scrape_pending_urls[608336c8-41ab-43ba-8d07-a10847fa0c05] succeeded in 0.0024926000041887164s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,754: INFO/MainProcess] Task tasks.scrape_pending_urls[60dd7146-587a-40e9-9384-c3cd4a518606] received
[2026-03-27 00:42:48,757: INFO/MainProcess] Task tasks.scrape_pending_urls[60dd7146-587a-40e9-9384-c3cd4a518606] succeeded in 0.0025166000705212355s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,759: INFO/MainProcess] Task tasks.scrape_pending_urls[0a2ab476-f845-4819-a8ca-b9d613de2354] received
[2026-03-27 00:42:48,762: INFO/MainProcess] Task tasks.scrape_pending_urls[0a2ab476-f845-4819-a8ca-b9d613de2354] succeeded in 0.002669100067578256s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,764: INFO/MainProcess] Task tasks.scrape_pending_urls[890baa8d-fa98-4c6c-b22f-f1a6bfa6a95a] received
[2026-03-27 00:42:48,766: INFO/MainProcess] Task tasks.scrape_pending_urls[890baa8d-fa98-4c6c-b22f-f1a6bfa6a95a] succeeded in 0.0024979000445455313s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,768: INFO/MainProcess] Task tasks.scrape_pending_urls[492213ed-394d-4589-8ee9-8e8b697b77ec] received
[2026-03-27 00:42:48,770: INFO/MainProcess] Task tasks.scrape_pending_urls[492213ed-394d-4589-8ee9-8e8b697b77ec] succeeded in 0.0025177999632433057s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,772: INFO/MainProcess] Task tasks.scrape_pending_urls[0a40a5bf-d911-460c-b714-ace740442c52] received
[2026-03-27 00:42:48,776: INFO/MainProcess] Task tasks.scrape_pending_urls[0a40a5bf-d911-460c-b714-ace740442c52] succeeded in 0.003994300030171871s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,778: INFO/MainProcess] Task tasks.scrape_pending_urls[aa5a80cf-4c68-4494-9648-ed608a6022c8] received
[2026-03-27 00:42:48,781: INFO/MainProcess] Task tasks.scrape_pending_urls[aa5a80cf-4c68-4494-9648-ed608a6022c8] succeeded in 0.002548599964939058s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,782: INFO/MainProcess] Task tasks.scrape_pending_urls[19b68578-ce03-43b9-bcd9-3c1d5057001d] received
[2026-03-27 00:42:48,785: INFO/MainProcess] Task tasks.scrape_pending_urls[19b68578-ce03-43b9-bcd9-3c1d5057001d] succeeded in 0.002402900019660592s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,786: INFO/MainProcess] Task tasks.scrape_pending_urls[988d985d-c85a-4c8a-8055-72d9e6cf9cb2] received
[2026-03-27 00:42:48,789: INFO/MainProcess] Task tasks.scrape_pending_urls[988d985d-c85a-4c8a-8055-72d9e6cf9cb2] succeeded in 0.0025148000568151474s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,792: INFO/MainProcess] Task tasks.scrape_pending_urls[580af579-e25e-4c4c-a2b9-036e64220907] received
[2026-03-27 00:42:48,795: INFO/MainProcess] Task tasks.scrape_pending_urls[580af579-e25e-4c4c-a2b9-036e64220907] succeeded in 0.002953300019726157s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,797: INFO/MainProcess] Task tasks.scrape_pending_urls[b3d9e888-50db-4393-a56a-7590fe0fdbd6] received
[2026-03-27 00:42:48,800: INFO/MainProcess] Task tasks.scrape_pending_urls[b3d9e888-50db-4393-a56a-7590fe0fdbd6] succeeded in 0.002536600106395781s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,801: INFO/MainProcess] Task tasks.scrape_pending_urls[2bf8f399-6766-4518-a726-ceaac1cebbcc] received
[2026-03-27 00:42:48,804: INFO/MainProcess] Task tasks.scrape_pending_urls[2bf8f399-6766-4518-a726-ceaac1cebbcc] succeeded in 0.0024727999698370695s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,806: INFO/MainProcess] Task tasks.scrape_pending_urls[ddb49c98-0893-48ed-82a0-21dd655bed92] received
[2026-03-27 00:42:48,809: INFO/MainProcess] Task tasks.scrape_pending_urls[ddb49c98-0893-48ed-82a0-21dd655bed92] succeeded in 0.0026410999707877636s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,810: INFO/MainProcess] Task tasks.scrape_pending_urls[ce0ce464-9568-4c2d-b996-c05f44c4b98c] received
[2026-03-27 00:42:48,813: INFO/MainProcess] Task tasks.scrape_pending_urls[ce0ce464-9568-4c2d-b996-c05f44c4b98c] succeeded in 0.0024976000422611833s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,814: INFO/MainProcess] Task tasks.scrape_pending_urls[b148763b-cf32-45e2-9660-6afd0048bc88] received
[2026-03-27 00:42:48,817: INFO/MainProcess] Task tasks.scrape_pending_urls[b148763b-cf32-45e2-9660-6afd0048bc88] succeeded in 0.002444899990223348s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,819: INFO/MainProcess] Task tasks.scrape_pending_urls[5e27c7c4-5f27-46d9-8276-ce5757c1661d] received
[2026-03-27 00:42:48,822: INFO/MainProcess] Task tasks.scrape_pending_urls[5e27c7c4-5f27-46d9-8276-ce5757c1661d] succeeded in 0.003558299969881773s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,824: INFO/MainProcess] Task tasks.scrape_pending_urls[5efbb90c-621a-4bca-aa0d-bd27c75b1aa0] received
[2026-03-27 00:42:48,827: INFO/MainProcess] Task tasks.scrape_pending_urls[5efbb90c-621a-4bca-aa0d-bd27c75b1aa0] succeeded in 0.0025059999898076057s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,828: INFO/MainProcess] Task tasks.scrape_pending_urls[5af28a5f-0364-46b3-9169-89b4a41e391f] received
[2026-03-27 00:42:48,831: INFO/MainProcess] Task tasks.scrape_pending_urls[5af28a5f-0364-46b3-9169-89b4a41e391f] succeeded in 0.0023387999972328544s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,832: INFO/MainProcess] Task tasks.scrape_pending_urls[688a1a6f-d9a1-4eec-9cf5-4448aabca563] received
[2026-03-27 00:42:48,835: INFO/MainProcess] Task tasks.scrape_pending_urls[688a1a6f-d9a1-4eec-9cf5-4448aabca563] succeeded in 0.002898499951697886s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,837: INFO/MainProcess] Task tasks.scrape_pending_urls[59a7c057-78ae-4919-824f-ee929ef44188] received
[2026-03-27 00:42:48,840: INFO/MainProcess] Task tasks.scrape_pending_urls[59a7c057-78ae-4919-824f-ee929ef44188] succeeded in 0.002493400010280311s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,842: INFO/MainProcess] Task tasks.scrape_pending_urls[cf6d655c-c5b5-4024-921f-227290740b2a] received
[2026-03-27 00:42:48,844: INFO/MainProcess] Task tasks.scrape_pending_urls[cf6d655c-c5b5-4024-921f-227290740b2a] succeeded in 0.0023331999545916915s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,846: INFO/MainProcess] Task tasks.scrape_pending_urls[9e8a1123-3c3d-4f7f-9b2e-960d2236e13e] received
[2026-03-27 00:42:48,848: INFO/MainProcess] Task tasks.scrape_pending_urls[9e8a1123-3c3d-4f7f-9b2e-960d2236e13e] succeeded in 0.002355300006456673s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,850: INFO/MainProcess] Task tasks.scrape_pending_urls[d262ff0a-0c67-455d-95f5-2b18ca6c2bb6] received
[2026-03-27 00:42:48,853: INFO/MainProcess] Task tasks.scrape_pending_urls[d262ff0a-0c67-455d-95f5-2b18ca6c2bb6] succeeded in 0.0030553999822586775s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,855: INFO/MainProcess] Task tasks.scrape_pending_urls[253248f7-1b97-444f-acc3-486531395958] received
[2026-03-27 00:42:48,858: INFO/MainProcess] Task tasks.scrape_pending_urls[253248f7-1b97-444f-acc3-486531395958] succeeded in 0.002299700048752129s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,859: INFO/MainProcess] Task tasks.scrape_pending_urls[a1630254-938c-4b2f-b0c2-58d88950abb2] received
[2026-03-27 00:42:48,862: INFO/MainProcess] Task tasks.scrape_pending_urls[a1630254-938c-4b2f-b0c2-58d88950abb2] succeeded in 0.002161900047212839s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,863: INFO/MainProcess] Task tasks.scrape_pending_urls[2afa0f62-a303-4053-bf79-a67dadd87686] received
[2026-03-27 00:42:48,865: INFO/MainProcess] Task tasks.scrape_pending_urls[2afa0f62-a303-4053-bf79-a67dadd87686] succeeded in 0.002135300077497959s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,867: INFO/MainProcess] Task tasks.scrape_pending_urls[e8d7bcb0-7a03-43b1-a46a-a933c9f6b873] received
[2026-03-27 00:42:48,870: INFO/MainProcess] Task tasks.scrape_pending_urls[e8d7bcb0-7a03-43b1-a46a-a933c9f6b873] succeeded in 0.003397700027562678s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,872: INFO/MainProcess] Task tasks.scrape_pending_urls[f0117410-638c-440f-9f06-f348ee02798e] received
[2026-03-27 00:42:48,876: INFO/MainProcess] Task tasks.scrape_pending_urls[f0117410-638c-440f-9f06-f348ee02798e] succeeded in 0.003732999903149903s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,878: INFO/MainProcess] Task tasks.scrape_pending_urls[255c08bf-381a-40d3-8686-240b9a865a72] received
[2026-03-27 00:42:48,881: INFO/MainProcess] Task tasks.scrape_pending_urls[255c08bf-381a-40d3-8686-240b9a865a72] succeeded in 0.0024386000586673617s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,882: INFO/MainProcess] Task tasks.scrape_pending_urls[35cf62ba-9c44-4319-a4d7-80e00a271563] received
[2026-03-27 00:42:48,886: INFO/MainProcess] Task tasks.scrape_pending_urls[35cf62ba-9c44-4319-a4d7-80e00a271563] succeeded in 0.003569799941033125s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,887: INFO/MainProcess] Task tasks.scrape_pending_urls[87eedebb-10ac-48dd-b3dc-4bdd6fbc02b9] received
[2026-03-27 00:42:48,890: INFO/MainProcess] Task tasks.scrape_pending_urls[87eedebb-10ac-48dd-b3dc-4bdd6fbc02b9] succeeded in 0.0024778000079095364s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,892: INFO/MainProcess] Task tasks.scrape_pending_urls[40d7a008-3787-4927-a5f8-acc8b4f0a87c] received
[2026-03-27 00:42:48,894: INFO/MainProcess] Task tasks.scrape_pending_urls[40d7a008-3787-4927-a5f8-acc8b4f0a87c] succeeded in 0.002291699987836182s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,896: INFO/MainProcess] Task tasks.scrape_pending_urls[4cf568e8-0924-4df3-81af-cf23431204c2] received
[2026-03-27 00:42:48,898: INFO/MainProcess] Task tasks.scrape_pending_urls[4cf568e8-0924-4df3-81af-cf23431204c2] succeeded in 0.002305599977262318s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,900: INFO/MainProcess] Task tasks.scrape_pending_urls[bb30ddfd-8928-4820-9624-83674272054a] received
[2026-03-27 00:42:48,903: INFO/MainProcess] Task tasks.scrape_pending_urls[bb30ddfd-8928-4820-9624-83674272054a] succeeded in 0.0026805000379681587s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,905: INFO/MainProcess] Task tasks.scrape_pending_urls[0b192f29-da55-4ce2-8640-583760243f48] received
[2026-03-27 00:42:48,908: INFO/MainProcess] Task tasks.scrape_pending_urls[0b192f29-da55-4ce2-8640-583760243f48] succeeded in 0.0025536000030115247s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,909: INFO/MainProcess] Task tasks.scrape_pending_urls[2072c74c-9f3c-4161-b30f-b70b5eef0709] received
[2026-03-27 00:42:48,912: INFO/MainProcess] Task tasks.scrape_pending_urls[2072c74c-9f3c-4161-b30f-b70b5eef0709] succeeded in 0.0024440999841317534s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,914: INFO/MainProcess] Task tasks.scrape_pending_urls[86b14d14-298e-437e-8630-ed7973849cd2] received
[2026-03-27 00:42:48,918: INFO/MainProcess] Task tasks.scrape_pending_urls[86b14d14-298e-437e-8630-ed7973849cd2] succeeded in 0.003724799957126379s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,919: INFO/MainProcess] Task tasks.scrape_pending_urls[26794990-7daf-4dba-afaa-144d0d489fa4] received
[2026-03-27 00:42:48,923: INFO/MainProcess] Task tasks.scrape_pending_urls[26794990-7daf-4dba-afaa-144d0d489fa4] succeeded in 0.0027942999731749296s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,924: INFO/MainProcess] Task tasks.scrape_pending_urls[65438799-b4b0-422f-82e8-99d3960464cc] received
[2026-03-27 00:42:48,928: INFO/MainProcess] Task tasks.scrape_pending_urls[65438799-b4b0-422f-82e8-99d3960464cc] succeeded in 0.0028851000824943185s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,929: INFO/MainProcess] Task tasks.scrape_pending_urls[1f5dd09d-e5df-41a8-ad91-0a469f1c68a7] received
[2026-03-27 00:42:48,933: INFO/MainProcess] Task tasks.scrape_pending_urls[1f5dd09d-e5df-41a8-ad91-0a469f1c68a7] succeeded in 0.0034457999281585217s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,934: INFO/MainProcess] Task tasks.scrape_pending_urls[c0746b34-eb69-4a16-9652-7326dedd4fb2] received
[2026-03-27 00:42:48,937: INFO/MainProcess] Task tasks.scrape_pending_urls[c0746b34-eb69-4a16-9652-7326dedd4fb2] succeeded in 0.002600400010123849s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,939: INFO/MainProcess] Task tasks.scrape_pending_urls[189ebe10-a84b-411c-8146-45deecf7e444] received
[2026-03-27 00:42:48,942: INFO/MainProcess] Task tasks.scrape_pending_urls[189ebe10-a84b-411c-8146-45deecf7e444] succeeded in 0.002528300043195486s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,943: INFO/MainProcess] Task tasks.scrape_pending_urls[8da91e13-c48d-4075-b053-63eb075eb6af] received
[2026-03-27 00:42:48,946: INFO/MainProcess] Task tasks.scrape_pending_urls[8da91e13-c48d-4075-b053-63eb075eb6af] succeeded in 0.002425100072287023s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,948: INFO/MainProcess] Task tasks.scrape_pending_urls[5a451448-dc47-4315-af41-9c8e5089186c] received
[2026-03-27 00:42:48,952: INFO/MainProcess] Task tasks.scrape_pending_urls[5a451448-dc47-4315-af41-9c8e5089186c] succeeded in 0.0029442000668495893s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,953: INFO/MainProcess] Task tasks.scrape_pending_urls[72d0898b-bc45-4897-b38b-938cbf4e8a04] received
[2026-03-27 00:42:48,956: INFO/MainProcess] Task tasks.scrape_pending_urls[72d0898b-bc45-4897-b38b-938cbf4e8a04] succeeded in 0.002558099920861423s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,958: INFO/MainProcess] Task tasks.scrape_pending_urls[979802b8-655f-45d7-bccd-523de15666f6] received
[2026-03-27 00:42:48,961: INFO/MainProcess] Task tasks.scrape_pending_urls[979802b8-655f-45d7-bccd-523de15666f6] succeeded in 0.0025204999838024378s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,962: INFO/MainProcess] Task tasks.scrape_pending_urls[efce0f2e-6543-48f4-b861-511a15dc7b88] received
[2026-03-27 00:42:48,966: INFO/MainProcess] Task tasks.scrape_pending_urls[efce0f2e-6543-48f4-b861-511a15dc7b88] succeeded in 0.0036184999626129866s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,968: INFO/MainProcess] Task tasks.scrape_pending_urls[2923b470-f742-4ae8-bae3-210ab86af143] received
[2026-03-27 00:42:48,971: INFO/MainProcess] Task tasks.scrape_pending_urls[2923b470-f742-4ae8-bae3-210ab86af143] succeeded in 0.002602500026114285s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,972: INFO/MainProcess] Task tasks.scrape_pending_urls[7d4a37a3-3980-4ae2-ab8c-c5eaa526d39c] received
[2026-03-27 00:42:48,975: INFO/MainProcess] Task tasks.scrape_pending_urls[7d4a37a3-3980-4ae2-ab8c-c5eaa526d39c] succeeded in 0.002494000014849007s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,977: INFO/MainProcess] Task tasks.scrape_pending_urls[0fb57ae5-1323-4201-8fec-fe512e7d7a09] received
[2026-03-27 00:42:48,980: INFO/MainProcess] Task tasks.scrape_pending_urls[0fb57ae5-1323-4201-8fec-fe512e7d7a09] succeeded in 0.0032355000730603933s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,982: INFO/MainProcess] Task tasks.scrape_pending_urls[308a4f0f-4a15-4aa2-b234-4334bf8c2acc] received
[2026-03-27 00:42:48,985: INFO/MainProcess] Task tasks.scrape_pending_urls[308a4f0f-4a15-4aa2-b234-4334bf8c2acc] succeeded in 0.0026279999874532223s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,987: INFO/MainProcess] Task tasks.scrape_pending_urls[97beaa81-eb00-4c04-ac35-90d2c364aa64] received
[2026-03-27 00:42:48,990: INFO/MainProcess] Task tasks.scrape_pending_urls[97beaa81-eb00-4c04-ac35-90d2c364aa64] succeeded in 0.0025153999449685216s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,991: INFO/MainProcess] Task tasks.scrape_pending_urls[9f436c24-e336-4191-852a-12eb2943498e] received
[2026-03-27 00:42:48,994: INFO/MainProcess] Task tasks.scrape_pending_urls[9f436c24-e336-4191-852a-12eb2943498e] succeeded in 0.0024217000463977456s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:48,996: INFO/MainProcess] Task tasks.scrape_pending_urls[388eec8e-05b4-429b-acdb-a1a7665412da] received
[2026-03-27 00:42:48,999: INFO/MainProcess] Task tasks.scrape_pending_urls[388eec8e-05b4-429b-acdb-a1a7665412da] succeeded in 0.002911000046879053s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,001: INFO/MainProcess] Task tasks.scrape_pending_urls[59e02dc9-a19f-4c7a-84ea-ace620801b5e] received
[2026-03-27 00:42:49,004: INFO/MainProcess] Task tasks.scrape_pending_urls[59e02dc9-a19f-4c7a-84ea-ace620801b5e] succeeded in 0.0029503999976441264s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,006: INFO/MainProcess] Task tasks.scrape_pending_urls[84242778-0254-4288-a128-84f4a81e5c2c] received
[2026-03-27 00:42:49,009: INFO/MainProcess] Task tasks.scrape_pending_urls[84242778-0254-4288-a128-84f4a81e5c2c] succeeded in 0.0024594999849796295s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,010: INFO/MainProcess] Task tasks.scrape_pending_urls[74ffec49-4a9d-46ec-ae43-96cfd67c3358] received
[2026-03-27 00:42:49,015: INFO/MainProcess] Task tasks.scrape_pending_urls[74ffec49-4a9d-46ec-ae43-96cfd67c3358] succeeded in 0.0029259000439196825s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,016: INFO/MainProcess] Task tasks.scrape_pending_urls[bde1745e-4125-4388-b58a-c29ff554a920] received
[2026-03-27 00:42:49,019: INFO/MainProcess] Task tasks.scrape_pending_urls[bde1745e-4125-4388-b58a-c29ff554a920] succeeded in 0.002543900045566261s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,021: INFO/MainProcess] Task tasks.scrape_pending_urls[f08272c7-3489-4b27-87af-149317bfa197] received
[2026-03-27 00:42:49,024: INFO/MainProcess] Task tasks.scrape_pending_urls[f08272c7-3489-4b27-87af-149317bfa197] succeeded in 0.002523500006645918s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,025: INFO/MainProcess] Task tasks.scrape_pending_urls[e05ab469-7052-4141-9b29-5afa48427788] received
[2026-03-27 00:42:49,029: INFO/MainProcess] Task tasks.scrape_pending_urls[e05ab469-7052-4141-9b29-5afa48427788] succeeded in 0.003415199927985668s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,031: INFO/MainProcess] Task tasks.scrape_pending_urls[454aff9e-5e96-49a6-b1ac-01ca2d044f02] received
[2026-03-27 00:42:49,034: INFO/MainProcess] Task tasks.scrape_pending_urls[454aff9e-5e96-49a6-b1ac-01ca2d044f02] succeeded in 0.0026647000340744853s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,035: INFO/MainProcess] Task tasks.scrape_pending_urls[d1720c2c-8ccd-4805-bb43-e6d4caecb460] received
[2026-03-27 00:42:49,038: INFO/MainProcess] Task tasks.scrape_pending_urls[d1720c2c-8ccd-4805-bb43-e6d4caecb460] succeeded in 0.002571400022134185s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,040: INFO/MainProcess] Task tasks.scrape_pending_urls[2c394a8e-4fce-458d-8903-08c55ae5c960] received
[2026-03-27 00:42:49,043: INFO/MainProcess] Task tasks.scrape_pending_urls[2c394a8e-4fce-458d-8903-08c55ae5c960] succeeded in 0.003216999932192266s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,045: INFO/MainProcess] Task tasks.scrape_pending_urls[af6a7227-9547-4ed9-95c0-916127bfb9fd] received
[2026-03-27 00:42:49,049: INFO/MainProcess] Task tasks.scrape_pending_urls[af6a7227-9547-4ed9-95c0-916127bfb9fd] succeeded in 0.0031707999296486378s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,051: INFO/MainProcess] Task tasks.scrape_pending_urls[ab02a93a-4772-432c-9e5e-844b19f07c41] received
[2026-03-27 00:42:49,054: INFO/MainProcess] Task tasks.scrape_pending_urls[ab02a93a-4772-432c-9e5e-844b19f07c41] succeeded in 0.0026384000666439533s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,055: INFO/MainProcess] Task tasks.scrape_pending_urls[ebfd41f9-4167-411f-82e7-38a3ee2ca528] received
[2026-03-27 00:42:49,058: INFO/MainProcess] Task tasks.scrape_pending_urls[ebfd41f9-4167-411f-82e7-38a3ee2ca528] succeeded in 0.002575900056399405s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,061: INFO/MainProcess] Task tasks.scrape_pending_urls[287fbf61-9cfa-4786-b22f-d6b3f3899e6f] received
[2026-03-27 00:42:49,064: INFO/MainProcess] Task tasks.scrape_pending_urls[287fbf61-9cfa-4786-b22f-d6b3f3899e6f] succeeded in 0.0026690999511629343s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,065: INFO/MainProcess] Task tasks.scrape_pending_urls[6d4dbaad-8f38-4a19-942f-183cb491cfba] received
[2026-03-27 00:42:49,068: INFO/MainProcess] Task tasks.scrape_pending_urls[6d4dbaad-8f38-4a19-942f-183cb491cfba] succeeded in 0.0025174999609589577s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,070: INFO/MainProcess] Task tasks.scrape_pending_urls[46c9b099-edcb-4fe3-bea1-1f93bfe963ec] received
[2026-03-27 00:42:49,072: INFO/MainProcess] Task tasks.scrape_pending_urls[46c9b099-edcb-4fe3-bea1-1f93bfe963ec] succeeded in 0.0025125000393018126s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,074: INFO/MainProcess] Task tasks.scrape_pending_urls[68a9cc77-3a3e-44ee-a7d0-86afeddc096d] received
[2026-03-27 00:42:49,079: INFO/MainProcess] Task tasks.scrape_pending_urls[68a9cc77-3a3e-44ee-a7d0-86afeddc096d] succeeded in 0.0029808999970555305s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,080: INFO/MainProcess] Task tasks.scrape_pending_urls[c569f542-04d2-4023-b7c2-49879273ac26] received
[2026-03-27 00:42:49,083: INFO/MainProcess] Task tasks.scrape_pending_urls[c569f542-04d2-4023-b7c2-49879273ac26] succeeded in 0.002572299912571907s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,085: INFO/MainProcess] Task tasks.scrape_pending_urls[56ddad06-82b6-46c2-9d86-92890fffd00c] received
[2026-03-27 00:42:49,088: INFO/MainProcess] Task tasks.scrape_pending_urls[56ddad06-82b6-46c2-9d86-92890fffd00c] succeeded in 0.002513199928216636s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,089: INFO/MainProcess] Task tasks.scrape_pending_urls[8a8fd875-409a-43ea-948d-e0903c83915d] received
[2026-03-27 00:42:49,093: INFO/MainProcess] Task tasks.scrape_pending_urls[8a8fd875-409a-43ea-948d-e0903c83915d] succeeded in 0.003857300034724176s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,095: INFO/MainProcess] Task tasks.scrape_pending_urls[546eb9a0-ecaf-4e21-aa8c-b8f384a8d6ca] received
[2026-03-27 00:42:49,098: INFO/MainProcess] Task tasks.scrape_pending_urls[546eb9a0-ecaf-4e21-aa8c-b8f384a8d6ca] succeeded in 0.0028945000376552343s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,100: INFO/MainProcess] Task tasks.scrape_pending_urls[3fc1ee19-2175-4408-a0ea-be3971a0bf68] received
[2026-03-27 00:42:49,103: INFO/MainProcess] Task tasks.scrape_pending_urls[3fc1ee19-2175-4408-a0ea-be3971a0bf68] succeeded in 0.002522700000554323s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,104: INFO/MainProcess] Task tasks.scrape_pending_urls[9f7c4198-b018-40ab-a413-8e6ef4c28ab5] received
[2026-03-27 00:42:49,108: INFO/MainProcess] Task tasks.scrape_pending_urls[9f7c4198-b018-40ab-a413-8e6ef4c28ab5] succeeded in 0.0035746999783441424s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,110: INFO/MainProcess] Task tasks.scrape_pending_urls[1add7194-0eea-4c03-839b-fdbd07e62121] received
[2026-03-27 00:42:49,113: INFO/MainProcess] Task tasks.scrape_pending_urls[1add7194-0eea-4c03-839b-fdbd07e62121] succeeded in 0.0025704000145196915s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,114: INFO/MainProcess] Task tasks.scrape_pending_urls[62a3e60a-4c35-4dff-86bd-0272a351fb03] received
[2026-03-27 00:42:49,117: INFO/MainProcess] Task tasks.scrape_pending_urls[62a3e60a-4c35-4dff-86bd-0272a351fb03] succeeded in 0.0025282000424340367s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,119: INFO/MainProcess] Task tasks.scrape_pending_urls[ea299f4e-9ec6-46e6-97c3-ce1648b74a38] received
[2026-03-27 00:42:49,122: INFO/MainProcess] Task tasks.scrape_pending_urls[ea299f4e-9ec6-46e6-97c3-ce1648b74a38] succeeded in 0.0025589000433683395s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,125: INFO/MainProcess] Task tasks.scrape_pending_urls[75324050-a5f2-4831-b579-03125eaf591c] received
[2026-03-27 00:42:49,128: INFO/MainProcess] Task tasks.scrape_pending_urls[75324050-a5f2-4831-b579-03125eaf591c] succeeded in 0.002791399951092899s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,130: INFO/MainProcess] Task tasks.scrape_pending_urls[191f5dce-4c15-41f1-a353-52395a5850d9] received
[2026-03-27 00:42:49,133: INFO/MainProcess] Task tasks.scrape_pending_urls[191f5dce-4c15-41f1-a353-52395a5850d9] succeeded in 0.0027193999849259853s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,134: INFO/MainProcess] Task tasks.scrape_pending_urls[445d7527-f0f4-4129-b994-f43e91cc0678] received
[2026-03-27 00:42:49,137: INFO/MainProcess] Task tasks.scrape_pending_urls[445d7527-f0f4-4129-b994-f43e91cc0678] succeeded in 0.002536299987696111s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,139: INFO/MainProcess] Task tasks.scrape_pending_urls[4625c4c7-32e4-4191-87d8-68c247686e30] received
[2026-03-27 00:42:49,143: INFO/MainProcess] Task tasks.scrape_pending_urls[4625c4c7-32e4-4191-87d8-68c247686e30] succeeded in 0.003185399924404919s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,145: INFO/MainProcess] Task tasks.scrape_pending_urls[eab162ec-0b7d-4d1a-ac51-f0c1f343c099] received
[2026-03-27 00:42:49,148: INFO/MainProcess] Task tasks.scrape_pending_urls[eab162ec-0b7d-4d1a-ac51-f0c1f343c099] succeeded in 0.0026032000314444304s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,149: INFO/MainProcess] Task tasks.scrape_pending_urls[aa51c981-2da3-4005-8226-e2fb8e445d72] received
[2026-03-27 00:42:49,152: INFO/MainProcess] Task tasks.scrape_pending_urls[aa51c981-2da3-4005-8226-e2fb8e445d72] succeeded in 0.002513099927455187s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,153: INFO/MainProcess] Task tasks.scrape_pending_urls[509dfec0-23ba-487c-a453-8f428a120d43] received
[2026-03-27 00:42:49,158: INFO/MainProcess] Task tasks.scrape_pending_urls[509dfec0-23ba-487c-a453-8f428a120d43] succeeded in 0.003264899947680533s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,160: INFO/MainProcess] Task tasks.scrape_pending_urls[c4da3aa6-d89b-4020-a945-80321726123a] received
[2026-03-27 00:42:49,163: INFO/MainProcess] Task tasks.scrape_pending_urls[c4da3aa6-d89b-4020-a945-80321726123a] succeeded in 0.0025652999756857753s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,164: INFO/MainProcess] Task tasks.scrape_pending_urls[ce8be9c0-6040-4d32-b781-f41435c2cb9e] received
[2026-03-27 00:42:49,167: INFO/MainProcess] Task tasks.scrape_pending_urls[ce8be9c0-6040-4d32-b781-f41435c2cb9e] succeeded in 0.0024687000550329685s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,169: INFO/MainProcess] Task tasks.scrape_pending_urls[83992a6b-6bae-489d-a1b3-630f0a06c988] received
[2026-03-27 00:42:49,173: INFO/MainProcess] Task tasks.scrape_pending_urls[83992a6b-6bae-489d-a1b3-630f0a06c988] succeeded in 0.00413080002181232s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,175: INFO/MainProcess] Task tasks.scrape_pending_urls[ce505275-d1d0-46f6-9618-1f60cd4d585b] received
[2026-03-27 00:42:49,178: INFO/MainProcess] Task tasks.scrape_pending_urls[ce505275-d1d0-46f6-9618-1f60cd4d585b] succeeded in 0.0026193999219685793s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,180: INFO/MainProcess] Task tasks.scrape_pending_urls[43352fba-7629-461b-b813-f33952205468] received
[2026-03-27 00:42:49,183: INFO/MainProcess] Task tasks.scrape_pending_urls[43352fba-7629-461b-b813-f33952205468] succeeded in 0.0025286999298259616s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,184: INFO/MainProcess] Task tasks.scrape_pending_urls[715e53c2-a378-45cd-8ed9-2837b96262b0] received
[2026-03-27 00:42:49,188: INFO/MainProcess] Task tasks.scrape_pending_urls[715e53c2-a378-45cd-8ed9-2837b96262b0] succeeded in 0.0034441999159753323s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,190: INFO/MainProcess] Task tasks.scrape_pending_urls[7fb42c62-8db8-41cc-b761-7362f14a98df] received
[2026-03-27 00:42:49,193: INFO/MainProcess] Task tasks.scrape_pending_urls[7fb42c62-8db8-41cc-b761-7362f14a98df] succeeded in 0.002694800030440092s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,194: INFO/MainProcess] Task tasks.scrape_pending_urls[5973c5a6-66a1-4b47-b52d-8498523a0867] received
[2026-03-27 00:42:49,197: INFO/MainProcess] Task tasks.scrape_pending_urls[5973c5a6-66a1-4b47-b52d-8498523a0867] succeeded in 0.0025589000433683395s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,199: INFO/MainProcess] Task tasks.scrape_pending_urls[cabe24df-3b70-4661-8b2d-78891a40f94a] received
[2026-03-27 00:42:49,202: INFO/MainProcess] Task tasks.scrape_pending_urls[cabe24df-3b70-4661-8b2d-78891a40f94a] succeeded in 0.0030807999428361654s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,204: INFO/MainProcess] Task tasks.scrape_pending_urls[98df01fb-a3a6-4d4e-80eb-22b08f636519] received
[2026-03-27 00:42:49,207: INFO/MainProcess] Task tasks.scrape_pending_urls[98df01fb-a3a6-4d4e-80eb-22b08f636519] succeeded in 0.0026508000446483493s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,208: INFO/MainProcess] Task tasks.scrape_pending_urls[07383730-0863-4399-80f2-e0ded636f00d] received
[2026-03-27 00:42:49,211: INFO/MainProcess] Task tasks.scrape_pending_urls[07383730-0863-4399-80f2-e0ded636f00d] succeeded in 0.0025730000343173742s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,213: INFO/MainProcess] Task tasks.scrape_pending_urls[54d41991-88bb-4789-a136-e35ff9c1efcc] received
[2026-03-27 00:42:49,215: INFO/MainProcess] Task tasks.scrape_pending_urls[54d41991-88bb-4789-a136-e35ff9c1efcc] succeeded in 0.002485400065779686s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,217: INFO/MainProcess] Task tasks.scrape_pending_urls[1b05768f-1ffa-4415-8dce-993172c10704] received
[2026-03-27 00:42:49,220: INFO/MainProcess] Task tasks.scrape_pending_urls[1b05768f-1ffa-4415-8dce-993172c10704] succeeded in 0.0026682999450713396s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,222: INFO/MainProcess] Task tasks.scrape_pending_urls[ec472e22-cb3d-465c-8d12-d4443f93d70d] received
[2026-03-27 00:42:49,225: INFO/MainProcess] Task tasks.scrape_pending_urls[ec472e22-cb3d-465c-8d12-d4443f93d70d] succeeded in 0.002464899909682572s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,226: INFO/MainProcess] Task tasks.scrape_pending_urls[d7c186f8-afbb-48e1-adb0-70c41930e517] received
[2026-03-27 00:42:49,229: INFO/MainProcess] Task tasks.scrape_pending_urls[d7c186f8-afbb-48e1-adb0-70c41930e517] succeeded in 0.0025476000737398863s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,231: INFO/MainProcess] Task tasks.scrape_pending_urls[86fdd115-01a3-4c49-af5f-c1b669d12b24] received
[2026-03-27 00:42:49,235: INFO/MainProcess] Task tasks.scrape_pending_urls[86fdd115-01a3-4c49-af5f-c1b669d12b24] succeeded in 0.004002699977718294s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,237: INFO/MainProcess] Task tasks.scrape_pending_urls[0f4b397c-304c-4fc9-a85d-1dd527d17284] received
[2026-03-27 00:42:49,240: INFO/MainProcess] Task tasks.scrape_pending_urls[0f4b397c-304c-4fc9-a85d-1dd527d17284] succeeded in 0.002682400052435696s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,241: INFO/MainProcess] Task tasks.scrape_pending_urls[a0d13fbe-dd94-43c0-bbd5-19d031e43809] received
[2026-03-27 00:42:49,244: INFO/MainProcess] Task tasks.scrape_pending_urls[a0d13fbe-dd94-43c0-bbd5-19d031e43809] succeeded in 0.0025671999901533127s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,246: INFO/MainProcess] Task tasks.scrape_pending_urls[96fc533c-07df-4ca8-a7d3-33513e243707] received
[2026-03-27 00:42:49,249: INFO/MainProcess] Task tasks.scrape_pending_urls[96fc533c-07df-4ca8-a7d3-33513e243707] succeeded in 0.0027742000529542565s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,251: INFO/MainProcess] Task tasks.scrape_pending_urls[19b8c842-f94e-432d-b3b6-736abadf4fea] received
[2026-03-27 00:42:49,254: INFO/MainProcess] Task tasks.scrape_pending_urls[19b8c842-f94e-432d-b3b6-736abadf4fea] succeeded in 0.0026664999313652515s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,255: INFO/MainProcess] Task tasks.scrape_pending_urls[8a5cd671-7c37-4de9-8011-098f308073b6] received
[2026-03-27 00:42:49,258: INFO/MainProcess] Task tasks.scrape_pending_urls[8a5cd671-7c37-4de9-8011-098f308073b6] succeeded in 0.002338399994187057s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,260: INFO/MainProcess] Task tasks.scrape_pending_urls[bde4430a-a98a-468b-a032-82c2e3f0edaf] received
[2026-03-27 00:42:49,262: INFO/MainProcess] Task tasks.scrape_pending_urls[bde4430a-a98a-468b-a032-82c2e3f0edaf] succeeded in 0.002416800009086728s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,264: INFO/MainProcess] Task tasks.scrape_pending_urls[eee69750-d11e-457f-ac29-138a8efa9dd7] received
[2026-03-27 00:42:49,268: INFO/MainProcess] Task tasks.scrape_pending_urls[eee69750-d11e-457f-ac29-138a8efa9dd7] succeeded in 0.003895799978636205s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,269: INFO/MainProcess] Task tasks.scrape_pending_urls[2f9ca2be-b1bb-46c8-89bb-adf1e803b93a] received
[2026-03-27 00:42:49,273: INFO/MainProcess] Task tasks.scrape_pending_urls[2f9ca2be-b1bb-46c8-89bb-adf1e803b93a] succeeded in 0.003000600030645728s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,274: INFO/MainProcess] Task tasks.scrape_pending_urls[aa418ecd-bf4d-469f-b636-de58242b0117] received
[2026-03-27 00:42:49,277: INFO/MainProcess] Task tasks.scrape_pending_urls[aa418ecd-bf4d-469f-b636-de58242b0117] succeeded in 0.002493900014087558s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,279: INFO/MainProcess] Task tasks.scrape_pending_urls[636f70e5-572f-450b-a1aa-a31591d367c1] received
[2026-03-27 00:42:49,283: INFO/MainProcess] Task tasks.scrape_pending_urls[636f70e5-572f-450b-a1aa-a31591d367c1] succeeded in 0.0038898999337106943s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,285: INFO/MainProcess] Task tasks.scrape_pending_urls[338d1f71-6582-4535-b937-de8ea214b1a6] received
[2026-03-27 00:42:49,289: INFO/MainProcess] Task tasks.scrape_pending_urls[338d1f71-6582-4535-b937-de8ea214b1a6] succeeded in 0.0037031000247225165s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,291: INFO/MainProcess] Task tasks.scrape_pending_urls[af35d17e-c5f3-4411-ae85-18761d63c88f] received
[2026-03-27 00:42:49,295: INFO/MainProcess] Task tasks.scrape_pending_urls[af35d17e-c5f3-4411-ae85-18761d63c88f] succeeded in 0.0037270999746397138s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,299: INFO/MainProcess] Task tasks.scrape_pending_urls[eb907576-a5f6-4b1e-a45b-1f861f9d884f] received
[2026-03-27 00:42:49,303: INFO/MainProcess] Task tasks.scrape_pending_urls[eb907576-a5f6-4b1e-a45b-1f861f9d884f] succeeded in 0.003850300097838044s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,305: INFO/MainProcess] Task tasks.scrape_pending_urls[14b005b5-0b73-4cc0-996e-231fb5387204] received
[2026-03-27 00:42:49,308: INFO/MainProcess] Task tasks.scrape_pending_urls[14b005b5-0b73-4cc0-996e-231fb5387204] succeeded in 0.003194899996742606s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,310: INFO/MainProcess] Task tasks.scrape_pending_urls[f4bce095-409f-4910-a964-0432bc6536b7] received
[2026-03-27 00:42:49,315: INFO/MainProcess] Task tasks.scrape_pending_urls[f4bce095-409f-4910-a964-0432bc6536b7] succeeded in 0.004844099981710315s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:42:49,317: INFO/MainProcess] Task tasks.scrape_pending_urls[f81f1a5a-dc52-44eb-8d39-105b77cb8f7a] received
[2026-03-27 00:42:49,321: INFO/MainProcess] Task tasks.scrape_pending_urls[f81f1a5a-dc52-44eb-8d39-105b77cb8f7a] succeeded in 0.003756399964913726s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:43:15,697: INFO/MainProcess] Task tasks.scrape_pending_urls[128bb2c3-19bd-4206-beee-782d9c7abead] received
[2026-03-27 00:43:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[128bb2c3-19bd-4206-beee-782d9c7abead] succeeded in 0.003307799925096333s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:43:45,697: INFO/MainProcess] Task tasks.scrape_pending_urls[12e7b7f9-baf9-407a-9698-ee1adad726cf] received
[2026-03-27 00:43:45,701: INFO/MainProcess] Task tasks.scrape_pending_urls[12e7b7f9-baf9-407a-9698-ee1adad726cf] succeeded in 0.0035607999889180064s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:44:15,697: INFO/MainProcess] Task tasks.scrape_pending_urls[724683d1-34e1-4a0f-bb2d-8f1c301d5e39] received
[2026-03-27 00:44:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[724683d1-34e1-4a0f-bb2d-8f1c301d5e39] succeeded in 0.0032875000033527613s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:44:45,590: INFO/MainProcess] Task tasks.collect_system_metrics[774a399e-f537-42ec-9dbc-46a00fc5ebd4] received
[2026-03-27 00:44:46,107: INFO/MainProcess] Task tasks.collect_system_metrics[774a399e-f537-42ec-9dbc-46a00fc5ebd4] succeeded in 0.5169840999878943s: {'cpu': 10.5, 'memory': 44.9}
[2026-03-27 00:44:46,109: INFO/MainProcess] Task tasks.scrape_pending_urls[59101532-1621-4207-b09f-4cbd3e900ce9] received
[2026-03-27 00:44:46,113: INFO/MainProcess] Task tasks.scrape_pending_urls[59101532-1621-4207-b09f-4cbd3e900ce9] succeeded in 0.0033520000288262963s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:45:15,697: INFO/MainProcess] Task tasks.scrape_pending_urls[28da37d5-b511-45ef-8f6c-510fb3a14fed] received
[2026-03-27 00:45:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[28da37d5-b511-45ef-8f6c-510fb3a14fed] succeeded in 0.0034055999713018537s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:45:45,697: INFO/MainProcess] Task tasks.scrape_pending_urls[c14ddbdb-50fd-4e3d-8726-e46f42520bd0] received
[2026-03-27 00:45:45,701: INFO/MainProcess] Task tasks.scrape_pending_urls[c14ddbdb-50fd-4e3d-8726-e46f42520bd0] succeeded in 0.0034853999968618155s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:46:15,697: INFO/MainProcess] Task tasks.scrape_pending_urls[8d94444c-393b-441d-9638-fc3d33fa7a52] received
[2026-03-27 00:46:15,700: INFO/MainProcess] Task tasks.scrape_pending_urls[8d94444c-393b-441d-9638-fc3d33fa7a52] succeeded in 0.003242200007662177s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:46:45,698: INFO/MainProcess] Task tasks.scrape_pending_urls[fc37278c-4a5a-4e73-8f41-cbdc5649f7b1] received
[2026-03-27 00:46:45,701: INFO/MainProcess] Task tasks.scrape_pending_urls[fc37278c-4a5a-4e73-8f41-cbdc5649f7b1] succeeded in 0.0033900999696925282s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:47:15,697: INFO/MainProcess] Task tasks.scrape_pending_urls[7d97ec2a-b120-43ce-9d3b-f763ae1df313] received
[2026-03-27 00:47:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[7d97ec2a-b120-43ce-9d3b-f763ae1df313] succeeded in 0.003232200047932565s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:47:45,698: INFO/MainProcess] Task tasks.scrape_pending_urls[93890b48-4105-4554-8dde-82f69a65ac36] received
[2026-03-27 00:47:45,702: INFO/MainProcess] Task tasks.scrape_pending_urls[93890b48-4105-4554-8dde-82f69a65ac36] succeeded in 0.003715099999681115s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:48:15,697: INFO/MainProcess] Task tasks.scrape_pending_urls[bfc2459f-97fe-4b19-99e8-4c1acc4973ee] received
[2026-03-27 00:48:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[bfc2459f-97fe-4b19-99e8-4c1acc4973ee] succeeded in 0.003257900010794401s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:48:45,702: INFO/MainProcess] Task tasks.scrape_pending_urls[85c9731a-0959-4952-afbc-46e722d3662a] received
[2026-03-27 00:48:45,706: INFO/MainProcess] Task tasks.scrape_pending_urls[85c9731a-0959-4952-afbc-46e722d3662a] succeeded in 0.003702000016346574s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:49:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[a64f3e87-9dac-4962-9f31-c49a3fce88f7] received
[2026-03-27 00:49:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[a64f3e87-9dac-4962-9f31-c49a3fce88f7] succeeded in 0.003221399965696037s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:49:45,582: INFO/MainProcess] Task tasks.reset_stale_processing_urls[31ec562c-1a30-47f3-88b1-469da1fc409f] received
[2026-03-27 00:49:45,585: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 00:49:45,586: INFO/MainProcess] Task tasks.reset_stale_processing_urls[31ec562c-1a30-47f3-88b1-469da1fc409f] succeeded in 0.0039036000380292535s: {'reset': 0}
[2026-03-27 00:49:45,589: INFO/MainProcess] Task tasks.collect_system_metrics[4587a9bf-eb6e-434f-8211-beb31e3902d2] received
[2026-03-27 00:49:46,106: INFO/MainProcess] Task tasks.collect_system_metrics[4587a9bf-eb6e-434f-8211-beb31e3902d2] succeeded in 0.5163146000122651s: {'cpu': 19.1, 'memory': 44.8}
[2026-03-27 00:49:46,108: INFO/MainProcess] Task tasks.scrape_pending_urls[e9e851c0-f707-48c7-88dd-22479110527b] received
[2026-03-27 00:49:46,112: INFO/MainProcess] Task tasks.scrape_pending_urls[e9e851c0-f707-48c7-88dd-22479110527b] succeeded in 0.003017100039869547s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:50:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[42315c45-e480-4f75-88cb-2cadd9384291] received
[2026-03-27 00:50:15,704: INFO/MainProcess] Task tasks.scrape_pending_urls[42315c45-e480-4f75-88cb-2cadd9384291] succeeded in 0.0030527999624609947s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:50:45,701: INFO/MainProcess] Task tasks.scrape_pending_urls[9412ac91-f175-4084-b43f-064984b6e14c] received
[2026-03-27 00:50:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[9412ac91-f175-4084-b43f-064984b6e14c] succeeded in 0.003555299947038293s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:51:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[913bcfd1-3089-4070-81b5-1e293991f03c] received
[2026-03-27 00:51:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[913bcfd1-3089-4070-81b5-1e293991f03c] succeeded in 0.0035151999909430742s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:51:45,702: INFO/MainProcess] Task tasks.scrape_pending_urls[58a3a878-359b-4805-ad01-5abe1dbfa20b] received
[2026-03-27 00:51:45,706: INFO/MainProcess] Task tasks.scrape_pending_urls[58a3a878-359b-4805-ad01-5abe1dbfa20b] succeeded in 0.0033987999195232987s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:52:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[d86dabf8-7c13-493f-9c13-4b34a747e151] received
[2026-03-27 00:52:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[d86dabf8-7c13-493f-9c13-4b34a747e151] succeeded in 0.0035348000237718225s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:52:45,702: INFO/MainProcess] Task tasks.scrape_pending_urls[1c27971e-83d5-46a9-9054-b7876dbd14a0] received
[2026-03-27 00:52:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[1c27971e-83d5-46a9-9054-b7876dbd14a0] succeeded in 0.0033165999921038747s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:53:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[460745b9-739e-4e0e-bb01-fa9f19a642d7] received
[2026-03-27 00:53:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[460745b9-739e-4e0e-bb01-fa9f19a642d7] succeeded in 0.0032160000409930944s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:53:45,702: INFO/MainProcess] Task tasks.scrape_pending_urls[fd8bd0ba-671a-4756-90cd-29a422a93054] received
[2026-03-27 00:53:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[fd8bd0ba-671a-4756-90cd-29a422a93054] succeeded in 0.003382900031283498s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:54:15,701: INFO/MainProcess] Task tasks.scrape_pending_urls[4f1bce5b-8544-4380-9b1c-e180e775b6d2] received
[2026-03-27 00:54:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[4f1bce5b-8544-4380-9b1c-e180e775b6d2] succeeded in 0.0031174999894574285s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:54:45,590: INFO/MainProcess] Task tasks.collect_system_metrics[011243f0-ebe8-4fc8-bbd2-7f45321b3ff1] received
[2026-03-27 00:54:46,107: INFO/MainProcess] Task tasks.collect_system_metrics[011243f0-ebe8-4fc8-bbd2-7f45321b3ff1] succeeded in 0.5164383000228554s: {'cpu': 9.6, 'memory': 44.8}
[2026-03-27 00:54:46,109: INFO/MainProcess] Task tasks.scrape_pending_urls[c0829183-87d0-4039-9164-fd9306d57cdc] received
[2026-03-27 00:54:46,113: INFO/MainProcess] Task tasks.scrape_pending_urls[c0829183-87d0-4039-9164-fd9306d57cdc] succeeded in 0.003787000081501901s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:55:15,704: INFO/MainProcess] Task tasks.scrape_pending_urls[d0dd77f6-8b12-4483-a894-c33064f75fca] received
[2026-03-27 00:55:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[d0dd77f6-8b12-4483-a894-c33064f75fca] succeeded in 0.003245400032028556s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:55:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[00a0b3f4-40c8-42d8-b0d3-4da9bbdcfe64] received
[2026-03-27 00:55:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[00a0b3f4-40c8-42d8-b0d3-4da9bbdcfe64] succeeded in 0.003632600069977343s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:56:15,704: INFO/MainProcess] Task tasks.scrape_pending_urls[3b95bcc0-81c1-4426-aa87-600800ee3b50] received
[2026-03-27 00:56:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[3b95bcc0-81c1-4426-aa87-600800ee3b50] succeeded in 0.003482899977825582s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:56:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[a8315f6a-2a49-4048-a2b2-a1ec8bb33817] received
[2026-03-27 00:56:45,708: INFO/MainProcess] Task tasks.scrape_pending_urls[a8315f6a-2a49-4048-a2b2-a1ec8bb33817] succeeded in 0.0031077000312507153s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:57:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[e60c87c5-19d7-4aff-a7cb-34692df1f035] received
[2026-03-27 00:57:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[e60c87c5-19d7-4aff-a7cb-34692df1f035] succeeded in 0.0034672999754548073s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:57:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[1ad98b33-3d20-4f99-8436-8b379285b1fa] received
[2026-03-27 00:57:45,708: INFO/MainProcess] Task tasks.scrape_pending_urls[1ad98b33-3d20-4f99-8436-8b379285b1fa] succeeded in 0.003042300115339458s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:58:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[f97bd9ca-ab90-4b69-89b1-3bc4e4e8c12d] received
[2026-03-27 00:58:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[f97bd9ca-ab90-4b69-89b1-3bc4e4e8c12d] succeeded in 0.003645600052550435s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:58:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[c666adc3-43d2-487c-9254-38634b548916] received
[2026-03-27 00:58:45,708: INFO/MainProcess] Task tasks.scrape_pending_urls[c666adc3-43d2-487c-9254-38634b548916] succeeded in 0.003042800002731383s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:59:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[3544a663-ebf7-44a9-92ef-f892ee006021] received
[2026-03-27 00:59:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[3544a663-ebf7-44a9-92ef-f892ee006021] succeeded in 0.003566899918951094s: {'status': 'idle', 'pending': 0}
[2026-03-27 00:59:45,590: INFO/MainProcess] Task tasks.collect_system_metrics[5a8b01fd-8dff-4bfe-8a98-ab10e822e7b7] received
[2026-03-27 00:59:46,107: INFO/MainProcess] Task tasks.collect_system_metrics[5a8b01fd-8dff-4bfe-8a98-ab10e822e7b7] succeeded in 0.516233199974522s: {'cpu': 10.2, 'memory': 44.6}
[2026-03-27 00:59:46,109: INFO/MainProcess] Task tasks.scrape_pending_urls[e8ef80e5-346b-41b9-85d7-38480d603b40] received
[2026-03-27 00:59:46,113: INFO/MainProcess] Task tasks.scrape_pending_urls[e8ef80e5-346b-41b9-85d7-38480d603b40] succeeded in 0.003834499977529049s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:00:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[56cbd4ad-aa2f-4e4e-80c4-96e063546b69] received
[2026-03-27 01:00:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[56cbd4ad-aa2f-4e4e-80c4-96e063546b69] succeeded in 0.0031865000491961837s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:00:45,705: INFO/MainProcess] Task tasks.scrape_pending_urls[6614ee14-ede8-42a7-8625-e6282eced4f2] received
[2026-03-27 01:00:45,708: INFO/MainProcess] Task tasks.scrape_pending_urls[6614ee14-ede8-42a7-8625-e6282eced4f2] succeeded in 0.003078400040976703s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:01:15,705: INFO/MainProcess] Task tasks.scrape_pending_urls[a9e1a44a-d996-4d86-a734-127174b3bf1a] received
[2026-03-27 01:01:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[a9e1a44a-d996-4d86-a734-127174b3bf1a] succeeded in 0.003135400009341538s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:01:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[312b3315-874b-4b42-b53c-8b102e29b6d8] received
[2026-03-27 01:01:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[312b3315-874b-4b42-b53c-8b102e29b6d8] succeeded in 0.003279099939391017s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:02:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[76741c68-8876-4904-b339-7d2a04672fa9] received
[2026-03-27 01:02:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[76741c68-8876-4904-b339-7d2a04672fa9] succeeded in 0.003854700014926493s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:02:45,708: INFO/MainProcess] Task tasks.scrape_pending_urls[4797aafd-4164-4998-8ea9-5510a6d3c60e] received
[2026-03-27 01:02:45,712: INFO/MainProcess] Task tasks.scrape_pending_urls[4797aafd-4164-4998-8ea9-5510a6d3c60e] succeeded in 0.0031261000549420714s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:03:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[19d61141-24d7-461d-8169-674c4716c459] received
[2026-03-27 01:03:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[19d61141-24d7-461d-8169-674c4716c459] succeeded in 0.003179199993610382s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:03:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[4cdb42d4-0067-4fa8-bb41-79654711889b] received
[2026-03-27 01:03:45,712: INFO/MainProcess] Task tasks.scrape_pending_urls[4cdb42d4-0067-4fa8-bb41-79654711889b] succeeded in 0.0033144999761134386s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:04:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[8a72bc9e-2347-4602-9794-60f927002b9e] received
[2026-03-27 01:04:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[8a72bc9e-2347-4602-9794-60f927002b9e] succeeded in 0.003470800002105534s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:04:45,590: INFO/MainProcess] Task tasks.collect_system_metrics[ee4982df-532b-448b-a666-9bf6a594e16b] received
[2026-03-27 01:04:46,107: INFO/MainProcess] Task tasks.collect_system_metrics[ee4982df-532b-448b-a666-9bf6a594e16b] succeeded in 0.51612699998077s: {'cpu': 17.8, 'memory': 44.7}
[2026-03-27 01:04:46,109: INFO/MainProcess] Task tasks.scrape_pending_urls[146076e8-173d-43ca-b2ed-4db8521584ec] received
[2026-03-27 01:04:46,113: INFO/MainProcess] Task tasks.scrape_pending_urls[146076e8-173d-43ca-b2ed-4db8521584ec] succeeded in 0.0034490999532863498s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:05:15,708: INFO/MainProcess] Task tasks.scrape_pending_urls[61ebfd9d-a34a-4ba1-8561-20a491928690] received
[2026-03-27 01:05:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[61ebfd9d-a34a-4ba1-8561-20a491928690] succeeded in 0.003287100000306964s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:05:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[745b7298-547d-4f9c-ae6a-b9e255e6a7d1] received
[2026-03-27 01:05:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[745b7298-547d-4f9c-ae6a-b9e255e6a7d1] succeeded in 0.003337399917654693s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:06:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[91f41d28-412c-4aa4-a06d-f156b52bc42a] received
[2026-03-27 01:06:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[91f41d28-412c-4aa4-a06d-f156b52bc42a] succeeded in 0.0035152999917045236s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:06:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[c50b4c2d-fcda-4d8a-b503-aa513f3c9978] received
[2026-03-27 01:06:45,712: INFO/MainProcess] Task tasks.scrape_pending_urls[c50b4c2d-fcda-4d8a-b503-aa513f3c9978] succeeded in 0.0030273000011220574s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:07:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[43577ee1-057d-46f3-9d2d-4d584af1ec6f] received
[2026-03-27 01:07:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[43577ee1-057d-46f3-9d2d-4d584af1ec6f] succeeded in 0.0032665999606251717s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:07:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[71a1cafe-285c-40a4-b036-1fd81031fc89] received
[2026-03-27 01:07:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[71a1cafe-285c-40a4-b036-1fd81031fc89] succeeded in 0.003158399951644242s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:08:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[7cec8a9e-cb28-402d-b39f-238ea1a2817b] received
[2026-03-27 01:08:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[7cec8a9e-cb28-402d-b39f-238ea1a2817b] succeeded in 0.0031767000909894705s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:08:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[32bc0f11-6a1e-4b60-8ff3-09fcf86e1e7e] received
[2026-03-27 01:08:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[32bc0f11-6a1e-4b60-8ff3-09fcf86e1e7e] succeeded in 0.0032676999690011144s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:09:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[0cce41cc-d780-4025-b753-b9cae1b14d5a] received
[2026-03-27 01:09:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[0cce41cc-d780-4025-b753-b9cae1b14d5a] succeeded in 0.0031536000315099955s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:09:45,590: INFO/MainProcess] Task tasks.collect_system_metrics[fd4aceed-39ac-4800-af8e-8e660277881a] received
[2026-03-27 01:09:46,107: INFO/MainProcess] Task tasks.collect_system_metrics[fd4aceed-39ac-4800-af8e-8e660277881a] succeeded in 0.5164820000063628s: {'cpu': 13.7, 'memory': 44.6}
[2026-03-27 01:09:46,109: INFO/MainProcess] Task tasks.scrape_pending_urls[16e4cb42-6af4-4984-b87e-2903190f5eff] received
[2026-03-27 01:09:46,114: INFO/MainProcess] Task tasks.scrape_pending_urls[16e4cb42-6af4-4984-b87e-2903190f5eff] succeeded in 0.004129500011913478s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:10:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[5dbe50a6-7242-4582-9575-ac5397eba40e] received
[2026-03-27 01:10:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[5dbe50a6-7242-4582-9575-ac5397eba40e] succeeded in 0.0032892000162974s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:10:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[b5820681-c99f-4893-9e21-979a1e6014bb] received
[2026-03-27 01:10:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[b5820681-c99f-4893-9e21-979a1e6014bb] succeeded in 0.003322600037790835s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:11:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[a5f03b47-b939-44e3-92c0-edfdcad07fc9] received
[2026-03-27 01:11:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[a5f03b47-b939-44e3-92c0-edfdcad07fc9] succeeded in 0.0031681000255048275s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:11:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[62629d82-d0af-4f67-b6bd-07bb03cfb5fc] received
[2026-03-27 01:11:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[62629d82-d0af-4f67-b6bd-07bb03cfb5fc] succeeded in 0.003088400000706315s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:12:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[4ac0999d-3733-48e8-a81d-777ad4fefe00] received
[2026-03-27 01:12:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[4ac0999d-3733-48e8-a81d-777ad4fefe00] succeeded in 0.0035646000178530812s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:12:45,710: INFO/MainProcess] Task tasks.scrape_pending_urls[20169cb3-b866-49ac-a3f6-1b8e41b4f8ff] received
[2026-03-27 01:12:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[20169cb3-b866-49ac-a3f6-1b8e41b4f8ff] succeeded in 0.003223499981686473s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:13:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[8fcb3cfc-4809-45b6-9aa1-f654f9481e8a] received
[2026-03-27 01:13:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[8fcb3cfc-4809-45b6-9aa1-f654f9481e8a] succeeded in 0.003427599905990064s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:13:45,709: INFO/MainProcess] Task tasks.scrape_pending_urls[93a4bbd9-20d6-498a-90bb-d94172685515] received
[2026-03-27 01:13:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[93a4bbd9-20d6-498a-90bb-d94172685515] succeeded in 0.003264400060288608s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:14:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[cf94bfa0-c2bb-4fbc-9f13-8575f1c6a329] received
[2026-03-27 01:14:15,712: INFO/MainProcess] Task tasks.scrape_pending_urls[cf94bfa0-c2bb-4fbc-9f13-8575f1c6a329] succeeded in 0.0031164000974968076s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:14:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[f2e4c51d-ee62-44fd-a463-818532815681] received
[2026-03-27 01:14:46,111: INFO/MainProcess] Task tasks.collect_system_metrics[f2e4c51d-ee62-44fd-a463-818532815681] succeeded in 0.5163971000583842s: {'cpu': 16.2, 'memory': 44.5}
[2026-03-27 01:14:46,113: INFO/MainProcess] Task tasks.scrape_pending_urls[6d2f7d71-88ef-4a84-8326-f9e20508a2f6] received
[2026-03-27 01:14:46,117: INFO/MainProcess] Task tasks.scrape_pending_urls[6d2f7d71-88ef-4a84-8326-f9e20508a2f6] succeeded in 0.003267599968239665s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:15:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[e15aba3c-125d-4442-91de-65abf49b0e32] received
[2026-03-27 01:15:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[e15aba3c-125d-4442-91de-65abf49b0e32] succeeded in 0.003373799961991608s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:15:45,710: INFO/MainProcess] Task tasks.scrape_pending_urls[cb8a7a04-dc47-4adc-8341-401b0b936b1c] received
[2026-03-27 01:15:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[cb8a7a04-dc47-4adc-8341-401b0b936b1c] succeeded in 0.0030981999589130282s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:16:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[91f4a066-1d23-4031-b748-725d3df0c9eb] received
[2026-03-27 01:16:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[91f4a066-1d23-4031-b748-725d3df0c9eb] succeeded in 0.0031467999797314405s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:16:45,710: INFO/MainProcess] Task tasks.scrape_pending_urls[bdd06d19-040b-4c86-a3de-45c7ce97dae6] received
[2026-03-27 01:16:45,713: INFO/MainProcess] Task tasks.scrape_pending_urls[bdd06d19-040b-4c86-a3de-45c7ce97dae6] succeeded in 0.0030249999836087227s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:17:15,709: INFO/MainProcess] Task tasks.scrape_pending_urls[77b543ba-ce4c-4076-b768-2fd693b803df] received
[2026-03-27 01:17:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[77b543ba-ce4c-4076-b768-2fd693b803df] succeeded in 0.003282399964518845s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:17:45,714: INFO/MainProcess] Task tasks.scrape_pending_urls[f6895bf2-a1ee-4a8c-b0ac-c0ed5e4627a5] received
[2026-03-27 01:17:45,718: INFO/MainProcess] Task tasks.scrape_pending_urls[f6895bf2-a1ee-4a8c-b0ac-c0ed5e4627a5] succeeded in 0.0032949999440461397s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:18:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[93017308-25de-4120-949a-3114dccaccdd] received
[2026-03-27 01:18:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[93017308-25de-4120-949a-3114dccaccdd] succeeded in 0.0033388000447303057s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:18:45,714: INFO/MainProcess] Task tasks.scrape_pending_urls[e69f1774-366f-4c80-a851-9df38c57eb3d] received
[2026-03-27 01:18:45,717: INFO/MainProcess] Task tasks.scrape_pending_urls[e69f1774-366f-4c80-a851-9df38c57eb3d] succeeded in 0.0030352999456226826s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:19:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[9a3a2b5d-0341-4d39-8230-9a45f26de78f] received
[2026-03-27 01:19:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[9a3a2b5d-0341-4d39-8230-9a45f26de78f] succeeded in 0.0031935001024976373s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:19:45,582: INFO/MainProcess] Task tasks.reset_stale_processing_urls[65efc00f-02a3-44eb-b238-381a97c83746] received
[2026-03-27 01:19:45,585: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 01:19:45,587: INFO/MainProcess] Task tasks.reset_stale_processing_urls[65efc00f-02a3-44eb-b238-381a97c83746] succeeded in 0.004155100090429187s: {'reset': 0}
[2026-03-27 01:19:45,593: INFO/MainProcess] Task tasks.collect_system_metrics[8114f4c7-9c4d-424e-bfcd-0fade3b1993b] received
[2026-03-27 01:19:46,110: INFO/MainProcess] Task tasks.collect_system_metrics[8114f4c7-9c4d-424e-bfcd-0fade3b1993b] succeeded in 0.5165827999589965s: {'cpu': 10.5, 'memory': 44.6}
[2026-03-27 01:19:46,112: INFO/MainProcess] Task tasks.scrape_pending_urls[7cb62332-1a61-4e7f-9fa2-08b158003793] received
[2026-03-27 01:19:46,116: INFO/MainProcess] Task tasks.scrape_pending_urls[7cb62332-1a61-4e7f-9fa2-08b158003793] succeeded in 0.0030208999523893s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:20:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[0710b238-de38-4579-9f82-7a3c9ee1b5ad] received
[2026-03-27 01:20:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[0710b238-de38-4579-9f82-7a3c9ee1b5ad] succeeded in 0.0031501000048592687s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:20:45,714: INFO/MainProcess] Task tasks.scrape_pending_urls[56aa740b-00c1-4ace-8742-58cb8ff2d3f0] received
[2026-03-27 01:20:45,717: INFO/MainProcess] Task tasks.scrape_pending_urls[56aa740b-00c1-4ace-8742-58cb8ff2d3f0] succeeded in 0.0030986000783741474s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:21:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[2aac127d-046d-48a2-9154-34640d8274a8] received
[2026-03-27 01:21:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[2aac127d-046d-48a2-9154-34640d8274a8] succeeded in 0.003055499983020127s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:21:45,714: INFO/MainProcess] Task tasks.scrape_pending_urls[c2cd5c6b-3287-4054-a7e6-edea6053f01e] received
[2026-03-27 01:21:45,807: INFO/MainProcess] Task tasks.scrape_pending_urls[c2cd5c6b-3287-4054-a7e6-edea6053f01e] succeeded in 0.09331370005384088s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:22:15,713: INFO/MainProcess] Task tasks.scrape_pending_urls[50929b3e-d7b2-42ed-ae35-9dde21a66eb8] received
[2026-03-27 01:22:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[50929b3e-d7b2-42ed-ae35-9dde21a66eb8] succeeded in 0.0032579998951405287s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:22:45,714: INFO/MainProcess] Task tasks.scrape_pending_urls[c8e2aa36-94bf-4ef7-9be9-da77fce25405] received
[2026-03-27 01:22:45,718: INFO/MainProcess] Task tasks.scrape_pending_urls[c8e2aa36-94bf-4ef7-9be9-da77fce25405] succeeded in 0.003285400103777647s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:23:15,714: INFO/MainProcess] Task tasks.scrape_pending_urls[8ae83b26-9db8-4d35-97c5-ded0780e338b] received
[2026-03-27 01:23:15,718: INFO/MainProcess] Task tasks.scrape_pending_urls[8ae83b26-9db8-4d35-97c5-ded0780e338b] succeeded in 0.003618700080551207s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:23:45,714: INFO/MainProcess] Task tasks.scrape_pending_urls[be5613fb-aa29-4e67-99ba-bc70d84b5701] received
[2026-03-27 01:23:45,718: INFO/MainProcess] Task tasks.scrape_pending_urls[be5613fb-aa29-4e67-99ba-bc70d84b5701] succeeded in 0.0030658000614494085s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:24:15,716: INFO/MainProcess] Task tasks.scrape_pending_urls[e5751576-ed84-41d3-a94d-18b80f39c518] received
[2026-03-27 01:24:15,720: INFO/MainProcess] Task tasks.scrape_pending_urls[e5751576-ed84-41d3-a94d-18b80f39c518] succeeded in 0.003320900024846196s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:24:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[c88993f5-3fb8-4d4f-b1cc-81a813440e97] received
[2026-03-27 01:24:46,113: INFO/MainProcess] Task tasks.collect_system_metrics[c88993f5-3fb8-4d4f-b1cc-81a813440e97] succeeded in 0.5189383999677375s: {'cpu': 13.5, 'memory': 44.8}
[2026-03-27 01:24:46,115: INFO/MainProcess] Task tasks.scrape_pending_urls[7e379a71-d45f-4911-871f-a82bc9269a87] received
[2026-03-27 01:24:46,119: INFO/MainProcess] Task tasks.scrape_pending_urls[7e379a71-d45f-4911-871f-a82bc9269a87] succeeded in 0.0034969999687746167s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:25:15,716: INFO/MainProcess] Task tasks.scrape_pending_urls[9036f062-700c-43f0-853f-349a104eb008] received
[2026-03-27 01:25:15,720: INFO/MainProcess] Task tasks.scrape_pending_urls[9036f062-700c-43f0-853f-349a104eb008] succeeded in 0.003424099995754659s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:25:45,717: INFO/MainProcess] Task tasks.scrape_pending_urls[cc47756e-7725-40ca-a2cf-1dcd7e728347] received
[2026-03-27 01:25:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[cc47756e-7725-40ca-a2cf-1dcd7e728347] succeeded in 0.0031913999700918794s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:26:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[7f9a6212-160b-4879-bdcf-b424b4d11eb4] received
[2026-03-27 01:26:15,720: INFO/MainProcess] Task tasks.scrape_pending_urls[7f9a6212-160b-4879-bdcf-b424b4d11eb4] succeeded in 0.0031071999110281467s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:26:45,717: INFO/MainProcess] Task tasks.scrape_pending_urls[1bb89236-e0b3-4430-b203-4b9ca94346c8] received
[2026-03-27 01:26:45,720: INFO/MainProcess] Task tasks.scrape_pending_urls[1bb89236-e0b3-4430-b203-4b9ca94346c8] succeeded in 0.003054099972359836s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:27:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[351912cd-c133-4d2d-a7f9-e81cb400b1f9] received
[2026-03-27 01:27:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[351912cd-c133-4d2d-a7f9-e81cb400b1f9] succeeded in 0.003695900086313486s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:27:45,717: INFO/MainProcess] Task tasks.scrape_pending_urls[d1c7c4f3-a5a1-4345-8b37-52c512483f6d] received
[2026-03-27 01:27:45,739: INFO/MainProcess] Task tasks.scrape_pending_urls[d1c7c4f3-a5a1-4345-8b37-52c512483f6d] succeeded in 0.021287300041876733s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:28:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[26724b1a-0217-4111-aaa1-fcb6f5809135] received
[2026-03-27 01:28:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[26724b1a-0217-4111-aaa1-fcb6f5809135] succeeded in 0.006656500045210123s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:28:45,717: INFO/MainProcess] Task tasks.scrape_pending_urls[9c225322-9f61-4625-8c89-c306317ddee4] received
[2026-03-27 01:28:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[9c225322-9f61-4625-8c89-c306317ddee4] succeeded in 0.0031487999949604273s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:29:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[a9997eaa-4e3e-4e1a-9a07-dd5ea7af6663] received
[2026-03-27 01:29:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[a9997eaa-4e3e-4e1a-9a07-dd5ea7af6663] succeeded in 0.05509400006849319s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:29:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[8ea070b9-6822-47c1-bfc2-a2b24e30b022] received
[2026-03-27 01:29:46,165: INFO/MainProcess] Task tasks.collect_system_metrics[8ea070b9-6822-47c1-bfc2-a2b24e30b022] succeeded in 0.57071740005631s: {'cpu': 14.3, 'memory': 44.8}
[2026-03-27 01:29:46,167: INFO/MainProcess] Task tasks.scrape_pending_urls[435337c4-3efd-4747-b18c-7b7397c6a7e9] received
[2026-03-27 01:29:46,171: INFO/MainProcess] Task tasks.scrape_pending_urls[435337c4-3efd-4747-b18c-7b7397c6a7e9] succeeded in 0.0031293000793084502s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[bbd59b0f-6f53-4582-bebf-37db9ec05e12] received
[2026-03-27 01:30:00,006: INFO/MainProcess] Task tasks.purge_old_debug_html[bbd59b0f-6f53-4582-bebf-37db9ec05e12] succeeded in 0.001861400087364018s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 01:30:15,717: INFO/MainProcess] Task tasks.scrape_pending_urls[d5f44ea8-f272-4851-aa5f-980bac7f7b69] received
[2026-03-27 01:30:15,720: INFO/MainProcess] Task tasks.scrape_pending_urls[d5f44ea8-f272-4851-aa5f-980bac7f7b69] succeeded in 0.003573100082576275s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:30:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[d195edf8-0a92-49b1-9f27-ea0f54696fa2] received
[2026-03-27 01:30:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[d195edf8-0a92-49b1-9f27-ea0f54696fa2] succeeded in 0.0035446000983938575s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:31:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[3becb2e6-36dc-4e52-9a12-3af9dc492553] received
[2026-03-27 01:31:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[3becb2e6-36dc-4e52-9a12-3af9dc492553] succeeded in 0.00370679993648082s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:31:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[7028b6d9-ef01-4f3f-ac8b-a2fa3d45e8aa] received
[2026-03-27 01:31:45,724: INFO/MainProcess] Task tasks.scrape_pending_urls[7028b6d9-ef01-4f3f-ac8b-a2fa3d45e8aa] succeeded in 0.0032192000653594732s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:32:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[a227e650-f932-4a8b-a60f-7ffb31901515] received
[2026-03-27 01:32:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[a227e650-f932-4a8b-a60f-7ffb31901515] succeeded in 0.003470800002105534s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:32:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[a2330834-fec9-4a74-9550-0a7396804d88] received
[2026-03-27 01:32:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[a2330834-fec9-4a74-9550-0a7396804d88] succeeded in 0.0031751999631524086s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:33:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[c008a1ce-ceff-40e4-bce1-036e430d82ac] received
[2026-03-27 01:33:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[c008a1ce-ceff-40e4-bce1-036e430d82ac] succeeded in 0.0035305999917909503s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:33:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[e0830c37-00bd-427d-8220-8b493b6d0033] received
[2026-03-27 01:33:45,726: INFO/MainProcess] Task tasks.scrape_pending_urls[e0830c37-00bd-427d-8220-8b493b6d0033] succeeded in 0.0040398999117314816s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:34:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[636a09ce-dcf9-409e-806b-1dbd8a3a08e7] received
[2026-03-27 01:34:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[636a09ce-dcf9-409e-806b-1dbd8a3a08e7] succeeded in 0.0034919000463560224s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:34:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[233bca76-ed2a-4368-b9df-5c4d54623563] received
[2026-03-27 01:34:46,114: INFO/MainProcess] Task tasks.collect_system_metrics[233bca76-ed2a-4368-b9df-5c4d54623563] succeeded in 0.5189095999812707s: {'cpu': 14.3, 'memory': 44.8}
[2026-03-27 01:34:46,116: INFO/MainProcess] Task tasks.scrape_pending_urls[1dcbb0af-5fe0-47f5-9fc6-9f7bc2c83b09] received
[2026-03-27 01:34:46,120: INFO/MainProcess] Task tasks.scrape_pending_urls[1dcbb0af-5fe0-47f5-9fc6-9f7bc2c83b09] succeeded in 0.003947499906644225s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:35:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[7bd3674e-71af-40bb-b481-d3077764c2c6] received
[2026-03-27 01:35:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[7bd3674e-71af-40bb-b481-d3077764c2c6] succeeded in 0.003598199924454093s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:35:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[44bcbb12-f3a8-46fe-aeb2-0ef1b5a1dcf0] received
[2026-03-27 01:35:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[44bcbb12-f3a8-46fe-aeb2-0ef1b5a1dcf0] succeeded in 0.0034673999762162566s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:36:15,721: INFO/MainProcess] Task tasks.scrape_pending_urls[8ac67aa8-469e-473b-8b69-a1d3c7e61fc4] received
[2026-03-27 01:36:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[8ac67aa8-469e-473b-8b69-a1d3c7e61fc4] succeeded in 0.0033035000087693334s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:36:45,721: INFO/MainProcess] Task tasks.scrape_pending_urls[88491e4d-7309-4e9c-a1d3-537520162205] received
[2026-03-27 01:36:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[88491e4d-7309-4e9c-a1d3-537520162205] succeeded in 0.0030526999616995454s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:37:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[e66b26db-052c-4922-94b7-b77f60347521] received
[2026-03-27 01:37:15,730: INFO/MainProcess] Task tasks.scrape_pending_urls[e66b26db-052c-4922-94b7-b77f60347521] succeeded in 0.0042013999773189425s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:37:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[f625306d-683d-4bb9-91ee-0729c74d0d25] received
[2026-03-27 01:37:45,728: INFO/MainProcess] Task tasks.scrape_pending_urls[f625306d-683d-4bb9-91ee-0729c74d0d25] succeeded in 0.003141300054267049s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:38:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[22e7d122-b225-47b9-8dfe-ff4efc2e383a] received
[2026-03-27 01:38:15,728: INFO/MainProcess] Task tasks.scrape_pending_urls[22e7d122-b225-47b9-8dfe-ff4efc2e383a] succeeded in 0.0034183000680059195s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:38:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[b889c6f4-56dc-4077-a44f-07f77b9f5ab4] received
[2026-03-27 01:38:45,728: INFO/MainProcess] Task tasks.scrape_pending_urls[b889c6f4-56dc-4077-a44f-07f77b9f5ab4] succeeded in 0.0031887999502941966s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:39:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[6957621e-96bd-4dd2-83cf-d899754dec6c] received
[2026-03-27 01:39:15,728: INFO/MainProcess] Task tasks.scrape_pending_urls[6957621e-96bd-4dd2-83cf-d899754dec6c] succeeded in 0.003347699996083975s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:39:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[dd8ff99d-17f1-4c64-ba51-1b8e892b5a40] received
[2026-03-27 01:39:46,112: INFO/MainProcess] Task tasks.collect_system_metrics[dd8ff99d-17f1-4c64-ba51-1b8e892b5a40] succeeded in 0.5169278999092057s: {'cpu': 13.7, 'memory': 44.7}
[2026-03-27 01:39:46,114: INFO/MainProcess] Task tasks.scrape_pending_urls[ef72b58d-4a48-4bfa-8b68-49363e40e8d3] received
[2026-03-27 01:39:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[ef72b58d-4a48-4bfa-8b68-49363e40e8d3] succeeded in 0.003577299998141825s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:40:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[f22b3de3-c2a0-4024-911f-90789caec69e] received
[2026-03-27 01:40:15,728: INFO/MainProcess] Task tasks.scrape_pending_urls[f22b3de3-c2a0-4024-911f-90789caec69e] succeeded in 0.0035824000369757414s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:40:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[dcf6f7ff-7163-4d2c-8f45-7573b81fa587] received
[2026-03-27 01:40:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[dcf6f7ff-7163-4d2c-8f45-7573b81fa587] succeeded in 0.003323200042359531s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:41:15,724: INFO/MainProcess] Task tasks.scrape_pending_urls[a8fa549a-961c-40a2-942b-3a3681e4cedf] received
[2026-03-27 01:41:15,728: INFO/MainProcess] Task tasks.scrape_pending_urls[a8fa549a-961c-40a2-942b-3a3681e4cedf] succeeded in 0.0035082000540569425s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:41:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[3c196052-d846-4c13-908e-97acb5328d7c] received
[2026-03-27 01:41:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[3c196052-d846-4c13-908e-97acb5328d7c] succeeded in 0.0033035000087693334s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:42:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[22e0dd0d-a78c-4886-919e-09edcd05b112] received
[2026-03-27 01:42:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[22e0dd0d-a78c-4886-919e-09edcd05b112] succeeded in 0.003530499991029501s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:42:45,725: INFO/MainProcess] Task tasks.scrape_pending_urls[9a64045c-3a9e-4539-ad14-48fc60d3f730] received
[2026-03-27 01:42:45,728: INFO/MainProcess] Task tasks.scrape_pending_urls[9a64045c-3a9e-4539-ad14-48fc60d3f730] succeeded in 0.0030233999714255333s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:43:15,725: INFO/MainProcess] Task tasks.scrape_pending_urls[49831485-8957-4916-9d35-8e17ed07f76b] received
[2026-03-27 01:43:15,728: INFO/MainProcess] Task tasks.scrape_pending_urls[49831485-8957-4916-9d35-8e17ed07f76b] succeeded in 0.003396800020709634s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:43:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[119c83c0-57c0-4189-aeb6-19794c1fc66c] received
[2026-03-27 01:43:45,732: INFO/MainProcess] Task tasks.scrape_pending_urls[119c83c0-57c0-4189-aeb6-19794c1fc66c] succeeded in 0.0030427000019699335s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:44:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[adfa2b15-0454-4a36-b980-1f220ac35c74] received
[2026-03-27 01:44:15,734: INFO/MainProcess] Task tasks.scrape_pending_urls[adfa2b15-0454-4a36-b980-1f220ac35c74] succeeded in 0.0037981999339535832s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:44:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[e934c1fd-c8fd-44e2-b2ca-894ccf88a3e0] received
[2026-03-27 01:44:46,112: INFO/MainProcess] Task tasks.collect_system_metrics[e934c1fd-c8fd-44e2-b2ca-894ccf88a3e0] succeeded in 0.5170267999637872s: {'cpu': 10.0, 'memory': 44.5}
[2026-03-27 01:44:46,114: INFO/MainProcess] Task tasks.scrape_pending_urls[75aa7837-659d-46a2-ac57-2e444ef70479] received
[2026-03-27 01:44:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[75aa7837-659d-46a2-ac57-2e444ef70479] succeeded in 0.0036785000702366233s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:45:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[457c0c83-a6c6-46ee-875b-a1a0d42e2b73] received
[2026-03-27 01:45:15,734: INFO/MainProcess] Task tasks.scrape_pending_urls[457c0c83-a6c6-46ee-875b-a1a0d42e2b73] succeeded in 0.004001099965535104s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:45:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[166187d1-4a18-47ad-8e93-fe73d6e4b363] received
[2026-03-27 01:45:45,732: INFO/MainProcess] Task tasks.scrape_pending_urls[166187d1-4a18-47ad-8e93-fe73d6e4b363] succeeded in 0.0030746000120416284s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:46:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[61e92a93-a34d-4c5f-9c8c-48244698d34b] received
[2026-03-27 01:46:15,732: INFO/MainProcess] Task tasks.scrape_pending_urls[61e92a93-a34d-4c5f-9c8c-48244698d34b] succeeded in 0.0032616000389680266s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:46:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[e1fe62b2-fb0d-4d86-b23a-54bf9830586c] received
[2026-03-27 01:46:45,733: INFO/MainProcess] Task tasks.scrape_pending_urls[e1fe62b2-fb0d-4d86-b23a-54bf9830586c] succeeded in 0.0033521000295877457s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:47:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[d62b4384-3372-4aba-84b6-d3fb89ebd9ca] received
[2026-03-27 01:47:15,733: INFO/MainProcess] Task tasks.scrape_pending_urls[d62b4384-3372-4aba-84b6-d3fb89ebd9ca] succeeded in 0.003782199928537011s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:47:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[3e211780-4836-446d-9682-3cf950718bd4] received
[2026-03-27 01:47:45,733: INFO/MainProcess] Task tasks.scrape_pending_urls[3e211780-4836-446d-9682-3cf950718bd4] succeeded in 0.0035271000815555453s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:48:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[8875884f-cfa2-43d8-ad18-bf340e364997] received
[2026-03-27 01:48:15,733: INFO/MainProcess] Task tasks.scrape_pending_urls[8875884f-cfa2-43d8-ad18-bf340e364997] succeeded in 0.003252000082284212s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:48:45,729: INFO/MainProcess] Task tasks.scrape_pending_urls[96d62ea8-2454-4d45-889d-6470f00ca81d] received
[2026-03-27 01:48:45,733: INFO/MainProcess] Task tasks.scrape_pending_urls[96d62ea8-2454-4d45-889d-6470f00ca81d] succeeded in 0.003069199970923364s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:49:15,729: INFO/MainProcess] Task tasks.scrape_pending_urls[e91f3abb-bc0f-4085-bc22-7ba06bfcebe6] received
[2026-03-27 01:49:15,733: INFO/MainProcess] Task tasks.scrape_pending_urls[e91f3abb-bc0f-4085-bc22-7ba06bfcebe6] succeeded in 0.0035251000663265586s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:49:45,582: INFO/MainProcess] Task tasks.reset_stale_processing_urls[78c517de-a967-46bf-a1dd-335995e4e8b8] received
[2026-03-27 01:49:45,586: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 01:49:45,587: INFO/MainProcess] Task tasks.reset_stale_processing_urls[78c517de-a967-46bf-a1dd-335995e4e8b8] succeeded in 0.0044911999721080065s: {'reset': 0}
[2026-03-27 01:49:45,593: INFO/MainProcess] Task tasks.collect_system_metrics[74ee96e8-980a-49ef-ad04-a0aba13a3d50] received
[2026-03-27 01:49:46,110: INFO/MainProcess] Task tasks.collect_system_metrics[74ee96e8-980a-49ef-ad04-a0aba13a3d50] succeeded in 0.5162094999104738s: {'cpu': 10.9, 'memory': 44.6}
[2026-03-27 01:49:46,112: INFO/MainProcess] Task tasks.scrape_pending_urls[870f25ec-f34e-44c2-9809-e0dec94fe5d8] received
[2026-03-27 01:49:46,116: INFO/MainProcess] Task tasks.scrape_pending_urls[870f25ec-f34e-44c2-9809-e0dec94fe5d8] succeeded in 0.003054399974644184s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:50:15,735: INFO/MainProcess] Task tasks.scrape_pending_urls[8ad84924-e739-4910-bba7-0f7670924fc3] received
[2026-03-27 01:50:15,739: INFO/MainProcess] Task tasks.scrape_pending_urls[8ad84924-e739-4910-bba7-0f7670924fc3] succeeded in 0.0034532001009210944s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:50:45,735: INFO/MainProcess] Task tasks.scrape_pending_urls[6c455d1b-9f90-4fef-a6a8-a21eff9c7e0c] received
[2026-03-27 01:50:45,739: INFO/MainProcess] Task tasks.scrape_pending_urls[6c455d1b-9f90-4fef-a6a8-a21eff9c7e0c] succeeded in 0.0030326000414788723s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:51:15,735: INFO/MainProcess] Task tasks.scrape_pending_urls[6944666e-18ea-46ca-9c07-9132be466821] received
[2026-03-27 01:51:15,739: INFO/MainProcess] Task tasks.scrape_pending_urls[6944666e-18ea-46ca-9c07-9132be466821] succeeded in 0.0032952999463304877s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:51:45,736: INFO/MainProcess] Task tasks.scrape_pending_urls[8d58190b-9caa-45e9-a045-b8b0b7b062ee] received
[2026-03-27 01:51:45,739: INFO/MainProcess] Task tasks.scrape_pending_urls[8d58190b-9caa-45e9-a045-b8b0b7b062ee] succeeded in 0.003172599943354726s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:52:15,735: INFO/MainProcess] Task tasks.scrape_pending_urls[3e445b09-f742-4dc3-814d-77d1a81de8a1] received
[2026-03-27 01:52:15,739: INFO/MainProcess] Task tasks.scrape_pending_urls[3e445b09-f742-4dc3-814d-77d1a81de8a1] succeeded in 0.0033973000245168805s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:52:45,736: INFO/MainProcess] Task tasks.scrape_pending_urls[95dd42cd-d88d-471a-82bd-660d76180cc3] received
[2026-03-27 01:52:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[95dd42cd-d88d-471a-82bd-660d76180cc3] succeeded in 0.0033292999723926187s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:53:15,735: INFO/MainProcess] Task tasks.scrape_pending_urls[8a767083-473d-41d3-a7a0-de9818832c14] received
[2026-03-27 01:53:15,739: INFO/MainProcess] Task tasks.scrape_pending_urls[8a767083-473d-41d3-a7a0-de9818832c14] succeeded in 0.0036518999841064215s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:53:45,736: INFO/MainProcess] Task tasks.scrape_pending_urls[d43f28b1-039d-4aee-aee4-852ad4878c5a] received
[2026-03-27 01:53:45,739: INFO/MainProcess] Task tasks.scrape_pending_urls[d43f28b1-039d-4aee-aee4-852ad4878c5a] succeeded in 0.0032214000821113586s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:54:15,735: INFO/MainProcess] Task tasks.scrape_pending_urls[5766be02-078d-4674-97cf-e3565adfd6b1] received
[2026-03-27 01:54:15,739: INFO/MainProcess] Task tasks.scrape_pending_urls[5766be02-078d-4674-97cf-e3565adfd6b1] succeeded in 0.003461900050751865s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:54:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[ed7975ea-4869-4663-8e54-8cb9ada58088] received
[2026-03-27 01:54:46,117: INFO/MainProcess] Task tasks.collect_system_metrics[ed7975ea-4869-4663-8e54-8cb9ada58088] succeeded in 0.5225679000141099s: {'cpu': 25.7, 'memory': 44.6}
[2026-03-27 01:54:46,119: INFO/MainProcess] Task tasks.scrape_pending_urls[fcfb51b3-839e-4818-b94f-ed5751ca3955] received
[2026-03-27 01:54:46,123: INFO/MainProcess] Task tasks.scrape_pending_urls[fcfb51b3-839e-4818-b94f-ed5751ca3955] succeeded in 0.0032619000412523746s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:55:15,736: INFO/MainProcess] Task tasks.scrape_pending_urls[0bed11c0-41ef-41ee-a88b-cd4216287f28] received
[2026-03-27 01:55:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[0bed11c0-41ef-41ee-a88b-cd4216287f28] succeeded in 0.003995900042355061s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:55:45,736: INFO/MainProcess] Task tasks.scrape_pending_urls[c0ba5256-f4d1-4e0f-a1dd-faa4547657b6] received
[2026-03-27 01:55:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[c0ba5256-f4d1-4e0f-a1dd-faa4547657b6] succeeded in 0.003311099950224161s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:56:15,736: INFO/MainProcess] Task tasks.scrape_pending_urls[fdd39805-3902-437c-85b6-67c355a193db] received
[2026-03-27 01:56:15,739: INFO/MainProcess] Task tasks.scrape_pending_urls[fdd39805-3902-437c-85b6-67c355a193db] succeeded in 0.0034516999730840325s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:56:45,741: INFO/MainProcess] Task tasks.scrape_pending_urls[cce53746-6ce4-4603-9aaa-2995c564e6db] received
[2026-03-27 01:56:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[cce53746-6ce4-4603-9aaa-2995c564e6db] succeeded in 0.0033044000156223774s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:57:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[40e2c246-01c8-43e1-89d7-a0171f3defeb] received
[2026-03-27 01:57:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[40e2c246-01c8-43e1-89d7-a0171f3defeb] succeeded in 0.003291300032287836s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:57:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[277fe168-130d-4c9a-8e73-0eb87a6c6c05] received
[2026-03-27 01:57:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[277fe168-130d-4c9a-8e73-0eb87a6c6c05] succeeded in 0.0035611999919638038s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:58:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[bf021142-0f52-4c3a-bd87-5de8f0299a01] received
[2026-03-27 01:58:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[bf021142-0f52-4c3a-bd87-5de8f0299a01] succeeded in 0.0033778001088649035s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:58:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[f1ac9d6c-ef06-4b5e-aef6-e08041b3a712] received
[2026-03-27 01:58:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[f1ac9d6c-ef06-4b5e-aef6-e08041b3a712] succeeded in 0.0035575999645516276s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:59:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[122112a5-1ae6-40b3-b061-01f66ff29770] received
[2026-03-27 01:59:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[122112a5-1ae6-40b3-b061-01f66ff29770] succeeded in 0.003237099968828261s: {'status': 'idle', 'pending': 0}
[2026-03-27 01:59:45,595: INFO/MainProcess] Task tasks.collect_system_metrics[c800b00b-5a95-4980-9659-e347e2c69ab2] received
[2026-03-27 01:59:46,112: INFO/MainProcess] Task tasks.collect_system_metrics[c800b00b-5a95-4980-9659-e347e2c69ab2] succeeded in 0.5167912000324577s: {'cpu': 14.9, 'memory': 44.5}
[2026-03-27 01:59:46,114: INFO/MainProcess] Task tasks.scrape_pending_urls[2acf4132-ab47-47cf-8c39-62bc4483db41] received
[2026-03-27 01:59:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[2acf4132-ab47-47cf-8c39-62bc4483db41] succeeded in 0.004040599917061627s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:00:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[e7a538e8-c148-4e3c-890b-2700359e23ad] received
[2026-03-27 02:00:15,744: INFO/MainProcess] Task tasks.scrape_pending_urls[e7a538e8-c148-4e3c-890b-2700359e23ad] succeeded in 0.003342100069858134s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:00:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[0738fd76-3bc6-4097-9f7b-1d9f6861b864] received
[2026-03-27 02:00:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[0738fd76-3bc6-4097-9f7b-1d9f6861b864] succeeded in 0.003113500075414777s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:01:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[de7ae81f-ee5f-40f7-a88c-5eeb4902e0e2] received
[2026-03-27 02:01:15,744: INFO/MainProcess] Task tasks.scrape_pending_urls[de7ae81f-ee5f-40f7-a88c-5eeb4902e0e2] succeeded in 0.003502099891193211s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:01:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[88dd7c64-579b-4994-8526-5c90ef6208ae] received
[2026-03-27 02:01:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[88dd7c64-579b-4994-8526-5c90ef6208ae] succeeded in 0.0032887000124901533s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:02:15,740: INFO/MainProcess] Task tasks.scrape_pending_urls[a9fbcbce-b552-41a2-b85f-6383dc993cd6] received
[2026-03-27 02:02:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[a9fbcbce-b552-41a2-b85f-6383dc993cd6] succeeded in 0.0031786999898031354s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:02:45,740: INFO/MainProcess] Task tasks.scrape_pending_urls[e66c4dff-91d5-4702-b19e-be5ecf51479c] received
[2026-03-27 02:02:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[e66c4dff-91d5-4702-b19e-be5ecf51479c] succeeded in 0.00301939994096756s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:03:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[d17691ff-c899-49ee-87d9-fc3828337633] received
[2026-03-27 02:03:15,748: INFO/MainProcess] Task tasks.scrape_pending_urls[d17691ff-c899-49ee-87d9-fc3828337633] succeeded in 0.0037626000121235847s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:03:45,743: INFO/MainProcess] Task tasks.scrape_pending_urls[b2a395fd-2643-4cd6-86fe-ada3d7271a36] received
[2026-03-27 02:03:45,747: INFO/MainProcess] Task tasks.scrape_pending_urls[b2a395fd-2643-4cd6-86fe-ada3d7271a36] succeeded in 0.003049400052987039s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:04:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[29f535c0-8b27-438c-b70d-1979c2317e0d] received
[2026-03-27 02:04:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[29f535c0-8b27-438c-b70d-1979c2317e0d] succeeded in 0.003526599961332977s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:04:45,594: INFO/MainProcess] Task tasks.collect_system_metrics[7e886f66-3191-4570-aa2a-18b0018745a3] received
[2026-03-27 02:04:46,111: INFO/MainProcess] Task tasks.collect_system_metrics[7e886f66-3191-4570-aa2a-18b0018745a3] succeeded in 0.5163471000269055s: {'cpu': 25.1, 'memory': 44.6}
[2026-03-27 02:04:46,113: INFO/MainProcess] Task tasks.scrape_pending_urls[4fa3df11-def8-4cfd-b826-718bcd22b9f4] received
[2026-03-27 02:04:46,117: INFO/MainProcess] Task tasks.scrape_pending_urls[4fa3df11-def8-4cfd-b826-718bcd22b9f4] succeeded in 0.003329800092615187s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:05:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[2eadfc33-1632-4116-b531-01d6f26b9fb5] received
[2026-03-27 02:05:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[2eadfc33-1632-4116-b531-01d6f26b9fb5] succeeded in 0.00333510001655668s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:05:45,743: INFO/MainProcess] Task tasks.scrape_pending_urls[43b70ce9-febe-4be0-9ee1-5d08b848444f] received
[2026-03-27 02:05:45,747: INFO/MainProcess] Task tasks.scrape_pending_urls[43b70ce9-febe-4be0-9ee1-5d08b848444f] succeeded in 0.003004699945449829s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:06:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[3cfcb745-d9b2-4925-b236-b568e27e25ea] received
[2026-03-27 02:06:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[3cfcb745-d9b2-4925-b236-b568e27e25ea] succeeded in 0.0035301001043990254s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:06:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[685c90e5-4726-4c5e-be7a-d0af8eebd260] received
[2026-03-27 02:06:45,748: INFO/MainProcess] Task tasks.scrape_pending_urls[685c90e5-4726-4c5e-be7a-d0af8eebd260] succeeded in 0.003356899949721992s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:07:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[6ad8f2f3-fdd7-4003-ac98-9bb5de39e8e5] received
[2026-03-27 02:07:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[6ad8f2f3-fdd7-4003-ac98-9bb5de39e8e5] succeeded in 0.0032857999904081225s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:07:45,743: INFO/MainProcess] Task tasks.scrape_pending_urls[6bed52bb-52eb-454e-a9d5-18bf7745be15] received
[2026-03-27 02:07:45,747: INFO/MainProcess] Task tasks.scrape_pending_urls[6bed52bb-52eb-454e-a9d5-18bf7745be15] succeeded in 0.0033533000387251377s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:08:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[db0f8056-7535-4760-b5e3-dfc0fb025ddb] received
[2026-03-27 02:08:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[db0f8056-7535-4760-b5e3-dfc0fb025ddb] succeeded in 0.003627199912443757s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:08:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[7ba2819e-4e57-4170-bf21-e5cf47456efb] received
[2026-03-27 02:08:45,747: INFO/MainProcess] Task tasks.scrape_pending_urls[7ba2819e-4e57-4170-bf21-e5cf47456efb] succeeded in 0.0031594999600201845s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:09:15,744: INFO/MainProcess] Task tasks.scrape_pending_urls[cd348ce9-4388-45dc-afdb-4d8cfd1d91d2] received
[2026-03-27 02:09:15,748: INFO/MainProcess] Task tasks.scrape_pending_urls[cd348ce9-4388-45dc-afdb-4d8cfd1d91d2] succeeded in 0.0037797000259160995s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:09:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[19f0c01e-ee6d-4244-a792-e42d6af18d9b] received
[2026-03-27 02:09:46,116: INFO/MainProcess] Task tasks.collect_system_metrics[19f0c01e-ee6d-4244-a792-e42d6af18d9b] succeeded in 0.5165760000236332s: {'cpu': 17.9, 'memory': 44.8}
[2026-03-27 02:09:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[87442075-9fb3-4b2e-8a00-36a400f97df2] received
[2026-03-27 02:09:46,122: INFO/MainProcess] Task tasks.scrape_pending_urls[87442075-9fb3-4b2e-8a00-36a400f97df2] succeeded in 0.003274399903602898s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:10:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[cc5578df-1864-426a-9721-8f7560f27486] received
[2026-03-27 02:10:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[cc5578df-1864-426a-9721-8f7560f27486] succeeded in 0.003272100002504885s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:10:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[91f17f6e-17f1-4947-a5ce-5027570988e0] received
[2026-03-27 02:10:45,748: INFO/MainProcess] Task tasks.scrape_pending_urls[91f17f6e-17f1-4947-a5ce-5027570988e0] succeeded in 0.0034380999859422445s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:11:15,743: INFO/MainProcess] Task tasks.scrape_pending_urls[48796cbe-3f8c-400b-bf45-19346a86dace] received
[2026-03-27 02:11:15,747: INFO/MainProcess] Task tasks.scrape_pending_urls[48796cbe-3f8c-400b-bf45-19346a86dace] succeeded in 0.0034649999579414725s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:11:45,744: INFO/MainProcess] Task tasks.scrape_pending_urls[55e7e1eb-3a72-4639-88db-cac98a39c047] received
[2026-03-27 02:11:45,747: INFO/MainProcess] Task tasks.scrape_pending_urls[55e7e1eb-3a72-4639-88db-cac98a39c047] succeeded in 0.003265300067141652s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:12:15,744: INFO/MainProcess] Task tasks.scrape_pending_urls[3110516d-b7ab-4ebc-8f7c-be6c3cef9f97] received
[2026-03-27 02:12:15,748: INFO/MainProcess] Task tasks.scrape_pending_urls[3110516d-b7ab-4ebc-8f7c-be6c3cef9f97] succeeded in 0.003821799997240305s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:12:45,750: INFO/MainProcess] Task tasks.scrape_pending_urls[35ec3609-64b3-4cbc-bcae-f022057649dc] received
[2026-03-27 02:12:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[35ec3609-64b3-4cbc-bcae-f022057649dc] succeeded in 0.003043500008061528s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:13:15,749: INFO/MainProcess] Task tasks.scrape_pending_urls[4c73cfc1-8179-4bbc-9395-5e5685e5bb88] received
[2026-03-27 02:13:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[4c73cfc1-8179-4bbc-9395-5e5685e5bb88] succeeded in 0.003402199945412576s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:13:45,750: INFO/MainProcess] Task tasks.scrape_pending_urls[2ae9065d-5335-441a-a432-0836c8b1e90f] received
[2026-03-27 02:13:45,753: INFO/MainProcess] Task tasks.scrape_pending_urls[2ae9065d-5335-441a-a432-0836c8b1e90f] succeeded in 0.003162899985909462s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:14:15,750: INFO/MainProcess] Task tasks.scrape_pending_urls[f50b7b63-4f68-4623-8208-5849ad3b56f0] received
[2026-03-27 02:14:15,755: INFO/MainProcess] Task tasks.scrape_pending_urls[f50b7b63-4f68-4623-8208-5849ad3b56f0] succeeded in 0.004650500020943582s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:14:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[6df4911f-9a90-4dae-8e77-ce1f55652a5b] received
[2026-03-27 02:14:46,116: INFO/MainProcess] Task tasks.collect_system_metrics[6df4911f-9a90-4dae-8e77-ce1f55652a5b] succeeded in 0.5172974999295548s: {'cpu': 11.6, 'memory': 44.6}
[2026-03-27 02:14:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[9ee9f36b-cf59-4631-bbda-9544fd78ead0] received
[2026-03-27 02:14:46,124: INFO/MainProcess] Task tasks.scrape_pending_urls[9ee9f36b-cf59-4631-bbda-9544fd78ead0] succeeded in 0.005598100018687546s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:15:15,750: INFO/MainProcess] Task tasks.scrape_pending_urls[fc99ebb8-aef3-4f29-9059-ef80cda5ec7b] received
[2026-03-27 02:15:15,754: INFO/MainProcess] Task tasks.scrape_pending_urls[fc99ebb8-aef3-4f29-9059-ef80cda5ec7b] succeeded in 0.0034617000492289662s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:15:45,750: INFO/MainProcess] Task tasks.scrape_pending_urls[e2fa24dd-8492-4866-bd32-1c1f5f7b466f] received
[2026-03-27 02:15:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[e2fa24dd-8492-4866-bd32-1c1f5f7b466f] succeeded in 0.0033790000015869737s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:16:15,750: INFO/MainProcess] Task tasks.scrape_pending_urls[7b0174fe-665a-4a04-af00-0b0e775526c6] received
[2026-03-27 02:16:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[7b0174fe-665a-4a04-af00-0b0e775526c6] succeeded in 0.0033562000608071685s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:16:45,750: INFO/MainProcess] Task tasks.scrape_pending_urls[9a505f87-e46e-4f28-8d85-93c8b3dde8cb] received
[2026-03-27 02:16:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[9a505f87-e46e-4f28-8d85-93c8b3dde8cb] succeeded in 0.0032021000515669584s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:17:15,750: INFO/MainProcess] Task tasks.scrape_pending_urls[03ba4573-a25d-48e4-8971-9d29b2547330] received
[2026-03-27 02:17:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[03ba4573-a25d-48e4-8971-9d29b2547330] succeeded in 0.003382599912583828s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:17:45,750: INFO/MainProcess] Task tasks.scrape_pending_urls[b0984b28-724c-4d6c-ac8d-a6c96815816e] received
[2026-03-27 02:17:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[b0984b28-724c-4d6c-ac8d-a6c96815816e] succeeded in 0.0033443999709561467s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:18:15,750: INFO/MainProcess] Task tasks.scrape_pending_urls[1391dcb3-4a81-47f7-90aa-5f22259b9853] received
[2026-03-27 02:18:15,754: INFO/MainProcess] Task tasks.scrape_pending_urls[1391dcb3-4a81-47f7-90aa-5f22259b9853] succeeded in 0.003616499947384s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:18:45,750: INFO/MainProcess] Task tasks.scrape_pending_urls[67334875-74ff-47e7-bc2c-ca4acd6bfa6a] received
[2026-03-27 02:18:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[67334875-74ff-47e7-bc2c-ca4acd6bfa6a] succeeded in 0.003475200035609305s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:19:15,754: INFO/MainProcess] Task tasks.scrape_pending_urls[8553e999-28da-4061-a36f-1bd9eecf6a47] received
[2026-03-27 02:19:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[8553e999-28da-4061-a36f-1bd9eecf6a47] succeeded in 0.003375000087544322s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:19:45,582: INFO/MainProcess] Task tasks.reset_stale_processing_urls[aac26d6c-479c-4248-88fa-b7f5da9d4503] received
[2026-03-27 02:19:45,585: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 02:19:45,586: INFO/MainProcess] Task tasks.reset_stale_processing_urls[aac26d6c-479c-4248-88fa-b7f5da9d4503] succeeded in 0.003833599970676005s: {'reset': 0}
[2026-03-27 02:19:45,704: INFO/MainProcess] Task tasks.collect_system_metrics[efd6e999-76e4-4ca1-91b1-0ef26853d337] received
[2026-03-27 02:19:46,221: INFO/MainProcess] Task tasks.collect_system_metrics[efd6e999-76e4-4ca1-91b1-0ef26853d337] succeeded in 0.516891699982807s: {'cpu': 17.2, 'memory': 44.7}
[2026-03-27 02:19:46,223: INFO/MainProcess] Task tasks.scrape_pending_urls[56f3eea0-1963-44c2-8aaa-d7b2d9d77ae2] received
[2026-03-27 02:19:46,227: INFO/MainProcess] Task tasks.scrape_pending_urls[56f3eea0-1963-44c2-8aaa-d7b2d9d77ae2] succeeded in 0.0034344999585300684s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:20:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[68cde5e2-c3b0-49be-9883-bdae18ab5b2a] received
[2026-03-27 02:20:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[68cde5e2-c3b0-49be-9883-bdae18ab5b2a] succeeded in 0.003182200016453862s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:20:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[e20be5ca-8666-46a3-a794-f6b481682760] received
[2026-03-27 02:20:45,757: INFO/MainProcess] Task tasks.scrape_pending_urls[e20be5ca-8666-46a3-a794-f6b481682760] succeeded in 0.003327899961732328s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:21:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[26acf6dd-d160-4066-b039-9deae1d8d73a] received
[2026-03-27 02:21:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[26acf6dd-d160-4066-b039-9deae1d8d73a] succeeded in 0.003387899952940643s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:21:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[86630330-91be-4303-a8e4-a3398c159325] received
[2026-03-27 02:21:45,757: INFO/MainProcess] Task tasks.scrape_pending_urls[86630330-91be-4303-a8e4-a3398c159325] succeeded in 0.003462799941189587s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:22:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[3eae85eb-7b8f-4405-938a-b997a1f0e822] received
[2026-03-27 02:22:15,811: INFO/MainProcess] Task tasks.scrape_pending_urls[3eae85eb-7b8f-4405-938a-b997a1f0e822] succeeded in 0.05697209993377328s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:22:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[47b38a55-42a6-4f3d-b803-8809545f0371] received
[2026-03-27 02:22:45,757: INFO/MainProcess] Task tasks.scrape_pending_urls[47b38a55-42a6-4f3d-b803-8809545f0371] succeeded in 0.003174500074237585s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:23:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[9903483a-debf-4799-b69b-e80b96e58bb6] received
[2026-03-27 02:23:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[9903483a-debf-4799-b69b-e80b96e58bb6] succeeded in 0.003627200028859079s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:23:45,754: INFO/MainProcess] Task tasks.scrape_pending_urls[432ca57e-6656-47c0-b029-b32c35405b37] received
[2026-03-27 02:23:45,757: INFO/MainProcess] Task tasks.scrape_pending_urls[432ca57e-6656-47c0-b029-b32c35405b37] succeeded in 0.003207299974747002s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:24:15,753: INFO/MainProcess] Task tasks.scrape_pending_urls[0d3ccd29-92e1-4b62-8202-512f9cdcfeb6] received
[2026-03-27 02:24:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[0d3ccd29-92e1-4b62-8202-512f9cdcfeb6] succeeded in 0.0031125000678002834s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:24:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[a25fc59b-6f94-43cc-b521-4a566805250a] received
[2026-03-27 02:24:46,116: INFO/MainProcess] Task tasks.collect_system_metrics[a25fc59b-6f94-43cc-b521-4a566805250a] succeeded in 0.5167105000000447s: {'cpu': 17.7, 'memory': 44.8}
[2026-03-27 02:24:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[660ba768-c50f-4e5f-a99c-7cd799edfb5e] received
[2026-03-27 02:24:46,123: INFO/MainProcess] Task tasks.scrape_pending_urls[660ba768-c50f-4e5f-a99c-7cd799edfb5e] succeeded in 0.004826599964872003s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:25:15,754: INFO/MainProcess] Task tasks.scrape_pending_urls[f4e214ae-35d8-4583-b542-4712887230f2] received
[2026-03-27 02:25:15,758: INFO/MainProcess] Task tasks.scrape_pending_urls[f4e214ae-35d8-4583-b542-4712887230f2] succeeded in 0.0036065999884158373s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:25:45,758: INFO/MainProcess] Task tasks.scrape_pending_urls[924f354c-4c6a-4726-96a4-213dc5edbeaf] received
[2026-03-27 02:25:45,762: INFO/MainProcess] Task tasks.scrape_pending_urls[924f354c-4c6a-4726-96a4-213dc5edbeaf] succeeded in 0.003485499997623265s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:26:15,758: INFO/MainProcess] Task tasks.scrape_pending_urls[e1eb4ded-0e35-44ac-950d-480992e78bd3] received
[2026-03-27 02:26:15,762: INFO/MainProcess] Task tasks.scrape_pending_urls[e1eb4ded-0e35-44ac-950d-480992e78bd3] succeeded in 0.004002699977718294s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:26:45,757: INFO/MainProcess] Task tasks.scrape_pending_urls[bda4eb5b-ffc5-4805-a43f-0f60fcedda5a] received
[2026-03-27 02:26:45,761: INFO/MainProcess] Task tasks.scrape_pending_urls[bda4eb5b-ffc5-4805-a43f-0f60fcedda5a] succeeded in 0.0032099001109600067s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:27:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[4a6c30f9-bf9f-4d29-a601-243de80d6188] received
[2026-03-27 02:27:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[4a6c30f9-bf9f-4d29-a601-243de80d6188] succeeded in 0.0036259000189602375s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:27:45,758: INFO/MainProcess] Task tasks.scrape_pending_urls[1677664c-04ee-429c-b69f-4ec1c1d915ce] received
[2026-03-27 02:27:45,761: INFO/MainProcess] Task tasks.scrape_pending_urls[1677664c-04ee-429c-b69f-4ec1c1d915ce] succeeded in 0.00317349995020777s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:28:15,758: INFO/MainProcess] Task tasks.scrape_pending_urls[c7696a54-5dc7-4580-bc40-016b32280de7] received
[2026-03-27 02:28:15,762: INFO/MainProcess] Task tasks.scrape_pending_urls[c7696a54-5dc7-4580-bc40-016b32280de7] succeeded in 0.0036319999489933252s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:28:45,758: INFO/MainProcess] Task tasks.scrape_pending_urls[d0775524-95aa-49d5-a08a-921aa5b9f394] received
[2026-03-27 02:28:45,762: INFO/MainProcess] Task tasks.scrape_pending_urls[d0775524-95aa-49d5-a08a-921aa5b9f394] succeeded in 0.00360319996252656s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:29:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[ccc06fe5-f0b5-4641-85f1-17aca658040f] received
[2026-03-27 02:29:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[ccc06fe5-f0b5-4641-85f1-17aca658040f] succeeded in 0.0034888999070972204s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:29:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[138316f0-9fa7-44fb-8991-68da682cd83d] received
[2026-03-27 02:29:46,175: INFO/MainProcess] Task tasks.collect_system_metrics[138316f0-9fa7-44fb-8991-68da682cd83d] succeeded in 0.575392400030978s: {'cpu': 13.7, 'memory': 44.6}
[2026-03-27 02:29:46,177: INFO/MainProcess] Task tasks.scrape_pending_urls[ae570b72-2cf7-48f5-b897-6b2aff2820a2] received
[2026-03-27 02:29:46,230: INFO/MainProcess] Task tasks.scrape_pending_urls[ae570b72-2cf7-48f5-b897-6b2aff2820a2] succeeded in 0.052292800042778254s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[d75e84d9-4905-4396-9e6f-4927169c7d44] received
[2026-03-27 02:30:00,005: INFO/MainProcess] Task tasks.purge_old_debug_html[d75e84d9-4905-4396-9e6f-4927169c7d44] succeeded in 0.0021339000668376684s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 02:30:15,758: INFO/MainProcess] Task tasks.scrape_pending_urls[dae26ae3-b5bd-4ca6-89cd-140b52050fd7] received
[2026-03-27 02:30:15,762: INFO/MainProcess] Task tasks.scrape_pending_urls[dae26ae3-b5bd-4ca6-89cd-140b52050fd7] succeeded in 0.0040055999998003244s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:30:45,758: INFO/MainProcess] Task tasks.scrape_pending_urls[da1202de-34a4-4219-9908-5579ef21e75a] received
[2026-03-27 02:30:45,762: INFO/MainProcess] Task tasks.scrape_pending_urls[da1202de-34a4-4219-9908-5579ef21e75a] succeeded in 0.003604099969379604s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:31:15,757: INFO/MainProcess] Task tasks.scrape_pending_urls[32fdf7d2-0d71-42c0-b57a-c8a61867cc3f] received
[2026-03-27 02:31:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[32fdf7d2-0d71-42c0-b57a-c8a61867cc3f] succeeded in 0.0034404000034555793s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:31:45,758: INFO/MainProcess] Task tasks.scrape_pending_urls[e6d75a1b-2889-450f-af48-ced9b6eaeaa1] received
[2026-03-27 02:31:45,762: INFO/MainProcess] Task tasks.scrape_pending_urls[e6d75a1b-2889-450f-af48-ced9b6eaeaa1] succeeded in 0.003454499994404614s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:32:15,760: INFO/MainProcess] Task tasks.scrape_pending_urls[a85d387f-96c7-478b-a450-6b9ec32b7c50] received
[2026-03-27 02:32:15,764: INFO/MainProcess] Task tasks.scrape_pending_urls[a85d387f-96c7-478b-a450-6b9ec32b7c50] succeeded in 0.0034235999919474125s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:32:45,761: INFO/MainProcess] Task tasks.scrape_pending_urls[1f76ca09-8703-46c8-9d2f-11469a83050c] received
[2026-03-27 02:32:45,765: INFO/MainProcess] Task tasks.scrape_pending_urls[1f76ca09-8703-46c8-9d2f-11469a83050c] succeeded in 0.00352159992326051s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:33:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[945f2df2-ceab-447d-b81d-08ac171b9ddd] received
[2026-03-27 02:33:15,764: INFO/MainProcess] Task tasks.scrape_pending_urls[945f2df2-ceab-447d-b81d-08ac171b9ddd] succeeded in 0.003460200037807226s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:33:45,761: INFO/MainProcess] Task tasks.scrape_pending_urls[59893046-a054-4d7b-80c2-aba0a6e32c22] received
[2026-03-27 02:33:45,765: INFO/MainProcess] Task tasks.scrape_pending_urls[59893046-a054-4d7b-80c2-aba0a6e32c22] succeeded in 0.003541699959896505s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:34:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[136ef2e1-7894-4f59-9b6e-8aa749db563c] received
[2026-03-27 02:34:15,764: INFO/MainProcess] Task tasks.scrape_pending_urls[136ef2e1-7894-4f59-9b6e-8aa749db563c] succeeded in 0.0034106000093743205s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:34:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[b2abf16b-857a-4487-986e-26fc49da084b] received
[2026-03-27 02:34:46,118: INFO/MainProcess] Task tasks.collect_system_metrics[b2abf16b-857a-4487-986e-26fc49da084b] succeeded in 0.5188447999535128s: {'cpu': 11.1, 'memory': 44.7}
[2026-03-27 02:34:46,120: INFO/MainProcess] Task tasks.scrape_pending_urls[937f7f99-6b9d-45da-a72d-c0b4ac5466d8] received
[2026-03-27 02:34:46,124: INFO/MainProcess] Task tasks.scrape_pending_urls[937f7f99-6b9d-45da-a72d-c0b4ac5466d8] succeeded in 0.0036857000086456537s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:35:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[75770f88-8ef9-4a02-8689-95acac1d2534] received
[2026-03-27 02:35:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[75770f88-8ef9-4a02-8689-95acac1d2534] succeeded in 0.0037850000662729144s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:35:45,761: INFO/MainProcess] Task tasks.scrape_pending_urls[20e9c948-b188-4939-ab5f-f53c2a3089bb] received
[2026-03-27 02:35:45,765: INFO/MainProcess] Task tasks.scrape_pending_urls[20e9c948-b188-4939-ab5f-f53c2a3089bb] succeeded in 0.003287400002591312s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:36:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[e9f9faeb-6a6b-44ea-866a-6dc07dffd535] received
[2026-03-27 02:36:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[e9f9faeb-6a6b-44ea-866a-6dc07dffd535] succeeded in 0.0037773000076413155s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:36:45,762: INFO/MainProcess] Task tasks.scrape_pending_urls[32c9f996-8bd1-4795-9c56-e90ff4bcc85e] received
[2026-03-27 02:36:45,766: INFO/MainProcess] Task tasks.scrape_pending_urls[32c9f996-8bd1-4795-9c56-e90ff4bcc85e] succeeded in 0.0033213000278919935s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:37:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[0cf5043c-eeb4-4a63-bc70-466288434848] received
[2026-03-27 02:37:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[0cf5043c-eeb4-4a63-bc70-466288434848] succeeded in 0.0033337000058963895s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:37:45,761: INFO/MainProcess] Task tasks.scrape_pending_urls[e184c0a7-610f-459d-8212-2663e6ba4c0f] received
[2026-03-27 02:37:45,765: INFO/MainProcess] Task tasks.scrape_pending_urls[e184c0a7-610f-459d-8212-2663e6ba4c0f] succeeded in 0.0031725000590085983s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:38:15,761: INFO/MainProcess] Task tasks.scrape_pending_urls[bcad91c6-7543-44d6-8df9-e2e09fed9f43] received
[2026-03-27 02:38:15,764: INFO/MainProcess] Task tasks.scrape_pending_urls[bcad91c6-7543-44d6-8df9-e2e09fed9f43] succeeded in 0.0033096999395638704s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:38:45,766: INFO/MainProcess] Task tasks.scrape_pending_urls[fa979c6c-b550-4684-87d6-ab2fea3796f8] received
[2026-03-27 02:38:45,769: INFO/MainProcess] Task tasks.scrape_pending_urls[fa979c6c-b550-4684-87d6-ab2fea3796f8] succeeded in 0.0035379999317228794s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:39:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[ffe4cc87-7603-4dcf-880e-1dc934c577c4] received
[2026-03-27 02:39:15,769: INFO/MainProcess] Task tasks.scrape_pending_urls[ffe4cc87-7603-4dcf-880e-1dc934c577c4] succeeded in 0.003913299995474517s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:39:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[c7c3ef7d-f75c-49c7-918d-7bc24b7f30f2] received
[2026-03-27 02:39:46,118: INFO/MainProcess] Task tasks.collect_system_metrics[c7c3ef7d-f75c-49c7-918d-7bc24b7f30f2] succeeded in 0.5190583999501541s: {'cpu': 14.1, 'memory': 44.6}
[2026-03-27 02:39:46,120: INFO/MainProcess] Task tasks.scrape_pending_urls[78c2b511-27f2-436a-9e3e-4c5301a47adf] received
[2026-03-27 02:39:46,124: INFO/MainProcess] Task tasks.scrape_pending_urls[78c2b511-27f2-436a-9e3e-4c5301a47adf] succeeded in 0.0033331000013276935s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:40:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[3b4c2fda-1591-46bc-a951-4e0fd42af90d] received
[2026-03-27 02:40:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[3b4c2fda-1591-46bc-a951-4e0fd42af90d] succeeded in 0.0032345000654459s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:40:45,766: INFO/MainProcess] Task tasks.scrape_pending_urls[0172eb7f-ef18-4b1e-8883-102c8f5c2ece] received
[2026-03-27 02:40:45,770: INFO/MainProcess] Task tasks.scrape_pending_urls[0172eb7f-ef18-4b1e-8883-102c8f5c2ece] succeeded in 0.0036551000084728003s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:41:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[aeebacef-ba7f-42e2-a9c0-68dfb0c1f0b2] received
[2026-03-27 02:41:15,769: INFO/MainProcess] Task tasks.scrape_pending_urls[aeebacef-ba7f-42e2-a9c0-68dfb0c1f0b2] succeeded in 0.0034266000147908926s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:41:45,765: INFO/MainProcess] Task tasks.scrape_pending_urls[ad109832-f079-462d-b4ce-1d833c813a7c] received
[2026-03-27 02:41:45,770: INFO/MainProcess] Task tasks.scrape_pending_urls[ad109832-f079-462d-b4ce-1d833c813a7c] succeeded in 0.003930300008505583s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:42:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[590a68d1-24f3-4389-a913-15006063c302] received
[2026-03-27 02:42:15,769: INFO/MainProcess] Task tasks.scrape_pending_urls[590a68d1-24f3-4389-a913-15006063c302] succeeded in 0.0033654000144451857s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:42:45,765: INFO/MainProcess] Task tasks.scrape_pending_urls[943fe505-2a01-4605-8816-0478c5838273] received
[2026-03-27 02:42:45,769: INFO/MainProcess] Task tasks.scrape_pending_urls[943fe505-2a01-4605-8816-0478c5838273] succeeded in 0.0030516000697389245s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:43:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[63600d83-06dd-4ff2-8a47-78575337442f] received
[2026-03-27 02:43:15,769: INFO/MainProcess] Task tasks.scrape_pending_urls[63600d83-06dd-4ff2-8a47-78575337442f] succeeded in 0.0034978999756276608s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:43:45,766: INFO/MainProcess] Task tasks.scrape_pending_urls[252dfcb5-878a-4114-97f0-41295c849256] received
[2026-03-27 02:43:45,769: INFO/MainProcess] Task tasks.scrape_pending_urls[252dfcb5-878a-4114-97f0-41295c849256] succeeded in 0.0033193000126630068s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:44:15,765: INFO/MainProcess] Task tasks.scrape_pending_urls[a20a312f-9032-4c08-9976-ce68a80f5e62] received
[2026-03-27 02:44:15,769: INFO/MainProcess] Task tasks.scrape_pending_urls[a20a312f-9032-4c08-9976-ce68a80f5e62] succeeded in 0.00335269991774112s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:44:45,598: INFO/MainProcess] Task tasks.collect_system_metrics[06b64290-8aed-4c0f-81e8-3b4d350ca8d4] received
[2026-03-27 02:44:46,116: INFO/MainProcess] Task tasks.collect_system_metrics[06b64290-8aed-4c0f-81e8-3b4d350ca8d4] succeeded in 0.5175588000565767s: {'cpu': 13.4, 'memory': 44.6}
[2026-03-27 02:44:46,119: INFO/MainProcess] Task tasks.scrape_pending_urls[8958d6c5-abb4-439d-974f-27dad876bec4] received
[2026-03-27 02:44:46,123: INFO/MainProcess] Task tasks.scrape_pending_urls[8958d6c5-abb4-439d-974f-27dad876bec4] succeeded in 0.003974399995058775s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:45:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[f81910b7-1ee4-4058-a2fa-588e74f974eb] received
[2026-03-27 02:45:15,771: INFO/MainProcess] Task tasks.scrape_pending_urls[f81910b7-1ee4-4058-a2fa-588e74f974eb] succeeded in 0.003224399988539517s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:45:45,768: INFO/MainProcess] Task tasks.scrape_pending_urls[2671fee8-311e-4418-8964-e405366d2c00] received
[2026-03-27 02:45:45,772: INFO/MainProcess] Task tasks.scrape_pending_urls[2671fee8-311e-4418-8964-e405366d2c00] succeeded in 0.0033521000295877457s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:46:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[ea6af953-0156-4a44-ac40-d5031564cae0] received
[2026-03-27 02:46:15,771: INFO/MainProcess] Task tasks.scrape_pending_urls[ea6af953-0156-4a44-ac40-d5031564cae0] succeeded in 0.0031905999640002847s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:46:45,768: INFO/MainProcess] Task tasks.scrape_pending_urls[1bded04d-cd9f-46eb-9e8a-b20fef5cacb7] received
[2026-03-27 02:46:45,772: INFO/MainProcess] Task tasks.scrape_pending_urls[1bded04d-cd9f-46eb-9e8a-b20fef5cacb7] succeeded in 0.00374399998690933s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:47:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[49318524-3d04-43b4-bfef-f6a70d4c0676] received
[2026-03-27 02:47:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[49318524-3d04-43b4-bfef-f6a70d4c0676] succeeded in 0.00330700003542006s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:47:45,768: INFO/MainProcess] Task tasks.scrape_pending_urls[22a9b04a-0574-41da-9b28-6f8a44a317b3] received
[2026-03-27 02:47:45,772: INFO/MainProcess] Task tasks.scrape_pending_urls[22a9b04a-0574-41da-9b28-6f8a44a317b3] succeeded in 0.0030366999562829733s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:48:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[17da9ccc-7689-4180-af59-f794f1d7692c] received
[2026-03-27 02:48:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[17da9ccc-7689-4180-af59-f794f1d7692c] succeeded in 0.003713299985975027s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:48:45,768: INFO/MainProcess] Task tasks.scrape_pending_urls[72e9a399-fd97-45a1-b10d-0588ddef5206] received
[2026-03-27 02:48:45,772: INFO/MainProcess] Task tasks.scrape_pending_urls[72e9a399-fd97-45a1-b10d-0588ddef5206] succeeded in 0.003029300016351044s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:49:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[242ece00-7788-4e1a-a918-2df2152080ad] received
[2026-03-27 02:49:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[242ece00-7788-4e1a-a918-2df2152080ad] succeeded in 0.0030892000067979097s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:49:45,583: INFO/MainProcess] Task tasks.reset_stale_processing_urls[5ffef8f5-8495-47c6-8c90-93400eb50b46] received
[2026-03-27 02:49:45,586: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 02:49:45,587: INFO/MainProcess] Task tasks.reset_stale_processing_urls[5ffef8f5-8495-47c6-8c90-93400eb50b46] succeeded in 0.0038137000519782305s: {'reset': 0}
[2026-03-27 02:49:45,705: INFO/MainProcess] Task tasks.collect_system_metrics[96f90393-db94-4fb9-8695-2260322b97b5] received
[2026-03-27 02:49:46,223: INFO/MainProcess] Task tasks.collect_system_metrics[96f90393-db94-4fb9-8695-2260322b97b5] succeeded in 0.5172973999287933s: {'cpu': 15.4, 'memory': 44.6}
[2026-03-27 02:49:46,225: INFO/MainProcess] Task tasks.scrape_pending_urls[a1d1178b-810d-492c-ae67-53b4c0f4baf8] received
[2026-03-27 02:49:46,229: INFO/MainProcess] Task tasks.scrape_pending_urls[a1d1178b-810d-492c-ae67-53b4c0f4baf8] succeeded in 0.003463399945758283s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:50:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[b1c915c0-51af-40af-afe0-7300e6860562] received
[2026-03-27 02:50:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[b1c915c0-51af-40af-afe0-7300e6860562] succeeded in 0.0033045999007299542s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:50:45,769: INFO/MainProcess] Task tasks.scrape_pending_urls[b10a3c73-432b-4ad1-b8ef-f932efee90ab] received
[2026-03-27 02:50:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[b10a3c73-432b-4ad1-b8ef-f932efee90ab] succeeded in 0.003432300058193505s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:51:15,768: INFO/MainProcess] Task tasks.scrape_pending_urls[c60d4f0a-efa5-4037-876c-bb023bebd6d9] received
[2026-03-27 02:51:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[c60d4f0a-efa5-4037-876c-bb023bebd6d9] succeeded in 0.0033321999944746494s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:51:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[7f4bcf5a-8606-4e0e-bf68-2d40bd5bf65c] received
[2026-03-27 02:51:45,777: INFO/MainProcess] Task tasks.scrape_pending_urls[7f4bcf5a-8606-4e0e-bf68-2d40bd5bf65c] succeeded in 0.0033421999542042613s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:52:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[4e59425f-54c4-4929-99df-b58b2520d46c] received
[2026-03-27 02:52:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[4e59425f-54c4-4929-99df-b58b2520d46c] succeeded in 0.003183300024829805s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:52:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[6f2bc240-f350-485f-96a5-f79041c01480] received
[2026-03-27 02:52:45,777: INFO/MainProcess] Task tasks.scrape_pending_urls[6f2bc240-f350-485f-96a5-f79041c01480] succeeded in 0.003410100005567074s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:53:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[8b461666-f1ca-4627-9ed7-bb56176f4102] received
[2026-03-27 02:53:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[8b461666-f1ca-4627-9ed7-bb56176f4102] succeeded in 0.003302800003439188s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:53:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[9ec76aa6-6d2c-41c1-be69-f9777404f658] received
[2026-03-27 02:53:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[9ec76aa6-6d2c-41c1-be69-f9777404f658] succeeded in 0.0030276000034064054s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:54:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[1637085b-51c5-40af-b7f3-a43d36783cf0] received
[2026-03-27 02:54:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[1637085b-51c5-40af-b7f3-a43d36783cf0] succeeded in 0.003178400103934109s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:54:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[b7ce63d2-114f-4994-82b2-1a854d0d6487] received
[2026-03-27 02:54:46,117: INFO/MainProcess] Task tasks.collect_system_metrics[b7ce63d2-114f-4994-82b2-1a854d0d6487] succeeded in 0.5180846999865025s: {'cpu': 14.5, 'memory': 44.6}
[2026-03-27 02:54:46,119: INFO/MainProcess] Task tasks.scrape_pending_urls[e9442a63-66f3-4c23-bad0-87663681cda2] received
[2026-03-27 02:54:46,123: INFO/MainProcess] Task tasks.scrape_pending_urls[e9442a63-66f3-4c23-bad0-87663681cda2] succeeded in 0.003339499933645129s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:55:15,772: INFO/MainProcess] Task tasks.scrape_pending_urls[34a0870e-2db5-401b-a383-3223d4af03ad] received
[2026-03-27 02:55:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[34a0870e-2db5-401b-a383-3223d4af03ad] succeeded in 0.0031395999249070883s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:55:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[6294b0fa-d221-47d4-92b0-c0990084c7e9] received
[2026-03-27 02:55:45,777: INFO/MainProcess] Task tasks.scrape_pending_urls[6294b0fa-d221-47d4-92b0-c0990084c7e9] succeeded in 0.0035431000869721174s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:56:15,773: INFO/MainProcess] Task tasks.scrape_pending_urls[bc69a11c-1be6-4eec-ab1d-d9f9e13df922] received
[2026-03-27 02:56:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[bc69a11c-1be6-4eec-ab1d-d9f9e13df922] succeeded in 0.0032396999886259437s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:56:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[631511c0-454f-4c10-bc4e-6b70cc0ae518] received
[2026-03-27 02:56:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[631511c0-454f-4c10-bc4e-6b70cc0ae518] succeeded in 0.003034300054423511s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:57:15,773: INFO/MainProcess] Task tasks.scrape_pending_urls[46afcc79-f699-47f2-a608-e28246f54cca] received
[2026-03-27 02:57:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[46afcc79-f699-47f2-a608-e28246f54cca] succeeded in 0.0032001000363379717s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:57:45,773: INFO/MainProcess] Task tasks.scrape_pending_urls[91e0e0fb-31ae-4242-bd24-52bc1fd04ab2] received
[2026-03-27 02:57:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[91e0e0fb-31ae-4242-bd24-52bc1fd04ab2] succeeded in 0.0030611000256612897s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:58:15,775: INFO/MainProcess] Task tasks.scrape_pending_urls[3545d48a-9294-452c-9bdb-770b19a8be68] received
[2026-03-27 02:58:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[3545d48a-9294-452c-9bdb-770b19a8be68] succeeded in 0.0030492000514641404s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:58:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[8caf6ae1-4998-463c-891e-0b971bad48cb] received
[2026-03-27 02:58:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[8caf6ae1-4998-463c-891e-0b971bad48cb] succeeded in 0.003216200042515993s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:59:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[ef957931-77d2-4c4d-9136-270e5f326886] received
[2026-03-27 02:59:15,781: INFO/MainProcess] Task tasks.scrape_pending_urls[ef957931-77d2-4c4d-9136-270e5f326886] succeeded in 0.004345599911175668s: {'status': 'idle', 'pending': 0}
[2026-03-27 02:59:45,599: INFO/MainProcess] Task tasks.collect_system_metrics[3fb1c592-3c19-4c5a-b506-2aaff1c198d7] received
[2026-03-27 02:59:46,115: INFO/MainProcess] Task tasks.collect_system_metrics[3fb1c592-3c19-4c5a-b506-2aaff1c198d7] succeeded in 0.5165132000111043s: {'cpu': 14.2, 'memory': 44.6}
[2026-03-27 02:59:46,118: INFO/MainProcess] Task tasks.scrape_pending_urls[f33c626d-0d2c-4400-8b4c-979df90c554a] received
[2026-03-27 02:59:46,121: INFO/MainProcess] Task tasks.scrape_pending_urls[f33c626d-0d2c-4400-8b4c-979df90c554a] succeeded in 0.003374999971129s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:00:15,775: INFO/MainProcess] Task tasks.scrape_pending_urls[3b015649-bf0c-48ac-9d85-892516cd13dc] received
[2026-03-27 03:00:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[3b015649-bf0c-48ac-9d85-892516cd13dc] succeeded in 0.003114399965852499s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:00:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[ed6b4d10-7050-4773-8832-f76f45b9beb5] received
[2026-03-27 03:00:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[ed6b4d10-7050-4773-8832-f76f45b9beb5] succeeded in 0.003268799977377057s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:01:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[053b71cc-0e74-4074-90cf-1fb39d320e23] received
[2026-03-27 03:01:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[053b71cc-0e74-4074-90cf-1fb39d320e23] succeeded in 0.0034464000491425395s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:01:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[12d167bd-15ad-43ac-8197-4239b96a200f] received
[2026-03-27 03:01:45,779: INFO/MainProcess] Task tasks.scrape_pending_urls[12d167bd-15ad-43ac-8197-4239b96a200f] succeeded in 0.003073300002142787s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:02:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[0bf46cdc-99a2-49e5-864c-01781c29e93e] received
[2026-03-27 03:02:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[0bf46cdc-99a2-49e5-864c-01781c29e93e] succeeded in 0.003281199955381453s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:02:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[4177babf-1e2d-43e4-85e7-edc93e3e349a] received
[2026-03-27 03:02:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[4177babf-1e2d-43e4-85e7-edc93e3e349a] succeeded in 0.0030686999671161175s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:03:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[de370060-835f-4f98-bb24-d683a1338949] received
[2026-03-27 03:03:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[de370060-835f-4f98-bb24-d683a1338949] succeeded in 0.0031615999760106206s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:03:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[f76d2171-30da-4350-bb4b-e125b693c416] received
[2026-03-27 03:03:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[f76d2171-30da-4350-bb4b-e125b693c416] succeeded in 0.0035294999834150076s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:04:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[377300e0-ab57-47fa-b887-4a5d88c8f350] received
[2026-03-27 03:04:15,780: INFO/MainProcess] Task tasks.scrape_pending_urls[377300e0-ab57-47fa-b887-4a5d88c8f350] succeeded in 0.003306100028567016s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:04:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[822ed806-fd36-4977-ac8f-b76c12ca1129] received
[2026-03-27 03:04:46,119: INFO/MainProcess] Task tasks.collect_system_metrics[822ed806-fd36-4977-ac8f-b76c12ca1129] succeeded in 0.5161466000135988s: {'cpu': 11.7, 'memory': 44.7}
[2026-03-27 03:04:46,121: INFO/MainProcess] Task tasks.scrape_pending_urls[1c713ad9-751a-4712-991f-612e31baa9a3] received
[2026-03-27 03:04:46,126: INFO/MainProcess] Task tasks.scrape_pending_urls[1c713ad9-751a-4712-991f-612e31baa9a3] succeeded in 0.004373600007966161s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:05:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[53d6e395-f50a-4825-8dd5-e651394db10c] received
[2026-03-27 03:05:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[53d6e395-f50a-4825-8dd5-e651394db10c] succeeded in 0.0033167999936267734s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:05:45,777: INFO/MainProcess] Task tasks.scrape_pending_urls[17f388a8-d5be-47be-8751-ede48fd8e760] received
[2026-03-27 03:05:45,781: INFO/MainProcess] Task tasks.scrape_pending_urls[17f388a8-d5be-47be-8751-ede48fd8e760] succeeded in 0.0034452000400051475s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:06:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[c75fc3a1-7946-4aa0-8914-a8320977c94f] received
[2026-03-27 03:06:15,780: INFO/MainProcess] Task tasks.scrape_pending_urls[c75fc3a1-7946-4aa0-8914-a8320977c94f] succeeded in 0.0031445000786334276s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:06:45,776: INFO/MainProcess] Task tasks.scrape_pending_urls[b6f43509-9025-445f-b015-dcded872f0c9] received
[2026-03-27 03:06:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[b6f43509-9025-445f-b015-dcded872f0c9] succeeded in 0.003224099986255169s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:07:15,776: INFO/MainProcess] Task tasks.scrape_pending_urls[7701d139-0712-45e8-a2df-be0340c8247f] received
[2026-03-27 03:07:15,780: INFO/MainProcess] Task tasks.scrape_pending_urls[7701d139-0712-45e8-a2df-be0340c8247f] succeeded in 0.003230300033465028s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:07:45,779: INFO/MainProcess] Task tasks.scrape_pending_urls[fe445aeb-d9ac-4041-bc80-b24acef5db3c] received
[2026-03-27 03:07:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[fe445aeb-d9ac-4041-bc80-b24acef5db3c] succeeded in 0.003433499950915575s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:08:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[ad9206d4-0b42-445c-9193-c1201184f73c] received
[2026-03-27 03:08:15,783: INFO/MainProcess] Task tasks.scrape_pending_urls[ad9206d4-0b42-445c-9193-c1201184f73c] succeeded in 0.0034100000048056245s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:08:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[1f04ca9a-c560-4259-a410-b732c88d45eb] received
[2026-03-27 03:08:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[1f04ca9a-c560-4259-a410-b732c88d45eb] succeeded in 0.003340400056913495s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:09:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[3d49470b-358f-4d06-b6a5-5c39e070e4c9] received
[2026-03-27 03:09:15,783: INFO/MainProcess] Task tasks.scrape_pending_urls[3d49470b-358f-4d06-b6a5-5c39e070e4c9] succeeded in 0.003426400013267994s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:09:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[f50d2ee8-c356-4140-861d-abacb2541325] received
[2026-03-27 03:09:46,119: INFO/MainProcess] Task tasks.collect_system_metrics[f50d2ee8-c356-4140-861d-abacb2541325] succeeded in 0.5163041000487283s: {'cpu': 16.0, 'memory': 44.7}
[2026-03-27 03:09:46,121: INFO/MainProcess] Task tasks.scrape_pending_urls[dbd470fe-97c6-4c8a-ad7b-edd20f62647e] received
[2026-03-27 03:09:46,125: INFO/MainProcess] Task tasks.scrape_pending_urls[dbd470fe-97c6-4c8a-ad7b-edd20f62647e] succeeded in 0.0033301999792456627s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:10:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[938d9619-48b5-471b-9c2d-d4498d5c2143] received
[2026-03-27 03:10:15,783: INFO/MainProcess] Task tasks.scrape_pending_urls[938d9619-48b5-471b-9c2d-d4498d5c2143] succeeded in 0.0035343999043107033s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:10:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[4ee760a1-fbb8-4d6c-9ad1-c0e83bc024a5] received
[2026-03-27 03:10:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[4ee760a1-fbb8-4d6c-9ad1-c0e83bc024a5] succeeded in 0.0035064000403508544s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:11:15,780: INFO/MainProcess] Task tasks.scrape_pending_urls[357405fb-13d2-45f5-b573-8cba9b384086] received
[2026-03-27 03:11:15,784: INFO/MainProcess] Task tasks.scrape_pending_urls[357405fb-13d2-45f5-b573-8cba9b384086] succeeded in 0.003630799939855933s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:11:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[211e2896-77f7-4443-a06d-2c4166ab02b5] received
[2026-03-27 03:11:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[211e2896-77f7-4443-a06d-2c4166ab02b5] succeeded in 0.0031372999073937535s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:12:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[92664273-03f8-42e1-9541-db8997c6a1b3] received
[2026-03-27 03:12:15,783: INFO/MainProcess] Task tasks.scrape_pending_urls[92664273-03f8-42e1-9541-db8997c6a1b3] succeeded in 0.003346199984662235s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:12:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[c48822dd-af0a-4964-afe3-fd367bc401c7] received
[2026-03-27 03:12:45,784: INFO/MainProcess] Task tasks.scrape_pending_urls[c48822dd-af0a-4964-afe3-fd367bc401c7] succeeded in 0.003356899949721992s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:13:15,779: INFO/MainProcess] Task tasks.scrape_pending_urls[6f29a98e-aef8-48e0-af8d-2bfb57c18017] received
[2026-03-27 03:13:15,783: INFO/MainProcess] Task tasks.scrape_pending_urls[6f29a98e-aef8-48e0-af8d-2bfb57c18017] succeeded in 0.0034829999785870314s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:13:45,780: INFO/MainProcess] Task tasks.scrape_pending_urls[3a6e52e8-8b88-4e16-b69b-ef3d189d8d5d] received
[2026-03-27 03:13:45,784: INFO/MainProcess] Task tasks.scrape_pending_urls[3a6e52e8-8b88-4e16-b69b-ef3d189d8d5d] succeeded in 0.0034413000103086233s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:14:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[bf1486e8-1c0b-4b76-868d-6d72e2319cf2] received
[2026-03-27 03:14:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[bf1486e8-1c0b-4b76-868d-6d72e2319cf2] succeeded in 0.003347999998368323s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:14:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[48930018-2036-445b-a3f3-69792121d0cd] received
[2026-03-27 03:14:46,121: INFO/MainProcess] Task tasks.collect_system_metrics[48930018-2036-445b-a3f3-69792121d0cd] succeeded in 0.5176659999415278s: {'cpu': 15.2, 'memory': 44.5}
[2026-03-27 03:14:46,123: INFO/MainProcess] Task tasks.scrape_pending_urls[97ecf19a-b155-4b5b-9b77-944de5f7f7db] received
[2026-03-27 03:14:46,127: INFO/MainProcess] Task tasks.scrape_pending_urls[97ecf19a-b155-4b5b-9b77-944de5f7f7db] succeeded in 0.0033997000427916646s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:15:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[b1ed27cd-aeda-4c75-b8fe-c80ca1096d72] received
[2026-03-27 03:15:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[b1ed27cd-aeda-4c75-b8fe-c80ca1096d72] succeeded in 0.0034410000080242753s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:15:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[66b39574-a8bb-447b-9184-20b63a714fb8] received
[2026-03-27 03:15:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[66b39574-a8bb-447b-9184-20b63a714fb8] succeeded in 0.0033371999161317945s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:16:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[5dc38fcf-43d6-4916-b4d6-a1a07f826216] received
[2026-03-27 03:16:15,787: INFO/MainProcess] Task tasks.scrape_pending_urls[5dc38fcf-43d6-4916-b4d6-a1a07f826216] succeeded in 0.0037400999572128057s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:16:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[b1bd4687-9a30-4191-b4c5-f064b2d1acd8] received
[2026-03-27 03:16:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[b1bd4687-9a30-4191-b4c5-f064b2d1acd8] succeeded in 0.0033458999823778868s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:17:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[c14a2ae2-5858-4ee6-b20d-b6e672a264ee] received
[2026-03-27 03:17:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[c14a2ae2-5858-4ee6-b20d-b6e672a264ee] succeeded in 0.003261400037445128s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:17:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[1c99d642-25eb-4402-accc-3ba5fc25e866] received
[2026-03-27 03:17:45,786: INFO/MainProcess] Task tasks.scrape_pending_urls[1c99d642-25eb-4402-accc-3ba5fc25e866] succeeded in 0.003236799966543913s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:18:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[42c07293-b733-4af1-9736-f61fb7aa500c] received
[2026-03-27 03:18:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[42c07293-b733-4af1-9736-f61fb7aa500c] succeeded in 0.0033440999686717987s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:18:45,783: INFO/MainProcess] Task tasks.scrape_pending_urls[679f3741-62aa-4140-9a7f-e4b939e7388e] received
[2026-03-27 03:18:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[679f3741-62aa-4140-9a7f-e4b939e7388e] succeeded in 0.003316999995149672s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:19:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[b29021c8-6b91-440d-85b4-0b39233680e0] received
[2026-03-27 03:19:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[b29021c8-6b91-440d-85b4-0b39233680e0] succeeded in 0.0034431000240147114s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:19:45,583: INFO/MainProcess] Task tasks.reset_stale_processing_urls[dcd31729-6003-4fd1-9710-f1c64b56ae86] received
[2026-03-27 03:19:45,586: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 03:19:45,587: INFO/MainProcess] Task tasks.reset_stale_processing_urls[dcd31729-6003-4fd1-9710-f1c64b56ae86] succeeded in 0.004233099985867739s: {'reset': 0}
[2026-03-27 03:19:45,602: INFO/MainProcess] Task tasks.collect_system_metrics[66734fee-13e9-4fda-bd7c-2d98ad52725d] received
[2026-03-27 03:19:46,120: INFO/MainProcess] Task tasks.collect_system_metrics[66734fee-13e9-4fda-bd7c-2d98ad52725d] succeeded in 0.5175804001046345s: {'cpu': 12.1, 'memory': 44.7}
[2026-03-27 03:19:46,122: INFO/MainProcess] Task tasks.scrape_pending_urls[df99fd9c-a896-4e36-81c6-f9f5f0bc5574] received
[2026-03-27 03:19:46,126: INFO/MainProcess] Task tasks.scrape_pending_urls[df99fd9c-a896-4e36-81c6-f9f5f0bc5574] succeeded in 0.0030126000056043267s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:20:15,782: INFO/MainProcess] Task tasks.scrape_pending_urls[391a8d6f-4b44-40b4-a3c1-9bed07ae5c75] received
[2026-03-27 03:20:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[391a8d6f-4b44-40b4-a3c1-9bed07ae5c75] succeeded in 0.0033151000970974565s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:20:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[027074d3-ddcf-40d7-a021-b233f117e4b5] received
[2026-03-27 03:20:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[027074d3-ddcf-40d7-a021-b233f117e4b5] succeeded in 0.003035800065845251s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:21:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[c0624d07-4790-4dde-8f95-2131f1f6ce25] received
[2026-03-27 03:21:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[c0624d07-4790-4dde-8f95-2131f1f6ce25] succeeded in 0.0032727000070735812s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:21:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[3e4a4bc1-b784-4c12-8eec-ea31c6fb4aba] received
[2026-03-27 03:21:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[3e4a4bc1-b784-4c12-8eec-ea31c6fb4aba] succeeded in 0.003019699943251908s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:22:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[6d08da12-3959-4c4b-9845-c92e0e7b8247] received
[2026-03-27 03:22:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[6d08da12-3959-4c4b-9845-c92e0e7b8247] succeeded in 0.003186199930496514s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:22:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[bb8e76cb-8cb7-4671-bd98-00858d77a105] received
[2026-03-27 03:22:45,854: INFO/MainProcess] Task tasks.scrape_pending_urls[bb8e76cb-8cb7-4671-bd98-00858d77a105] succeeded in 0.06701260001864284s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:23:15,787: INFO/MainProcess] Task tasks.scrape_pending_urls[3fb5506c-30b4-4a4f-88b6-9cc411c6c3f6] received
[2026-03-27 03:23:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[3fb5506c-30b4-4a4f-88b6-9cc411c6c3f6] succeeded in 0.003414600039832294s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:23:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[9857b164-8da2-434b-abac-c8197acb183b] received
[2026-03-27 03:23:45,791: INFO/MainProcess] Task tasks.scrape_pending_urls[9857b164-8da2-434b-abac-c8197acb183b] succeeded in 0.003504200023598969s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:24:15,786: INFO/MainProcess] Task tasks.scrape_pending_urls[4310b894-36f8-4ad7-b12f-636d701da3d7] received
[2026-03-27 03:24:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[4310b894-36f8-4ad7-b12f-636d701da3d7] succeeded in 0.003525999956764281s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:24:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[a500d33e-1b52-4b76-ab20-6c5ba0dfd945] received
[2026-03-27 03:24:46,120: INFO/MainProcess] Task tasks.collect_system_metrics[a500d33e-1b52-4b76-ab20-6c5ba0dfd945] succeeded in 0.5166056999005377s: {'cpu': 10.8, 'memory': 44.5}
[2026-03-27 03:24:46,122: INFO/MainProcess] Task tasks.scrape_pending_urls[b3bff411-51a6-435a-8791-70b4fef04cef] received
[2026-03-27 03:24:46,125: INFO/MainProcess] Task tasks.scrape_pending_urls[b3bff411-51a6-435a-8791-70b4fef04cef] succeeded in 0.003076000022701919s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:25:15,787: INFO/MainProcess] Task tasks.scrape_pending_urls[6743562c-736a-4589-a55e-8ab4cec3a100] received
[2026-03-27 03:25:15,791: INFO/MainProcess] Task tasks.scrape_pending_urls[6743562c-736a-4589-a55e-8ab4cec3a100] succeeded in 0.00372340006288141s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:25:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[5027f431-3d9d-4630-b984-5e42262b0e74] received
[2026-03-27 03:25:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[5027f431-3d9d-4630-b984-5e42262b0e74] succeeded in 0.003238299977965653s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:26:15,787: INFO/MainProcess] Task tasks.scrape_pending_urls[f2d499ba-01ac-42ff-ab19-8e90b087c03c] received
[2026-03-27 03:26:15,791: INFO/MainProcess] Task tasks.scrape_pending_urls[f2d499ba-01ac-42ff-ab19-8e90b087c03c] succeeded in 0.0033178998855873942s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:26:45,787: INFO/MainProcess] Task tasks.scrape_pending_urls[23cde506-4ef5-4f0f-9e61-37500b3cb88e] received
[2026-03-27 03:26:45,791: INFO/MainProcess] Task tasks.scrape_pending_urls[23cde506-4ef5-4f0f-9e61-37500b3cb88e] succeeded in 0.003636099980212748s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:27:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[9545135c-4f64-483c-8d9a-a1ed258facdd] received
[2026-03-27 03:27:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[9545135c-4f64-483c-8d9a-a1ed258facdd] succeeded in 0.0035708999494090676s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:27:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[8c030d52-fb07-4c67-bd11-af56e4b9bc0f] received
[2026-03-27 03:27:45,794: INFO/MainProcess] Task tasks.scrape_pending_urls[8c030d52-fb07-4c67-bd11-af56e4b9bc0f] succeeded in 0.003265199949964881s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:28:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[f3359dc4-45a5-41e7-b0fb-341058567746] received
[2026-03-27 03:28:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[f3359dc4-45a5-41e7-b0fb-341058567746] succeeded in 0.003499200101941824s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:28:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[593bcc68-959f-4efa-b778-c092c3d66b20] received
[2026-03-27 03:28:45,794: INFO/MainProcess] Task tasks.scrape_pending_urls[593bcc68-959f-4efa-b778-c092c3d66b20] succeeded in 0.003449499956332147s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:29:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[0848ba2f-6035-42a0-bff1-a5ecd1925a4b] received
[2026-03-27 03:29:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[0848ba2f-6035-42a0-bff1-a5ecd1925a4b] succeeded in 0.0033807000145316124s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:29:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[057decc3-b008-4961-a105-cb52eb6aada8] received
[2026-03-27 03:29:46,123: INFO/MainProcess] Task tasks.collect_system_metrics[057decc3-b008-4961-a105-cb52eb6aada8] succeeded in 0.5196276999777183s: {'cpu': 10.7, 'memory': 44.5}
[2026-03-27 03:29:46,125: INFO/MainProcess] Task tasks.scrape_pending_urls[a1e7875d-4973-4b37-a229-88afefff95d3] received
[2026-03-27 03:29:46,197: INFO/MainProcess] Task tasks.scrape_pending_urls[a1e7875d-4973-4b37-a229-88afefff95d3] succeeded in 0.07136239996179938s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[d2b2e157-d0dd-4652-9f2d-9dd1c9291943] received
[2026-03-27 03:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[d2b2e157-d0dd-4652-9f2d-9dd1c9291943] succeeded in 0.0015084999613463879s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 03:30:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[42555961-02a7-42bb-8651-9bb6abb92cf2] received
[2026-03-27 03:30:15,845: INFO/MainProcess] Task tasks.scrape_pending_urls[42555961-02a7-42bb-8651-9bb6abb92cf2] succeeded in 0.05543449998367578s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:30:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[23b3ec7d-9eeb-4690-8c6e-439434946c13] received
[2026-03-27 03:30:45,794: INFO/MainProcess] Task tasks.scrape_pending_urls[23b3ec7d-9eeb-4690-8c6e-439434946c13] succeeded in 0.0033449999755248427s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:31:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[d02d1eab-4d2c-4528-8236-08963e4efb49] received
[2026-03-27 03:31:15,795: INFO/MainProcess] Task tasks.scrape_pending_urls[d02d1eab-4d2c-4528-8236-08963e4efb49] succeeded in 0.00411300000268966s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:31:45,791: INFO/MainProcess] Task tasks.scrape_pending_urls[f4da22c3-5fd8-4599-9d08-275e4961510f] received
[2026-03-27 03:31:45,795: INFO/MainProcess] Task tasks.scrape_pending_urls[f4da22c3-5fd8-4599-9d08-275e4961510f] succeeded in 0.0036994999973103404s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:32:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[7078063f-0ce2-4468-826e-4ff806b90e25] received
[2026-03-27 03:32:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[7078063f-0ce2-4468-826e-4ff806b90e25] succeeded in 0.003421999979764223s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:32:45,790: INFO/MainProcess] Task tasks.scrape_pending_urls[60f1b61c-6554-4a64-987b-aa770ee9d0d2] received
[2026-03-27 03:32:45,794: INFO/MainProcess] Task tasks.scrape_pending_urls[60f1b61c-6554-4a64-987b-aa770ee9d0d2] succeeded in 0.0032133000204339623s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:33:15,790: INFO/MainProcess] Task tasks.scrape_pending_urls[2a99a0be-423a-44b2-b584-957ebd9121a8] received
[2026-03-27 03:33:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[2a99a0be-423a-44b2-b584-957ebd9121a8] succeeded in 0.003505400032736361s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:33:45,795: INFO/MainProcess] Task tasks.scrape_pending_urls[cf0ca96f-7f0a-4997-b195-eb958a0f99f0] received
[2026-03-27 03:33:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[cf0ca96f-7f0a-4997-b195-eb958a0f99f0] succeeded in 0.003235599957406521s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:34:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[02991f2a-53f4-45c8-95b2-71d07f8705f3] received
[2026-03-27 03:34:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[02991f2a-53f4-45c8-95b2-71d07f8705f3] succeeded in 0.003519499907270074s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:34:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[2dd11907-6b92-49f5-a74a-e0eedad27c2c] received
[2026-03-27 03:34:46,122: INFO/MainProcess] Task tasks.collect_system_metrics[2dd11907-6b92-49f5-a74a-e0eedad27c2c] succeeded in 0.518502099905163s: {'cpu': 14.7, 'memory': 44.7}
[2026-03-27 03:34:46,124: INFO/MainProcess] Task tasks.scrape_pending_urls[83ad1069-9261-45b1-b6c0-6b0b971357b5] received
[2026-03-27 03:34:46,128: INFO/MainProcess] Task tasks.scrape_pending_urls[83ad1069-9261-45b1-b6c0-6b0b971357b5] succeeded in 0.003698199987411499s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:35:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[e8b0bd38-525d-4f06-9b69-ab6e2db07c51] received
[2026-03-27 03:35:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[e8b0bd38-525d-4f06-9b69-ab6e2db07c51] succeeded in 0.003317900002002716s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:35:45,795: INFO/MainProcess] Task tasks.scrape_pending_urls[906a72f4-9d00-42a2-914d-36b5bcd770b1] received
[2026-03-27 03:35:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[906a72f4-9d00-42a2-914d-36b5bcd770b1] succeeded in 0.0033451999770477414s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:36:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[377c30bc-7783-4e85-ba4f-ad65b23552c3] received
[2026-03-27 03:36:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[377c30bc-7783-4e85-ba4f-ad65b23552c3] succeeded in 0.0034088999964296818s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:36:45,795: INFO/MainProcess] Task tasks.scrape_pending_urls[2fac992a-17b3-40f5-bcd4-0b3039b8f76b] received
[2026-03-27 03:36:45,799: INFO/MainProcess] Task tasks.scrape_pending_urls[2fac992a-17b3-40f5-bcd4-0b3039b8f76b] succeeded in 0.0035531000467017293s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:37:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[601c3cca-24c4-402f-ba20-246a2f3bf85d] received
[2026-03-27 03:37:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[601c3cca-24c4-402f-ba20-246a2f3bf85d] succeeded in 0.0036908999318256974s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:37:45,795: INFO/MainProcess] Task tasks.scrape_pending_urls[a0704670-bb4c-4a43-b3ba-8b25a742dfae] received
[2026-03-27 03:37:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[a0704670-bb4c-4a43-b3ba-8b25a742dfae] succeeded in 0.003079200047068298s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:38:15,794: INFO/MainProcess] Task tasks.scrape_pending_urls[cc3b58be-cf50-49c6-8bac-1aeb0b2d03ed] received
[2026-03-27 03:38:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[cc3b58be-cf50-49c6-8bac-1aeb0b2d03ed] succeeded in 0.0033108999487012625s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:38:45,795: INFO/MainProcess] Task tasks.scrape_pending_urls[f84eb058-faeb-4a06-bcbd-62c918113185] received
[2026-03-27 03:38:45,799: INFO/MainProcess] Task tasks.scrape_pending_urls[f84eb058-faeb-4a06-bcbd-62c918113185] succeeded in 0.0034553000004962087s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:39:15,795: INFO/MainProcess] Task tasks.scrape_pending_urls[aec2d5f0-f16e-4847-885d-4804485a6963] received
[2026-03-27 03:39:15,799: INFO/MainProcess] Task tasks.scrape_pending_urls[aec2d5f0-f16e-4847-885d-4804485a6963] succeeded in 0.0034832999808713794s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:39:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[d5696522-6d6c-470c-98b9-58dead978e1b] received
[2026-03-27 03:39:46,122: INFO/MainProcess] Task tasks.collect_system_metrics[d5696522-6d6c-470c-98b9-58dead978e1b] succeeded in 0.5188811999978498s: {'cpu': 10.8, 'memory': 44.7}
[2026-03-27 03:39:46,124: INFO/MainProcess] Task tasks.scrape_pending_urls[2d924963-4972-4094-9f37-76174e799711] received
[2026-03-27 03:39:46,129: INFO/MainProcess] Task tasks.scrape_pending_urls[2d924963-4972-4094-9f37-76174e799711] succeeded in 0.0038029999705031514s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:40:15,797: INFO/MainProcess] Task tasks.scrape_pending_urls[1a240f8c-2cae-40a2-ba21-7ddbd0adca33] received
[2026-03-27 03:40:15,801: INFO/MainProcess] Task tasks.scrape_pending_urls[1a240f8c-2cae-40a2-ba21-7ddbd0adca33] succeeded in 0.0031110000563785434s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:40:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[314b73c9-4c61-4af3-b590-799e3e838cad] received
[2026-03-27 03:40:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[314b73c9-4c61-4af3-b590-799e3e838cad] succeeded in 0.003363099996931851s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:41:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[58e1ab2c-8d49-4583-878f-df4a00781c8d] received
[2026-03-27 03:41:15,803: INFO/MainProcess] Task tasks.scrape_pending_urls[58e1ab2c-8d49-4583-878f-df4a00781c8d] succeeded in 0.003919400041922927s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:41:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[c6f01cb1-6e8a-4ce0-b65e-41901b3e3d1b] received
[2026-03-27 03:41:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[c6f01cb1-6e8a-4ce0-b65e-41901b3e3d1b] succeeded in 0.0034283000277355313s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:42:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[742ef83c-496d-4d9f-ab60-b80a3f510412] received
[2026-03-27 03:42:15,803: INFO/MainProcess] Task tasks.scrape_pending_urls[742ef83c-496d-4d9f-ab60-b80a3f510412] succeeded in 0.0039635999128222466s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:42:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[17bf84e5-2a5b-406c-9233-112a6ab73129] received
[2026-03-27 03:42:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[17bf84e5-2a5b-406c-9233-112a6ab73129] succeeded in 0.0034410000080242753s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:43:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[86c1e08e-bf65-4216-9b5d-4b8335f9cc91] received
[2026-03-27 03:43:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[86c1e08e-bf65-4216-9b5d-4b8335f9cc91] succeeded in 0.0033289999701082706s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:43:45,799: INFO/MainProcess] Task tasks.scrape_pending_urls[37a7a69a-a56e-4fa6-b265-3d78de18c6b0] received
[2026-03-27 03:43:45,803: INFO/MainProcess] Task tasks.scrape_pending_urls[37a7a69a-a56e-4fa6-b265-3d78de18c6b0] succeeded in 0.0033528999192640185s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:44:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[1f34a7be-b8ef-4604-b73a-25f6fd33e7f1] received
[2026-03-27 03:44:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[1f34a7be-b8ef-4604-b73a-25f6fd33e7f1] succeeded in 0.0033686000388115644s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:44:45,603: INFO/MainProcess] Task tasks.collect_system_metrics[9f7a3682-8489-4744-908a-e9b2f42f317d] received
[2026-03-27 03:44:46,120: INFO/MainProcess] Task tasks.collect_system_metrics[9f7a3682-8489-4744-908a-e9b2f42f317d] succeeded in 0.5166627999860793s: {'cpu': 17.6, 'memory': 44.6}
[2026-03-27 03:44:46,122: INFO/MainProcess] Task tasks.scrape_pending_urls[7c01ad70-5eb9-4e66-adbd-cc1ced3b829c] received
[2026-03-27 03:44:46,126: INFO/MainProcess] Task tasks.scrape_pending_urls[7c01ad70-5eb9-4e66-adbd-cc1ced3b829c] succeeded in 0.003397700027562678s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:45:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[5073bb47-1435-435c-b844-5e94fbcda0d2] received
[2026-03-27 03:45:15,801: INFO/MainProcess] Task tasks.scrape_pending_urls[5073bb47-1435-435c-b844-5e94fbcda0d2] succeeded in 0.0031313999788835645s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:45:45,798: INFO/MainProcess] Task tasks.scrape_pending_urls[187ef0b3-a8ea-4423-8b5b-a00558d5e047] received
[2026-03-27 03:45:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[187ef0b3-a8ea-4423-8b5b-a00558d5e047] succeeded in 0.0033388000447303057s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:46:15,798: INFO/MainProcess] Task tasks.scrape_pending_urls[72ad12ea-4c16-456b-bfae-83fd5e379905] received
[2026-03-27 03:46:15,819: INFO/MainProcess] Task tasks.scrape_pending_urls[72ad12ea-4c16-456b-bfae-83fd5e379905] succeeded in 0.020858900039456785s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:46:45,803: INFO/MainProcess] Task tasks.scrape_pending_urls[d9648338-c70d-4078-b0e8-3da0d4a49bfe] received
[2026-03-27 03:46:45,806: INFO/MainProcess] Task tasks.scrape_pending_urls[d9648338-c70d-4078-b0e8-3da0d4a49bfe] succeeded in 0.00330400001257658s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:47:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[d36519f9-6964-42bb-95e8-e990de5a24c5] received
[2026-03-27 03:47:15,805: INFO/MainProcess] Task tasks.scrape_pending_urls[d36519f9-6964-42bb-95e8-e990de5a24c5] succeeded in 0.003078300040215254s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:47:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[aad87c50-d115-406c-8392-c68b3d9a0958] received
[2026-03-27 03:47:45,806: INFO/MainProcess] Task tasks.scrape_pending_urls[aad87c50-d115-406c-8392-c68b3d9a0958] succeeded in 0.0033432000782340765s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:48:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[b10cc40a-2e5e-4d1a-b917-182ffa1fbba7] received
[2026-03-27 03:48:15,806: INFO/MainProcess] Task tasks.scrape_pending_urls[b10cc40a-2e5e-4d1a-b917-182ffa1fbba7] succeeded in 0.003384699928574264s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:48:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[9c646906-701a-44ed-993f-bcbd8dbec24a] received
[2026-03-27 03:48:45,806: INFO/MainProcess] Task tasks.scrape_pending_urls[9c646906-701a-44ed-993f-bcbd8dbec24a] succeeded in 0.003024499979801476s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:49:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[26c9eb94-169b-4124-aaf0-5da46aadc511] received
[2026-03-27 03:49:15,806: INFO/MainProcess] Task tasks.scrape_pending_urls[26c9eb94-169b-4124-aaf0-5da46aadc511] succeeded in 0.0033522999146953225s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:49:45,582: INFO/MainProcess] Task tasks.reset_stale_processing_urls[3c473c84-58d2-45ee-a27c-a355953c42bc] received
[2026-03-27 03:49:45,586: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-27 03:49:45,587: INFO/MainProcess] Task tasks.reset_stale_processing_urls[3c473c84-58d2-45ee-a27c-a355953c42bc] succeeded in 0.004026600043289363s: {'reset': 0}
[2026-03-27 03:49:45,704: INFO/MainProcess] Task tasks.collect_system_metrics[754d374f-10b4-410b-b834-f2430edc8a60] received
[2026-03-27 03:49:46,222: INFO/MainProcess] Task tasks.collect_system_metrics[754d374f-10b4-410b-b834-f2430edc8a60] succeeded in 0.5174965000478551s: {'cpu': 13.6, 'memory': 44.7}
[2026-03-27 03:49:46,225: INFO/MainProcess] Task tasks.scrape_pending_urls[898d8dbc-877e-4c33-848d-7933759c67f1] received
[2026-03-27 03:49:46,228: INFO/MainProcess] Task tasks.scrape_pending_urls[898d8dbc-877e-4c33-848d-7933759c67f1] succeeded in 0.003214700031094253s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:50:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[6f6ad9b4-9225-4dc2-ab6e-2196ddf4cb38] received
[2026-03-27 03:50:15,806: INFO/MainProcess] Task tasks.scrape_pending_urls[6f6ad9b4-9225-4dc2-ab6e-2196ddf4cb38] succeeded in 0.003387399949133396s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:50:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[564706cf-73ec-430f-9d7d-5ec023928d68] received
[2026-03-27 03:50:45,806: INFO/MainProcess] Task tasks.scrape_pending_urls[564706cf-73ec-430f-9d7d-5ec023928d68] succeeded in 0.003061800030991435s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:51:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[529ae165-2c58-40f8-9399-ae6cfb5b28a6] received
[2026-03-27 03:51:15,807: INFO/MainProcess] Task tasks.scrape_pending_urls[529ae165-2c58-40f8-9399-ae6cfb5b28a6] succeeded in 0.003941999981179833s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:51:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[747a3938-04d0-4723-a902-d2920cb2dde4] received
[2026-03-27 03:51:45,806: INFO/MainProcess] Task tasks.scrape_pending_urls[747a3938-04d0-4723-a902-d2920cb2dde4] succeeded in 0.003028700011782348s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:52:15,802: INFO/MainProcess] Task tasks.scrape_pending_urls[0a4f888a-4b1d-4eb0-9618-bf0ff9c32edc] received
[2026-03-27 03:52:15,806: INFO/MainProcess] Task tasks.scrape_pending_urls[0a4f888a-4b1d-4eb0-9618-bf0ff9c32edc] succeeded in 0.003243299899622798s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:52:45,802: INFO/MainProcess] Task tasks.scrape_pending_urls[eb866d8e-63f7-46af-a2ab-e71cd0c26057] received
[2026-03-27 03:52:45,807: INFO/MainProcess] Task tasks.scrape_pending_urls[eb866d8e-63f7-46af-a2ab-e71cd0c26057] succeeded in 0.0038841000059619546s: {'status': 'idle', 'pending': 0}
[2026-03-27 03:53:15,805: INFO/MainProcess] Task tasks.scrape_pending_urls[4ca26fc6-5bdc-41a3-af6e-e5efe09fcafc] received
[2026-03-27 03:53:15,809: INFO/MainProcess] Task tasks.scrape_pending_urls[4ca26fc6-5bdc-41a3-af6e-e5efe09fcafc] succeeded in 0.003893899964168668s: {'status': 'idle', 'pending': 0}
