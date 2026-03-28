
===  BookingScraper Celery Worker  ===


 -------------- worker@HOUSE v5.4.0 (opalescent)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0 2026-03-27 16:49:20
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         bookingscraper:0x174b344d2b0
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

[2026-03-27 16:49:22,983: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-27 16:49:25,022: INFO/MainProcess] mingle: searching for neighbors
[2026-03-27 16:49:32,158: INFO/MainProcess] mingle: all alone
[2026-03-27 16:49:42,372: INFO/MainProcess] worker@HOUSE ready.
[2026-03-27 16:49:42,375: INFO/MainProcess] Task tasks.scrape_pending_urls[5e15f171-c1d0-4a81-8258-f7b25170aff5] received
[2026-03-27 16:49:44,578: INFO/MainProcess] Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5
[2026-03-27 16:49:44,700: INFO/MainProcess] Task tasks.scrape_pending_urls[5e15f171-c1d0-4a81-8258-f7b25170aff5] succeeded in 2.3244549999944866s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:49:52,777: INFO/MainProcess] Task tasks.scrape_pending_urls[715adeb4-23b5-4faf-9e65-e5b8e3908f98] received
[2026-03-27 16:49:52,781: INFO/MainProcess] Task tasks.scrape_pending_urls[715adeb4-23b5-4faf-9e65-e5b8e3908f98] succeeded in 0.0037247000727802515s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:50:22,778: INFO/MainProcess] Task tasks.scrape_pending_urls[428074ce-e7ee-44af-9d29-23093150ef4f] received
[2026-03-27 16:50:22,782: INFO/MainProcess] Task tasks.scrape_pending_urls[428074ce-e7ee-44af-9d29-23093150ef4f] succeeded in 0.003585300059057772s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:50:52,777: INFO/MainProcess] Task tasks.scrape_pending_urls[5b85c2af-e8e0-48cf-a103-e1ca3fbeac50] received
[2026-03-27 16:50:52,781: INFO/MainProcess] Task tasks.scrape_pending_urls[5b85c2af-e8e0-48cf-a103-e1ca3fbeac50] succeeded in 0.0035788000095635653s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:51:22,778: INFO/MainProcess] Task tasks.scrape_pending_urls[966ff33c-4cd5-41ff-959f-3ca241a5a7f2] received
[2026-03-27 16:51:22,782: INFO/MainProcess] Task tasks.scrape_pending_urls[966ff33c-4cd5-41ff-959f-3ca241a5a7f2] succeeded in 0.003894199966453016s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:51:52,778: INFO/MainProcess] Task tasks.scrape_pending_urls[a7a3c569-4f8d-4b73-ab35-07ebc005d1d1] received
[2026-03-27 16:51:52,782: INFO/MainProcess] Task tasks.scrape_pending_urls[a7a3c569-4f8d-4b73-ab35-07ebc005d1d1] succeeded in 0.004434100002981722s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:52:22,778: INFO/MainProcess] Task tasks.scrape_pending_urls[90505e90-44a9-45fc-88fd-2f249ab8766c] received
[2026-03-27 16:52:22,782: INFO/MainProcess] Task tasks.scrape_pending_urls[90505e90-44a9-45fc-88fd-2f249ab8766c] succeeded in 0.0036146000493317842s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:52:52,782: INFO/MainProcess] Task tasks.scrape_pending_urls[4a67bb87-9d22-4ddf-bd84-4e9166c3c036] received
[2026-03-27 16:52:52,789: INFO/MainProcess] Task tasks.scrape_pending_urls[4a67bb87-9d22-4ddf-bd84-4e9166c3c036] succeeded in 0.005625099991448224s: {'status': 'idle', 'pending': 0}
[2026-03-27 16:53:22,316: INFO/MainProcess] Task tasks.collect_system_metrics[474c46c7-612a-49e6-bf74-f76cb1f78d75] received
[2026-03-27 16:53:22,833: INFO/MainProcess] Task tasks.collect_system_metrics[474c46c7-612a-49e6-bf74-f76cb1f78d75] succeeded in 0.5169332000659779s: {'cpu': 12.0, 'memory': 46.8}
[2026-03-27 16:53:22,835: INFO/MainProcess] Task tasks.scrape_pending_urls[6f8231c3-0d56-498d-99ae-8440f5f50a2b] received
[2026-03-27 16:53:24,863: INFO/MainProcess] scrape_pending_urls: starting auto-batch, pending=13
[2026-03-27 16:53:25,808: INFO/MainProcess] VPN: original IP = 194.34.233.20
[2026-03-27 16:53:26,860: INFO/MainProcess] VPN: home country detected = IT
[2026-03-27 16:53:26,861: INFO/MainProcess] NordVPNManager initialised | interactive=False | original_ip=194.34.233.20 | home_country=IT
[2026-03-27 16:53:26,861: INFO/MainProcess] ScraperService INIT | VPN_ENABLED=True | HEADLESS_BROWSER=False | workers=2 | languages=en,es,de,it,fr,pt | vpn_interval=50s | vpn_countries=Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden
[2026-03-27 16:53:26,896: INFO/MainProcess] VPN: excluding home country IT from pool — remaining: ES,DE,FR,NL,CA,SE
[2026-03-27 16:53:26,896: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-27 16:53:47,878: INFO/MainProcess] VPN connected to Sweden — IP: 193.46.242.66
[2026-03-27 16:53:47,879: INFO/MainProcess] VPN connected OK before batch start.
[2026-03-27 16:53:47,880: INFO/MainProcess] Dispatching batch: urls=13 workers=2
[2026-03-27 16:53:47,881: INFO/MainProcess] Redis connection pool created: max_connections=20
[2026-03-27 16:53:52,970: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:53:52,975: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:02,484: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:03,646: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:07,213: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:07,863: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:15,954: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:17,091: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:22,631: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:23,298: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:33,022: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:33,023: INFO/MainProcess] CloudScraper failed for a2f386b2-21a2-424f-9467-6f6b72d6e482/en — trying Selenium.
[2026-03-27 16:54:33,719: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-27 16:54:33,720: INFO/MainProcess] CloudScraper failed for d15e1aa5-32b2-4451-99fd-8a80e3c301d1/en — trying Selenium.
[2026-03-27 16:54:36,301: INFO/MainProcess] Selenium: Brave started
[2026-03-27 16:57:18,803: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 16:57:21,400: INFO/MainProcess] Gallery: 131 images loaded after scroll
[2026-03-27 16:57:25,161: INFO/MainProcess] Gallery: 138 unique image URLs extracted
[2026-03-27 16:57:25,291: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 16:57:25,292: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 16:57:53,423: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for a2f386b2-21a2-424f-9467-6f6b72d6e482
[2026-03-27 16:58:07,797: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 15daa759-5ff1-4ece-a7e1-cda9e5528eca
[2026-03-27 16:58:07,798: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 15daa759-5ff1-4ece-a7e1-cda9e5528eca
[2026-03-27 16:58:07,804: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482 lang=en: SUCCESS
[2026-03-27 16:58:10,569: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-27 16:58:23,211: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-27 16:58:27,913: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-27 16:58:40,386: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-27 16:58:46,613: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-27 16:58:58,872: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-27 16:58:58,872: INFO/MainProcess] CloudScraper failed for a2f386b2-21a2-424f-9467-6f6b72d6e482/es — trying Selenium.
[2026-03-27 17:00:13,701: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 17:00:15,662: INFO/MainProcess] Gallery: 137 images loaded after scroll
[2026-03-27 17:00:19,218: INFO/MainProcess] Gallery: 144 unique image URLs extracted
[2026-03-27 17:00:19,363: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 17:00:19,364: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 17:00:42,938: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for d15e1aa5-32b2-4451-99fd-8a80e3c301d1
[2026-03-27 17:00:53,204: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 0736cf08-e6ee-4969-ae96-d62011258065
[2026-03-27 17:00:53,205: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 0736cf08-e6ee-4969-ae96-d62011258065
[2026-03-27 17:00:53,219: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1 lang=en: SUCCESS
[2026-03-27 17:00:55,949: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-27 17:01:07,830: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-27 17:01:12,575: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-27 17:01:43,117: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-27 17:01:49,337: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-27 17:01:57,908: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-27 17:01:57,908: INFO/MainProcess] CloudScraper failed for d15e1aa5-32b2-4451-99fd-8a80e3c301d1/es — trying Selenium.
[2026-03-27 17:02:00,719: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482 lang=es: SUCCESS
[2026-03-27 17:02:03,471: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-27 17:02:24,738: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-27 17:02:29,585: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-27 17:02:37,993: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-27 17:02:44,198: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-27 17:03:06,966: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-27 17:03:06,967: INFO/MainProcess] CloudScraper failed for a2f386b2-21a2-424f-9467-6f6b72d6e482/de — trying Selenium.
[2026-03-27 17:03:19,063: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1 lang=es: SUCCESS
[2026-03-27 17:03:21,913: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-27 17:03:31,798: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-27 17:03:36,957: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-27 17:03:49,380: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-27 17:03:55,596: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-27 17:04:05,372: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-27 17:04:05,373: INFO/MainProcess] CloudScraper failed for d15e1aa5-32b2-4451-99fd-8a80e3c301d1/de — trying Selenium.
[2026-03-27 17:04:37,247: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482 lang=de: SUCCESS
[2026-03-27 17:04:40,054: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-27 17:04:49,099: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-27 17:04:53,881: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-27 17:05:05,137: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-27 17:05:11,339: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-27 17:05:25,028: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-27 17:05:25,028: INFO/MainProcess] CloudScraper failed for a2f386b2-21a2-424f-9467-6f6b72d6e482/it — trying Selenium.
[2026-03-27 17:06:11,076: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1 lang=de: SUCCESS
[2026-03-27 17:06:13,884: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-27 17:06:24,006: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-27 17:06:28,759: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-27 17:06:40,700: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-27 17:06:46,910: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-27 17:06:57,152: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-27 17:06:57,152: INFO/MainProcess] CloudScraper failed for d15e1aa5-32b2-4451-99fd-8a80e3c301d1/it — trying Selenium.
[2026-03-27 17:07:29,976: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482 lang=it: SUCCESS
[2026-03-27 17:07:32,706: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-27 17:07:42,500: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-27 17:07:47,249: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-27 17:08:00,107: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-27 17:08:06,317: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-27 17:08:32,481: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-27 17:08:32,481: INFO/MainProcess] CloudScraper failed for a2f386b2-21a2-424f-9467-6f6b72d6e482/fr — trying Selenium.
[2026-03-27 17:08:48,077: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1 lang=it: SUCCESS
[2026-03-27 17:08:50,899: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-27 17:09:05,924: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-27 17:09:10,789: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-27 17:09:23,365: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-27 17:09:29,581: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-27 17:09:38,843: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-27 17:09:38,843: INFO/MainProcess] CloudScraper failed for d15e1aa5-32b2-4451-99fd-8a80e3c301d1/fr — trying Selenium.
[2026-03-27 17:10:06,980: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482 lang=fr: SUCCESS
[2026-03-27 17:10:09,812: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:10:22,127: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:10:37,274: WARNING/MainProcess] CloudScraper attempt 2/3 failed: [ConnectionError] HTTPSConnectionPool(host='www.booking.com', port=443): Max retries exceeded with url: /hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt (Caused by NameResolutionError("HTTPSConnection(host='www.booking.com', port=443): Failed to resolve 'www.booking.com' ([Errno 11001] getaddrinfo failed)"))
[2026-03-27 17:10:41,338: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:10:48,184: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:11:02,354: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:11:02,354: INFO/MainProcess] CloudScraper failed for a2f386b2-21a2-424f-9467-6f6b72d6e482/pt — trying Selenium.
[2026-03-27 17:11:46,185: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1 lang=fr: SUCCESS
[2026-03-27 17:11:49,127: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:11:59,469: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:12:04,291: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:12:17,020: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:12:23,249: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:12:36,383: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-27 17:12:36,384: INFO/MainProcess] CloudScraper failed for d15e1aa5-32b2-4451-99fd-8a80e3c301d1/pt — trying Selenium.
[2026-03-27 17:13:03,418: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482 lang=pt: SUCCESS
[2026-03-27 17:13:03,421: INFO/MainProcess] URL a2f386b2-21a2-424f-9467-6f6b72d6e482: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 17:13:06,344: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-27 17:13:16,168: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-27 17:13:21,022: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-27 17:13:29,054: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-27 17:13:35,260: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-27 17:13:49,821: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-27 17:13:49,822: INFO/MainProcess] CloudScraper failed for 653550be-6f27-44b3-9c40-6ae08a9d3d90/en — trying Selenium.
[2026-03-27 17:14:23,034: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1 lang=pt: SUCCESS
[2026-03-27 17:14:23,036: INFO/MainProcess] URL d15e1aa5-32b2-4451-99fd-8a80e3c301d1: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 17:14:25,866: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-27 17:14:35,894: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-27 17:14:40,695: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-27 17:15:09,603: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-27 17:15:15,826: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-27 17:15:23,918: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-27 17:15:23,918: INFO/MainProcess] CloudScraper failed for 26796e26-40b0-4144-8802-ece475addb04/en — trying Selenium.
[2026-03-27 17:16:44,454: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 17:16:46,394: INFO/MainProcess] Gallery: 87 images loaded after scroll
[2026-03-27 17:16:48,579: INFO/MainProcess] Gallery: 94 unique image URLs extracted
[2026-03-27 17:16:48,706: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 17:16:48,706: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 17:17:16,977: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 653550be-6f27-44b3-9c40-6ae08a9d3d90
[2026-03-27 17:17:33,730: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 74b28923-248e-45c5-bd7c-39ae53908209
[2026-03-27 17:17:33,731: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 74b28923-248e-45c5-bd7c-39ae53908209
[2026-03-27 17:17:33,736: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90 lang=en: SUCCESS
[2026-03-27 17:17:36,608: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-27 17:17:45,839: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-27 17:17:50,772: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-27 17:18:01,488: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-27 17:18:07,702: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-27 17:18:21,318: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-27 17:18:21,318: INFO/MainProcess] CloudScraper failed for 653550be-6f27-44b3-9c40-6ae08a9d3d90/es — trying Selenium.
[2026-03-27 17:19:39,056: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 17:19:41,886: INFO/MainProcess] Gallery: 266 images loaded after scroll
[2026-03-27 17:19:47,204: INFO/MainProcess] Gallery: 273 unique image URLs extracted
[2026-03-27 17:19:47,391: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 17:19:47,392: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 17:20:15,007: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 26796e26-40b0-4144-8802-ece475addb04
[2026-03-27 17:20:27,091: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 516b0641-24d1-4475-a76d-ed31e412fc77
[2026-03-27 17:20:27,091: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 516b0641-24d1-4475-a76d-ed31e412fc77
[2026-03-27 17:20:27,101: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04 lang=en: SUCCESS
[2026-03-27 17:20:30,260: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-27 17:20:39,259: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-27 17:20:44,094: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-27 17:20:53,196: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-27 17:20:59,411: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-27 17:21:12,545: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-27 17:21:12,545: INFO/MainProcess] CloudScraper failed for 26796e26-40b0-4144-8802-ece475addb04/es — trying Selenium.
[2026-03-27 17:21:32,214: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90 lang=es: SUCCESS
[2026-03-27 17:21:35,229: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-27 17:21:48,456: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-27 17:21:53,268: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-27 17:22:26,919: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-27 17:22:33,096: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-27 17:22:50,624: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04 lang=es: SUCCESS
[2026-03-27 17:22:53,441: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-27 17:23:09,331: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-27 17:23:09,331: INFO/MainProcess] CloudScraper failed for 653550be-6f27-44b3-9c40-6ae08a9d3d90/de — trying Selenium.
[2026-03-27 17:23:31,104: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-27 17:23:35,911: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-27 17:23:48,227: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-27 17:23:54,426: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-27 17:24:08,840: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-27 17:24:08,841: INFO/MainProcess] CloudScraper failed for 26796e26-40b0-4144-8802-ece475addb04/de — trying Selenium.
[2026-03-27 17:24:27,039: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90 lang=de: SUCCESS
[2026-03-27 17:24:29,943: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-27 17:25:00,142: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-27 17:25:05,065: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-27 17:25:15,407: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-27 17:25:21,621: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-27 17:25:35,794: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-27 17:25:35,794: INFO/MainProcess] CloudScraper failed for 653550be-6f27-44b3-9c40-6ae08a9d3d90/it — trying Selenium.
[2026-03-27 17:25:44,560: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04 lang=de: SUCCESS
[2026-03-27 17:25:47,326: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-27 17:26:00,329: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-27 17:26:05,215: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-27 17:26:16,673: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-27 17:26:22,890: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-27 17:26:31,757: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-27 17:26:31,757: INFO/MainProcess] CloudScraper failed for 26796e26-40b0-4144-8802-ece475addb04/it — trying Selenium.
[2026-03-27 17:27:03,470: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90 lang=it: SUCCESS
[2026-03-27 17:27:06,238: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-27 17:27:28,900: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-27 17:27:33,912: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-27 17:27:44,868: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-27 17:27:51,092: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-27 17:28:04,845: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-27 17:28:04,845: INFO/MainProcess] CloudScraper failed for 653550be-6f27-44b3-9c40-6ae08a9d3d90/fr — trying Selenium.
[2026-03-27 17:28:37,139: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04 lang=it: SUCCESS
[2026-03-27 17:28:40,001: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-27 17:28:54,239: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-27 17:28:59,008: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-27 17:29:11,039: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-27 17:29:17,304: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-27 17:29:26,819: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-27 17:29:26,820: INFO/MainProcess] CloudScraper failed for 26796e26-40b0-4144-8802-ece475addb04/fr — trying Selenium.
[2026-03-27 17:29:56,209: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90 lang=fr: SUCCESS
[2026-03-27 17:29:59,048: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:30:12,975: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:30:17,823: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:30:32,740: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:30:38,959: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:30:47,413: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:30:47,413: INFO/MainProcess] CloudScraper failed for 653550be-6f27-44b3-9c40-6ae08a9d3d90/pt — trying Selenium.
[2026-03-27 17:31:13,651: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04 lang=fr: SUCCESS
[2026-03-27 17:31:16,563: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-27 17:31:30,539: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-27 17:31:35,854: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-27 17:31:47,117: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-27 17:31:53,353: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-27 17:32:02,528: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-27 17:32:02,528: INFO/MainProcess] CloudScraper failed for 26796e26-40b0-4144-8802-ece475addb04/pt — trying Selenium.
[2026-03-27 17:32:31,367: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90 lang=pt: SUCCESS
[2026-03-27 17:32:31,369: INFO/MainProcess] URL 653550be-6f27-44b3-9c40-6ae08a9d3d90: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 17:32:34,281: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-27 17:32:42,878: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-27 17:32:47,634: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-27 17:32:58,195: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-27 17:33:04,393: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-27 17:33:14,893: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-27 17:33:14,893: INFO/MainProcess] CloudScraper failed for e5ec6178-a48d-46d3-9165-0dcd4f668629/en — trying Selenium.
[2026-03-27 17:34:04,070: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04 lang=pt: SUCCESS
[2026-03-27 17:34:04,073: INFO/MainProcess] URL 26796e26-40b0-4144-8802-ece475addb04: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 17:34:06,887: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-27 17:34:29,717: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-27 17:34:34,497: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-27 17:34:44,615: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-27 17:34:50,832: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-27 17:35:19,268: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-27 17:35:19,270: INFO/MainProcess] CloudScraper failed for 10f37dfd-108d-459a-b890-167f81bbe196/en — trying Selenium.
[2026-03-27 17:36:26,552: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 17:36:28,624: INFO/MainProcess] Gallery: 118 images loaded after scroll
[2026-03-27 17:36:32,314: INFO/MainProcess] Gallery: 125 unique image URLs extracted
[2026-03-27 17:36:32,499: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 17:36:32,500: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 17:37:01,191: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for e5ec6178-a48d-46d3-9165-0dcd4f668629
[2026-03-27 17:37:12,824: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel d6be7154-28e6-45e7-ac65-77e08bc85dc3
[2026-03-27 17:37:12,824: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel d6be7154-28e6-45e7-ac65-77e08bc85dc3
[2026-03-27 17:37:12,829: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629 lang=en: SUCCESS
[2026-03-27 17:37:15,716: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-27 17:37:29,855: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-27 17:37:35,370: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-27 17:37:45,555: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-27 17:37:51,768: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-27 17:38:02,163: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-27 17:38:02,163: INFO/MainProcess] CloudScraper failed for e5ec6178-a48d-46d3-9165-0dcd4f668629/es — trying Selenium.
[2026-03-27 17:39:23,518: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 17:39:25,408: INFO/MainProcess] Gallery: 24 images loaded after scroll
[2026-03-27 17:39:26,542: INFO/MainProcess] Gallery: 31 unique image URLs extracted
[2026-03-27 17:39:26,675: INFO/MainProcess] hotelPhotos JS: 24 photos extracted from page source
[2026-03-27 17:39:26,676: INFO/MainProcess] Gallery: 24 photos with full metadata (hotelPhotos JS)
[2026-03-27 17:39:53,812: INFO/MainProcess] Photos: 24 rich photo records (hotelPhotos JS) for 10f37dfd-108d-459a-b890-167f81bbe196
[2026-03-27 17:39:59,260: INFO/MainProcess] download_photo_batch: 72/72 photo-files saved for hotel aebf2ebd-fee0-4c9a-9e7a-e900c8ed1c99
[2026-03-27 17:39:59,261: INFO/MainProcess] ImageDownloader (photo_batch): 72/24 photos saved for hotel aebf2ebd-fee0-4c9a-9e7a-e900c8ed1c99
[2026-03-27 17:39:59,267: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196 lang=en: SUCCESS
[2026-03-27 17:40:02,446: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-27 17:40:16,353: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-27 17:40:21,124: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-27 17:40:57,122: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-27 17:41:03,321: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-27 17:41:13,107: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629 lang=es: SUCCESS
[2026-03-27 17:41:15,964: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-27 17:41:16,299: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-27 17:41:16,299: INFO/MainProcess] CloudScraper failed for 10f37dfd-108d-459a-b890-167f81bbe196/es — trying Selenium.
[2026-03-27 17:41:24,370: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-27 17:41:29,370: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-27 17:41:37,595: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-27 17:41:43,794: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-27 17:41:57,755: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-27 17:41:57,755: INFO/MainProcess] CloudScraper failed for e5ec6178-a48d-46d3-9165-0dcd4f668629/de — trying Selenium.
[2026-03-27 17:42:35,106: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196 lang=es: SUCCESS
[2026-03-27 17:42:37,825: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-27 17:42:46,464: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-27 17:42:52,196: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-27 17:43:03,724: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-27 17:43:09,936: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-27 17:43:23,941: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-27 17:43:23,941: INFO/MainProcess] CloudScraper failed for 10f37dfd-108d-459a-b890-167f81bbe196/de — trying Selenium.
[2026-03-27 17:43:53,884: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629 lang=de: SUCCESS
[2026-03-27 17:43:56,660: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-27 17:44:10,244: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-27 17:44:15,165: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-27 17:44:27,278: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-27 17:44:33,491: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-27 17:44:41,577: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-27 17:44:41,577: INFO/MainProcess] CloudScraper failed for e5ec6178-a48d-46d3-9165-0dcd4f668629/it — trying Selenium.
[2026-03-27 17:45:28,966: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196 lang=de: SUCCESS
[2026-03-27 17:45:31,684: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-27 17:45:46,665: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-27 17:45:51,604: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-27 17:46:05,072: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-27 17:46:11,276: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-27 17:46:21,131: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-27 17:46:21,131: INFO/MainProcess] CloudScraper failed for 10f37dfd-108d-459a-b890-167f81bbe196/it — trying Selenium.
[2026-03-27 17:46:47,611: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629 lang=it: SUCCESS
[2026-03-27 17:46:50,614: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-27 17:47:01,035: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-27 17:47:05,729: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-27 17:47:17,533: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-27 17:47:23,728: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-27 17:47:36,815: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-27 17:47:36,816: INFO/MainProcess] CloudScraper failed for e5ec6178-a48d-46d3-9165-0dcd4f668629/fr — trying Selenium.
[2026-03-27 17:48:04,335: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196 lang=it: SUCCESS
[2026-03-27 17:48:07,109: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-27 17:48:21,871: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-27 17:48:26,812: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-27 17:48:35,755: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-27 17:48:41,966: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-27 17:48:54,330: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-27 17:48:54,330: INFO/MainProcess] CloudScraper failed for 10f37dfd-108d-459a-b890-167f81bbe196/fr — trying Selenium.
[2026-03-27 17:49:22,189: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629 lang=fr: SUCCESS
[2026-03-27 17:49:25,103: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:49:34,133: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:49:38,916: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:49:49,439: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:49:55,646: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:50:29,231: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-27 17:50:29,231: INFO/MainProcess] CloudScraper failed for e5ec6178-a48d-46d3-9165-0dcd4f668629/pt — trying Selenium.
[2026-03-27 17:50:52,274: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196 lang=fr: SUCCESS
[2026-03-27 17:50:55,205: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-27 17:51:04,878: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-27 17:51:09,634: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-27 17:51:22,991: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-27 17:51:29,218: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-27 17:51:41,122: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-27 17:51:41,122: INFO/MainProcess] CloudScraper failed for 10f37dfd-108d-459a-b890-167f81bbe196/pt — trying Selenium.
[2026-03-27 17:52:10,365: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629 lang=pt: SUCCESS
[2026-03-27 17:52:10,367: INFO/MainProcess] URL e5ec6178-a48d-46d3-9165-0dcd4f668629: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 17:52:13,168: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-27 17:52:22,795: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-27 17:52:27,672: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-27 17:52:36,152: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-27 17:52:42,371: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-27 17:52:55,426: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-27 17:52:55,426: INFO/MainProcess] CloudScraper failed for c66f6ead-1b95-459e-8011-b01871a89a57/en — trying Selenium.
[2026-03-27 17:53:29,840: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196 lang=pt: SUCCESS
[2026-03-27 17:53:29,843: INFO/MainProcess] URL 10f37dfd-108d-459a-b890-167f81bbe196: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 17:53:32,626: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:53:40,970: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:53:45,795: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:53:58,907: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:54:05,139: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:54:14,557: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:54:14,557: INFO/MainProcess] CloudScraper failed for 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/en — trying Selenium.
[2026-03-27 17:55:50,446: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 17:55:52,398: INFO/MainProcess] Gallery: 144 images loaded after scroll
[2026-03-27 17:55:56,624: INFO/MainProcess] Gallery: 151 unique image URLs extracted
[2026-03-27 17:55:56,794: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 17:55:56,795: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 17:56:23,537: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for c66f6ead-1b95-459e-8011-b01871a89a57
[2026-03-27 17:56:32,111: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel b7e64bdb-7dfe-4262-888e-140d5e332e39
[2026-03-27 17:56:32,111: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel b7e64bdb-7dfe-4262-888e-140d5e332e39
[2026-03-27 17:56:32,121: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57 lang=en: SUCCESS
[2026-03-27 17:56:35,333: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-27 17:56:48,722: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-27 17:56:53,502: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-27 17:57:02,895: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-27 17:57:09,110: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-27 17:57:23,208: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-27 17:57:23,208: INFO/MainProcess] CloudScraper failed for c66f6ead-1b95-459e-8011-b01871a89a57/es — trying Selenium.
[2026-03-27 17:57:43,278: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-27 17:57:51,951: INFO/MainProcess] Selenium retry 2 -- waiting 18s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 17:59:24,679: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-27 17:59:36,576: INFO/MainProcess] Selenium retry 3 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:01:11,681: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-27 18:01:11,682: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:01:11,684: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/en
[2026-03-27 18:01:11,684: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-27 18:01:12,936: INFO/MainProcess] VPN disconnected.
[2026-03-27 18:01:17,936: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-27 18:01:37,348: INFO/MainProcess] VPN connected to Germany — IP: 45.129.35.59
[2026-03-27 18:01:37,348: INFO/MainProcess] VPN rotation successful → Germany
[2026-03-27 18:01:37,350: INFO/MainProcess] VPN rotated — retrying 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/en with CloudScraper.
[2026-03-27 18:01:40,174: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:01:48,199: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:01:48,199: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-27 18:02:30,304: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57 lang=es: SUCCESS
[2026-03-27 18:02:33,095: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-27 18:02:43,031: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-27 18:02:47,798: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-27 18:02:58,133: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-27 18:03:04,342: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-27 18:03:19,269: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-27 18:03:19,269: INFO/MainProcess] CloudScraper failed for c66f6ead-1b95-459e-8011-b01871a89a57/de — trying Selenium.
[2026-03-27 18:03:49,473: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-27 18:03:59,912: INFO/MainProcess] Selenium retry 2 -- waiting 18s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:05:33,009: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-27 18:05:47,831: INFO/MainProcess] Selenium retry 3 -- waiting 24s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:07:26,770: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-27 18:07:26,770: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-27 18:07:26,791: WARNING/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec lang=en: FAILED
[2026-03-27 18:07:29,497: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-27 18:08:07,431: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-27 18:08:12,146: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-27 18:08:22,648: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-27 18:08:28,823: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-27 18:08:38,361: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-27 18:08:38,361: INFO/MainProcess] CloudScraper failed for 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/es — trying Selenium.
[2026-03-27 18:08:46,695: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57 lang=de: SUCCESS
[2026-03-27 18:08:49,365: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-27 18:09:00,078: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-27 18:09:04,812: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-27 18:09:19,615: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-27 18:09:25,766: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-27 18:09:35,246: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-27 18:09:35,246: INFO/MainProcess] CloudScraper failed for c66f6ead-1b95-459e-8011-b01871a89a57/it — trying Selenium.
[2026-03-27 18:10:06,081: INFO/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec lang=es: SUCCESS
[2026-03-27 18:10:09,085: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:10:20,463: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:10:25,449: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:10:35,798: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:10:42,007: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:10:54,045: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:10:54,045: INFO/MainProcess] CloudScraper failed for 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/de — trying Selenium.
[2026-03-27 18:11:38,959: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57 lang=it: SUCCESS
[2026-03-27 18:11:41,814: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-27 18:11:51,470: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-27 18:11:56,172: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-27 18:12:07,334: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-27 18:12:13,510: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-27 18:12:27,063: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-27 18:12:27,063: INFO/MainProcess] CloudScraper failed for c66f6ead-1b95-459e-8011-b01871a89a57/fr — trying Selenium.
[2026-03-27 18:12:56,261: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-27 18:13:04,406: INFO/MainProcess] Selenium retry 2 -- waiting 21s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:14:39,922: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-27 18:14:52,492: INFO/MainProcess] Selenium retry 3 -- waiting 34s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:16:41,796: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-27 18:16:41,796: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:16:41,798: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/de
[2026-03-27 18:16:41,798: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-27 18:16:42,765: INFO/MainProcess] VPN disconnected.
[2026-03-27 18:16:47,766: INFO/MainProcess] VPN: connecting to Spain (ES)...
[2026-03-27 18:17:06,515: INFO/MainProcess] VPN connected to Spain — IP: 79.116.133.126
[2026-03-27 18:17:06,515: INFO/MainProcess] VPN rotation successful → Spain
[2026-03-27 18:17:06,517: INFO/MainProcess] VPN rotated — retrying 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/de with CloudScraper.
[2026-03-27 18:17:09,303: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:17:23,666: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:17:23,667: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-27 18:18:02,029: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57 lang=fr: SUCCESS
[2026-03-27 18:18:04,751: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-27 18:18:17,312: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-27 18:18:22,589: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-27 18:18:30,926: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-27 18:18:37,115: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-27 18:19:10,105: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-27 18:19:10,105: INFO/MainProcess] CloudScraper failed for c66f6ead-1b95-459e-8011-b01871a89a57/pt — trying Selenium.
[2026-03-27 18:19:20,268: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-27 18:19:29,985: INFO/MainProcess] Selenium retry 2 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:21:01,194: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-27 18:21:16,081: INFO/MainProcess] Selenium retry 3 -- waiting 32s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:23:02,702: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-27 18:23:02,703: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-27 18:23:02,735: WARNING/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec lang=de: FAILED
[2026-03-27 18:23:05,492: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:23:14,666: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:23:19,302: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:23:29,513: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:23:35,697: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:23:49,797: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:23:49,798: INFO/MainProcess] CloudScraper failed for 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/it — trying Selenium.
[2026-03-27 18:24:21,887: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57 lang=pt: SUCCESS
[2026-03-27 18:24:21,890: INFO/MainProcess] URL c66f6ead-1b95-459e-8011-b01871a89a57: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 18:24:24,727: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-27 18:24:37,309: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-27 18:24:42,024: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-27 18:24:50,654: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-27 18:24:56,817: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-27 18:25:07,030: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-27 18:25:07,031: INFO/MainProcess] CloudScraper failed for 67bbbef6-d0c9-4d44-9273-9f66a22957d5/en — trying Selenium.
[2026-03-27 18:25:38,714: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-27 18:25:53,325: INFO/MainProcess] Selenium retry 2 -- waiting 13s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:27:20,947: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-27 18:27:33,512: INFO/MainProcess] Selenium retry 3 -- waiting 27s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:29:15,845: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-27 18:29:15,845: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:29:15,847: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/it
[2026-03-27 18:29:15,848: INFO/MainProcess] VPN: rotating (current=ES)...
[2026-03-27 18:29:17,066: INFO/MainProcess] VPN disconnected.
[2026-03-27 18:29:22,068: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-27 18:29:40,310: INFO/MainProcess] VPN connected to Sweden — IP: 77.243.86.73
[2026-03-27 18:29:40,311: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-27 18:29:40,312: INFO/MainProcess] VPN rotated — retrying 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/it with CloudScraper.
[2026-03-27 18:29:42,948: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:29:55,160: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:29:55,160: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-27 18:31:36,113: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 18:31:38,033: INFO/MainProcess] Gallery: 113 images loaded after scroll
[2026-03-27 18:31:41,603: INFO/MainProcess] Gallery: 120 unique image URLs extracted
[2026-03-27 18:31:41,788: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 18:31:41,789: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 18:32:09,464: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 67bbbef6-d0c9-4d44-9273-9f66a22957d5
[2026-03-27 18:32:19,291: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel b480bc22-62b2-417e-bd52-c59b0ae4b81e
[2026-03-27 18:32:19,291: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel b480bc22-62b2-417e-bd52-c59b0ae4b81e
[2026-03-27 18:32:19,305: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5 lang=en: SUCCESS
[2026-03-27 18:32:21,865: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-27 18:32:30,775: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-27 18:32:35,258: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-27 18:32:48,542: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-27 18:32:54,583: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-27 18:33:05,843: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-27 18:33:05,844: INFO/MainProcess] CloudScraper failed for 67bbbef6-d0c9-4d44-9273-9f66a22957d5/es — trying Selenium.
[2026-03-27 18:33:27,412: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-27 18:33:37,423: INFO/MainProcess] Selenium retry 2 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:35:08,273: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-27 18:35:20,427: INFO/MainProcess] Selenium retry 3 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:36:58,126: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-27 18:36:58,126: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-27 18:36:58,148: WARNING/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec lang=it: FAILED
[2026-03-27 18:37:00,677: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:37:12,909: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:37:17,458: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:37:28,476: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:37:34,519: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:37:46,445: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:37:46,446: INFO/MainProcess] CloudScraper failed for 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/fr — trying Selenium.
[2026-03-27 18:38:18,168: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5 lang=es: SUCCESS
[2026-03-27 18:38:20,689: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-27 18:38:34,864: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-27 18:38:39,427: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-27 18:38:49,852: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-27 18:38:55,893: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-27 18:39:06,627: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-27 18:39:06,627: INFO/MainProcess] CloudScraper failed for 67bbbef6-d0c9-4d44-9273-9f66a22957d5/de — trying Selenium.
[2026-03-27 18:39:36,705: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 18:39:48,695: INFO/MainProcess] Selenium retry 2 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:41:19,275: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 18:41:33,078: INFO/MainProcess] Selenium retry 3 -- waiting 32s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:43:19,473: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 18:43:19,474: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:43:19,475: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/fr
[2026-03-27 18:43:19,476: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-27 18:43:20,496: INFO/MainProcess] VPN disconnected.
[2026-03-27 18:43:25,497: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-27 18:43:44,578: INFO/MainProcess] VPN connected to Germany — IP: 45.130.105.43
[2026-03-27 18:43:44,579: INFO/MainProcess] VPN rotation successful → Germany
[2026-03-27 18:43:44,580: INFO/MainProcess] VPN rotated — retrying 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/fr with CloudScraper.
[2026-03-27 18:43:47,396: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:43:56,193: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:43:56,193: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-27 18:44:39,550: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5 lang=de: SUCCESS
[2026-03-27 18:44:42,282: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-27 18:44:54,165: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-27 18:44:58,872: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-27 18:45:10,828: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-27 18:45:17,001: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-27 18:45:27,596: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-27 18:45:27,596: INFO/MainProcess] CloudScraper failed for 67bbbef6-d0c9-4d44-9273-9f66a22957d5/it — trying Selenium.
[2026-03-27 18:45:57,150: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 18:46:11,212: INFO/MainProcess] Selenium retry 2 -- waiting 12s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:47:38,186: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 18:47:50,506: INFO/MainProcess] Selenium retry 3 -- waiting 19s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:49:24,841: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-27 18:49:24,842: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-27 18:49:24,864: WARNING/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec lang=fr: FAILED
[2026-03-27 18:49:27,514: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:49:42,289: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:49:46,982: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:50:25,746: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:50:31,865: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:50:44,459: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5 lang=it: SUCCESS
[2026-03-27 18:50:47,134: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 18:50:56,014: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 18:51:00,668: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 18:51:09,749: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 18:51:11,603: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:51:11,603: INFO/MainProcess] CloudScraper failed for 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/pt — trying Selenium.
[2026-03-27 18:51:15,907: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 18:51:24,251: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-27 18:51:24,252: INFO/MainProcess] CloudScraper failed for 67bbbef6-d0c9-4d44-9273-9f66a22957d5/fr — trying Selenium.
[2026-03-27 18:52:30,163: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-27 18:52:41,500: INFO/MainProcess] Selenium retry 2 -- waiting 10s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:54:06,317: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-27 18:54:14,672: INFO/MainProcess] Selenium retry 3 -- waiting 21s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:55:50,864: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-27 18:55:50,865: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:55:50,867: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/pt
[2026-03-27 18:55:50,867: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-27 18:55:51,791: INFO/MainProcess] VPN disconnected.
[2026-03-27 18:55:56,792: INFO/MainProcess] VPN: connecting to France (FR)...
[2026-03-27 18:56:15,715: INFO/MainProcess] VPN connected to France — IP: 45.141.123.241
[2026-03-27 18:56:15,715: INFO/MainProcess] VPN rotation successful → France
[2026-03-27 18:56:15,717: INFO/MainProcess] VPN rotated — retrying 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec/pt with CloudScraper.
[2026-03-27 18:56:18,509: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:56:54,773: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 18:56:54,774: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-27 18:57:08,970: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5 lang=fr: SUCCESS
[2026-03-27 18:57:11,612: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-27 18:57:21,118: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-27 18:57:25,843: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-27 18:57:40,112: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-27 18:57:46,285: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-27 18:58:01,063: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-27 18:58:01,063: INFO/MainProcess] CloudScraper failed for 67bbbef6-d0c9-4d44-9273-9f66a22957d5/pt — trying Selenium.
[2026-03-27 18:58:28,156: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-27 18:58:41,177: INFO/MainProcess] Selenium retry 2 -- waiting 11s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 19:00:06,850: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-27 19:00:15,033: INFO/MainProcess] Selenium retry 3 -- waiting 24s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 19:01:53,825: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-27 19:01:53,825: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-27 19:01:53,855: WARNING/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec lang=pt: FAILED
[2026-03-27 19:01:53,857: WARNING/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec: PARTIAL — Incomplete: 1/6 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:01:53,863: INFO/MainProcess] URL 130cce12-0d6d-4f13-9db2-3fa4ab2c94ec marked incomplete — data PRESERVED. ok=['es'] fail=['en', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:01:56,502: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 19:02:30,265: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 19:02:35,093: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 19:03:12,021: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 19:03:12,723: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5 lang=pt: SUCCESS
[2026-03-27 19:03:12,725: INFO/MainProcess] URL 67bbbef6-d0c9-4d44-9273-9f66a22957d5: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:03:15,384: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 19:03:18,218: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 19:03:23,496: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 19:03:28,256: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 19:03:29,403: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-27 19:03:29,404: INFO/MainProcess] CloudScraper failed for d37bc34b-b4c4-4863-8858-bced1aad4d30/en — trying Selenium.
[2026-03-27 19:03:41,489: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 19:03:47,677: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 19:03:58,447: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-27 19:03:58,448: INFO/MainProcess] CloudScraper failed for f5638f32-e093-4ceb-90dc-ada5f38d5e83/en — trying Selenium.
[2026-03-27 19:05:50,768: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 19:05:52,667: INFO/MainProcess] Gallery: 40 images loaded after scroll
[2026-03-27 19:05:55,030: INFO/MainProcess] Gallery: 47 unique image URLs extracted
[2026-03-27 19:05:55,162: INFO/MainProcess] hotelPhotos JS: 40 photos extracted from page source
[2026-03-27 19:05:55,163: INFO/MainProcess] Gallery: 40 photos with full metadata (hotelPhotos JS)
[2026-03-27 19:06:21,166: INFO/MainProcess] Photos: 40 rich photo records (hotelPhotos JS) for d37bc34b-b4c4-4863-8858-bced1aad4d30
[2026-03-27 19:06:27,947: INFO/MainProcess] download_photo_batch: 120/120 photo-files saved for hotel 79b2efdf-5bd2-4a10-be7d-eb452a7b3b31
[2026-03-27 19:06:27,948: INFO/MainProcess] ImageDownloader (photo_batch): 120/40 photos saved for hotel 79b2efdf-5bd2-4a10-be7d-eb452a7b3b31
[2026-03-27 19:06:27,962: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30 lang=en: SUCCESS
[2026-03-27 19:06:30,899: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 19:06:42,987: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 19:06:47,631: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 19:07:01,954: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 19:07:08,140: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 19:07:20,366: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-27 19:07:20,366: INFO/MainProcess] CloudScraper failed for d37bc34b-b4c4-4863-8858-bced1aad4d30/es — trying Selenium.
[2026-03-27 19:08:41,804: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 19:08:43,714: INFO/MainProcess] Gallery: 57 images loaded after scroll
[2026-03-27 19:08:45,525: INFO/MainProcess] Gallery: 64 unique image URLs extracted
[2026-03-27 19:08:45,659: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 19:08:45,662: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 19:09:11,636: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for f5638f32-e093-4ceb-90dc-ada5f38d5e83
[2026-03-27 19:09:17,805: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel a541289f-1c51-40fd-8fb8-63c67c55e6c7
[2026-03-27 19:09:17,805: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel a541289f-1c51-40fd-8fb8-63c67c55e6c7
[2026-03-27 19:09:17,812: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83 lang=en: SUCCESS
[2026-03-27 19:09:20,680: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 19:09:34,115: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 19:09:38,965: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 19:09:47,821: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 19:09:54,011: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 19:10:07,389: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-27 19:10:07,390: INFO/MainProcess] CloudScraper failed for f5638f32-e093-4ceb-90dc-ada5f38d5e83/es — trying Selenium.
[2026-03-27 19:10:28,818: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30 lang=es: SUCCESS
[2026-03-27 19:10:31,482: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 19:10:41,646: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 19:10:46,327: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 19:11:13,706: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 19:11:19,894: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 19:11:31,539: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-27 19:11:31,541: INFO/MainProcess] CloudScraper failed for d37bc34b-b4c4-4863-8858-bced1aad4d30/de — trying Selenium.
[2026-03-27 19:11:46,956: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83 lang=es: SUCCESS
[2026-03-27 19:11:49,721: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 19:11:58,223: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 19:12:02,894: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 19:12:11,380: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 19:12:17,559: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 19:12:41,818: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-27 19:12:41,818: INFO/MainProcess] CloudScraper failed for f5638f32-e093-4ceb-90dc-ada5f38d5e83/de — trying Selenium.
[2026-03-27 19:13:06,541: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30 lang=de: SUCCESS
[2026-03-27 19:13:09,194: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 19:13:21,683: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 19:13:26,413: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 19:14:00,648: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 19:14:06,851: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 19:14:37,086: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-27 19:14:37,102: INFO/MainProcess] CloudScraper failed for d37bc34b-b4c4-4863-8858-bced1aad4d30/it — trying Selenium.
[2026-03-27 19:14:37,488: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83 lang=de: SUCCESS
[2026-03-27 19:14:40,192: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 19:14:51,814: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 19:14:56,592: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 19:15:06,616: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 19:15:12,808: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 19:15:27,478: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-27 19:15:27,478: INFO/MainProcess] CloudScraper failed for f5638f32-e093-4ceb-90dc-ada5f38d5e83/it — trying Selenium.
[2026-03-27 19:15:57,116: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30 lang=it: SUCCESS
[2026-03-27 19:15:59,898: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 19:16:08,822: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 19:16:13,491: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 19:16:26,612: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 19:16:32,781: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 19:16:47,068: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-27 19:16:47,071: INFO/MainProcess] CloudScraper failed for d37bc34b-b4c4-4863-8858-bced1aad4d30/fr — trying Selenium.
[2026-03-27 19:17:16,410: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83 lang=it: SUCCESS
[2026-03-27 19:17:19,115: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 19:17:33,068: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 19:17:37,789: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 19:17:46,026: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 19:17:52,215: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 19:18:02,566: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-27 19:18:02,566: INFO/MainProcess] CloudScraper failed for f5638f32-e093-4ceb-90dc-ada5f38d5e83/fr — trying Selenium.
[2026-03-27 19:18:35,625: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30 lang=fr: SUCCESS
[2026-03-27 19:18:38,438: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-27 19:18:50,872: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-27 19:18:55,614: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-27 19:19:06,310: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-27 19:19:12,496: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-27 19:19:21,011: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-27 19:19:21,011: INFO/MainProcess] CloudScraper failed for d37bc34b-b4c4-4863-8858-bced1aad4d30/pt — trying Selenium.
[2026-03-27 19:20:06,086: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83 lang=fr: SUCCESS
[2026-03-27 19:20:08,753: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-27 19:20:34,169: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-27 19:20:39,093: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-27 19:20:48,276: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-27 19:20:54,472: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-27 19:21:08,018: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-27 19:21:08,018: INFO/MainProcess] CloudScraper failed for f5638f32-e093-4ceb-90dc-ada5f38d5e83/pt — trying Selenium.
[2026-03-27 19:21:24,053: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30 lang=pt: SUCCESS
[2026-03-27 19:21:24,056: INFO/MainProcess] URL d37bc34b-b4c4-4863-8858-bced1aad4d30: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:21:26,727: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 19:21:41,253: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 19:21:46,054: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 19:21:55,213: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 19:22:01,395: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 19:22:16,376: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-27 19:22:16,376: INFO/MainProcess] CloudScraper failed for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7/en — trying Selenium.
[2026-03-27 19:22:42,007: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83 lang=pt: SUCCESS
[2026-03-27 19:22:42,009: INFO/MainProcess] URL f5638f32-e093-4ceb-90dc-ada5f38d5e83: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:22:44,792: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 19:22:56,851: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 19:23:01,570: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 19:23:15,500: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 19:23:21,897: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 19:23:44,562: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-27 19:23:44,563: INFO/MainProcess] CloudScraper failed for bdec8c7e-05ec-47ca-a6e2-829ffa43688a/en — trying Selenium.
[2026-03-27 19:25:02,088: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 19:25:04,136: INFO/MainProcess] Gallery: 70 images loaded after scroll
[2026-03-27 19:25:06,791: INFO/MainProcess] Gallery: 77 unique image URLs extracted
[2026-03-27 19:25:06,934: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-27 19:25:06,935: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-27 19:25:33,689: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7
[2026-03-27 19:25:44,733: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel af92373c-0cdc-4047-aaed-2c40ecd10424
[2026-03-27 19:25:44,734: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel af92373c-0cdc-4047-aaed-2c40ecd10424
[2026-03-27 19:25:44,744: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7 lang=en: SUCCESS
[2026-03-27 19:25:47,583: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 19:25:56,293: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 19:26:01,044: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 19:26:27,769: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 19:26:33,939: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 19:26:43,558: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-27 19:26:43,559: INFO/MainProcess] CloudScraper failed for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7/es — trying Selenium.
[2026-03-27 19:27:53,863: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-27 19:27:55,759: INFO/MainProcess] Gallery: 34 images loaded after scroll
[2026-03-27 19:27:58,070: INFO/MainProcess] Gallery: 41 unique image URLs extracted
[2026-03-27 19:27:58,190: INFO/MainProcess] hotelPhotos JS: 34 photos extracted from page source
[2026-03-27 19:27:58,191: INFO/MainProcess] Gallery: 34 photos with full metadata (hotelPhotos JS)
[2026-03-27 19:28:25,145: INFO/MainProcess] Photos: 34 rich photo records (hotelPhotos JS) for bdec8c7e-05ec-47ca-a6e2-829ffa43688a
[2026-03-27 19:28:31,329: INFO/MainProcess] download_photo_batch: 102/102 photo-files saved for hotel 1e5c59a5-58cb-4faf-9273-a6eac5605346
[2026-03-27 19:28:31,330: INFO/MainProcess] ImageDownloader (photo_batch): 102/34 photos saved for hotel 1e5c59a5-58cb-4faf-9273-a6eac5605346
[2026-03-27 19:28:31,338: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a lang=en: SUCCESS
[2026-03-27 19:28:34,266: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 19:28:43,434: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 19:28:48,145: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 19:29:01,077: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 19:29:07,266: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 19:29:45,433: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7 lang=es: SUCCESS
[2026-03-27 19:29:45,691: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-27 19:29:45,692: INFO/MainProcess] CloudScraper failed for bdec8c7e-05ec-47ca-a6e2-829ffa43688a/es — trying Selenium.
[2026-03-27 19:29:48,069: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 19:29:58,084: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 19:30:02,768: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 19:30:16,555: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 19:30:22,753: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 19:30:34,612: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-27 19:30:34,613: INFO/MainProcess] CloudScraper failed for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7/de — trying Selenium.
[2026-03-27 19:31:05,302: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a lang=es: SUCCESS
[2026-03-27 19:31:07,973: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 19:31:17,788: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 19:31:22,390: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 19:31:50,294: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 19:31:56,430: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 19:32:20,410: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-27 19:32:20,410: INFO/MainProcess] CloudScraper failed for bdec8c7e-05ec-47ca-a6e2-829ffa43688a/de — trying Selenium.
[2026-03-27 19:32:25,112: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7 lang=de: SUCCESS
[2026-03-27 19:32:27,744: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 19:32:41,616: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 19:32:46,405: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 19:32:55,079: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 19:33:01,264: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 19:33:14,299: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-27 19:33:14,299: INFO/MainProcess] CloudScraper failed for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7/it — trying Selenium.
[2026-03-27 19:33:58,128: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a lang=de: SUCCESS
[2026-03-27 19:34:00,776: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 19:34:22,175: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 19:34:26,869: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 19:34:49,046: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 19:34:55,209: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 19:35:17,152: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7 lang=it: SUCCESS
[2026-03-27 19:35:19,899: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 19:35:23,043: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-27 19:35:23,043: INFO/MainProcess] CloudScraper failed for bdec8c7e-05ec-47ca-a6e2-829ffa43688a/it — trying Selenium.
[2026-03-27 19:35:33,697: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 19:35:38,451: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 19:35:51,544: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 19:35:57,736: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 19:36:30,699: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-27 19:36:30,699: INFO/MainProcess] CloudScraper failed for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7/fr — trying Selenium.
[2026-03-27 19:36:42,589: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a lang=it: SUCCESS
[2026-03-27 19:36:45,240: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 19:37:20,365: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 19:37:25,165: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 19:37:35,468: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 19:37:41,867: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 19:38:02,361: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7 lang=fr: SUCCESS
[2026-03-27 19:38:05,131: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-27 19:38:10,022: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-27 19:38:10,023: INFO/MainProcess] CloudScraper failed for bdec8c7e-05ec-47ca-a6e2-829ffa43688a/fr — trying Selenium.
[2026-03-27 19:38:19,737: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-27 19:38:24,355: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-27 19:38:36,969: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-27 19:38:43,159: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-27 19:38:54,112: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-27 19:38:54,112: INFO/MainProcess] CloudScraper failed for 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7/pt — trying Selenium.
[2026-03-27 19:39:42,585: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a lang=fr: SUCCESS
[2026-03-27 19:39:45,324: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-27 19:39:53,994: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-27 19:39:58,791: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-27 19:40:12,582: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-27 19:40:18,757: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-27 19:40:32,211: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-27 19:40:32,211: INFO/MainProcess] CloudScraper failed for bdec8c7e-05ec-47ca-a6e2-829ffa43688a/pt — trying Selenium.
[2026-03-27 19:41:00,203: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7 lang=pt: SUCCESS
[2026-03-27 19:41:00,205: INFO/MainProcess] URL 2e8e8e95-bae8-4fba-9bb3-fe291e0238b7: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:42:17,851: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a lang=pt: SUCCESS
[2026-03-27 19:42:17,853: INFO/MainProcess] URL bdec8c7e-05ec-47ca-a6e2-829ffa43688a: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-27 19:42:20,256: INFO/MainProcess] Selenium browser closed after batch completion.
[2026-03-27 19:42:20,257: INFO/MainProcess] scrape_pending_urls: batch complete — {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-27 19:42:20,260: INFO/MainProcess] Task tasks.scrape_pending_urls[6f8231c3-0d56-498d-99ae-8440f5f50a2b] succeeded in 10137.424210899975s: {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-27 19:42:20,525: INFO/MainProcess] Task tasks.reset_stale_processing_urls[de412752-9a49-439c-ac92-89d08e3a9d2a] received
[2026-03-27 19:42:20,530: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-27 19:42:20,531: INFO/MainProcess] Task tasks.reset_stale_processing_urls[de412752-9a49-439c-ac92-89d08e3a9d2a] succeeded in 0.005314200068823993s: {'reset': 0}
[2026-03-27 19:42:20,533: INFO/MainProcess] Task tasks.collect_system_metrics[efe9ad56-8e5b-4726-a988-10fa903cf027] received
[2026-03-27 19:42:21,053: INFO/MainProcess] Task tasks.collect_system_metrics[efe9ad56-8e5b-4726-a988-10fa903cf027] succeeded in 0.5193270000163466s: {'cpu': 25.9, 'memory': 44.6}
[2026-03-27 19:42:21,055: INFO/MainProcess] Task tasks.scrape_pending_urls[388fee4a-ce22-4a42-a8a1-3bd3547bebda] received
[2026-03-27 19:42:21,059: INFO/MainProcess] Task tasks.scrape_pending_urls[388fee4a-ce22-4a42-a8a1-3bd3547bebda] succeeded in 0.003646500059403479s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:21,061: INFO/MainProcess] Task tasks.purge_old_debug_html[b121ab96-bfc3-490d-b575-ca69148fce4a] received
[2026-03-27 19:42:21,063: INFO/MainProcess] Task tasks.purge_old_debug_html[b121ab96-bfc3-490d-b575-ca69148fce4a] succeeded in 0.0018817000091075897s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-27 19:42:21,065: INFO/MainProcess] Task tasks.collect_system_metrics[aefe19a7-f9bf-4dc4-bb31-ea08463e3b35] received
[2026-03-27 19:42:21,583: INFO/MainProcess] Task tasks.collect_system_metrics[aefe19a7-f9bf-4dc4-bb31-ea08463e3b35] succeeded in 0.5178420000011101s: {'cpu': 15.0, 'memory': 44.6}
[2026-03-27 19:42:21,585: INFO/MainProcess] Task tasks.scrape_pending_urls[5f625067-97e9-48f9-b713-e6f5d816f23c] received
[2026-03-27 19:42:21,589: INFO/MainProcess] Task tasks.scrape_pending_urls[5f625067-97e9-48f9-b713-e6f5d816f23c] succeeded in 0.003553300048224628s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:21,591: INFO/MainProcess] Task tasks.reset_stale_processing_urls[6212c0d9-9c65-49dd-93c6-852e3785251f] received
[2026-03-27 19:42:21,594: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-27 19:42:21,595: INFO/MainProcess] Task tasks.reset_stale_processing_urls[6212c0d9-9c65-49dd-93c6-852e3785251f] succeeded in 0.003554699942469597s: {'reset': 0}
[2026-03-27 19:42:21,598: INFO/MainProcess] Task tasks.collect_system_metrics[668d28d3-f5e9-46fc-be7d-808b0ad38901] received
[2026-03-27 19:42:22,106: INFO/MainProcess] Task tasks.collect_system_metrics[668d28d3-f5e9-46fc-be7d-808b0ad38901] succeeded in 0.5068280999548733s: {'cpu': 10.2, 'memory': 44.6}
[2026-03-27 19:42:22,108: INFO/MainProcess] Task tasks.scrape_pending_urls[7ab790af-de23-4794-bbf1-01902c1a0fef] received
[2026-03-27 19:42:22,113: INFO/MainProcess] Task tasks.scrape_pending_urls[7ab790af-de23-4794-bbf1-01902c1a0fef] succeeded in 0.00392920000012964s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:22,115: INFO/MainProcess] Task tasks.collect_system_metrics[7abf8076-0a97-4f9d-99e9-61338052cfba] received
[2026-03-27 19:42:22,633: INFO/MainProcess] Task tasks.collect_system_metrics[7abf8076-0a97-4f9d-99e9-61338052cfba] succeeded in 0.518404999980703s: {'cpu': 6.4, 'memory': 44.6}
[2026-03-27 19:42:22,636: INFO/MainProcess] Task tasks.scrape_pending_urls[00a05c5a-e650-403c-b69f-85b6b10b5f8d] received
[2026-03-27 19:42:22,640: INFO/MainProcess] Task tasks.scrape_pending_urls[00a05c5a-e650-403c-b69f-85b6b10b5f8d] succeeded in 0.004313400015234947s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:22,642: INFO/MainProcess] Task tasks.collect_system_metrics[6c35495c-4851-455d-89d2-2d4e43c410af] received
[2026-03-27 19:42:23,160: INFO/MainProcess] Task tasks.collect_system_metrics[6c35495c-4851-455d-89d2-2d4e43c410af] succeeded in 0.5174126999918371s: {'cpu': 5.9, 'memory': 44.6}
[2026-03-27 19:42:23,162: INFO/MainProcess] Task tasks.scrape_pending_urls[56a2ade7-47e2-40d4-886d-b96dcc0ba68f] received
[2026-03-27 19:42:23,167: INFO/MainProcess] Task tasks.scrape_pending_urls[56a2ade7-47e2-40d4-886d-b96dcc0ba68f] succeeded in 0.004293300095014274s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:23,169: INFO/MainProcess] Task tasks.collect_system_metrics[2ebeb510-8b69-4756-9351-d183f83682fb] received
[2026-03-27 19:42:23,675: INFO/MainProcess] Task tasks.collect_system_metrics[2ebeb510-8b69-4756-9351-d183f83682fb] succeeded in 0.5060593000380322s: {'cpu': 16.7, 'memory': 44.6}
[2026-03-27 19:42:23,677: INFO/MainProcess] Task tasks.scrape_pending_urls[7bc461f5-6bc2-4d3e-b4a6-ecebe8bc5d8f] received
[2026-03-27 19:42:23,683: INFO/MainProcess] Task tasks.scrape_pending_urls[7bc461f5-6bc2-4d3e-b4a6-ecebe8bc5d8f] succeeded in 0.005182799999602139s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:23,684: INFO/MainProcess] Task tasks.collect_system_metrics[45253bae-5fc3-4455-9035-1f67b6c91c19] received
[2026-03-27 19:42:24,202: INFO/MainProcess] Task tasks.collect_system_metrics[45253bae-5fc3-4455-9035-1f67b6c91c19] succeeded in 0.5178133000154048s: {'cpu': 2.0, 'memory': 44.6}
[2026-03-27 19:42:24,206: INFO/MainProcess] Task tasks.scrape_pending_urls[5de65b19-6b6f-4b07-b984-21bfb9ac6458] received
[2026-03-27 19:42:24,209: INFO/MainProcess] Task tasks.scrape_pending_urls[5de65b19-6b6f-4b07-b984-21bfb9ac6458] succeeded in 0.003428799915127456s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:24,211: INFO/MainProcess] Task tasks.collect_system_metrics[2a2896b5-b087-4c13-bdbf-475acad0fc1c] received
[2026-03-27 19:42:24,728: INFO/MainProcess] Task tasks.collect_system_metrics[2a2896b5-b087-4c13-bdbf-475acad0fc1c] succeeded in 0.5167554999934509s: {'cpu': 15.7, 'memory': 44.5}
[2026-03-27 19:42:24,731: INFO/MainProcess] Task tasks.scrape_pending_urls[1adccfa2-4ef9-415a-aed1-2f3c5cc522b3] received
[2026-03-27 19:42:24,734: INFO/MainProcess] Task tasks.scrape_pending_urls[1adccfa2-4ef9-415a-aed1-2f3c5cc522b3] succeeded in 0.002993200090713799s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:24,735: INFO/MainProcess] Task tasks.collect_system_metrics[b6edc964-34c0-4ef9-8afe-9b9015c5ece1] received
[2026-03-27 19:42:25,253: INFO/MainProcess] Task tasks.collect_system_metrics[b6edc964-34c0-4ef9-8afe-9b9015c5ece1] succeeded in 0.5171137000434101s: {'cpu': 10.9, 'memory': 44.5}
[2026-03-27 19:42:25,255: INFO/MainProcess] Task tasks.scrape_pending_urls[9764a3b3-297b-4d76-b063-7f507e80d31a] received
[2026-03-27 19:42:25,259: INFO/MainProcess] Task tasks.scrape_pending_urls[9764a3b3-297b-4d76-b063-7f507e80d31a] succeeded in 0.003741699969395995s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:25,261: INFO/MainProcess] Task tasks.collect_system_metrics[b797bc8c-4de5-4355-bfa1-87dbf8d7005b] received
[2026-03-27 19:42:25,778: INFO/MainProcess] Task tasks.collect_system_metrics[b797bc8c-4de5-4355-bfa1-87dbf8d7005b] succeeded in 0.516556299990043s: {'cpu': 7.0, 'memory': 44.5}
[2026-03-27 19:42:25,781: INFO/MainProcess] Task tasks.scrape_pending_urls[7b2a3fc2-9b27-4e15-8e7b-014f09334513] received
[2026-03-27 19:42:25,785: INFO/MainProcess] Task tasks.scrape_pending_urls[7b2a3fc2-9b27-4e15-8e7b-014f09334513] succeeded in 0.004004399990662932s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:25,787: INFO/MainProcess] Task tasks.collect_system_metrics[052b2e87-ed70-42be-a8c2-6259da1234b1] received
[2026-03-27 19:42:26,304: INFO/MainProcess] Task tasks.collect_system_metrics[052b2e87-ed70-42be-a8c2-6259da1234b1] succeeded in 0.5167095999931917s: {'cpu': 2.0, 'memory': 44.5}
[2026-03-27 19:42:26,306: INFO/MainProcess] Task tasks.scrape_pending_urls[61c748bf-e7be-4f16-a8fd-6a3e0432bccd] received
[2026-03-27 19:42:26,311: INFO/MainProcess] Task tasks.scrape_pending_urls[61c748bf-e7be-4f16-a8fd-6a3e0432bccd] succeeded in 0.0038924000691622496s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,313: INFO/MainProcess] Task tasks.scrape_pending_urls[ba3688f2-0464-4d98-a7c3-0ae77ef13ef7] received
[2026-03-27 19:42:26,317: INFO/MainProcess] Task tasks.scrape_pending_urls[ba3688f2-0464-4d98-a7c3-0ae77ef13ef7] succeeded in 0.003557400079444051s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,319: INFO/MainProcess] Task tasks.scrape_pending_urls[268158db-bb1d-4c02-81d0-7c800a3d13e1] received
[2026-03-27 19:42:26,322: INFO/MainProcess] Task tasks.scrape_pending_urls[268158db-bb1d-4c02-81d0-7c800a3d13e1] succeeded in 0.003028900013305247s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,324: INFO/MainProcess] Task tasks.scrape_pending_urls[3f0b6eeb-3886-4be1-96cd-8d1301da49c7] received
[2026-03-27 19:42:26,327: INFO/MainProcess] Task tasks.scrape_pending_urls[3f0b6eeb-3886-4be1-96cd-8d1301da49c7] succeeded in 0.0028002000181004405s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,329: INFO/MainProcess] Task tasks.scrape_pending_urls[0edbe2d7-d415-4fa9-9a24-62d246fc0b5a] received
[2026-03-27 19:42:26,333: INFO/MainProcess] Task tasks.scrape_pending_urls[0edbe2d7-d415-4fa9-9a24-62d246fc0b5a] succeeded in 0.0038357999874278903s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,334: INFO/MainProcess] Task tasks.scrape_pending_urls[06595455-cb95-467a-b9dc-e78322c1f4a8] received
[2026-03-27 19:42:26,337: INFO/MainProcess] Task tasks.scrape_pending_urls[06595455-cb95-467a-b9dc-e78322c1f4a8] succeeded in 0.002741200034506619s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,339: INFO/MainProcess] Task tasks.scrape_pending_urls[b1360831-fef9-42f9-a14e-f27f47ee4ab0] received
[2026-03-27 19:42:26,342: INFO/MainProcess] Task tasks.scrape_pending_urls[b1360831-fef9-42f9-a14e-f27f47ee4ab0] succeeded in 0.002482800045982003s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,343: INFO/MainProcess] Task tasks.scrape_pending_urls[eaabac5a-5656-4234-b469-46d3b06f49a9] received
[2026-03-27 19:42:26,346: INFO/MainProcess] Task tasks.scrape_pending_urls[eaabac5a-5656-4234-b469-46d3b06f49a9] succeeded in 0.0025742000434547663s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,801: INFO/MainProcess] Task tasks.scrape_pending_urls[a5fa3895-5684-40bf-8e98-9e3a25faa709] received
[2026-03-27 19:42:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[a5fa3895-5684-40bf-8e98-9e3a25faa709] succeeded in 0.0031917999731376767s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,806: INFO/MainProcess] Task tasks.scrape_pending_urls[62cd4b6b-f1f7-4b64-8e11-591273586dc4] received
[2026-03-27 19:42:26,810: INFO/MainProcess] Task tasks.scrape_pending_urls[62cd4b6b-f1f7-4b64-8e11-591273586dc4] succeeded in 0.003148999996483326s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,813: INFO/MainProcess] Task tasks.scrape_pending_urls[ec905335-2575-4c5b-a2c8-f22d5e23892e] received
[2026-03-27 19:42:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[ec905335-2575-4c5b-a2c8-f22d5e23892e] succeeded in 0.0037890999810770154s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,819: INFO/MainProcess] Task tasks.scrape_pending_urls[6215cfc9-9996-4587-a779-cde2e2d5c645] received
[2026-03-27 19:42:26,824: INFO/MainProcess] Task tasks.scrape_pending_urls[6215cfc9-9996-4587-a779-cde2e2d5c645] succeeded in 0.0045972999650985s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,826: INFO/MainProcess] Task tasks.scrape_pending_urls[417d57f8-a333-4b9f-b7ab-8b8c8bcdc4e4] received
[2026-03-27 19:42:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[417d57f8-a333-4b9f-b7ab-8b8c8bcdc4e4] succeeded in 0.003420499968342483s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,832: INFO/MainProcess] Task tasks.scrape_pending_urls[1c9a1c5e-d84b-4ad8-941b-78372bd270d7] received
[2026-03-27 19:42:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[1c9a1c5e-d84b-4ad8-941b-78372bd270d7] succeeded in 0.0032195999519899487s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,838: INFO/MainProcess] Task tasks.scrape_pending_urls[2cd857b2-a790-4042-9c30-90a56509779a] received
[2026-03-27 19:42:26,841: INFO/MainProcess] Task tasks.scrape_pending_urls[2cd857b2-a790-4042-9c30-90a56509779a] succeeded in 0.0029972000047564507s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,844: INFO/MainProcess] Task tasks.scrape_pending_urls[f12570c3-1976-4d0b-95c6-ac51d938963e] received
[2026-03-27 19:42:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[f12570c3-1976-4d0b-95c6-ac51d938963e] succeeded in 0.0037721999688073993s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,851: INFO/MainProcess] Task tasks.scrape_pending_urls[55cd9ac8-8c9d-44eb-bfbd-2a5b889fb80d] received
[2026-03-27 19:42:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[55cd9ac8-8c9d-44eb-bfbd-2a5b889fb80d] succeeded in 0.0032161000417545438s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,856: INFO/MainProcess] Task tasks.scrape_pending_urls[62d8ea37-471a-4908-84e9-3e62583e3340] received
[2026-03-27 19:42:26,860: INFO/MainProcess] Task tasks.scrape_pending_urls[62d8ea37-471a-4908-84e9-3e62583e3340] succeeded in 0.0035592999774962664s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,862: INFO/MainProcess] Task tasks.scrape_pending_urls[2ef0d754-c719-4fb9-aac3-5b8c7b8a2a56] received
[2026-03-27 19:42:26,865: INFO/MainProcess] Task tasks.scrape_pending_urls[2ef0d754-c719-4fb9-aac3-5b8c7b8a2a56] succeeded in 0.003102000104263425s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,867: INFO/MainProcess] Task tasks.scrape_pending_urls[e073f107-038b-4655-a0d1-89f47953dd67] received
[2026-03-27 19:42:26,871: INFO/MainProcess] Task tasks.scrape_pending_urls[e073f107-038b-4655-a0d1-89f47953dd67] succeeded in 0.003183600027114153s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[ade754a3-861e-4691-9417-541dfbbc6a85] received
[2026-03-27 19:42:26,878: INFO/MainProcess] Task tasks.scrape_pending_urls[ade754a3-861e-4691-9417-541dfbbc6a85] succeeded in 0.0034721000120043755s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[509e3601-ac21-4c45-ac65-fd8ec055e888] received
[2026-03-27 19:42:26,884: INFO/MainProcess] Task tasks.scrape_pending_urls[509e3601-ac21-4c45-ac65-fd8ec055e888] succeeded in 0.0036199999740347266s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[27b100a8-f0e4-4bd4-89a4-c5a52deb8937] received
[2026-03-27 19:42:26,889: INFO/MainProcess] Task tasks.scrape_pending_urls[27b100a8-f0e4-4bd4-89a4-c5a52deb8937] succeeded in 0.0030882999999448657s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,891: INFO/MainProcess] Task tasks.scrape_pending_urls[86b8522a-bba7-4f84-bc6d-fb07cdc17fb4] received
[2026-03-27 19:42:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[86b8522a-bba7-4f84-bc6d-fb07cdc17fb4] succeeded in 0.0028156000189483166s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,896: INFO/MainProcess] Task tasks.scrape_pending_urls[975b2463-ca5e-4acb-9edb-3873a756848d] received
[2026-03-27 19:42:26,899: INFO/MainProcess] Task tasks.scrape_pending_urls[975b2463-ca5e-4acb-9edb-3873a756848d] succeeded in 0.0025730000343173742s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[2079e9d6-8447-4de9-a6d6-4e624e02d357] received
[2026-03-27 19:42:26,903: INFO/MainProcess] Task tasks.scrape_pending_urls[2079e9d6-8447-4de9-a6d6-4e624e02d357] succeeded in 0.0025381000014021993s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[2d68af60-f3d9-4673-bbe0-e68a2f78238d] received
[2026-03-27 19:42:26,910: INFO/MainProcess] Task tasks.scrape_pending_urls[2d68af60-f3d9-4673-bbe0-e68a2f78238d] succeeded in 0.00365059997420758s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[ab329078-3579-4991-aa8e-e8948a83c52a] received
[2026-03-27 19:42:26,914: INFO/MainProcess] Task tasks.scrape_pending_urls[ab329078-3579-4991-aa8e-e8948a83c52a] succeeded in 0.0026280999882146716s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,916: INFO/MainProcess] Task tasks.scrape_pending_urls[5375040b-b3c8-48e0-8275-e726f43cd5c5] received
[2026-03-27 19:42:26,919: INFO/MainProcess] Task tasks.scrape_pending_urls[5375040b-b3c8-48e0-8275-e726f43cd5c5] succeeded in 0.0025218999944627285s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,920: INFO/MainProcess] Task tasks.scrape_pending_urls[ca80759e-c90e-43fb-a06a-b305e6f0d1ac] received
[2026-03-27 19:42:26,926: INFO/MainProcess] Task tasks.scrape_pending_urls[ca80759e-c90e-43fb-a06a-b305e6f0d1ac] succeeded in 0.0052779000252485275s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,929: INFO/MainProcess] Task tasks.scrape_pending_urls[7e96243a-079f-49ce-a7ec-bf4e191a8d2d] received
[2026-03-27 19:42:26,933: INFO/MainProcess] Task tasks.scrape_pending_urls[7e96243a-079f-49ce-a7ec-bf4e191a8d2d] succeeded in 0.0039721999783068895s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,935: INFO/MainProcess] Task tasks.scrape_pending_urls[f937249c-142f-4d78-825c-d487ecca0c15] received
[2026-03-27 19:42:26,941: INFO/MainProcess] Task tasks.scrape_pending_urls[f937249c-142f-4d78-825c-d487ecca0c15] succeeded in 0.005280000041238964s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,943: INFO/MainProcess] Task tasks.scrape_pending_urls[128e2487-b681-4d07-992b-83697c3f3e17] received
[2026-03-27 19:42:26,948: INFO/MainProcess] Task tasks.scrape_pending_urls[128e2487-b681-4d07-992b-83697c3f3e17] succeeded in 0.003977699903771281s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,950: INFO/MainProcess] Task tasks.scrape_pending_urls[fea25d81-b72e-4427-93c7-eeaec8a88519] received
[2026-03-27 19:42:26,954: INFO/MainProcess] Task tasks.scrape_pending_urls[fea25d81-b72e-4427-93c7-eeaec8a88519] succeeded in 0.004279499989934266s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,956: INFO/MainProcess] Task tasks.scrape_pending_urls[f8a2757f-3ea2-40c1-9518-c4084671aec9] received
[2026-03-27 19:42:26,959: INFO/MainProcess] Task tasks.scrape_pending_urls[f8a2757f-3ea2-40c1-9518-c4084671aec9] succeeded in 0.002750699990428984s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,961: INFO/MainProcess] Task tasks.scrape_pending_urls[95dfd24b-f713-4d42-88a7-775ccd4c2b0f] received
[2026-03-27 19:42:26,964: INFO/MainProcess] Task tasks.scrape_pending_urls[95dfd24b-f713-4d42-88a7-775ccd4c2b0f] succeeded in 0.0025928999530151486s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,965: INFO/MainProcess] Task tasks.scrape_pending_urls[be632a2a-262f-4fa7-b8ec-7957a06bb885] received
[2026-03-27 19:42:26,968: INFO/MainProcess] Task tasks.scrape_pending_urls[be632a2a-262f-4fa7-b8ec-7957a06bb885] succeeded in 0.0026169000193476677s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,971: INFO/MainProcess] Task tasks.scrape_pending_urls[3d40e6fd-4668-4db0-b0e3-1c8e03cc43fc] received
[2026-03-27 19:42:26,974: INFO/MainProcess] Task tasks.scrape_pending_urls[3d40e6fd-4668-4db0-b0e3-1c8e03cc43fc] succeeded in 0.003097799955867231s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,976: INFO/MainProcess] Task tasks.scrape_pending_urls[22bd777f-2a8d-4837-98ab-efa8cc368e26] received
[2026-03-27 19:42:26,979: INFO/MainProcess] Task tasks.scrape_pending_urls[22bd777f-2a8d-4837-98ab-efa8cc368e26] succeeded in 0.002740600029937923s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,980: INFO/MainProcess] Task tasks.scrape_pending_urls[de4223a9-e375-4977-9296-2018594ef242] received
[2026-03-27 19:42:26,983: INFO/MainProcess] Task tasks.scrape_pending_urls[de4223a9-e375-4977-9296-2018594ef242] succeeded in 0.002154399990104139s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,984: INFO/MainProcess] Task tasks.scrape_pending_urls[81cefb36-104a-4d2e-a8cf-2ab7a19c113d] received
[2026-03-27 19:42:26,989: INFO/MainProcess] Task tasks.scrape_pending_urls[81cefb36-104a-4d2e-a8cf-2ab7a19c113d] succeeded in 0.0033684000372886658s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,991: INFO/MainProcess] Task tasks.scrape_pending_urls[b35fe385-73d5-4740-80c4-74bc33cd371c] received
[2026-03-27 19:42:26,993: INFO/MainProcess] Task tasks.scrape_pending_urls[b35fe385-73d5-4740-80c4-74bc33cd371c] succeeded in 0.002280500018969178s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,994: INFO/MainProcess] Task tasks.scrape_pending_urls[4a110a5a-e022-4cd0-8631-e21ea2ccfe31] received
[2026-03-27 19:42:26,997: INFO/MainProcess] Task tasks.scrape_pending_urls[4a110a5a-e022-4cd0-8631-e21ea2ccfe31] succeeded in 0.002081100014038384s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:26,998: INFO/MainProcess] Task tasks.scrape_pending_urls[c5738abb-8994-4adf-ac2a-23e57272e6b8] received
[2026-03-27 19:42:27,001: INFO/MainProcess] Task tasks.scrape_pending_urls[c5738abb-8994-4adf-ac2a-23e57272e6b8] succeeded in 0.003096100059337914s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,003: INFO/MainProcess] Task tasks.scrape_pending_urls[0b28e83e-da4e-4178-98a2-74e0a574a057] received
[2026-03-27 19:42:27,005: INFO/MainProcess] Task tasks.scrape_pending_urls[0b28e83e-da4e-4178-98a2-74e0a574a057] succeeded in 0.002272099955007434s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,007: INFO/MainProcess] Task tasks.scrape_pending_urls[f0a6c5cc-ec3e-489b-8ff7-4effd08eb2a7] received
[2026-03-27 19:42:27,009: INFO/MainProcess] Task tasks.scrape_pending_urls[f0a6c5cc-ec3e-489b-8ff7-4effd08eb2a7] succeeded in 0.002151499968022108s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,010: INFO/MainProcess] Task tasks.scrape_pending_urls[aa4141ca-e634-46dd-a8d2-fdf0739d4d69] received
[2026-03-27 19:42:27,012: INFO/MainProcess] Task tasks.scrape_pending_urls[aa4141ca-e634-46dd-a8d2-fdf0739d4d69] succeeded in 0.0021285999100655317s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,014: INFO/MainProcess] Task tasks.scrape_pending_urls[7aef1389-036c-4b48-ad32-b62c0c0f2cd9] received
[2026-03-27 19:42:27,016: INFO/MainProcess] Task tasks.scrape_pending_urls[7aef1389-036c-4b48-ad32-b62c0c0f2cd9] succeeded in 0.0021160999312996864s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,019: INFO/MainProcess] Task tasks.scrape_pending_urls[73c89477-5572-4479-b494-839909763735] received
[2026-03-27 19:42:27,022: INFO/MainProcess] Task tasks.scrape_pending_urls[73c89477-5572-4479-b494-839909763735] succeeded in 0.002910599927417934s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,024: INFO/MainProcess] Task tasks.scrape_pending_urls[aead128f-ae9f-4eff-ae47-e1c4158b3d82] received
[2026-03-27 19:42:27,026: INFO/MainProcess] Task tasks.scrape_pending_urls[aead128f-ae9f-4eff-ae47-e1c4158b3d82] succeeded in 0.002270700060762465s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,027: INFO/MainProcess] Task tasks.scrape_pending_urls[8da21628-23ef-4e0f-b8c8-a920f077800e] received
[2026-03-27 19:42:27,030: INFO/MainProcess] Task tasks.scrape_pending_urls[8da21628-23ef-4e0f-b8c8-a920f077800e] succeeded in 0.0021723000099882483s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,031: INFO/MainProcess] Task tasks.scrape_pending_urls[678cfb57-188c-481d-9f18-fabf8aef2ec5] received
[2026-03-27 19:42:27,035: INFO/MainProcess] Task tasks.scrape_pending_urls[678cfb57-188c-481d-9f18-fabf8aef2ec5] succeeded in 0.003586200065910816s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,036: INFO/MainProcess] Task tasks.scrape_pending_urls[dbcf8c56-275e-418b-b8e7-0c2ca770890c] received
[2026-03-27 19:42:27,039: INFO/MainProcess] Task tasks.scrape_pending_urls[dbcf8c56-275e-418b-b8e7-0c2ca770890c] succeeded in 0.002236599917523563s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,040: INFO/MainProcess] Task tasks.scrape_pending_urls[ad00d17c-14f8-43c3-8fd7-3fa7e532c1d2] received
[2026-03-27 19:42:27,042: INFO/MainProcess] Task tasks.scrape_pending_urls[ad00d17c-14f8-43c3-8fd7-3fa7e532c1d2] succeeded in 0.0021469000494107604s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,044: INFO/MainProcess] Task tasks.scrape_pending_urls[f41d138f-7780-432e-acc3-3dbbd9892fc3] received
[2026-03-27 19:42:27,046: INFO/MainProcess] Task tasks.scrape_pending_urls[f41d138f-7780-432e-acc3-3dbbd9892fc3] succeeded in 0.002600100007839501s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,048: INFO/MainProcess] Task tasks.scrape_pending_urls[43129f19-1cfe-4c4a-acef-e1f0d29bda17] received
[2026-03-27 19:42:27,052: INFO/MainProcess] Task tasks.scrape_pending_urls[43129f19-1cfe-4c4a-acef-e1f0d29bda17] succeeded in 0.0026166000170633197s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,053: INFO/MainProcess] Task tasks.scrape_pending_urls[1e862272-458d-47b9-9f84-f2d1ceaf70b5] received
[2026-03-27 19:42:27,056: INFO/MainProcess] Task tasks.scrape_pending_urls[1e862272-458d-47b9-9f84-f2d1ceaf70b5] succeeded in 0.002348800073377788s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,057: INFO/MainProcess] Task tasks.scrape_pending_urls[95704510-d801-4522-aa83-a0f7360746e7] received
[2026-03-27 19:42:27,060: INFO/MainProcess] Task tasks.scrape_pending_urls[95704510-d801-4522-aa83-a0f7360746e7] succeeded in 0.0022767999907955527s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,061: INFO/MainProcess] Task tasks.scrape_pending_urls[15ca45dc-4de1-49a2-8ebf-1aacde5d5baf] received
[2026-03-27 19:42:27,063: INFO/MainProcess] Task tasks.scrape_pending_urls[15ca45dc-4de1-49a2-8ebf-1aacde5d5baf] succeeded in 0.002237799926660955s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,066: INFO/MainProcess] Task tasks.scrape_pending_urls[f7d78dd6-7226-443c-adfa-c232dee7f193] received
[2026-03-27 19:42:27,069: INFO/MainProcess] Task tasks.scrape_pending_urls[f7d78dd6-7226-443c-adfa-c232dee7f193] succeeded in 0.002948800101876259s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,071: INFO/MainProcess] Task tasks.scrape_pending_urls[ea4713a1-572e-47a7-b706-a5d5126487a4] received
[2026-03-27 19:42:27,073: INFO/MainProcess] Task tasks.scrape_pending_urls[ea4713a1-572e-47a7-b706-a5d5126487a4] succeeded in 0.002361200051382184s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,075: INFO/MainProcess] Task tasks.scrape_pending_urls[8346c269-0724-40ae-bfee-d56298e978a6] received
[2026-03-27 19:42:27,077: INFO/MainProcess] Task tasks.scrape_pending_urls[8346c269-0724-40ae-bfee-d56298e978a6] succeeded in 0.0022316999966278672s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,079: INFO/MainProcess] Task tasks.scrape_pending_urls[bfd56c27-7a4b-4197-84a9-b2a5e16bf89e] received
[2026-03-27 19:42:27,083: INFO/MainProcess] Task tasks.scrape_pending_urls[bfd56c27-7a4b-4197-84a9-b2a5e16bf89e] succeeded in 0.00372919999063015s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,084: INFO/MainProcess] Task tasks.scrape_pending_urls[8ffa46b7-91f3-43c2-99e8-6acfada9d407] received
[2026-03-27 19:42:27,087: INFO/MainProcess] Task tasks.scrape_pending_urls[8ffa46b7-91f3-43c2-99e8-6acfada9d407] succeeded in 0.0023458999348804355s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,088: INFO/MainProcess] Task tasks.scrape_pending_urls[9db1f911-e3b0-4b16-b3cb-f01283a949ff] received
[2026-03-27 19:42:27,091: INFO/MainProcess] Task tasks.scrape_pending_urls[9db1f911-e3b0-4b16-b3cb-f01283a949ff] succeeded in 0.0022392000537365675s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,092: INFO/MainProcess] Task tasks.scrape_pending_urls[34cd0962-999d-4ffe-a462-1fd59b594f82] received
[2026-03-27 19:42:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[34cd0962-999d-4ffe-a462-1fd59b594f82] succeeded in 0.002675299998372793s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,097: INFO/MainProcess] Task tasks.scrape_pending_urls[faee43bb-5b13-4ff7-8d36-66a47c67dd22] received
[2026-03-27 19:42:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[faee43bb-5b13-4ff7-8d36-66a47c67dd22] succeeded in 0.0026144000003114343s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,101: INFO/MainProcess] Task tasks.scrape_pending_urls[fc79b4c2-829d-4664-bbdd-e1b920337e8e] received
[2026-03-27 19:42:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[fc79b4c2-829d-4664-bbdd-e1b920337e8e] succeeded in 0.0024645000230520964s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,105: INFO/MainProcess] Task tasks.scrape_pending_urls[de20220a-6c7c-4fa4-8cba-c4775894bedc] received
[2026-03-27 19:42:27,108: INFO/MainProcess] Task tasks.scrape_pending_urls[de20220a-6c7c-4fa4-8cba-c4775894bedc] succeeded in 0.0023727999068796635s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[bd54cb77-ec8b-4123-96d5-846eb02d89fc] received
[2026-03-27 19:42:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[bd54cb77-ec8b-4123-96d5-846eb02d89fc] succeeded in 0.0025267000310122967s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,115: INFO/MainProcess] Task tasks.scrape_pending_urls[29dfa5aa-764f-43db-807c-688c7a0fd4bf] received
[2026-03-27 19:42:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[29dfa5aa-764f-43db-807c-688c7a0fd4bf] succeeded in 0.0028103000950068235s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,119: INFO/MainProcess] Task tasks.scrape_pending_urls[81f82649-fa18-46ce-8db2-00f4c6ddf143] received
[2026-03-27 19:42:27,122: INFO/MainProcess] Task tasks.scrape_pending_urls[81f82649-fa18-46ce-8db2-00f4c6ddf143] succeeded in 0.0022412999533116817s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,123: INFO/MainProcess] Task tasks.scrape_pending_urls[1970105a-d227-4431-8cbc-3cd11911c446] received
[2026-03-27 19:42:27,125: INFO/MainProcess] Task tasks.scrape_pending_urls[1970105a-d227-4431-8cbc-3cd11911c446] succeeded in 0.002127800020389259s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,126: INFO/MainProcess] Task tasks.scrape_pending_urls[b0b833c2-4418-465b-8228-c2a1d8d64003] received
[2026-03-27 19:42:27,129: INFO/MainProcess] Task tasks.scrape_pending_urls[b0b833c2-4418-465b-8228-c2a1d8d64003] succeeded in 0.0027046999894082546s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,130: INFO/MainProcess] Task tasks.scrape_pending_urls[24954ddc-6a3c-41e8-9f84-3e04b9eea447] received
[2026-03-27 19:42:27,133: INFO/MainProcess] Task tasks.scrape_pending_urls[24954ddc-6a3c-41e8-9f84-3e04b9eea447] succeeded in 0.0021970000816509128s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,134: INFO/MainProcess] Task tasks.scrape_pending_urls[e3461c90-d8eb-4717-95c3-ca0dad07b51d] received
[2026-03-27 19:42:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[e3461c90-d8eb-4717-95c3-ca0dad07b51d] succeeded in 0.0020884000696241856s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,137: INFO/MainProcess] Task tasks.scrape_pending_urls[2fc5c742-3f3a-4067-a906-1a8ba5f9d15f] received
[2026-03-27 19:42:27,140: INFO/MainProcess] Task tasks.scrape_pending_urls[2fc5c742-3f3a-4067-a906-1a8ba5f9d15f] succeeded in 0.0024887999752536416s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[3d5b698a-ae58-49cb-9fab-a5bd67a4e117] received
[2026-03-27 19:42:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[3d5b698a-ae58-49cb-9fab-a5bd67a4e117] succeeded in 0.003005499951541424s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,146: INFO/MainProcess] Task tasks.scrape_pending_urls[316d1731-bd09-4277-9a7a-2b50a71323c5] received
[2026-03-27 19:42:27,148: INFO/MainProcess] Task tasks.scrape_pending_urls[316d1731-bd09-4277-9a7a-2b50a71323c5] succeeded in 0.0022236000513657928s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,150: INFO/MainProcess] Task tasks.scrape_pending_urls[339a389c-2eda-4b4c-bd50-f24a0d67354f] received
[2026-03-27 19:42:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[339a389c-2eda-4b4c-bd50-f24a0d67354f] succeeded in 0.00207290006801486s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[940f3985-9f4a-4fe6-92a4-86e1b7f9b30c] received
[2026-03-27 19:42:27,155: INFO/MainProcess] Task tasks.scrape_pending_urls[940f3985-9f4a-4fe6-92a4-86e1b7f9b30c] succeeded in 0.0020800000056624413s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[434a60ed-a212-4ef5-b219-0fbe5ba3a664] received
[2026-03-27 19:42:27,159: INFO/MainProcess] Task tasks.scrape_pending_urls[434a60ed-a212-4ef5-b219-0fbe5ba3a664] succeeded in 0.0027414000360295177s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,163: INFO/MainProcess] Task tasks.scrape_pending_urls[44f1557a-a92d-4a24-a4f7-0ac324034208] received
[2026-03-27 19:42:27,166: INFO/MainProcess] Task tasks.scrape_pending_urls[44f1557a-a92d-4a24-a4f7-0ac324034208] succeeded in 0.002926299930550158s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[140d2871-2d5e-47b5-8b46-df439be6b5c7] received
[2026-03-27 19:42:27,170: INFO/MainProcess] Task tasks.scrape_pending_urls[140d2871-2d5e-47b5-8b46-df439be6b5c7] succeeded in 0.0027694000164046884s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,172: INFO/MainProcess] Task tasks.scrape_pending_urls[fb7a8501-48f9-4ea3-b2b4-83ec291749e1] received
[2026-03-27 19:42:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[fb7a8501-48f9-4ea3-b2b4-83ec291749e1] succeeded in 0.002647999906912446s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,179: INFO/MainProcess] Task tasks.scrape_pending_urls[fd0582fb-b9f7-4e99-ac9b-6daed01af14b] received
[2026-03-27 19:42:27,183: INFO/MainProcess] Task tasks.scrape_pending_urls[fd0582fb-b9f7-4e99-ac9b-6daed01af14b] succeeded in 0.0035129000898450613s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,185: INFO/MainProcess] Task tasks.scrape_pending_urls[93bbcc42-98a8-4573-84db-7805427db2ca] received
[2026-03-27 19:42:27,188: INFO/MainProcess] Task tasks.scrape_pending_urls[93bbcc42-98a8-4573-84db-7805427db2ca] succeeded in 0.0027974999975413084s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,190: INFO/MainProcess] Task tasks.scrape_pending_urls[fd678ee5-3fe4-4e12-af2a-0d94a3eb585f] received
[2026-03-27 19:42:27,194: INFO/MainProcess] Task tasks.scrape_pending_urls[fd678ee5-3fe4-4e12-af2a-0d94a3eb585f] succeeded in 0.004164500045590103s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,196: INFO/MainProcess] Task tasks.scrape_pending_urls[efca5d05-23f0-466f-aa66-7de4b17eb85a] received
[2026-03-27 19:42:27,199: INFO/MainProcess] Task tasks.scrape_pending_urls[efca5d05-23f0-466f-aa66-7de4b17eb85a] succeeded in 0.0030290998984128237s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,201: INFO/MainProcess] Task tasks.scrape_pending_urls[00b8dff1-0b96-41d1-812a-da6d639bfb1f] received
[2026-03-27 19:42:27,204: INFO/MainProcess] Task tasks.scrape_pending_urls[00b8dff1-0b96-41d1-812a-da6d639bfb1f] succeeded in 0.0027571999235078692s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,205: INFO/MainProcess] Task tasks.scrape_pending_urls[ce42741f-fdd1-4536-ac8d-301d33dfc07e] received
[2026-03-27 19:42:27,209: INFO/MainProcess] Task tasks.scrape_pending_urls[ce42741f-fdd1-4536-ac8d-301d33dfc07e] succeeded in 0.002956799929961562s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,210: INFO/MainProcess] Task tasks.scrape_pending_urls[8020b1c8-d992-4c17-9b53-6ac98e8e3857] received
[2026-03-27 19:42:27,213: INFO/MainProcess] Task tasks.scrape_pending_urls[8020b1c8-d992-4c17-9b53-6ac98e8e3857] succeeded in 0.0026563999708741903s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,214: INFO/MainProcess] Task tasks.scrape_pending_urls[3b32eaf1-a786-4a9e-a5e5-a6c482ee9b58] received
[2026-03-27 19:42:27,217: INFO/MainProcess] Task tasks.scrape_pending_urls[3b32eaf1-a786-4a9e-a5e5-a6c482ee9b58] succeeded in 0.002112400019541383s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,218: INFO/MainProcess] Task tasks.scrape_pending_urls[0cf40ece-b983-46dc-8fc9-7e79672082ff] received
[2026-03-27 19:42:27,220: INFO/MainProcess] Task tasks.scrape_pending_urls[0cf40ece-b983-46dc-8fc9-7e79672082ff] succeeded in 0.0020794000010937452s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,221: INFO/MainProcess] Task tasks.scrape_pending_urls[822b7594-174e-46a5-85b2-e43a88631e21] received
[2026-03-27 19:42:27,225: INFO/MainProcess] Task tasks.scrape_pending_urls[822b7594-174e-46a5-85b2-e43a88631e21] succeeded in 0.0031231000320985913s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,226: INFO/MainProcess] Task tasks.scrape_pending_urls[71a3d13d-dde6-4b2b-ae0d-dbe62bd097d8] received
[2026-03-27 19:42:27,229: INFO/MainProcess] Task tasks.scrape_pending_urls[71a3d13d-dde6-4b2b-ae0d-dbe62bd097d8] succeeded in 0.002234900020994246s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,230: INFO/MainProcess] Task tasks.scrape_pending_urls[86d28178-d687-4cea-a302-5334d1a1e901] received
[2026-03-27 19:42:27,232: INFO/MainProcess] Task tasks.scrape_pending_urls[86d28178-d687-4cea-a302-5334d1a1e901] succeeded in 0.0025007999502122402s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,234: INFO/MainProcess] Task tasks.scrape_pending_urls[c9a541a0-b39e-4f69-a883-2a35d253a22e] received
[2026-03-27 19:42:27,236: INFO/MainProcess] Task tasks.scrape_pending_urls[c9a541a0-b39e-4f69-a883-2a35d253a22e] succeeded in 0.0022238000528886914s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,237: INFO/MainProcess] Task tasks.scrape_pending_urls[88ec6905-7f72-4859-acfb-5ee0394f4eb4] received
[2026-03-27 19:42:27,240: INFO/MainProcess] Task tasks.scrape_pending_urls[88ec6905-7f72-4859-acfb-5ee0394f4eb4] succeeded in 0.002522299997508526s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,241: INFO/MainProcess] Task tasks.scrape_pending_urls[fe77f4a6-7950-4f47-aae6-a0b7d255fe27] received
[2026-03-27 19:42:27,244: INFO/MainProcess] Task tasks.scrape_pending_urls[fe77f4a6-7950-4f47-aae6-a0b7d255fe27] succeeded in 0.002181699965149164s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,245: INFO/MainProcess] Task tasks.scrape_pending_urls[05b31793-ab99-4f4a-9689-81a5e8db4d7a] received
[2026-03-27 19:42:27,247: INFO/MainProcess] Task tasks.scrape_pending_urls[05b31793-ab99-4f4a-9689-81a5e8db4d7a] succeeded in 0.0020584999583661556s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,248: INFO/MainProcess] Task tasks.scrape_pending_urls[abe57a47-aa4b-4ef2-86e6-2ef6dc0c2a01] received
[2026-03-27 19:42:27,251: INFO/MainProcess] Task tasks.scrape_pending_urls[abe57a47-aa4b-4ef2-86e6-2ef6dc0c2a01] succeeded in 0.002063599997200072s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,252: INFO/MainProcess] Task tasks.scrape_pending_urls[f84b127e-6662-4653-9992-7ede19b1505c] received
[2026-03-27 19:42:27,255: INFO/MainProcess] Task tasks.scrape_pending_urls[f84b127e-6662-4653-9992-7ede19b1505c] succeeded in 0.0033134999684989452s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,257: INFO/MainProcess] Task tasks.scrape_pending_urls[85d11566-6302-4334-8554-a5d1f6674950] received
[2026-03-27 19:42:27,260: INFO/MainProcess] Task tasks.scrape_pending_urls[85d11566-6302-4334-8554-a5d1f6674950] succeeded in 0.0023590000346302986s: {'status': 'idle', 'pending': 0}
[2026-03-27 19:42:27,261: INFO/MainProcess] Task tasks.scrape_pending_urls[ce4621e7-9e7a-41f5-b861-f01e04b50594] received
[2026-03-27 19:42:27,264: INFO/MainProcess] Task tasks.scrape_pending_urls[ce4621e7-9e7a-41f5-b861-f01e04b50594] succeeded in 0.00212009996175766s: {'status': 'idle', 'pending': 0}
