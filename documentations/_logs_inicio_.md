
===  BookingScraper Celery Worker  ===


 -------------- worker@HOUSE v5.4.0 (opalescent)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0 2026-03-29 03:43:57
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         bookingscraper:0x1ac457f8830
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

[2026-03-29 03:43:59,187: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-29 03:44:01,233: INFO/MainProcess] mingle: searching for neighbors
[2026-03-29 03:44:08,367: INFO/MainProcess] mingle: all alone
[2026-03-29 03:44:18,610: INFO/MainProcess] worker@HOUSE ready.
[2026-03-29 03:44:32,810: INFO/MainProcess] Task tasks.scrape_pending_urls[0dae15c3-8cf4-4de9-a02a-56bbec8cbf9e] received
[2026-03-29 03:44:35,047: INFO/MainProcess] Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5
[2026-03-29 03:44:35,150: INFO/MainProcess] Task tasks.scrape_pending_urls[0dae15c3-8cf4-4de9-a02a-56bbec8cbf9e] succeeded in 2.3399221999570727s: {'status': 'idle', 'pending': 0}
[2026-03-29 03:44:56,641: INFO/MainProcess] Task tasks.scrape_pending_urls[c7da86e2-0a33-4f85-85e2-c3b6a6390265] received
[2026-03-29 03:44:56,645: INFO/MainProcess] Task tasks.scrape_pending_urls[c7da86e2-0a33-4f85-85e2-c3b6a6390265] succeeded in 0.003329999977722764s: {'status': 'idle', 'pending': 0}
[2026-03-29 03:45:26,641: INFO/MainProcess] Task tasks.scrape_pending_urls[a9226231-8b3a-4b9f-ae64-55a0e0b7e4fc] received
[2026-03-29 03:45:28,658: INFO/MainProcess] scrape_pending_urls: starting auto-batch, pending=13
[2026-03-29 03:45:29,516: INFO/MainProcess] VPN: original IP = 45.88.190.214
[2026-03-29 03:45:30,364: INFO/MainProcess] VPN: home country detected = CA
[2026-03-29 03:45:30,366: INFO/MainProcess] NordVPNManager initialised | interactive=False | original_ip=45.88.190.214 | home_country=CA
[2026-03-29 03:45:30,366: INFO/MainProcess] ScraperService INIT | VPN_ENABLED=True | HEADLESS_BROWSER=False | workers=2 | languages=en,es,de,it,fr,pt | vpn_interval=50s | vpn_countries=Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden
[2026-03-29 03:45:30,391: INFO/MainProcess] VPN: excluding home country CA from pool — remaining: ES,DE,FR,NL,IT,SE
[2026-03-29 03:45:30,391: INFO/MainProcess] VPN: connecting to France (FR)...
[2026-03-29 03:45:51,556: INFO/MainProcess] VPN connected to France — IP: 185.81.125.218
[2026-03-29 03:45:51,556: INFO/MainProcess] VPN connected OK before batch start.
[2026-03-29 03:45:51,558: INFO/MainProcess] Dispatching batch: urls=13 workers=2
[2026-03-29 03:45:51,559: INFO/MainProcess] Redis connection pool created: max_connections=20
[2026-03-29 03:45:56,555: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:45:56,626: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:07,506: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:08,177: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:12,096: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:12,370: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:23,567: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:24,256: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:30,222: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:30,455: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:43,112: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:43,112: INFO/MainProcess] CloudScraper failed for 2ee0f35c-618b-426a-b01b-f61d9c89988f/en — trying Selenium.
[2026-03-29 03:46:43,776: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 03:46:43,777: INFO/MainProcess] CloudScraper failed for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe/en — trying Selenium.
[2026-03-29 03:46:45,979: INFO/MainProcess] Selenium: Brave started
[2026-03-29 03:49:11,551: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 03:49:13,509: INFO/MainProcess] Gallery: 137 images loaded after scroll
[2026-03-29 03:49:16,824: INFO/MainProcess] Gallery: 144 unique image URLs extracted
[2026-03-29 03:49:16,976: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 03:49:16,977: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 03:49:43,117: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 2ee0f35c-618b-426a-b01b-f61d9c89988f
[2026-03-29 03:49:51,062: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 92f5182c-e6de-4277-9732-880b796eaf04
[2026-03-29 03:49:51,062: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 92f5182c-e6de-4277-9732-880b796eaf04
[2026-03-29 03:49:51,071: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f lang=en: SUCCESS
[2026-03-29 03:49:53,808: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 03:50:03,797: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 03:50:08,376: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 03:50:17,552: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 03:50:23,982: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 03:50:36,128: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 03:50:36,129: INFO/MainProcess] CloudScraper failed for 2ee0f35c-618b-426a-b01b-f61d9c89988f/es — trying Selenium.
[2026-03-29 03:52:05,666: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 03:52:07,589: INFO/MainProcess] Gallery: 131 images loaded after scroll
[2026-03-29 03:52:11,072: INFO/MainProcess] Gallery: 138 unique image URLs extracted
[2026-03-29 03:52:11,202: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 03:52:11,203: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 03:52:36,865: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe
[2026-03-29 03:52:45,886: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 6b2bd834-f6ff-460c-9356-e39c1a5d45ae
[2026-03-29 03:52:45,886: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 6b2bd834-f6ff-460c-9356-e39c1a5d45ae
[2026-03-29 03:52:45,896: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe lang=en: SUCCESS
[2026-03-29 03:52:48,601: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 03:53:03,249: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 03:53:08,010: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 03:53:29,055: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 03:53:35,192: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 03:53:56,436: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f lang=es: SUCCESS
[2026-03-29 03:53:58,535: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 03:53:58,535: INFO/MainProcess] CloudScraper failed for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe/es — trying Selenium.
[2026-03-29 03:53:59,458: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 03:54:08,772: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 03:54:13,497: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 03:54:28,393: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 03:54:34,604: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 03:54:46,198: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 03:54:46,198: INFO/MainProcess] CloudScraper failed for 2ee0f35c-618b-426a-b01b-f61d9c89988f/de — trying Selenium.
[2026-03-29 03:55:17,946: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe lang=es: SUCCESS
[2026-03-29 03:55:20,725: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 03:55:41,999: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 03:55:46,628: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 03:55:55,968: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 03:56:02,158: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 03:56:13,163: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 03:56:13,164: INFO/MainProcess] CloudScraper failed for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe/de — trying Selenium.
[2026-03-29 03:56:35,053: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f lang=de: SUCCESS
[2026-03-29 03:56:37,896: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 03:56:46,474: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 03:56:51,123: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 03:57:03,269: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 03:57:09,459: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 03:57:20,748: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 03:57:20,749: INFO/MainProcess] CloudScraper failed for 2ee0f35c-618b-426a-b01b-f61d9c89988f/it — trying Selenium.
[2026-03-29 03:58:06,591: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe lang=de: SUCCESS
[2026-03-29 03:58:09,268: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 03:58:17,833: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 03:58:22,456: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 03:58:52,425: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 03:58:58,552: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 03:59:26,102: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f lang=it: SUCCESS
[2026-03-29 03:59:28,187: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 03:59:28,188: INFO/MainProcess] CloudScraper failed for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe/it — trying Selenium.
[2026-03-29 03:59:28,806: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 03:59:41,739: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 03:59:46,385: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 04:00:11,281: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 04:00:17,406: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 04:00:46,011: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe lang=it: SUCCESS
[2026-03-29 04:00:48,627: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 04:00:57,176: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 04:00:57,176: INFO/MainProcess] CloudScraper failed for 2ee0f35c-618b-426a-b01b-f61d9c89988f/fr — trying Selenium.
[2026-03-29 04:01:16,945: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 04:01:21,652: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 04:01:31,446: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 04:01:37,831: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 04:02:12,425: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 04:02:12,426: INFO/MainProcess] CloudScraper failed for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe/fr — trying Selenium.
[2026-03-29 04:02:15,632: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f lang=fr: SUCCESS
[2026-03-29 04:02:18,279: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:02:40,384: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:02:45,193: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:02:54,739: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:03:00,972: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:03:27,862: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:03:27,862: INFO/MainProcess] CloudScraper failed for 2ee0f35c-618b-426a-b01b-f61d9c89988f/pt — trying Selenium.
[2026-03-29 04:03:34,661: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe lang=fr: SUCCESS
[2026-03-29 04:03:37,342: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:03:52,264: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:03:57,529: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:04:09,132: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:04:15,344: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:04:27,877: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 04:04:27,878: INFO/MainProcess] CloudScraper failed for d1b326ef-52b2-4acb-945d-9f69ca1b3ffe/pt — trying Selenium.
[2026-03-29 04:04:53,335: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f lang=pt: SUCCESS
[2026-03-29 04:04:53,339: INFO/MainProcess] URL 2ee0f35c-618b-426a-b01b-f61d9c89988f: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 04:04:56,000: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 04:05:08,568: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 04:05:13,256: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 04:05:23,600: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 04:05:29,794: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 04:05:44,487: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 04:05:44,487: INFO/MainProcess] CloudScraper failed for c20c2f07-c8b4-4a35-b070-63c17ee2f54f/en — trying Selenium.
[2026-03-29 04:06:25,840: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe lang=pt: SUCCESS
[2026-03-29 04:06:25,842: INFO/MainProcess] URL d1b326ef-52b2-4acb-945d-9f69ca1b3ffe: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 04:06:28,484: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 04:06:36,893: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 04:06:41,597: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 04:06:52,213: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 04:06:58,415: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 04:07:06,665: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 04:07:06,665: INFO/MainProcess] CloudScraper failed for 6cba877d-e641-49c7-abc9-5c535a2a3ecf/en — trying Selenium.
[2026-03-29 04:08:46,906: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 04:08:48,824: INFO/MainProcess] Gallery: 87 images loaded after scroll
[2026-03-29 04:08:51,263: INFO/MainProcess] Gallery: 94 unique image URLs extracted
[2026-03-29 04:08:51,396: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 04:08:51,397: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 04:09:17,524: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for c20c2f07-c8b4-4a35-b070-63c17ee2f54f
[2026-03-29 04:09:25,461: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel de0ff309-ca95-4767-bb0b-d3b50eabc79e
[2026-03-29 04:09:25,461: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel de0ff309-ca95-4767-bb0b-d3b50eabc79e
[2026-03-29 04:09:25,470: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f lang=en: SUCCESS
[2026-03-29 04:09:28,410: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 04:09:37,807: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 04:09:42,477: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 04:09:56,263: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 04:10:02,459: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 04:10:17,006: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 04:10:17,007: INFO/MainProcess] CloudScraper failed for c20c2f07-c8b4-4a35-b070-63c17ee2f54f/es — trying Selenium.
[2026-03-29 04:11:39,814: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 04:11:41,794: INFO/MainProcess] Gallery: 266 images loaded after scroll
[2026-03-29 04:11:46,979: INFO/MainProcess] Gallery: 273 unique image URLs extracted
[2026-03-29 04:11:47,204: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 04:11:47,205: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 04:12:15,273: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 6cba877d-e641-49c7-abc9-5c535a2a3ecf
[2026-03-29 04:12:23,346: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel e260ae37-943c-4526-a024-77bed1cc8fcb
[2026-03-29 04:12:23,346: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel e260ae37-943c-4526-a024-77bed1cc8fcb
[2026-03-29 04:12:23,356: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf lang=en: SUCCESS
[2026-03-29 04:12:26,166: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 04:12:37,234: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 04:12:41,954: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 04:12:51,707: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 04:12:57,895: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 04:13:06,440: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 04:13:06,441: INFO/MainProcess] CloudScraper failed for 6cba877d-e641-49c7-abc9-5c535a2a3ecf/es — trying Selenium.
[2026-03-29 04:13:34,667: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f lang=es: SUCCESS
[2026-03-29 04:13:37,295: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 04:14:06,886: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 04:14:11,624: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 04:14:22,058: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 04:14:28,396: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 04:14:38,630: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 04:14:38,630: INFO/MainProcess] CloudScraper failed for c20c2f07-c8b4-4a35-b070-63c17ee2f54f/de — trying Selenium.
[2026-03-29 04:14:54,236: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf lang=es: SUCCESS
[2026-03-29 04:14:56,945: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 04:15:11,612: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 04:15:16,576: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 04:15:25,068: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 04:15:31,264: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 04:15:39,942: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 04:15:39,943: INFO/MainProcess] CloudScraper failed for 6cba877d-e641-49c7-abc9-5c535a2a3ecf/de — trying Selenium.
[2026-03-29 04:16:12,630: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f lang=de: SUCCESS
[2026-03-29 04:16:15,433: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 04:16:25,325: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 04:16:30,111: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 04:16:42,059: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 04:16:48,249: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 04:17:01,413: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 04:17:01,413: INFO/MainProcess] CloudScraper failed for c20c2f07-c8b4-4a35-b070-63c17ee2f54f/it — trying Selenium.
[2026-03-29 04:17:46,499: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf lang=de: SUCCESS
[2026-03-29 04:17:49,168: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-29 04:18:28,771: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-29 04:18:33,415: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-29 04:19:05,900: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f lang=it: SUCCESS
[2026-03-29 04:19:08,625: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-29 04:19:09,156: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-29 04:19:15,846: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-29 04:19:22,546: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-29 04:19:26,719: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-29 04:19:27,903: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-29 04:19:27,903: INFO/MainProcess] CloudScraper failed for 6cba877d-e641-49c7-abc9-5c535a2a3ecf/it — trying Selenium.
[2026-03-29 04:19:36,803: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-29 04:19:43,527: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-29 04:19:56,915: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-29 04:19:56,916: INFO/MainProcess] CloudScraper failed for c20c2f07-c8b4-4a35-b070-63c17ee2f54f/fr — trying Selenium.
[2026-03-29 04:20:47,607: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf lang=it: SUCCESS
[2026-03-29 04:20:50,290: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-29 04:21:01,164: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-29 04:21:05,850: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-29 04:21:16,084: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-29 04:21:22,296: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-29 04:21:35,481: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-29 04:21:35,482: INFO/MainProcess] CloudScraper failed for 6cba877d-e641-49c7-abc9-5c535a2a3ecf/fr — trying Selenium.
[2026-03-29 04:22:06,247: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f lang=fr: SUCCESS
[2026-03-29 04:22:08,979: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:22:19,541: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:22:24,274: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:22:35,703: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:22:41,902: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:22:53,652: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:22:53,653: INFO/MainProcess] CloudScraper failed for c20c2f07-c8b4-4a35-b070-63c17ee2f54f/pt — trying Selenium.
[2026-03-29 04:23:25,600: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf lang=fr: SUCCESS
[2026-03-29 04:23:28,352: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-29 04:23:36,735: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-29 04:23:41,400: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-29 04:23:50,458: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-29 04:23:56,646: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-29 04:24:10,769: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-29 04:24:10,770: INFO/MainProcess] CloudScraper failed for 6cba877d-e641-49c7-abc9-5c535a2a3ecf/pt — trying Selenium.
[2026-03-29 04:24:55,417: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f lang=pt: SUCCESS
[2026-03-29 04:24:55,419: INFO/MainProcess] URL c20c2f07-c8b4-4a35-b070-63c17ee2f54f: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 04:24:58,109: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-29 04:25:36,340: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-29 04:25:41,062: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-29 04:26:15,165: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf lang=pt: SUCCESS
[2026-03-29 04:26:15,167: INFO/MainProcess] URL 6cba877d-e641-49c7-abc9-5c535a2a3ecf: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 04:26:16,602: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-29 04:26:17,891: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-29 04:26:22,810: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-29 04:26:31,257: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-29 04:26:34,363: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-29 04:26:34,363: INFO/MainProcess] CloudScraper failed for d5e28bdd-ec05-46b6-82c2-dad58968aea1/en — trying Selenium.
[2026-03-29 04:26:36,221: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-29 04:26:50,359: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-29 04:26:56,556: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-29 04:27:05,928: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-29 04:27:05,929: INFO/MainProcess] CloudScraper failed for 0a677962-a7c9-4563-89d5-dcd78e545656/en — trying Selenium.
[2026-03-29 04:28:56,673: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 04:28:58,610: INFO/MainProcess] Gallery: 118 images loaded after scroll
[2026-03-29 04:29:02,329: INFO/MainProcess] Gallery: 125 unique image URLs extracted
[2026-03-29 04:29:02,516: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 04:29:02,517: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 04:29:30,365: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for d5e28bdd-ec05-46b6-82c2-dad58968aea1
[2026-03-29 04:29:37,862: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel e62bd354-eb66-4600-a8ad-e6c1b564bfea
[2026-03-29 04:29:37,862: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel e62bd354-eb66-4600-a8ad-e6c1b564bfea
[2026-03-29 04:29:37,869: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1 lang=en: SUCCESS
[2026-03-29 04:29:40,720: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-29 04:29:49,924: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-29 04:29:54,585: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-29 04:30:05,150: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-29 04:30:11,330: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-29 04:30:23,102: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-29 04:30:23,102: INFO/MainProcess] CloudScraper failed for d5e28bdd-ec05-46b6-82c2-dad58968aea1/es — trying Selenium.
[2026-03-29 04:31:51,940: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 04:31:53,822: INFO/MainProcess] Gallery: 24 images loaded after scroll
[2026-03-29 04:31:55,047: INFO/MainProcess] Gallery: 31 unique image URLs extracted
[2026-03-29 04:31:55,146: INFO/MainProcess] hotelPhotos JS: 24 photos extracted from page source
[2026-03-29 04:31:55,147: INFO/MainProcess] Gallery: 24 photos with full metadata (hotelPhotos JS)
[2026-03-29 04:32:21,294: INFO/MainProcess] Photos: 24 rich photo records (hotelPhotos JS) for 0a677962-a7c9-4563-89d5-dcd78e545656
[2026-03-29 04:32:25,708: INFO/MainProcess] download_photo_batch: 72/72 photo-files saved for hotel fb464b89-9504-4e9d-809a-45463d65b940
[2026-03-29 04:32:25,708: INFO/MainProcess] ImageDownloader (photo_batch): 72/24 photos saved for hotel fb464b89-9504-4e9d-809a-45463d65b940
[2026-03-29 04:32:25,713: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656 lang=en: SUCCESS
[2026-03-29 04:32:28,637: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-29 04:32:41,531: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-29 04:32:46,439: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-29 04:32:56,537: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-29 04:33:02,767: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-29 04:33:15,084: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-29 04:33:15,084: INFO/MainProcess] CloudScraper failed for 0a677962-a7c9-4563-89d5-dcd78e545656/es — trying Selenium.
[2026-03-29 04:33:41,462: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1 lang=es: SUCCESS
[2026-03-29 04:33:44,215: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-29 04:33:56,424: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-29 04:34:01,171: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-29 04:34:10,937: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-29 04:34:17,124: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-29 04:34:56,432: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-29 04:34:56,432: INFO/MainProcess] CloudScraper failed for d5e28bdd-ec05-46b6-82c2-dad58968aea1/de — trying Selenium.
[2026-03-29 04:34:58,829: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656 lang=es: SUCCESS
[2026-03-29 04:35:01,567: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-29 04:35:16,473: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-29 04:35:21,713: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-29 04:35:31,554: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-29 04:35:37,749: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-29 04:36:11,103: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-29 04:36:11,104: INFO/MainProcess] CloudScraper failed for 0a677962-a7c9-4563-89d5-dcd78e545656/de — trying Selenium.
[2026-03-29 04:36:16,855: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1 lang=de: SUCCESS
[2026-03-29 04:36:19,794: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-29 04:36:31,713: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-29 04:36:36,445: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-29 04:36:50,220: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-29 04:36:56,419: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-29 04:37:07,270: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-29 04:37:07,270: INFO/MainProcess] CloudScraper failed for d5e28bdd-ec05-46b6-82c2-dad58968aea1/it — trying Selenium.
[2026-03-29 04:37:46,213: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656 lang=de: SUCCESS
[2026-03-29 04:37:48,904: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-29 04:37:59,251: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-29 04:38:03,932: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-29 04:38:12,237: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-29 04:38:18,438: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-29 04:38:32,968: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-29 04:38:32,969: INFO/MainProcess] CloudScraper failed for 0a677962-a7c9-4563-89d5-dcd78e545656/it — trying Selenium.
[2026-03-29 04:39:04,731: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1 lang=it: SUCCESS
[2026-03-29 04:39:07,420: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-29 04:39:20,886: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-29 04:39:25,624: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-29 04:39:35,431: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-29 04:39:41,616: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-29 04:40:11,358: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-29 04:40:11,358: INFO/MainProcess] CloudScraper failed for d5e28bdd-ec05-46b6-82c2-dad58968aea1/fr — trying Selenium.
[2026-03-29 04:40:23,875: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656 lang=it: SUCCESS
[2026-03-29 04:40:26,522: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-29 04:40:40,065: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-29 04:40:44,818: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-29 04:40:53,559: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-29 04:40:59,748: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-29 04:41:13,989: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-29 04:41:13,990: INFO/MainProcess] CloudScraper failed for 0a677962-a7c9-4563-89d5-dcd78e545656/fr — trying Selenium.
[2026-03-29 04:41:42,634: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1 lang=fr: SUCCESS
[2026-03-29 04:41:45,488: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:42:13,522: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:42:18,231: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:42:30,857: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:42:37,037: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:42:49,209: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-29 04:42:49,211: INFO/MainProcess] CloudScraper failed for d5e28bdd-ec05-46b6-82c2-dad58968aea1/pt — trying Selenium.
[2026-03-29 04:43:12,487: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656 lang=fr: SUCCESS
[2026-03-29 04:43:15,271: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-29 04:43:29,243: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-29 04:43:34,025: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-29 04:43:45,189: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-29 04:43:51,389: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-29 04:44:04,259: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-29 04:44:04,259: INFO/MainProcess] CloudScraper failed for 0a677962-a7c9-4563-89d5-dcd78e545656/pt — trying Selenium.
[2026-03-29 04:44:31,328: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1 lang=pt: SUCCESS
[2026-03-29 04:44:31,330: INFO/MainProcess] URL d5e28bdd-ec05-46b6-82c2-dad58968aea1: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 04:44:34,073: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-29 04:44:45,832: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-29 04:44:50,588: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-29 04:44:59,665: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-29 04:45:05,853: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-29 04:45:14,553: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-29 04:45:14,553: INFO/MainProcess] CloudScraper failed for c53f0d9b-4436-4b67-8a21-7e3484439e5d/en — trying Selenium.
[2026-03-29 04:45:49,063: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656 lang=pt: SUCCESS
[2026-03-29 04:45:49,066: INFO/MainProcess] URL 0a677962-a7c9-4563-89d5-dcd78e545656: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 04:45:51,791: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:46:06,119: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:46:11,268: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:46:23,646: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:46:29,848: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:46:39,149: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:46:39,150: INFO/MainProcess] CloudScraper failed for 3420c869-fd48-4f79-9557-5e185e9e580f/en — trying Selenium.
[2026-03-29 04:48:08,926: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 04:48:10,901: INFO/MainProcess] Gallery: 144 images loaded after scroll
[2026-03-29 04:48:14,874: INFO/MainProcess] Gallery: 151 unique image URLs extracted
[2026-03-29 04:48:15,047: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 04:48:15,048: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 04:48:42,885: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for c53f0d9b-4436-4b67-8a21-7e3484439e5d
[2026-03-29 04:48:50,634: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 3acfe53f-5864-44b5-b545-d3ecc67c33d9
[2026-03-29 04:48:50,635: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 3acfe53f-5864-44b5-b545-d3ecc67c33d9
[2026-03-29 04:48:50,639: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=en: SUCCESS
[2026-03-29 04:48:53,543: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-29 04:49:15,125: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-29 04:49:20,072: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-29 04:49:32,858: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-29 04:49:39,060: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-29 04:49:48,752: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-29 04:49:48,752: INFO/MainProcess] CloudScraper failed for c53f0d9b-4436-4b67-8a21-7e3484439e5d/es — trying Selenium.
[2026-03-29 04:50:02,936: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-29 04:50:13,790: INFO/MainProcess] Selenium retry 2 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:51:49,155: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-29 04:52:02,163: INFO/MainProcess] Selenium retry 3 -- waiting 35s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:53:51,940: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-29 04:53:51,940: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:53:51,943: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 3420c869-fd48-4f79-9557-5e185e9e580f/en
[2026-03-29 04:53:51,943: INFO/MainProcess] VPN: rotating (current=FR)...
[2026-03-29 04:53:52,906: INFO/MainProcess] VPN disconnected.
[2026-03-29 04:53:57,907: INFO/MainProcess] VPN: connecting to Canada (CA)...
[2026-03-29 04:54:17,641: INFO/MainProcess] VPN connected to Canada — IP: 212.15.86.114
[2026-03-29 04:54:17,642: INFO/MainProcess] VPN rotation successful → Canada
[2026-03-29 04:54:17,644: INFO/MainProcess] VPN rotated — retrying 3420c869-fd48-4f79-9557-5e185e9e580f/en with CloudScraper.
[2026-03-29 04:54:20,502: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:54:31,771: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:54:31,771: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-29 04:55:11,753: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=es: SUCCESS
[2026-03-29 04:55:14,767: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-29 04:55:23,130: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-29 04:55:27,955: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-29 04:55:39,742: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-29 04:55:47,199: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-29 04:55:59,596: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-29 04:55:59,596: INFO/MainProcess] CloudScraper failed for c53f0d9b-4436-4b67-8a21-7e3484439e5d/de — trying Selenium.
[2026-03-29 04:56:30,269: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-29 04:56:39,278: INFO/MainProcess] Selenium retry 2 -- waiting 11s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 04:58:06,865: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-29 04:58:14,917: INFO/MainProcess] Selenium retry 3 -- waiting 32s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 05:00:03,091: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-29 05:00:03,091: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-29 05:00:03,101: WARNING/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f lang=en: FAILED
[2026-03-29 05:00:05,899: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-29 05:00:19,422: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-29 05:00:24,315: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-29 05:00:37,055: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-29 05:00:43,219: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-29 05:00:52,444: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-29 05:00:52,445: INFO/MainProcess] CloudScraper failed for 3420c869-fd48-4f79-9557-5e185e9e580f/es — trying Selenium.
[2026-03-29 05:01:23,363: WARNING/MainProcess] BUG-DB-002-FIX: No legal section found for url_id=c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=de — inserting empty record (has_legal_content=False)
[2026-03-29 05:01:23,405: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=de: SUCCESS
[2026-03-29 05:01:26,351: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:01:39,880: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:01:44,861: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:01:55,791: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:02:01,957: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:02:11,257: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:02:11,257: INFO/MainProcess] CloudScraper failed for c53f0d9b-4436-4b67-8a21-7e3484439e5d/it — trying Selenium.
[2026-03-29 05:02:41,654: WARNING/MainProcess] BUG-DB-002-FIX: No legal section found for url_id=3420c869-fd48-4f79-9557-5e185e9e580f lang=es — inserting empty record (has_legal_content=False)
[2026-03-29 05:02:41,743: INFO/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f lang=es: SUCCESS
[2026-03-29 05:02:44,583: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:02:56,248: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:03:01,213: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:03:15,899: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:03:22,063: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:03:33,171: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:03:33,172: INFO/MainProcess] CloudScraper failed for 3420c869-fd48-4f79-9557-5e185e9e580f/de — trying Selenium.
[2026-03-29 05:04:27,054: WARNING/MainProcess] Selenium: Cloudflare challenge on attempt 1
[2026-03-29 05:04:27,054: INFO/MainProcess] Selenium retry 2 -- waiting 15s -- https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-29 05:05:57,967: WARNING/MainProcess] BUG-DB-002-FIX: No legal section found for url_id=c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=it — inserting empty record (has_legal_content=False)
[2026-03-29 05:05:58,045: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=it: SUCCESS
[2026-03-29 05:06:00,858: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-29 05:06:09,371: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-29 05:06:14,268: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-29 05:06:25,125: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-29 05:06:31,285: WARNING/MainProcess] Short HTML (2024 bytes) for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-29 05:06:45,241: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-29 05:06:45,242: INFO/MainProcess] CloudScraper failed for c53f0d9b-4436-4b67-8a21-7e3484439e5d/fr — trying Selenium.
[2026-03-29 05:07:18,632: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-29 05:07:28,261: INFO/MainProcess] Selenium retry 2 -- waiting 21s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:09:05,874: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-29 05:09:16,417: INFO/MainProcess] Selenium retry 3 -- waiting 18s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:10:50,081: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-29 05:10:50,081: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:10:50,083: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 3420c869-fd48-4f79-9557-5e185e9e580f/de
[2026-03-29 05:10:50,083: INFO/MainProcess] VPN: rotating (current=CA)...
[2026-03-29 05:10:51,028: INFO/MainProcess] VPN disconnected.
[2026-03-29 05:10:56,029: INFO/MainProcess] VPN: connecting to Netherlands (NL)...
[2026-03-29 05:11:15,397: INFO/MainProcess] VPN connected to Netherlands — IP: 193.142.201.16
[2026-03-29 05:11:15,397: INFO/MainProcess] VPN rotation successful → Netherlands
[2026-03-29 05:11:15,399: INFO/MainProcess] VPN rotated — retrying 3420c869-fd48-4f79-9557-5e185e9e580f/de with CloudScraper.
[2026-03-29 05:11:18,105: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:11:31,997: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:11:31,997: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-29 05:12:10,704: WARNING/MainProcess] BUG-DB-002-FIX: No legal section found for url_id=c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=fr — inserting empty record (has_legal_content=False)
[2026-03-29 05:12:10,771: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=fr: SUCCESS
[2026-03-29 05:12:13,450: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-29 05:12:25,999: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-29 05:12:30,660: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-29 05:12:41,427: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-29 05:12:47,597: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-29 05:12:56,293: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-29 05:12:56,294: INFO/MainProcess] CloudScraper failed for c53f0d9b-4436-4b67-8a21-7e3484439e5d/pt — trying Selenium.
[2026-03-29 05:13:30,685: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-29 05:13:40,001: INFO/MainProcess] Selenium retry 2 -- waiting 24s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:15:19,419: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-29 05:15:27,807: INFO/MainProcess] Selenium retry 3 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:16:59,904: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-29 05:16:59,905: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-29 05:16:59,926: WARNING/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f lang=de: FAILED
[2026-03-29 05:17:02,542: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:17:13,844: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:17:18,507: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:17:29,213: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:17:35,391: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:17:43,431: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:17:43,432: INFO/MainProcess] CloudScraper failed for 3420c869-fd48-4f79-9557-5e185e9e580f/it — trying Selenium.
[2026-03-29 05:18:20,126: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d lang=pt: SUCCESS
[2026-03-29 05:18:20,129: INFO/MainProcess] URL c53f0d9b-4436-4b67-8a21-7e3484439e5d: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 05:18:22,796: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-29 05:18:32,759: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-29 05:18:37,411: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-29 05:18:49,939: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-29 05:18:56,113: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-29 05:19:06,958: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-29 05:19:06,959: INFO/MainProcess] CloudScraper failed for 5e1064f4-ed16-4251-8bde-be64c3946f9b/en — trying Selenium.
[2026-03-29 05:19:38,046: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-29 05:19:48,594: INFO/MainProcess] Selenium retry 2 -- waiting 10s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:21:14,813: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-29 05:21:24,357: INFO/MainProcess] Selenium retry 3 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:22:59,775: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-29 05:22:59,775: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:22:59,778: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 3420c869-fd48-4f79-9557-5e185e9e580f/it
[2026-03-29 05:22:59,778: INFO/MainProcess] VPN: rotating (current=NL)...
[2026-03-29 05:23:00,711: INFO/MainProcess] VPN disconnected.
[2026-03-29 05:23:05,712: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-29 05:23:25,146: INFO/MainProcess] VPN connected to Germany — IP: 212.23.215.65
[2026-03-29 05:23:25,146: INFO/MainProcess] VPN rotation successful → Germany
[2026-03-29 05:23:25,148: INFO/MainProcess] VPN rotated — retrying 3420c869-fd48-4f79-9557-5e185e9e580f/it with CloudScraper.
[2026-03-29 05:23:27,823: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:23:42,775: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:23:42,775: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-29 05:25:22,267: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 05:25:24,203: INFO/MainProcess] Gallery: 113 images loaded after scroll
[2026-03-29 05:25:27,682: INFO/MainProcess] Gallery: 120 unique image URLs extracted
[2026-03-29 05:25:27,848: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 05:25:27,849: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 05:25:54,841: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 5e1064f4-ed16-4251-8bde-be64c3946f9b
[2026-03-29 05:26:03,473: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 759e2e11-9069-477c-94c0-02032a68601c
[2026-03-29 05:26:03,473: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 759e2e11-9069-477c-94c0-02032a68601c
[2026-03-29 05:26:03,483: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b lang=en: SUCCESS
[2026-03-29 05:26:06,411: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-29 05:26:17,852: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-29 05:26:22,499: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-29 05:26:31,868: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-29 05:26:38,043: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-29 05:27:14,077: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-29 05:27:16,865: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-29 05:27:16,865: INFO/MainProcess] CloudScraper failed for 5e1064f4-ed16-4251-8bde-be64c3946f9b/es — trying Selenium.
[2026-03-29 05:27:26,172: INFO/MainProcess] Selenium retry 2 -- waiting 15s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:28:56,037: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-29 05:29:09,376: INFO/MainProcess] Selenium retry 3 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:30:40,491: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-29 05:30:40,492: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-29 05:30:40,515: WARNING/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f lang=it: FAILED
[2026-03-29 05:30:43,169: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:30:57,669: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:31:02,409: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:31:16,260: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:31:22,574: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:31:34,220: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:31:34,221: INFO/MainProcess] CloudScraper failed for 3420c869-fd48-4f79-9557-5e185e9e580f/fr — trying Selenium.
[2026-03-29 05:31:58,120: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b lang=es: SUCCESS
[2026-03-29 05:32:00,782: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-29 05:32:13,422: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-29 05:32:18,231: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-29 05:32:27,759: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-29 05:32:33,929: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-29 05:32:47,221: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-29 05:32:47,221: INFO/MainProcess] CloudScraper failed for 5e1064f4-ed16-4251-8bde-be64c3946f9b/de — trying Selenium.
[2026-03-29 05:33:15,848: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-29 05:33:27,276: INFO/MainProcess] Selenium retry 2 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:35:01,732: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-29 05:35:13,075: INFO/MainProcess] Selenium retry 3 -- waiting 27s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:36:55,082: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-29 05:36:55,083: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:36:55,084: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 3420c869-fd48-4f79-9557-5e185e9e580f/fr
[2026-03-29 05:36:55,085: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-29 05:36:56,015: INFO/MainProcess] VPN disconnected.
[2026-03-29 05:37:01,016: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-29 05:37:20,594: INFO/MainProcess] VPN connected to Sweden — IP: 193.46.242.174
[2026-03-29 05:37:20,594: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-29 05:37:20,596: INFO/MainProcess] VPN rotated — retrying 3420c869-fd48-4f79-9557-5e185e9e580f/fr with CloudScraper.
[2026-03-29 05:37:23,519: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:37:33,224: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:37:33,224: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-29 05:38:13,670: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b lang=de: SUCCESS
[2026-03-29 05:38:16,538: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-29 05:38:30,944: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-29 05:38:35,748: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-29 05:38:48,472: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-29 05:38:54,691: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-29 05:39:27,110: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-29 05:39:27,110: INFO/MainProcess] CloudScraper failed for 5e1064f4-ed16-4251-8bde-be64c3946f9b/it — trying Selenium.
[2026-03-29 05:39:31,823: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-29 05:39:39,979: INFO/MainProcess] Selenium retry 2 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:41:10,624: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-29 05:41:24,629: INFO/MainProcess] Selenium retry 3 -- waiting 34s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:43:13,384: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-29 05:43:13,385: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-29 05:43:13,405: WARNING/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f lang=fr: FAILED
[2026-03-29 05:43:16,282: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:43:27,663: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:43:32,470: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:43:46,609: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:43:52,827: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:44:04,911: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:44:04,912: INFO/MainProcess] CloudScraper failed for 3420c869-fd48-4f79-9557-5e185e9e580f/pt — trying Selenium.
[2026-03-29 05:44:31,421: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b lang=it: SUCCESS
[2026-03-29 05:44:34,218: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-29 05:45:02,991: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-29 05:45:07,801: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-29 05:45:17,825: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-29 05:45:24,049: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-29 05:45:36,187: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-29 05:45:36,187: INFO/MainProcess] CloudScraper failed for 5e1064f4-ed16-4251-8bde-be64c3946f9b/fr — trying Selenium.
[2026-03-29 05:45:49,705: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-29 05:46:02,826: INFO/MainProcess] Selenium retry 2 -- waiting 17s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:47:34,736: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-29 05:47:44,651: INFO/MainProcess] Selenium retry 3 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:49:22,751: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-29 05:49:22,751: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:49:22,753: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 3420c869-fd48-4f79-9557-5e185e9e580f/pt
[2026-03-29 05:49:22,754: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-29 05:49:23,652: INFO/MainProcess] VPN disconnected.
[2026-03-29 05:49:28,654: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-29 05:49:48,695: INFO/MainProcess] VPN connected to Sweden — IP: 193.46.242.174
[2026-03-29 05:49:48,695: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-29 05:49:48,696: INFO/MainProcess] VPN rotated — retrying 3420c869-fd48-4f79-9557-5e185e9e580f/pt with CloudScraper.
[2026-03-29 05:49:51,554: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:50:06,228: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:50:06,229: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-29 05:50:41,620: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b lang=fr: SUCCESS
[2026-03-29 05:50:44,392: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-29 05:51:10,102: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-29 05:51:15,161: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-29 05:51:29,496: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-29 05:51:35,715: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-29 05:51:45,698: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-29 05:51:45,698: INFO/MainProcess] CloudScraper failed for 5e1064f4-ed16-4251-8bde-be64c3946f9b/pt — trying Selenium.
[2026-03-29 05:52:00,645: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-29 05:52:12,678: INFO/MainProcess] Selenium retry 2 -- waiting 10s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:53:37,647: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-29 05:53:49,449: INFO/MainProcess] Selenium retry 3 -- waiting 33s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:55:37,391: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-29 05:55:37,392: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-29 05:55:37,495: WARNING/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f lang=pt: FAILED
[2026-03-29 05:55:37,498: WARNING/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f: PARTIAL — Incomplete: 1/6 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr', 'pt']
[2026-03-29 05:55:37,504: INFO/MainProcess] URL 3420c869-fd48-4f79-9557-5e185e9e580f marked incomplete — data PRESERVED. ok=['es'] fail=['en', 'de', 'it', 'fr', 'pt']
[2026-03-29 05:55:40,261: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-29 05:55:48,807: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-29 05:55:53,622: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-29 05:56:02,669: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-29 05:56:08,877: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-29 05:56:19,192: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-29 05:56:19,192: INFO/MainProcess] CloudScraper failed for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841/en — trying Selenium.
[2026-03-29 05:56:57,339: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b lang=pt: SUCCESS
[2026-03-29 05:56:57,342: INFO/MainProcess] URL 5e1064f4-ed16-4251-8bde-be64c3946f9b: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 05:57:00,150: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-29 05:57:11,711: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-29 05:57:16,705: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-29 05:57:31,349: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-29 05:57:37,594: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-29 05:58:08,233: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-29 05:58:08,234: INFO/MainProcess] CloudScraper failed for e68e63b9-b0ec-49d0-bf17-11cf7772000e/en — trying Selenium.
[2026-03-29 05:59:17,799: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 05:59:19,699: INFO/MainProcess] Gallery: 40 images loaded after scroll
[2026-03-29 05:59:22,029: INFO/MainProcess] Gallery: 47 unique image URLs extracted
[2026-03-29 05:59:22,174: INFO/MainProcess] hotelPhotos JS: 40 photos extracted from page source
[2026-03-29 05:59:22,175: INFO/MainProcess] Gallery: 40 photos with full metadata (hotelPhotos JS)
[2026-03-29 05:59:47,937: INFO/MainProcess] Photos: 40 rich photo records (hotelPhotos JS) for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841
[2026-03-29 05:59:56,249: INFO/MainProcess] download_photo_batch: 120/120 photo-files saved for hotel bed202f0-c608-4c5c-9f4c-2d6172664253
[2026-03-29 05:59:56,250: INFO/MainProcess] ImageDownloader (photo_batch): 120/40 photos saved for hotel bed202f0-c608-4c5c-9f4c-2d6172664253
[2026-03-29 05:59:56,257: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841 lang=en: SUCCESS
[2026-03-29 05:59:59,267: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-29 06:00:09,941: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-29 06:00:14,781: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-29 06:00:28,853: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-29 06:00:35,074: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-29 06:00:49,577: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-29 06:00:49,578: INFO/MainProcess] CloudScraper failed for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841/es — trying Selenium.
[2026-03-29 06:02:09,562: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 06:02:11,453: INFO/MainProcess] Gallery: 57 images loaded after scroll
[2026-03-29 06:02:13,247: INFO/MainProcess] Gallery: 64 unique image URLs extracted
[2026-03-29 06:02:13,369: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 06:02:13,369: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 06:02:41,061: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for e68e63b9-b0ec-49d0-bf17-11cf7772000e
[2026-03-29 06:02:50,845: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 001efbba-3b24-4cc4-82e7-5eafbad6dd45
[2026-03-29 06:02:50,846: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 001efbba-3b24-4cc4-82e7-5eafbad6dd45
[2026-03-29 06:02:50,851: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e lang=en: SUCCESS
[2026-03-29 06:02:53,657: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-29 06:03:03,779: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-29 06:03:08,590: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-29 06:03:19,064: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-29 06:03:25,283: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-29 06:03:34,437: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-29 06:03:34,437: INFO/MainProcess] CloudScraper failed for e68e63b9-b0ec-49d0-bf17-11cf7772000e/es — trying Selenium.
[2026-03-29 06:03:58,685: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841 lang=es: SUCCESS
[2026-03-29 06:04:01,420: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-29 06:04:14,530: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-29 06:04:19,357: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-29 06:04:32,750: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-29 06:04:38,976: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-29 06:04:47,848: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-29 06:04:47,848: INFO/MainProcess] CloudScraper failed for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841/de — trying Selenium.
[2026-03-29 06:05:16,333: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e lang=es: SUCCESS
[2026-03-29 06:05:19,149: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-29 06:05:33,057: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-29 06:05:37,872: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-29 06:06:16,135: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-29 06:06:22,341: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-29 06:06:30,712: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-29 06:06:30,712: INFO/MainProcess] CloudScraper failed for e68e63b9-b0ec-49d0-bf17-11cf7772000e/de — trying Selenium.
[2026-03-29 06:06:36,032: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841 lang=de: SUCCESS
[2026-03-29 06:06:38,792: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-29 06:06:51,705: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-29 06:06:56,522: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-29 06:07:09,094: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-29 06:07:15,319: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-29 06:07:51,825: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-29 06:07:51,825: INFO/MainProcess] CloudScraper failed for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841/it — trying Selenium.
[2026-03-29 06:08:08,939: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e lang=de: SUCCESS
[2026-03-29 06:08:11,952: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-29 06:08:26,062: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-29 06:08:30,849: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-29 06:08:43,389: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-29 06:08:49,595: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-29 06:08:58,972: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-29 06:08:58,973: INFO/MainProcess] CloudScraper failed for e68e63b9-b0ec-49d0-bf17-11cf7772000e/it — trying Selenium.
[2026-03-29 06:09:25,847: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841 lang=it: SUCCESS
[2026-03-29 06:09:28,783: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-29 06:09:41,614: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-29 06:09:46,485: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-29 06:10:22,871: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-29 06:10:29,085: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-29 06:10:37,166: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-29 06:10:37,166: INFO/MainProcess] CloudScraper failed for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841/fr — trying Selenium.
[2026-03-29 06:10:42,642: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e lang=it: SUCCESS
[2026-03-29 06:10:45,569: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-29 06:10:56,545: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-29 06:11:01,363: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-29 06:11:11,021: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-29 06:11:17,238: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-29 06:11:30,880: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-29 06:11:30,881: INFO/MainProcess] CloudScraper failed for e68e63b9-b0ec-49d0-bf17-11cf7772000e/fr — trying Selenium.
[2026-03-29 06:11:59,515: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841 lang=fr: SUCCESS
[2026-03-29 06:12:02,346: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-29 06:12:12,130: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-29 06:12:16,985: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-29 06:12:27,436: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-29 06:12:33,630: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-29 06:12:44,630: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-29 06:12:44,631: INFO/MainProcess] CloudScraper failed for 04a78f87-e9b3-4852-b7f3-3cf7d20ab841/pt — trying Selenium.
[2026-03-29 06:13:32,100: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e lang=fr: SUCCESS
[2026-03-29 06:13:34,850: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-29 06:14:12,701: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-29 06:14:17,637: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-29 06:14:29,620: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-29 06:14:35,820: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-29 06:14:49,256: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-29 06:14:49,256: INFO/MainProcess] CloudScraper failed for e68e63b9-b0ec-49d0-bf17-11cf7772000e/pt — trying Selenium.
[2026-03-29 06:14:51,096: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841 lang=pt: SUCCESS
[2026-03-29 06:14:51,099: INFO/MainProcess] URL 04a78f87-e9b3-4852-b7f3-3cf7d20ab841: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 06:14:53,864: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-29 06:15:16,983: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-29 06:15:21,809: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-29 06:15:35,757: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-29 06:15:41,981: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-29 06:15:55,070: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-29 06:15:55,070: INFO/MainProcess] CloudScraper failed for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2/en — trying Selenium.
[2026-03-29 06:16:10,473: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e lang=pt: SUCCESS
[2026-03-29 06:16:10,476: INFO/MainProcess] URL e68e63b9-b0ec-49d0-bf17-11cf7772000e: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 06:16:13,321: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-29 06:16:25,790: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-29 06:16:30,638: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-29 06:16:39,126: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-29 06:16:45,343: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-29 06:16:54,100: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-29 06:16:54,100: INFO/MainProcess] CloudScraper failed for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c/en — trying Selenium.
[2026-03-29 06:18:31,793: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 06:18:33,693: INFO/MainProcess] Gallery: 70 images loaded after scroll
[2026-03-29 06:18:36,744: INFO/MainProcess] Gallery: 77 unique image URLs extracted
[2026-03-29 06:18:36,890: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 06:18:36,891: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 06:19:03,660: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2
[2026-03-29 06:19:15,236: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 21814bbc-9175-476e-917e-54c8780f2c7c
[2026-03-29 06:19:15,236: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 21814bbc-9175-476e-917e-54c8780f2c7c
[2026-03-29 06:19:15,242: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2 lang=en: SUCCESS
[2026-03-29 06:19:18,046: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-29 06:19:31,710: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-29 06:19:37,118: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-29 06:20:04,379: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-29 06:20:10,616: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-29 06:20:21,369: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-29 06:20:21,369: INFO/MainProcess] CloudScraper failed for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2/es — trying Selenium.
[2026-03-29 06:21:24,500: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 06:21:26,396: INFO/MainProcess] Gallery: 34 images loaded after scroll
[2026-03-29 06:21:28,697: INFO/MainProcess] Gallery: 41 unique image URLs extracted
[2026-03-29 06:21:28,834: INFO/MainProcess] hotelPhotos JS: 34 photos extracted from page source
[2026-03-29 06:21:28,835: INFO/MainProcess] Gallery: 34 photos with full metadata (hotelPhotos JS)
[2026-03-29 06:21:55,407: INFO/MainProcess] Photos: 34 rich photo records (hotelPhotos JS) for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c
[2026-03-29 06:22:01,787: INFO/MainProcess] download_photo_batch: 102/102 photo-files saved for hotel 06791b07-7080-4418-b295-f749095ac81a
[2026-03-29 06:22:01,788: INFO/MainProcess] ImageDownloader (photo_batch): 102/34 photos saved for hotel 06791b07-7080-4418-b295-f749095ac81a
[2026-03-29 06:22:01,794: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c lang=en: SUCCESS
[2026-03-29 06:22:04,838: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-29 06:22:17,666: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-29 06:22:22,442: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-29 06:22:34,488: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-29 06:22:40,698: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-29 06:23:05,084: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-29 06:23:05,085: INFO/MainProcess] CloudScraper failed for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c/es — trying Selenium.
[2026-03-29 06:23:14,101: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2 lang=es: SUCCESS
[2026-03-29 06:23:17,039: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-29 06:23:26,564: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-29 06:23:31,332: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-29 06:23:52,195: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-29 06:23:58,404: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-29 06:24:31,832: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c lang=es: SUCCESS
[2026-03-29 06:24:33,511: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-29 06:24:33,511: INFO/MainProcess] CloudScraper failed for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2/de — trying Selenium.
[2026-03-29 06:24:35,155: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-29 06:24:43,665: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-29 06:24:48,403: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-29 06:24:57,641: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-29 06:25:03,849: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-29 06:25:12,628: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-29 06:25:12,629: INFO/MainProcess] CloudScraper failed for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c/de — trying Selenium.
[2026-03-29 06:25:51,689: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2 lang=de: SUCCESS
[2026-03-29 06:25:54,429: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-29 06:26:07,256: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-29 06:26:12,120: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-29 06:26:33,482: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-29 06:26:39,702: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-29 06:26:52,077: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-29 06:26:52,077: INFO/MainProcess] CloudScraper failed for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2/it — trying Selenium.
[2026-03-29 06:27:23,286: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c lang=de: SUCCESS
[2026-03-29 06:27:26,093: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-29 06:27:39,144: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-29 06:27:43,898: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-29 06:27:52,926: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-29 06:27:59,135: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-29 06:28:11,058: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-29 06:28:11,059: INFO/MainProcess] CloudScraper failed for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c/it — trying Selenium.
[2026-03-29 06:28:40,642: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2 lang=it: SUCCESS
[2026-03-29 06:28:43,550: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-29 06:28:52,888: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-29 06:28:57,778: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-29 06:29:12,703: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-29 06:29:18,907: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-29 06:29:31,142: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-29 06:29:31,143: INFO/MainProcess] CloudScraper failed for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2/fr — trying Selenium.
[2026-03-29 06:29:57,467: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c lang=it: SUCCESS
[2026-03-29 06:30:00,251: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-29 06:30:14,888: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-29 06:30:19,715: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-29 06:30:34,054: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-29 06:30:40,281: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-29 06:30:54,795: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-29 06:30:54,796: INFO/MainProcess] CloudScraper failed for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c/fr — trying Selenium.
[2026-03-29 06:31:17,539: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2 lang=fr: SUCCESS
[2026-03-29 06:31:20,272: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-29 06:31:29,077: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-29 06:31:33,823: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-29 06:31:44,760: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-29 06:31:50,966: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-29 06:32:02,756: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-29 06:32:02,756: INFO/MainProcess] CloudScraper failed for 1e9f631d-e30b-47f6-86a7-a8c0d74630a2/pt — trying Selenium.
[2026-03-29 06:32:49,199: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c lang=fr: SUCCESS
[2026-03-29 06:32:51,901: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-29 06:33:03,780: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-29 06:33:08,486: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-29 06:33:23,129: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-29 06:33:29,343: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-29 06:33:39,069: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-29 06:33:39,070: INFO/MainProcess] CloudScraper failed for 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c/pt — trying Selenium.
[2026-03-29 06:34:07,965: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2 lang=pt: SUCCESS
[2026-03-29 06:34:07,967: INFO/MainProcess] URL 1e9f631d-e30b-47f6-86a7-a8c0d74630a2: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 06:35:27,014: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c lang=pt: SUCCESS
[2026-03-29 06:35:27,016: INFO/MainProcess] URL 0c90b5e4-e8a8-4f92-a8b4-b2d9480d145c: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 06:35:29,391: INFO/MainProcess] Selenium browser closed after batch completion.
[2026-03-29 06:35:29,392: INFO/MainProcess] scrape_pending_urls: batch complete — {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-29 06:35:29,394: INFO/MainProcess] Task tasks.scrape_pending_urls[a9226231-8b3a-4b9f-ae64-55a0e0b7e4fc] succeeded in 10202.752588300034s: {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-29 06:35:29,719: INFO/MainProcess] Task tasks.reset_stale_processing_urls[e22af507-b259-42aa-8d33-6378de1be029] received
[2026-03-29 06:35:29,723: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 06:35:29,724: INFO/MainProcess] Task tasks.reset_stale_processing_urls[e22af507-b259-42aa-8d33-6378de1be029] succeeded in 0.0044917999766767025s: {'reset': 0}
[2026-03-29 06:35:29,727: INFO/MainProcess] Task tasks.collect_system_metrics[f496957d-25e3-4626-8ec3-2b5f4922323c] received
[2026-03-29 06:35:30,252: INFO/MainProcess] Task tasks.collect_system_metrics[f496957d-25e3-4626-8ec3-2b5f4922323c] succeeded in 0.5251076000276953s: {'cpu': 19.4, 'memory': 45.2}
[2026-03-29 06:35:30,254: INFO/MainProcess] Task tasks.scrape_pending_urls[b36bf431-1a1c-4782-89ed-42d8bf859b60] received
[2026-03-29 06:35:30,257: INFO/MainProcess] Task tasks.scrape_pending_urls[b36bf431-1a1c-4782-89ed-42d8bf859b60] succeeded in 0.0028704999713227153s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:30,259: INFO/MainProcess] Task tasks.purge_old_debug_html[e061e330-65a8-426f-ac64-60a6c8ce58ee] received
[2026-03-29 06:35:30,260: INFO/MainProcess] Task tasks.purge_old_debug_html[e061e330-65a8-426f-ac64-60a6c8ce58ee] succeeded in 0.0009678000351414084s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 06:35:30,261: INFO/MainProcess] Task tasks.collect_system_metrics[45c3c385-b9ef-4e46-985f-3dcfe946413c] received
[2026-03-29 06:35:30,779: INFO/MainProcess] Task tasks.collect_system_metrics[45c3c385-b9ef-4e46-985f-3dcfe946413c] succeeded in 0.5178170000435784s: {'cpu': 12.8, 'memory': 45.2}
[2026-03-29 06:35:30,782: INFO/MainProcess] Task tasks.scrape_pending_urls[492b7716-b0f5-45fa-9f88-2f8e2aed3040] received
[2026-03-29 06:35:30,785: INFO/MainProcess] Task tasks.scrape_pending_urls[492b7716-b0f5-45fa-9f88-2f8e2aed3040] succeeded in 0.002789899939671159s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:30,786: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d49f3f4f-911b-4df7-aca9-ff6e1de294c8] received
[2026-03-29 06:35:30,788: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 06:35:30,789: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d49f3f4f-911b-4df7-aca9-ff6e1de294c8] succeeded in 0.002747700084000826s: {'reset': 0}
[2026-03-29 06:35:30,790: INFO/MainProcess] Task tasks.collect_system_metrics[213da3b3-50ce-46dd-ad4e-34ffb174d51c] received
[2026-03-29 06:35:31,296: INFO/MainProcess] Task tasks.collect_system_metrics[213da3b3-50ce-46dd-ad4e-34ffb174d51c] succeeded in 0.5058205999666825s: {'cpu': 6.5, 'memory': 45.2}
[2026-03-29 06:35:31,298: INFO/MainProcess] Task tasks.scrape_pending_urls[8823a686-d6f7-4abb-b6c0-d73e571493ca] received
[2026-03-29 06:35:31,301: INFO/MainProcess] Task tasks.scrape_pending_urls[8823a686-d6f7-4abb-b6c0-d73e571493ca] succeeded in 0.002345499931834638s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:31,302: INFO/MainProcess] Task tasks.reset_stale_processing_urls[a1e1b364-1c23-4a49-89f1-58e06e258bce] received
[2026-03-29 06:35:31,304: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 06:35:31,305: INFO/MainProcess] Task tasks.reset_stale_processing_urls[a1e1b364-1c23-4a49-89f1-58e06e258bce] succeeded in 0.002775800065137446s: {'reset': 0}
[2026-03-29 06:35:31,307: INFO/MainProcess] Task tasks.collect_system_metrics[671c67bb-31c7-40ea-842f-afa348311684] received
[2026-03-29 06:35:31,824: INFO/MainProcess] Task tasks.collect_system_metrics[671c67bb-31c7-40ea-842f-afa348311684] succeeded in 0.516773600014858s: {'cpu': 4.7, 'memory': 45.2}
[2026-03-29 06:35:31,826: INFO/MainProcess] Task tasks.scrape_pending_urls[5ebd4f12-3c5e-4b6c-86a0-be22bf0fb5cc] received
[2026-03-29 06:35:31,829: INFO/MainProcess] Task tasks.scrape_pending_urls[5ebd4f12-3c5e-4b6c-86a0-be22bf0fb5cc] succeeded in 0.00279450009111315s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:31,830: INFO/MainProcess] Task tasks.purge_old_debug_html[90985dbe-c76b-4468-918b-330023246e79] received
[2026-03-29 06:35:31,832: INFO/MainProcess] Task tasks.purge_old_debug_html[90985dbe-c76b-4468-918b-330023246e79] succeeded in 0.0009270000737160444s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 06:35:31,833: INFO/MainProcess] Task tasks.collect_system_metrics[1fea2074-3903-4630-a791-a9ddbf7cb1b1] received
[2026-03-29 06:35:32,352: INFO/MainProcess] Task tasks.collect_system_metrics[1fea2074-3903-4630-a791-a9ddbf7cb1b1] succeeded in 0.518731200019829s: {'cpu': 4.7, 'memory': 45.2}
[2026-03-29 06:35:32,354: INFO/MainProcess] Task tasks.scrape_pending_urls[21df646f-61c8-48ea-bf4f-e093cb86e3f8] received
[2026-03-29 06:35:32,357: INFO/MainProcess] Task tasks.scrape_pending_urls[21df646f-61c8-48ea-bf4f-e093cb86e3f8] succeeded in 0.002289400086738169s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:32,358: INFO/MainProcess] Task tasks.reset_stale_processing_urls[b981c752-4fd8-405a-857a-833ac590302a] received
[2026-03-29 06:35:32,360: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 06:35:32,361: INFO/MainProcess] Task tasks.reset_stale_processing_urls[b981c752-4fd8-405a-857a-833ac590302a] succeeded in 0.00278700003400445s: {'reset': 0}
[2026-03-29 06:35:32,362: INFO/MainProcess] Task tasks.collect_system_metrics[ddfd8d31-8aff-4d22-9993-4fee3e40f3b0] received
[2026-03-29 06:35:32,880: INFO/MainProcess] Task tasks.collect_system_metrics[ddfd8d31-8aff-4d22-9993-4fee3e40f3b0] succeeded in 0.5171182999620214s: {'cpu': 6.5, 'memory': 45.2}
[2026-03-29 06:35:32,882: INFO/MainProcess] Task tasks.scrape_pending_urls[15d327e0-faf3-4ed9-b114-0f414c780539] received
[2026-03-29 06:35:32,885: INFO/MainProcess] Task tasks.scrape_pending_urls[15d327e0-faf3-4ed9-b114-0f414c780539] succeeded in 0.002685599960386753s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:32,886: INFO/MainProcess] Task tasks.reset_stale_processing_urls[1988a6ba-a1d9-43a0-8e02-129ebde70e1e] received
[2026-03-29 06:35:32,888: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 06:35:32,889: INFO/MainProcess] Task tasks.reset_stale_processing_urls[1988a6ba-a1d9-43a0-8e02-129ebde70e1e] succeeded in 0.0027055999962612987s: {'reset': 0}
[2026-03-29 06:35:32,890: INFO/MainProcess] Task tasks.collect_system_metrics[084c014a-8590-41b7-a8b0-2e17cfdb3d91] received
[2026-03-29 06:35:33,409: INFO/MainProcess] Task tasks.collect_system_metrics[084c014a-8590-41b7-a8b0-2e17cfdb3d91] succeeded in 0.5180796999484301s: {'cpu': 0.8, 'memory': 45.2}
[2026-03-29 06:35:33,411: INFO/MainProcess] Task tasks.scrape_pending_urls[0bd0dfa7-3cae-422c-a1f7-49b6b8f1dcbe] received
[2026-03-29 06:35:33,413: INFO/MainProcess] Task tasks.scrape_pending_urls[0bd0dfa7-3cae-422c-a1f7-49b6b8f1dcbe] succeeded in 0.0023233999963849783s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:33,415: INFO/MainProcess] Task tasks.purge_old_debug_html[aaedc199-9b17-4b17-9049-6e5171ff07fb] received
[2026-03-29 06:35:33,416: INFO/MainProcess] Task tasks.purge_old_debug_html[aaedc199-9b17-4b17-9049-6e5171ff07fb] succeeded in 0.0009256999474018812s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 06:35:33,417: INFO/MainProcess] Task tasks.collect_system_metrics[f487eee8-6162-4700-a08b-faa713813d0a] received
[2026-03-29 06:35:33,935: INFO/MainProcess] Task tasks.collect_system_metrics[f487eee8-6162-4700-a08b-faa713813d0a] succeeded in 0.5174260000931099s: {'cpu': 1.6, 'memory': 45.2}
[2026-03-29 06:35:33,937: INFO/MainProcess] Task tasks.scrape_pending_urls[afeb7695-5533-4933-9351-d6352fce74ab] received
[2026-03-29 06:35:33,940: INFO/MainProcess] Task tasks.scrape_pending_urls[afeb7695-5533-4933-9351-d6352fce74ab] succeeded in 0.0026405000826343894s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:33,941: INFO/MainProcess] Task tasks.collect_system_metrics[57415682-c7f5-454d-a8e3-3fe04cd53652] received
[2026-03-29 06:35:34,458: INFO/MainProcess] Task tasks.collect_system_metrics[57415682-c7f5-454d-a8e3-3fe04cd53652] succeeded in 0.5166913000866771s: {'cpu': 7.1, 'memory': 45.3}
[2026-03-29 06:35:34,461: INFO/MainProcess] Task tasks.scrape_pending_urls[c436cb6b-d954-4e30-8567-653a728897b4] received
[2026-03-29 06:35:34,465: INFO/MainProcess] Task tasks.scrape_pending_urls[c436cb6b-d954-4e30-8567-653a728897b4] succeeded in 0.003832999966107309s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:34,467: INFO/MainProcess] Task tasks.collect_system_metrics[d2728bf2-47f7-4259-bae0-dd021f650cce] received
[2026-03-29 06:35:34,983: INFO/MainProcess] Task tasks.collect_system_metrics[d2728bf2-47f7-4259-bae0-dd021f650cce] succeeded in 0.5165233000880107s: {'cpu': 9.8, 'memory': 45.3}
[2026-03-29 06:35:34,985: INFO/MainProcess] Task tasks.scrape_pending_urls[bfe848ea-036b-4d30-8121-900cd7127a9d] received
[2026-03-29 06:35:34,988: INFO/MainProcess] Task tasks.scrape_pending_urls[bfe848ea-036b-4d30-8121-900cd7127a9d] succeeded in 0.002889100112952292s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:34,990: INFO/MainProcess] Task tasks.collect_system_metrics[16c650a1-3142-4cca-8a48-fb6aba2b1834] received
[2026-03-29 06:35:35,508: INFO/MainProcess] Task tasks.collect_system_metrics[16c650a1-3142-4cca-8a48-fb6aba2b1834] succeeded in 0.5167832000879571s: {'cpu': 3.1, 'memory': 45.3}
[2026-03-29 06:35:35,509: INFO/MainProcess] Task tasks.scrape_pending_urls[52020f54-eb77-4b5d-98bd-2a8c0ccf40b0] received
[2026-03-29 06:35:35,512: INFO/MainProcess] Task tasks.scrape_pending_urls[52020f54-eb77-4b5d-98bd-2a8c0ccf40b0] succeeded in 0.002328700036741793s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:35,513: INFO/MainProcess] Task tasks.collect_system_metrics[ed069a5f-fe82-45df-a37a-a416aff62d8b] received
[2026-03-29 06:35:36,031: INFO/MainProcess] Task tasks.collect_system_metrics[ed069a5f-fe82-45df-a37a-a416aff62d8b] succeeded in 0.5168339000083506s: {'cpu': 4.7, 'memory': 45.3}
[2026-03-29 06:35:36,032: INFO/MainProcess] Task tasks.scrape_pending_urls[aa9126af-54b1-463d-a47e-24c7d4f2a29d] received
[2026-03-29 06:35:36,036: INFO/MainProcess] Task tasks.scrape_pending_urls[aa9126af-54b1-463d-a47e-24c7d4f2a29d] succeeded in 0.0031667000148445368s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:36,037: INFO/MainProcess] Task tasks.collect_system_metrics[b59c262a-e455-4d0d-b94d-b9fa4128d03b] received
[2026-03-29 06:35:36,554: INFO/MainProcess] Task tasks.collect_system_metrics[b59c262a-e455-4d0d-b94d-b9fa4128d03b] succeeded in 0.5163205999415368s: {'cpu': 1.2, 'memory': 45.3}
[2026-03-29 06:35:36,556: INFO/MainProcess] Task tasks.scrape_pending_urls[adab02dc-27b9-44bb-a279-957efb0703a5] received
[2026-03-29 06:35:36,558: INFO/MainProcess] Task tasks.scrape_pending_urls[adab02dc-27b9-44bb-a279-957efb0703a5] succeeded in 0.002181099960580468s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:36,559: INFO/MainProcess] Task tasks.collect_system_metrics[8458a440-de9a-49c8-b0c8-67b00041ee4e] received
[2026-03-29 06:35:37,076: INFO/MainProcess] Task tasks.collect_system_metrics[8458a440-de9a-49c8-b0c8-67b00041ee4e] succeeded in 0.516572599997744s: {'cpu': 3.5, 'memory': 45.3}
[2026-03-29 06:35:37,078: INFO/MainProcess] Task tasks.scrape_pending_urls[43156bd9-6ff7-435c-90c1-4ca1cc5e082c] received
[2026-03-29 06:35:37,081: INFO/MainProcess] Task tasks.scrape_pending_urls[43156bd9-6ff7-435c-90c1-4ca1cc5e082c] succeeded in 0.0029293999541550875s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:37,083: INFO/MainProcess] Task tasks.collect_system_metrics[48ed28ad-46e6-4f37-a92b-fbb97a7e5602] received
[2026-03-29 06:35:37,600: INFO/MainProcess] Task tasks.collect_system_metrics[48ed28ad-46e6-4f37-a92b-fbb97a7e5602] succeeded in 0.5166012999834493s: {'cpu': 4.8, 'memory': 45.3}
[2026-03-29 06:35:37,601: INFO/MainProcess] Task tasks.scrape_pending_urls[daabb49e-5535-4fff-b157-6758ba9631e5] received
[2026-03-29 06:35:37,604: INFO/MainProcess] Task tasks.scrape_pending_urls[daabb49e-5535-4fff-b157-6758ba9631e5] succeeded in 0.0022216999204829335s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:37,605: INFO/MainProcess] Task tasks.collect_system_metrics[a388b15d-e55c-4994-bf1a-cac6a02f5ada] received
[2026-03-29 06:35:38,112: INFO/MainProcess] Task tasks.collect_system_metrics[a388b15d-e55c-4994-bf1a-cac6a02f5ada] succeeded in 0.5061261000810191s: {'cpu': 9.8, 'memory': 45.3}
[2026-03-29 06:35:38,114: INFO/MainProcess] Task tasks.scrape_pending_urls[c87f82e6-4b08-4177-8d56-3d8ac1b99a96] received
[2026-03-29 06:35:38,119: INFO/MainProcess] Task tasks.scrape_pending_urls[c87f82e6-4b08-4177-8d56-3d8ac1b99a96] succeeded in 0.004764600074850023s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:38,121: INFO/MainProcess] Task tasks.collect_system_metrics[a478cf5a-a820-41c6-a234-3cc416774d92] received
[2026-03-29 06:35:38,639: INFO/MainProcess] Task tasks.collect_system_metrics[a478cf5a-a820-41c6-a234-3cc416774d92] succeeded in 0.5170016998890787s: {'cpu': 11.2, 'memory': 45.4}
[2026-03-29 06:35:38,641: INFO/MainProcess] Task tasks.scrape_pending_urls[0d38e72e-d617-4455-86a7-615cb273c9f8] received
[2026-03-29 06:35:38,643: INFO/MainProcess] Task tasks.scrape_pending_urls[0d38e72e-d617-4455-86a7-615cb273c9f8] succeeded in 0.0022109000710770488s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:38,645: INFO/MainProcess] Task tasks.collect_system_metrics[d6e0c7cc-556d-4092-9fa9-670fb34f5430] received
[2026-03-29 06:35:39,161: INFO/MainProcess] Task tasks.collect_system_metrics[d6e0c7cc-556d-4092-9fa9-670fb34f5430] succeeded in 0.5161060000536963s: {'cpu': 2.0, 'memory': 45.4}
[2026-03-29 06:35:39,163: INFO/MainProcess] Task tasks.scrape_pending_urls[aa828c8b-2940-406f-89d2-58c261529bdf] received
[2026-03-29 06:35:39,166: INFO/MainProcess] Task tasks.scrape_pending_urls[aa828c8b-2940-406f-89d2-58c261529bdf] succeeded in 0.002799800015054643s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:39,167: INFO/MainProcess] Task tasks.collect_system_metrics[af04315e-3092-4233-84d5-5c4c72f7793d] received
[2026-03-29 06:35:39,683: INFO/MainProcess] Task tasks.collect_system_metrics[af04315e-3092-4233-84d5-5c4c72f7793d] succeeded in 0.5153692999156192s: {'cpu': 14.3, 'memory': 45.5}
[2026-03-29 06:35:39,685: INFO/MainProcess] Task tasks.scrape_pending_urls[215f7a93-439b-4465-9a92-6c1a32b75651] received
[2026-03-29 06:35:39,687: INFO/MainProcess] Task tasks.scrape_pending_urls[215f7a93-439b-4465-9a92-6c1a32b75651] succeeded in 0.0021790999453514814s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:39,689: INFO/MainProcess] Task tasks.collect_system_metrics[546eff22-3ea5-4b29-b6db-ef8cc1ad6f82] received
[2026-03-29 06:35:40,205: INFO/MainProcess] Task tasks.collect_system_metrics[546eff22-3ea5-4b29-b6db-ef8cc1ad6f82] succeeded in 0.5162496999837458s: {'cpu': 7.4, 'memory': 45.5}
[2026-03-29 06:35:40,207: INFO/MainProcess] Task tasks.scrape_pending_urls[6a282a7f-aaee-45c7-a892-11f085e57361] received
[2026-03-29 06:35:40,210: INFO/MainProcess] Task tasks.scrape_pending_urls[6a282a7f-aaee-45c7-a892-11f085e57361] succeeded in 0.0029241000302135944s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:40,212: INFO/MainProcess] Task tasks.collect_system_metrics[3c1e430f-707d-4fcb-a80a-d4bc37ed6107] received
[2026-03-29 06:35:40,728: INFO/MainProcess] Task tasks.collect_system_metrics[3c1e430f-707d-4fcb-a80a-d4bc37ed6107] succeeded in 0.5164222000166774s: {'cpu': 5.9, 'memory': 45.5}
[2026-03-29 06:35:40,730: INFO/MainProcess] Task tasks.scrape_pending_urls[20312170-1230-447b-9c1f-8d48e0b81a9d] received
[2026-03-29 06:35:40,733: INFO/MainProcess] Task tasks.scrape_pending_urls[20312170-1230-447b-9c1f-8d48e0b81a9d] succeeded in 0.0022191000171005726s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:40,734: INFO/MainProcess] Task tasks.collect_system_metrics[0e073e0f-0d72-4166-9dbf-a93e330f5f5c] received
[2026-03-29 06:35:41,251: INFO/MainProcess] Task tasks.collect_system_metrics[0e073e0f-0d72-4166-9dbf-a93e330f5f5c] succeeded in 0.5164435000624508s: {'cpu': 7.7, 'memory': 45.5}
[2026-03-29 06:35:41,252: INFO/MainProcess] Task tasks.scrape_pending_urls[bb099346-e6f7-4860-8e30-a772ccab0253] received
[2026-03-29 06:35:41,256: INFO/MainProcess] Task tasks.scrape_pending_urls[bb099346-e6f7-4860-8e30-a772ccab0253] succeeded in 0.003042199998162687s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:41,257: INFO/MainProcess] Task tasks.collect_system_metrics[3d3d85f1-8257-44c6-9a40-cfc31a4e0fc5] received
[2026-03-29 06:35:41,774: INFO/MainProcess] Task tasks.collect_system_metrics[3d3d85f1-8257-44c6-9a40-cfc31a4e0fc5] succeeded in 0.5163395999697968s: {'cpu': 0.8, 'memory': 45.5}
[2026-03-29 06:35:41,775: INFO/MainProcess] Task tasks.scrape_pending_urls[89a6426f-8a1e-4ff6-9c44-c4eddf898378] received
[2026-03-29 06:35:41,778: INFO/MainProcess] Task tasks.scrape_pending_urls[89a6426f-8a1e-4ff6-9c44-c4eddf898378] succeeded in 0.0022029998945072293s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:41,779: INFO/MainProcess] Task tasks.collect_system_metrics[66c7a583-ded9-4c65-bde0-94743a970dea] received
[2026-03-29 06:35:42,296: INFO/MainProcess] Task tasks.collect_system_metrics[66c7a583-ded9-4c65-bde0-94743a970dea] succeeded in 0.5166207000147551s: {'cpu': 4.7, 'memory': 45.5}
[2026-03-29 06:35:42,298: INFO/MainProcess] Task tasks.scrape_pending_urls[a01eaaab-56d6-4a26-8691-2d4482289881] received
[2026-03-29 06:35:42,301: INFO/MainProcess] Task tasks.scrape_pending_urls[a01eaaab-56d6-4a26-8691-2d4482289881] succeeded in 0.0027794999768957496s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:42,303: INFO/MainProcess] Task tasks.collect_system_metrics[d674f267-c03a-480f-959b-d82ea8c3ae73] received
[2026-03-29 06:35:42,819: INFO/MainProcess] Task tasks.collect_system_metrics[d674f267-c03a-480f-959b-d82ea8c3ae73] succeeded in 0.5162219000048935s: {'cpu': 7.6, 'memory': 45.5}
[2026-03-29 06:35:42,821: INFO/MainProcess] Task tasks.scrape_pending_urls[8840b00e-bcdc-48ab-a683-be80266f389c] received
[2026-03-29 06:35:42,824: INFO/MainProcess] Task tasks.scrape_pending_urls[8840b00e-bcdc-48ab-a683-be80266f389c] succeeded in 0.0022113999584689736s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:42,825: INFO/MainProcess] Task tasks.collect_system_metrics[fca65fb3-8afb-4f16-a40f-17491bae7fb3] received
[2026-03-29 06:35:43,341: INFO/MainProcess] Task tasks.collect_system_metrics[fca65fb3-8afb-4f16-a40f-17491bae7fb3] succeeded in 0.5159342000260949s: {'cpu': 7.5, 'memory': 45.5}
[2026-03-29 06:35:43,343: INFO/MainProcess] Task tasks.scrape_pending_urls[a8648924-e935-4548-b87d-cc5089ac1d2d] received
[2026-03-29 06:35:43,346: INFO/MainProcess] Task tasks.scrape_pending_urls[a8648924-e935-4548-b87d-cc5089ac1d2d] succeeded in 0.003033099928870797s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:43,348: INFO/MainProcess] Task tasks.collect_system_metrics[389a8dbe-60dc-4505-bf97-67bcc91dbcab] received
[2026-03-29 06:35:43,866: INFO/MainProcess] Task tasks.collect_system_metrics[389a8dbe-60dc-4505-bf97-67bcc91dbcab] succeeded in 0.5180365999694914s: {'cpu': 10.0, 'memory': 45.5}
[2026-03-29 06:35:43,868: INFO/MainProcess] Task tasks.scrape_pending_urls[4c883df6-dd78-4d0e-9726-9a6775e7fb64] received
[2026-03-29 06:35:43,871: INFO/MainProcess] Task tasks.scrape_pending_urls[4c883df6-dd78-4d0e-9726-9a6775e7fb64] succeeded in 0.0022535999305546284s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:43,872: INFO/MainProcess] Task tasks.collect_system_metrics[0b34b12e-08c9-4c52-8af7-c078f4455590] received
[2026-03-29 06:35:44,389: INFO/MainProcess] Task tasks.collect_system_metrics[0b34b12e-08c9-4c52-8af7-c078f4455590] succeeded in 0.5160083000082523s: {'cpu': 9.3, 'memory': 45.4}
[2026-03-29 06:35:44,391: INFO/MainProcess] Task tasks.scrape_pending_urls[9233a50d-b52e-4e80-86ea-539fb0fd3f96] received
[2026-03-29 06:35:44,395: INFO/MainProcess] Task tasks.scrape_pending_urls[9233a50d-b52e-4e80-86ea-539fb0fd3f96] succeeded in 0.0035552000626921654s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:44,396: INFO/MainProcess] Task tasks.collect_system_metrics[1fa06ffa-c357-4641-93b3-ed88abcfa2f8] received
[2026-03-29 06:35:44,913: INFO/MainProcess] Task tasks.collect_system_metrics[1fa06ffa-c357-4641-93b3-ed88abcfa2f8] succeeded in 0.5165389000903815s: {'cpu': 6.4, 'memory': 45.4}
[2026-03-29 06:35:44,915: INFO/MainProcess] Task tasks.scrape_pending_urls[c1d055eb-5891-43af-b50f-1c4400ca0ed9] received
[2026-03-29 06:35:44,918: INFO/MainProcess] Task tasks.scrape_pending_urls[c1d055eb-5891-43af-b50f-1c4400ca0ed9] succeeded in 0.0022140999790281057s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:44,919: INFO/MainProcess] Task tasks.collect_system_metrics[d9be5763-5a32-4d87-b23a-442909052710] received
[2026-03-29 06:35:45,437: INFO/MainProcess] Task tasks.collect_system_metrics[d9be5763-5a32-4d87-b23a-442909052710] succeeded in 0.5170182000147179s: {'cpu': 4.3, 'memory': 45.4}
[2026-03-29 06:35:45,439: INFO/MainProcess] Task tasks.scrape_pending_urls[20640219-81f7-4544-8870-c3b2388d35d1] received
[2026-03-29 06:35:45,442: INFO/MainProcess] Task tasks.scrape_pending_urls[20640219-81f7-4544-8870-c3b2388d35d1] succeeded in 0.0028608000138774514s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:45,443: INFO/MainProcess] Task tasks.collect_system_metrics[487aaa15-8c53-4d89-8e4a-751664dc21ed] received
[2026-03-29 06:35:45,960: INFO/MainProcess] Task tasks.collect_system_metrics[487aaa15-8c53-4d89-8e4a-751664dc21ed] succeeded in 0.5169812000822276s: {'cpu': 5.6, 'memory': 45.4}
[2026-03-29 06:35:45,962: INFO/MainProcess] Task tasks.scrape_pending_urls[dc8d9d51-e0f9-4d4d-988a-c38adfe97fce] received
[2026-03-29 06:35:45,965: INFO/MainProcess] Task tasks.scrape_pending_urls[dc8d9d51-e0f9-4d4d-988a-c38adfe97fce] succeeded in 0.0030996999703347683s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:45,967: INFO/MainProcess] Task tasks.collect_system_metrics[063b8e0d-9c74-4d1d-8aa6-1926f0e2b86a] received
[2026-03-29 06:35:46,484: INFO/MainProcess] Task tasks.collect_system_metrics[063b8e0d-9c74-4d1d-8aa6-1926f0e2b86a] succeeded in 0.5162698000203818s: {'cpu': 5.1, 'memory': 45.4}
[2026-03-29 06:35:46,485: INFO/MainProcess] Task tasks.scrape_pending_urls[f89766df-6585-42fb-890a-70f783e72dfc] received
[2026-03-29 06:35:46,488: INFO/MainProcess] Task tasks.scrape_pending_urls[f89766df-6585-42fb-890a-70f783e72dfc] succeeded in 0.0028334000380709767s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:46,490: INFO/MainProcess] Task tasks.collect_system_metrics[83fb6924-2fee-4e8c-954d-6561dbf45cc4] received
[2026-03-29 06:35:47,007: INFO/MainProcess] Task tasks.collect_system_metrics[83fb6924-2fee-4e8c-954d-6561dbf45cc4] succeeded in 0.5171377999940887s: {'cpu': 5.4, 'memory': 45.4}
[2026-03-29 06:35:47,009: INFO/MainProcess] Task tasks.scrape_pending_urls[9ec4adce-c7e2-44e0-a3d7-17b373482d6a] received
[2026-03-29 06:35:47,012: INFO/MainProcess] Task tasks.scrape_pending_urls[9ec4adce-c7e2-44e0-a3d7-17b373482d6a] succeeded in 0.0021978000877425075s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,013: INFO/MainProcess] Task tasks.collect_system_metrics[80b916cd-9ef7-4f40-a329-d150a388109f] received
[2026-03-29 06:35:47,530: INFO/MainProcess] Task tasks.collect_system_metrics[80b916cd-9ef7-4f40-a329-d150a388109f] succeeded in 0.5159176000161096s: {'cpu': 3.9, 'memory': 45.4}
[2026-03-29 06:35:47,531: INFO/MainProcess] Task tasks.scrape_pending_urls[2c41d5b2-8c55-41cb-9629-c3c40fa34217] received
[2026-03-29 06:35:47,534: INFO/MainProcess] Task tasks.scrape_pending_urls[2c41d5b2-8c55-41cb-9629-c3c40fa34217] succeeded in 0.0028250999748706818s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,536: INFO/MainProcess] Task tasks.scrape_pending_urls[a3104035-89c7-4801-807f-55f3ad4ad49f] received
[2026-03-29 06:35:47,538: INFO/MainProcess] Task tasks.scrape_pending_urls[a3104035-89c7-4801-807f-55f3ad4ad49f] succeeded in 0.00223580002784729s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,540: INFO/MainProcess] Task tasks.scrape_pending_urls[ac825733-69d0-4294-8f5c-f296bb275ec0] received
[2026-03-29 06:35:47,542: INFO/MainProcess] Task tasks.scrape_pending_urls[ac825733-69d0-4294-8f5c-f296bb275ec0] succeeded in 0.0020404000533744693s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,543: INFO/MainProcess] Task tasks.scrape_pending_urls[b0aa15ad-531e-4b51-9a74-5388f3e358b6] received
[2026-03-29 06:35:47,545: INFO/MainProcess] Task tasks.scrape_pending_urls[b0aa15ad-531e-4b51-9a74-5388f3e358b6] succeeded in 0.0020186000037938356s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,547: INFO/MainProcess] Task tasks.scrape_pending_urls[d2c87e44-20ab-4bcd-a9e2-680aaad1a989] received
[2026-03-29 06:35:47,549: INFO/MainProcess] Task tasks.scrape_pending_urls[d2c87e44-20ab-4bcd-a9e2-680aaad1a989] succeeded in 0.002005299902521074s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,550: INFO/MainProcess] Task tasks.scrape_pending_urls[715495b8-e387-42a4-9680-de427022036a] received
[2026-03-29 06:35:47,554: INFO/MainProcess] Task tasks.scrape_pending_urls[715495b8-e387-42a4-9680-de427022036a] succeeded in 0.0022956999018788338s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,555: INFO/MainProcess] Task tasks.scrape_pending_urls[d0646a41-8fa5-4265-a2be-f11714bc92f0] received
[2026-03-29 06:35:47,557: INFO/MainProcess] Task tasks.scrape_pending_urls[d0646a41-8fa5-4265-a2be-f11714bc92f0] succeeded in 0.002038300037384033s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,559: INFO/MainProcess] Task tasks.scrape_pending_urls[ec3134ef-b3ab-4120-add9-467950aacd75] received
[2026-03-29 06:35:47,561: INFO/MainProcess] Task tasks.scrape_pending_urls[ec3134ef-b3ab-4120-add9-467950aacd75] succeeded in 0.0020074000349268317s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,562: INFO/MainProcess] Task tasks.scrape_pending_urls[4eb00280-0f91-4d81-b672-323843573082] received
[2026-03-29 06:35:47,565: INFO/MainProcess] Task tasks.scrape_pending_urls[4eb00280-0f91-4d81-b672-323843573082] succeeded in 0.0019987999694421887s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:47,566: INFO/MainProcess] Task tasks.scrape_pending_urls[e53cf956-5d46-49a4-84a3-35a507c589fe] received
[2026-03-29 06:35:47,569: INFO/MainProcess] Task tasks.scrape_pending_urls[e53cf956-5d46-49a4-84a3-35a507c589fe] succeeded in 0.00264770002104342s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,005: INFO/MainProcess] Task tasks.scrape_pending_urls[d6121307-864e-40a4-a53b-82d539fde58f] received
[2026-03-29 06:35:48,007: INFO/MainProcess] Task tasks.scrape_pending_urls[d6121307-864e-40a4-a53b-82d539fde58f] succeeded in 0.0021855999948456883s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,008: INFO/MainProcess] Task tasks.scrape_pending_urls[59d261fd-de9d-4591-8595-e54cc61ac5dc] received
[2026-03-29 06:35:48,011: INFO/MainProcess] Task tasks.scrape_pending_urls[59d261fd-de9d-4591-8595-e54cc61ac5dc] succeeded in 0.0020313001004979014s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,012: INFO/MainProcess] Task tasks.scrape_pending_urls[9ae9a85c-d470-4254-ad64-bea7fff33e57] received
[2026-03-29 06:35:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[9ae9a85c-d470-4254-ad64-bea7fff33e57] succeeded in 0.002145000034943223s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[d71f2dee-cab2-4885-ac2a-a1f2873632cb] received
[2026-03-29 06:35:48,020: INFO/MainProcess] Task tasks.scrape_pending_urls[d71f2dee-cab2-4885-ac2a-a1f2873632cb] succeeded in 0.002214199979789555s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,021: INFO/MainProcess] Task tasks.scrape_pending_urls[6e44a419-2a76-447d-a05f-01dd60403762] received
[2026-03-29 06:35:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[6e44a419-2a76-447d-a05f-01dd60403762] succeeded in 0.0020430999575182796s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,025: INFO/MainProcess] Task tasks.scrape_pending_urls[e883c41b-5b4a-45ef-a66d-7b79dd89faf4] received
[2026-03-29 06:35:48,027: INFO/MainProcess] Task tasks.scrape_pending_urls[e883c41b-5b4a-45ef-a66d-7b79dd89faf4] succeeded in 0.0020129000768065453s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,028: INFO/MainProcess] Task tasks.scrape_pending_urls[21e5395a-803d-4ba1-83cd-581078789002] received
[2026-03-29 06:35:48,031: INFO/MainProcess] Task tasks.scrape_pending_urls[21e5395a-803d-4ba1-83cd-581078789002] succeeded in 0.0025344000896438956s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,033: INFO/MainProcess] Task tasks.scrape_pending_urls[3428a554-c7bc-4164-abdd-9fe512b1b545] received
[2026-03-29 06:35:48,036: INFO/MainProcess] Task tasks.scrape_pending_urls[3428a554-c7bc-4164-abdd-9fe512b1b545] succeeded in 0.0025368999922648072s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,037: INFO/MainProcess] Task tasks.scrape_pending_urls[79201e18-27c9-41eb-b302-6aaaea3ccdec] received
[2026-03-29 06:35:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[79201e18-27c9-41eb-b302-6aaaea3ccdec] succeeded in 0.0020803000079467893s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,041: INFO/MainProcess] Task tasks.scrape_pending_urls[719d2dd0-6df6-4141-a3db-d175766dbe95] received
[2026-03-29 06:35:48,044: INFO/MainProcess] Task tasks.scrape_pending_urls[719d2dd0-6df6-4141-a3db-d175766dbe95] succeeded in 0.0022402999456971884s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,045: INFO/MainProcess] Task tasks.scrape_pending_urls[9bf20f97-4845-4d92-b115-93488aa785c6] received
[2026-03-29 06:35:48,049: INFO/MainProcess] Task tasks.scrape_pending_urls[9bf20f97-4845-4d92-b115-93488aa785c6] succeeded in 0.0032445999095216393s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,050: INFO/MainProcess] Task tasks.scrape_pending_urls[73e8508e-35fc-4a45-8a51-3f0981c1d973] received
[2026-03-29 06:35:48,053: INFO/MainProcess] Task tasks.scrape_pending_urls[73e8508e-35fc-4a45-8a51-3f0981c1d973] succeeded in 0.002107099979184568s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,054: INFO/MainProcess] Task tasks.scrape_pending_urls[cf51485a-4d16-42b5-a0fa-d8cfe47b221d] received
[2026-03-29 06:35:48,056: INFO/MainProcess] Task tasks.scrape_pending_urls[cf51485a-4d16-42b5-a0fa-d8cfe47b221d] succeeded in 0.002034100005403161s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,058: INFO/MainProcess] Task tasks.scrape_pending_urls[48409d50-1507-461c-b18d-5884931e5ff8] received
[2026-03-29 06:35:48,060: INFO/MainProcess] Task tasks.scrape_pending_urls[48409d50-1507-461c-b18d-5884931e5ff8] succeeded in 0.002001899993047118s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,061: INFO/MainProcess] Task tasks.scrape_pending_urls[66a2f99a-dc43-4249-88d0-223f02a2f6b4] received
[2026-03-29 06:35:48,065: INFO/MainProcess] Task tasks.scrape_pending_urls[66a2f99a-dc43-4249-88d0-223f02a2f6b4] succeeded in 0.0037620000075548887s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,067: INFO/MainProcess] Task tasks.scrape_pending_urls[e67d5a67-afdf-40c5-a2b1-a75c8d0cdaf3] received
[2026-03-29 06:35:48,069: INFO/MainProcess] Task tasks.scrape_pending_urls[e67d5a67-afdf-40c5-a2b1-a75c8d0cdaf3] succeeded in 0.002186700003221631s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,071: INFO/MainProcess] Task tasks.scrape_pending_urls[91477f64-29dd-4727-b93c-9e61f129d2bd] received
[2026-03-29 06:35:48,073: INFO/MainProcess] Task tasks.scrape_pending_urls[91477f64-29dd-4727-b93c-9e61f129d2bd] succeeded in 0.0020568999461829662s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,074: INFO/MainProcess] Task tasks.scrape_pending_urls[40449d37-6bab-4394-a80d-fa0f30424c30] received
[2026-03-29 06:35:48,077: INFO/MainProcess] Task tasks.scrape_pending_urls[40449d37-6bab-4394-a80d-fa0f30424c30] succeeded in 0.0020219999132677913s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,079: INFO/MainProcess] Task tasks.scrape_pending_urls[73bab211-3a59-4acc-b9eb-155ae4a8f83b] received
[2026-03-29 06:35:48,081: INFO/MainProcess] Task tasks.scrape_pending_urls[73bab211-3a59-4acc-b9eb-155ae4a8f83b] succeeded in 0.0023702000034973025s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,083: INFO/MainProcess] Task tasks.scrape_pending_urls[ea5f64f8-775f-4193-9ce8-d71d791b7076] received
[2026-03-29 06:35:48,085: INFO/MainProcess] Task tasks.scrape_pending_urls[ea5f64f8-775f-4193-9ce8-d71d791b7076] succeeded in 0.0020401999354362488s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,086: INFO/MainProcess] Task tasks.scrape_pending_urls[9ea8cabc-de03-4ae5-9b21-7bd5c7fde203] received
[2026-03-29 06:35:48,089: INFO/MainProcess] Task tasks.scrape_pending_urls[9ea8cabc-de03-4ae5-9b21-7bd5c7fde203] succeeded in 0.002047399990260601s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,090: INFO/MainProcess] Task tasks.scrape_pending_urls[a4fbe2cf-c9fc-4890-9828-8a55bd0b0542] received
[2026-03-29 06:35:48,092: INFO/MainProcess] Task tasks.scrape_pending_urls[a4fbe2cf-c9fc-4890-9828-8a55bd0b0542] succeeded in 0.00202669994905591s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,095: INFO/MainProcess] Task tasks.scrape_pending_urls[078f9e2c-e120-4ab1-865c-c5eb90eec74d] received
[2026-03-29 06:35:48,098: INFO/MainProcess] Task tasks.scrape_pending_urls[078f9e2c-e120-4ab1-865c-c5eb90eec74d] succeeded in 0.0030677999602630734s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,100: INFO/MainProcess] Task tasks.scrape_pending_urls[bdb3fbe5-7359-4632-8f1f-e6f9fa92bc18] received
[2026-03-29 06:35:48,102: INFO/MainProcess] Task tasks.scrape_pending_urls[bdb3fbe5-7359-4632-8f1f-e6f9fa92bc18] succeeded in 0.0020905000856146216s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,103: INFO/MainProcess] Task tasks.scrape_pending_urls[f5b3dcbf-ca49-45ad-aad4-95640eb8e97d] received
[2026-03-29 06:35:48,106: INFO/MainProcess] Task tasks.scrape_pending_urls[f5b3dcbf-ca49-45ad-aad4-95640eb8e97d] succeeded in 0.002027300070039928s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,107: INFO/MainProcess] Task tasks.scrape_pending_urls[44f8a61d-0e04-4a98-a31a-28d8fb097aaa] received
[2026-03-29 06:35:48,110: INFO/MainProcess] Task tasks.scrape_pending_urls[44f8a61d-0e04-4a98-a31a-28d8fb097aaa] succeeded in 0.002791399951092899s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,112: INFO/MainProcess] Task tasks.scrape_pending_urls[ceacedfe-25bb-478b-a626-8e7c0dbbfd23] received
[2026-03-29 06:35:48,114: INFO/MainProcess] Task tasks.scrape_pending_urls[ceacedfe-25bb-478b-a626-8e7c0dbbfd23] succeeded in 0.0021971999667584896s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,116: INFO/MainProcess] Task tasks.scrape_pending_urls[c5c7aa59-f796-4c14-bbb1-8635a94bb776] received
[2026-03-29 06:35:48,118: INFO/MainProcess] Task tasks.scrape_pending_urls[c5c7aa59-f796-4c14-bbb1-8635a94bb776] succeeded in 0.0020318999886512756s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,119: INFO/MainProcess] Task tasks.scrape_pending_urls[33ffcb1e-96cd-4216-ae1f-4ddcdde7b792] received
[2026-03-29 06:35:48,122: INFO/MainProcess] Task tasks.scrape_pending_urls[33ffcb1e-96cd-4216-ae1f-4ddcdde7b792] succeeded in 0.0020886999554932117s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,123: INFO/MainProcess] Task tasks.scrape_pending_urls[ca5486cd-a2e2-4959-b71d-b2123ca25867] received
[2026-03-29 06:35:48,126: INFO/MainProcess] Task tasks.scrape_pending_urls[ca5486cd-a2e2-4959-b71d-b2123ca25867] succeeded in 0.002677600015886128s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,128: INFO/MainProcess] Task tasks.scrape_pending_urls[41ee8a0c-7682-4edf-86ba-d174198d4e02] received
[2026-03-29 06:35:48,131: INFO/MainProcess] Task tasks.scrape_pending_urls[41ee8a0c-7682-4edf-86ba-d174198d4e02] succeeded in 0.0024358000373467803s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,133: INFO/MainProcess] Task tasks.scrape_pending_urls[6fd3d648-4a4e-4e02-a92c-d67ddfe63070] received
[2026-03-29 06:35:48,135: INFO/MainProcess] Task tasks.scrape_pending_urls[6fd3d648-4a4e-4e02-a92c-d67ddfe63070] succeeded in 0.0020217999117448926s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,136: INFO/MainProcess] Task tasks.scrape_pending_urls[d16c4ac8-a824-42db-af01-dbbce6c2ee2f] received
[2026-03-29 06:35:48,139: INFO/MainProcess] Task tasks.scrape_pending_urls[d16c4ac8-a824-42db-af01-dbbce6c2ee2f] succeeded in 0.0020724000642076135s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,140: INFO/MainProcess] Task tasks.scrape_pending_urls[48d88a17-8962-4ccf-8142-84f0b7bc2a5a] received
[2026-03-29 06:35:48,143: INFO/MainProcess] Task tasks.scrape_pending_urls[48d88a17-8962-4ccf-8142-84f0b7bc2a5a] succeeded in 0.002994599984958768s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,144: INFO/MainProcess] Task tasks.scrape_pending_urls[2f0dceb7-a65f-4b07-b091-715d2c67da71] received
[2026-03-29 06:35:48,147: INFO/MainProcess] Task tasks.scrape_pending_urls[2f0dceb7-a65f-4b07-b091-715d2c67da71] succeeded in 0.0021300000371411443s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,148: INFO/MainProcess] Task tasks.scrape_pending_urls[1bc98e33-ff10-4364-87b1-654cf3ef557d] received
[2026-03-29 06:35:48,151: INFO/MainProcess] Task tasks.scrape_pending_urls[1bc98e33-ff10-4364-87b1-654cf3ef557d] succeeded in 0.0020451999735087156s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,152: INFO/MainProcess] Task tasks.scrape_pending_urls[5c290e61-e00a-4053-b854-f3e36a1351ce] received
[2026-03-29 06:35:48,154: INFO/MainProcess] Task tasks.scrape_pending_urls[5c290e61-e00a-4053-b854-f3e36a1351ce] succeeded in 0.002027199952863157s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,156: INFO/MainProcess] Task tasks.scrape_pending_urls[6d777ba2-0755-41c7-bf76-fde8ee381589] received
[2026-03-29 06:35:48,160: INFO/MainProcess] Task tasks.scrape_pending_urls[6d777ba2-0755-41c7-bf76-fde8ee381589] succeeded in 0.003939300077036023s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,162: INFO/MainProcess] Task tasks.scrape_pending_urls[f4316c56-0d89-4e6c-a17a-1e1d801f6557] received
[2026-03-29 06:35:48,165: INFO/MainProcess] Task tasks.scrape_pending_urls[f4316c56-0d89-4e6c-a17a-1e1d801f6557] succeeded in 0.003256399999372661s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,167: INFO/MainProcess] Task tasks.scrape_pending_urls[33d148b7-7d6a-4d60-8671-c186494dd0db] received
[2026-03-29 06:35:48,169: INFO/MainProcess] Task tasks.scrape_pending_urls[33d148b7-7d6a-4d60-8671-c186494dd0db] succeeded in 0.0021419000113382936s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,170: INFO/MainProcess] Task tasks.scrape_pending_urls[352ee657-4a35-493e-a789-fab091dc33f7] received
[2026-03-29 06:35:48,173: INFO/MainProcess] Task tasks.scrape_pending_urls[352ee657-4a35-493e-a789-fab091dc33f7] succeeded in 0.0021765000419691205s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,176: INFO/MainProcess] Task tasks.scrape_pending_urls[5897c511-5ae4-4bb0-be24-318032fdabfb] received
[2026-03-29 06:35:48,179: INFO/MainProcess] Task tasks.scrape_pending_urls[5897c511-5ae4-4bb0-be24-318032fdabfb] succeeded in 0.0023236999986693263s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,180: INFO/MainProcess] Task tasks.scrape_pending_urls[bfaf1fd8-339c-4965-9063-3a1408836808] received
[2026-03-29 06:35:48,183: INFO/MainProcess] Task tasks.scrape_pending_urls[bfaf1fd8-339c-4965-9063-3a1408836808] succeeded in 0.0026893001049757004s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,184: INFO/MainProcess] Task tasks.scrape_pending_urls[261a2b61-130d-4e7a-9070-f9d89c45ed68] received
[2026-03-29 06:35:48,187: INFO/MainProcess] Task tasks.scrape_pending_urls[261a2b61-130d-4e7a-9070-f9d89c45ed68] succeeded in 0.0021437000250443816s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,188: INFO/MainProcess] Task tasks.scrape_pending_urls[efa9fb5d-5bff-4cef-a593-493cf805109e] received
[2026-03-29 06:35:48,191: INFO/MainProcess] Task tasks.scrape_pending_urls[efa9fb5d-5bff-4cef-a593-493cf805109e] succeeded in 0.003000800032168627s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,193: INFO/MainProcess] Task tasks.scrape_pending_urls[b8641d37-5ca1-4395-90c0-be2ca06e8bd0] received
[2026-03-29 06:35:48,195: INFO/MainProcess] Task tasks.scrape_pending_urls[b8641d37-5ca1-4395-90c0-be2ca06e8bd0] succeeded in 0.002234600018709898s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,197: INFO/MainProcess] Task tasks.scrape_pending_urls[4692d08d-38a8-4994-9ff7-b861dfb4477c] received
[2026-03-29 06:35:48,200: INFO/MainProcess] Task tasks.scrape_pending_urls[4692d08d-38a8-4994-9ff7-b861dfb4477c] succeeded in 0.0025510999839752913s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,201: INFO/MainProcess] Task tasks.scrape_pending_urls[1e63bc36-0ef3-440b-8819-26ff5a10ad5c] received
[2026-03-29 06:35:48,203: INFO/MainProcess] Task tasks.scrape_pending_urls[1e63bc36-0ef3-440b-8819-26ff5a10ad5c] succeeded in 0.0020834000315517187s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,205: INFO/MainProcess] Task tasks.scrape_pending_urls[7b83abb5-a9c5-4682-b277-a277b4c9ee58] received
[2026-03-29 06:35:48,209: INFO/MainProcess] Task tasks.scrape_pending_urls[7b83abb5-a9c5-4682-b277-a277b4c9ee58] succeeded in 0.0036975000984966755s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,210: INFO/MainProcess] Task tasks.scrape_pending_urls[1f4478d0-f3e4-4da6-8b7b-3a6299cd3ac8] received
[2026-03-29 06:35:48,212: INFO/MainProcess] Task tasks.scrape_pending_urls[1f4478d0-f3e4-4da6-8b7b-3a6299cd3ac8] succeeded in 0.0021246999967843294s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,213: INFO/MainProcess] Task tasks.scrape_pending_urls[c738226a-8e82-44c3-a04b-9d736aca898f] received
[2026-03-29 06:35:48,216: INFO/MainProcess] Task tasks.scrape_pending_urls[c738226a-8e82-44c3-a04b-9d736aca898f] succeeded in 0.0019845999777317047s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,217: INFO/MainProcess] Task tasks.scrape_pending_urls[1eab9843-b6e8-480d-a961-1dbe685bae47] received
[2026-03-29 06:35:48,219: INFO/MainProcess] Task tasks.scrape_pending_urls[1eab9843-b6e8-480d-a961-1dbe685bae47] succeeded in 0.002026100060902536s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,220: INFO/MainProcess] Task tasks.scrape_pending_urls[cd0b28bb-1657-40af-b711-6661b047e1b0] received
[2026-03-29 06:35:48,225: INFO/MainProcess] Task tasks.scrape_pending_urls[cd0b28bb-1657-40af-b711-6661b047e1b0] succeeded in 0.004038700019009411s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,226: INFO/MainProcess] Task tasks.scrape_pending_urls[178c87c8-132a-43fb-b60f-edd174d5097c] received
[2026-03-29 06:35:48,229: INFO/MainProcess] Task tasks.scrape_pending_urls[178c87c8-132a-43fb-b60f-edd174d5097c] succeeded in 0.0021265000104904175s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,230: INFO/MainProcess] Task tasks.scrape_pending_urls[d4fafd18-2dce-41fe-a933-7cab54da3775] received
[2026-03-29 06:35:48,233: INFO/MainProcess] Task tasks.scrape_pending_urls[d4fafd18-2dce-41fe-a933-7cab54da3775] succeeded in 0.0026820000493898988s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,234: INFO/MainProcess] Task tasks.scrape_pending_urls[7a31bed3-55bf-4e38-baf4-b06063cf3d7c] received
[2026-03-29 06:35:48,237: INFO/MainProcess] Task tasks.scrape_pending_urls[7a31bed3-55bf-4e38-baf4-b06063cf3d7c] succeeded in 0.002279600012116134s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,239: INFO/MainProcess] Task tasks.scrape_pending_urls[b934b204-06da-401d-8f6c-f682e1b092bc] received
[2026-03-29 06:35:48,242: INFO/MainProcess] Task tasks.scrape_pending_urls[b934b204-06da-401d-8f6c-f682e1b092bc] succeeded in 0.002541600028052926s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,243: INFO/MainProcess] Task tasks.scrape_pending_urls[8d0d3825-c975-4778-86b0-13fb99516d7d] received
[2026-03-29 06:35:48,246: INFO/MainProcess] Task tasks.scrape_pending_urls[8d0d3825-c975-4778-86b0-13fb99516d7d] succeeded in 0.0025287000462412834s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,247: INFO/MainProcess] Task tasks.scrape_pending_urls[d58ecae2-d16f-4fc0-b04e-3d61af71162e] received
[2026-03-29 06:35:48,250: INFO/MainProcess] Task tasks.scrape_pending_urls[d58ecae2-d16f-4fc0-b04e-3d61af71162e] succeeded in 0.0020680000307038426s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,251: INFO/MainProcess] Task tasks.scrape_pending_urls[e8158351-d5f4-4fa9-b052-43b54b13a583] received
[2026-03-29 06:35:48,255: INFO/MainProcess] Task tasks.scrape_pending_urls[e8158351-d5f4-4fa9-b052-43b54b13a583] succeeded in 0.003728099982254207s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,257: INFO/MainProcess] Task tasks.scrape_pending_urls[63637bf3-c748-45a2-b883-2de7e2553565] received
[2026-03-29 06:35:48,260: INFO/MainProcess] Task tasks.scrape_pending_urls[63637bf3-c748-45a2-b883-2de7e2553565] succeeded in 0.0027595999417826533s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,262: INFO/MainProcess] Task tasks.scrape_pending_urls[f09c8b04-b1eb-4ed7-985c-06c6942800ef] received
[2026-03-29 06:35:48,265: INFO/MainProcess] Task tasks.scrape_pending_urls[f09c8b04-b1eb-4ed7-985c-06c6942800ef] succeeded in 0.0026017000200226903s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,267: INFO/MainProcess] Task tasks.scrape_pending_urls[06037ba6-4395-4b7f-a4af-50619a42cc04] received
[2026-03-29 06:35:48,271: INFO/MainProcess] Task tasks.scrape_pending_urls[06037ba6-4395-4b7f-a4af-50619a42cc04] succeeded in 0.0036240998888388276s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,273: INFO/MainProcess] Task tasks.scrape_pending_urls[d0c884f3-0c67-4e11-badb-9e7017166960] received
[2026-03-29 06:35:48,276: INFO/MainProcess] Task tasks.scrape_pending_urls[d0c884f3-0c67-4e11-badb-9e7017166960] succeeded in 0.002936400007456541s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,277: INFO/MainProcess] Task tasks.scrape_pending_urls[395d8120-5ec8-4926-9d58-8b4c2513fcf8] received
[2026-03-29 06:35:48,280: INFO/MainProcess] Task tasks.scrape_pending_urls[395d8120-5ec8-4926-9d58-8b4c2513fcf8] succeeded in 0.0020369000267237425s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,281: INFO/MainProcess] Task tasks.scrape_pending_urls[b8ce33b7-7d6e-4d40-93b6-4779b6141ca0] received
[2026-03-29 06:35:48,283: INFO/MainProcess] Task tasks.scrape_pending_urls[b8ce33b7-7d6e-4d40-93b6-4779b6141ca0] succeeded in 0.0019670999608933926s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,285: INFO/MainProcess] Task tasks.scrape_pending_urls[7affcf90-0753-430d-8a0b-0fbdba2c98fc] received
[2026-03-29 06:35:48,290: INFO/MainProcess] Task tasks.scrape_pending_urls[7affcf90-0753-430d-8a0b-0fbdba2c98fc] succeeded in 0.0032056999625638127s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,291: INFO/MainProcess] Task tasks.scrape_pending_urls[c79e4cd9-96e6-4a2e-90e7-9922cad4e163] received
[2026-03-29 06:35:48,295: INFO/MainProcess] Task tasks.scrape_pending_urls[c79e4cd9-96e6-4a2e-90e7-9922cad4e163] succeeded in 0.002796499989926815s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,296: INFO/MainProcess] Task tasks.scrape_pending_urls[c767567b-7a65-4090-84d2-bab7a6f62681] received
[2026-03-29 06:35:48,299: INFO/MainProcess] Task tasks.scrape_pending_urls[c767567b-7a65-4090-84d2-bab7a6f62681] succeeded in 0.002646500011906028s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,301: INFO/MainProcess] Task tasks.scrape_pending_urls[468f7714-29f2-48b3-ad8e-bd66bef002f7] received
[2026-03-29 06:35:48,306: INFO/MainProcess] Task tasks.scrape_pending_urls[468f7714-29f2-48b3-ad8e-bd66bef002f7] succeeded in 0.0036633999552577734s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,308: INFO/MainProcess] Task tasks.scrape_pending_urls[787285be-dde1-4bb4-972d-97340daff294] received
[2026-03-29 06:35:48,312: INFO/MainProcess] Task tasks.scrape_pending_urls[787285be-dde1-4bb4-972d-97340daff294] succeeded in 0.003912400105036795s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,315: INFO/MainProcess] Task tasks.scrape_pending_urls[d5ac61f1-9f46-4b54-860c-c16a7828d5b1] received
[2026-03-29 06:35:48,320: INFO/MainProcess] Task tasks.scrape_pending_urls[d5ac61f1-9f46-4b54-860c-c16a7828d5b1] succeeded in 0.004856299958191812s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,322: INFO/MainProcess] Task tasks.scrape_pending_urls[ce4245e3-a882-4234-a312-ad0c4064dcbe] received
[2026-03-29 06:35:48,326: INFO/MainProcess] Task tasks.scrape_pending_urls[ce4245e3-a882-4234-a312-ad0c4064dcbe] succeeded in 0.003648799960501492s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,328: INFO/MainProcess] Task tasks.scrape_pending_urls[081d03c8-414e-49e4-a117-12e9579dab69] received
[2026-03-29 06:35:48,331: INFO/MainProcess] Task tasks.scrape_pending_urls[081d03c8-414e-49e4-a117-12e9579dab69] succeeded in 0.003590799984522164s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,334: INFO/MainProcess] Task tasks.scrape_pending_urls[e564b1bb-102c-4331-997b-c63deb0a0d6b] received
[2026-03-29 06:35:48,338: INFO/MainProcess] Task tasks.scrape_pending_urls[e564b1bb-102c-4331-997b-c63deb0a0d6b] succeeded in 0.003893999964930117s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,341: INFO/MainProcess] Task tasks.scrape_pending_urls[c7949bfb-0d43-4655-ab8e-f7de310e99b5] received
[2026-03-29 06:35:48,344: INFO/MainProcess] Task tasks.scrape_pending_urls[c7949bfb-0d43-4655-ab8e-f7de310e99b5] succeeded in 0.0027883000439032912s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,345: INFO/MainProcess] Task tasks.scrape_pending_urls[f324f05e-06bd-479e-ba82-638234dfde55] received
[2026-03-29 06:35:48,347: INFO/MainProcess] Task tasks.scrape_pending_urls[f324f05e-06bd-479e-ba82-638234dfde55] succeeded in 0.00201370008289814s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,350: INFO/MainProcess] Task tasks.scrape_pending_urls[4c3b617b-05c8-43c8-8f39-c9098eefbdd1] received
[2026-03-29 06:35:48,353: INFO/MainProcess] Task tasks.scrape_pending_urls[4c3b617b-05c8-43c8-8f39-c9098eefbdd1] succeeded in 0.003104700008407235s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,355: INFO/MainProcess] Task tasks.scrape_pending_urls[23ee4a88-2160-4297-91ca-c3fc4d81c58b] received
[2026-03-29 06:35:48,357: INFO/MainProcess] Task tasks.scrape_pending_urls[23ee4a88-2160-4297-91ca-c3fc4d81c58b] succeeded in 0.0021765000419691205s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,358: INFO/MainProcess] Task tasks.scrape_pending_urls[00e591a6-e51e-4ef3-b819-364d12bec794] received
[2026-03-29 06:35:48,361: INFO/MainProcess] Task tasks.scrape_pending_urls[00e591a6-e51e-4ef3-b819-364d12bec794] succeeded in 0.002116300049237907s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,362: INFO/MainProcess] Task tasks.scrape_pending_urls[dac26a2b-6622-4a85-bd9f-bc1a6fd7b2f0] received
[2026-03-29 06:35:48,364: INFO/MainProcess] Task tasks.scrape_pending_urls[dac26a2b-6622-4a85-bd9f-bc1a6fd7b2f0] succeeded in 0.0021090999944135547s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,366: INFO/MainProcess] Task tasks.scrape_pending_urls[46f5cbee-d937-4dcd-969a-0540a7a35076] received
[2026-03-29 06:35:48,368: INFO/MainProcess] Task tasks.scrape_pending_urls[46f5cbee-d937-4dcd-969a-0540a7a35076] succeeded in 0.002218600013293326s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,370: INFO/MainProcess] Task tasks.scrape_pending_urls[a3f2583c-ff76-46e0-9294-f735757a6693] received
[2026-03-29 06:35:48,372: INFO/MainProcess] Task tasks.scrape_pending_urls[a3f2583c-ff76-46e0-9294-f735757a6693] succeeded in 0.0020895999623462558s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,373: INFO/MainProcess] Task tasks.scrape_pending_urls[7bd1e14e-03bd-4d1b-b3d8-bac747dd5bc3] received
[2026-03-29 06:35:48,375: INFO/MainProcess] Task tasks.scrape_pending_urls[7bd1e14e-03bd-4d1b-b3d8-bac747dd5bc3] succeeded in 0.0020812000147998333s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,377: INFO/MainProcess] Task tasks.scrape_pending_urls[20387388-f3b7-46dd-9055-3c114124290a] received
[2026-03-29 06:35:48,379: INFO/MainProcess] Task tasks.scrape_pending_urls[20387388-f3b7-46dd-9055-3c114124290a] succeeded in 0.002091199974529445s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,380: INFO/MainProcess] Task tasks.scrape_pending_urls[4e40b876-2ea6-4758-9f42-bffd43fa34f2] received
[2026-03-29 06:35:48,384: INFO/MainProcess] Task tasks.scrape_pending_urls[4e40b876-2ea6-4758-9f42-bffd43fa34f2] succeeded in 0.0025155000621452928s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,386: INFO/MainProcess] Task tasks.scrape_pending_urls[37720514-8da4-4227-8dd0-89b4185681b8] received
[2026-03-29 06:35:48,389: INFO/MainProcess] Task tasks.scrape_pending_urls[37720514-8da4-4227-8dd0-89b4185681b8] succeeded in 0.002463500015437603s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,390: INFO/MainProcess] Task tasks.scrape_pending_urls[7ac420b5-fac6-4ccc-82ec-8b85ec5a1ebc] received
[2026-03-29 06:35:48,392: INFO/MainProcess] Task tasks.scrape_pending_urls[7ac420b5-fac6-4ccc-82ec-8b85ec5a1ebc] succeeded in 0.002186099998652935s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,394: INFO/MainProcess] Task tasks.scrape_pending_urls[a0e95543-850c-4434-9e25-b49ea7cc42ed] received
[2026-03-29 06:35:48,396: INFO/MainProcess] Task tasks.scrape_pending_urls[a0e95543-850c-4434-9e25-b49ea7cc42ed] succeeded in 0.0021918999264016747s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,398: INFO/MainProcess] Task tasks.scrape_pending_urls[62777708-f886-4c72-9b24-0a436ad103c8] received
[2026-03-29 06:35:48,401: INFO/MainProcess] Task tasks.scrape_pending_urls[62777708-f886-4c72-9b24-0a436ad103c8] succeeded in 0.002257999964058399s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,402: INFO/MainProcess] Task tasks.scrape_pending_urls[72aee795-a4e1-45dc-ab58-b8e1ca07870a] received
[2026-03-29 06:35:48,404: INFO/MainProcess] Task tasks.scrape_pending_urls[72aee795-a4e1-45dc-ab58-b8e1ca07870a] succeeded in 0.002126300008967519s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,405: INFO/MainProcess] Task tasks.scrape_pending_urls[1cb28c2b-c201-4f2b-bc8b-a0a08809e297] received
[2026-03-29 06:35:48,408: INFO/MainProcess] Task tasks.scrape_pending_urls[1cb28c2b-c201-4f2b-bc8b-a0a08809e297] succeeded in 0.0020970000186935067s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,409: INFO/MainProcess] Task tasks.scrape_pending_urls[49dd6299-7e4b-4838-ab32-d4760499735d] received
[2026-03-29 06:35:48,411: INFO/MainProcess] Task tasks.scrape_pending_urls[49dd6299-7e4b-4838-ab32-d4760499735d] succeeded in 0.002092299982905388s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,413: INFO/MainProcess] Task tasks.scrape_pending_urls[f2c1dd23-638e-4296-94d3-b9de2b219994] received
[2026-03-29 06:35:48,417: INFO/MainProcess] Task tasks.scrape_pending_urls[f2c1dd23-638e-4296-94d3-b9de2b219994] succeeded in 0.0029184999875724316s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,418: INFO/MainProcess] Task tasks.scrape_pending_urls[236d24ff-e906-40dc-bcd4-cd4b19a7d956] received
[2026-03-29 06:35:48,420: INFO/MainProcess] Task tasks.scrape_pending_urls[236d24ff-e906-40dc-bcd4-cd4b19a7d956] succeeded in 0.002254999941214919s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,422: INFO/MainProcess] Task tasks.scrape_pending_urls[00e35d0c-0d44-430e-88be-073f7629cb48] received
[2026-03-29 06:35:48,424: INFO/MainProcess] Task tasks.scrape_pending_urls[00e35d0c-0d44-430e-88be-073f7629cb48] succeeded in 0.0021640999475494027s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,425: INFO/MainProcess] Task tasks.scrape_pending_urls[5f620ddc-3fff-49e6-ad0a-9684bbd556e8] received
[2026-03-29 06:35:48,427: INFO/MainProcess] Task tasks.scrape_pending_urls[5f620ddc-3fff-49e6-ad0a-9684bbd556e8] succeeded in 0.0019994000904262066s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,429: INFO/MainProcess] Task tasks.scrape_pending_urls[61690039-d338-41a1-b1a4-28646d8550b6] received
[2026-03-29 06:35:48,432: INFO/MainProcess] Task tasks.scrape_pending_urls[61690039-d338-41a1-b1a4-28646d8550b6] succeeded in 0.002312400029040873s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,433: INFO/MainProcess] Task tasks.scrape_pending_urls[f6e97726-997a-4ede-a8f3-9f677bec964c] received
[2026-03-29 06:35:48,435: INFO/MainProcess] Task tasks.scrape_pending_urls[f6e97726-997a-4ede-a8f3-9f677bec964c] succeeded in 0.0021201999625191092s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,436: INFO/MainProcess] Task tasks.scrape_pending_urls[64904119-c2d1-44c7-8d23-58f962aa036e] received
[2026-03-29 06:35:48,439: INFO/MainProcess] Task tasks.scrape_pending_urls[64904119-c2d1-44c7-8d23-58f962aa036e] succeeded in 0.0021083999890834093s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,440: INFO/MainProcess] Task tasks.scrape_pending_urls[6643965b-c10f-4ecc-a7d3-60810c19f648] received
[2026-03-29 06:35:48,442: INFO/MainProcess] Task tasks.scrape_pending_urls[6643965b-c10f-4ecc-a7d3-60810c19f648] succeeded in 0.002089899964630604s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,443: INFO/MainProcess] Task tasks.scrape_pending_urls[b23376fb-2782-4e9c-9564-f416cba58171] received
[2026-03-29 06:35:48,447: INFO/MainProcess] Task tasks.scrape_pending_urls[b23376fb-2782-4e9c-9564-f416cba58171] succeeded in 0.0036312000593170524s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,449: INFO/MainProcess] Task tasks.scrape_pending_urls[2ca61e1a-aa30-4ba8-8534-208a86b4095c] received
[2026-03-29 06:35:48,452: INFO/MainProcess] Task tasks.scrape_pending_urls[2ca61e1a-aa30-4ba8-8534-208a86b4095c] succeeded in 0.0024056999245658517s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,453: INFO/MainProcess] Task tasks.scrape_pending_urls[cd5681b9-d57b-4bc7-983f-7383ec94e525] received
[2026-03-29 06:35:48,455: INFO/MainProcess] Task tasks.scrape_pending_urls[cd5681b9-d57b-4bc7-983f-7383ec94e525] succeeded in 0.002169199986383319s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,457: INFO/MainProcess] Task tasks.scrape_pending_urls[5705414f-92f8-481c-9f36-bfece7d4b605] received
[2026-03-29 06:35:48,459: INFO/MainProcess] Task tasks.scrape_pending_urls[5705414f-92f8-481c-9f36-bfece7d4b605] succeeded in 0.002102700062096119s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,460: INFO/MainProcess] Task tasks.scrape_pending_urls[cb1d1baf-2256-45ff-ab54-b2adddbc40a6] received
[2026-03-29 06:35:48,464: INFO/MainProcess] Task tasks.scrape_pending_urls[cb1d1baf-2256-45ff-ab54-b2adddbc40a6] succeeded in 0.002607000060379505s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,465: INFO/MainProcess] Task tasks.scrape_pending_urls[b909942d-2bc8-4421-b7a7-961baeb39d06] received
[2026-03-29 06:35:48,468: INFO/MainProcess] Task tasks.scrape_pending_urls[b909942d-2bc8-4421-b7a7-961baeb39d06] succeeded in 0.0021866000024601817s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,469: INFO/MainProcess] Task tasks.scrape_pending_urls[9d09fd76-67f1-4d59-81b0-d845c1590505] received
[2026-03-29 06:35:48,471: INFO/MainProcess] Task tasks.scrape_pending_urls[9d09fd76-67f1-4d59-81b0-d845c1590505] succeeded in 0.0021106998901814222s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,472: INFO/MainProcess] Task tasks.scrape_pending_urls[f782c6b5-2137-4667-8d58-a2170fc35993] received
[2026-03-29 06:35:48,475: INFO/MainProcess] Task tasks.scrape_pending_urls[f782c6b5-2137-4667-8d58-a2170fc35993] succeeded in 0.002064900007098913s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,476: INFO/MainProcess] Task tasks.scrape_pending_urls[cb198169-668e-4546-9ecf-864d4228d7d5] received
[2026-03-29 06:35:48,480: INFO/MainProcess] Task tasks.scrape_pending_urls[cb198169-668e-4546-9ecf-864d4228d7d5] succeeded in 0.002767500001937151s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,481: INFO/MainProcess] Task tasks.scrape_pending_urls[168a41df-9f5a-494c-a7da-8c96d646e296] received
[2026-03-29 06:35:48,483: INFO/MainProcess] Task tasks.scrape_pending_urls[168a41df-9f5a-494c-a7da-8c96d646e296] succeeded in 0.0022003999911248684s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,485: INFO/MainProcess] Task tasks.scrape_pending_urls[8d0681cb-d77a-47a8-aae2-7871609cac29] received
[2026-03-29 06:35:48,487: INFO/MainProcess] Task tasks.scrape_pending_urls[8d0681cb-d77a-47a8-aae2-7871609cac29] succeeded in 0.0021764999255537987s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,488: INFO/MainProcess] Task tasks.scrape_pending_urls[c43f133f-2365-43ad-aaa3-d2ae31e6ba43] received
[2026-03-29 06:35:48,491: INFO/MainProcess] Task tasks.scrape_pending_urls[c43f133f-2365-43ad-aaa3-d2ae31e6ba43] succeeded in 0.002110700006596744s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,492: INFO/MainProcess] Task tasks.scrape_pending_urls[ffe606cd-2455-4034-92b4-7e8a512627f5] received
[2026-03-29 06:35:48,495: INFO/MainProcess] Task tasks.scrape_pending_urls[ffe606cd-2455-4034-92b4-7e8a512627f5] succeeded in 0.0024109999649226665s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,497: INFO/MainProcess] Task tasks.scrape_pending_urls[ae487eb2-f4c8-4e5a-b124-92bcfa574d69] received
[2026-03-29 06:35:48,499: INFO/MainProcess] Task tasks.scrape_pending_urls[ae487eb2-f4c8-4e5a-b124-92bcfa574d69] succeeded in 0.002217500004917383s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,500: INFO/MainProcess] Task tasks.scrape_pending_urls[404df4de-1006-439e-9642-ccf01242fd86] received
[2026-03-29 06:35:48,503: INFO/MainProcess] Task tasks.scrape_pending_urls[404df4de-1006-439e-9642-ccf01242fd86] succeeded in 0.002219800022430718s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,504: INFO/MainProcess] Task tasks.scrape_pending_urls[d91535de-23fe-4527-a10b-b4aec85c7b5f] received
[2026-03-29 06:35:48,506: INFO/MainProcess] Task tasks.scrape_pending_urls[d91535de-23fe-4527-a10b-b4aec85c7b5f] succeeded in 0.0020942999981343746s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,508: INFO/MainProcess] Task tasks.scrape_pending_urls[47f846a7-12a4-4b43-aade-fb4b0c4bdfc6] received
[2026-03-29 06:35:48,512: INFO/MainProcess] Task tasks.scrape_pending_urls[47f846a7-12a4-4b43-aade-fb4b0c4bdfc6] succeeded in 0.0026526000583544374s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,514: INFO/MainProcess] Task tasks.scrape_pending_urls[1242c527-5494-4c29-a241-62a5b3920b99] received
[2026-03-29 06:35:48,516: INFO/MainProcess] Task tasks.scrape_pending_urls[1242c527-5494-4c29-a241-62a5b3920b99] succeeded in 0.0024965000338852406s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,518: INFO/MainProcess] Task tasks.scrape_pending_urls[91e2a9b3-d1d6-453a-86fe-f0a20e51fea8] received
[2026-03-29 06:35:48,520: INFO/MainProcess] Task tasks.scrape_pending_urls[91e2a9b3-d1d6-453a-86fe-f0a20e51fea8] succeeded in 0.0020626999903470278s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,521: INFO/MainProcess] Task tasks.scrape_pending_urls[886d3ddb-2384-4b8c-9697-af6978d474e4] received
[2026-03-29 06:35:48,524: INFO/MainProcess] Task tasks.scrape_pending_urls[886d3ddb-2384-4b8c-9697-af6978d474e4] succeeded in 0.0023244000039994717s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,527: INFO/MainProcess] Task tasks.scrape_pending_urls[7f293cbf-8e6b-4b33-a860-4cb289478c85] received
[2026-03-29 06:35:48,530: INFO/MainProcess] Task tasks.scrape_pending_urls[7f293cbf-8e6b-4b33-a860-4cb289478c85] succeeded in 0.002814200008288026s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,531: INFO/MainProcess] Task tasks.scrape_pending_urls[8882c37b-051c-473b-bfa5-2659ee869fd9] received
[2026-03-29 06:35:48,534: INFO/MainProcess] Task tasks.scrape_pending_urls[8882c37b-051c-473b-bfa5-2659ee869fd9] succeeded in 0.002143800025805831s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,535: INFO/MainProcess] Task tasks.scrape_pending_urls[41deed7c-7f8f-47aa-9b10-a6d31e52724b] received
[2026-03-29 06:35:48,537: INFO/MainProcess] Task tasks.scrape_pending_urls[41deed7c-7f8f-47aa-9b10-a6d31e52724b] succeeded in 0.0020427999552339315s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,539: INFO/MainProcess] Task tasks.scrape_pending_urls[452fa0e5-ca62-433e-a173-18752b69d65a] received
[2026-03-29 06:35:48,542: INFO/MainProcess] Task tasks.scrape_pending_urls[452fa0e5-ca62-433e-a173-18752b69d65a] succeeded in 0.0031471000984311104s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,543: INFO/MainProcess] Task tasks.scrape_pending_urls[50338cd0-3a69-4335-8628-983fdd634839] received
[2026-03-29 06:35:48,546: INFO/MainProcess] Task tasks.scrape_pending_urls[50338cd0-3a69-4335-8628-983fdd634839] succeeded in 0.0026772000128403306s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,548: INFO/MainProcess] Task tasks.scrape_pending_urls[fcb2611e-0463-4d54-819a-2889d8986978] received
[2026-03-29 06:35:48,550: INFO/MainProcess] Task tasks.scrape_pending_urls[fcb2611e-0463-4d54-819a-2889d8986978] succeeded in 0.0021844999864697456s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,551: INFO/MainProcess] Task tasks.scrape_pending_urls[ffc5658b-6e0e-4ddf-8a0a-4b7329b0789d] received
[2026-03-29 06:35:48,554: INFO/MainProcess] Task tasks.scrape_pending_urls[ffc5658b-6e0e-4ddf-8a0a-4b7329b0789d] succeeded in 0.002033800003118813s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,555: INFO/MainProcess] Task tasks.scrape_pending_urls[4e375b28-9e3e-4209-8cfd-1a847cd0900d] received
[2026-03-29 06:35:48,559: INFO/MainProcess] Task tasks.scrape_pending_urls[4e375b28-9e3e-4209-8cfd-1a847cd0900d] succeeded in 0.003975900006480515s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,560: INFO/MainProcess] Task tasks.scrape_pending_urls[6a0b5164-8536-4b49-84aa-d6cf376295d0] received
[2026-03-29 06:35:48,563: INFO/MainProcess] Task tasks.scrape_pending_urls[6a0b5164-8536-4b49-84aa-d6cf376295d0] succeeded in 0.0020836000330746174s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,564: INFO/MainProcess] Task tasks.scrape_pending_urls[f740b520-95b5-4fe4-bc3c-3a4772f920cd] received
[2026-03-29 06:35:48,566: INFO/MainProcess] Task tasks.scrape_pending_urls[f740b520-95b5-4fe4-bc3c-3a4772f920cd] succeeded in 0.0020125999581068754s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,567: INFO/MainProcess] Task tasks.scrape_pending_urls[f26d3ace-cfe8-4c59-bff9-1b54791dcd5d] received
[2026-03-29 06:35:48,570: INFO/MainProcess] Task tasks.scrape_pending_urls[f26d3ace-cfe8-4c59-bff9-1b54791dcd5d] succeeded in 0.0019651000620797276s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,571: INFO/MainProcess] Task tasks.scrape_pending_urls[43fd315e-b4be-48ab-a315-1bf83ebef989] received
[2026-03-29 06:35:48,575: INFO/MainProcess] Task tasks.scrape_pending_urls[43fd315e-b4be-48ab-a315-1bf83ebef989] succeeded in 0.003963100025430322s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,576: INFO/MainProcess] Task tasks.scrape_pending_urls[50c0ea01-de07-4485-a9ef-b2dd3cec09ee] received
[2026-03-29 06:35:48,579: INFO/MainProcess] Task tasks.scrape_pending_urls[50c0ea01-de07-4485-a9ef-b2dd3cec09ee] succeeded in 0.002261499990709126s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,581: INFO/MainProcess] Task tasks.scrape_pending_urls[2cc877cb-2b66-4cf2-acc6-468bb6b66a58] received
[2026-03-29 06:35:48,583: INFO/MainProcess] Task tasks.scrape_pending_urls[2cc877cb-2b66-4cf2-acc6-468bb6b66a58] succeeded in 0.002562299952842295s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,585: INFO/MainProcess] Task tasks.scrape_pending_urls[7a140f58-bc97-4306-a879-4c28056d49bd] received
[2026-03-29 06:35:48,587: INFO/MainProcess] Task tasks.scrape_pending_urls[7a140f58-bc97-4306-a879-4c28056d49bd] succeeded in 0.002225800068117678s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,589: INFO/MainProcess] Task tasks.scrape_pending_urls[3033ed9b-4083-4199-8430-24e249e6bc8e] received
[2026-03-29 06:35:48,592: INFO/MainProcess] Task tasks.scrape_pending_urls[3033ed9b-4083-4199-8430-24e249e6bc8e] succeeded in 0.0021813000785186887s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,593: INFO/MainProcess] Task tasks.scrape_pending_urls[d10e061d-9e87-4d86-8f38-a3aa1aaa96b1] received
[2026-03-29 06:35:48,595: INFO/MainProcess] Task tasks.scrape_pending_urls[d10e061d-9e87-4d86-8f38-a3aa1aaa96b1] succeeded in 0.001991499913856387s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,596: INFO/MainProcess] Task tasks.scrape_pending_urls[981c6868-4989-40d3-9539-4d35f06d2438] received
[2026-03-29 06:35:48,599: INFO/MainProcess] Task tasks.scrape_pending_urls[981c6868-4989-40d3-9539-4d35f06d2438] succeeded in 0.0019620999228209257s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,600: INFO/MainProcess] Task tasks.scrape_pending_urls[5c0626ba-814f-44f2-a123-8c3f8e3aa669] received
[2026-03-29 06:35:48,602: INFO/MainProcess] Task tasks.scrape_pending_urls[5c0626ba-814f-44f2-a123-8c3f8e3aa669] succeeded in 0.0019725000020116568s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,604: INFO/MainProcess] Task tasks.scrape_pending_urls[204be4a8-82fd-4598-b439-56c31508283a] received
[2026-03-29 06:35:48,607: INFO/MainProcess] Task tasks.scrape_pending_urls[204be4a8-82fd-4598-b439-56c31508283a] succeeded in 0.002625199966132641s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,609: INFO/MainProcess] Task tasks.scrape_pending_urls[89f4d7c7-0a31-4ed5-9c24-389ff05b2958] received
[2026-03-29 06:35:48,612: INFO/MainProcess] Task tasks.scrape_pending_urls[89f4d7c7-0a31-4ed5-9c24-389ff05b2958] succeeded in 0.0026226999470964074s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,613: INFO/MainProcess] Task tasks.scrape_pending_urls[12b8f1c6-1f18-4e59-988a-199bc5992269] received
[2026-03-29 06:35:48,615: INFO/MainProcess] Task tasks.scrape_pending_urls[12b8f1c6-1f18-4e59-988a-199bc5992269] succeeded in 0.0021892000222578645s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,617: INFO/MainProcess] Task tasks.scrape_pending_urls[020144a9-4179-4d8c-b066-f05f9c3de4be] received
[2026-03-29 06:35:48,620: INFO/MainProcess] Task tasks.scrape_pending_urls[020144a9-4179-4d8c-b066-f05f9c3de4be] succeeded in 0.0025546998949721456s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,622: INFO/MainProcess] Task tasks.scrape_pending_urls[40433656-edf4-460b-80e8-a16c8e9a2276] received
[2026-03-29 06:35:48,624: INFO/MainProcess] Task tasks.scrape_pending_urls[40433656-edf4-460b-80e8-a16c8e9a2276] succeeded in 0.0022769999923184514s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,626: INFO/MainProcess] Task tasks.scrape_pending_urls[ad4fc63f-ca4e-4d90-9ad4-eb12839c81d9] received
[2026-03-29 06:35:48,628: INFO/MainProcess] Task tasks.scrape_pending_urls[ad4fc63f-ca4e-4d90-9ad4-eb12839c81d9] succeeded in 0.0020417000632733107s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,629: INFO/MainProcess] Task tasks.scrape_pending_urls[d4f23a8c-6e6d-4b7b-a07d-925621e96fce] received
[2026-03-29 06:35:48,631: INFO/MainProcess] Task tasks.scrape_pending_urls[d4f23a8c-6e6d-4b7b-a07d-925621e96fce] succeeded in 0.0019856999861076474s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,633: INFO/MainProcess] Task tasks.scrape_pending_urls[a2d099be-8f3f-450a-91a4-c15bf94c6321] received
[2026-03-29 06:35:48,635: INFO/MainProcess] Task tasks.scrape_pending_urls[a2d099be-8f3f-450a-91a4-c15bf94c6321] succeeded in 0.0021652000723406672s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,638: INFO/MainProcess] Task tasks.scrape_pending_urls[43479d4f-af49-4b7f-b352-c3bac9d44fab] received
[2026-03-29 06:35:48,641: INFO/MainProcess] Task tasks.scrape_pending_urls[43479d4f-af49-4b7f-b352-c3bac9d44fab] succeeded in 0.0022338000126183033s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,642: INFO/MainProcess] Task tasks.scrape_pending_urls[37d7e104-1b91-4e1a-9fd2-43df11ae3426] received
[2026-03-29 06:35:48,644: INFO/MainProcess] Task tasks.scrape_pending_urls[37d7e104-1b91-4e1a-9fd2-43df11ae3426] succeeded in 0.0020052000181749463s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,646: INFO/MainProcess] Task tasks.scrape_pending_urls[7a04e9d7-3c06-4a26-a784-c69228ca85dc] received
[2026-03-29 06:35:48,648: INFO/MainProcess] Task tasks.scrape_pending_urls[7a04e9d7-3c06-4a26-a784-c69228ca85dc] succeeded in 0.002554900012910366s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,650: INFO/MainProcess] Task tasks.scrape_pending_urls[f4aa5a24-3136-4e9c-954d-b34e15a621fe] received
[2026-03-29 06:35:48,653: INFO/MainProcess] Task tasks.scrape_pending_urls[f4aa5a24-3136-4e9c-954d-b34e15a621fe] succeeded in 0.002910400042310357s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,654: INFO/MainProcess] Task tasks.scrape_pending_urls[dc7b3fdf-b3d5-4085-9da7-13cb337141e8] received
[2026-03-29 06:35:48,657: INFO/MainProcess] Task tasks.scrape_pending_urls[dc7b3fdf-b3d5-4085-9da7-13cb337141e8] succeeded in 0.002085900050587952s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,658: INFO/MainProcess] Task tasks.scrape_pending_urls[198f9f72-445a-4331-81c8-f8508d64052b] received
[2026-03-29 06:35:48,660: INFO/MainProcess] Task tasks.scrape_pending_urls[198f9f72-445a-4331-81c8-f8508d64052b] succeeded in 0.0020887000719085336s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,661: INFO/MainProcess] Task tasks.scrape_pending_urls[0a793c9d-3967-4790-b3e7-0b262c220c32] received
[2026-03-29 06:35:48,664: INFO/MainProcess] Task tasks.scrape_pending_urls[0a793c9d-3967-4790-b3e7-0b262c220c32] succeeded in 0.0019579000072553754s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,665: INFO/MainProcess] Task tasks.scrape_pending_urls[c5878deb-f632-4227-acac-401a2ee49273] received
[2026-03-29 06:35:48,668: INFO/MainProcess] Task tasks.scrape_pending_urls[c5878deb-f632-4227-acac-401a2ee49273] succeeded in 0.003024800098501146s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,670: INFO/MainProcess] Task tasks.scrape_pending_urls[3e59c390-6048-480e-adce-35d04ee3c508] received
[2026-03-29 06:35:48,672: INFO/MainProcess] Task tasks.scrape_pending_urls[3e59c390-6048-480e-adce-35d04ee3c508] succeeded in 0.002264800015836954s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,674: INFO/MainProcess] Task tasks.scrape_pending_urls[ee523b1f-8058-4303-81c0-c5515e5a102c] received
[2026-03-29 06:35:48,677: INFO/MainProcess] Task tasks.scrape_pending_urls[ee523b1f-8058-4303-81c0-c5515e5a102c] succeeded in 0.0026443999959155917s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,678: INFO/MainProcess] Task tasks.scrape_pending_urls[c0a1dfba-1c0c-44c4-9da4-cdca59145ec7] received
[2026-03-29 06:35:48,680: INFO/MainProcess] Task tasks.scrape_pending_urls[c0a1dfba-1c0c-44c4-9da4-cdca59145ec7] succeeded in 0.0021175999427214265s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,681: INFO/MainProcess] Task tasks.scrape_pending_urls[6ea66dbc-6fe4-4051-91bb-1d962e8b27a1] received
[2026-03-29 06:35:48,685: INFO/MainProcess] Task tasks.scrape_pending_urls[6ea66dbc-6fe4-4051-91bb-1d962e8b27a1] succeeded in 0.0023462000535801053s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,686: INFO/MainProcess] Task tasks.scrape_pending_urls[baca8961-3fd9-412a-a073-39b656a9faad] received
[2026-03-29 06:35:48,689: INFO/MainProcess] Task tasks.scrape_pending_urls[baca8961-3fd9-412a-a073-39b656a9faad] succeeded in 0.002092299982905388s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,690: INFO/MainProcess] Task tasks.scrape_pending_urls[623f820b-ebad-4256-8605-4fbdd8185a96] received
[2026-03-29 06:35:48,692: INFO/MainProcess] Task tasks.scrape_pending_urls[623f820b-ebad-4256-8605-4fbdd8185a96] succeeded in 0.0020809000125154853s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,694: INFO/MainProcess] Task tasks.scrape_pending_urls[6e8f0fc1-f6ac-4b98-83cf-d52971cdb267] received
[2026-03-29 06:35:48,696: INFO/MainProcess] Task tasks.scrape_pending_urls[6e8f0fc1-f6ac-4b98-83cf-d52971cdb267] succeeded in 0.0020717999432235956s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,697: INFO/MainProcess] Task tasks.scrape_pending_urls[5e9a27ce-a7d7-46be-93cf-60de746de714] received
[2026-03-29 06:35:48,701: INFO/MainProcess] Task tasks.scrape_pending_urls[5e9a27ce-a7d7-46be-93cf-60de746de714] succeeded in 0.002429499989375472s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,702: INFO/MainProcess] Task tasks.scrape_pending_urls[a3ddf45e-f12f-43e5-93d5-a84f27519b4a] received
[2026-03-29 06:35:48,705: INFO/MainProcess] Task tasks.scrape_pending_urls[a3ddf45e-f12f-43e5-93d5-a84f27519b4a] succeeded in 0.0021349999587982893s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,706: INFO/MainProcess] Task tasks.scrape_pending_urls[d51dfcb4-c94a-466a-a94e-572c851039e2] received
[2026-03-29 06:35:48,708: INFO/MainProcess] Task tasks.scrape_pending_urls[d51dfcb4-c94a-466a-a94e-572c851039e2] succeeded in 0.0020848000422120094s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,710: INFO/MainProcess] Task tasks.scrape_pending_urls[a5d80203-787f-444c-8bc4-82a67b281a68] received
[2026-03-29 06:35:48,713: INFO/MainProcess] Task tasks.scrape_pending_urls[a5d80203-787f-444c-8bc4-82a67b281a68] succeeded in 0.0027470000786706805s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,715: INFO/MainProcess] Task tasks.scrape_pending_urls[af4b0713-742c-4c3a-9d9c-5b86fe1f40a1] received
[2026-03-29 06:35:48,717: INFO/MainProcess] Task tasks.scrape_pending_urls[af4b0713-742c-4c3a-9d9c-5b86fe1f40a1] succeeded in 0.0022984000388532877s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,718: INFO/MainProcess] Task tasks.scrape_pending_urls[b2366323-438b-441b-9d2b-96ff57c6ed8a] received
[2026-03-29 06:35:48,721: INFO/MainProcess] Task tasks.scrape_pending_urls[b2366323-438b-441b-9d2b-96ff57c6ed8a] succeeded in 0.0021335999481379986s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,722: INFO/MainProcess] Task tasks.scrape_pending_urls[aaa9f7f4-b0a2-45f8-a88f-461a055affc4] received
[2026-03-29 06:35:48,724: INFO/MainProcess] Task tasks.scrape_pending_urls[aaa9f7f4-b0a2-45f8-a88f-461a055affc4] succeeded in 0.002097700024023652s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,726: INFO/MainProcess] Task tasks.scrape_pending_urls[50bf6a4f-d8ba-4cc3-8a5d-500ba838b190] received
[2026-03-29 06:35:48,728: INFO/MainProcess] Task tasks.scrape_pending_urls[50bf6a4f-d8ba-4cc3-8a5d-500ba838b190] succeeded in 0.002093199989758432s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,730: INFO/MainProcess] Task tasks.scrape_pending_urls[4fadb374-3106-4850-99e2-3eb85e13b16d] received
[2026-03-29 06:35:48,733: INFO/MainProcess] Task tasks.scrape_pending_urls[4fadb374-3106-4850-99e2-3eb85e13b16d] succeeded in 0.0025483000790700316s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,734: INFO/MainProcess] Task tasks.scrape_pending_urls[167f83bd-44fd-40e0-a12e-126800d02376] received
[2026-03-29 06:35:48,737: INFO/MainProcess] Task tasks.scrape_pending_urls[167f83bd-44fd-40e0-a12e-126800d02376] succeeded in 0.002176900045014918s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,738: INFO/MainProcess] Task tasks.scrape_pending_urls[5cd0980a-3fe9-4253-868a-6f30669a92a9] received
[2026-03-29 06:35:48,741: INFO/MainProcess] Task tasks.scrape_pending_urls[5cd0980a-3fe9-4253-868a-6f30669a92a9] succeeded in 0.0027968999929726124s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,743: INFO/MainProcess] Task tasks.scrape_pending_urls[068f6234-f465-492f-84f3-6139620eb483] received
[2026-03-29 06:35:48,745: INFO/MainProcess] Task tasks.scrape_pending_urls[068f6234-f465-492f-84f3-6139620eb483] succeeded in 0.002580300089903176s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,748: INFO/MainProcess] Task tasks.scrape_pending_urls[fb60b47c-1415-49ef-a90a-c2d162685629] received
[2026-03-29 06:35:48,750: INFO/MainProcess] Task tasks.scrape_pending_urls[fb60b47c-1415-49ef-a90a-c2d162685629] succeeded in 0.0024100999580696225s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,752: INFO/MainProcess] Task tasks.scrape_pending_urls[cf71cd65-f005-4d70-bcd4-5538122fa022] received
[2026-03-29 06:35:48,755: INFO/MainProcess] Task tasks.scrape_pending_urls[cf71cd65-f005-4d70-bcd4-5538122fa022] succeeded in 0.002458099974319339s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,756: INFO/MainProcess] Task tasks.scrape_pending_urls[7bcc7ac0-6ded-4917-9402-c9b6f7ac837e] received
[2026-03-29 06:35:48,758: INFO/MainProcess] Task tasks.scrape_pending_urls[7bcc7ac0-6ded-4917-9402-c9b6f7ac837e] succeeded in 0.002350500086322427s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,760: INFO/MainProcess] Task tasks.scrape_pending_urls[165fbc97-9026-4207-a1f1-4036412c7cef] received
[2026-03-29 06:35:48,763: INFO/MainProcess] Task tasks.scrape_pending_urls[165fbc97-9026-4207-a1f1-4036412c7cef] succeeded in 0.0033769001020118594s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,765: INFO/MainProcess] Task tasks.scrape_pending_urls[c22f6c44-8e60-425b-9aea-81c122f85594] received
[2026-03-29 06:35:48,767: INFO/MainProcess] Task tasks.scrape_pending_urls[c22f6c44-8e60-425b-9aea-81c122f85594] succeeded in 0.0023705000057816505s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,769: INFO/MainProcess] Task tasks.scrape_pending_urls[9f0136b3-a367-4718-9b54-c4067a3d9ebd] received
[2026-03-29 06:35:48,771: INFO/MainProcess] Task tasks.scrape_pending_urls[9f0136b3-a367-4718-9b54-c4067a3d9ebd] succeeded in 0.002208600053563714s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,773: INFO/MainProcess] Task tasks.scrape_pending_urls[6c4d6c29-4b90-42f6-9727-d0a8b2f0c86d] received
[2026-03-29 06:35:48,775: INFO/MainProcess] Task tasks.scrape_pending_urls[6c4d6c29-4b90-42f6-9727-d0a8b2f0c86d] succeeded in 0.0022063000360503793s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,777: INFO/MainProcess] Task tasks.scrape_pending_urls[bb8ceb33-2377-4ee4-b355-e7f5aa0b7304] received
[2026-03-29 06:35:48,780: INFO/MainProcess] Task tasks.scrape_pending_urls[bb8ceb33-2377-4ee4-b355-e7f5aa0b7304] succeeded in 0.003155199927277863s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,781: INFO/MainProcess] Task tasks.scrape_pending_urls[dadf237d-fc66-4c99-ab64-e76f8957eeac] received
[2026-03-29 06:35:48,784: INFO/MainProcess] Task tasks.scrape_pending_urls[dadf237d-fc66-4c99-ab64-e76f8957eeac] succeeded in 0.002132499939762056s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,785: INFO/MainProcess] Task tasks.scrape_pending_urls[13f54a41-e7a7-4a5d-b930-4917b8b9a2e8] received
[2026-03-29 06:35:48,787: INFO/MainProcess] Task tasks.scrape_pending_urls[13f54a41-e7a7-4a5d-b930-4917b8b9a2e8] succeeded in 0.0020263000624254346s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,789: INFO/MainProcess] Task tasks.scrape_pending_urls[607382ef-7559-42c9-a7d3-7ace265e5168] received
[2026-03-29 06:35:48,791: INFO/MainProcess] Task tasks.scrape_pending_urls[607382ef-7559-42c9-a7d3-7ace265e5168] succeeded in 0.0020278000738471746s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,792: INFO/MainProcess] Task tasks.scrape_pending_urls[7c241fdd-7cfa-4032-ae5a-51dd9ab32cbd] received
[2026-03-29 06:35:48,796: INFO/MainProcess] Task tasks.scrape_pending_urls[7c241fdd-7cfa-4032-ae5a-51dd9ab32cbd] succeeded in 0.0035230000503361225s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,797: INFO/MainProcess] Task tasks.scrape_pending_urls[eda81e27-d871-4756-a9ce-575cae093256] received
[2026-03-29 06:35:48,800: INFO/MainProcess] Task tasks.scrape_pending_urls[eda81e27-d871-4756-a9ce-575cae093256] succeeded in 0.002266800031065941s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,801: INFO/MainProcess] Task tasks.scrape_pending_urls[ff9c4542-a896-42eb-80c3-44fbf8dbdf77] received
[2026-03-29 06:35:48,803: INFO/MainProcess] Task tasks.scrape_pending_urls[ff9c4542-a896-42eb-80c3-44fbf8dbdf77] succeeded in 0.002189700026065111s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,805: INFO/MainProcess] Task tasks.scrape_pending_urls[6f2e89af-a739-4cbe-b3d7-c5e1dc5cdc9c] received
[2026-03-29 06:35:48,808: INFO/MainProcess] Task tasks.scrape_pending_urls[6f2e89af-a739-4cbe-b3d7-c5e1dc5cdc9c] succeeded in 0.002702199970372021s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,809: INFO/MainProcess] Task tasks.scrape_pending_urls[1fb3b3b2-fd00-41f2-94f4-26d8190d61ba] received
[2026-03-29 06:35:48,812: INFO/MainProcess] Task tasks.scrape_pending_urls[1fb3b3b2-fd00-41f2-94f4-26d8190d61ba] succeeded in 0.002416699891909957s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,814: INFO/MainProcess] Task tasks.scrape_pending_urls[23b5cc7b-d679-493b-a5c8-970d652cf05b] received
[2026-03-29 06:35:48,816: INFO/MainProcess] Task tasks.scrape_pending_urls[23b5cc7b-d679-493b-a5c8-970d652cf05b] succeeded in 0.0022358999121934175s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,817: INFO/MainProcess] Task tasks.scrape_pending_urls[77d0d7ad-d7f8-4307-b53b-07f0e6c8a803] received
[2026-03-29 06:35:48,820: INFO/MainProcess] Task tasks.scrape_pending_urls[77d0d7ad-d7f8-4307-b53b-07f0e6c8a803] succeeded in 0.0021772999316453934s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,821: INFO/MainProcess] Task tasks.scrape_pending_urls[7dd725e3-18f5-4a9c-9c4f-8c48590a61d9] received
[2026-03-29 06:35:48,823: INFO/MainProcess] Task tasks.scrape_pending_urls[7dd725e3-18f5-4a9c-9c4f-8c48590a61d9] succeeded in 0.002184600103646517s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,825: INFO/MainProcess] Task tasks.scrape_pending_urls[8dc4183d-cf5f-4998-974d-767b4b4bca4e] received
[2026-03-29 06:35:48,829: INFO/MainProcess] Task tasks.scrape_pending_urls[8dc4183d-cf5f-4998-974d-767b4b4bca4e] succeeded in 0.002360299928113818s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,830: INFO/MainProcess] Task tasks.scrape_pending_urls[2cd3b694-5c3a-405d-af1c-a7b8b7791f1b] received
[2026-03-29 06:35:48,832: INFO/MainProcess] Task tasks.scrape_pending_urls[2cd3b694-5c3a-405d-af1c-a7b8b7791f1b] succeeded in 0.0020122000714764s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,834: INFO/MainProcess] Task tasks.scrape_pending_urls[231e8d84-186a-421d-b81f-44e09d7a80c7] received
[2026-03-29 06:35:48,836: INFO/MainProcess] Task tasks.scrape_pending_urls[231e8d84-186a-421d-b81f-44e09d7a80c7] succeeded in 0.001998899970203638s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,837: INFO/MainProcess] Task tasks.scrape_pending_urls[6ef4b89c-91f2-4615-bf63-ef59600af6a8] received
[2026-03-29 06:35:48,839: INFO/MainProcess] Task tasks.scrape_pending_urls[6ef4b89c-91f2-4615-bf63-ef59600af6a8] succeeded in 0.0020105999428778887s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,841: INFO/MainProcess] Task tasks.scrape_pending_urls[b33a8ed1-5d6b-45b6-8c1f-740f4f6fdc2a] received
[2026-03-29 06:35:48,845: INFO/MainProcess] Task tasks.scrape_pending_urls[b33a8ed1-5d6b-45b6-8c1f-740f4f6fdc2a] succeeded in 0.0025179999647662044s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,846: INFO/MainProcess] Task tasks.scrape_pending_urls[39b92e84-7f44-40d3-932a-9cad2d67903a] received
[2026-03-29 06:35:48,848: INFO/MainProcess] Task tasks.scrape_pending_urls[39b92e84-7f44-40d3-932a-9cad2d67903a] succeeded in 0.002245199983008206s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,850: INFO/MainProcess] Task tasks.scrape_pending_urls[20af8932-fd3b-4e4d-be32-0c4c506282d1] received
[2026-03-29 06:35:48,852: INFO/MainProcess] Task tasks.scrape_pending_urls[20af8932-fd3b-4e4d-be32-0c4c506282d1] succeeded in 0.0021924000466242433s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,853: INFO/MainProcess] Task tasks.scrape_pending_urls[a493789b-a6c5-46a6-b631-688a36db44e3] received
[2026-03-29 06:35:48,856: INFO/MainProcess] Task tasks.scrape_pending_urls[a493789b-a6c5-46a6-b631-688a36db44e3] succeeded in 0.0021723000099882483s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,857: INFO/MainProcess] Task tasks.scrape_pending_urls[c3cae25c-db26-4d9d-a5db-05474bdb15f7] received
[2026-03-29 06:35:48,861: INFO/MainProcess] Task tasks.scrape_pending_urls[c3cae25c-db26-4d9d-a5db-05474bdb15f7] succeeded in 0.0024057000409811735s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,862: INFO/MainProcess] Task tasks.scrape_pending_urls[4622996d-8f11-4067-b874-eb5bc556669b] received
[2026-03-29 06:35:48,864: INFO/MainProcess] Task tasks.scrape_pending_urls[4622996d-8f11-4067-b874-eb5bc556669b] succeeded in 0.002035900019109249s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,866: INFO/MainProcess] Task tasks.scrape_pending_urls[d870f37e-d5a6-44ef-90d9-087d9d806d02] received
[2026-03-29 06:35:48,868: INFO/MainProcess] Task tasks.scrape_pending_urls[d870f37e-d5a6-44ef-90d9-087d9d806d02] succeeded in 0.0019985000835731626s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,869: INFO/MainProcess] Task tasks.scrape_pending_urls[09bbc0d7-4f4c-4d9d-81db-fcc6c2ef1a57] received
[2026-03-29 06:35:48,872: INFO/MainProcess] Task tasks.scrape_pending_urls[09bbc0d7-4f4c-4d9d-81db-fcc6c2ef1a57] succeeded in 0.0026415999745950103s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,874: INFO/MainProcess] Task tasks.scrape_pending_urls[b8fef69a-754b-4c6f-8aaf-f8a9378a1d96] received
[2026-03-29 06:35:48,876: INFO/MainProcess] Task tasks.scrape_pending_urls[b8fef69a-754b-4c6f-8aaf-f8a9378a1d96] succeeded in 0.002175699919462204s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,878: INFO/MainProcess] Task tasks.scrape_pending_urls[8815cf45-e1e1-406c-b34a-4d32f4deaf1e] received
[2026-03-29 06:35:48,880: INFO/MainProcess] Task tasks.scrape_pending_urls[8815cf45-e1e1-406c-b34a-4d32f4deaf1e] succeeded in 0.0020460999803617597s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,881: INFO/MainProcess] Task tasks.scrape_pending_urls[884f3acd-491c-49ef-ab0e-5f482426f648] received
[2026-03-29 06:35:48,884: INFO/MainProcess] Task tasks.scrape_pending_urls[884f3acd-491c-49ef-ab0e-5f482426f648] succeeded in 0.0020611999789252877s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,885: INFO/MainProcess] Task tasks.scrape_pending_urls[ac798a69-e705-4f04-980a-0917d05f1f0b] received
[2026-03-29 06:35:48,887: INFO/MainProcess] Task tasks.scrape_pending_urls[ac798a69-e705-4f04-980a-0917d05f1f0b] succeeded in 0.0020764999790117145s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,888: INFO/MainProcess] Task tasks.scrape_pending_urls[2db30256-551b-4a07-8939-7d30d35cac61] received
[2026-03-29 06:35:48,893: INFO/MainProcess] Task tasks.scrape_pending_urls[2db30256-551b-4a07-8939-7d30d35cac61] succeeded in 0.002864300040528178s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,895: INFO/MainProcess] Task tasks.scrape_pending_urls[dc8a6090-7b26-4de9-9e5d-c5f7775d1a19] received
[2026-03-29 06:35:48,897: INFO/MainProcess] Task tasks.scrape_pending_urls[dc8a6090-7b26-4de9-9e5d-c5f7775d1a19] succeeded in 0.0020935999928042293s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,898: INFO/MainProcess] Task tasks.scrape_pending_urls[4e46b389-8a84-425d-873d-73cbbb494a2e] received
[2026-03-29 06:35:48,900: INFO/MainProcess] Task tasks.scrape_pending_urls[4e46b389-8a84-425d-873d-73cbbb494a2e] succeeded in 0.002014199970290065s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,902: INFO/MainProcess] Task tasks.scrape_pending_urls[e978ab15-1d6c-40a4-91df-d2b9767c3851] received
[2026-03-29 06:35:48,904: INFO/MainProcess] Task tasks.scrape_pending_urls[e978ab15-1d6c-40a4-91df-d2b9767c3851] succeeded in 0.002000999986194074s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,906: INFO/MainProcess] Task tasks.scrape_pending_urls[ab94218e-65d2-4971-a66d-a20431ba1c17] received
[2026-03-29 06:35:48,910: INFO/MainProcess] Task tasks.scrape_pending_urls[ab94218e-65d2-4971-a66d-a20431ba1c17] succeeded in 0.0023682001046836376s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,911: INFO/MainProcess] Task tasks.scrape_pending_urls[2b718a51-0976-489d-8f10-28c179600321] received
[2026-03-29 06:35:48,914: INFO/MainProcess] Task tasks.scrape_pending_urls[2b718a51-0976-489d-8f10-28c179600321] succeeded in 0.002083800034597516s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,915: INFO/MainProcess] Task tasks.scrape_pending_urls[fae43c77-dc96-4a2b-bd85-bc6d449da181] received
[2026-03-29 06:35:48,917: INFO/MainProcess] Task tasks.scrape_pending_urls[fae43c77-dc96-4a2b-bd85-bc6d449da181] succeeded in 0.0020970000186935067s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,918: INFO/MainProcess] Task tasks.scrape_pending_urls[1afbf6f5-3da6-4308-920d-549752b04eb2] received
[2026-03-29 06:35:48,921: INFO/MainProcess] Task tasks.scrape_pending_urls[1afbf6f5-3da6-4308-920d-549752b04eb2] succeeded in 0.002688499982468784s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,924: INFO/MainProcess] Task tasks.scrape_pending_urls[5990a657-2b6f-48b3-8cce-f9f6067e3418] received
[2026-03-29 06:35:48,926: INFO/MainProcess] Task tasks.scrape_pending_urls[5990a657-2b6f-48b3-8cce-f9f6067e3418] succeeded in 0.0022971000289544463s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,928: INFO/MainProcess] Task tasks.scrape_pending_urls[c8fdd15d-d6fc-44e0-9a51-9d15b2241d02] received
[2026-03-29 06:35:48,930: INFO/MainProcess] Task tasks.scrape_pending_urls[c8fdd15d-d6fc-44e0-9a51-9d15b2241d02] succeeded in 0.0021269998978823423s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,931: INFO/MainProcess] Task tasks.scrape_pending_urls[cb5e25c6-76cb-4473-8b9c-661a025feb01] received
[2026-03-29 06:35:48,934: INFO/MainProcess] Task tasks.scrape_pending_urls[cb5e25c6-76cb-4473-8b9c-661a025feb01] succeeded in 0.002054099924862385s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,935: INFO/MainProcess] Task tasks.scrape_pending_urls[8d9ff467-dad0-4cf0-9573-a84bab79a75a] received
[2026-03-29 06:35:48,939: INFO/MainProcess] Task tasks.scrape_pending_urls[8d9ff467-dad0-4cf0-9573-a84bab79a75a] succeeded in 0.003535000025294721s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,940: INFO/MainProcess] Task tasks.scrape_pending_urls[ebcae2b3-ddbc-41f7-93e3-96caa588fa1c] received
[2026-03-29 06:35:48,943: INFO/MainProcess] Task tasks.scrape_pending_urls[ebcae2b3-ddbc-41f7-93e3-96caa588fa1c] succeeded in 0.0021105000050738454s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,944: INFO/MainProcess] Task tasks.scrape_pending_urls[79b806a8-12c0-430f-89b6-3d1b68634298] received
[2026-03-29 06:35:48,946: INFO/MainProcess] Task tasks.scrape_pending_urls[79b806a8-12c0-430f-89b6-3d1b68634298] succeeded in 0.0019990000873804092s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,947: INFO/MainProcess] Task tasks.scrape_pending_urls[1e0b05dc-8646-41f9-ba5f-b11ea3659e12] received
[2026-03-29 06:35:48,950: INFO/MainProcess] Task tasks.scrape_pending_urls[1e0b05dc-8646-41f9-ba5f-b11ea3659e12] succeeded in 0.001995700062252581s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,951: INFO/MainProcess] Task tasks.scrape_pending_urls[0f4681a3-ddb5-46b8-8062-e7476a6e8dc5] received
[2026-03-29 06:35:48,954: INFO/MainProcess] Task tasks.scrape_pending_urls[0f4681a3-ddb5-46b8-8062-e7476a6e8dc5] succeeded in 0.002940199919976294s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,956: INFO/MainProcess] Task tasks.scrape_pending_urls[53168824-1373-4be3-b36c-e6736e3934d5] received
[2026-03-29 06:35:48,959: INFO/MainProcess] Task tasks.scrape_pending_urls[53168824-1373-4be3-b36c-e6736e3934d5] succeeded in 0.002914499957114458s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,961: INFO/MainProcess] Task tasks.scrape_pending_urls[f176a5db-7613-4201-bc7f-e9556cd00304] received
[2026-03-29 06:35:48,963: INFO/MainProcess] Task tasks.scrape_pending_urls[f176a5db-7613-4201-bc7f-e9556cd00304] succeeded in 0.0021660999627783895s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,964: INFO/MainProcess] Task tasks.scrape_pending_urls[cd5a6a95-0f10-465d-9932-28e986386f3f] received
[2026-03-29 06:35:48,967: INFO/MainProcess] Task tasks.scrape_pending_urls[cd5a6a95-0f10-465d-9932-28e986386f3f] succeeded in 0.002069000038318336s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,968: INFO/MainProcess] Task tasks.scrape_pending_urls[d335e236-07b1-4d89-8f38-28df95098d68] received
[2026-03-29 06:35:48,972: INFO/MainProcess] Task tasks.scrape_pending_urls[d335e236-07b1-4d89-8f38-28df95098d68] succeeded in 0.0032133000204339623s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,973: INFO/MainProcess] Task tasks.scrape_pending_urls[a8096c53-a7a5-4a60-9986-36f0872ad3a8] received
[2026-03-29 06:35:48,975: INFO/MainProcess] Task tasks.scrape_pending_urls[a8096c53-a7a5-4a60-9986-36f0872ad3a8] succeeded in 0.002215999993495643s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,977: INFO/MainProcess] Task tasks.scrape_pending_urls[c270bb7c-c418-4bc0-badf-dcd07a281961] received
[2026-03-29 06:35:48,979: INFO/MainProcess] Task tasks.scrape_pending_urls[c270bb7c-c418-4bc0-badf-dcd07a281961] succeeded in 0.002083800034597516s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,980: INFO/MainProcess] Task tasks.scrape_pending_urls[aa469596-606b-4d94-bfd3-a07b51effdd1] received
[2026-03-29 06:35:48,982: INFO/MainProcess] Task tasks.scrape_pending_urls[aa469596-606b-4d94-bfd3-a07b51effdd1] succeeded in 0.002041399944573641s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,984: INFO/MainProcess] Task tasks.scrape_pending_urls[61acf5aa-952f-47b1-8884-a55ef6d57502] received
[2026-03-29 06:35:48,988: INFO/MainProcess] Task tasks.scrape_pending_urls[61acf5aa-952f-47b1-8884-a55ef6d57502] succeeded in 0.004386899992823601s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,990: INFO/MainProcess] Task tasks.scrape_pending_urls[07ec10d9-d6df-421a-af14-b250f8d2c9ac] received
[2026-03-29 06:35:48,992: INFO/MainProcess] Task tasks.scrape_pending_urls[07ec10d9-d6df-421a-af14-b250f8d2c9ac] succeeded in 0.0022704999428242445s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,994: INFO/MainProcess] Task tasks.scrape_pending_urls[6a1e6fbd-ce94-41c4-b19a-3c85e5259906] received
[2026-03-29 06:35:48,996: INFO/MainProcess] Task tasks.scrape_pending_urls[6a1e6fbd-ce94-41c4-b19a-3c85e5259906] succeeded in 0.002026100060902536s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:48,997: INFO/MainProcess] Task tasks.scrape_pending_urls[becf3b29-f341-4f8a-bba7-715b5e18469b] received
[2026-03-29 06:35:48,999: INFO/MainProcess] Task tasks.scrape_pending_urls[becf3b29-f341-4f8a-bba7-715b5e18469b] succeeded in 0.002034700009971857s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,001: INFO/MainProcess] Task tasks.scrape_pending_urls[169cb273-9b23-4d79-9200-bfc4fe46878a] received
[2026-03-29 06:35:49,007: INFO/MainProcess] Task tasks.scrape_pending_urls[169cb273-9b23-4d79-9200-bfc4fe46878a] succeeded in 0.004042199929244816s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,009: INFO/MainProcess] Task tasks.scrape_pending_urls[221d789f-b4d8-4773-9219-7097f6c3b3eb] received
[2026-03-29 06:35:49,013: INFO/MainProcess] Task tasks.scrape_pending_urls[221d789f-b4d8-4773-9219-7097f6c3b3eb] succeeded in 0.0035738000879064202s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,014: INFO/MainProcess] Task tasks.scrape_pending_urls[6b0f96c2-c26e-4710-8f74-f4013fe01a29] received
[2026-03-29 06:35:49,018: INFO/MainProcess] Task tasks.scrape_pending_urls[6b0f96c2-c26e-4710-8f74-f4013fe01a29] succeeded in 0.003182200016453862s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,019: INFO/MainProcess] Task tasks.scrape_pending_urls[ee95810a-12a1-44d9-bdaf-e51dc1dba0eb] received
[2026-03-29 06:35:49,022: INFO/MainProcess] Task tasks.scrape_pending_urls[ee95810a-12a1-44d9-bdaf-e51dc1dba0eb] succeeded in 0.0023849999997764826s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,023: INFO/MainProcess] Task tasks.scrape_pending_urls[d3102848-0dee-4e10-9e16-fc9acb363107] received
[2026-03-29 06:35:49,026: INFO/MainProcess] Task tasks.scrape_pending_urls[d3102848-0dee-4e10-9e16-fc9acb363107] succeeded in 0.002181899966672063s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,027: INFO/MainProcess] Task tasks.scrape_pending_urls[d6e034c7-d28d-4b6f-a9a6-10e9bb94312d] received
[2026-03-29 06:35:49,029: INFO/MainProcess] Task tasks.scrape_pending_urls[d6e034c7-d28d-4b6f-a9a6-10e9bb94312d] succeeded in 0.002140600001439452s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,031: INFO/MainProcess] Task tasks.scrape_pending_urls[ac596422-1246-4d4c-90ff-d959c5db3b5a] received
[2026-03-29 06:35:49,033: INFO/MainProcess] Task tasks.scrape_pending_urls[ac596422-1246-4d4c-90ff-d959c5db3b5a] succeeded in 0.002560799941420555s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,036: INFO/MainProcess] Task tasks.scrape_pending_urls[3f6debcc-0cbb-4cf5-bea6-aade92237544] received
[2026-03-29 06:35:49,039: INFO/MainProcess] Task tasks.scrape_pending_urls[3f6debcc-0cbb-4cf5-bea6-aade92237544] succeeded in 0.002398999989964068s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,040: INFO/MainProcess] Task tasks.scrape_pending_urls[1b264b58-872b-4e19-9d01-36dd399b42da] received
[2026-03-29 06:35:49,043: INFO/MainProcess] Task tasks.scrape_pending_urls[1b264b58-872b-4e19-9d01-36dd399b42da] succeeded in 0.002091799979098141s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,044: INFO/MainProcess] Task tasks.scrape_pending_urls[737e5bfe-fb00-4f6c-bd59-417b6cdf64e9] received
[2026-03-29 06:35:49,046: INFO/MainProcess] Task tasks.scrape_pending_urls[737e5bfe-fb00-4f6c-bd59-417b6cdf64e9] succeeded in 0.002064000000245869s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,048: INFO/MainProcess] Task tasks.scrape_pending_urls[fa1cd286-d4ea-445d-95c5-47dccf224b19] received
[2026-03-29 06:35:49,051: INFO/MainProcess] Task tasks.scrape_pending_urls[fa1cd286-d4ea-445d-95c5-47dccf224b19] succeeded in 0.003154700039885938s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,052: INFO/MainProcess] Task tasks.scrape_pending_urls[3be62e78-7dcf-4dc5-8484-d9db1976207f] received
[2026-03-29 06:35:49,055: INFO/MainProcess] Task tasks.scrape_pending_urls[3be62e78-7dcf-4dc5-8484-d9db1976207f] succeeded in 0.0022648999001830816s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,056: INFO/MainProcess] Task tasks.scrape_pending_urls[b93a72bd-9ce3-4bbc-8374-d35e21387d29] received
[2026-03-29 06:35:49,058: INFO/MainProcess] Task tasks.scrape_pending_urls[b93a72bd-9ce3-4bbc-8374-d35e21387d29] succeeded in 0.00217779993545264s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,060: INFO/MainProcess] Task tasks.scrape_pending_urls[16f2447b-e89c-45ec-a614-c87b3ecf5ab3] received
[2026-03-29 06:35:49,062: INFO/MainProcess] Task tasks.scrape_pending_urls[16f2447b-e89c-45ec-a614-c87b3ecf5ab3] succeeded in 0.002168099978007376s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,063: INFO/MainProcess] Task tasks.scrape_pending_urls[f201c52a-d515-42ec-aea4-db9b98b2c930] received
[2026-03-29 06:35:49,067: INFO/MainProcess] Task tasks.scrape_pending_urls[f201c52a-d515-42ec-aea4-db9b98b2c930] succeeded in 0.0035023000091314316s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,070: INFO/MainProcess] Task tasks.scrape_pending_urls[3aacf712-8e64-4811-b686-fbb049763442] received
[2026-03-29 06:35:49,072: INFO/MainProcess] Task tasks.scrape_pending_urls[3aacf712-8e64-4811-b686-fbb049763442] succeeded in 0.0021667000837624073s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,073: INFO/MainProcess] Task tasks.scrape_pending_urls[51042cc5-8bb6-49e4-b93d-6468b956101e] received
[2026-03-29 06:35:49,076: INFO/MainProcess] Task tasks.scrape_pending_urls[51042cc5-8bb6-49e4-b93d-6468b956101e] succeeded in 0.0020255999406799674s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,077: INFO/MainProcess] Task tasks.scrape_pending_urls[4fef9894-3669-454a-95ff-7f319c3b29b5] received
[2026-03-29 06:35:49,079: INFO/MainProcess] Task tasks.scrape_pending_urls[4fef9894-3669-454a-95ff-7f319c3b29b5] succeeded in 0.0019835999701172113s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,080: INFO/MainProcess] Task tasks.scrape_pending_urls[dc0ea813-3be3-4fec-95b5-a89f7f92b723] received
[2026-03-29 06:35:49,083: INFO/MainProcess] Task tasks.scrape_pending_urls[dc0ea813-3be3-4fec-95b5-a89f7f92b723] succeeded in 0.002446400001645088s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,085: INFO/MainProcess] Task tasks.scrape_pending_urls[8c6fef82-ead0-4f78-8612-b075899ae19e] received
[2026-03-29 06:35:49,087: INFO/MainProcess] Task tasks.scrape_pending_urls[8c6fef82-ead0-4f78-8612-b075899ae19e] succeeded in 0.002012799959629774s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,088: INFO/MainProcess] Task tasks.scrape_pending_urls[7a1644c2-80fc-4834-b35e-0d1bac070553] received
[2026-03-29 06:35:49,090: INFO/MainProcess] Task tasks.scrape_pending_urls[7a1644c2-80fc-4834-b35e-0d1bac070553] succeeded in 0.001974300015717745s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,092: INFO/MainProcess] Task tasks.scrape_pending_urls[5876de97-5e97-496b-9dbe-86d12b786b59] received
[2026-03-29 06:35:49,094: INFO/MainProcess] Task tasks.scrape_pending_urls[5876de97-5e97-496b-9dbe-86d12b786b59] succeeded in 0.001964899944141507s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,095: INFO/MainProcess] Task tasks.scrape_pending_urls[60885c67-1bc6-48a0-b706-f83743e6ea98] received
[2026-03-29 06:35:49,099: INFO/MainProcess] Task tasks.scrape_pending_urls[60885c67-1bc6-48a0-b706-f83743e6ea98] succeeded in 0.0036828999873250723s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,101: INFO/MainProcess] Task tasks.scrape_pending_urls[340b690d-22ab-4f84-b531-9726e28affc5] received
[2026-03-29 06:35:49,103: INFO/MainProcess] Task tasks.scrape_pending_urls[340b690d-22ab-4f84-b531-9726e28affc5] succeeded in 0.0024414999643340707s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,105: INFO/MainProcess] Task tasks.scrape_pending_urls[61f5977e-4910-452b-b9bb-c6fbee1a6c8a] received
[2026-03-29 06:35:49,107: INFO/MainProcess] Task tasks.scrape_pending_urls[61f5977e-4910-452b-b9bb-c6fbee1a6c8a] succeeded in 0.0020308999810367823s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,108: INFO/MainProcess] Task tasks.scrape_pending_urls[e6384b60-ca24-4a77-9541-e17ef25e871f] received
[2026-03-29 06:35:49,111: INFO/MainProcess] Task tasks.scrape_pending_urls[e6384b60-ca24-4a77-9541-e17ef25e871f] succeeded in 0.002028799965046346s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,112: INFO/MainProcess] Task tasks.scrape_pending_urls[550b909b-ddc9-4ea9-a392-8f874a04927f] received
[2026-03-29 06:35:49,115: INFO/MainProcess] Task tasks.scrape_pending_urls[550b909b-ddc9-4ea9-a392-8f874a04927f] succeeded in 0.0027864999137818813s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,116: INFO/MainProcess] Task tasks.scrape_pending_urls[6681a45a-4b9f-4bf5-a056-79605dc70eb8] received
[2026-03-29 06:35:49,119: INFO/MainProcess] Task tasks.scrape_pending_urls[6681a45a-4b9f-4bf5-a056-79605dc70eb8] succeeded in 0.002023999928496778s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,120: INFO/MainProcess] Task tasks.scrape_pending_urls[f396427d-830c-42e7-bd85-af4ad62ad56b] received
[2026-03-29 06:35:49,122: INFO/MainProcess] Task tasks.scrape_pending_urls[f396427d-830c-42e7-bd85-af4ad62ad56b] succeeded in 0.002042099949903786s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,123: INFO/MainProcess] Task tasks.scrape_pending_urls[f85fd7d1-b1d5-4079-8b63-c5b502bb427c] received
[2026-03-29 06:35:49,126: INFO/MainProcess] Task tasks.scrape_pending_urls[f85fd7d1-b1d5-4079-8b63-c5b502bb427c] succeeded in 0.001963100046850741s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,127: INFO/MainProcess] Task tasks.scrape_pending_urls[f88e7a59-0861-4b3d-aefb-eaf22a18ddf0] received
[2026-03-29 06:35:49,131: INFO/MainProcess] Task tasks.scrape_pending_urls[f88e7a59-0861-4b3d-aefb-eaf22a18ddf0] succeeded in 0.0039793000323697925s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,133: INFO/MainProcess] Task tasks.scrape_pending_urls[fc94588b-c16d-4109-83ae-8f2d92557fe4] received
[2026-03-29 06:35:49,135: INFO/MainProcess] Task tasks.scrape_pending_urls[fc94588b-c16d-4109-83ae-8f2d92557fe4] succeeded in 0.002155099995434284s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,136: INFO/MainProcess] Task tasks.scrape_pending_urls[bc9520bb-5c7e-4cc5-9ad8-cff3078cf93f] received
[2026-03-29 06:35:49,139: INFO/MainProcess] Task tasks.scrape_pending_urls[bc9520bb-5c7e-4cc5-9ad8-cff3078cf93f] succeeded in 0.002029599971137941s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,140: INFO/MainProcess] Task tasks.scrape_pending_urls[a6896fa6-4cc2-40c7-be50-c159b4926798] received
[2026-03-29 06:35:49,142: INFO/MainProcess] Task tasks.scrape_pending_urls[a6896fa6-4cc2-40c7-be50-c159b4926798] succeeded in 0.002031099982559681s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,143: INFO/MainProcess] Task tasks.scrape_pending_urls[eae9e204-c489-4a81-9d9b-ab7cb5ebae14] received
[2026-03-29 06:35:49,148: INFO/MainProcess] Task tasks.scrape_pending_urls[eae9e204-c489-4a81-9d9b-ab7cb5ebae14] succeeded in 0.0038958999793976545s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,149: INFO/MainProcess] Task tasks.scrape_pending_urls[5aae6cdb-28bb-49e8-b1e1-9866eeec82c0] received
[2026-03-29 06:35:49,151: INFO/MainProcess] Task tasks.scrape_pending_urls[5aae6cdb-28bb-49e8-b1e1-9866eeec82c0] succeeded in 0.0022603999823331833s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,153: INFO/MainProcess] Task tasks.scrape_pending_urls[23db42dc-3698-44ee-8685-ea26259b8a82] received
[2026-03-29 06:35:49,155: INFO/MainProcess] Task tasks.scrape_pending_urls[23db42dc-3698-44ee-8685-ea26259b8a82] succeeded in 0.002203500014729798s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,156: INFO/MainProcess] Task tasks.scrape_pending_urls[dce2c2a6-faf4-4b9b-87e4-34a10233ab88] received
[2026-03-29 06:35:49,159: INFO/MainProcess] Task tasks.scrape_pending_urls[dce2c2a6-faf4-4b9b-87e4-34a10233ab88] succeeded in 0.0021725998958572745s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,160: INFO/MainProcess] Task tasks.scrape_pending_urls[d5765bbb-94fd-4a88-ae4e-e4f055b31148] received
[2026-03-29 06:35:49,164: INFO/MainProcess] Task tasks.scrape_pending_urls[d5765bbb-94fd-4a88-ae4e-e4f055b31148] succeeded in 0.0029713999247178435s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,166: INFO/MainProcess] Task tasks.scrape_pending_urls[a16f50c7-f6c2-400b-a357-94a8d42a30de] received
[2026-03-29 06:35:49,168: INFO/MainProcess] Task tasks.scrape_pending_urls[a16f50c7-f6c2-400b-a357-94a8d42a30de] succeeded in 0.002059000078588724s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,169: INFO/MainProcess] Task tasks.scrape_pending_urls[7cef6385-6c64-47c0-bb36-f2ed94554792] received
[2026-03-29 06:35:49,171: INFO/MainProcess] Task tasks.scrape_pending_urls[7cef6385-6c64-47c0-bb36-f2ed94554792] succeeded in 0.001999799977056682s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,173: INFO/MainProcess] Task tasks.scrape_pending_urls[40819e24-986a-415e-b932-ee21dd86362a] received
[2026-03-29 06:35:49,175: INFO/MainProcess] Task tasks.scrape_pending_urls[40819e24-986a-415e-b932-ee21dd86362a] succeeded in 0.0019890000112354755s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,177: INFO/MainProcess] Task tasks.scrape_pending_urls[bfb7c2ce-9c58-43bb-b5cf-5f8c5f09e3ae] received
[2026-03-29 06:35:49,180: INFO/MainProcess] Task tasks.scrape_pending_urls[bfb7c2ce-9c58-43bb-b5cf-5f8c5f09e3ae] succeeded in 0.0023120000259950757s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,181: INFO/MainProcess] Task tasks.scrape_pending_urls[572a31e6-d290-47be-8f5b-e3c2443c99e8] received
[2026-03-29 06:35:49,184: INFO/MainProcess] Task tasks.scrape_pending_urls[572a31e6-d290-47be-8f5b-e3c2443c99e8] succeeded in 0.0024193000281229615s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,185: INFO/MainProcess] Task tasks.scrape_pending_urls[53537e83-9ee4-41d5-8a05-f8c34d2ebb23] received
[2026-03-29 06:35:49,188: INFO/MainProcess] Task tasks.scrape_pending_urls[53537e83-9ee4-41d5-8a05-f8c34d2ebb23] succeeded in 0.0022122999653220177s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,189: INFO/MainProcess] Task tasks.scrape_pending_urls[14e55239-afdd-4e53-9873-24ebc1e26ddf] received
[2026-03-29 06:35:49,191: INFO/MainProcess] Task tasks.scrape_pending_urls[14e55239-afdd-4e53-9873-24ebc1e26ddf] succeeded in 0.0021840999834239483s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,193: INFO/MainProcess] Task tasks.scrape_pending_urls[02f17079-b197-46bb-adf2-f7cf4d573a4b] received
[2026-03-29 06:35:49,198: INFO/MainProcess] Task tasks.scrape_pending_urls[02f17079-b197-46bb-adf2-f7cf4d573a4b] succeeded in 0.0025499999755993485s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,199: INFO/MainProcess] Task tasks.scrape_pending_urls[29ea7f4d-24a6-4c42-aef3-c90c5b9e6a47] received
[2026-03-29 06:35:49,201: INFO/MainProcess] Task tasks.scrape_pending_urls[29ea7f4d-24a6-4c42-aef3-c90c5b9e6a47] succeeded in 0.0022507000248879194s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,203: INFO/MainProcess] Task tasks.scrape_pending_urls[92356c8f-dc34-4273-896c-86ebb880ee41] received
[2026-03-29 06:35:49,205: INFO/MainProcess] Task tasks.scrape_pending_urls[92356c8f-dc34-4273-896c-86ebb880ee41] succeeded in 0.002230800106190145s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,206: INFO/MainProcess] Task tasks.scrape_pending_urls[59478baf-eb45-429c-b87b-eb6fff8ff1ac] received
[2026-03-29 06:35:49,209: INFO/MainProcess] Task tasks.scrape_pending_urls[59478baf-eb45-429c-b87b-eb6fff8ff1ac] succeeded in 0.002883399953134358s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,211: INFO/MainProcess] Task tasks.scrape_pending_urls[e6c333d6-81e4-4531-aec4-1777f88f109a] received
[2026-03-29 06:35:49,213: INFO/MainProcess] Task tasks.scrape_pending_urls[e6c333d6-81e4-4531-aec4-1777f88f109a] succeeded in 0.0021443000296130776s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,214: INFO/MainProcess] Task tasks.scrape_pending_urls[898006bf-6ec5-4cd1-bcbb-ef088ec051ce] received
[2026-03-29 06:35:49,217: INFO/MainProcess] Task tasks.scrape_pending_urls[898006bf-6ec5-4cd1-bcbb-ef088ec051ce] succeeded in 0.0020512999035418034s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,218: INFO/MainProcess] Task tasks.scrape_pending_urls[9b320031-1c97-4399-a649-36f64089bf85] received
[2026-03-29 06:35:49,220: INFO/MainProcess] Task tasks.scrape_pending_urls[9b320031-1c97-4399-a649-36f64089bf85] succeeded in 0.0019972999580204487s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,221: INFO/MainProcess] Task tasks.scrape_pending_urls[5995344f-7722-4ba1-a6e2-063b3260713c] received
[2026-03-29 06:35:49,224: INFO/MainProcess] Task tasks.scrape_pending_urls[5995344f-7722-4ba1-a6e2-063b3260713c] succeeded in 0.0021045999601483345s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,227: INFO/MainProcess] Task tasks.scrape_pending_urls[8eb821a6-63cd-4d64-a299-8cf080111db2] received
[2026-03-29 06:35:49,230: INFO/MainProcess] Task tasks.scrape_pending_urls[8eb821a6-63cd-4d64-a299-8cf080111db2] succeeded in 0.0023222999880090356s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,231: INFO/MainProcess] Task tasks.scrape_pending_urls[b8f66aad-608f-4993-9eb7-2f6d15b1e4e0] received
[2026-03-29 06:35:49,233: INFO/MainProcess] Task tasks.scrape_pending_urls[b8f66aad-608f-4993-9eb7-2f6d15b1e4e0] succeeded in 0.0020478999940678477s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,235: INFO/MainProcess] Task tasks.scrape_pending_urls[dcd805b5-199c-4754-a27d-b7f67dadeb5f] received
[2026-03-29 06:35:49,237: INFO/MainProcess] Task tasks.scrape_pending_urls[dcd805b5-199c-4754-a27d-b7f67dadeb5f] succeeded in 0.002043199958279729s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,238: INFO/MainProcess] Task tasks.scrape_pending_urls[2976afac-0a38-4de8-986b-dec4fd46d5bb] received
[2026-03-29 06:35:49,241: INFO/MainProcess] Task tasks.scrape_pending_urls[2976afac-0a38-4de8-986b-dec4fd46d5bb] succeeded in 0.0024962000316008925s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,242: INFO/MainProcess] Task tasks.scrape_pending_urls[ca7da60d-8a2b-453c-9a8e-a9cf793f7546] received
[2026-03-29 06:35:49,245: INFO/MainProcess] Task tasks.scrape_pending_urls[ca7da60d-8a2b-453c-9a8e-a9cf793f7546] succeeded in 0.002127000014297664s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:49,246: INFO/MainProcess] Task tasks.scrape_pending_urls[563c3a2d-aec8-4bf6-ab05-d9f5dc45b547] received
[2026-03-29 06:35:49,248: INFO/MainProcess] Task tasks.scrape_pending_urls[563c3a2d-aec8-4bf6-ab05-d9f5dc45b547] succeeded in 0.001993000041693449s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:35:56,789: INFO/MainProcess] Task tasks.scrape_pending_urls[99ee6836-4d37-4b35-ac19-53600b83c357] received
[2026-03-29 06:35:56,793: INFO/MainProcess] Task tasks.scrape_pending_urls[99ee6836-4d37-4b35-ac19-53600b83c357] succeeded in 0.003020299947820604s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:36:26,790: INFO/MainProcess] Task tasks.scrape_pending_urls[8f29dcf5-3da5-4b19-91d6-a2ba7686b22c] received
[2026-03-29 06:36:26,793: INFO/MainProcess] Task tasks.scrape_pending_urls[8f29dcf5-3da5-4b19-91d6-a2ba7686b22c] succeeded in 0.002692999900318682s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:36:56,790: INFO/MainProcess] Task tasks.scrape_pending_urls[347e29dc-fd9e-425f-805a-a72802bee6df] received
[2026-03-29 06:36:56,793: INFO/MainProcess] Task tasks.scrape_pending_urls[347e29dc-fd9e-425f-805a-a72802bee6df] succeeded in 0.0027706000255420804s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:37:26,790: INFO/MainProcess] Task tasks.scrape_pending_urls[beaa28f4-abd7-45ba-952c-fdf0e9ac8c82] received
[2026-03-29 06:37:26,793: INFO/MainProcess] Task tasks.scrape_pending_urls[beaa28f4-abd7-45ba-952c-fdf0e9ac8c82] succeeded in 0.002542699920013547s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:37:56,790: INFO/MainProcess] Task tasks.scrape_pending_urls[5ecfd5bc-c41f-4df4-97f9-d9c6d79a7024] received
[2026-03-29 06:37:56,793: INFO/MainProcess] Task tasks.scrape_pending_urls[5ecfd5bc-c41f-4df4-97f9-d9c6d79a7024] succeeded in 0.002648000023327768s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:38:26,790: INFO/MainProcess] Task tasks.scrape_pending_urls[c2816909-274e-44c4-9dd6-c8a325697f91] received
[2026-03-29 06:38:26,793: INFO/MainProcess] Task tasks.scrape_pending_urls[c2816909-274e-44c4-9dd6-c8a325697f91] succeeded in 0.002857400104403496s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:38:56,648: INFO/MainProcess] Task tasks.collect_system_metrics[2c6c69fa-8209-4d1d-a09e-114966833698] received
[2026-03-29 06:38:57,165: INFO/MainProcess] Task tasks.collect_system_metrics[2c6c69fa-8209-4d1d-a09e-114966833698] succeeded in 0.5165600000182167s: {'cpu': 14.2, 'memory': 45.3}
[2026-03-29 06:38:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[c38b10d5-1768-4df2-9d8e-de57a67be532] received
[2026-03-29 06:38:57,170: INFO/MainProcess] Task tasks.scrape_pending_urls[c38b10d5-1768-4df2-9d8e-de57a67be532] succeeded in 0.002764199976809323s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:39:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[87a0076f-ec5b-4b99-90c7-97de246dc1d6] received
[2026-03-29 06:39:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[87a0076f-ec5b-4b99-90c7-97de246dc1d6] succeeded in 0.0027077000122517347s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:39:56,794: INFO/MainProcess] Task tasks.scrape_pending_urls[eab9a7f0-72d6-41ca-a5b8-cd542a764140] received
[2026-03-29 06:39:56,797: INFO/MainProcess] Task tasks.scrape_pending_urls[eab9a7f0-72d6-41ca-a5b8-cd542a764140] succeeded in 0.002553700003772974s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:40:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[42dad865-e1c3-4149-ad9c-6ae6d76ade00] received
[2026-03-29 06:40:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[42dad865-e1c3-4149-ad9c-6ae6d76ade00] succeeded in 0.0025840000016614795s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:40:56,794: INFO/MainProcess] Task tasks.scrape_pending_urls[3baf763b-2f02-4831-80ac-bd4f894022cd] received
[2026-03-29 06:40:56,797: INFO/MainProcess] Task tasks.scrape_pending_urls[3baf763b-2f02-4831-80ac-bd4f894022cd] succeeded in 0.0025690000038594007s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:41:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[8b0b69b1-0e3c-487b-a2d7-d86f523d57e4] received
[2026-03-29 06:41:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[8b0b69b1-0e3c-487b-a2d7-d86f523d57e4] succeeded in 0.0027631999691948295s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:41:56,794: INFO/MainProcess] Task tasks.scrape_pending_urls[80df3deb-8016-4466-a132-458d4da04fd7] received
[2026-03-29 06:41:56,797: INFO/MainProcess] Task tasks.scrape_pending_urls[80df3deb-8016-4466-a132-458d4da04fd7] succeeded in 0.002546900068409741s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:42:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[7968d051-6aa8-42d2-9033-e2c3332bbf77] received
[2026-03-29 06:42:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[7968d051-6aa8-42d2-9033-e2c3332bbf77] succeeded in 0.002731099957600236s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:42:56,794: INFO/MainProcess] Task tasks.scrape_pending_urls[bf05586b-d4f9-4c01-97d0-b879ad28819b] received
[2026-03-29 06:42:56,797: INFO/MainProcess] Task tasks.scrape_pending_urls[bf05586b-d4f9-4c01-97d0-b879ad28819b] succeeded in 0.0028734999941661954s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:43:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[c01d35d4-5ba2-4bab-aee2-bae238f35352] received
[2026-03-29 06:43:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[c01d35d4-5ba2-4bab-aee2-bae238f35352] succeeded in 0.002689399989321828s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:43:56,638: INFO/MainProcess] Task tasks.reset_stale_processing_urls[dce5a0c2-8e44-4a6f-843d-8b12e439efc7] received
[2026-03-29 06:43:56,641: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 06:43:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[dce5a0c2-8e44-4a6f-843d-8b12e439efc7] succeeded in 0.0038531000027433038s: {'reset': 0}
[2026-03-29 06:43:56,648: INFO/MainProcess] Task tasks.collect_system_metrics[3d26ee9c-d126-4464-90cd-ac17b30f1d77] received
[2026-03-29 06:43:57,163: INFO/MainProcess] Task tasks.collect_system_metrics[3d26ee9c-d126-4464-90cd-ac17b30f1d77] succeeded in 0.5154337000567466s: {'cpu': 15.2, 'memory': 45.1}
[2026-03-29 06:43:57,165: INFO/MainProcess] Task tasks.scrape_pending_urls[a164d092-aa83-4c90-95a6-7c36da6910e1] received
[2026-03-29 06:43:57,168: INFO/MainProcess] Task tasks.scrape_pending_urls[a164d092-aa83-4c90-95a6-7c36da6910e1] succeeded in 0.002225200063548982s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:44:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[2b244392-00a9-45fc-994c-2233e3de15bd] received
[2026-03-29 06:44:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[2b244392-00a9-45fc-994c-2233e3de15bd] succeeded in 0.0026603000005707145s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:44:56,794: INFO/MainProcess] Task tasks.scrape_pending_urls[b5eb4fa5-a42f-4591-b244-98c463c486b8] received
[2026-03-29 06:44:56,797: INFO/MainProcess] Task tasks.scrape_pending_urls[b5eb4fa5-a42f-4591-b244-98c463c486b8] succeeded in 0.0027002000715583563s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:45:26,794: INFO/MainProcess] Task tasks.scrape_pending_urls[5e194e41-1ae7-45a8-b19e-9551483fbfaf] received
[2026-03-29 06:45:26,797: INFO/MainProcess] Task tasks.scrape_pending_urls[5e194e41-1ae7-45a8-b19e-9551483fbfaf] succeeded in 0.0026189000345766544s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:45:56,799: INFO/MainProcess] Task tasks.scrape_pending_urls[3e5b4f81-2bf9-4df0-a72e-894de25222fe] received
[2026-03-29 06:45:56,802: INFO/MainProcess] Task tasks.scrape_pending_urls[3e5b4f81-2bf9-4df0-a72e-894de25222fe] succeeded in 0.0026221000589430332s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:46:26,799: INFO/MainProcess] Task tasks.scrape_pending_urls[1efa30f2-0237-402e-9954-78b18c57c61d] received
[2026-03-29 06:46:26,802: INFO/MainProcess] Task tasks.scrape_pending_urls[1efa30f2-0237-402e-9954-78b18c57c61d] succeeded in 0.002745700068771839s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:46:56,799: INFO/MainProcess] Task tasks.scrape_pending_urls[5ddbf0eb-2359-4897-ad38-31f11a7d168b] received
[2026-03-29 06:46:56,802: INFO/MainProcess] Task tasks.scrape_pending_urls[5ddbf0eb-2359-4897-ad38-31f11a7d168b] succeeded in 0.002692099893465638s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:47:26,799: INFO/MainProcess] Task tasks.scrape_pending_urls[a14754c2-fdf3-467c-9906-a71010fd31ff] received
[2026-03-29 06:47:26,802: INFO/MainProcess] Task tasks.scrape_pending_urls[a14754c2-fdf3-467c-9906-a71010fd31ff] succeeded in 0.0035920999944210052s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:47:56,799: INFO/MainProcess] Task tasks.scrape_pending_urls[50d72c65-2872-467b-bec8-6cb77ac4db46] received
[2026-03-29 06:47:56,802: INFO/MainProcess] Task tasks.scrape_pending_urls[50d72c65-2872-467b-bec8-6cb77ac4db46] succeeded in 0.0026488000294193625s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:48:26,799: INFO/MainProcess] Task tasks.scrape_pending_urls[60c28418-8ca6-450f-9439-0a52891e3a14] received
[2026-03-29 06:48:26,802: INFO/MainProcess] Task tasks.scrape_pending_urls[60c28418-8ca6-450f-9439-0a52891e3a14] succeeded in 0.0030427000019699335s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:48:56,648: INFO/MainProcess] Task tasks.collect_system_metrics[17c5af82-9c6b-4c80-b0af-37b4813dd15b] received
[2026-03-29 06:48:57,164: INFO/MainProcess] Task tasks.collect_system_metrics[17c5af82-9c6b-4c80-b0af-37b4813dd15b] succeeded in 0.5157374999253079s: {'cpu': 18.8, 'memory': 45.3}
[2026-03-29 06:48:57,166: INFO/MainProcess] Task tasks.scrape_pending_urls[7ed96ce8-62be-46b8-81e6-cba2d291c624] received
[2026-03-29 06:48:57,169: INFO/MainProcess] Task tasks.scrape_pending_urls[7ed96ce8-62be-46b8-81e6-cba2d291c624] succeeded in 0.0026694999542087317s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:49:26,799: INFO/MainProcess] Task tasks.scrape_pending_urls[791817cd-9d43-49ee-aabd-8a4deb624ec3] received
[2026-03-29 06:49:26,802: INFO/MainProcess] Task tasks.scrape_pending_urls[791817cd-9d43-49ee-aabd-8a4deb624ec3] succeeded in 0.0025149000575765967s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:49:56,799: INFO/MainProcess] Task tasks.scrape_pending_urls[c43d71e7-c5fd-47ff-ac0b-11d228044fd6] received
[2026-03-29 06:49:56,802: INFO/MainProcess] Task tasks.scrape_pending_urls[c43d71e7-c5fd-47ff-ac0b-11d228044fd6] succeeded in 0.0027648000977933407s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:50:26,799: INFO/MainProcess] Task tasks.scrape_pending_urls[c8d46551-1171-4e92-afd7-ed222a5e4323] received
[2026-03-29 06:50:26,802: INFO/MainProcess] Task tasks.scrape_pending_urls[c8d46551-1171-4e92-afd7-ed222a5e4323] succeeded in 0.002825799980200827s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:50:56,800: INFO/MainProcess] Task tasks.scrape_pending_urls[07130f4f-5f04-40e1-b487-ad39e4105809] received
[2026-03-29 06:50:56,861: INFO/MainProcess] Task tasks.scrape_pending_urls[07130f4f-5f04-40e1-b487-ad39e4105809] succeeded in 0.061038700048811734s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:51:26,799: INFO/MainProcess] Task tasks.scrape_pending_urls[7967516c-825c-4814-a17c-648fe2843b75] received
[2026-03-29 06:51:26,861: INFO/MainProcess] Task tasks.scrape_pending_urls[7967516c-825c-4814-a17c-648fe2843b75] succeeded in 0.06160349992569536s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:51:56,799: INFO/MainProcess] Task tasks.scrape_pending_urls[876e3cd0-3c20-4d6b-9e7f-9cb1c2c35b10] received
[2026-03-29 06:51:56,802: INFO/MainProcess] Task tasks.scrape_pending_urls[876e3cd0-3c20-4d6b-9e7f-9cb1c2c35b10] succeeded in 0.002656400087289512s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:52:26,803: INFO/MainProcess] Task tasks.scrape_pending_urls[a82a4a95-6b08-4e66-a8b4-7528ee28839f] received
[2026-03-29 06:52:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[a82a4a95-6b08-4e66-a8b4-7528ee28839f] succeeded in 0.0028241000836715102s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:52:56,803: INFO/MainProcess] Task tasks.scrape_pending_urls[e08defcb-3b7c-4fe6-9e09-1c69b06f474d] received
[2026-03-29 06:52:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[e08defcb-3b7c-4fe6-9e09-1c69b06f474d] succeeded in 0.0027016999665647745s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:53:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[cfbb2828-f357-4991-bb87-cf877b1dc175] received
[2026-03-29 06:53:26,808: INFO/MainProcess] Task tasks.scrape_pending_urls[cfbb2828-f357-4991-bb87-cf877b1dc175] succeeded in 0.002924300031736493s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:53:56,649: INFO/MainProcess] Task tasks.collect_system_metrics[dbe9a489-34a1-4ce3-a225-eea3139320d3] received
[2026-03-29 06:53:57,168: INFO/MainProcess] Task tasks.collect_system_metrics[dbe9a489-34a1-4ce3-a225-eea3139320d3] succeeded in 0.5185846999520436s: {'cpu': 10.4, 'memory': 45.1}
[2026-03-29 06:53:57,170: INFO/MainProcess] Task tasks.scrape_pending_urls[7e713309-18c6-44ac-89e6-f847aeca5607] received
[2026-03-29 06:53:57,173: INFO/MainProcess] Task tasks.scrape_pending_urls[7e713309-18c6-44ac-89e6-f847aeca5607] succeeded in 0.0028735999949276447s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:54:26,803: INFO/MainProcess] Task tasks.scrape_pending_urls[f0edacb1-8b6e-4722-b88d-475f6b1ab338] received
[2026-03-29 06:54:26,806: INFO/MainProcess] Task tasks.scrape_pending_urls[f0edacb1-8b6e-4722-b88d-475f6b1ab338] succeeded in 0.0025067999958992004s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:54:56,803: INFO/MainProcess] Task tasks.scrape_pending_urls[78688270-8eec-4f0f-9479-6dad26c3a475] received
[2026-03-29 06:54:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[78688270-8eec-4f0f-9479-6dad26c3a475] succeeded in 0.002816900028847158s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:55:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[52e7be32-6fa2-4473-bdf3-6b6c6adf35f7] received
[2026-03-29 06:55:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[52e7be32-6fa2-4473-bdf3-6b6c6adf35f7] succeeded in 0.0031127999536693096s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:55:56,804: INFO/MainProcess] Task tasks.scrape_pending_urls[e679d1ff-680c-46d2-bf8d-4178ddd327dd] received
[2026-03-29 06:55:56,870: INFO/MainProcess] Task tasks.scrape_pending_urls[e679d1ff-680c-46d2-bf8d-4178ddd327dd] succeeded in 0.06586480000987649s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:56:26,803: INFO/MainProcess] Task tasks.scrape_pending_urls[ebf2f897-8ebe-4b9e-a358-9799208699fb] received
[2026-03-29 06:56:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[ebf2f897-8ebe-4b9e-a358-9799208699fb] succeeded in 0.0027472999645397067s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:56:56,804: INFO/MainProcess] Task tasks.scrape_pending_urls[331df668-ecd4-4d0a-be0c-774d1015c182] received
[2026-03-29 06:56:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[331df668-ecd4-4d0a-be0c-774d1015c182] succeeded in 0.0030629999237135053s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:57:26,803: INFO/MainProcess] Task tasks.scrape_pending_urls[2d1c1737-50d1-418a-ae48-3a017a819c05] received
[2026-03-29 06:57:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[2d1c1737-50d1-418a-ae48-3a017a819c05] succeeded in 0.002951500006020069s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:57:56,804: INFO/MainProcess] Task tasks.scrape_pending_urls[bcd8d714-15bc-40e9-91db-6c0bfd201f3c] received
[2026-03-29 06:57:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[bcd8d714-15bc-40e9-91db-6c0bfd201f3c] succeeded in 0.0025961999781429768s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:58:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[c3e8ec45-0179-4b8f-af69-e26b0d93e627] received
[2026-03-29 06:58:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[c3e8ec45-0179-4b8f-af69-e26b0d93e627] succeeded in 0.0027974999975413084s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:58:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[8234c22a-c2e5-412d-bce0-b2b2c33e5205] received
[2026-03-29 06:58:57,172: INFO/MainProcess] Task tasks.collect_system_metrics[8234c22a-c2e5-412d-bce0-b2b2c33e5205] succeeded in 0.5188086000271142s: {'cpu': 12.1, 'memory': 45.1}
[2026-03-29 06:58:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[9ee62d88-2727-4e47-86b0-709adab8d546] received
[2026-03-29 06:58:57,177: INFO/MainProcess] Task tasks.scrape_pending_urls[9ee62d88-2727-4e47-86b0-709adab8d546] succeeded in 0.002750700106844306s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:59:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[18371155-d082-4d1f-a2a5-8ad70448646f] received
[2026-03-29 06:59:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[18371155-d082-4d1f-a2a5-8ad70448646f] succeeded in 0.0027924999594688416s: {'status': 'idle', 'pending': 0}
[2026-03-29 06:59:56,804: INFO/MainProcess] Task tasks.scrape_pending_urls[56c81f30-ff06-407e-8ec3-a0308b8d9882] received
[2026-03-29 06:59:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[56c81f30-ff06-407e-8ec3-a0308b8d9882] succeeded in 0.00275859993416816s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:00:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[af2f3c8a-c674-43f8-bfdd-87aa63fca6f6] received
[2026-03-29 07:00:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[af2f3c8a-c674-43f8-bfdd-87aa63fca6f6] succeeded in 0.0027626999653875828s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:00:56,804: INFO/MainProcess] Task tasks.scrape_pending_urls[1d8613bc-9833-48e8-ab90-4827b7969151] received
[2026-03-29 07:00:56,808: INFO/MainProcess] Task tasks.scrape_pending_urls[1d8613bc-9833-48e8-ab90-4827b7969151] succeeded in 0.003320800024084747s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:01:26,804: INFO/MainProcess] Task tasks.scrape_pending_urls[212c17e4-5d4f-40c4-a0db-c0a5667bc7f7] received
[2026-03-29 07:01:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[212c17e4-5d4f-40c4-a0db-c0a5667bc7f7] succeeded in 0.002961799968034029s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:01:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[a6679fce-d582-4e82-9d54-b60ca7833978] received
[2026-03-29 07:01:56,810: INFO/MainProcess] Task tasks.scrape_pending_urls[a6679fce-d582-4e82-9d54-b60ca7833978] succeeded in 0.0027420000405982137s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:02:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[303b85e8-09b4-4dd3-b235-8807ba6dcc81] received
[2026-03-29 07:02:26,811: INFO/MainProcess] Task tasks.scrape_pending_urls[303b85e8-09b4-4dd3-b235-8807ba6dcc81] succeeded in 0.0028974999440833926s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:02:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[28daf6f4-9a74-4631-97aa-bbed5fc68cd4] received
[2026-03-29 07:02:56,810: INFO/MainProcess] Task tasks.scrape_pending_urls[28daf6f4-9a74-4631-97aa-bbed5fc68cd4] succeeded in 0.0026138999965041876s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:03:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[c220389d-8a24-4671-b1c5-7319ff978664] received
[2026-03-29 07:03:26,810: INFO/MainProcess] Task tasks.scrape_pending_urls[c220389d-8a24-4671-b1c5-7319ff978664] succeeded in 0.002588600036688149s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:03:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[4ba09b74-8da1-4600-8d4f-817fd40899f8] received
[2026-03-29 07:03:57,173: INFO/MainProcess] Task tasks.collect_system_metrics[4ba09b74-8da1-4600-8d4f-817fd40899f8] succeeded in 0.5189265999943018s: {'cpu': 13.5, 'memory': 45.1}
[2026-03-29 07:03:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[c8c5b405-b1df-4098-b611-fe955884352d] received
[2026-03-29 07:03:57,178: INFO/MainProcess] Task tasks.scrape_pending_urls[c8c5b405-b1df-4098-b611-fe955884352d] succeeded in 0.0033022999996319413s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:04:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[047de140-6e9f-48e2-8c08-5b4667f94303] received
[2026-03-29 07:04:26,811: INFO/MainProcess] Task tasks.scrape_pending_urls[047de140-6e9f-48e2-8c08-5b4667f94303] succeeded in 0.0038524999981746078s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:04:56,808: INFO/MainProcess] Task tasks.scrape_pending_urls[78d2fe3a-09e1-4924-abb0-c6d6e1a341db] received
[2026-03-29 07:04:56,812: INFO/MainProcess] Task tasks.scrape_pending_urls[78d2fe3a-09e1-4924-abb0-c6d6e1a341db] succeeded in 0.0032023999374359846s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:05:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[47e5a188-35f5-4db6-a5f2-3ba9c6ae6c5d] received
[2026-03-29 07:05:26,811: INFO/MainProcess] Task tasks.scrape_pending_urls[47e5a188-35f5-4db6-a5f2-3ba9c6ae6c5d] succeeded in 0.002765699988231063s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:05:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[ba6301e6-6b72-4284-ab75-3d74557fe414] received
[2026-03-29 07:05:56,810: INFO/MainProcess] Task tasks.scrape_pending_urls[ba6301e6-6b72-4284-ab75-3d74557fe414] succeeded in 0.0026412000879645348s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:06:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[1597b1c0-c83e-4f5a-98e9-de23809240ea] received
[2026-03-29 07:06:26,810: INFO/MainProcess] Task tasks.scrape_pending_urls[1597b1c0-c83e-4f5a-98e9-de23809240ea] succeeded in 0.002525499905459583s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:06:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[40f0141c-5d7a-4f0b-9e27-41807688e3c8] received
[2026-03-29 07:06:56,810: INFO/MainProcess] Task tasks.scrape_pending_urls[40f0141c-5d7a-4f0b-9e27-41807688e3c8] succeeded in 0.0026117999805137515s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:07:26,807: INFO/MainProcess] Task tasks.scrape_pending_urls[6e747874-8663-4885-a22e-bda6c2f00758] received
[2026-03-29 07:07:26,810: INFO/MainProcess] Task tasks.scrape_pending_urls[6e747874-8663-4885-a22e-bda6c2f00758] succeeded in 0.0026703999610617757s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:07:56,807: INFO/MainProcess] Task tasks.scrape_pending_urls[c1852504-171d-40dd-ab28-1d866803401b] received
[2026-03-29 07:07:56,810: INFO/MainProcess] Task tasks.scrape_pending_urls[c1852504-171d-40dd-ab28-1d866803401b] succeeded in 0.002677900018170476s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:08:26,813: INFO/MainProcess] Task tasks.scrape_pending_urls[06ce942d-a96c-4768-93b1-57e3308250c4] received
[2026-03-29 07:08:26,816: INFO/MainProcess] Task tasks.scrape_pending_urls[06ce942d-a96c-4768-93b1-57e3308250c4] succeeded in 0.002766599995084107s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:08:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[22d6081d-b151-4029-85e5-b6e48db1ea45] received
[2026-03-29 07:08:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[22d6081d-b151-4029-85e5-b6e48db1ea45] succeeded in 0.5161286999937147s: {'cpu': 9.4, 'memory': 45.2}
[2026-03-29 07:08:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[a9fb6bfd-b31d-4dc3-81cf-3d2570ccae80] received
[2026-03-29 07:08:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[a9fb6bfd-b31d-4dc3-81cf-3d2570ccae80] succeeded in 0.0027222000062465668s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:09:26,812: INFO/MainProcess] Task tasks.scrape_pending_urls[6317af90-aadf-431c-b426-e3fae1f8b4b1] received
[2026-03-29 07:09:26,816: INFO/MainProcess] Task tasks.scrape_pending_urls[6317af90-aadf-431c-b426-e3fae1f8b4b1] succeeded in 0.003013300010934472s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:09:56,812: INFO/MainProcess] Task tasks.scrape_pending_urls[d8689617-2526-4ebb-acb7-3aeb2f71ca51] received
[2026-03-29 07:09:56,816: INFO/MainProcess] Task tasks.scrape_pending_urls[d8689617-2526-4ebb-acb7-3aeb2f71ca51] succeeded in 0.0029903999529778957s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:10:26,812: INFO/MainProcess] Task tasks.scrape_pending_urls[ffa2b928-fd82-4b18-9ab6-d3cbc8a67673] received
[2026-03-29 07:10:26,815: INFO/MainProcess] Task tasks.scrape_pending_urls[ffa2b928-fd82-4b18-9ab6-d3cbc8a67673] succeeded in 0.002481000032275915s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:10:56,812: INFO/MainProcess] Task tasks.scrape_pending_urls[5d790f32-048a-4510-a1bc-d89b8d753f14] received
[2026-03-29 07:10:56,815: INFO/MainProcess] Task tasks.scrape_pending_urls[5d790f32-048a-4510-a1bc-d89b8d753f14] succeeded in 0.002616899902932346s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:11:26,812: INFO/MainProcess] Task tasks.scrape_pending_urls[66022b88-11c2-4aa4-a027-af840645b04c] received
[2026-03-29 07:11:26,816: INFO/MainProcess] Task tasks.scrape_pending_urls[66022b88-11c2-4aa4-a027-af840645b04c] succeeded in 0.0026943000266328454s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:11:56,813: INFO/MainProcess] Task tasks.scrape_pending_urls[fcb7ec75-2bbc-497c-8693-d45ce9fccc56] received
[2026-03-29 07:11:56,816: INFO/MainProcess] Task tasks.scrape_pending_urls[fcb7ec75-2bbc-497c-8693-d45ce9fccc56] succeeded in 0.002540700021199882s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:12:26,813: INFO/MainProcess] Task tasks.scrape_pending_urls[0a57e576-84a0-423f-8053-12a140533d74] received
[2026-03-29 07:12:26,816: INFO/MainProcess] Task tasks.scrape_pending_urls[0a57e576-84a0-423f-8053-12a140533d74] succeeded in 0.002660500002093613s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:12:56,813: INFO/MainProcess] Task tasks.scrape_pending_urls[d273e308-19e9-4f07-a855-1ecdd17d0915] received
[2026-03-29 07:12:56,816: INFO/MainProcess] Task tasks.scrape_pending_urls[d273e308-19e9-4f07-a855-1ecdd17d0915] succeeded in 0.002644499996677041s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:13:26,813: INFO/MainProcess] Task tasks.scrape_pending_urls[fd060bda-0b79-4dd8-afd0-ceb75d6683df] received
[2026-03-29 07:13:26,816: INFO/MainProcess] Task tasks.scrape_pending_urls[fd060bda-0b79-4dd8-afd0-ceb75d6683df] succeeded in 0.0026386999525129795s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:13:56,638: INFO/MainProcess] Task tasks.reset_stale_processing_urls[55f18e85-b7dd-4511-880e-ef90572e73c0] received
[2026-03-29 07:13:56,641: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 07:13:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[55f18e85-b7dd-4511-880e-ef90572e73c0] succeeded in 0.003632600069977343s: {'reset': 0}
[2026-03-29 07:13:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[646c424b-ae00-41a9-859a-37f8acc7075d] received
[2026-03-29 07:13:57,169: INFO/MainProcess] Task tasks.collect_system_metrics[646c424b-ae00-41a9-859a-37f8acc7075d] succeeded in 0.5156871000071988s: {'cpu': 10.2, 'memory': 45.5}
[2026-03-29 07:13:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[39ffc986-2aa5-45d9-a930-1e04ed7a6438] received
[2026-03-29 07:13:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[39ffc986-2aa5-45d9-a930-1e04ed7a6438] succeeded in 0.0026437999913468957s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:14:26,813: INFO/MainProcess] Task tasks.scrape_pending_urls[5a1a9e0d-9b93-475e-9582-50e04999d042] received
[2026-03-29 07:14:26,816: INFO/MainProcess] Task tasks.scrape_pending_urls[5a1a9e0d-9b93-475e-9582-50e04999d042] succeeded in 0.002642699982970953s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:14:56,817: INFO/MainProcess] Task tasks.scrape_pending_urls[6e4e8535-29b2-4598-a730-ff3933e1370f] received
[2026-03-29 07:14:56,820: INFO/MainProcess] Task tasks.scrape_pending_urls[6e4e8535-29b2-4598-a730-ff3933e1370f] succeeded in 0.0026506000431254506s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:15:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[51d236e9-4092-4f8d-b6bc-c4d53a35de4c] received
[2026-03-29 07:15:26,820: INFO/MainProcess] Task tasks.scrape_pending_urls[51d236e9-4092-4f8d-b6bc-c4d53a35de4c] succeeded in 0.002648100024089217s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:15:56,817: INFO/MainProcess] Task tasks.scrape_pending_urls[05a8bec8-4095-49a0-9409-afc45fa40132] received
[2026-03-29 07:15:56,820: INFO/MainProcess] Task tasks.scrape_pending_urls[05a8bec8-4095-49a0-9409-afc45fa40132] succeeded in 0.0026279999874532223s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:16:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[01e988da-080f-4e40-b339-ac9fc63d0836] received
[2026-03-29 07:16:26,821: INFO/MainProcess] Task tasks.scrape_pending_urls[01e988da-080f-4e40-b339-ac9fc63d0836] succeeded in 0.0029716999270021915s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:16:56,817: INFO/MainProcess] Task tasks.scrape_pending_urls[453aa6a3-4255-4f6c-90ce-e0538ca4696f] received
[2026-03-29 07:16:56,820: INFO/MainProcess] Task tasks.scrape_pending_urls[453aa6a3-4255-4f6c-90ce-e0538ca4696f] succeeded in 0.0028117999900132418s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:17:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[1e93f1a0-32d8-4fb8-b5d0-33652b8ea5a0] received
[2026-03-29 07:17:26,820: INFO/MainProcess] Task tasks.scrape_pending_urls[1e93f1a0-32d8-4fb8-b5d0-33652b8ea5a0] succeeded in 0.002864800044335425s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:17:56,817: INFO/MainProcess] Task tasks.scrape_pending_urls[10f21397-9044-4896-b8e3-c2588678e934] received
[2026-03-29 07:17:56,821: INFO/MainProcess] Task tasks.scrape_pending_urls[10f21397-9044-4896-b8e3-c2588678e934] succeeded in 0.0028452000115066767s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:18:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[c657d7b5-1296-4c1c-8207-11db9d30543b] received
[2026-03-29 07:18:26,820: INFO/MainProcess] Task tasks.scrape_pending_urls[c657d7b5-1296-4c1c-8207-11db9d30543b] succeeded in 0.002475599991157651s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:18:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[6ee41b2a-101a-46ff-a9bb-c614ce3e2807] received
[2026-03-29 07:18:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[6ee41b2a-101a-46ff-a9bb-c614ce3e2807] succeeded in 0.5168163999915123s: {'cpu': 10.4, 'memory': 45.3}
[2026-03-29 07:18:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[b114465c-fbc8-4bc3-ac1b-abe77157779c] received
[2026-03-29 07:18:57,176: INFO/MainProcess] Task tasks.scrape_pending_urls[b114465c-fbc8-4bc3-ac1b-abe77157779c] succeeded in 0.002990800072439015s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:19:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[d33d33df-0691-4f58-84fb-a8f4f6d6c0ea] received
[2026-03-29 07:19:26,820: INFO/MainProcess] Task tasks.scrape_pending_urls[d33d33df-0691-4f58-84fb-a8f4f6d6c0ea] succeeded in 0.0026843000669032335s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:19:56,817: INFO/MainProcess] Task tasks.scrape_pending_urls[a2b23df6-1240-444b-ad69-55d699c86379] received
[2026-03-29 07:19:56,821: INFO/MainProcess] Task tasks.scrape_pending_urls[a2b23df6-1240-444b-ad69-55d699c86379] succeeded in 0.0031956000020727515s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:20:26,817: INFO/MainProcess] Task tasks.scrape_pending_urls[2f5887f5-2ec8-4ebe-b79d-dc07a3af16e1] received
[2026-03-29 07:20:26,821: INFO/MainProcess] Task tasks.scrape_pending_urls[2f5887f5-2ec8-4ebe-b79d-dc07a3af16e1] succeeded in 0.00283440004568547s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:20:56,817: INFO/MainProcess] Task tasks.scrape_pending_urls[8eced2cc-e223-4c49-823b-572337d1f7a1] received
[2026-03-29 07:20:56,821: INFO/MainProcess] Task tasks.scrape_pending_urls[8eced2cc-e223-4c49-823b-572337d1f7a1] succeeded in 0.002840499975718558s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:21:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[98e04d2e-b03d-4c57-aacd-577e409faf6d] received
[2026-03-29 07:21:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[98e04d2e-b03d-4c57-aacd-577e409faf6d] succeeded in 0.002641799976117909s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:21:56,822: INFO/MainProcess] Task tasks.scrape_pending_urls[2c529b82-09e8-4d0a-85a2-cd1e55abec99] received
[2026-03-29 07:21:56,825: INFO/MainProcess] Task tasks.scrape_pending_urls[2c529b82-09e8-4d0a-85a2-cd1e55abec99] succeeded in 0.0026329999091103673s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:22:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[015eb9ff-1eba-4d8e-b152-6c3bc08048e0] received
[2026-03-29 07:22:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[015eb9ff-1eba-4d8e-b152-6c3bc08048e0] succeeded in 0.002660099999047816s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:22:56,822: INFO/MainProcess] Task tasks.scrape_pending_urls[439faf1c-f8a6-4b65-8f9c-592ea5fe89f3] received
[2026-03-29 07:22:56,825: INFO/MainProcess] Task tasks.scrape_pending_urls[439faf1c-f8a6-4b65-8f9c-592ea5fe89f3] succeeded in 0.0024901999859139323s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:23:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[81912dde-e968-41fb-b6b5-675ed9916d17] received
[2026-03-29 07:23:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[81912dde-e968-41fb-b6b5-675ed9916d17] succeeded in 0.002888699993491173s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:23:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[8968f760-a65d-4604-a830-328faa9b39e3] received
[2026-03-29 07:23:57,169: INFO/MainProcess] Task tasks.collect_system_metrics[8968f760-a65d-4604-a830-328faa9b39e3] succeeded in 0.5158828999847174s: {'cpu': 14.8, 'memory': 45.2}
[2026-03-29 07:23:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[5322ed52-2414-4a6f-a8da-48c644e47124] received
[2026-03-29 07:23:57,179: INFO/MainProcess] Task tasks.scrape_pending_urls[5322ed52-2414-4a6f-a8da-48c644e47124] succeeded in 0.006452100002206862s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:24:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[e335f980-9384-49a3-b3cc-a0490be1e987] received
[2026-03-29 07:24:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[e335f980-9384-49a3-b3cc-a0490be1e987] succeeded in 0.0026744999922811985s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:24:56,822: INFO/MainProcess] Task tasks.scrape_pending_urls[1d8e8eff-6f04-4646-89bc-e7ceada6eee7] received
[2026-03-29 07:24:56,825: INFO/MainProcess] Task tasks.scrape_pending_urls[1d8e8eff-6f04-4646-89bc-e7ceada6eee7] succeeded in 0.0027254000306129456s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:25:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[04b17afd-cdb3-4390-9ed0-182d0b823666] received
[2026-03-29 07:25:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[04b17afd-cdb3-4390-9ed0-182d0b823666] succeeded in 0.00276459997985512s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:25:56,822: INFO/MainProcess] Task tasks.scrape_pending_urls[fe6fafe1-1796-406a-8308-09628019ee3e] received
[2026-03-29 07:25:56,825: INFO/MainProcess] Task tasks.scrape_pending_urls[fe6fafe1-1796-406a-8308-09628019ee3e] succeeded in 0.0028084999648854136s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:26:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[75660d8f-2189-4e74-871f-a9058322e1f5] received
[2026-03-29 07:26:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[75660d8f-2189-4e74-871f-a9058322e1f5] succeeded in 0.002511599916033447s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:26:56,822: INFO/MainProcess] Task tasks.scrape_pending_urls[967a3a12-f02b-42bb-b93e-34a4e9dcbc6c] received
[2026-03-29 07:26:56,825: INFO/MainProcess] Task tasks.scrape_pending_urls[967a3a12-f02b-42bb-b93e-34a4e9dcbc6c] succeeded in 0.0026763000059872866s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:27:26,822: INFO/MainProcess] Task tasks.scrape_pending_urls[51df8e6a-0ed3-4779-92c9-560c8af0d5b1] received
[2026-03-29 07:27:26,825: INFO/MainProcess] Task tasks.scrape_pending_urls[51df8e6a-0ed3-4779-92c9-560c8af0d5b1] succeeded in 0.002636200049892068s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:27:56,827: INFO/MainProcess] Task tasks.scrape_pending_urls[7850ca40-9161-4731-b95c-0f61758711b6] received
[2026-03-29 07:27:56,830: INFO/MainProcess] Task tasks.scrape_pending_urls[7850ca40-9161-4731-b95c-0f61758711b6] succeeded in 0.0031484999926760793s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:28:26,827: INFO/MainProcess] Task tasks.scrape_pending_urls[acf8c7c5-ec8c-4b29-8dd5-2f9d6075ee3d] received
[2026-03-29 07:28:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[acf8c7c5-ec8c-4b29-8dd5-2f9d6075ee3d] succeeded in 0.002688600099645555s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:28:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[d95e2cf7-c3d1-4603-97bd-8e052509a87b] received
[2026-03-29 07:28:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[d95e2cf7-c3d1-4603-97bd-8e052509a87b] succeeded in 0.5163408999796957s: {'cpu': 13.7, 'memory': 45.4}
[2026-03-29 07:28:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[eea63f3c-e014-4408-aed1-744b6d6689ce] received
[2026-03-29 07:28:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[eea63f3c-e014-4408-aed1-744b6d6689ce] succeeded in 0.0029338999884203076s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:29:26,827: INFO/MainProcess] Task tasks.scrape_pending_urls[3c7edc48-f783-4833-a4d0-35729c312479] received
[2026-03-29 07:29:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[3c7edc48-f783-4833-a4d0-35729c312479] succeeded in 0.0027959999861195683s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:29:56,827: INFO/MainProcess] Task tasks.scrape_pending_urls[fff55d09-b765-497d-baf5-4e0d7c3335a6] received
[2026-03-29 07:29:56,830: INFO/MainProcess] Task tasks.scrape_pending_urls[fff55d09-b765-497d-baf5-4e0d7c3335a6] succeeded in 0.002499000052921474s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:30:00,001: INFO/MainProcess] Task tasks.purge_old_debug_html[9fbc0d49-2d7e-4582-9cc7-4c06e5ff577d] received
[2026-03-29 07:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[9fbc0d49-2d7e-4582-9cc7-4c06e5ff577d] succeeded in 0.0014785999665036798s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 07:30:26,827: INFO/MainProcess] Task tasks.scrape_pending_urls[0cca5d11-7178-423b-a384-98e9e3b890f1] received
[2026-03-29 07:30:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[0cca5d11-7178-423b-a384-98e9e3b890f1] succeeded in 0.0026710000820457935s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:30:56,827: INFO/MainProcess] Task tasks.scrape_pending_urls[c033ab6d-1290-4845-9924-a3adbf7b1b2e] received
[2026-03-29 07:30:56,831: INFO/MainProcess] Task tasks.scrape_pending_urls[c033ab6d-1290-4845-9924-a3adbf7b1b2e] succeeded in 0.0033227000385522842s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:31:26,827: INFO/MainProcess] Task tasks.scrape_pending_urls[345b5e56-0b8c-4122-acf5-dd640ab70c72] received
[2026-03-29 07:31:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[345b5e56-0b8c-4122-acf5-dd640ab70c72] succeeded in 0.002559899934567511s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:31:56,827: INFO/MainProcess] Task tasks.scrape_pending_urls[ec6036a5-93b4-421d-8cee-c98149aadc1c] received
[2026-03-29 07:31:56,830: INFO/MainProcess] Task tasks.scrape_pending_urls[ec6036a5-93b4-421d-8cee-c98149aadc1c] succeeded in 0.0025095000164583325s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:32:26,827: INFO/MainProcess] Task tasks.scrape_pending_urls[bc3be232-8139-42f6-a534-ddaa5f4f729d] received
[2026-03-29 07:32:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[bc3be232-8139-42f6-a534-ddaa5f4f729d] succeeded in 0.003083999967202544s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:32:56,827: INFO/MainProcess] Task tasks.scrape_pending_urls[ecc4e67b-b2e4-4326-8a0c-b1a0d9d1c2d5] received
[2026-03-29 07:32:56,830: INFO/MainProcess] Task tasks.scrape_pending_urls[ecc4e67b-b2e4-4326-8a0c-b1a0d9d1c2d5] succeeded in 0.002910100040026009s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:33:26,827: INFO/MainProcess] Task tasks.scrape_pending_urls[2c4538e6-2b7b-4904-b3da-b9f5a95e0521] received
[2026-03-29 07:33:26,830: INFO/MainProcess] Task tasks.scrape_pending_urls[2c4538e6-2b7b-4904-b3da-b9f5a95e0521] succeeded in 0.0028829999500885606s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:33:56,654: INFO/MainProcess] Task tasks.collect_system_metrics[8031a5d8-5e18-48ea-9233-e9f2eb38b01e] received
[2026-03-29 07:33:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[8031a5d8-5e18-48ea-9233-e9f2eb38b01e] succeeded in 0.5158464999403805s: {'cpu': 14.0, 'memory': 45.4}
[2026-03-29 07:33:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[14b08b03-e410-40dc-84ef-219376111573] received
[2026-03-29 07:33:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[14b08b03-e410-40dc-84ef-219376111573] succeeded in 0.0026930999010801315s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:34:26,832: INFO/MainProcess] Task tasks.scrape_pending_urls[458f1618-00ab-4618-8b69-07756eaa2207] received
[2026-03-29 07:34:26,835: INFO/MainProcess] Task tasks.scrape_pending_urls[458f1618-00ab-4618-8b69-07756eaa2207] succeeded in 0.002643899992108345s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:34:56,831: INFO/MainProcess] Task tasks.scrape_pending_urls[dbf9bbc9-8e4c-4eb1-856d-53e5d5875ef3] received
[2026-03-29 07:34:56,834: INFO/MainProcess] Task tasks.scrape_pending_urls[dbf9bbc9-8e4c-4eb1-856d-53e5d5875ef3] succeeded in 0.0026813000440597534s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:35:26,831: INFO/MainProcess] Task tasks.scrape_pending_urls[c40babc7-1ab5-46fd-8585-ecfc8cda7e61] received
[2026-03-29 07:35:26,834: INFO/MainProcess] Task tasks.scrape_pending_urls[c40babc7-1ab5-46fd-8585-ecfc8cda7e61] succeeded in 0.002641799976117909s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:35:56,831: INFO/MainProcess] Task tasks.scrape_pending_urls[77143005-8821-46bd-8621-46ea68b747dc] received
[2026-03-29 07:35:56,834: INFO/MainProcess] Task tasks.scrape_pending_urls[77143005-8821-46bd-8621-46ea68b747dc] succeeded in 0.0026664999313652515s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:36:26,831: INFO/MainProcess] Task tasks.scrape_pending_urls[a99068fa-f299-403b-8761-ffebf5aade08] received
[2026-03-29 07:36:26,835: INFO/MainProcess] Task tasks.scrape_pending_urls[a99068fa-f299-403b-8761-ffebf5aade08] succeeded in 0.0026551999617367983s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:36:56,832: INFO/MainProcess] Task tasks.scrape_pending_urls[21414f57-d25e-4a7e-97f5-b6d828036255] received
[2026-03-29 07:36:56,835: INFO/MainProcess] Task tasks.scrape_pending_urls[21414f57-d25e-4a7e-97f5-b6d828036255] succeeded in 0.00270239997189492s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:37:26,831: INFO/MainProcess] Task tasks.scrape_pending_urls[2146bf0b-347d-4935-bd01-eb1e386d6862] received
[2026-03-29 07:37:26,835: INFO/MainProcess] Task tasks.scrape_pending_urls[2146bf0b-347d-4935-bd01-eb1e386d6862] succeeded in 0.0027612000703811646s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:37:56,831: INFO/MainProcess] Task tasks.scrape_pending_urls[2967cac0-ba16-473d-a98a-d7b300a8acb1] received
[2026-03-29 07:37:56,834: INFO/MainProcess] Task tasks.scrape_pending_urls[2967cac0-ba16-473d-a98a-d7b300a8acb1] succeeded in 0.0027554999105632305s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:38:26,831: INFO/MainProcess] Task tasks.scrape_pending_urls[f40cb08b-9dc3-4144-adee-b1b77f15d266] received
[2026-03-29 07:38:26,834: INFO/MainProcess] Task tasks.scrape_pending_urls[f40cb08b-9dc3-4144-adee-b1b77f15d266] succeeded in 0.002633200027048588s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:38:56,653: INFO/MainProcess] Task tasks.collect_system_metrics[2d23fdb7-8f60-4c3d-b190-57b4ce7428fa] received
[2026-03-29 07:38:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[2d23fdb7-8f60-4c3d-b190-57b4ce7428fa] succeeded in 0.5160446000518277s: {'cpu': 17.1, 'memory': 45.2}
[2026-03-29 07:38:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[ae9e9f83-e804-405f-ab94-587f7c417fb3] received
[2026-03-29 07:38:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[ae9e9f83-e804-405f-ab94-587f7c417fb3] succeeded in 0.0025776999536901712s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:39:26,832: INFO/MainProcess] Task tasks.scrape_pending_urls[a79a23ed-0bcf-4061-a9a0-97ce96d4df0e] received
[2026-03-29 07:39:26,835: INFO/MainProcess] Task tasks.scrape_pending_urls[a79a23ed-0bcf-4061-a9a0-97ce96d4df0e] succeeded in 0.0026386999525129795s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:39:56,832: INFO/MainProcess] Task tasks.scrape_pending_urls[a5561f91-33aa-442c-a392-60c74d6b5e66] received
[2026-03-29 07:39:56,835: INFO/MainProcess] Task tasks.scrape_pending_urls[a5561f91-33aa-442c-a392-60c74d6b5e66] succeeded in 0.0029425000539049506s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:40:26,832: INFO/MainProcess] Task tasks.scrape_pending_urls[694dfb20-76cf-43ae-865e-2ac8452c7d8b] received
[2026-03-29 07:40:26,835: INFO/MainProcess] Task tasks.scrape_pending_urls[694dfb20-76cf-43ae-865e-2ac8452c7d8b] succeeded in 0.0026456000050529838s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:40:56,836: INFO/MainProcess] Task tasks.scrape_pending_urls[a95f81b9-84a8-4759-8ef8-4cb78be0595a] received
[2026-03-29 07:40:56,839: INFO/MainProcess] Task tasks.scrape_pending_urls[a95f81b9-84a8-4759-8ef8-4cb78be0595a] succeeded in 0.0027127000503242016s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:41:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[38b97f86-9b10-4dd8-b7fc-c1981e8d4eb0] received
[2026-03-29 07:41:26,839: INFO/MainProcess] Task tasks.scrape_pending_urls[38b97f86-9b10-4dd8-b7fc-c1981e8d4eb0] succeeded in 0.0027057999977841973s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:41:56,836: INFO/MainProcess] Task tasks.scrape_pending_urls[8dd4dfe5-0ec0-4932-a90f-291214db14fb] received
[2026-03-29 07:41:56,839: INFO/MainProcess] Task tasks.scrape_pending_urls[8dd4dfe5-0ec0-4932-a90f-291214db14fb] succeeded in 0.0026512000476941466s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:42:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[0475ec8f-a7a5-49a6-bde6-5435259a5d0d] received
[2026-03-29 07:42:26,839: INFO/MainProcess] Task tasks.scrape_pending_urls[0475ec8f-a7a5-49a6-bde6-5435259a5d0d] succeeded in 0.0027061000000685453s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:42:56,836: INFO/MainProcess] Task tasks.scrape_pending_urls[8f3ba7fa-c65d-47c6-9e51-5852860ac8ba] received
[2026-03-29 07:42:56,839: INFO/MainProcess] Task tasks.scrape_pending_urls[8f3ba7fa-c65d-47c6-9e51-5852860ac8ba] succeeded in 0.0027744999388232827s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:43:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[bc8ad636-847f-4366-9634-de98e4f49e8c] received
[2026-03-29 07:43:26,839: INFO/MainProcess] Task tasks.scrape_pending_urls[bc8ad636-847f-4366-9634-de98e4f49e8c] succeeded in 0.002671999973244965s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:43:56,638: INFO/MainProcess] Task tasks.reset_stale_processing_urls[04c116be-bd94-4588-90d4-95b3133aa725] received
[2026-03-29 07:43:56,640: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 07:43:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[04c116be-bd94-4588-90d4-95b3133aa725] succeeded in 0.003591699991375208s: {'reset': 0}
[2026-03-29 07:43:56,760: INFO/MainProcess] Task tasks.collect_system_metrics[387befd6-6d36-4b8a-92ce-5e3c09b82d88] received
[2026-03-29 07:43:57,277: INFO/MainProcess] Task tasks.collect_system_metrics[387befd6-6d36-4b8a-92ce-5e3c09b82d88] succeeded in 0.5162144999485463s: {'cpu': 18.0, 'memory': 45.3}
[2026-03-29 07:43:57,279: INFO/MainProcess] Task tasks.scrape_pending_urls[deed1cdf-b7a4-4de9-b30d-50bdb415e725] received
[2026-03-29 07:43:57,281: INFO/MainProcess] Task tasks.scrape_pending_urls[deed1cdf-b7a4-4de9-b30d-50bdb415e725] succeeded in 0.0022193000186234713s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:44:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[dae75a92-7443-4614-91a1-d807ab5acd9b] received
[2026-03-29 07:44:26,839: INFO/MainProcess] Task tasks.scrape_pending_urls[dae75a92-7443-4614-91a1-d807ab5acd9b] succeeded in 0.002634100033901632s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:44:56,836: INFO/MainProcess] Task tasks.scrape_pending_urls[118445f1-7d87-4731-8d66-9bbf267de133] received
[2026-03-29 07:44:56,839: INFO/MainProcess] Task tasks.scrape_pending_urls[118445f1-7d87-4731-8d66-9bbf267de133] succeeded in 0.0027286000549793243s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:45:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[e0b2219c-2ca1-4823-8264-c3af58876db6] received
[2026-03-29 07:45:26,839: INFO/MainProcess] Task tasks.scrape_pending_urls[e0b2219c-2ca1-4823-8264-c3af58876db6] succeeded in 0.0027061000000685453s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:45:56,836: INFO/MainProcess] Task tasks.scrape_pending_urls[e98df19e-37fc-4148-bbd3-2e46be57cc25] received
[2026-03-29 07:45:56,839: INFO/MainProcess] Task tasks.scrape_pending_urls[e98df19e-37fc-4148-bbd3-2e46be57cc25] succeeded in 0.002499899943359196s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:46:26,836: INFO/MainProcess] Task tasks.scrape_pending_urls[35330081-3ded-476e-8892-4f73287ca9c9] received
[2026-03-29 07:46:26,839: INFO/MainProcess] Task tasks.scrape_pending_urls[35330081-3ded-476e-8892-4f73287ca9c9] succeeded in 0.002537399996072054s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:46:56,836: INFO/MainProcess] Task tasks.scrape_pending_urls[6dd14ffe-709b-4c22-9d82-a9c590bf7529] received
[2026-03-29 07:46:56,839: INFO/MainProcess] Task tasks.scrape_pending_urls[6dd14ffe-709b-4c22-9d82-a9c590bf7529] succeeded in 0.002745400066487491s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:47:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[567985f8-d122-4473-b6f6-6da5bf4933e4] received
[2026-03-29 07:47:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[567985f8-d122-4473-b6f6-6da5bf4933e4] succeeded in 0.0028400999726727605s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:47:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[fa0021bf-fc41-4a01-9bfb-e2966cee73c5] received
[2026-03-29 07:47:56,843: INFO/MainProcess] Task tasks.scrape_pending_urls[fa0021bf-fc41-4a01-9bfb-e2966cee73c5] succeeded in 0.002606600057333708s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:48:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[ac878252-a7c0-4ee7-a552-a3cc9ef46451] received
[2026-03-29 07:48:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[ac878252-a7c0-4ee7-a552-a3cc9ef46451] succeeded in 0.0027287000557407737s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:48:56,654: INFO/MainProcess] Task tasks.collect_system_metrics[fdc22ca6-94bd-4a76-94c0-8af4c60bf78a] received
[2026-03-29 07:48:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[fdc22ca6-94bd-4a76-94c0-8af4c60bf78a] succeeded in 0.5159777000080794s: {'cpu': 13.7, 'memory': 45.5}
[2026-03-29 07:48:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[ae21abdb-c4ab-4cd2-8cc6-77f93aac216b] received
[2026-03-29 07:48:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[ae21abdb-c4ab-4cd2-8cc6-77f93aac216b] succeeded in 0.0026436999905854464s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:49:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[56f5c6de-c0f8-448a-a0a5-9a557593f2a4] received
[2026-03-29 07:49:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[56f5c6de-c0f8-448a-a0a5-9a557593f2a4] succeeded in 0.0026344999205321074s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:49:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[d8ab9db2-ae52-4ce5-ac1f-bbd71717e364] received
[2026-03-29 07:49:56,843: INFO/MainProcess] Task tasks.scrape_pending_urls[d8ab9db2-ae52-4ce5-ac1f-bbd71717e364] succeeded in 0.0029061000095680356s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:50:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[0a272ecf-3345-4f4f-9804-b78f959e660a] received
[2026-03-29 07:50:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[0a272ecf-3345-4f4f-9804-b78f959e660a] succeeded in 0.0027456999523565173s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:50:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[ae5f7450-a05d-4c48-98d8-e719bddfaee1] received
[2026-03-29 07:50:56,843: INFO/MainProcess] Task tasks.scrape_pending_urls[ae5f7450-a05d-4c48-98d8-e719bddfaee1] succeeded in 0.0026443999959155917s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:51:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[ea69beb4-5449-423f-9605-72a8c9e9feed] received
[2026-03-29 07:51:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[ea69beb4-5449-423f-9605-72a8c9e9feed] succeeded in 0.06359820009674877s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:51:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[ae19b272-4d39-47d6-9965-0812f6f4ba35] received
[2026-03-29 07:51:56,904: INFO/MainProcess] Task tasks.scrape_pending_urls[ae19b272-4d39-47d6-9965-0812f6f4ba35] succeeded in 0.06369650003034621s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:52:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[9dfb0e99-29f8-49eb-bf45-95ba4c3f439b] received
[2026-03-29 07:52:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[9dfb0e99-29f8-49eb-bf45-95ba4c3f439b] succeeded in 0.002669000066816807s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:52:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[0f1f192c-51c1-436e-aa09-c018bc339ef5] received
[2026-03-29 07:52:56,844: INFO/MainProcess] Task tasks.scrape_pending_urls[0f1f192c-51c1-436e-aa09-c018bc339ef5] succeeded in 0.0028771000215783715s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:53:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[3b251f91-9ffc-43a0-8b46-d55e9cb4f8c5] received
[2026-03-29 07:53:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[3b251f91-9ffc-43a0-8b46-d55e9cb4f8c5] succeeded in 0.002669299952685833s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:53:56,659: INFO/MainProcess] Task tasks.collect_system_metrics[8daf18bb-362f-4ec4-a5ca-f69d7256497a] received
[2026-03-29 07:53:57,175: INFO/MainProcess] Task tasks.collect_system_metrics[8daf18bb-362f-4ec4-a5ca-f69d7256497a] succeeded in 0.5160589000442997s: {'cpu': 10.6, 'memory': 45.3}
[2026-03-29 07:53:57,177: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d4ea7c-6f04-4962-a016-7ec1607a99f2] received
[2026-03-29 07:53:57,180: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d4ea7c-6f04-4962-a016-7ec1607a99f2] succeeded in 0.002933099982328713s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:54:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[cea5c0c9-2c0a-4148-b10c-2034c7bc6d37] received
[2026-03-29 07:54:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[cea5c0c9-2c0a-4148-b10c-2034c7bc6d37] succeeded in 0.002812199993059039s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:54:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[5f50a331-9816-4972-8dd3-ff69de33005d] received
[2026-03-29 07:54:56,843: INFO/MainProcess] Task tasks.scrape_pending_urls[5f50a331-9816-4972-8dd3-ff69de33005d] succeeded in 0.0027221000054851174s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:55:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[b65dc584-a6a0-49c4-a6e7-cc993b5dbd58] received
[2026-03-29 07:55:26,843: INFO/MainProcess] Task tasks.scrape_pending_urls[b65dc584-a6a0-49c4-a6e7-cc993b5dbd58] succeeded in 0.002836100058630109s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:55:56,840: INFO/MainProcess] Task tasks.scrape_pending_urls[c3e0e76b-6b94-4151-b656-49c94b9b81bc] received
[2026-03-29 07:55:56,844: INFO/MainProcess] Task tasks.scrape_pending_urls[c3e0e76b-6b94-4151-b656-49c94b9b81bc] succeeded in 0.0030051000649109483s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:56:26,840: INFO/MainProcess] Task tasks.scrape_pending_urls[467cfe18-210f-4aa4-8774-1bdd0d365f87] received
[2026-03-29 07:56:26,903: INFO/MainProcess] Task tasks.scrape_pending_urls[467cfe18-210f-4aa4-8774-1bdd0d365f87] succeeded in 0.062406099983491004s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:56:56,845: INFO/MainProcess] Task tasks.scrape_pending_urls[73d315e7-7063-45da-b707-a2ba6da5f794] received
[2026-03-29 07:56:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[73d315e7-7063-45da-b707-a2ba6da5f794] succeeded in 0.0032733000116422772s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:57:26,845: INFO/MainProcess] Task tasks.scrape_pending_urls[c561b590-4f2a-459b-8f7a-c843255af49c] received
[2026-03-29 07:57:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[c561b590-4f2a-459b-8f7a-c843255af49c] succeeded in 0.0033341998932883143s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:57:56,845: INFO/MainProcess] Task tasks.scrape_pending_urls[732883e4-53c3-4b20-93b8-be84c315ef47] received
[2026-03-29 07:57:56,848: INFO/MainProcess] Task tasks.scrape_pending_urls[732883e4-53c3-4b20-93b8-be84c315ef47] succeeded in 0.002861300017684698s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:58:26,845: INFO/MainProcess] Task tasks.scrape_pending_urls[1c3767a6-b60d-4834-9210-f6f17eaa2eaf] received
[2026-03-29 07:58:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[1c3767a6-b60d-4834-9210-f6f17eaa2eaf] succeeded in 0.0030886000022292137s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:58:56,659: INFO/MainProcess] Task tasks.collect_system_metrics[d0376bf1-9bb7-4c33-b6d1-c77b8148d1c3] received
[2026-03-29 07:58:57,178: INFO/MainProcess] Task tasks.collect_system_metrics[d0376bf1-9bb7-4c33-b6d1-c77b8148d1c3] succeeded in 0.5184756000526249s: {'cpu': 13.3, 'memory': 45.2}
[2026-03-29 07:58:57,179: INFO/MainProcess] Task tasks.scrape_pending_urls[8fa88284-eeca-4326-a88f-e09d3a02b126] received
[2026-03-29 07:58:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[8fa88284-eeca-4326-a88f-e09d3a02b126] succeeded in 0.002727000042796135s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:59:26,845: INFO/MainProcess] Task tasks.scrape_pending_urls[18cbec73-6d02-4e9e-b32f-c7cd52d59492] received
[2026-03-29 07:59:26,848: INFO/MainProcess] Task tasks.scrape_pending_urls[18cbec73-6d02-4e9e-b32f-c7cd52d59492] succeeded in 0.002659599995240569s: {'status': 'idle', 'pending': 0}
[2026-03-29 07:59:56,845: INFO/MainProcess] Task tasks.scrape_pending_urls[9cedf659-ab6a-4e2b-a124-c2d1c16c852e] received
[2026-03-29 07:59:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[9cedf659-ab6a-4e2b-a124-c2d1c16c852e] succeeded in 0.002900600084103644s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:00:26,845: INFO/MainProcess] Task tasks.scrape_pending_urls[f0e6faaa-c042-4eb8-a59d-a3759a2165c2] received
[2026-03-29 08:00:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[f0e6faaa-c042-4eb8-a59d-a3759a2165c2] succeeded in 0.0029681000160053372s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:00:56,845: INFO/MainProcess] Task tasks.scrape_pending_urls[ed5d029e-e9c2-4ab4-aa1e-cc5bd7f4b32a] received
[2026-03-29 08:00:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[ed5d029e-e9c2-4ab4-aa1e-cc5bd7f4b32a] succeeded in 0.003055900102481246s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:01:26,845: INFO/MainProcess] Task tasks.scrape_pending_urls[2374b9d3-a66a-4542-a771-e823b3da3ef2] received
[2026-03-29 08:01:26,848: INFO/MainProcess] Task tasks.scrape_pending_urls[2374b9d3-a66a-4542-a771-e823b3da3ef2] succeeded in 0.002610699972137809s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:01:56,846: INFO/MainProcess] Task tasks.scrape_pending_urls[ed262ee7-59b5-4f4e-9aa7-4aad7aa1f2d6] received
[2026-03-29 08:01:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[ed262ee7-59b5-4f4e-9aa7-4aad7aa1f2d6] succeeded in 0.0028851000824943185s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:02:26,845: INFO/MainProcess] Task tasks.scrape_pending_urls[c4af4373-e133-4932-b5ee-e84debb0a3f7] received
[2026-03-29 08:02:26,848: INFO/MainProcess] Task tasks.scrape_pending_urls[c4af4373-e133-4932-b5ee-e84debb0a3f7] succeeded in 0.0027073000092059374s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:02:56,845: INFO/MainProcess] Task tasks.scrape_pending_urls[b665ccdb-3eb9-4ea1-8626-dc8a674121ee] received
[2026-03-29 08:02:56,848: INFO/MainProcess] Task tasks.scrape_pending_urls[b665ccdb-3eb9-4ea1-8626-dc8a674121ee] succeeded in 0.0025869000237435102s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:03:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[277ca904-e52b-4ab9-8c84-f58c147edbe6] received
[2026-03-29 08:03:26,852: INFO/MainProcess] Task tasks.scrape_pending_urls[277ca904-e52b-4ab9-8c84-f58c147edbe6] succeeded in 0.002881999942474067s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:03:56,658: INFO/MainProcess] Task tasks.collect_system_metrics[8ea23254-def0-4596-a7a8-7c7374b828e1] received
[2026-03-29 08:03:57,173: INFO/MainProcess] Task tasks.collect_system_metrics[8ea23254-def0-4596-a7a8-7c7374b828e1] succeeded in 0.5141253999900073s: {'cpu': 17.0, 'memory': 45.3}
[2026-03-29 08:03:57,176: INFO/MainProcess] Task tasks.scrape_pending_urls[d409c187-c6e3-4c6c-95c2-5561975b3fb6] received
[2026-03-29 08:03:57,179: INFO/MainProcess] Task tasks.scrape_pending_urls[d409c187-c6e3-4c6c-95c2-5561975b3fb6] succeeded in 0.002695700037293136s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:04:26,850: INFO/MainProcess] Task tasks.scrape_pending_urls[fcb0ea0f-ebf1-41e1-8a53-c4b0a3729f39] received
[2026-03-29 08:04:26,853: INFO/MainProcess] Task tasks.scrape_pending_urls[fcb0ea0f-ebf1-41e1-8a53-c4b0a3729f39] succeeded in 0.0028107999823987484s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:04:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[be5d4359-7b25-402e-bb19-785a74a547fc] received
[2026-03-29 08:04:56,854: INFO/MainProcess] Task tasks.scrape_pending_urls[be5d4359-7b25-402e-bb19-785a74a547fc] succeeded in 0.004061899962835014s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:05:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[9cff8c03-3da9-4828-89f3-6735e40dcb22] received
[2026-03-29 08:05:26,853: INFO/MainProcess] Task tasks.scrape_pending_urls[9cff8c03-3da9-4828-89f3-6735e40dcb22] succeeded in 0.0032085999846458435s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:05:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[1e18b817-afa6-4d4f-8e37-b21b648057b6] received
[2026-03-29 08:05:56,853: INFO/MainProcess] Task tasks.scrape_pending_urls[1e18b817-afa6-4d4f-8e37-b21b648057b6] succeeded in 0.002865700051188469s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:06:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[78a91f76-5acb-4e28-ae69-f610268705cc] received
[2026-03-29 08:06:26,853: INFO/MainProcess] Task tasks.scrape_pending_urls[78a91f76-5acb-4e28-ae69-f610268705cc] succeeded in 0.0026923000114038587s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:06:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[4dd74bf7-dcfb-4eb2-b86c-3caccca239f1] received
[2026-03-29 08:06:56,852: INFO/MainProcess] Task tasks.scrape_pending_urls[4dd74bf7-dcfb-4eb2-b86c-3caccca239f1] succeeded in 0.002602399908937514s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:07:26,849: INFO/MainProcess] Task tasks.scrape_pending_urls[9134c13d-3173-491f-b346-a5cf7e7079b2] received
[2026-03-29 08:07:26,852: INFO/MainProcess] Task tasks.scrape_pending_urls[9134c13d-3173-491f-b346-a5cf7e7079b2] succeeded in 0.0026736001018434763s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:07:56,849: INFO/MainProcess] Task tasks.scrape_pending_urls[db04c384-6ffd-49f3-9829-f315005d1ca3] received
[2026-03-29 08:07:56,852: INFO/MainProcess] Task tasks.scrape_pending_urls[db04c384-6ffd-49f3-9829-f315005d1ca3] succeeded in 0.002481900039128959s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:08:26,850: INFO/MainProcess] Task tasks.scrape_pending_urls[16c16f7e-c448-4aed-89b4-ce15008ffc3c] received
[2026-03-29 08:08:26,853: INFO/MainProcess] Task tasks.scrape_pending_urls[16c16f7e-c448-4aed-89b4-ce15008ffc3c] succeeded in 0.002697400050237775s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:08:56,659: INFO/MainProcess] Task tasks.collect_system_metrics[02664c89-1755-44c4-aaa1-87dab221d083] received
[2026-03-29 08:08:57,177: INFO/MainProcess] Task tasks.collect_system_metrics[02664c89-1755-44c4-aaa1-87dab221d083] succeeded in 0.5180831000907347s: {'cpu': 13.7, 'memory': 45.2}
[2026-03-29 08:08:57,179: INFO/MainProcess] Task tasks.scrape_pending_urls[39851460-8eb2-4062-bcae-92174ae75c8b] received
[2026-03-29 08:08:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[39851460-8eb2-4062-bcae-92174ae75c8b] succeeded in 0.0027172000845894217s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:09:26,850: INFO/MainProcess] Task tasks.scrape_pending_urls[c458ff51-2ba1-4f86-b916-0a450433836b] received
[2026-03-29 08:09:26,852: INFO/MainProcess] Task tasks.scrape_pending_urls[c458ff51-2ba1-4f86-b916-0a450433836b] succeeded in 0.002581799984909594s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:09:56,854: INFO/MainProcess] Task tasks.scrape_pending_urls[80dc6637-d567-4073-ae3c-721c265283d7] received
[2026-03-29 08:09:56,857: INFO/MainProcess] Task tasks.scrape_pending_urls[80dc6637-d567-4073-ae3c-721c265283d7] succeeded in 0.0026253999676555395s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:10:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[6e53e4a6-2510-434a-9cf5-2f5970e33248] received
[2026-03-29 08:10:26,857: INFO/MainProcess] Task tasks.scrape_pending_urls[6e53e4a6-2510-434a-9cf5-2f5970e33248] succeeded in 0.002506999997422099s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:10:56,854: INFO/MainProcess] Task tasks.scrape_pending_urls[bbc402d7-87ce-4c87-9a1e-2f3a6e4e1208] received
[2026-03-29 08:10:56,857: INFO/MainProcess] Task tasks.scrape_pending_urls[bbc402d7-87ce-4c87-9a1e-2f3a6e4e1208] succeeded in 0.002666100044734776s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:11:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[7df9e980-caec-4a35-9d2d-2d5dc6bbef1b] received
[2026-03-29 08:11:26,857: INFO/MainProcess] Task tasks.scrape_pending_urls[7df9e980-caec-4a35-9d2d-2d5dc6bbef1b] succeeded in 0.0026387000689283013s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:11:56,854: INFO/MainProcess] Task tasks.scrape_pending_urls[3e84d5d1-6724-47c5-831e-4fb7d60ee3f3] received
[2026-03-29 08:11:56,857: INFO/MainProcess] Task tasks.scrape_pending_urls[3e84d5d1-6724-47c5-831e-4fb7d60ee3f3] succeeded in 0.0027805001009255648s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:12:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[00fe3dea-065e-4d05-b588-1432b7b69de6] received
[2026-03-29 08:12:26,857: INFO/MainProcess] Task tasks.scrape_pending_urls[00fe3dea-065e-4d05-b588-1432b7b69de6] succeeded in 0.0026538000674918294s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:12:56,855: INFO/MainProcess] Task tasks.scrape_pending_urls[5e903588-a94c-4b9b-a8af-709c1b7d6f9d] received
[2026-03-29 08:12:56,858: INFO/MainProcess] Task tasks.scrape_pending_urls[5e903588-a94c-4b9b-a8af-709c1b7d6f9d] succeeded in 0.002783800009638071s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:13:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[d28af288-34a2-47b6-993b-35d8874d6dad] received
[2026-03-29 08:13:26,858: INFO/MainProcess] Task tasks.scrape_pending_urls[d28af288-34a2-47b6-993b-35d8874d6dad] succeeded in 0.0032374999718740582s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:13:56,638: INFO/MainProcess] Task tasks.reset_stale_processing_urls[de60a268-6d86-4b93-9210-476622be7188] received
[2026-03-29 08:13:56,641: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 08:13:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[de60a268-6d86-4b93-9210-476622be7188] succeeded in 0.003608300001360476s: {'reset': 0}
[2026-03-29 08:13:56,760: INFO/MainProcess] Task tasks.collect_system_metrics[eba7e806-4d25-489f-a7e7-7d2a99f323b9] received
[2026-03-29 08:13:57,276: INFO/MainProcess] Task tasks.collect_system_metrics[eba7e806-4d25-489f-a7e7-7d2a99f323b9] succeeded in 0.516163400025107s: {'cpu': 14.0, 'memory': 45.3}
[2026-03-29 08:13:57,279: INFO/MainProcess] Task tasks.scrape_pending_urls[6858704f-bcf4-4909-9b95-897054b9a0d4] received
[2026-03-29 08:13:57,286: INFO/MainProcess] Task tasks.scrape_pending_urls[6858704f-bcf4-4909-9b95-897054b9a0d4] succeeded in 0.005909400060772896s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:14:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[d822eb21-6832-422a-818a-2d496635a803] received
[2026-03-29 08:14:26,858: INFO/MainProcess] Task tasks.scrape_pending_urls[d822eb21-6832-422a-818a-2d496635a803] succeeded in 0.0028072999557480216s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:14:56,854: INFO/MainProcess] Task tasks.scrape_pending_urls[77856ce1-8d74-442a-b0d1-26160893f5b1] received
[2026-03-29 08:14:56,857: INFO/MainProcess] Task tasks.scrape_pending_urls[77856ce1-8d74-442a-b0d1-26160893f5b1] succeeded in 0.0025382000021636486s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:15:26,854: INFO/MainProcess] Task tasks.scrape_pending_urls[c1c4c0fb-904b-4cb5-98c9-6719b5d63f81] received
[2026-03-29 08:15:26,857: INFO/MainProcess] Task tasks.scrape_pending_urls[c1c4c0fb-904b-4cb5-98c9-6719b5d63f81] succeeded in 0.0026292999973520637s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:15:56,855: INFO/MainProcess] Task tasks.scrape_pending_urls[4dbb4450-2d08-4c78-847a-3e1b85fd591c] received
[2026-03-29 08:15:56,858: INFO/MainProcess] Task tasks.scrape_pending_urls[4dbb4450-2d08-4c78-847a-3e1b85fd591c] succeeded in 0.002678500022739172s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:16:26,859: INFO/MainProcess] Task tasks.scrape_pending_urls[41a52180-59c5-4de5-ad61-26432cc6b6d7] received
[2026-03-29 08:16:26,862: INFO/MainProcess] Task tasks.scrape_pending_urls[41a52180-59c5-4de5-ad61-26432cc6b6d7] succeeded in 0.0026409999700263143s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:16:56,859: INFO/MainProcess] Task tasks.scrape_pending_urls[a9dc49a6-1a85-4440-8a7c-2531e5ddf2c9] received
[2026-03-29 08:16:56,862: INFO/MainProcess] Task tasks.scrape_pending_urls[a9dc49a6-1a85-4440-8a7c-2531e5ddf2c9] succeeded in 0.002626999979838729s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:17:26,859: INFO/MainProcess] Task tasks.scrape_pending_urls[e29811a2-dc0d-485d-bf0a-f19a9c304c82] received
[2026-03-29 08:17:26,862: INFO/MainProcess] Task tasks.scrape_pending_urls[e29811a2-dc0d-485d-bf0a-f19a9c304c82] succeeded in 0.00280149991158396s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:17:56,859: INFO/MainProcess] Task tasks.scrape_pending_urls[1108f3ca-2732-46a1-a108-55cfacef0d82] received
[2026-03-29 08:17:56,862: INFO/MainProcess] Task tasks.scrape_pending_urls[1108f3ca-2732-46a1-a108-55cfacef0d82] succeeded in 0.002626800094731152s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:18:26,859: INFO/MainProcess] Task tasks.scrape_pending_urls[39bbda16-9495-4207-bb7a-9aead19daaa2] received
[2026-03-29 08:18:26,863: INFO/MainProcess] Task tasks.scrape_pending_urls[39bbda16-9495-4207-bb7a-9aead19daaa2] succeeded in 0.0034235999919474125s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:18:56,659: INFO/MainProcess] Task tasks.collect_system_metrics[b277f271-59b0-4441-8d5a-76a69f2e5e70] received
[2026-03-29 08:18:57,176: INFO/MainProcess] Task tasks.collect_system_metrics[b277f271-59b0-4441-8d5a-76a69f2e5e70] succeeded in 0.516878700000234s: {'cpu': 13.7, 'memory': 45.3}
[2026-03-29 08:18:57,178: INFO/MainProcess] Task tasks.scrape_pending_urls[7b57178c-0331-4a12-8836-4febae4be7ed] received
[2026-03-29 08:18:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[7b57178c-0331-4a12-8836-4febae4be7ed] succeeded in 0.002696200041100383s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:19:26,860: INFO/MainProcess] Task tasks.scrape_pending_urls[a2b9bde5-def0-47e0-a996-d71cccab8883] received
[2026-03-29 08:19:26,863: INFO/MainProcess] Task tasks.scrape_pending_urls[a2b9bde5-def0-47e0-a996-d71cccab8883] succeeded in 0.00270990002900362s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:19:56,859: INFO/MainProcess] Task tasks.scrape_pending_urls[859999d7-d27c-4e31-84c2-9219fa9209b5] received
[2026-03-29 08:19:56,862: INFO/MainProcess] Task tasks.scrape_pending_urls[859999d7-d27c-4e31-84c2-9219fa9209b5] succeeded in 0.0026679999427869916s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:20:26,859: INFO/MainProcess] Task tasks.scrape_pending_urls[b694a4fb-272d-4f7b-89f4-c9f907fe510b] received
[2026-03-29 08:20:26,862: INFO/MainProcess] Task tasks.scrape_pending_urls[b694a4fb-272d-4f7b-89f4-c9f907fe510b] succeeded in 0.002701599965803325s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:20:56,859: INFO/MainProcess] Task tasks.scrape_pending_urls[5534653f-d5b1-4593-8983-9e46e918347e] received
[2026-03-29 08:20:56,863: INFO/MainProcess] Task tasks.scrape_pending_urls[5534653f-d5b1-4593-8983-9e46e918347e] succeeded in 0.0028273999923840165s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:21:26,860: INFO/MainProcess] Task tasks.scrape_pending_urls[ffa332ff-1aa3-4928-bedd-d61b68101e00] received
[2026-03-29 08:21:26,863: INFO/MainProcess] Task tasks.scrape_pending_urls[ffa332ff-1aa3-4928-bedd-d61b68101e00] succeeded in 0.002697999938391149s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:21:56,859: INFO/MainProcess] Task tasks.scrape_pending_urls[b426ac1d-7088-4e68-828c-d7db3301e3a2] received
[2026-03-29 08:21:56,863: INFO/MainProcess] Task tasks.scrape_pending_urls[b426ac1d-7088-4e68-828c-d7db3301e3a2] succeeded in 0.003008799976669252s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:22:26,859: INFO/MainProcess] Task tasks.scrape_pending_urls[3d9ba798-19cb-4e0f-b849-d9c7f9a0d0a4] received
[2026-03-29 08:22:26,863: INFO/MainProcess] Task tasks.scrape_pending_urls[3d9ba798-19cb-4e0f-b849-d9c7f9a0d0a4] succeeded in 0.002665200037881732s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:22:56,864: INFO/MainProcess] Task tasks.scrape_pending_urls[9e0124e9-4161-4993-9b95-da102cf1557b] received
[2026-03-29 08:22:56,868: INFO/MainProcess] Task tasks.scrape_pending_urls[9e0124e9-4161-4993-9b95-da102cf1557b] succeeded in 0.003103499999269843s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:23:26,864: INFO/MainProcess] Task tasks.scrape_pending_urls[77247b61-122d-445e-9afa-cc9b26133dfb] received
[2026-03-29 08:23:26,867: INFO/MainProcess] Task tasks.scrape_pending_urls[77247b61-122d-445e-9afa-cc9b26133dfb] succeeded in 0.0025031999684870243s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:23:56,658: INFO/MainProcess] Task tasks.collect_system_metrics[6adfb4da-1061-44cb-bb05-5657f62cf9c8] received
[2026-03-29 08:23:57,174: INFO/MainProcess] Task tasks.collect_system_metrics[6adfb4da-1061-44cb-bb05-5657f62cf9c8] succeeded in 0.5155983999138698s: {'cpu': 14.6, 'memory': 45.2}
[2026-03-29 08:23:57,176: INFO/MainProcess] Task tasks.scrape_pending_urls[71b30694-8651-4020-81f9-c32126b3a174] received
[2026-03-29 08:23:57,179: INFO/MainProcess] Task tasks.scrape_pending_urls[71b30694-8651-4020-81f9-c32126b3a174] succeeded in 0.0026367000536993146s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:24:26,864: INFO/MainProcess] Task tasks.scrape_pending_urls[b8c425a7-69ad-47c2-8882-724aed9987c9] received
[2026-03-29 08:24:26,867: INFO/MainProcess] Task tasks.scrape_pending_urls[b8c425a7-69ad-47c2-8882-724aed9987c9] succeeded in 0.0026458000065758824s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:24:56,865: INFO/MainProcess] Task tasks.scrape_pending_urls[dc015507-79df-447a-9a13-6a5a98e3541f] received
[2026-03-29 08:24:56,868: INFO/MainProcess] Task tasks.scrape_pending_urls[dc015507-79df-447a-9a13-6a5a98e3541f] succeeded in 0.0026044000405818224s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:25:26,864: INFO/MainProcess] Task tasks.scrape_pending_urls[ae33c0a2-d33f-486a-afc6-c39bafa77a21] received
[2026-03-29 08:25:26,867: INFO/MainProcess] Task tasks.scrape_pending_urls[ae33c0a2-d33f-486a-afc6-c39bafa77a21] succeeded in 0.0025328999618068337s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:25:56,865: INFO/MainProcess] Task tasks.scrape_pending_urls[b35578ed-25dc-4952-83b3-5873e3b98fed] received
[2026-03-29 08:25:56,868: INFO/MainProcess] Task tasks.scrape_pending_urls[b35578ed-25dc-4952-83b3-5873e3b98fed] succeeded in 0.002575199934653938s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:26:26,864: INFO/MainProcess] Task tasks.scrape_pending_urls[f818eac8-101c-4248-acff-dbd35bbe4d7e] received
[2026-03-29 08:26:26,867: INFO/MainProcess] Task tasks.scrape_pending_urls[f818eac8-101c-4248-acff-dbd35bbe4d7e] succeeded in 0.0026728000957518816s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:26:56,864: INFO/MainProcess] Task tasks.scrape_pending_urls[e66e0380-bd55-4787-b0ea-cfddfc86d225] received
[2026-03-29 08:26:56,867: INFO/MainProcess] Task tasks.scrape_pending_urls[e66e0380-bd55-4787-b0ea-cfddfc86d225] succeeded in 0.002520599984563887s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:27:26,864: INFO/MainProcess] Task tasks.scrape_pending_urls[1919c6e5-8ec4-4f75-bbea-566bc067467f] received
[2026-03-29 08:27:26,868: INFO/MainProcess] Task tasks.scrape_pending_urls[1919c6e5-8ec4-4f75-bbea-566bc067467f] succeeded in 0.0031671999022364616s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:27:56,864: INFO/MainProcess] Task tasks.scrape_pending_urls[90ae33f4-ffaf-4e5f-8c23-8d15405ca261] received
[2026-03-29 08:27:56,867: INFO/MainProcess] Task tasks.scrape_pending_urls[90ae33f4-ffaf-4e5f-8c23-8d15405ca261] succeeded in 0.0026989999460056424s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:28:26,864: INFO/MainProcess] Task tasks.scrape_pending_urls[8753e821-58b8-4fc7-ad6e-11f0f7214166] received
[2026-03-29 08:28:26,867: INFO/MainProcess] Task tasks.scrape_pending_urls[8753e821-58b8-4fc7-ad6e-11f0f7214166] succeeded in 0.002488599973730743s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:28:56,658: INFO/MainProcess] Task tasks.collect_system_metrics[0d528bd4-4934-4f12-8461-c3c838fbcfe8] received
[2026-03-29 08:28:57,175: INFO/MainProcess] Task tasks.collect_system_metrics[0d528bd4-4934-4f12-8461-c3c838fbcfe8] succeeded in 0.5162089000223204s: {'cpu': 15.3, 'memory': 45.4}
[2026-03-29 08:28:57,177: INFO/MainProcess] Task tasks.scrape_pending_urls[5f45ef66-de1b-4e2f-954f-3dada2b840db] received
[2026-03-29 08:28:57,180: INFO/MainProcess] Task tasks.scrape_pending_urls[5f45ef66-de1b-4e2f-954f-3dada2b840db] succeeded in 0.0025496999733150005s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:29:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[8ce74eb9-851e-4da5-b893-faee69b6f035] received
[2026-03-29 08:29:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[8ce74eb9-851e-4da5-b893-faee69b6f035] succeeded in 0.003270000102929771s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:29:56,869: INFO/MainProcess] Task tasks.scrape_pending_urls[7924ba28-8d31-43ad-b388-fae9106adc2a] received
[2026-03-29 08:29:56,872: INFO/MainProcess] Task tasks.scrape_pending_urls[7924ba28-8d31-43ad-b388-fae9106adc2a] succeeded in 0.0026599999982863665s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[51987e37-d44b-42ea-9054-404c337d4cd4] received
[2026-03-29 08:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[51987e37-d44b-42ea-9054-404c337d4cd4] succeeded in 0.0013566999696195126s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 08:30:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[e9625bcb-5562-409b-b1e9-21abf4d2df70] received
[2026-03-29 08:30:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[e9625bcb-5562-409b-b1e9-21abf4d2df70] succeeded in 0.0030134000116959214s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:30:56,868: INFO/MainProcess] Task tasks.scrape_pending_urls[30be7814-d194-47c9-a497-88e3cc08dc78] received
[2026-03-29 08:30:56,871: INFO/MainProcess] Task tasks.scrape_pending_urls[30be7814-d194-47c9-a497-88e3cc08dc78] succeeded in 0.0027321999659761786s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:31:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[1ad14b8c-4631-4de1-a362-0ede9e1bcecf] received
[2026-03-29 08:31:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[1ad14b8c-4631-4de1-a362-0ede9e1bcecf] succeeded in 0.002942799939773977s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:31:56,869: INFO/MainProcess] Task tasks.scrape_pending_urls[10b464fb-6762-4413-abde-eea49606984c] received
[2026-03-29 08:31:56,872: INFO/MainProcess] Task tasks.scrape_pending_urls[10b464fb-6762-4413-abde-eea49606984c] succeeded in 0.002660700003616512s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:32:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[8e4e9090-4c8f-42b2-8275-20df9043239b] received
[2026-03-29 08:32:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[8e4e9090-4c8f-42b2-8275-20df9043239b] succeeded in 0.0027187999803572893s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:32:56,869: INFO/MainProcess] Task tasks.scrape_pending_urls[bdcdd60d-e66d-4fe4-8b68-846a5d0b894f] received
[2026-03-29 08:32:56,872: INFO/MainProcess] Task tasks.scrape_pending_urls[bdcdd60d-e66d-4fe4-8b68-846a5d0b894f] succeeded in 0.002729399944655597s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:33:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[a73175c1-55ee-4db3-9ef0-29569a019165] received
[2026-03-29 08:33:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[a73175c1-55ee-4db3-9ef0-29569a019165] succeeded in 0.0026388000696897507s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:33:56,659: INFO/MainProcess] Task tasks.collect_system_metrics[920dbc76-29c0-442e-8c28-163c35e5c336] received
[2026-03-29 08:33:57,175: INFO/MainProcess] Task tasks.collect_system_metrics[920dbc76-29c0-442e-8c28-163c35e5c336] succeeded in 0.5158614999381825s: {'cpu': 20.9, 'memory': 45.1}
[2026-03-29 08:33:57,177: INFO/MainProcess] Task tasks.scrape_pending_urls[b57aeda4-72e1-4474-b48a-f9ad52071c27] received
[2026-03-29 08:33:57,180: INFO/MainProcess] Task tasks.scrape_pending_urls[b57aeda4-72e1-4474-b48a-f9ad52071c27] succeeded in 0.0029478000942617655s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:34:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[9b86ef5a-b84d-4879-bac5-6d1eb147dc06] received
[2026-03-29 08:34:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[9b86ef5a-b84d-4879-bac5-6d1eb147dc06] succeeded in 0.0026172000216320157s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:34:56,869: INFO/MainProcess] Task tasks.scrape_pending_urls[e2ae5e02-b587-4373-a575-a78fd0dd2438] received
[2026-03-29 08:34:56,872: INFO/MainProcess] Task tasks.scrape_pending_urls[e2ae5e02-b587-4373-a575-a78fd0dd2438] succeeded in 0.002654600073583424s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:35:26,869: INFO/MainProcess] Task tasks.scrape_pending_urls[6600bc18-88d4-45b0-b774-72a593d79d9c] received
[2026-03-29 08:35:26,872: INFO/MainProcess] Task tasks.scrape_pending_urls[6600bc18-88d4-45b0-b774-72a593d79d9c] succeeded in 0.0024873000802472234s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:35:56,873: INFO/MainProcess] Task tasks.scrape_pending_urls[0882ea72-9b8c-4950-8468-7616416e8d93] received
[2026-03-29 08:35:56,876: INFO/MainProcess] Task tasks.scrape_pending_urls[0882ea72-9b8c-4950-8468-7616416e8d93] succeeded in 0.0026461000088602304s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:36:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[115b5e4b-3b1c-4069-846d-b57c6e2a91d7] received
[2026-03-29 08:36:26,876: INFO/MainProcess] Task tasks.scrape_pending_urls[115b5e4b-3b1c-4069-846d-b57c6e2a91d7] succeeded in 0.0029639999847859144s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:36:56,873: INFO/MainProcess] Task tasks.scrape_pending_urls[71e6e31e-931b-4513-9660-92142d373ebb] received
[2026-03-29 08:36:56,876: INFO/MainProcess] Task tasks.scrape_pending_urls[71e6e31e-931b-4513-9660-92142d373ebb] succeeded in 0.0026925000129267573s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:37:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[19e5d263-81c1-4c9e-8f98-cda8e3606c81] received
[2026-03-29 08:37:26,876: INFO/MainProcess] Task tasks.scrape_pending_urls[19e5d263-81c1-4c9e-8f98-cda8e3606c81] succeeded in 0.002515799948014319s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:37:56,873: INFO/MainProcess] Task tasks.scrape_pending_urls[666f580e-75a9-40ab-a5da-14fdab8fc1c9] received
[2026-03-29 08:37:56,876: INFO/MainProcess] Task tasks.scrape_pending_urls[666f580e-75a9-40ab-a5da-14fdab8fc1c9] succeeded in 0.0027492999797686934s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:38:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[c72f6dcd-cbb3-4e23-910c-36848ae4efbe] received
[2026-03-29 08:38:26,876: INFO/MainProcess] Task tasks.scrape_pending_urls[c72f6dcd-cbb3-4e23-910c-36848ae4efbe] succeeded in 0.0028291000053286552s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:38:56,659: INFO/MainProcess] Task tasks.collect_system_metrics[caf3ac68-7188-4356-87fe-5b8857abecf3] received
[2026-03-29 08:38:57,175: INFO/MainProcess] Task tasks.collect_system_metrics[caf3ac68-7188-4356-87fe-5b8857abecf3] succeeded in 0.5160774999530986s: {'cpu': 16.5, 'memory': 45.3}
[2026-03-29 08:38:57,177: INFO/MainProcess] Task tasks.scrape_pending_urls[8beb30b2-d689-422e-afd8-157da03353c8] received
[2026-03-29 08:38:57,180: INFO/MainProcess] Task tasks.scrape_pending_urls[8beb30b2-d689-422e-afd8-157da03353c8] succeeded in 0.0025746000465005636s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:39:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[e8698fff-2022-4ed2-9be9-ee6d0485a7cf] received
[2026-03-29 08:39:26,876: INFO/MainProcess] Task tasks.scrape_pending_urls[e8698fff-2022-4ed2-9be9-ee6d0485a7cf] succeeded in 0.002524100011214614s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:39:56,873: INFO/MainProcess] Task tasks.scrape_pending_urls[e11ee0a8-a4b1-46ad-a1d7-68ba602223e6] received
[2026-03-29 08:39:56,876: INFO/MainProcess] Task tasks.scrape_pending_urls[e11ee0a8-a4b1-46ad-a1d7-68ba602223e6] succeeded in 0.0028324000304564834s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:40:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[9885e706-aa71-4c49-809d-5c8483f52e13] received
[2026-03-29 08:40:26,876: INFO/MainProcess] Task tasks.scrape_pending_urls[9885e706-aa71-4c49-809d-5c8483f52e13] succeeded in 0.0026663000462576747s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:40:56,873: INFO/MainProcess] Task tasks.scrape_pending_urls[18b9546c-cf7a-4c28-90e6-f39416e33e8a] received
[2026-03-29 08:40:56,876: INFO/MainProcess] Task tasks.scrape_pending_urls[18b9546c-cf7a-4c28-90e6-f39416e33e8a] succeeded in 0.002704799990169704s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:41:26,873: INFO/MainProcess] Task tasks.scrape_pending_urls[8ecdd266-6e6c-4791-8dee-aa708b4507b6] received
[2026-03-29 08:41:26,876: INFO/MainProcess] Task tasks.scrape_pending_urls[8ecdd266-6e6c-4791-8dee-aa708b4507b6] succeeded in 0.002684500068426132s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:41:56,873: INFO/MainProcess] Task tasks.scrape_pending_urls[676f10f1-ec22-42a6-b46a-c152a7c0ce38] received
[2026-03-29 08:41:56,876: INFO/MainProcess] Task tasks.scrape_pending_urls[676f10f1-ec22-42a6-b46a-c152a7c0ce38] succeeded in 0.0027080000145360827s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:42:26,878: INFO/MainProcess] Task tasks.scrape_pending_urls[334dfe64-c170-4a37-b889-3a6e4b34ede1] received
[2026-03-29 08:42:26,881: INFO/MainProcess] Task tasks.scrape_pending_urls[334dfe64-c170-4a37-b889-3a6e4b34ede1] succeeded in 0.0026561999693512917s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:42:56,877: INFO/MainProcess] Task tasks.scrape_pending_urls[ea3aa620-6b79-4648-a5d6-aaa15067e532] received
[2026-03-29 08:42:56,880: INFO/MainProcess] Task tasks.scrape_pending_urls[ea3aa620-6b79-4648-a5d6-aaa15067e532] succeeded in 0.0025607000570744276s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:43:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[bcd46ce7-1764-4e63-a992-078d78676bb7] received
[2026-03-29 08:43:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[bcd46ce7-1764-4e63-a992-078d78676bb7] succeeded in 0.0029061000095680356s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:43:56,638: INFO/MainProcess] Task tasks.reset_stale_processing_urls[f2934a98-dd8c-4649-aa3d-c45311c052a1] received
[2026-03-29 08:43:56,641: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 08:43:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[f2934a98-dd8c-4649-aa3d-c45311c052a1] succeeded in 0.0034573000157251954s: {'reset': 0}
[2026-03-29 08:43:56,760: INFO/MainProcess] Task tasks.collect_system_metrics[de2b50e9-7d5a-4f45-84ce-b1bdafaab745] received
[2026-03-29 08:43:57,278: INFO/MainProcess] Task tasks.collect_system_metrics[de2b50e9-7d5a-4f45-84ce-b1bdafaab745] succeeded in 0.5169814000837505s: {'cpu': 18.5, 'memory': 45.3}
[2026-03-29 08:43:57,280: INFO/MainProcess] Task tasks.scrape_pending_urls[abc3050b-7302-416d-bc9c-3841457e39e2] received
[2026-03-29 08:43:57,283: INFO/MainProcess] Task tasks.scrape_pending_urls[abc3050b-7302-416d-bc9c-3841457e39e2] succeeded in 0.0022468999959528446s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:44:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[63bc0de8-f555-439e-88da-5b866fc4ff1b] received
[2026-03-29 08:44:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[63bc0de8-f555-439e-88da-5b866fc4ff1b] succeeded in 0.0027332999743521214s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:44:56,877: INFO/MainProcess] Task tasks.scrape_pending_urls[10145c7b-0bf4-4d1e-b4e6-55317b0e54f3] received
[2026-03-29 08:44:56,880: INFO/MainProcess] Task tasks.scrape_pending_urls[10145c7b-0bf4-4d1e-b4e6-55317b0e54f3] succeeded in 0.0027173999696969986s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:45:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[1ac00577-0514-4723-95df-75abaaa47f74] received
[2026-03-29 08:45:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[1ac00577-0514-4723-95df-75abaaa47f74] succeeded in 0.0027057999977841973s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:45:56,877: INFO/MainProcess] Task tasks.scrape_pending_urls[f1ecff93-6e52-43d4-84b6-86f226ef96c5] received
[2026-03-29 08:45:56,880: INFO/MainProcess] Task tasks.scrape_pending_urls[f1ecff93-6e52-43d4-84b6-86f226ef96c5] succeeded in 0.0026436999905854464s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:46:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[e21134cd-40bf-42a6-8db9-872f3d1e0ea0] received
[2026-03-29 08:46:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[e21134cd-40bf-42a6-8db9-872f3d1e0ea0] succeeded in 0.00252620002720505s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:46:56,877: INFO/MainProcess] Task tasks.scrape_pending_urls[015cd068-f543-4912-88c4-13bb48468641] received
[2026-03-29 08:46:56,880: INFO/MainProcess] Task tasks.scrape_pending_urls[015cd068-f543-4912-88c4-13bb48468641] succeeded in 0.0025801999727264047s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:47:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[31b2437d-c8c5-47af-8b29-be6cc075eeca] received
[2026-03-29 08:47:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[31b2437d-c8c5-47af-8b29-be6cc075eeca] succeeded in 0.00265670008957386s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:47:56,877: INFO/MainProcess] Task tasks.scrape_pending_urls[50f84a0c-6d1d-4ede-9941-22163070d682] received
[2026-03-29 08:47:56,881: INFO/MainProcess] Task tasks.scrape_pending_urls[50f84a0c-6d1d-4ede-9941-22163070d682] succeeded in 0.0026485000271350145s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:48:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[c27506cd-f3b2-472c-a5b6-1201ef851ca5] received
[2026-03-29 08:48:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[c27506cd-f3b2-472c-a5b6-1201ef851ca5] succeeded in 0.002763899974524975s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:48:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[89238dfb-1824-4017-b0ef-5de3911ccb5c] received
[2026-03-29 08:48:57,179: INFO/MainProcess] Task tasks.collect_system_metrics[89238dfb-1824-4017-b0ef-5de3911ccb5c] succeeded in 0.5161764000076801s: {'cpu': 10.1, 'memory': 45.3}
[2026-03-29 08:48:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[2cc44f3a-ec24-400d-8332-d793e7fc4758] received
[2026-03-29 08:48:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[2cc44f3a-ec24-400d-8332-d793e7fc4758] succeeded in 0.003021000069566071s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:49:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[8e25033b-9bd4-487f-b21a-6913897283eb] received
[2026-03-29 08:49:26,880: INFO/MainProcess] Task tasks.scrape_pending_urls[8e25033b-9bd4-487f-b21a-6913897283eb] succeeded in 0.00248030002694577s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:49:56,878: INFO/MainProcess] Task tasks.scrape_pending_urls[71aab149-fbf1-4954-b778-f59fabf4a1d9] received
[2026-03-29 08:49:56,881: INFO/MainProcess] Task tasks.scrape_pending_urls[71aab149-fbf1-4954-b778-f59fabf4a1d9] succeeded in 0.0028093999717384577s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:50:26,877: INFO/MainProcess] Task tasks.scrape_pending_urls[ab222325-d02b-4cf2-b527-1a09f10f42eb] received
[2026-03-29 08:50:26,881: INFO/MainProcess] Task tasks.scrape_pending_urls[ab222325-d02b-4cf2-b527-1a09f10f42eb] succeeded in 0.0029339001048356295s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:50:56,877: INFO/MainProcess] Task tasks.scrape_pending_urls[c1f50666-ead8-4bce-8ee3-b9feaecaaf85] received
[2026-03-29 08:50:56,881: INFO/MainProcess] Task tasks.scrape_pending_urls[c1f50666-ead8-4bce-8ee3-b9feaecaaf85] succeeded in 0.003462199936620891s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:51:26,878: INFO/MainProcess] Task tasks.scrape_pending_urls[ec5f4870-dd00-4c9a-94d7-705904900f6f] received
[2026-03-29 08:51:26,881: INFO/MainProcess] Task tasks.scrape_pending_urls[ec5f4870-dd00-4c9a-94d7-705904900f6f] succeeded in 0.002639699960127473s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:51:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[e79142af-a9e0-49a0-a398-7bcd9028a53a] received
[2026-03-29 08:51:56,947: INFO/MainProcess] Task tasks.scrape_pending_urls[e79142af-a9e0-49a0-a398-7bcd9028a53a] succeeded in 0.06466029991861433s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:52:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[061d1370-d881-44cb-a128-4245dd57709e] received
[2026-03-29 08:52:26,946: INFO/MainProcess] Task tasks.scrape_pending_urls[061d1370-d881-44cb-a128-4245dd57709e] succeeded in 0.06380680005531758s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:52:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[ead02f19-63ee-4fb9-a0e0-9cfbc6da62b1] received
[2026-03-29 08:52:56,885: INFO/MainProcess] Task tasks.scrape_pending_urls[ead02f19-63ee-4fb9-a0e0-9cfbc6da62b1] succeeded in 0.002534799976274371s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:53:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[79c97446-d4b0-47a2-94bd-ebce2711117f] received
[2026-03-29 08:53:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[79c97446-d4b0-47a2-94bd-ebce2711117f] succeeded in 0.003244200022891164s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:53:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[21821796-2db9-4f5f-bdf4-c695405be755] received
[2026-03-29 08:53:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[21821796-2db9-4f5f-bdf4-c695405be755] succeeded in 0.518929100013338s: {'cpu': 12.3, 'memory': 45.3}
[2026-03-29 08:53:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[576af011-1ccf-4bf9-b9d6-a42542bb0114] received
[2026-03-29 08:53:57,188: INFO/MainProcess] Task tasks.scrape_pending_urls[576af011-1ccf-4bf9-b9d6-a42542bb0114] succeeded in 0.0031166999833658338s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:54:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[e83bc567-6b69-4f67-9c53-76a69343e0e1] received
[2026-03-29 08:54:26,885: INFO/MainProcess] Task tasks.scrape_pending_urls[e83bc567-6b69-4f67-9c53-76a69343e0e1] succeeded in 0.0029052000027149916s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:54:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[3de4e6dd-971f-475f-b728-fe9a89e9689c] received
[2026-03-29 08:54:56,885: INFO/MainProcess] Task tasks.scrape_pending_urls[3de4e6dd-971f-475f-b728-fe9a89e9689c] succeeded in 0.002714899950660765s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:55:26,883: INFO/MainProcess] Task tasks.scrape_pending_urls[2a0bb359-ee0f-437b-92ba-57c89a96bfeb] received
[2026-03-29 08:55:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[2a0bb359-ee0f-437b-92ba-57c89a96bfeb] succeeded in 0.002788800047710538s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:55:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[2150c34c-be0e-4f67-9d56-2ae750a3a719] received
[2026-03-29 08:55:56,885: INFO/MainProcess] Task tasks.scrape_pending_urls[2150c34c-be0e-4f67-9d56-2ae750a3a719] succeeded in 0.0027724000392481685s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:56:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[b6d2a745-35d1-4496-bde3-fc812ecb71d4] received
[2026-03-29 08:56:26,885: INFO/MainProcess] Task tasks.scrape_pending_urls[b6d2a745-35d1-4496-bde3-fc812ecb71d4] succeeded in 0.002818999928422272s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:56:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[2bfb78c3-aaf7-4daf-8fbb-66e346fdeb4e] received
[2026-03-29 08:56:56,951: INFO/MainProcess] Task tasks.scrape_pending_urls[2bfb78c3-aaf7-4daf-8fbb-66e346fdeb4e] succeeded in 0.06803399999625981s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:57:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[5e027a83-79f1-4dea-88a6-05da41a47c62] received
[2026-03-29 08:57:26,885: INFO/MainProcess] Task tasks.scrape_pending_urls[5e027a83-79f1-4dea-88a6-05da41a47c62] succeeded in 0.0026847999542951584s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:57:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[3acc9649-4f3a-478e-90e6-c31773d564df] received
[2026-03-29 08:57:56,886: INFO/MainProcess] Task tasks.scrape_pending_urls[3acc9649-4f3a-478e-90e6-c31773d564df] succeeded in 0.0029248999198898673s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:58:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[f86bb365-ca48-46c8-ab26-f9ad295d9b2a] received
[2026-03-29 08:58:26,885: INFO/MainProcess] Task tasks.scrape_pending_urls[f86bb365-ca48-46c8-ab26-f9ad295d9b2a] succeeded in 0.0026897999923676252s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:58:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[2dd8499e-0e92-4de1-8eec-2a1ebe80fab4] received
[2026-03-29 08:58:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[2dd8499e-0e92-4de1-8eec-2a1ebe80fab4] succeeded in 0.5185973000479862s: {'cpu': 12.1, 'memory': 45.2}
[2026-03-29 08:58:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[af944cad-0ca0-47fa-89cd-b67fffd5da82] received
[2026-03-29 08:58:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[af944cad-0ca0-47fa-89cd-b67fffd5da82] succeeded in 0.0028132000006735325s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:59:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[dd0da723-0e21-47d6-92c3-12bf249dbd7e] received
[2026-03-29 08:59:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[dd0da723-0e21-47d6-92c3-12bf249dbd7e] succeeded in 0.003059100010432303s: {'status': 'idle', 'pending': 0}
[2026-03-29 08:59:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[89afa61f-7690-4233-862d-cfdba157ca54] received
[2026-03-29 08:59:56,885: INFO/MainProcess] Task tasks.scrape_pending_urls[89afa61f-7690-4233-862d-cfdba157ca54] succeeded in 0.002632400020956993s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:00:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[a16a5e4b-2543-42c5-a268-0006793ac459] received
[2026-03-29 09:00:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[a16a5e4b-2543-42c5-a268-0006793ac459] succeeded in 0.002938400022685528s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:00:56,883: INFO/MainProcess] Task tasks.scrape_pending_urls[1278856f-bd1c-4546-86c6-6faf3272d806] received
[2026-03-29 09:00:56,886: INFO/MainProcess] Task tasks.scrape_pending_urls[1278856f-bd1c-4546-86c6-6faf3272d806] succeeded in 0.002869499963708222s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:01:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[aaa259f2-4ddc-4450-8f06-36401a04cc0b] received
[2026-03-29 09:01:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[aaa259f2-4ddc-4450-8f06-36401a04cc0b] succeeded in 0.0027999000158160925s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:01:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[424b411b-0df0-4a9d-abcf-c5a644b4935e] received
[2026-03-29 09:01:56,886: INFO/MainProcess] Task tasks.scrape_pending_urls[424b411b-0df0-4a9d-abcf-c5a644b4935e] succeeded in 0.002622300060465932s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:02:26,882: INFO/MainProcess] Task tasks.scrape_pending_urls[2dd57668-ad6c-459b-9946-dd63760511cd] received
[2026-03-29 09:02:26,885: INFO/MainProcess] Task tasks.scrape_pending_urls[2dd57668-ad6c-459b-9946-dd63760511cd] succeeded in 0.002817399916239083s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:02:56,882: INFO/MainProcess] Task tasks.scrape_pending_urls[7661eedd-7142-4387-a1c5-04a24cf73768] received
[2026-03-29 09:02:56,886: INFO/MainProcess] Task tasks.scrape_pending_urls[7661eedd-7142-4387-a1c5-04a24cf73768] succeeded in 0.0027275000466033816s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:03:26,883: INFO/MainProcess] Task tasks.scrape_pending_urls[4108dabc-05f1-4c99-822f-4f116aa4e895] received
[2026-03-29 09:03:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[4108dabc-05f1-4c99-822f-4f116aa4e895] succeeded in 0.003066199948079884s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:03:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[631ec003-99d2-4a0b-9230-4d0112c16709] received
[2026-03-29 09:03:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[631ec003-99d2-4a0b-9230-4d0112c16709] succeeded in 0.5188843000214547s: {'cpu': 11.1, 'memory': 45.3}
[2026-03-29 09:03:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[7e21d2c9-9851-44fb-8f80-5c7017b2f8e8] received
[2026-03-29 09:03:57,188: INFO/MainProcess] Task tasks.scrape_pending_urls[7e21d2c9-9851-44fb-8f80-5c7017b2f8e8] succeeded in 0.0035022000083699822s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:04:26,883: INFO/MainProcess] Task tasks.scrape_pending_urls[1dde4b52-0e32-4e17-8073-cd12917c2474] received
[2026-03-29 09:04:26,886: INFO/MainProcess] Task tasks.scrape_pending_urls[1dde4b52-0e32-4e17-8073-cd12917c2474] succeeded in 0.003034499939531088s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:04:56,887: INFO/MainProcess] Task tasks.scrape_pending_urls[4d9d1e18-b71f-48e9-b217-a7bd5c3d0dfd] received
[2026-03-29 09:04:56,890: INFO/MainProcess] Task tasks.scrape_pending_urls[4d9d1e18-b71f-48e9-b217-a7bd5c3d0dfd] succeeded in 0.0028510000556707382s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:05:26,887: INFO/MainProcess] Task tasks.scrape_pending_urls[f224e485-10d6-4a63-913b-ecdd775990b5] received
[2026-03-29 09:05:26,890: INFO/MainProcess] Task tasks.scrape_pending_urls[f224e485-10d6-4a63-913b-ecdd775990b5] succeeded in 0.0027393000200390816s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:05:56,887: INFO/MainProcess] Task tasks.scrape_pending_urls[69cb6641-e71a-4a91-af52-c1faaea93a4b] received
[2026-03-29 09:05:56,890: INFO/MainProcess] Task tasks.scrape_pending_urls[69cb6641-e71a-4a91-af52-c1faaea93a4b] succeeded in 0.002520599984563887s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:06:26,887: INFO/MainProcess] Task tasks.scrape_pending_urls[31d9a837-ecf0-466b-9399-9d6236b70c23] received
[2026-03-29 09:06:26,890: INFO/MainProcess] Task tasks.scrape_pending_urls[31d9a837-ecf0-466b-9399-9d6236b70c23] succeeded in 0.0027803999837487936s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:06:56,887: INFO/MainProcess] Task tasks.scrape_pending_urls[39b27552-b1b1-4f1b-9b49-5e03f2c6345b] received
[2026-03-29 09:06:56,890: INFO/MainProcess] Task tasks.scrape_pending_urls[39b27552-b1b1-4f1b-9b49-5e03f2c6345b] succeeded in 0.0025252000195905566s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:07:26,887: INFO/MainProcess] Task tasks.scrape_pending_urls[59eb7e0a-2a1e-48df-a3a2-1a12370d23da] received
[2026-03-29 09:07:26,890: INFO/MainProcess] Task tasks.scrape_pending_urls[59eb7e0a-2a1e-48df-a3a2-1a12370d23da] succeeded in 0.002950900001451373s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:07:56,887: INFO/MainProcess] Task tasks.scrape_pending_urls[79700a44-7926-4482-8c68-7cca2557085a] received
[2026-03-29 09:07:56,890: INFO/MainProcess] Task tasks.scrape_pending_urls[79700a44-7926-4482-8c68-7cca2557085a] succeeded in 0.002688899985514581s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:08:26,887: INFO/MainProcess] Task tasks.scrape_pending_urls[4968e7f7-714d-4288-8465-34b51a836bca] received
[2026-03-29 09:08:26,890: INFO/MainProcess] Task tasks.scrape_pending_urls[4968e7f7-714d-4288-8465-34b51a836bca] succeeded in 0.002656299970112741s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:08:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[f7362bee-c871-4a6b-b3e1-f2be8039d04a] received
[2026-03-29 09:08:57,179: INFO/MainProcess] Task tasks.collect_system_metrics[f7362bee-c871-4a6b-b3e1-f2be8039d04a] succeeded in 0.5158383999951184s: {'cpu': 19.5, 'memory': 45.3}
[2026-03-29 09:08:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[51c8ef37-6142-4dd0-84c8-d203917017d7] received
[2026-03-29 09:08:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[51c8ef37-6142-4dd0-84c8-d203917017d7] succeeded in 0.002739100018516183s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:09:26,887: INFO/MainProcess] Task tasks.scrape_pending_urls[4d365246-c1de-4562-a597-716cba99bb89] received
[2026-03-29 09:09:26,891: INFO/MainProcess] Task tasks.scrape_pending_urls[4d365246-c1de-4562-a597-716cba99bb89] succeeded in 0.003385899937711656s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:09:56,887: INFO/MainProcess] Task tasks.scrape_pending_urls[ee061d3d-4a20-46ff-9cd6-e476cee0fc43] received
[2026-03-29 09:09:56,890: INFO/MainProcess] Task tasks.scrape_pending_urls[ee061d3d-4a20-46ff-9cd6-e476cee0fc43] succeeded in 0.0026437999913468957s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:10:26,887: INFO/MainProcess] Task tasks.scrape_pending_urls[926c6421-419b-405b-97d4-c99341a44d0e] received
[2026-03-29 09:10:26,890: INFO/MainProcess] Task tasks.scrape_pending_urls[926c6421-419b-405b-97d4-c99341a44d0e] succeeded in 0.0026570999762043357s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:10:56,888: INFO/MainProcess] Task tasks.scrape_pending_urls[507360aa-5ead-4210-a310-f8648838a94d] received
[2026-03-29 09:10:56,891: INFO/MainProcess] Task tasks.scrape_pending_urls[507360aa-5ead-4210-a310-f8648838a94d] succeeded in 0.0025460999459028244s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:11:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[575716f1-19dc-499a-897f-d58308e7ba47] received
[2026-03-29 09:11:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[575716f1-19dc-499a-897f-d58308e7ba47] succeeded in 0.0026214999379590154s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:11:56,892: INFO/MainProcess] Task tasks.scrape_pending_urls[3357da7e-bfc8-406c-9d63-f8d3dc9cef32] received
[2026-03-29 09:11:56,894: INFO/MainProcess] Task tasks.scrape_pending_urls[3357da7e-bfc8-406c-9d63-f8d3dc9cef32] succeeded in 0.0025340000865980983s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:12:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[0a56996c-b1c6-4f83-ab7e-88878efe9db4] received
[2026-03-29 09:12:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[0a56996c-b1c6-4f83-ab7e-88878efe9db4] succeeded in 0.0029589999467134476s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:12:56,892: INFO/MainProcess] Task tasks.scrape_pending_urls[1547ffc5-41ef-4693-a2dd-fe0f37eab802] received
[2026-03-29 09:12:56,894: INFO/MainProcess] Task tasks.scrape_pending_urls[1547ffc5-41ef-4693-a2dd-fe0f37eab802] succeeded in 0.0025269000325351954s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:13:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[3ee47298-dc93-45c3-ad14-660d7fa14a0f] received
[2026-03-29 09:13:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[3ee47298-dc93-45c3-ad14-660d7fa14a0f] succeeded in 0.002642800100147724s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:13:56,638: INFO/MainProcess] Task tasks.reset_stale_processing_urls[ed7f46d9-8d03-454b-8ef6-9e4289f17429] received
[2026-03-29 09:13:56,641: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 09:13:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[ed7f46d9-8d03-454b-8ef6-9e4289f17429] succeeded in 0.003818599972873926s: {'reset': 0}
[2026-03-29 09:13:56,760: INFO/MainProcess] Task tasks.collect_system_metrics[3606d1cf-576e-420c-af69-0edfa1df33b8] received
[2026-03-29 09:13:57,278: INFO/MainProcess] Task tasks.collect_system_metrics[3606d1cf-576e-420c-af69-0edfa1df33b8] succeeded in 0.5179755000863224s: {'cpu': 12.9, 'memory': 45.2}
[2026-03-29 09:13:57,280: INFO/MainProcess] Task tasks.scrape_pending_urls[9e6fc15a-ced0-484d-8183-1203b2c8972e] received
[2026-03-29 09:13:57,283: INFO/MainProcess] Task tasks.scrape_pending_urls[9e6fc15a-ced0-484d-8183-1203b2c8972e] succeeded in 0.0024064999306574464s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:14:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[6c8fdc61-86d2-4d29-987b-c86ab148ae38] received
[2026-03-29 09:14:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[6c8fdc61-86d2-4d29-987b-c86ab148ae38] succeeded in 0.0027689000125974417s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:14:56,892: INFO/MainProcess] Task tasks.scrape_pending_urls[488fd2f6-9b57-458e-8018-31f6555386a1] received
[2026-03-29 09:14:56,895: INFO/MainProcess] Task tasks.scrape_pending_urls[488fd2f6-9b57-458e-8018-31f6555386a1] succeeded in 0.0026981999399140477s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:15:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[422d73ea-f3b2-4632-b7f6-2040c49fa6ba] received
[2026-03-29 09:15:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[422d73ea-f3b2-4632-b7f6-2040c49fa6ba] succeeded in 0.002648300025612116s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:15:56,892: INFO/MainProcess] Task tasks.scrape_pending_urls[d8887dd8-5719-4fe3-a141-26b2b190729f] received
[2026-03-29 09:15:56,895: INFO/MainProcess] Task tasks.scrape_pending_urls[d8887dd8-5719-4fe3-a141-26b2b190729f] succeeded in 0.0026596999960020185s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:16:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[ffd605f5-5118-4b8e-b0ac-6b9e2a7d931d] received
[2026-03-29 09:16:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[ffd605f5-5118-4b8e-b0ac-6b9e2a7d931d] succeeded in 0.0029912999598309398s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:16:56,892: INFO/MainProcess] Task tasks.scrape_pending_urls[be8643fc-4b11-488b-8895-0ac13c0a2541] received
[2026-03-29 09:16:56,895: INFO/MainProcess] Task tasks.scrape_pending_urls[be8643fc-4b11-488b-8895-0ac13c0a2541] succeeded in 0.002956999931484461s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:17:26,892: INFO/MainProcess] Task tasks.scrape_pending_urls[2587243b-fcaa-43e9-8f74-5200eb8d7b85] received
[2026-03-29 09:17:26,895: INFO/MainProcess] Task tasks.scrape_pending_urls[2587243b-fcaa-43e9-8f74-5200eb8d7b85] succeeded in 0.0025302000576630235s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:17:56,896: INFO/MainProcess] Task tasks.scrape_pending_urls[335b1e32-4a3e-4748-8e91-dfd85ef76187] received
[2026-03-29 09:17:56,899: INFO/MainProcess] Task tasks.scrape_pending_urls[335b1e32-4a3e-4748-8e91-dfd85ef76187] succeeded in 0.00266400002874434s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:18:26,896: INFO/MainProcess] Task tasks.scrape_pending_urls[2558c8ec-5c7d-4d5b-849a-c4f63dcc60b1] received
[2026-03-29 09:18:26,900: INFO/MainProcess] Task tasks.scrape_pending_urls[2558c8ec-5c7d-4d5b-849a-c4f63dcc60b1] succeeded in 0.0034241999965161085s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:18:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[c7a76473-8ae8-4ef0-9419-989d083ab03d] received
[2026-03-29 09:18:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[c7a76473-8ae8-4ef0-9419-989d083ab03d] succeeded in 0.516756400000304s: {'cpu': 15.2, 'memory': 45.4}
[2026-03-29 09:18:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[9fb2cec0-0638-4ff0-95eb-5ea97f2e52f3] received
[2026-03-29 09:18:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[9fb2cec0-0638-4ff0-95eb-5ea97f2e52f3] succeeded in 0.002687699976377189s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:19:26,896: INFO/MainProcess] Task tasks.scrape_pending_urls[7c5464ec-9674-453e-a3b9-bc66db640e09] received
[2026-03-29 09:19:26,899: INFO/MainProcess] Task tasks.scrape_pending_urls[7c5464ec-9674-453e-a3b9-bc66db640e09] succeeded in 0.002711900044232607s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:19:56,897: INFO/MainProcess] Task tasks.scrape_pending_urls[ce44c129-edb3-4c9e-8b2a-be1e606b8742] received
[2026-03-29 09:19:56,901: INFO/MainProcess] Task tasks.scrape_pending_urls[ce44c129-edb3-4c9e-8b2a-be1e606b8742] succeeded in 0.003896899987012148s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:20:26,896: INFO/MainProcess] Task tasks.scrape_pending_urls[b78fa1b6-8321-44f2-9a25-3e07d521a457] received
[2026-03-29 09:20:26,899: INFO/MainProcess] Task tasks.scrape_pending_urls[b78fa1b6-8321-44f2-9a25-3e07d521a457] succeeded in 0.002803000039421022s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:20:56,897: INFO/MainProcess] Task tasks.scrape_pending_urls[d11d6c35-2c40-4c32-ab26-076da72e246f] received
[2026-03-29 09:20:56,900: INFO/MainProcess] Task tasks.scrape_pending_urls[d11d6c35-2c40-4c32-ab26-076da72e246f] succeeded in 0.003172100055962801s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:21:26,896: INFO/MainProcess] Task tasks.scrape_pending_urls[b98e110e-7021-4404-927b-fd99fef7a208] received
[2026-03-29 09:21:26,899: INFO/MainProcess] Task tasks.scrape_pending_urls[b98e110e-7021-4404-927b-fd99fef7a208] succeeded in 0.0024924000026658177s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:21:56,896: INFO/MainProcess] Task tasks.scrape_pending_urls[bb2e4b56-9c7a-47af-af86-818ff92f31bd] received
[2026-03-29 09:21:56,900: INFO/MainProcess] Task tasks.scrape_pending_urls[bb2e4b56-9c7a-47af-af86-818ff92f31bd] succeeded in 0.0028291000053286552s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:22:26,896: INFO/MainProcess] Task tasks.scrape_pending_urls[8f1499f1-8431-40b0-ae51-4447d9d42d8c] received
[2026-03-29 09:22:26,899: INFO/MainProcess] Task tasks.scrape_pending_urls[8f1499f1-8431-40b0-ae51-4447d9d42d8c] succeeded in 0.0025441000470891595s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:22:56,897: INFO/MainProcess] Task tasks.scrape_pending_urls[b7ddeaf5-40af-461e-bdc6-94fc481cb688] received
[2026-03-29 09:22:56,900: INFO/MainProcess] Task tasks.scrape_pending_urls[b7ddeaf5-40af-461e-bdc6-94fc481cb688] succeeded in 0.002513499930500984s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:23:26,897: INFO/MainProcess] Task tasks.scrape_pending_urls[e10535b4-2774-4e61-b15a-c57cea6607e3] received
[2026-03-29 09:23:26,900: INFO/MainProcess] Task tasks.scrape_pending_urls[e10535b4-2774-4e61-b15a-c57cea6607e3] succeeded in 0.003002000041306019s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:23:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[d6922e47-4ea8-4433-9286-33a182d25e72] received
[2026-03-29 09:23:57,181: INFO/MainProcess] Task tasks.collect_system_metrics[d6922e47-4ea8-4433-9286-33a182d25e72] succeeded in 0.5178859999869019s: {'cpu': 14.2, 'memory': 45.3}
[2026-03-29 09:23:57,183: INFO/MainProcess] Task tasks.scrape_pending_urls[e1dc1f32-4e45-4c5e-af09-52a0cdd6842a] received
[2026-03-29 09:23:57,186: INFO/MainProcess] Task tasks.scrape_pending_urls[e1dc1f32-4e45-4c5e-af09-52a0cdd6842a] succeeded in 0.002562299952842295s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:24:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[ee23e289-f1c4-493b-a6e5-ddd0ec4f7010] received
[2026-03-29 09:24:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[ee23e289-f1c4-493b-a6e5-ddd0ec4f7010] succeeded in 0.0026334000285714865s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:24:56,901: INFO/MainProcess] Task tasks.scrape_pending_urls[347728fd-67bb-4a7a-938f-c70dcb6042b3] received
[2026-03-29 09:24:56,904: INFO/MainProcess] Task tasks.scrape_pending_urls[347728fd-67bb-4a7a-938f-c70dcb6042b3] succeeded in 0.002886999980546534s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:25:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[df8ee572-5d5e-4be2-941a-3e38d13c5cc2] received
[2026-03-29 09:25:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[df8ee572-5d5e-4be2-941a-3e38d13c5cc2] succeeded in 0.002823999966494739s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:25:56,901: INFO/MainProcess] Task tasks.scrape_pending_urls[e9d0d7c5-bacb-460d-8b4f-ceeee2272754] received
[2026-03-29 09:25:56,904: INFO/MainProcess] Task tasks.scrape_pending_urls[e9d0d7c5-bacb-460d-8b4f-ceeee2272754] succeeded in 0.0026057000504806638s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:26:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[c4dad815-4713-44f4-8aa2-c9093a3a0898] received
[2026-03-29 09:26:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[c4dad815-4713-44f4-8aa2-c9093a3a0898] succeeded in 0.0030680999625474215s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:26:56,901: INFO/MainProcess] Task tasks.scrape_pending_urls[e81279a8-56e6-42f1-8bc4-469e507d83ea] received
[2026-03-29 09:26:56,904: INFO/MainProcess] Task tasks.scrape_pending_urls[e81279a8-56e6-42f1-8bc4-469e507d83ea] succeeded in 0.002545999945141375s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:27:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[249f9272-906d-4a93-989b-80e561ce3a64] received
[2026-03-29 09:27:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[249f9272-906d-4a93-989b-80e561ce3a64] succeeded in 0.0027679000049829483s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:27:56,901: INFO/MainProcess] Task tasks.scrape_pending_urls[c5f9afcc-f143-4ed0-ba0b-a3c31fcc5c54] received
[2026-03-29 09:27:56,904: INFO/MainProcess] Task tasks.scrape_pending_urls[c5f9afcc-f143-4ed0-ba0b-a3c31fcc5c54] succeeded in 0.003088700002990663s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:28:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[dd09a004-d1af-454b-9bd3-17985ce7331c] received
[2026-03-29 09:28:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[dd09a004-d1af-454b-9bd3-17985ce7331c] succeeded in 0.0025209999876096845s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:28:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[722973b8-0bd4-4338-abb2-67c3b0527c2d] received
[2026-03-29 09:28:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[722973b8-0bd4-4338-abb2-67c3b0527c2d] succeeded in 0.5163333000382408s: {'cpu': 11.9, 'memory': 45.4}
[2026-03-29 09:28:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[bc4408dc-56cf-497e-aa2a-cf60268fb9bd] received
[2026-03-29 09:28:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[bc4408dc-56cf-497e-aa2a-cf60268fb9bd] succeeded in 0.0025765999453142285s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:29:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[d99df405-33a8-4980-b849-b0338cc8e7dc] received
[2026-03-29 09:29:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[d99df405-33a8-4980-b849-b0338cc8e7dc] succeeded in 0.002644199994392693s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:29:56,901: INFO/MainProcess] Task tasks.scrape_pending_urls[20f04635-0cc0-4c44-a40a-b965dbd6658a] received
[2026-03-29 09:29:56,904: INFO/MainProcess] Task tasks.scrape_pending_urls[20f04635-0cc0-4c44-a40a-b965dbd6658a] succeeded in 0.002660400001332164s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:30:00,001: INFO/MainProcess] Task tasks.purge_old_debug_html[5b442b58-f70b-40bc-9eeb-81b805226c38] received
[2026-03-29 09:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[5b442b58-f70b-40bc-9eeb-81b805226c38] succeeded in 0.001446800073608756s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 09:30:26,901: INFO/MainProcess] Task tasks.scrape_pending_urls[454bbfc8-b0b9-4769-9c2d-98450cc29f9b] received
[2026-03-29 09:30:26,904: INFO/MainProcess] Task tasks.scrape_pending_urls[454bbfc8-b0b9-4769-9c2d-98450cc29f9b] succeeded in 0.0026264000916853547s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:30:56,905: INFO/MainProcess] Task tasks.scrape_pending_urls[10e5f033-2f51-4ded-a174-81ff88a3e0c0] received
[2026-03-29 09:30:56,908: INFO/MainProcess] Task tasks.scrape_pending_urls[10e5f033-2f51-4ded-a174-81ff88a3e0c0] succeeded in 0.0026390000712126493s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:31:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[5415daa3-9975-4e3e-a4c4-7bfc7475ae6d] received
[2026-03-29 09:31:26,908: INFO/MainProcess] Task tasks.scrape_pending_urls[5415daa3-9975-4e3e-a4c4-7bfc7475ae6d] succeeded in 0.002532100072130561s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:31:56,905: INFO/MainProcess] Task tasks.scrape_pending_urls[05afde37-3441-4d5e-94e3-f3cd10f296f6] received
[2026-03-29 09:31:56,908: INFO/MainProcess] Task tasks.scrape_pending_urls[05afde37-3441-4d5e-94e3-f3cd10f296f6] succeeded in 0.002649499918334186s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:32:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[864d9687-dfa6-43f9-b1ed-88bdc308568b] received
[2026-03-29 09:32:26,908: INFO/MainProcess] Task tasks.scrape_pending_urls[864d9687-dfa6-43f9-b1ed-88bdc308568b] succeeded in 0.002864200039766729s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:32:56,905: INFO/MainProcess] Task tasks.scrape_pending_urls[dcfe8306-d21a-48cd-a12f-c1ab063b6acc] received
[2026-03-29 09:32:56,908: INFO/MainProcess] Task tasks.scrape_pending_urls[dcfe8306-d21a-48cd-a12f-c1ab063b6acc] succeeded in 0.002881399937905371s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:33:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[9d4673ef-b9ca-484a-ae79-857c5616185d] received
[2026-03-29 09:33:26,908: INFO/MainProcess] Task tasks.scrape_pending_urls[9d4673ef-b9ca-484a-ae79-857c5616185d] succeeded in 0.002877600025385618s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:33:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[6361437e-0931-42c3-b84e-3ecbdcb8b7fa] received
[2026-03-29 09:33:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[6361437e-0931-42c3-b84e-3ecbdcb8b7fa] succeeded in 0.516243499936536s: {'cpu': 10.7, 'memory': 45.5}
[2026-03-29 09:33:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[b5cf59c1-76ff-4d10-aca3-0e550eaa4e9d] received
[2026-03-29 09:33:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[b5cf59c1-76ff-4d10-aca3-0e550eaa4e9d] succeeded in 0.0027289000572636724s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:34:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[a8dc3ebc-f5eb-4873-98fc-4657d499341e] received
[2026-03-29 09:34:26,908: INFO/MainProcess] Task tasks.scrape_pending_urls[a8dc3ebc-f5eb-4873-98fc-4657d499341e] succeeded in 0.0027312999591231346s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:34:56,905: INFO/MainProcess] Task tasks.scrape_pending_urls[2a7cba83-de19-4261-86ac-1a7863955d73] received
[2026-03-29 09:34:56,908: INFO/MainProcess] Task tasks.scrape_pending_urls[2a7cba83-de19-4261-86ac-1a7863955d73] succeeded in 0.0025206999853253365s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:35:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[009c6223-ca08-4e03-8868-9b929e8bdbcb] received
[2026-03-29 09:35:26,908: INFO/MainProcess] Task tasks.scrape_pending_urls[009c6223-ca08-4e03-8868-9b929e8bdbcb] succeeded in 0.0027215000009164214s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:35:56,905: INFO/MainProcess] Task tasks.scrape_pending_urls[449d7890-be63-42f7-af1b-37657f75ca9c] received
[2026-03-29 09:35:56,908: INFO/MainProcess] Task tasks.scrape_pending_urls[449d7890-be63-42f7-af1b-37657f75ca9c] succeeded in 0.002650899928994477s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:36:26,905: INFO/MainProcess] Task tasks.scrape_pending_urls[73ce90ae-7d49-48e3-ba49-99a242a24ae7] received
[2026-03-29 09:36:26,908: INFO/MainProcess] Task tasks.scrape_pending_urls[73ce90ae-7d49-48e3-ba49-99a242a24ae7] succeeded in 0.002697800053283572s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:36:56,905: INFO/MainProcess] Task tasks.scrape_pending_urls[a28086d2-ae54-4324-9994-c05d874baf20] received
[2026-03-29 09:36:56,908: INFO/MainProcess] Task tasks.scrape_pending_urls[a28086d2-ae54-4324-9994-c05d874baf20] succeeded in 0.0026564999716356397s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:37:26,910: INFO/MainProcess] Task tasks.scrape_pending_urls[fbd85449-d862-44cb-be03-3bfc701b4f4f] received
[2026-03-29 09:37:26,913: INFO/MainProcess] Task tasks.scrape_pending_urls[fbd85449-d862-44cb-be03-3bfc701b4f4f] succeeded in 0.0026834000600501895s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:37:56,910: INFO/MainProcess] Task tasks.scrape_pending_urls[62e4bcb7-178c-4594-b32f-68d230344bd2] received
[2026-03-29 09:37:56,913: INFO/MainProcess] Task tasks.scrape_pending_urls[62e4bcb7-178c-4594-b32f-68d230344bd2] succeeded in 0.0026686000637710094s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:38:26,910: INFO/MainProcess] Task tasks.scrape_pending_urls[2d3a6e06-9a96-4b17-9907-eacceec59f91] received
[2026-03-29 09:38:26,913: INFO/MainProcess] Task tasks.scrape_pending_urls[2d3a6e06-9a96-4b17-9907-eacceec59f91] succeeded in 0.002650099922902882s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:38:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[7218ffae-9f9c-41e3-a14e-6017d5bf9ec2] received
[2026-03-29 09:38:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[7218ffae-9f9c-41e3-a14e-6017d5bf9ec2] succeeded in 0.5165854999795556s: {'cpu': 16.1, 'memory': 45.3}
[2026-03-29 09:38:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[4674d05c-c529-4e18-9e2a-4a310869b4d3] received
[2026-03-29 09:38:57,189: INFO/MainProcess] Task tasks.scrape_pending_urls[4674d05c-c529-4e18-9e2a-4a310869b4d3] succeeded in 0.006162500008940697s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:39:26,910: INFO/MainProcess] Task tasks.scrape_pending_urls[08ac1833-6114-4c05-b300-65080752c01f] received
[2026-03-29 09:39:26,914: INFO/MainProcess] Task tasks.scrape_pending_urls[08ac1833-6114-4c05-b300-65080752c01f] succeeded in 0.0027185999788343906s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:39:56,911: INFO/MainProcess] Task tasks.scrape_pending_urls[97ebc464-3a29-472b-a628-d31d0427991d] received
[2026-03-29 09:39:56,914: INFO/MainProcess] Task tasks.scrape_pending_urls[97ebc464-3a29-472b-a628-d31d0427991d] succeeded in 0.0026670999359339476s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:40:26,910: INFO/MainProcess] Task tasks.scrape_pending_urls[50678fab-7f0f-4c24-9bb2-64d0f6900b74] received
[2026-03-29 09:40:26,913: INFO/MainProcess] Task tasks.scrape_pending_urls[50678fab-7f0f-4c24-9bb2-64d0f6900b74] succeeded in 0.002675600000657141s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:40:56,911: INFO/MainProcess] Task tasks.scrape_pending_urls[16589d87-aca7-4769-8a12-2955698f9a67] received
[2026-03-29 09:40:56,914: INFO/MainProcess] Task tasks.scrape_pending_urls[16589d87-aca7-4769-8a12-2955698f9a67] succeeded in 0.0026919000083580613s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:41:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[34990bc0-6068-4f18-9ac4-e268643e9c25] received
[2026-03-29 09:41:26,913: INFO/MainProcess] Task tasks.scrape_pending_urls[34990bc0-6068-4f18-9ac4-e268643e9c25] succeeded in 0.0025129999266937375s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:41:56,911: INFO/MainProcess] Task tasks.scrape_pending_urls[e8b22de4-144b-43a3-8dde-14c490ecf19b] received
[2026-03-29 09:41:56,914: INFO/MainProcess] Task tasks.scrape_pending_urls[e8b22de4-144b-43a3-8dde-14c490ecf19b] succeeded in 0.0027555000269785523s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:42:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[e979f6a7-6035-414f-90e2-c805083a0e83] received
[2026-03-29 09:42:26,915: INFO/MainProcess] Task tasks.scrape_pending_urls[e979f6a7-6035-414f-90e2-c805083a0e83] succeeded in 0.0038613000651821494s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:42:56,911: INFO/MainProcess] Task tasks.scrape_pending_urls[1b614d18-f698-40ee-ab96-6eb05a59d1b5] received
[2026-03-29 09:42:56,913: INFO/MainProcess] Task tasks.scrape_pending_urls[1b614d18-f698-40ee-ab96-6eb05a59d1b5] succeeded in 0.002523500006645918s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:43:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[020ff11e-f98c-446f-9c9f-9a3b718be75d] received
[2026-03-29 09:43:26,914: INFO/MainProcess] Task tasks.scrape_pending_urls[020ff11e-f98c-446f-9c9f-9a3b718be75d] succeeded in 0.0027104999171569943s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:43:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[6a25c642-f3e9-495f-8987-686bf1022b3d] received
[2026-03-29 09:43:56,645: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 09:43:56,646: INFO/MainProcess] Task tasks.reset_stale_processing_urls[6a25c642-f3e9-495f-8987-686bf1022b3d] succeeded in 0.00356330000795424s: {'reset': 0}
[2026-03-29 09:43:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[92628ac5-b046-42c2-b078-0e8433ca214e] received
[2026-03-29 09:43:57,179: INFO/MainProcess] Task tasks.collect_system_metrics[92628ac5-b046-42c2-b078-0e8433ca214e] succeeded in 0.5157163999974728s: {'cpu': 17.7, 'memory': 45.5}
[2026-03-29 09:43:57,180: INFO/MainProcess] Task tasks.scrape_pending_urls[5b7314ae-c0a3-4194-b013-de6876485e1c] received
[2026-03-29 09:43:57,183: INFO/MainProcess] Task tasks.scrape_pending_urls[5b7314ae-c0a3-4194-b013-de6876485e1c] succeeded in 0.002238100045360625s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:44:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[e982a1a0-214a-4038-bff1-e3c93d3e428c] received
[2026-03-29 09:44:26,914: INFO/MainProcess] Task tasks.scrape_pending_urls[e982a1a0-214a-4038-bff1-e3c93d3e428c] succeeded in 0.0026650000363588333s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:44:56,911: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b2142d-1338-4c9c-9b7b-f89477f453f5] received
[2026-03-29 09:44:56,914: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b2142d-1338-4c9c-9b7b-f89477f453f5] succeeded in 0.0028439000016078353s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:45:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[0769b4d7-bf70-4196-aaaf-c4eb24da0746] received
[2026-03-29 09:45:26,915: INFO/MainProcess] Task tasks.scrape_pending_urls[0769b4d7-bf70-4196-aaaf-c4eb24da0746] succeeded in 0.003168600029312074s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:45:56,911: INFO/MainProcess] Task tasks.scrape_pending_urls[ca6f7b7f-a22d-4c23-b98e-2e10d8d6cfd7] received
[2026-03-29 09:45:56,914: INFO/MainProcess] Task tasks.scrape_pending_urls[ca6f7b7f-a22d-4c23-b98e-2e10d8d6cfd7] succeeded in 0.0026636000256985426s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:46:26,911: INFO/MainProcess] Task tasks.scrape_pending_urls[22898461-01d0-4d97-a260-c0762b3ccde6] received
[2026-03-29 09:46:26,915: INFO/MainProcess] Task tasks.scrape_pending_urls[22898461-01d0-4d97-a260-c0762b3ccde6] succeeded in 0.003343599964864552s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:46:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[bca5ab5b-bc4f-47b7-b7bc-ae3b1eaeddea] received
[2026-03-29 09:46:57,085: INFO/MainProcess] Task tasks.scrape_pending_urls[bca5ab5b-bc4f-47b7-b7bc-ae3b1eaeddea] succeeded in 0.0028506999369710684s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:47:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[6fae9afb-f905-48b4-9e28-0cadcd1bf018] received
[2026-03-29 09:47:27,085: INFO/MainProcess] Task tasks.scrape_pending_urls[6fae9afb-f905-48b4-9e28-0cadcd1bf018] succeeded in 0.0027258999180048704s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:47:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[5132bc03-3508-4933-8a7c-cf93a4465259] received
[2026-03-29 09:47:57,085: INFO/MainProcess] Task tasks.scrape_pending_urls[5132bc03-3508-4933-8a7c-cf93a4465259] succeeded in 0.0026186000322923064s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:48:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[396ffccc-b89e-44b1-8152-30212e0cedb9] received
[2026-03-29 09:48:27,085: INFO/MainProcess] Task tasks.scrape_pending_urls[396ffccc-b89e-44b1-8152-30212e0cedb9] succeeded in 0.0028581999940797687s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:48:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[1079a781-fab8-40bd-aa75-752752a887fe] received
[2026-03-29 09:48:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[1079a781-fab8-40bd-aa75-752752a887fe] succeeded in 0.5164302000775933s: {'cpu': 15.0, 'memory': 45.6}
[2026-03-29 09:48:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[6caf81d1-a866-4c51-b206-c917e5cf4aa5] received
[2026-03-29 09:48:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[6caf81d1-a866-4c51-b206-c917e5cf4aa5] succeeded in 0.0027354999911040068s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:49:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[5160dbb6-7da6-4732-ac81-42b8a7f8c24b] received
[2026-03-29 09:49:27,085: INFO/MainProcess] Task tasks.scrape_pending_urls[5160dbb6-7da6-4732-ac81-42b8a7f8c24b] succeeded in 0.002701000077649951s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:49:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[c98e376f-27da-493e-a0fd-bc5e92d37cfb] received
[2026-03-29 09:49:57,085: INFO/MainProcess] Task tasks.scrape_pending_urls[c98e376f-27da-493e-a0fd-bc5e92d37cfb] succeeded in 0.002723500016145408s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:50:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[9cded9ae-af35-4ca6-84c3-6a40a15ce9b6] received
[2026-03-29 09:50:27,086: INFO/MainProcess] Task tasks.scrape_pending_urls[9cded9ae-af35-4ca6-84c3-6a40a15ce9b6] succeeded in 0.002750899991951883s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:50:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[6e51decc-fc4f-4ed7-a9d6-d003a53a47c8] received
[2026-03-29 09:50:57,085: INFO/MainProcess] Task tasks.scrape_pending_urls[6e51decc-fc4f-4ed7-a9d6-d003a53a47c8] succeeded in 0.002473499975167215s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:51:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[d174e1ae-7cfa-404f-a9f2-dc8cb3e780be] received
[2026-03-29 09:51:27,085: INFO/MainProcess] Task tasks.scrape_pending_urls[d174e1ae-7cfa-404f-a9f2-dc8cb3e780be] succeeded in 0.0027474999660626054s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:51:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[35eef5b2-e4ec-4196-b379-5f6db89d3fc8] received
[2026-03-29 09:51:57,086: INFO/MainProcess] Task tasks.scrape_pending_urls[35eef5b2-e4ec-4196-b379-5f6db89d3fc8] succeeded in 0.0031739999540150166s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:52:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[fe8e551d-9f62-4114-a43c-cec6277726ee] received
[2026-03-29 09:52:27,151: INFO/MainProcess] Task tasks.scrape_pending_urls[fe8e551d-9f62-4114-a43c-cec6277726ee] succeeded in 0.06852839991915971s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:52:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[680f129b-b8f2-4665-a4bd-59b2f76bc595] received
[2026-03-29 09:52:57,146: INFO/MainProcess] Task tasks.scrape_pending_urls[680f129b-b8f2-4665-a4bd-59b2f76bc595] succeeded in 0.06357400002889335s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:53:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[067cd804-7576-45f7-82e7-fcc048156338] received
[2026-03-29 09:53:27,085: INFO/MainProcess] Task tasks.scrape_pending_urls[067cd804-7576-45f7-82e7-fcc048156338] succeeded in 0.002944699954241514s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:53:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[fdad80e7-995d-458c-b86a-4a47f6c2870d] received
[2026-03-29 09:53:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[fdad80e7-995d-458c-b86a-4a47f6c2870d] succeeded in 0.5190311999758705s: {'cpu': 15.2, 'memory': 45.2}
[2026-03-29 09:53:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[e6cb4502-c1c9-46be-b3ee-00d9692505ea] received
[2026-03-29 09:53:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[e6cb4502-c1c9-46be-b3ee-00d9692505ea] succeeded in 0.0028076000744476914s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:54:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[e6911850-a7f3-413d-bd47-f80cf7cc0d21] received
[2026-03-29 09:54:27,085: INFO/MainProcess] Task tasks.scrape_pending_urls[e6911850-a7f3-413d-bd47-f80cf7cc0d21] succeeded in 0.002764899982139468s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:54:57,100: INFO/MainProcess] Task tasks.scrape_pending_urls[6a3dc7fa-8701-460c-80d7-a811568ff2c8] received
[2026-03-29 09:54:57,105: INFO/MainProcess] Task tasks.scrape_pending_urls[6a3dc7fa-8701-460c-80d7-a811568ff2c8] succeeded in 0.004310199990868568s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:55:27,083: INFO/MainProcess] Task tasks.scrape_pending_urls[7a6b5be4-4407-49c9-807e-69f5b7faa4bb] received
[2026-03-29 09:55:27,086: INFO/MainProcess] Task tasks.scrape_pending_urls[7a6b5be4-4407-49c9-807e-69f5b7faa4bb] succeeded in 0.0027085000183433294s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:55:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[20fcf2c3-5c5f-4b19-8bdc-e0d5c4a45880] received
[2026-03-29 09:55:57,085: INFO/MainProcess] Task tasks.scrape_pending_urls[20fcf2c3-5c5f-4b19-8bdc-e0d5c4a45880] succeeded in 0.0026560999685898423s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:56:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[550d968b-58de-4678-b992-a1c977b0f1da] received
[2026-03-29 09:56:27,086: INFO/MainProcess] Task tasks.scrape_pending_urls[550d968b-58de-4678-b992-a1c977b0f1da] succeeded in 0.002844899892807007s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:56:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[4ebf3288-e8f2-49f7-a13c-bac4503007bd] received
[2026-03-29 09:56:57,085: INFO/MainProcess] Task tasks.scrape_pending_urls[4ebf3288-e8f2-49f7-a13c-bac4503007bd] succeeded in 0.002661700011231005s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:57:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[73232d8c-08dc-43ae-9af1-9bbc2ba56346] received
[2026-03-29 09:57:27,147: INFO/MainProcess] Task tasks.scrape_pending_urls[73232d8c-08dc-43ae-9af1-9bbc2ba56346] succeeded in 0.06381880003027618s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:57:57,082: INFO/MainProcess] Task tasks.scrape_pending_urls[d2778f8d-2116-4243-8bcb-31d06b536fe3] received
[2026-03-29 09:57:57,086: INFO/MainProcess] Task tasks.scrape_pending_urls[d2778f8d-2116-4243-8bcb-31d06b536fe3] succeeded in 0.0030960000585764647s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:58:27,082: INFO/MainProcess] Task tasks.scrape_pending_urls[4eaa0542-c4a2-4597-9565-e02cec240186] received
[2026-03-29 09:58:27,086: INFO/MainProcess] Task tasks.scrape_pending_urls[4eaa0542-c4a2-4597-9565-e02cec240186] succeeded in 0.002757399925030768s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:58:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[423f9fac-7b84-486d-b266-ac33018b975c] received
[2026-03-29 09:58:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[423f9fac-7b84-486d-b266-ac33018b975c] succeeded in 0.5190334999933839s: {'cpu': 15.9, 'memory': 45.4}
[2026-03-29 09:58:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[deec0465-fe55-495e-bac0-f77c33541762] received
[2026-03-29 09:58:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[deec0465-fe55-495e-bac0-f77c33541762] succeeded in 0.0026671000523492694s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:59:27,083: INFO/MainProcess] Task tasks.scrape_pending_urls[a5c113aa-86e4-4724-8e0a-fd1dd641bd88] received
[2026-03-29 09:59:27,086: INFO/MainProcess] Task tasks.scrape_pending_urls[a5c113aa-86e4-4724-8e0a-fd1dd641bd88] succeeded in 0.002893800032325089s: {'status': 'idle', 'pending': 0}
[2026-03-29 09:59:57,087: INFO/MainProcess] Task tasks.scrape_pending_urls[922b4265-ed71-4fb6-9dd6-559ed4442fde] received
[2026-03-29 09:59:57,090: INFO/MainProcess] Task tasks.scrape_pending_urls[922b4265-ed71-4fb6-9dd6-559ed4442fde] succeeded in 0.002802699920721352s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:00:27,087: INFO/MainProcess] Task tasks.scrape_pending_urls[4473477c-d85a-463b-929c-0ee52c7699b4] received
[2026-03-29 10:00:27,090: INFO/MainProcess] Task tasks.scrape_pending_urls[4473477c-d85a-463b-929c-0ee52c7699b4] succeeded in 0.0026299000019207597s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:00:57,087: INFO/MainProcess] Task tasks.scrape_pending_urls[7200bfbe-b526-40b7-a1d0-737ed856359e] received
[2026-03-29 10:00:57,090: INFO/MainProcess] Task tasks.scrape_pending_urls[7200bfbe-b526-40b7-a1d0-737ed856359e] succeeded in 0.0026277999859303236s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:01:27,086: INFO/MainProcess] Task tasks.scrape_pending_urls[ef1b699d-7bf7-4481-a077-16fefd63c073] received
[2026-03-29 10:01:27,090: INFO/MainProcess] Task tasks.scrape_pending_urls[ef1b699d-7bf7-4481-a077-16fefd63c073] succeeded in 0.0029990000184625387s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:01:57,087: INFO/MainProcess] Task tasks.scrape_pending_urls[204cfe64-bf0e-4b81-a01a-36f43880aedb] received
[2026-03-29 10:01:57,090: INFO/MainProcess] Task tasks.scrape_pending_urls[204cfe64-bf0e-4b81-a01a-36f43880aedb] succeeded in 0.0031472999835386872s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:02:27,087: INFO/MainProcess] Task tasks.scrape_pending_urls[04a2faf5-d376-4385-b2f0-10664133c415] received
[2026-03-29 10:02:27,091: INFO/MainProcess] Task tasks.scrape_pending_urls[04a2faf5-d376-4385-b2f0-10664133c415] succeeded in 0.003825100022368133s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:02:57,087: INFO/MainProcess] Task tasks.scrape_pending_urls[0b78dbc9-d637-40e5-9fe6-cbe42e483326] received
[2026-03-29 10:02:57,091: INFO/MainProcess] Task tasks.scrape_pending_urls[0b78dbc9-d637-40e5-9fe6-cbe42e483326] succeeded in 0.002949999994598329s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:03:27,087: INFO/MainProcess] Task tasks.scrape_pending_urls[499efd60-a78d-4687-9ab5-837a4a82e904] received
[2026-03-29 10:03:27,090: INFO/MainProcess] Task tasks.scrape_pending_urls[499efd60-a78d-4687-9ab5-837a4a82e904] succeeded in 0.0027611999539658427s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:03:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[b1f636e5-855f-44da-a9fb-9c2e979af2fd] received
[2026-03-29 10:03:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[b1f636e5-855f-44da-a9fb-9c2e979af2fd] succeeded in 0.5187449000077322s: {'cpu': 17.8, 'memory': 45.4}
[2026-03-29 10:03:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[f39db7c1-cee6-46dd-8ed3-ae0809020875] received
[2026-03-29 10:03:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[f39db7c1-cee6-46dd-8ed3-ae0809020875] succeeded in 0.002715200069360435s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:04:27,087: INFO/MainProcess] Task tasks.scrape_pending_urls[a7c80ce6-a616-465e-8266-6038c336ef71] received
[2026-03-29 10:04:27,090: INFO/MainProcess] Task tasks.scrape_pending_urls[a7c80ce6-a616-465e-8266-6038c336ef71] succeeded in 0.0026967000449076295s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:04:57,087: INFO/MainProcess] Task tasks.scrape_pending_urls[ec8161af-205f-4467-83a6-00dbba44c9ea] received
[2026-03-29 10:04:57,090: INFO/MainProcess] Task tasks.scrape_pending_urls[ec8161af-205f-4467-83a6-00dbba44c9ea] succeeded in 0.002642399980686605s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:05:27,087: INFO/MainProcess] Task tasks.scrape_pending_urls[1361c036-79b1-4d5b-9262-4543a166eebd] received
[2026-03-29 10:05:27,090: INFO/MainProcess] Task tasks.scrape_pending_urls[1361c036-79b1-4d5b-9262-4543a166eebd] succeeded in 0.002776699955575168s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:05:57,087: INFO/MainProcess] Task tasks.scrape_pending_urls[096ed355-518a-4a76-95af-2c15b19d47a4] received
[2026-03-29 10:05:57,090: INFO/MainProcess] Task tasks.scrape_pending_urls[096ed355-518a-4a76-95af-2c15b19d47a4] succeeded in 0.0025309999473392963s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:06:27,091: INFO/MainProcess] Task tasks.scrape_pending_urls[57cf3226-a461-42cc-acc4-b0d1cafeff1c] received
[2026-03-29 10:06:27,094: INFO/MainProcess] Task tasks.scrape_pending_urls[57cf3226-a461-42cc-acc4-b0d1cafeff1c] succeeded in 0.002628499991260469s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:06:57,091: INFO/MainProcess] Task tasks.scrape_pending_urls[1dbb4288-79df-4140-8448-21f477f5bf79] received
[2026-03-29 10:06:57,094: INFO/MainProcess] Task tasks.scrape_pending_urls[1dbb4288-79df-4140-8448-21f477f5bf79] succeeded in 0.0028566999826580286s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:07:27,092: INFO/MainProcess] Task tasks.scrape_pending_urls[9261e208-da05-4c50-b5d9-1c7d0b964f98] received
[2026-03-29 10:07:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[9261e208-da05-4c50-b5d9-1c7d0b964f98] succeeded in 0.002682299935258925s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:07:57,091: INFO/MainProcess] Task tasks.scrape_pending_urls[8c76185d-996f-4a13-9278-b8463d3337b8] received
[2026-03-29 10:07:57,094: INFO/MainProcess] Task tasks.scrape_pending_urls[8c76185d-996f-4a13-9278-b8463d3337b8] succeeded in 0.0024935000110417604s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:08:27,091: INFO/MainProcess] Task tasks.scrape_pending_urls[0f3b97d7-7770-4aaa-8d29-17448efe3f5b] received
[2026-03-29 10:08:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[0f3b97d7-7770-4aaa-8d29-17448efe3f5b] succeeded in 0.0027520000003278255s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:08:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[21a2bbaf-ec57-4966-b029-19c7b2342e2d] received
[2026-03-29 10:08:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[21a2bbaf-ec57-4966-b029-19c7b2342e2d] succeeded in 0.5167545999865979s: {'cpu': 15.8, 'memory': 45.3}
[2026-03-29 10:08:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[3b872b96-613a-4e7c-b866-7ea25279fe95] received
[2026-03-29 10:08:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[3b872b96-613a-4e7c-b866-7ea25279fe95] succeeded in 0.00266669993288815s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:09:27,091: INFO/MainProcess] Task tasks.scrape_pending_urls[e0e12669-c3b3-48f9-bde5-be737ef98c6b] received
[2026-03-29 10:09:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[e0e12669-c3b3-48f9-bde5-be737ef98c6b] succeeded in 0.002783800009638071s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:09:57,091: INFO/MainProcess] Task tasks.scrape_pending_urls[5389c8e4-1282-4596-90b0-30aecb122fae] received
[2026-03-29 10:09:57,094: INFO/MainProcess] Task tasks.scrape_pending_urls[5389c8e4-1282-4596-90b0-30aecb122fae] succeeded in 0.002701199962757528s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:10:27,092: INFO/MainProcess] Task tasks.scrape_pending_urls[6a668677-3337-40f8-a48e-e21b15617a64] received
[2026-03-29 10:10:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[6a668677-3337-40f8-a48e-e21b15617a64] succeeded in 0.002666899934411049s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:10:57,091: INFO/MainProcess] Task tasks.scrape_pending_urls[02374db6-1eaa-4522-8985-42bfcf728f66] received
[2026-03-29 10:10:57,094: INFO/MainProcess] Task tasks.scrape_pending_urls[02374db6-1eaa-4522-8985-42bfcf728f66] succeeded in 0.002648600027896464s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:11:27,091: INFO/MainProcess] Task tasks.scrape_pending_urls[5043bd61-b6d5-493e-adbd-0da9a533f92d] received
[2026-03-29 10:11:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[5043bd61-b6d5-493e-adbd-0da9a533f92d] succeeded in 0.003251599962823093s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:11:57,091: INFO/MainProcess] Task tasks.scrape_pending_urls[dc155083-b339-44a9-b25e-7030c63386a7] received
[2026-03-29 10:11:57,094: INFO/MainProcess] Task tasks.scrape_pending_urls[dc155083-b339-44a9-b25e-7030c63386a7] succeeded in 0.002714000060223043s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:12:27,092: INFO/MainProcess] Task tasks.scrape_pending_urls[0a3bda49-922f-4322-a920-617188167a9f] received
[2026-03-29 10:12:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[0a3bda49-922f-4322-a920-617188167a9f] succeeded in 0.0026641000295057893s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:12:57,095: INFO/MainProcess] Task tasks.scrape_pending_urls[cb297a29-e26f-4233-89a5-19bfc8b6e881] received
[2026-03-29 10:12:57,098: INFO/MainProcess] Task tasks.scrape_pending_urls[cb297a29-e26f-4233-89a5-19bfc8b6e881] succeeded in 0.002493900014087558s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:13:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[f9dec79f-ac54-4ab8-b146-066475c806e6] received
[2026-03-29 10:13:27,098: INFO/MainProcess] Task tasks.scrape_pending_urls[f9dec79f-ac54-4ab8-b146-066475c806e6] succeeded in 0.0029872999293729663s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:13:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[a5b2a74c-0d87-4a1f-95fc-ec063ea4b3aa] received
[2026-03-29 10:13:56,645: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 10:13:56,646: INFO/MainProcess] Task tasks.reset_stale_processing_urls[a5b2a74c-0d87-4a1f-95fc-ec063ea4b3aa] succeeded in 0.003823600010946393s: {'reset': 0}
[2026-03-29 10:13:56,763: INFO/MainProcess] Task tasks.collect_system_metrics[83b2246c-6140-4304-8fbc-ba4b16158404] received
[2026-03-29 10:13:57,281: INFO/MainProcess] Task tasks.collect_system_metrics[83b2246c-6140-4304-8fbc-ba4b16158404] succeeded in 0.5167708999942988s: {'cpu': 12.9, 'memory': 45.8}
[2026-03-29 10:13:57,282: INFO/MainProcess] Task tasks.scrape_pending_urls[f4aa3120-836a-4f54-a05b-8c66caa72dc0] received
[2026-03-29 10:13:57,285: INFO/MainProcess] Task tasks.scrape_pending_urls[f4aa3120-836a-4f54-a05b-8c66caa72dc0] succeeded in 0.002318799961358309s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:14:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[84126a7b-d6f3-40f5-bc1d-a952f18ceb41] received
[2026-03-29 10:14:27,098: INFO/MainProcess] Task tasks.scrape_pending_urls[84126a7b-d6f3-40f5-bc1d-a952f18ceb41] succeeded in 0.0025408000219613314s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:14:57,095: INFO/MainProcess] Task tasks.scrape_pending_urls[34aec025-065e-462a-9213-f6f19e5348ca] received
[2026-03-29 10:14:57,098: INFO/MainProcess] Task tasks.scrape_pending_urls[34aec025-065e-462a-9213-f6f19e5348ca] succeeded in 0.002544500050134957s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:15:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[abfaa22e-487d-4a61-a0cb-3423e91cedaf] received
[2026-03-29 10:15:27,098: INFO/MainProcess] Task tasks.scrape_pending_urls[abfaa22e-487d-4a61-a0cb-3423e91cedaf] succeeded in 0.0026769000105559826s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:15:57,095: INFO/MainProcess] Task tasks.scrape_pending_urls[8a843e1f-9fa6-48ee-bda2-cc51945e7c36] received
[2026-03-29 10:15:57,099: INFO/MainProcess] Task tasks.scrape_pending_urls[8a843e1f-9fa6-48ee-bda2-cc51945e7c36] succeeded in 0.0031163999810814857s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:16:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[57f317cb-f7f4-42f1-95bd-05cf3c46cbc5] received
[2026-03-29 10:16:27,098: INFO/MainProcess] Task tasks.scrape_pending_urls[57f317cb-f7f4-42f1-95bd-05cf3c46cbc5] succeeded in 0.002642699982970953s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:16:57,095: INFO/MainProcess] Task tasks.scrape_pending_urls[582fb37a-f848-4bf9-8f8b-a3e744ceef51] received
[2026-03-29 10:16:57,098: INFO/MainProcess] Task tasks.scrape_pending_urls[582fb37a-f848-4bf9-8f8b-a3e744ceef51] succeeded in 0.002711100038141012s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:17:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[41b0666d-d240-4e0d-834f-843d9d785716] received
[2026-03-29 10:17:27,098: INFO/MainProcess] Task tasks.scrape_pending_urls[41b0666d-d240-4e0d-834f-843d9d785716] succeeded in 0.0026693999534472823s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:17:57,095: INFO/MainProcess] Task tasks.scrape_pending_urls[3f5e5c42-2549-494e-99ff-603e4412cad8] received
[2026-03-29 10:17:57,098: INFO/MainProcess] Task tasks.scrape_pending_urls[3f5e5c42-2549-494e-99ff-603e4412cad8] succeeded in 0.0025209999876096845s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:18:27,095: INFO/MainProcess] Task tasks.scrape_pending_urls[f5b4fb7d-2463-47ea-b51d-638cacea91ec] received
[2026-03-29 10:18:27,098: INFO/MainProcess] Task tasks.scrape_pending_urls[f5b4fb7d-2463-47ea-b51d-638cacea91ec] succeeded in 0.0026362999342381954s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:18:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[6de47132-b238-40ce-9e66-43977cbf05d8] received
[2026-03-29 10:18:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[6de47132-b238-40ce-9e66-43977cbf05d8] succeeded in 0.516469500027597s: {'cpu': 18.5, 'memory': 45.7}
[2026-03-29 10:18:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[b8cd405f-7db0-47c2-b1c2-85cbeace9622] received
[2026-03-29 10:18:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[b8cd405f-7db0-47c2-b1c2-85cbeace9622] succeeded in 0.0027376998914405704s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:19:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[f9a91fe4-5b64-49bc-a34d-65d5093b2826] received
[2026-03-29 10:19:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[f9a91fe4-5b64-49bc-a34d-65d5093b2826] succeeded in 0.002699999953620136s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:19:57,100: INFO/MainProcess] Task tasks.scrape_pending_urls[05109d76-f230-40c8-92a8-53824fe80b1b] received
[2026-03-29 10:19:57,102: INFO/MainProcess] Task tasks.scrape_pending_urls[05109d76-f230-40c8-92a8-53824fe80b1b] succeeded in 0.002511700033210218s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:20:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[0ba58411-a921-4b0c-8b91-1013d71cc918] received
[2026-03-29 10:20:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[0ba58411-a921-4b0c-8b91-1013d71cc918] succeeded in 0.0025413999101147056s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:20:57,100: INFO/MainProcess] Task tasks.scrape_pending_urls[61ec8487-5e0b-4a23-9235-d980c2cd16b9] received
[2026-03-29 10:20:57,103: INFO/MainProcess] Task tasks.scrape_pending_urls[61ec8487-5e0b-4a23-9235-d980c2cd16b9] succeeded in 0.0026626000180840492s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:21:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[4f0bfd46-f3c9-49dd-995f-97f41b0a984e] received
[2026-03-29 10:21:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[4f0bfd46-f3c9-49dd-995f-97f41b0a984e] succeeded in 0.00274379993788898s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:21:57,100: INFO/MainProcess] Task tasks.scrape_pending_urls[17ea8ea9-6859-490d-8789-48317287277c] received
[2026-03-29 10:21:57,103: INFO/MainProcess] Task tasks.scrape_pending_urls[17ea8ea9-6859-490d-8789-48317287277c] succeeded in 0.0028174000326544046s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:22:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[7939c512-4113-4119-bbc7-938e623d51de] received
[2026-03-29 10:22:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[7939c512-4113-4119-bbc7-938e623d51de] succeeded in 0.0029729000525549054s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:22:57,100: INFO/MainProcess] Task tasks.scrape_pending_urls[1a73f02f-5f3e-4fdf-a6a4-7a4b05e0da3c] received
[2026-03-29 10:22:57,103: INFO/MainProcess] Task tasks.scrape_pending_urls[1a73f02f-5f3e-4fdf-a6a4-7a4b05e0da3c] succeeded in 0.0027414000360295177s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:23:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[83ecd7d3-5497-4879-bd8c-bb77e3597c1a] received
[2026-03-29 10:23:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[83ecd7d3-5497-4879-bd8c-bb77e3597c1a] succeeded in 0.0025204999838024378s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:23:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[90e015a0-3739-41f7-bd21-c25897928c92] received
[2026-03-29 10:23:57,179: INFO/MainProcess] Task tasks.collect_system_metrics[90e015a0-3739-41f7-bd21-c25897928c92] succeeded in 0.5160389000084251s: {'cpu': 10.7, 'memory': 45.6}
[2026-03-29 10:23:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[80126c83-9901-4149-8a30-569d17243c2c] received
[2026-03-29 10:23:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[80126c83-9901-4149-8a30-569d17243c2c] succeeded in 0.0026229999493807554s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:24:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[f76522db-0cba-4d75-a42d-47ea6023a1e9] received
[2026-03-29 10:24:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[f76522db-0cba-4d75-a42d-47ea6023a1e9] succeeded in 0.0026377999456599355s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:24:57,100: INFO/MainProcess] Task tasks.scrape_pending_urls[c315af6c-7514-4302-a4c7-afe685b84ad9] received
[2026-03-29 10:24:57,103: INFO/MainProcess] Task tasks.scrape_pending_urls[c315af6c-7514-4302-a4c7-afe685b84ad9] succeeded in 0.0027001999551430345s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:25:27,100: INFO/MainProcess] Task tasks.scrape_pending_urls[1f2eb83f-9bc4-4c27-8654-708397fea378] received
[2026-03-29 10:25:27,103: INFO/MainProcess] Task tasks.scrape_pending_urls[1f2eb83f-9bc4-4c27-8654-708397fea378] succeeded in 0.0025259999092668295s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:25:57,104: INFO/MainProcess] Task tasks.scrape_pending_urls[64743c87-7487-4226-aa1b-0df5d3dffc8a] received
[2026-03-29 10:25:57,107: INFO/MainProcess] Task tasks.scrape_pending_urls[64743c87-7487-4226-aa1b-0df5d3dffc8a] succeeded in 0.002638000063598156s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:26:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[7772097d-e455-4955-b348-dc0027639309] received
[2026-03-29 10:26:27,107: INFO/MainProcess] Task tasks.scrape_pending_urls[7772097d-e455-4955-b348-dc0027639309] succeeded in 0.0027324999682605267s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:26:57,104: INFO/MainProcess] Task tasks.scrape_pending_urls[c46ceb89-5d5e-4053-88f6-199a0ea4e17f] received
[2026-03-29 10:26:57,107: INFO/MainProcess] Task tasks.scrape_pending_urls[c46ceb89-5d5e-4053-88f6-199a0ea4e17f] succeeded in 0.0027085000183433294s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:27:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[1e4c4b9d-50cb-4bc1-9da7-258cf37906f7] received
[2026-03-29 10:27:27,107: INFO/MainProcess] Task tasks.scrape_pending_urls[1e4c4b9d-50cb-4bc1-9da7-258cf37906f7] succeeded in 0.002792400075122714s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:27:57,104: INFO/MainProcess] Task tasks.scrape_pending_urls[7f61d634-942e-40b0-8852-d12907bceef6] received
[2026-03-29 10:27:57,107: INFO/MainProcess] Task tasks.scrape_pending_urls[7f61d634-942e-40b0-8852-d12907bceef6] succeeded in 0.002722600009292364s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:28:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[c9a82f59-6587-4149-b7bb-ebc8e806dd98] received
[2026-03-29 10:28:27,108: INFO/MainProcess] Task tasks.scrape_pending_urls[c9a82f59-6587-4149-b7bb-ebc8e806dd98] succeeded in 0.0031488999957218766s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:28:56,664: INFO/MainProcess] Task tasks.collect_system_metrics[04546b19-e962-4343-b5f6-2fc6cd7fe098] received
[2026-03-29 10:28:57,169: INFO/MainProcess] Task tasks.collect_system_metrics[04546b19-e962-4343-b5f6-2fc6cd7fe098] succeeded in 0.5052164000226185s: {'cpu': 14.1, 'memory': 45.6}
[2026-03-29 10:28:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[09280dce-eb91-4c63-8acc-4b90661a4721] received
[2026-03-29 10:28:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[09280dce-eb91-4c63-8acc-4b90661a4721] succeeded in 0.0027752999449148774s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:29:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[97e21de3-1406-4712-8108-a2ef153dcabd] received
[2026-03-29 10:29:27,108: INFO/MainProcess] Task tasks.scrape_pending_urls[97e21de3-1406-4712-8108-a2ef153dcabd] succeeded in 0.003137799911201s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:29:57,104: INFO/MainProcess] Task tasks.scrape_pending_urls[e5d6eb18-72fb-4134-86ee-2be540c43cfb] received
[2026-03-29 10:29:57,107: INFO/MainProcess] Task tasks.scrape_pending_urls[e5d6eb18-72fb-4134-86ee-2be540c43cfb] succeeded in 0.0027593999402597547s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[53131ee9-1bde-4251-8e0d-aa322aac56a9] received
[2026-03-29 10:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[53131ee9-1bde-4251-8e0d-aa322aac56a9] succeeded in 0.0013981000520288944s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 10:30:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[35fea59e-d2d2-45f9-9eed-3183044723d0] received
[2026-03-29 10:30:27,107: INFO/MainProcess] Task tasks.scrape_pending_urls[35fea59e-d2d2-45f9-9eed-3183044723d0] succeeded in 0.002521199989132583s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:30:57,104: INFO/MainProcess] Task tasks.scrape_pending_urls[4f2c3283-2577-4409-b581-6d64566440cf] received
[2026-03-29 10:30:57,108: INFO/MainProcess] Task tasks.scrape_pending_urls[4f2c3283-2577-4409-b581-6d64566440cf] succeeded in 0.0031275999499484897s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:31:27,104: INFO/MainProcess] Task tasks.scrape_pending_urls[49e897f0-a267-4b2c-9cff-a24a42e67221] received
[2026-03-29 10:31:27,107: INFO/MainProcess] Task tasks.scrape_pending_urls[49e897f0-a267-4b2c-9cff-a24a42e67221] succeeded in 0.0025286999298259616s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:31:57,104: INFO/MainProcess] Task tasks.scrape_pending_urls[55ba39b4-88a1-4ae0-8fd0-cc6c81fe6d5e] received
[2026-03-29 10:31:57,108: INFO/MainProcess] Task tasks.scrape_pending_urls[55ba39b4-88a1-4ae0-8fd0-cc6c81fe6d5e] succeeded in 0.0027395000215619802s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:32:27,108: INFO/MainProcess] Task tasks.scrape_pending_urls[b106cef6-c24d-4356-b837-b77c4f9f0143] received
[2026-03-29 10:32:27,111: INFO/MainProcess] Task tasks.scrape_pending_urls[b106cef6-c24d-4356-b837-b77c4f9f0143] succeeded in 0.0024884999729692936s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:32:57,108: INFO/MainProcess] Task tasks.scrape_pending_urls[8343ffc5-242b-4621-ad8b-8f5fd826abf2] received
[2026-03-29 10:32:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[8343ffc5-242b-4621-ad8b-8f5fd826abf2] succeeded in 0.0034178000641986728s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:33:27,108: INFO/MainProcess] Task tasks.scrape_pending_urls[99419b9d-c9db-4e2b-9c32-8e6f15f20b25] received
[2026-03-29 10:33:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[99419b9d-c9db-4e2b-9c32-8e6f15f20b25] succeeded in 0.002957899938337505s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:33:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[c24d7d69-b761-41a9-be88-fdce9d2d39b7] received
[2026-03-29 10:33:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[c24d7d69-b761-41a9-be88-fdce9d2d39b7] succeeded in 0.5162086000200361s: {'cpu': 11.2, 'memory': 45.6}
[2026-03-29 10:33:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[eaaa58b0-9a51-4060-9f5f-c350bc19b843] received
[2026-03-29 10:33:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[eaaa58b0-9a51-4060-9f5f-c350bc19b843] succeeded in 0.002674999996088445s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:34:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[f6a68b60-18aa-487a-9bbe-555ec5ece3d5] received
[2026-03-29 10:34:27,113: INFO/MainProcess] Task tasks.scrape_pending_urls[f6a68b60-18aa-487a-9bbe-555ec5ece3d5] succeeded in 0.0036486999597400427s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:34:57,109: INFO/MainProcess] Task tasks.scrape_pending_urls[e70bebd4-c8d4-4c50-b558-57b83ebe0087] received
[2026-03-29 10:34:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[e70bebd4-c8d4-4c50-b558-57b83ebe0087] succeeded in 0.002646600012667477s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:35:27,108: INFO/MainProcess] Task tasks.scrape_pending_urls[b6ba8f54-6f76-4b27-ab34-84107c3adfa6] received
[2026-03-29 10:35:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[b6ba8f54-6f76-4b27-ab34-84107c3adfa6] succeeded in 0.002668399945832789s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:35:57,109: INFO/MainProcess] Task tasks.scrape_pending_urls[88a49cfc-a453-4ff1-a969-aaec964743ab] received
[2026-03-29 10:35:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[88a49cfc-a453-4ff1-a969-aaec964743ab] succeeded in 0.0025447000516578555s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:36:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[547be34f-6808-4c9d-92dc-bdda96795d0e] received
[2026-03-29 10:36:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[547be34f-6808-4c9d-92dc-bdda96795d0e] succeeded in 0.002502300078049302s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:36:57,108: INFO/MainProcess] Task tasks.scrape_pending_urls[786bb407-a9e4-4a05-8fd1-ac795f066902] received
[2026-03-29 10:36:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[786bb407-a9e4-4a05-8fd1-ac795f066902] succeeded in 0.0027774000773206353s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:37:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[9cdac60a-7388-47a5-a6d1-79d24984bd34] received
[2026-03-29 10:37:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[9cdac60a-7388-47a5-a6d1-79d24984bd34] succeeded in 0.0027265000389888883s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:37:57,109: INFO/MainProcess] Task tasks.scrape_pending_urls[43168e2c-b3eb-43f4-b603-7f061ecc5016] received
[2026-03-29 10:37:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[43168e2c-b3eb-43f4-b603-7f061ecc5016] succeeded in 0.002650899928994477s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:38:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[fc6ceaf9-5c24-4d4e-af4e-5e3b5727731a] received
[2026-03-29 10:38:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[fc6ceaf9-5c24-4d4e-af4e-5e3b5727731a] succeeded in 0.0026400000788271427s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:38:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[9c8c1bd4-8889-4ba4-8653-b1a1c42fbcd0] received
[2026-03-29 10:38:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[9c8c1bd4-8889-4ba4-8653-b1a1c42fbcd0] succeeded in 0.5161307000089437s: {'cpu': 10.0, 'memory': 45.4}
[2026-03-29 10:38:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[dafa6124-c678-48eb-aa16-aec4b987cbc7] received
[2026-03-29 10:38:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[dafa6124-c678-48eb-aa16-aec4b987cbc7] succeeded in 0.002710800035856664s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:39:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[4b35cc23-fc67-4c3c-87f7-66d8259daa9e] received
[2026-03-29 10:39:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[4b35cc23-fc67-4c3c-87f7-66d8259daa9e] succeeded in 0.002737100003287196s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:39:57,109: INFO/MainProcess] Task tasks.scrape_pending_urls[5da76642-052d-4d96-a1c2-66abd433293b] received
[2026-03-29 10:39:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[5da76642-052d-4d96-a1c2-66abd433293b] succeeded in 0.0026923000114038587s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:40:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[0a3fe844-dec5-4875-a538-d5489563276d] received
[2026-03-29 10:40:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[0a3fe844-dec5-4875-a538-d5489563276d] succeeded in 0.0025242000119760633s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:40:57,109: INFO/MainProcess] Task tasks.scrape_pending_urls[e8d3e499-4e18-4719-bb36-2277ad960420] received
[2026-03-29 10:40:57,112: INFO/MainProcess] Task tasks.scrape_pending_urls[e8d3e499-4e18-4719-bb36-2277ad960420] succeeded in 0.0025385000044479966s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:41:27,109: INFO/MainProcess] Task tasks.scrape_pending_urls[35a90682-b099-4468-b05c-aaa267875ba9] received
[2026-03-29 10:41:27,112: INFO/MainProcess] Task tasks.scrape_pending_urls[35a90682-b099-4468-b05c-aaa267875ba9] succeeded in 0.002732600085437298s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:41:57,113: INFO/MainProcess] Task tasks.scrape_pending_urls[59b53e06-1d09-40d2-b7e3-653fe42d2409] received
[2026-03-29 10:41:57,116: INFO/MainProcess] Task tasks.scrape_pending_urls[59b53e06-1d09-40d2-b7e3-653fe42d2409] succeeded in 0.002625599969178438s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:42:27,113: INFO/MainProcess] Task tasks.scrape_pending_urls[9fc2dab9-c0e1-4e1e-9124-13d5c3d9f1ee] received
[2026-03-29 10:42:27,116: INFO/MainProcess] Task tasks.scrape_pending_urls[9fc2dab9-c0e1-4e1e-9124-13d5c3d9f1ee] succeeded in 0.002490099985152483s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:42:57,113: INFO/MainProcess] Task tasks.scrape_pending_urls[15b1e076-edab-4a7e-8492-4ec3b2b6899f] received
[2026-03-29 10:42:57,116: INFO/MainProcess] Task tasks.scrape_pending_urls[15b1e076-edab-4a7e-8492-4ec3b2b6899f] succeeded in 0.0025031999684870243s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:43:27,114: INFO/MainProcess] Task tasks.scrape_pending_urls[6ccbb7ad-17cc-43cf-b7e2-b98c15456394] received
[2026-03-29 10:43:27,117: INFO/MainProcess] Task tasks.scrape_pending_urls[6ccbb7ad-17cc-43cf-b7e2-b98c15456394] succeeded in 0.0026684999465942383s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:43:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[7740763c-7f56-442a-b9f2-e822f6f7dda8] received
[2026-03-29 10:43:56,645: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 10:43:56,646: INFO/MainProcess] Task tasks.reset_stale_processing_urls[7740763c-7f56-442a-b9f2-e822f6f7dda8] succeeded in 0.00373070000205189s: {'reset': 0}
[2026-03-29 10:43:56,764: INFO/MainProcess] Task tasks.collect_system_metrics[dee7b5cf-7317-4d7d-808c-e9f6eedf4210] received
[2026-03-29 10:43:57,282: INFO/MainProcess] Task tasks.collect_system_metrics[dee7b5cf-7317-4d7d-808c-e9f6eedf4210] succeeded in 0.5166844999184832s: {'cpu': 13.3, 'memory': 45.6}
[2026-03-29 10:43:57,284: INFO/MainProcess] Task tasks.scrape_pending_urls[acfe21c1-fbef-41d9-a207-4971b397b5ee] received
[2026-03-29 10:43:57,287: INFO/MainProcess] Task tasks.scrape_pending_urls[acfe21c1-fbef-41d9-a207-4971b397b5ee] succeeded in 0.0025252000195905566s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:44:27,113: INFO/MainProcess] Task tasks.scrape_pending_urls[0273a91f-1ba6-4579-ba6a-e349c2c950ab] received
[2026-03-29 10:44:27,116: INFO/MainProcess] Task tasks.scrape_pending_urls[0273a91f-1ba6-4579-ba6a-e349c2c950ab] succeeded in 0.002647400018759072s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:44:57,114: INFO/MainProcess] Task tasks.scrape_pending_urls[eea67e7a-2444-4159-bd02-c951f500198a] received
[2026-03-29 10:44:57,117: INFO/MainProcess] Task tasks.scrape_pending_urls[eea67e7a-2444-4159-bd02-c951f500198a] succeeded in 0.0032019000500440598s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:45:27,113: INFO/MainProcess] Task tasks.scrape_pending_urls[7a3cf8a8-5c1f-4985-a060-ccf0fc99a5fa] received
[2026-03-29 10:45:27,116: INFO/MainProcess] Task tasks.scrape_pending_urls[7a3cf8a8-5c1f-4985-a060-ccf0fc99a5fa] succeeded in 0.0026727999793365598s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:45:57,113: INFO/MainProcess] Task tasks.scrape_pending_urls[7203eaea-882b-4fd8-b57d-05c9e85c96e1] received
[2026-03-29 10:45:57,116: INFO/MainProcess] Task tasks.scrape_pending_urls[7203eaea-882b-4fd8-b57d-05c9e85c96e1] succeeded in 0.00254829996265471s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:46:27,113: INFO/MainProcess] Task tasks.scrape_pending_urls[1f047960-2ef4-4005-bc37-8fc18d4fa54e] received
[2026-03-29 10:46:27,116: INFO/MainProcess] Task tasks.scrape_pending_urls[1f047960-2ef4-4005-bc37-8fc18d4fa54e] succeeded in 0.0026147000025957823s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:46:57,114: INFO/MainProcess] Task tasks.scrape_pending_urls[b5aad878-136f-4ac8-8886-1b7e27fcaef6] received
[2026-03-29 10:46:57,117: INFO/MainProcess] Task tasks.scrape_pending_urls[b5aad878-136f-4ac8-8886-1b7e27fcaef6] succeeded in 0.0027314000762999058s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:47:27,113: INFO/MainProcess] Task tasks.scrape_pending_urls[b6fa0650-b7e7-4381-be1a-8debfe0f280c] received
[2026-03-29 10:47:27,116: INFO/MainProcess] Task tasks.scrape_pending_urls[b6fa0650-b7e7-4381-be1a-8debfe0f280c] succeeded in 0.002614299999549985s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:47:57,113: INFO/MainProcess] Task tasks.scrape_pending_urls[51775afd-7181-4e17-bcee-3010ab02a1cf] received
[2026-03-29 10:47:57,117: INFO/MainProcess] Task tasks.scrape_pending_urls[51775afd-7181-4e17-bcee-3010ab02a1cf] succeeded in 0.0029016999760642648s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:48:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[76d85d4e-d57b-40b8-a31f-fc14b29f650b] received
[2026-03-29 10:48:27,121: INFO/MainProcess] Task tasks.scrape_pending_urls[76d85d4e-d57b-40b8-a31f-fc14b29f650b] succeeded in 0.0026459000073373318s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:48:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[de3bc78a-8629-46c1-b90e-d87c6aa6d746] received
[2026-03-29 10:48:57,169: INFO/MainProcess] Task tasks.collect_system_metrics[de3bc78a-8629-46c1-b90e-d87c6aa6d746] succeeded in 0.5050893001025543s: {'cpu': 11.1, 'memory': 45.7}
[2026-03-29 10:48:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[38c40862-2cd5-4554-9f7a-eae4cf98c456] received
[2026-03-29 10:48:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[38c40862-2cd5-4554-9f7a-eae4cf98c456] succeeded in 0.0031238000374287367s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:49:27,117: INFO/MainProcess] Task tasks.scrape_pending_urls[a58ee7d7-4cf6-4cbb-8f51-9bc80f59f50b] received
[2026-03-29 10:49:27,120: INFO/MainProcess] Task tasks.scrape_pending_urls[a58ee7d7-4cf6-4cbb-8f51-9bc80f59f50b] succeeded in 0.002497200039215386s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:49:57,118: INFO/MainProcess] Task tasks.scrape_pending_urls[35f1df25-36dd-44ce-bdfc-a8091970fc5b] received
[2026-03-29 10:49:57,120: INFO/MainProcess] Task tasks.scrape_pending_urls[35f1df25-36dd-44ce-bdfc-a8091970fc5b] succeeded in 0.0025991000002250075s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:50:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[93b924b2-c225-420b-b8bd-2e13086af3c9] received
[2026-03-29 10:50:27,120: INFO/MainProcess] Task tasks.scrape_pending_urls[93b924b2-c225-420b-b8bd-2e13086af3c9] succeeded in 0.0026695000706240535s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:50:57,118: INFO/MainProcess] Task tasks.scrape_pending_urls[3281797a-01a9-4e8c-a0c9-53d396797abe] received
[2026-03-29 10:50:57,120: INFO/MainProcess] Task tasks.scrape_pending_urls[3281797a-01a9-4e8c-a0c9-53d396797abe] succeeded in 0.0025366999907419086s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:51:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[9799d33f-c529-4329-b68b-cbb2cadf091a] received
[2026-03-29 10:51:27,121: INFO/MainProcess] Task tasks.scrape_pending_urls[9799d33f-c529-4329-b68b-cbb2cadf091a] succeeded in 0.0026814000448212028s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:51:57,117: INFO/MainProcess] Task tasks.scrape_pending_urls[60dfede8-1080-4981-a18a-8043ed492fb3] received
[2026-03-29 10:51:57,120: INFO/MainProcess] Task tasks.scrape_pending_urls[60dfede8-1080-4981-a18a-8043ed492fb3] succeeded in 0.0025077000027522445s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:52:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[1571d9ee-8825-4175-acdd-1612e2816685] received
[2026-03-29 10:52:27,121: INFO/MainProcess] Task tasks.scrape_pending_urls[1571d9ee-8825-4175-acdd-1612e2816685] succeeded in 0.0025599999353289604s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:52:57,118: INFO/MainProcess] Task tasks.scrape_pending_urls[fe618a77-4619-4db0-88c7-e3462a48cb19] received
[2026-03-29 10:52:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[fe618a77-4619-4db0-88c7-e3462a48cb19] succeeded in 0.06368949997704476s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:53:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[d931e0da-873f-473b-8869-ca105e82f676] received
[2026-03-29 10:53:27,182: INFO/MainProcess] Task tasks.scrape_pending_urls[d931e0da-873f-473b-8869-ca105e82f676] succeeded in 0.06398740003351122s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:53:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[5abcca43-2d68-404a-ac18-38cb59f34880] received
[2026-03-29 10:53:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[5abcca43-2d68-404a-ac18-38cb59f34880] succeeded in 0.5160417000297457s: {'cpu': 14.0, 'memory': 45.3}
[2026-03-29 10:53:57,181: INFO/MainProcess] Task tasks.scrape_pending_urls[53ecf583-6285-4f5f-869b-5689cf87efc9] received
[2026-03-29 10:53:57,185: INFO/MainProcess] Task tasks.scrape_pending_urls[53ecf583-6285-4f5f-869b-5689cf87efc9] succeeded in 0.0027676000026986003s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:54:27,118: INFO/MainProcess] Task tasks.scrape_pending_urls[9f157697-6bff-4bb4-b65d-f56feef53a33] received
[2026-03-29 10:54:27,121: INFO/MainProcess] Task tasks.scrape_pending_urls[9f157697-6bff-4bb4-b65d-f56feef53a33] succeeded in 0.0029001999646425247s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:54:57,122: INFO/MainProcess] Task tasks.scrape_pending_urls[649c325d-c032-4010-9a2e-3fbec644b428] received
[2026-03-29 10:54:57,125: INFO/MainProcess] Task tasks.scrape_pending_urls[649c325d-c032-4010-9a2e-3fbec644b428] succeeded in 0.0027230000123381615s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:55:27,122: INFO/MainProcess] Task tasks.scrape_pending_urls[63c82ea0-5d20-4dc4-accc-f9deedc81964] received
[2026-03-29 10:55:27,125: INFO/MainProcess] Task tasks.scrape_pending_urls[63c82ea0-5d20-4dc4-accc-f9deedc81964] succeeded in 0.0026954999193549156s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:55:57,122: INFO/MainProcess] Task tasks.scrape_pending_urls[d49d4f33-dd21-4c36-9b19-a57b59b92932] received
[2026-03-29 10:55:57,126: INFO/MainProcess] Task tasks.scrape_pending_urls[d49d4f33-dd21-4c36-9b19-a57b59b92932] succeeded in 0.0030858999816700816s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:56:27,122: INFO/MainProcess] Task tasks.scrape_pending_urls[72cfb99d-4270-490a-bfd4-328179e223ff] received
[2026-03-29 10:56:27,125: INFO/MainProcess] Task tasks.scrape_pending_urls[72cfb99d-4270-490a-bfd4-328179e223ff] succeeded in 0.0026501999236643314s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:56:57,122: INFO/MainProcess] Task tasks.scrape_pending_urls[207c33f3-13df-486e-8aa3-52ee0a29ce84] received
[2026-03-29 10:56:57,125: INFO/MainProcess] Task tasks.scrape_pending_urls[207c33f3-13df-486e-8aa3-52ee0a29ce84] succeeded in 0.0026946000289171934s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:57:27,123: INFO/MainProcess] Task tasks.scrape_pending_urls[14f535d4-d71c-40f2-9de6-ab2f0e7bdcb2] received
[2026-03-29 10:57:27,126: INFO/MainProcess] Task tasks.scrape_pending_urls[14f535d4-d71c-40f2-9de6-ab2f0e7bdcb2] succeeded in 0.002965099993161857s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:57:57,122: INFO/MainProcess] Task tasks.scrape_pending_urls[18f6a05c-a582-469e-9cce-df60bccb844c] received
[2026-03-29 10:57:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[18f6a05c-a582-469e-9cce-df60bccb844c] succeeded in 0.060991100035607815s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:58:27,122: INFO/MainProcess] Task tasks.scrape_pending_urls[ddc67b98-db12-40b5-b979-e1cddce08fcd] received
[2026-03-29 10:58:27,126: INFO/MainProcess] Task tasks.scrape_pending_urls[ddc67b98-db12-40b5-b979-e1cddce08fcd] succeeded in 0.0031705000437796116s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:58:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[05a7fbd1-12ec-43d2-a8a4-1875313a1987] received
[2026-03-29 10:58:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[05a7fbd1-12ec-43d2-a8a4-1875313a1987] succeeded in 0.5185836999444291s: {'cpu': 10.4, 'memory': 45.4}
[2026-03-29 10:58:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[0fef8645-7aa4-412e-89e9-507056ddb85d] received
[2026-03-29 10:58:57,188: INFO/MainProcess] Task tasks.scrape_pending_urls[0fef8645-7aa4-412e-89e9-507056ddb85d] succeeded in 0.003221500082872808s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:59:27,122: INFO/MainProcess] Task tasks.scrape_pending_urls[b690da21-e87f-43ab-adf3-2043093b3cbb] received
[2026-03-29 10:59:27,125: INFO/MainProcess] Task tasks.scrape_pending_urls[b690da21-e87f-43ab-adf3-2043093b3cbb] succeeded in 0.0029103000415489078s: {'status': 'idle', 'pending': 0}
[2026-03-29 10:59:57,122: INFO/MainProcess] Task tasks.scrape_pending_urls[1320d881-33e9-4e45-8bfa-bc8c28aec724] received
[2026-03-29 10:59:57,125: INFO/MainProcess] Task tasks.scrape_pending_urls[1320d881-33e9-4e45-8bfa-bc8c28aec724] succeeded in 0.002766899997368455s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:00:27,122: INFO/MainProcess] Task tasks.scrape_pending_urls[1fc7f6e3-5075-4649-a67b-271691cc89df] received
[2026-03-29 11:00:27,125: INFO/MainProcess] Task tasks.scrape_pending_urls[1fc7f6e3-5075-4649-a67b-271691cc89df] succeeded in 0.002848300035111606s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:00:57,122: INFO/MainProcess] Task tasks.scrape_pending_urls[933ebaa5-964e-4a9a-b8bd-829b892c1772] received
[2026-03-29 11:00:57,125: INFO/MainProcess] Task tasks.scrape_pending_urls[933ebaa5-964e-4a9a-b8bd-829b892c1772] succeeded in 0.002737700007855892s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:01:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[7b49c072-9635-4629-9acd-0a30dcb9ee35] received
[2026-03-29 11:01:27,130: INFO/MainProcess] Task tasks.scrape_pending_urls[7b49c072-9635-4629-9acd-0a30dcb9ee35] succeeded in 0.002771700033918023s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:01:57,127: INFO/MainProcess] Task tasks.scrape_pending_urls[f47bf8df-51d0-4e6c-bc7e-3dcb3ad8f52d] received
[2026-03-29 11:01:57,130: INFO/MainProcess] Task tasks.scrape_pending_urls[f47bf8df-51d0-4e6c-bc7e-3dcb3ad8f52d] succeeded in 0.002680600038729608s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:02:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[8fae21e2-083b-4e47-bbf8-6a4b765e0ce6] received
[2026-03-29 11:02:27,130: INFO/MainProcess] Task tasks.scrape_pending_urls[8fae21e2-083b-4e47-bbf8-6a4b765e0ce6] succeeded in 0.003272100002504885s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:02:57,127: INFO/MainProcess] Task tasks.scrape_pending_urls[6ae1a2a1-20f8-492a-9cab-3322dc822b13] received
[2026-03-29 11:02:57,130: INFO/MainProcess] Task tasks.scrape_pending_urls[6ae1a2a1-20f8-492a-9cab-3322dc822b13] succeeded in 0.0027935999678447843s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:03:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[9a27ef97-2784-4867-bab5-b00dd75a63fe] received
[2026-03-29 11:03:27,130: INFO/MainProcess] Task tasks.scrape_pending_urls[9a27ef97-2784-4867-bab5-b00dd75a63fe] succeeded in 0.002910400042310357s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:03:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[8607b82a-5a44-4d29-b3fb-5dbd5d525522] received
[2026-03-29 11:03:57,182: INFO/MainProcess] Task tasks.collect_system_metrics[8607b82a-5a44-4d29-b3fb-5dbd5d525522] succeeded in 0.5182535999920219s: {'cpu': 10.4, 'memory': 45.5}
[2026-03-29 11:03:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[5a88e394-e2ab-4613-83b8-c901ef394fe2] received
[2026-03-29 11:03:57,192: INFO/MainProcess] Task tasks.scrape_pending_urls[5a88e394-e2ab-4613-83b8-c901ef394fe2] succeeded in 0.007480100030079484s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:04:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[1b77d095-9d85-49e2-8073-9a48c3ca6bf9] received
[2026-03-29 11:04:27,130: INFO/MainProcess] Task tasks.scrape_pending_urls[1b77d095-9d85-49e2-8073-9a48c3ca6bf9] succeeded in 0.0029899999499320984s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:04:57,127: INFO/MainProcess] Task tasks.scrape_pending_urls[a239c42d-9c1c-4779-b597-ea9d8c881422] received
[2026-03-29 11:04:57,130: INFO/MainProcess] Task tasks.scrape_pending_urls[a239c42d-9c1c-4779-b597-ea9d8c881422] succeeded in 0.002866300055757165s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:05:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[f5f5d051-c049-40e1-ad52-1f774e177c23] received
[2026-03-29 11:05:27,131: INFO/MainProcess] Task tasks.scrape_pending_urls[f5f5d051-c049-40e1-ad52-1f774e177c23] succeeded in 0.0031068000243976712s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:05:57,127: INFO/MainProcess] Task tasks.scrape_pending_urls[41cda1f6-ba2c-4244-a172-bf307c9aefd4] received
[2026-03-29 11:05:57,130: INFO/MainProcess] Task tasks.scrape_pending_urls[41cda1f6-ba2c-4244-a172-bf307c9aefd4] succeeded in 0.0026572999777272344s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:06:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b1d121-29f5-4e44-a6a0-e93e9d5e72bc] received
[2026-03-29 11:06:27,131: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b1d121-29f5-4e44-a6a0-e93e9d5e72bc] succeeded in 0.0031855000415816903s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:06:57,127: INFO/MainProcess] Task tasks.scrape_pending_urls[4804054a-4a87-4f9a-abd1-4f3bc5d9e697] received
[2026-03-29 11:06:57,130: INFO/MainProcess] Task tasks.scrape_pending_urls[4804054a-4a87-4f9a-abd1-4f3bc5d9e697] succeeded in 0.0028387000784277916s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:07:27,127: INFO/MainProcess] Task tasks.scrape_pending_urls[19a60663-9069-4085-94e9-d02b177f1a03] received
[2026-03-29 11:07:27,130: INFO/MainProcess] Task tasks.scrape_pending_urls[19a60663-9069-4085-94e9-d02b177f1a03] succeeded in 0.0028581999940797687s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:07:57,132: INFO/MainProcess] Task tasks.scrape_pending_urls[b8e2f819-8c30-4cd5-92ad-111ba5d7b3b4] received
[2026-03-29 11:07:57,135: INFO/MainProcess] Task tasks.scrape_pending_urls[b8e2f819-8c30-4cd5-92ad-111ba5d7b3b4] succeeded in 0.0026316000148653984s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:08:27,131: INFO/MainProcess] Task tasks.scrape_pending_urls[253c4c7a-2882-459d-83e3-f4bf4b585e93] received
[2026-03-29 11:08:27,134: INFO/MainProcess] Task tasks.scrape_pending_urls[253c4c7a-2882-459d-83e3-f4bf4b585e93] succeeded in 0.002667499938979745s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:08:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[2ab84c22-e12f-4c8b-9550-35b0a974cf0c] received
[2026-03-29 11:08:57,183: INFO/MainProcess] Task tasks.collect_system_metrics[2ab84c22-e12f-4c8b-9550-35b0a974cf0c] succeeded in 0.5190611999714747s: {'cpu': 10.0, 'memory': 45.6}
[2026-03-29 11:08:57,184: INFO/MainProcess] Task tasks.scrape_pending_urls[3864d92d-667b-460f-8fc9-b1710b386ff0] received
[2026-03-29 11:08:57,188: INFO/MainProcess] Task tasks.scrape_pending_urls[3864d92d-667b-460f-8fc9-b1710b386ff0] succeeded in 0.0033164999913424253s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:09:27,131: INFO/MainProcess] Task tasks.scrape_pending_urls[478af63e-2ce7-43c8-a5d9-2702408db9d6] received
[2026-03-29 11:09:27,134: INFO/MainProcess] Task tasks.scrape_pending_urls[478af63e-2ce7-43c8-a5d9-2702408db9d6] succeeded in 0.0025278000393882394s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:09:57,131: INFO/MainProcess] Task tasks.scrape_pending_urls[2c42b382-f93f-4d3f-abe6-4add2a6dc220] received
[2026-03-29 11:09:57,135: INFO/MainProcess] Task tasks.scrape_pending_urls[2c42b382-f93f-4d3f-abe6-4add2a6dc220] succeeded in 0.0027157000731676817s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:10:27,132: INFO/MainProcess] Task tasks.scrape_pending_urls[97a3ac9d-659a-4109-8268-0bed52051975] received
[2026-03-29 11:10:27,135: INFO/MainProcess] Task tasks.scrape_pending_urls[97a3ac9d-659a-4109-8268-0bed52051975] succeeded in 0.0026958000380545855s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:10:57,132: INFO/MainProcess] Task tasks.scrape_pending_urls[9e79727d-ad45-45c1-97bd-c6d41811b238] received
[2026-03-29 11:10:57,135: INFO/MainProcess] Task tasks.scrape_pending_urls[9e79727d-ad45-45c1-97bd-c6d41811b238] succeeded in 0.0033922999864444137s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:11:27,132: INFO/MainProcess] Task tasks.scrape_pending_urls[02d2b849-5660-4cc3-b29e-2fb4e1898698] received
[2026-03-29 11:11:27,135: INFO/MainProcess] Task tasks.scrape_pending_urls[02d2b849-5660-4cc3-b29e-2fb4e1898698] succeeded in 0.002780799986794591s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:11:57,132: INFO/MainProcess] Task tasks.scrape_pending_urls[4a77d866-fed5-4bd4-832f-03c285ae05e4] received
[2026-03-29 11:11:57,135: INFO/MainProcess] Task tasks.scrape_pending_urls[4a77d866-fed5-4bd4-832f-03c285ae05e4] succeeded in 0.0026765000075101852s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:12:27,132: INFO/MainProcess] Task tasks.scrape_pending_urls[c8fc7c82-9304-4750-89d6-b57ac07aa1ad] received
[2026-03-29 11:12:27,135: INFO/MainProcess] Task tasks.scrape_pending_urls[c8fc7c82-9304-4750-89d6-b57ac07aa1ad] succeeded in 0.002490699989721179s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:12:57,131: INFO/MainProcess] Task tasks.scrape_pending_urls[da50093e-036f-482c-8186-9443df6c8a7e] received
[2026-03-29 11:12:57,134: INFO/MainProcess] Task tasks.scrape_pending_urls[da50093e-036f-482c-8186-9443df6c8a7e] succeeded in 0.002548999967984855s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:13:27,132: INFO/MainProcess] Task tasks.scrape_pending_urls[d71e1260-2804-4113-923f-24b64aa2181b] received
[2026-03-29 11:13:27,134: INFO/MainProcess] Task tasks.scrape_pending_urls[d71e1260-2804-4113-923f-24b64aa2181b] succeeded in 0.0024849000619724393s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:13:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[adeb3213-12f5-4713-8aa3-eb35b88121f7] received
[2026-03-29 11:13:56,645: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 11:13:56,646: INFO/MainProcess] Task tasks.reset_stale_processing_urls[adeb3213-12f5-4713-8aa3-eb35b88121f7] succeeded in 0.0036859000101685524s: {'reset': 0}
[2026-03-29 11:13:56,763: INFO/MainProcess] Task tasks.collect_system_metrics[aa09c7b4-5dc8-406a-a93e-b7f352025bf0] received
[2026-03-29 11:13:57,281: INFO/MainProcess] Task tasks.collect_system_metrics[aa09c7b4-5dc8-406a-a93e-b7f352025bf0] succeeded in 0.5170231000520289s: {'cpu': 13.7, 'memory': 45.4}
[2026-03-29 11:13:57,283: INFO/MainProcess] Task tasks.scrape_pending_urls[c8f2dacf-a258-40ea-93f5-0b9e6b85024b] received
[2026-03-29 11:13:57,285: INFO/MainProcess] Task tasks.scrape_pending_urls[c8f2dacf-a258-40ea-93f5-0b9e6b85024b] succeeded in 0.002230099984444678s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:14:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[ae990cdd-5066-4daa-b59f-02660c59a76d] received
[2026-03-29 11:14:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[ae990cdd-5066-4daa-b59f-02660c59a76d] succeeded in 0.00283440004568547s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:14:57,136: INFO/MainProcess] Task tasks.scrape_pending_urls[23d912b4-5bcc-417a-ae95-f7647885664f] received
[2026-03-29 11:14:57,139: INFO/MainProcess] Task tasks.scrape_pending_urls[23d912b4-5bcc-417a-ae95-f7647885664f] succeeded in 0.003329399973154068s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:15:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[21e145b7-a57e-4153-8dbb-a8b7319a0e19] received
[2026-03-29 11:15:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[21e145b7-a57e-4153-8dbb-a8b7319a0e19] succeeded in 0.0025328999618068337s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:15:57,136: INFO/MainProcess] Task tasks.scrape_pending_urls[cd880b21-714c-4bbe-bfad-3a43af1e190c] received
[2026-03-29 11:15:57,139: INFO/MainProcess] Task tasks.scrape_pending_urls[cd880b21-714c-4bbe-bfad-3a43af1e190c] succeeded in 0.0024930000072345138s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:16:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[127e39a9-ecfe-4fb5-b2d3-6c614a9074e0] received
[2026-03-29 11:16:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[127e39a9-ecfe-4fb5-b2d3-6c614a9074e0] succeeded in 0.002494000014849007s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:16:57,136: INFO/MainProcess] Task tasks.scrape_pending_urls[c0f34fe2-9e56-498d-993b-15a6b09e0c89] received
[2026-03-29 11:16:57,139: INFO/MainProcess] Task tasks.scrape_pending_urls[c0f34fe2-9e56-498d-993b-15a6b09e0c89] succeeded in 0.002756600035354495s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:17:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[fa612cf5-3790-4126-ad56-338f4e092b6d] received
[2026-03-29 11:17:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[fa612cf5-3790-4126-ad56-338f4e092b6d] succeeded in 0.0026757000014185905s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:17:57,136: INFO/MainProcess] Task tasks.scrape_pending_urls[ed117fa5-98ca-435a-a0cc-34907f0e1687] received
[2026-03-29 11:17:57,139: INFO/MainProcess] Task tasks.scrape_pending_urls[ed117fa5-98ca-435a-a0cc-34907f0e1687] succeeded in 0.0024759999942034483s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:18:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[3561d16e-18f6-46c9-9312-2045d22b912a] received
[2026-03-29 11:18:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[3561d16e-18f6-46c9-9312-2045d22b912a] succeeded in 0.00250840000808239s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:18:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[3d885748-ec9b-4052-9164-c580274e2d5a] received
[2026-03-29 11:18:57,187: INFO/MainProcess] Task tasks.collect_system_metrics[3d885748-ec9b-4052-9164-c580274e2d5a] succeeded in 0.5237797999288887s: {'cpu': 19.3, 'memory': 45.6}
[2026-03-29 11:18:57,189: INFO/MainProcess] Task tasks.scrape_pending_urls[9cc31f91-9290-44af-8cf4-be721dc233c6] received
[2026-03-29 11:18:57,192: INFO/MainProcess] Task tasks.scrape_pending_urls[9cc31f91-9290-44af-8cf4-be721dc233c6] succeeded in 0.0029458999633789062s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:19:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[f6f1e456-402d-43a6-9469-ad8d858cf476] received
[2026-03-29 11:19:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[f6f1e456-402d-43a6-9469-ad8d858cf476] succeeded in 0.0027245000237599015s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:19:57,136: INFO/MainProcess] Task tasks.scrape_pending_urls[9bea83d6-817b-4b64-8db9-d367bf15a476] received
[2026-03-29 11:19:57,139: INFO/MainProcess] Task tasks.scrape_pending_urls[9bea83d6-817b-4b64-8db9-d367bf15a476] succeeded in 0.003047799924388528s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:20:27,136: INFO/MainProcess] Task tasks.scrape_pending_urls[48f49737-2694-459f-8ca9-9d774af586ae] received
[2026-03-29 11:20:27,139: INFO/MainProcess] Task tasks.scrape_pending_urls[48f49737-2694-459f-8ca9-9d774af586ae] succeeded in 0.002696799929253757s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:20:57,141: INFO/MainProcess] Task tasks.scrape_pending_urls[9cfe101c-5e7c-475b-8eee-1cff1b741d5c] received
[2026-03-29 11:20:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[9cfe101c-5e7c-475b-8eee-1cff1b741d5c] succeeded in 0.0036957000847905874s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:21:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[2323d2c1-bb89-4447-a298-fbdea1cd6c77] received
[2026-03-29 11:21:27,144: INFO/MainProcess] Task tasks.scrape_pending_urls[2323d2c1-bb89-4447-a298-fbdea1cd6c77] succeeded in 0.0029757999582216144s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:21:57,141: INFO/MainProcess] Task tasks.scrape_pending_urls[17cfe500-5e6a-4482-a6de-c5b3f673aef6] received
[2026-03-29 11:21:57,144: INFO/MainProcess] Task tasks.scrape_pending_urls[17cfe500-5e6a-4482-a6de-c5b3f673aef6] succeeded in 0.002709600026719272s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:22:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[009d36d9-7959-44f1-9afc-0bfea98d2d6d] received
[2026-03-29 11:22:27,144: INFO/MainProcess] Task tasks.scrape_pending_urls[009d36d9-7959-44f1-9afc-0bfea98d2d6d] succeeded in 0.0025458999443799257s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:22:57,141: INFO/MainProcess] Task tasks.scrape_pending_urls[a84adc28-8582-4b3e-b9e2-07b9f9456cb1] received
[2026-03-29 11:22:57,144: INFO/MainProcess] Task tasks.scrape_pending_urls[a84adc28-8582-4b3e-b9e2-07b9f9456cb1] succeeded in 0.0026008998975157738s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:23:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[67dd34b4-af35-4c3c-8b33-23c0c509366e] received
[2026-03-29 11:23:27,144: INFO/MainProcess] Task tasks.scrape_pending_urls[67dd34b4-af35-4c3c-8b33-23c0c509366e] succeeded in 0.0027305000694468617s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:23:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[34b67843-0b70-4d37-bb8f-c3be19cef559] received
[2026-03-29 11:23:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[34b67843-0b70-4d37-bb8f-c3be19cef559] succeeded in 0.5063465000130236s: {'cpu': 17.6, 'memory': 45.4}
[2026-03-29 11:23:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[3f316461-992a-45ca-a19c-1d991d0a379e] received
[2026-03-29 11:23:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[3f316461-992a-45ca-a19c-1d991d0a379e] succeeded in 0.0027522000018507242s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:24:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[4b43da97-01fb-4f0e-8ded-646337462ca7] received
[2026-03-29 11:24:27,144: INFO/MainProcess] Task tasks.scrape_pending_urls[4b43da97-01fb-4f0e-8ded-646337462ca7] succeeded in 0.0030486000468954444s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:24:57,141: INFO/MainProcess] Task tasks.scrape_pending_urls[cd78c4fd-2d45-4906-a77e-173d16c861af] received
[2026-03-29 11:24:57,144: INFO/MainProcess] Task tasks.scrape_pending_urls[cd78c4fd-2d45-4906-a77e-173d16c861af] succeeded in 0.0025328999618068337s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:25:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[53c99153-bdf3-490a-a952-f4def9252e92] received
[2026-03-29 11:25:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[53c99153-bdf3-490a-a952-f4def9252e92] succeeded in 0.0032273000106215477s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:25:57,141: INFO/MainProcess] Task tasks.scrape_pending_urls[4c027e1f-9ffd-492b-892d-e6b8a8d93c6c] received
[2026-03-29 11:25:57,144: INFO/MainProcess] Task tasks.scrape_pending_urls[4c027e1f-9ffd-492b-892d-e6b8a8d93c6c] succeeded in 0.002835600054822862s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:26:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[531b8c8b-3854-4c3e-a451-ba1813bc54fb] received
[2026-03-29 11:26:27,144: INFO/MainProcess] Task tasks.scrape_pending_urls[531b8c8b-3854-4c3e-a451-ba1813bc54fb] succeeded in 0.002814800012856722s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:26:57,143: INFO/MainProcess] Task tasks.scrape_pending_urls[760f61ad-1b81-48ef-b3d0-11ff943104d4] received
[2026-03-29 11:26:57,148: INFO/MainProcess] Task tasks.scrape_pending_urls[760f61ad-1b81-48ef-b3d0-11ff943104d4] succeeded in 0.004665000014938414s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:27:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[66b54b85-5a98-4b51-a62d-7b9f1907ebfa] received
[2026-03-29 11:27:27,146: INFO/MainProcess] Task tasks.scrape_pending_urls[66b54b85-5a98-4b51-a62d-7b9f1907ebfa] succeeded in 0.004369699978269637s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:27:57,142: INFO/MainProcess] Task tasks.scrape_pending_urls[72b37592-4907-49f5-88d2-342f490a4a59] received
[2026-03-29 11:27:57,146: INFO/MainProcess] Task tasks.scrape_pending_urls[72b37592-4907-49f5-88d2-342f490a4a59] succeeded in 0.004137699957937002s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:28:27,141: INFO/MainProcess] Task tasks.scrape_pending_urls[d9216fb3-9439-4c6c-b6bb-d6a97c0af9d4] received
[2026-03-29 11:28:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[d9216fb3-9439-4c6c-b6bb-d6a97c0af9d4] succeeded in 0.0027591000543907285s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:28:56,663: INFO/MainProcess] Task tasks.collect_system_metrics[08e3547b-cd56-48bf-8bb0-ffe3c9377432] received
[2026-03-29 11:28:57,170: INFO/MainProcess] Task tasks.collect_system_metrics[08e3547b-cd56-48bf-8bb0-ffe3c9377432] succeeded in 0.5060903000412509s: {'cpu': 14.0, 'memory': 45.8}
[2026-03-29 11:28:57,173: INFO/MainProcess] Task tasks.scrape_pending_urls[1d2405bc-510a-4835-affd-d087a295c84f] received
[2026-03-29 11:28:57,177: INFO/MainProcess] Task tasks.scrape_pending_urls[1d2405bc-510a-4835-affd-d087a295c84f] succeeded in 0.003423499991185963s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:29:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[02370e6e-8df9-4639-947a-e778a42f253f] received
[2026-03-29 11:29:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[02370e6e-8df9-4639-947a-e778a42f253f] succeeded in 0.0026870000874623656s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:29:57,141: INFO/MainProcess] Task tasks.scrape_pending_urls[47163800-e995-4567-aea6-8f927c676f92] received
[2026-03-29 11:29:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[47163800-e995-4567-aea6-8f927c676f92] succeeded in 0.0029221000149846077s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[587b244b-1ae5-4288-9df3-ae133e520822] received
[2026-03-29 11:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[587b244b-1ae5-4288-9df3-ae133e520822] succeeded in 0.0013593999901786447s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 11:30:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[e5071b42-3c73-4bc5-b8d5-5a2a8a5a7a92] received
[2026-03-29 11:30:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[e5071b42-3c73-4bc5-b8d5-5a2a8a5a7a92] succeeded in 0.003074800013564527s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:30:57,142: INFO/MainProcess] Task tasks.scrape_pending_urls[3bf78c90-ee7b-4b6c-b755-6932d09d541f] received
[2026-03-29 11:30:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[3bf78c90-ee7b-4b6c-b755-6932d09d541f] succeeded in 0.0030629000393673778s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:31:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[a04d1713-da7f-4a9f-a80c-08ff933eff28] received
[2026-03-29 11:31:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[a04d1713-da7f-4a9f-a80c-08ff933eff28] succeeded in 0.0030481999274343252s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:31:57,142: INFO/MainProcess] Task tasks.scrape_pending_urls[d36a8be1-d952-4baa-aa65-64ef78a1a83c] received
[2026-03-29 11:31:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[d36a8be1-d952-4baa-aa65-64ef78a1a83c] succeeded in 0.0031390999210998416s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:32:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[bec753de-cdec-47fb-9c59-88a8dadbeb75] received
[2026-03-29 11:32:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[bec753de-cdec-47fb-9c59-88a8dadbeb75] succeeded in 0.002890900010243058s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:32:57,142: INFO/MainProcess] Task tasks.scrape_pending_urls[f16e849c-e0cb-43b4-a147-2fa2bdccd656] received
[2026-03-29 11:32:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[f16e849c-e0cb-43b4-a147-2fa2bdccd656] succeeded in 0.0029153000796213746s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:33:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[f0db24d4-323e-4f38-8143-ec8e0cbd6aa3] received
[2026-03-29 11:33:27,146: INFO/MainProcess] Task tasks.scrape_pending_urls[f0db24d4-323e-4f38-8143-ec8e0cbd6aa3] succeeded in 0.0035131999757140875s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:33:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[89ff9032-b6fe-4afa-9b7d-f46ff0ad56be] received
[2026-03-29 11:33:57,185: INFO/MainProcess] Task tasks.collect_system_metrics[89ff9032-b6fe-4afa-9b7d-f46ff0ad56be] succeeded in 0.5172941000200808s: {'cpu': 27.9, 'memory': 45.5}
[2026-03-29 11:33:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[1857e0b3-25bf-4a52-9c1d-db69179a48ae] received
[2026-03-29 11:33:57,191: INFO/MainProcess] Task tasks.scrape_pending_urls[1857e0b3-25bf-4a52-9c1d-db69179a48ae] succeeded in 0.0035649000201374292s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:34:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[c3b5e99d-98a1-42ea-b825-975ee75e3592] received
[2026-03-29 11:34:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[c3b5e99d-98a1-42ea-b825-975ee75e3592] succeeded in 0.00277520006056875s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:34:57,142: INFO/MainProcess] Task tasks.scrape_pending_urls[d591a00e-e267-470a-9175-aa304929cf16] received
[2026-03-29 11:34:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[d591a00e-e267-470a-9175-aa304929cf16] succeeded in 0.003165900008752942s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:35:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[008b1175-afb2-426f-89ba-87cc7aca83ba] received
[2026-03-29 11:35:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[008b1175-afb2-426f-89ba-87cc7aca83ba] succeeded in 0.002868399955332279s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:35:57,142: INFO/MainProcess] Task tasks.scrape_pending_urls[130bfc53-0f07-4dcf-a698-99ee64cefc4e] received
[2026-03-29 11:35:57,146: INFO/MainProcess] Task tasks.scrape_pending_urls[130bfc53-0f07-4dcf-a698-99ee64cefc4e] succeeded in 0.003131299978122115s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:36:27,142: INFO/MainProcess] Task tasks.scrape_pending_urls[b7171d2e-0667-448b-9bbb-b8375e49af69] received
[2026-03-29 11:36:27,146: INFO/MainProcess] Task tasks.scrape_pending_urls[b7171d2e-0667-448b-9bbb-b8375e49af69] succeeded in 0.0031895999563857913s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:36:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[6f4445a8-b3f8-4c70-b8b9-66b2cda877cf] received
[2026-03-29 11:36:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[6f4445a8-b3f8-4c70-b8b9-66b2cda877cf] succeeded in 0.002996399998664856s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:37:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[e1992392-bddf-4358-b070-0a882009c4a8] received
[2026-03-29 11:37:27,148: INFO/MainProcess] Task tasks.scrape_pending_urls[e1992392-bddf-4358-b070-0a882009c4a8] succeeded in 0.0030399999814108014s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:37:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[b5ea1868-9c39-46d4-a3fc-f40dac159fd3] received
[2026-03-29 11:37:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[b5ea1868-9c39-46d4-a3fc-f40dac159fd3] succeeded in 0.0031027999939396977s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:38:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[514f8200-c303-4126-acbe-12838fa185db] received
[2026-03-29 11:38:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[514f8200-c303-4126-acbe-12838fa185db] succeeded in 0.0032610000343993306s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:38:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[6b687ea7-82a6-46a9-8eb6-7f55d317e165] received
[2026-03-29 11:38:57,185: INFO/MainProcess] Task tasks.collect_system_metrics[6b687ea7-82a6-46a9-8eb6-7f55d317e165] succeeded in 0.5171929999487475s: {'cpu': 24.2, 'memory': 45.6}
[2026-03-29 11:38:57,186: INFO/MainProcess] Task tasks.scrape_pending_urls[99c136ef-491e-458d-8264-c5e6507e83d2] received
[2026-03-29 11:38:57,191: INFO/MainProcess] Task tasks.scrape_pending_urls[99c136ef-491e-458d-8264-c5e6507e83d2] succeeded in 0.0035439999774098396s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:39:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[27c8b75b-ce48-435a-94f9-04d115778217] received
[2026-03-29 11:39:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[27c8b75b-ce48-435a-94f9-04d115778217] succeeded in 0.0035693999379873276s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:39:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[15928d71-dcf1-4877-97d0-9a116397fde1] received
[2026-03-29 11:39:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[15928d71-dcf1-4877-97d0-9a116397fde1] succeeded in 0.0031254999339580536s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:40:27,145: INFO/MainProcess] Task tasks.scrape_pending_urls[200b7f90-372b-410b-8a34-34833de9ba46] received
[2026-03-29 11:40:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[200b7f90-372b-410b-8a34-34833de9ba46] succeeded in 0.0029137999517843127s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:40:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[1edbcaf1-55cc-4be7-b10a-e87b9680485f] received
[2026-03-29 11:40:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[1edbcaf1-55cc-4be7-b10a-e87b9680485f] succeeded in 0.0031349000055342913s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:41:27,146: INFO/MainProcess] Task tasks.scrape_pending_urls[67319691-fb90-4847-a818-a70250a05126] received
[2026-03-29 11:41:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[67319691-fb90-4847-a818-a70250a05126] succeeded in 0.002840599976480007s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:41:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[da8b4864-b046-4573-8753-0d9db9e6a49d] received
[2026-03-29 11:41:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[da8b4864-b046-4573-8753-0d9db9e6a49d] succeeded in 0.002873999997973442s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:42:27,146: INFO/MainProcess] Task tasks.scrape_pending_urls[68d5d409-e1cb-4d0b-b222-01b61a1dad22] received
[2026-03-29 11:42:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[68d5d409-e1cb-4d0b-b222-01b61a1dad22] succeeded in 0.003113799961283803s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:42:57,145: INFO/MainProcess] Task tasks.scrape_pending_urls[d47c1273-e007-4df2-86e9-24331af30963] received
[2026-03-29 11:42:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[d47c1273-e007-4df2-86e9-24331af30963] succeeded in 0.0034206999698653817s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:43:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[4461519c-9f7c-40ba-99b1-afc3a77d4135] received
[2026-03-29 11:43:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[4461519c-9f7c-40ba-99b1-afc3a77d4135] succeeded in 0.00301360001321882s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:43:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[f2c3440c-b195-45ac-ab60-f8a515d61d8f] received
[2026-03-29 11:43:56,646: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 11:43:56,647: INFO/MainProcess] Task tasks.reset_stale_processing_urls[f2c3440c-b195-45ac-ab60-f8a515d61d8f] succeeded in 0.003979999921284616s: {'reset': 0}
[2026-03-29 11:43:56,666: INFO/MainProcess] Task tasks.collect_system_metrics[55dce205-031b-4268-b2b2-86eef6b630e2] received
[2026-03-29 11:43:57,281: INFO/MainProcess] Task tasks.collect_system_metrics[55dce205-031b-4268-b2b2-86eef6b630e2] succeeded in 0.5180191000690684s: {'cpu': 32.2, 'memory': 45.5}
[2026-03-29 11:43:57,283: INFO/MainProcess] Task tasks.scrape_pending_urls[0c0e3cfb-bb07-4a5f-998e-81e747854aa1] received
[2026-03-29 11:43:57,287: INFO/MainProcess] Task tasks.scrape_pending_urls[0c0e3cfb-bb07-4a5f-998e-81e747854aa1] succeeded in 0.0033117999555543065s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:44:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[f78c466a-6fee-4acb-8a0e-fda708cddb6d] received
[2026-03-29 11:44:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[f78c466a-6fee-4acb-8a0e-fda708cddb6d] succeeded in 0.0034558000043034554s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:44:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[f750531a-84c5-474f-a95c-e921630ad9b7] received
[2026-03-29 11:44:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[f750531a-84c5-474f-a95c-e921630ad9b7] succeeded in 0.0031180999940261245s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:45:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[fc057c83-f3f6-4a11-8256-a0f18ca4dfba] received
[2026-03-29 11:45:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[fc057c83-f3f6-4a11-8256-a0f18ca4dfba] succeeded in 0.002965599996969104s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:45:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[edaeb481-f5d8-4999-9338-94890de74d1b] received
[2026-03-29 11:45:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[edaeb481-f5d8-4999-9338-94890de74d1b] succeeded in 0.0029699000297114253s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:46:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[3eff1e8a-f9e4-4760-a836-f2725ccc5348] received
[2026-03-29 11:46:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[3eff1e8a-f9e4-4760-a836-f2725ccc5348] succeeded in 0.003482899977825582s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:46:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[fc442049-661a-456c-93ad-aef0dd7246e9] received
[2026-03-29 11:46:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[fc442049-661a-456c-93ad-aef0dd7246e9] succeeded in 0.0029790999833494425s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:47:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[457f5fef-097d-4500-9e56-f6a9ad7bcba3] received
[2026-03-29 11:47:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[457f5fef-097d-4500-9e56-f6a9ad7bcba3] succeeded in 0.003251100075431168s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:47:57,149: INFO/MainProcess] Task tasks.scrape_pending_urls[337cb625-f0f8-4d05-a8ad-ea67f09487b1] received
[2026-03-29 11:47:57,153: INFO/MainProcess] Task tasks.scrape_pending_urls[337cb625-f0f8-4d05-a8ad-ea67f09487b1] succeeded in 0.00351429998409003s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:48:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[78936186-4d65-4529-848f-7976d1619600] received
[2026-03-29 11:48:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[78936186-4d65-4529-848f-7976d1619600] succeeded in 0.0027930999640375376s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:48:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[b705f24d-76d6-4258-bec5-44718eb3af95] received
[2026-03-29 11:48:57,185: INFO/MainProcess] Task tasks.collect_system_metrics[b705f24d-76d6-4258-bec5-44718eb3af95] succeeded in 0.5172112000873312s: {'cpu': 23.0, 'memory': 45.7}
[2026-03-29 11:48:57,186: INFO/MainProcess] Task tasks.scrape_pending_urls[47054492-9bdc-4c83-88d2-5887abbb6549] received
[2026-03-29 11:48:57,190: INFO/MainProcess] Task tasks.scrape_pending_urls[47054492-9bdc-4c83-88d2-5887abbb6549] succeeded in 0.0029980000108480453s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:49:27,149: INFO/MainProcess] Task tasks.scrape_pending_urls[c69a5d63-1cb5-4de7-9458-8f9d8135e7c9] received
[2026-03-29 11:49:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[c69a5d63-1cb5-4de7-9458-8f9d8135e7c9] succeeded in 0.003198099904693663s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:49:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[893c5032-bd6d-4be0-a80c-e6c103c64169] received
[2026-03-29 11:49:57,155: INFO/MainProcess] Task tasks.scrape_pending_urls[893c5032-bd6d-4be0-a80c-e6c103c64169] succeeded in 0.0030768000287935138s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:50:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[be9b5c77-d97e-4887-8d1e-ad95bf215121] received
[2026-03-29 11:50:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[be9b5c77-d97e-4887-8d1e-ad95bf215121] succeeded in 0.0031759999692440033s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:50:57,153: INFO/MainProcess] Task tasks.scrape_pending_urls[9572666b-04f4-41df-b115-3666228f1193] received
[2026-03-29 11:50:57,157: INFO/MainProcess] Task tasks.scrape_pending_urls[9572666b-04f4-41df-b115-3666228f1193] succeeded in 0.003410500008612871s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:51:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[537bf032-64e0-4e60-bad2-efb5219fbfec] received
[2026-03-29 11:51:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[537bf032-64e0-4e60-bad2-efb5219fbfec] succeeded in 0.0033785999985411763s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:51:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[91b1b669-0ac2-4ec5-b93c-2f352e3d4f56] received
[2026-03-29 11:51:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[91b1b669-0ac2-4ec5-b93c-2f352e3d4f56] succeeded in 0.003295400063507259s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:52:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[371d5402-5cb5-411c-af58-1cf02d8e2ce1] received
[2026-03-29 11:52:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[371d5402-5cb5-411c-af58-1cf02d8e2ce1] succeeded in 0.003049100050702691s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:52:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[cf0fd596-ef71-4201-9be9-2aae43aaf6aa] received
[2026-03-29 11:52:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[cf0fd596-ef71-4201-9be9-2aae43aaf6aa] succeeded in 0.0030740000074729323s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:53:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[2b8f31de-d7c5-4cfd-b72b-52fb97035a68] received
[2026-03-29 11:53:27,225: INFO/MainProcess] Task tasks.scrape_pending_urls[2b8f31de-d7c5-4cfd-b72b-52fb97035a68] succeeded in 0.07217189995571971s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:53:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[c4597fc3-b6fb-4a81-925a-e00dbb8aacb5] received
[2026-03-29 11:53:57,251: INFO/MainProcess] Task tasks.collect_system_metrics[c4597fc3-b6fb-4a81-925a-e00dbb8aacb5] succeeded in 0.5833266999106854s: {'cpu': 25.8, 'memory': 45.4}
[2026-03-29 11:53:57,253: INFO/MainProcess] Task tasks.scrape_pending_urls[7feae13a-8e0c-491b-84d2-34e272b7dad8] received
[2026-03-29 11:53:57,257: INFO/MainProcess] Task tasks.scrape_pending_urls[7feae13a-8e0c-491b-84d2-34e272b7dad8] succeeded in 0.003230100031942129s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:54:27,153: INFO/MainProcess] Task tasks.scrape_pending_urls[06e91419-3d20-4e4a-a16a-c80df20d6c14] received
[2026-03-29 11:54:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[06e91419-3d20-4e4a-a16a-c80df20d6c14] succeeded in 0.0034739000257104635s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:54:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[52c013c6-bf3b-428a-a497-215227c55d86] received
[2026-03-29 11:54:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[52c013c6-bf3b-428a-a497-215227c55d86] succeeded in 0.003353400039486587s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:55:27,152: INFO/MainProcess] Task tasks.scrape_pending_urls[53e63c76-979e-49ff-8894-3c6c1b7b5a75] received
[2026-03-29 11:55:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[53e63c76-979e-49ff-8894-3c6c1b7b5a75] succeeded in 0.0028439000016078353s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:55:57,152: INFO/MainProcess] Task tasks.scrape_pending_urls[8986a3a4-8463-4521-99af-68d38d8ede93] received
[2026-03-29 11:55:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[8986a3a4-8463-4521-99af-68d38d8ede93] succeeded in 0.0033280999632552266s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:56:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[92e66f84-b069-40fa-a859-ef67fd7f3ecf] received
[2026-03-29 11:56:27,159: INFO/MainProcess] Task tasks.scrape_pending_urls[92e66f84-b069-40fa-a859-ef67fd7f3ecf] succeeded in 0.003295699949376285s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:56:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[4d071d05-33d0-49c0-a2c7-c251dedec491] received
[2026-03-29 11:56:57,159: INFO/MainProcess] Task tasks.scrape_pending_urls[4d071d05-33d0-49c0-a2c7-c251dedec491] succeeded in 0.0031642999965697527s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:57:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[5e64404b-d25f-4405-bb43-fad4b18ce303] received
[2026-03-29 11:57:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[5e64404b-d25f-4405-bb43-fad4b18ce303] succeeded in 0.003855000017210841s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:57:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[788177dd-4d2c-48eb-ac28-a6b3d51de91d] received
[2026-03-29 11:57:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[788177dd-4d2c-48eb-ac28-a6b3d51de91d] succeeded in 0.0034073999850079417s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:58:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[93ddca3c-38f0-4132-b40f-bec263ac025b] received
[2026-03-29 11:58:27,231: INFO/MainProcess] Task tasks.scrape_pending_urls[93ddca3c-38f0-4132-b40f-bec263ac025b] succeeded in 0.07538609998300672s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:58:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[dcd64574-8dde-447e-ad73-9732f1f2ce91] received
[2026-03-29 11:58:57,187: INFO/MainProcess] Task tasks.collect_system_metrics[dcd64574-8dde-447e-ad73-9732f1f2ce91] succeeded in 0.5191744000185281s: {'cpu': 28.7, 'memory': 45.5}
[2026-03-29 11:58:57,189: INFO/MainProcess] Task tasks.scrape_pending_urls[b2bfbd98-e1a7-4d38-86c3-9f9c627a9849] received
[2026-03-29 11:58:57,193: INFO/MainProcess] Task tasks.scrape_pending_urls[b2bfbd98-e1a7-4d38-86c3-9f9c627a9849] succeeded in 0.0035339000169187784s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:59:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[c82c1f4a-d9b0-4414-9ff7-d1903cb9e039] received
[2026-03-29 11:59:27,159: INFO/MainProcess] Task tasks.scrape_pending_urls[c82c1f4a-d9b0-4414-9ff7-d1903cb9e039] succeeded in 0.003052599960938096s: {'status': 'idle', 'pending': 0}
[2026-03-29 11:59:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[9f23bb79-8a3a-4d25-a74c-bada7a793473] received
[2026-03-29 11:59:57,159: INFO/MainProcess] Task tasks.scrape_pending_urls[9f23bb79-8a3a-4d25-a74c-bada7a793473] succeeded in 0.0029269999358803034s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:00:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[68f8c744-1a23-4460-838b-d743be9e902b] received
[2026-03-29 12:00:27,159: INFO/MainProcess] Task tasks.scrape_pending_urls[68f8c744-1a23-4460-838b-d743be9e902b] succeeded in 0.003241900005377829s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:00:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[e8538a5c-e8a7-4f8e-8ddc-e26ba252a254] received
[2026-03-29 12:00:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[e8538a5c-e8a7-4f8e-8ddc-e26ba252a254] succeeded in 0.0034796000691130757s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:01:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[5db02dfc-2e3c-4e46-a310-4d9165509aa3] received
[2026-03-29 12:01:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[5db02dfc-2e3c-4e46-a310-4d9165509aa3] succeeded in 0.003180100000463426s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:01:57,156: INFO/MainProcess] Task tasks.scrape_pending_urls[e281634e-1c77-4716-b323-bd7949cf4735] received
[2026-03-29 12:01:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[e281634e-1c77-4716-b323-bd7949cf4735] succeeded in 0.0035882999654859304s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:02:27,156: INFO/MainProcess] Task tasks.scrape_pending_urls[ab580a70-79c6-4b1a-bfb7-07359185e0ec] received
[2026-03-29 12:02:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[ab580a70-79c6-4b1a-bfb7-07359185e0ec] succeeded in 0.00359590002335608s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:02:57,159: INFO/MainProcess] Task tasks.scrape_pending_urls[8e2b273c-b545-4b62-a547-d2493e96630c] received
[2026-03-29 12:02:57,163: INFO/MainProcess] Task tasks.scrape_pending_urls[8e2b273c-b545-4b62-a547-d2493e96630c] succeeded in 0.0032851999858394265s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:03:27,159: INFO/MainProcess] Task tasks.scrape_pending_urls[97b9a342-dea3-443e-a07d-90bebc214284] received
[2026-03-29 12:03:27,163: INFO/MainProcess] Task tasks.scrape_pending_urls[97b9a342-dea3-443e-a07d-90bebc214284] succeeded in 0.0033364000264555216s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:03:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[4e411e23-1260-4680-98c8-d8fe024ad472] received
[2026-03-29 12:03:57,187: INFO/MainProcess] Task tasks.collect_system_metrics[4e411e23-1260-4680-98c8-d8fe024ad472] succeeded in 0.51967860001605s: {'cpu': 24.4, 'memory': 45.5}
[2026-03-29 12:03:57,189: INFO/MainProcess] Task tasks.scrape_pending_urls[15ea4017-0a0e-477e-9f47-67e12eae0f1e] received
[2026-03-29 12:03:57,193: INFO/MainProcess] Task tasks.scrape_pending_urls[15ea4017-0a0e-477e-9f47-67e12eae0f1e] succeeded in 0.0037368000485002995s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:04:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[c4169733-badf-496e-af17-c4d9cf146f1f] received
[2026-03-29 12:04:27,163: INFO/MainProcess] Task tasks.scrape_pending_urls[c4169733-badf-496e-af17-c4d9cf146f1f] succeeded in 0.003346199984662235s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:04:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[a6cb23be-7f23-42db-ac44-22c89d458c38] received
[2026-03-29 12:04:57,163: INFO/MainProcess] Task tasks.scrape_pending_urls[a6cb23be-7f23-42db-ac44-22c89d458c38] succeeded in 0.003068799967877567s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:05:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[4e77cf0c-bff7-42de-85d3-a3bd5059d834] received
[2026-03-29 12:05:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[4e77cf0c-bff7-42de-85d3-a3bd5059d834] succeeded in 0.0033391000470146537s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:05:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[da034974-f3f1-481e-ab6e-140d689b6e8d] received
[2026-03-29 12:05:57,164: INFO/MainProcess] Task tasks.scrape_pending_urls[da034974-f3f1-481e-ab6e-140d689b6e8d] succeeded in 0.003366400022059679s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:06:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[7d5af0d7-5919-446d-aeb1-6d5a468eadc5] received
[2026-03-29 12:06:27,163: INFO/MainProcess] Task tasks.scrape_pending_urls[7d5af0d7-5919-446d-aeb1-6d5a468eadc5] succeeded in 0.0031518000178039074s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:06:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[6a04a808-0b6f-4a5e-99cb-e1787f4b9e5f] received
[2026-03-29 12:06:57,164: INFO/MainProcess] Task tasks.scrape_pending_urls[6a04a808-0b6f-4a5e-99cb-e1787f4b9e5f] succeeded in 0.0035516999196261168s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:07:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[ac9e545c-5f73-4668-9eb0-57d55ccef2cc] received
[2026-03-29 12:07:27,163: INFO/MainProcess] Task tasks.scrape_pending_urls[ac9e545c-5f73-4668-9eb0-57d55ccef2cc] succeeded in 0.0029938999796286225s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:07:57,160: INFO/MainProcess] Task tasks.scrape_pending_urls[4fda3a56-d26e-4fb8-9538-4fdcf7049636] received
[2026-03-29 12:07:57,163: INFO/MainProcess] Task tasks.scrape_pending_urls[4fda3a56-d26e-4fb8-9538-4fdcf7049636] succeeded in 0.0029325999785214663s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:08:27,160: INFO/MainProcess] Task tasks.scrape_pending_urls[8b0be004-d63f-4587-84da-e136ec0f8a74] received
[2026-03-29 12:08:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[8b0be004-d63f-4587-84da-e136ec0f8a74] succeeded in 0.003581400029361248s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:08:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[eb6eedb3-1d97-4fd6-aa6f-c8a3b12b5325] received
[2026-03-29 12:08:57,185: INFO/MainProcess] Task tasks.collect_system_metrics[eb6eedb3-1d97-4fd6-aa6f-c8a3b12b5325] succeeded in 0.5174405000871047s: {'cpu': 23.3, 'memory': 45.7}
[2026-03-29 12:08:57,189: INFO/MainProcess] Task tasks.scrape_pending_urls[bcf7c6be-11a8-4bf6-8db7-3688affa00cc] received
[2026-03-29 12:08:57,193: INFO/MainProcess] Task tasks.scrape_pending_urls[bcf7c6be-11a8-4bf6-8db7-3688affa00cc] succeeded in 0.003455699887126684s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:09:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[5a196f91-c472-45fa-b2b9-609c0ce928d0] received
[2026-03-29 12:09:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[5a196f91-c472-45fa-b2b9-609c0ce928d0] succeeded in 0.003022500080987811s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:09:57,163: INFO/MainProcess] Task tasks.scrape_pending_urls[51126462-307c-428c-a715-b9e89660e010] received
[2026-03-29 12:09:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[51126462-307c-428c-a715-b9e89660e010] succeeded in 0.0030436000088229775s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:10:27,163: INFO/MainProcess] Task tasks.scrape_pending_urls[b16af6e2-ef2b-413f-bb60-019cb365b432] received
[2026-03-29 12:10:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[b16af6e2-ef2b-413f-bb60-019cb365b432] succeeded in 0.0033916999818757176s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:10:57,164: INFO/MainProcess] Task tasks.scrape_pending_urls[cee7a7aa-21dd-49be-9ead-95b1b014cf74] received
[2026-03-29 12:10:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[cee7a7aa-21dd-49be-9ead-95b1b014cf74] succeeded in 0.003153699915856123s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:11:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[9a2792c9-5b5d-4c5c-b0f9-f735e70a27d1] received
[2026-03-29 12:11:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[9a2792c9-5b5d-4c5c-b0f9-f735e70a27d1] succeeded in 0.0033912999788299203s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:11:57,164: INFO/MainProcess] Task tasks.scrape_pending_urls[ef8a14fd-5174-4396-bd6e-459832c133e8] received
[2026-03-29 12:11:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[ef8a14fd-5174-4396-bd6e-459832c133e8] succeeded in 0.003209700109437108s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:12:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[3050fe28-fc68-492a-bfdf-dab957bf7b08] received
[2026-03-29 12:12:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[3050fe28-fc68-492a-bfdf-dab957bf7b08] succeeded in 0.003138700034469366s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:12:57,164: INFO/MainProcess] Task tasks.scrape_pending_urls[a96e3a3d-5012-4081-b046-f8cf2d400ff5] received
[2026-03-29 12:12:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[a96e3a3d-5012-4081-b046-f8cf2d400ff5] succeeded in 0.0031526999082416296s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:13:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[9f51a33f-a30f-4412-99de-7aff18a1a7b5] received
[2026-03-29 12:13:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[9f51a33f-a30f-4412-99de-7aff18a1a7b5] succeeded in 0.0031376000260934234s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:13:56,642: INFO/MainProcess] Task tasks.reset_stale_processing_urls[20d61ae8-f7eb-4667-a11b-6397c5f901e2] received
[2026-03-29 12:13:56,646: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-29 12:13:56,647: INFO/MainProcess] Task tasks.reset_stale_processing_urls[20d61ae8-f7eb-4667-a11b-6397c5f901e2] succeeded in 0.003963900031521916s: {'reset': 0}
[2026-03-29 12:13:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[0575fb6c-c743-4c7e-9ffd-ff9327e7b7cd] received
[2026-03-29 12:13:57,280: INFO/MainProcess] Task tasks.collect_system_metrics[0575fb6c-c743-4c7e-9ffd-ff9327e7b7cd] succeeded in 0.5173324000788853s: {'cpu': 31.5, 'memory': 45.8}
[2026-03-29 12:13:57,282: INFO/MainProcess] Task tasks.scrape_pending_urls[141ed698-6777-4a4f-a8d7-3eaab3ce0dcc] received
[2026-03-29 12:13:57,285: INFO/MainProcess] Task tasks.scrape_pending_urls[141ed698-6777-4a4f-a8d7-3eaab3ce0dcc] succeeded in 0.003049899940378964s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:14:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[d1b1f3f8-4cd4-40ff-a871-8cefbdddcfa8] received
[2026-03-29 12:14:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[d1b1f3f8-4cd4-40ff-a871-8cefbdddcfa8] succeeded in 0.0032161999261006713s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:14:57,164: INFO/MainProcess] Task tasks.scrape_pending_urls[76a4c9fb-9d75-4cc8-8b66-a4cababfd8ae] received
[2026-03-29 12:14:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[76a4c9fb-9d75-4cc8-8b66-a4cababfd8ae] succeeded in 0.003043400007300079s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:15:27,164: INFO/MainProcess] Task tasks.scrape_pending_urls[8be29f1f-f4b2-492a-9981-9a854572fbd0] received
[2026-03-29 12:15:27,168: INFO/MainProcess] Task tasks.scrape_pending_urls[8be29f1f-f4b2-492a-9981-9a854572fbd0] succeeded in 0.003232999937608838s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:15:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[f30c56aa-841f-4746-81fc-232c2b943515] received
[2026-03-29 12:15:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[f30c56aa-841f-4746-81fc-232c2b943515] succeeded in 0.00372769997920841s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:16:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[d50836bb-572d-4b34-9f3c-320574d714e2] received
[2026-03-29 12:16:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[d50836bb-572d-4b34-9f3c-320574d714e2] succeeded in 0.003449500072747469s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:16:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[62beb38d-6453-435b-af22-66bccc61f176] received
[2026-03-29 12:16:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[62beb38d-6453-435b-af22-66bccc61f176] succeeded in 0.0031293999636545777s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:17:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[780e4bc6-20c7-4db6-a38e-3610ce29aae8] received
[2026-03-29 12:17:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[780e4bc6-20c7-4db6-a38e-3610ce29aae8] succeeded in 0.003172399941831827s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:17:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[3fef7f59-7a00-4a4f-9430-7dcf3856dbb5] received
[2026-03-29 12:17:57,170: INFO/MainProcess] Task tasks.scrape_pending_urls[3fef7f59-7a00-4a4f-9430-7dcf3856dbb5] succeeded in 0.002843800000846386s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:18:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[2c177532-c197-4912-bc41-f88593495256] received
[2026-03-29 12:18:27,170: INFO/MainProcess] Task tasks.scrape_pending_urls[2c177532-c197-4912-bc41-f88593495256] succeeded in 0.0027921999571844935s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:18:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[0d655669-dd3e-41b5-9fc2-629c853c94df] received
[2026-03-29 12:18:57,180: INFO/MainProcess] Task tasks.collect_system_metrics[0d655669-dd3e-41b5-9fc2-629c853c94df] succeeded in 0.5122091999510303s: {'cpu': 29.4, 'memory': 45.7}
[2026-03-29 12:18:57,182: INFO/MainProcess] Task tasks.scrape_pending_urls[1c99345d-389c-4e0f-9d19-0a429046687b] received
[2026-03-29 12:18:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[1c99345d-389c-4e0f-9d19-0a429046687b] succeeded in 0.0038778999587520957s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:19:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[d58e8ab5-d913-4170-bc47-fa82bb4bb097] received
[2026-03-29 12:19:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[d58e8ab5-d913-4170-bc47-fa82bb4bb097] succeeded in 0.0031853000400587916s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:19:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[e4d75f74-77cc-406c-9692-6989328c18ac] received
[2026-03-29 12:19:57,170: INFO/MainProcess] Task tasks.scrape_pending_urls[e4d75f74-77cc-406c-9692-6989328c18ac] succeeded in 0.0026067999424412847s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:20:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[240a03ba-d268-4133-a38a-52ad5c9a689f] received
[2026-03-29 12:20:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[240a03ba-d268-4133-a38a-52ad5c9a689f] succeeded in 0.0030809000600129366s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:20:57,167: INFO/MainProcess] Task tasks.scrape_pending_urls[dbdcfc5e-b36a-49c1-bed5-a67f8737a9e9] received
[2026-03-29 12:20:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[dbdcfc5e-b36a-49c1-bed5-a67f8737a9e9] succeeded in 0.0031217000214383006s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:21:27,167: INFO/MainProcess] Task tasks.scrape_pending_urls[7ab9d2f4-7691-49c1-8020-87e7930b93f7] received
[2026-03-29 12:21:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[7ab9d2f4-7691-49c1-8020-87e7930b93f7] succeeded in 0.0031789999920874834s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:21:57,168: INFO/MainProcess] Task tasks.scrape_pending_urls[ece37590-5827-4273-b1c7-a90a9489ab8e] received
[2026-03-29 12:21:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[ece37590-5827-4273-b1c7-a90a9489ab8e] succeeded in 0.003114200080744922s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:22:27,170: INFO/MainProcess] Task tasks.scrape_pending_urls[fe88e57c-48a5-474b-9d4e-f0a43fca2f39] received
[2026-03-29 12:22:27,174: INFO/MainProcess] Task tasks.scrape_pending_urls[fe88e57c-48a5-474b-9d4e-f0a43fca2f39] succeeded in 0.0029257999267429113s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:22:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[7dffbea1-1641-41d7-a843-9e97d2f18d21] received
[2026-03-29 12:22:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[7dffbea1-1641-41d7-a843-9e97d2f18d21] succeeded in 0.003060000017285347s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:23:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[ccd7db54-9ecd-4e2f-a1a4-7b25c9569e6a] received
[2026-03-29 12:23:27,174: INFO/MainProcess] Task tasks.scrape_pending_urls[ccd7db54-9ecd-4e2f-a1a4-7b25c9569e6a] succeeded in 0.002944400068372488s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:23:56,667: INFO/MainProcess] Task tasks.collect_system_metrics[2fe177de-41da-479e-ac9c-a372a5d2a5c1] received
[2026-03-29 12:23:57,185: INFO/MainProcess] Task tasks.collect_system_metrics[2fe177de-41da-479e-ac9c-a372a5d2a5c1] succeeded in 0.5168698000488803s: {'cpu': 21.5, 'memory': 45.4}
[2026-03-29 12:23:57,187: INFO/MainProcess] Task tasks.scrape_pending_urls[5953570c-63ec-489d-b53f-5ee1cfbc613f] received
[2026-03-29 12:23:57,190: INFO/MainProcess] Task tasks.scrape_pending_urls[5953570c-63ec-489d-b53f-5ee1cfbc613f] succeeded in 0.0031626999843865633s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:24:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[3988921b-e03d-4806-a16a-75dcff282352] received
[2026-03-29 12:24:27,174: INFO/MainProcess] Task tasks.scrape_pending_urls[3988921b-e03d-4806-a16a-75dcff282352] succeeded in 0.002824300085194409s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:24:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[a0fd2ace-78c2-4237-91a2-a88f0d51c717] received
[2026-03-29 12:24:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[a0fd2ace-78c2-4237-91a2-a88f0d51c717] succeeded in 0.003694599959999323s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:25:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[50a1ae70-1d72-4baf-812a-60bfad00a4e2] received
[2026-03-29 12:25:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[50a1ae70-1d72-4baf-812a-60bfad00a4e2] succeeded in 0.0030106999911367893s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:25:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[5a12de5a-098f-417e-9208-dae5f18f3133] received
[2026-03-29 12:25:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[5a12de5a-098f-417e-9208-dae5f18f3133] succeeded in 0.003162400098517537s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:26:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[d9f42f39-ea2a-4400-b910-c26041f44190] received
[2026-03-29 12:26:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[d9f42f39-ea2a-4400-b910-c26041f44190] succeeded in 0.003645499935373664s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:26:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[b0c03eb6-af1f-47f4-9be5-d0f57beac116] received
[2026-03-29 12:26:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[b0c03eb6-af1f-47f4-9be5-d0f57beac116] succeeded in 0.00312030001077801s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:27:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[7bb6d105-2d45-4b88-973c-84525db3f89d] received
[2026-03-29 12:27:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[7bb6d105-2d45-4b88-973c-84525db3f89d] succeeded in 0.002838499960489571s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:27:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[ae640b18-dde0-4654-82a4-3f8d4aa66bee] received
[2026-03-29 12:27:57,174: INFO/MainProcess] Task tasks.scrape_pending_urls[ae640b18-dde0-4654-82a4-3f8d4aa66bee] succeeded in 0.002884600078687072s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:28:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[b156ae60-115e-4ba5-8df6-e0a167a275a5] received
[2026-03-29 12:28:27,176: INFO/MainProcess] Task tasks.scrape_pending_urls[b156ae60-115e-4ba5-8df6-e0a167a275a5] succeeded in 0.004024699912406504s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:28:56,671: INFO/MainProcess] Task tasks.collect_system_metrics[e698fb9d-7cfb-4b71-be00-62873314fbac] received
[2026-03-29 12:28:57,191: INFO/MainProcess] Task tasks.collect_system_metrics[e698fb9d-7cfb-4b71-be00-62873314fbac] succeeded in 0.5192376999184489s: {'cpu': 28.0, 'memory': 45.6}
[2026-03-29 12:28:57,193: INFO/MainProcess] Task tasks.scrape_pending_urls[4979f894-a6d2-4de0-8c43-7351f387d9a0] received
[2026-03-29 12:28:57,197: INFO/MainProcess] Task tasks.scrape_pending_urls[4979f894-a6d2-4de0-8c43-7351f387d9a0] succeeded in 0.003436200087890029s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:29:27,171: INFO/MainProcess] Task tasks.scrape_pending_urls[9f82d86f-ddd6-4be7-a974-e053ee4bfde2] received
[2026-03-29 12:29:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[9f82d86f-ddd6-4be7-a974-e053ee4bfde2] succeeded in 0.0031513000139966607s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:29:57,171: INFO/MainProcess] Task tasks.scrape_pending_urls[f85b1da0-5db4-4465-b245-95c0fb0ebbe9] received
[2026-03-29 12:29:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[f85b1da0-5db4-4465-b245-95c0fb0ebbe9] succeeded in 0.003203999949619174s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[43d85b66-a239-4f69-b8c3-37a00d62e480] received
[2026-03-29 12:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[43d85b66-a239-4f69-b8c3-37a00d62e480] succeeded in 0.0013729999773204327s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-29 12:30:27,172: INFO/MainProcess] Task tasks.scrape_pending_urls[c23f2339-3f45-4e30-86c5-d7159379eb5f] received
[2026-03-29 12:30:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[c23f2339-3f45-4e30-86c5-d7159379eb5f] succeeded in 0.0033455999800935388s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:30:57,172: INFO/MainProcess] Task tasks.scrape_pending_urls[4facd996-0c92-4ec2-8de9-3ac38f482cd1] received
[2026-03-29 12:30:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[4facd996-0c92-4ec2-8de9-3ac38f482cd1] succeeded in 0.0032603000290691853s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:31:27,172: INFO/MainProcess] Task tasks.scrape_pending_urls[27a8555d-9602-4b76-9a01-d9740c4e536e] received
[2026-03-29 12:31:27,175: INFO/MainProcess] Task tasks.scrape_pending_urls[27a8555d-9602-4b76-9a01-d9740c4e536e] succeeded in 0.003195500001311302s: {'status': 'idle', 'pending': 0}
[2026-03-29 12:31:57,175: INFO/MainProcess] Task tasks.scrape_pending_urls[839fd274-5221-4ca7-a6bc-64fd7f67631b] received
[2026-03-29 12:31:57,178: INFO/MainProcess] Task tasks.scrape_pending_urls[839fd274-5221-4ca7-a6bc-64fd7f67631b] succeeded in 0.0034954999573528767s: {'status': 'idle', 'pending': 0}
