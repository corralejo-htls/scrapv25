
===  BookingScraper Celery Worker  ===


 -------------- worker@HOUSE v5.4.0 (opalescent)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0 2026-03-23 02:06:33
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         bookingscraper:0x291b18a46e0
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

[2026-03-23 02:06:35,874: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-23 02:06:37,905: INFO/MainProcess] mingle: searching for neighbors
[2026-03-23 02:06:45,027: INFO/MainProcess] mingle: all alone
[2026-03-23 02:06:55,239: INFO/MainProcess] worker@HOUSE ready.
[2026-03-23 02:06:55,243: INFO/MainProcess] Task tasks.scrape_pending_urls[c1d4db5e-527d-4659-a267-535c98ed756d] received
[2026-03-23 02:06:57,542: INFO/MainProcess] Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5
[2026-03-23 02:06:57,668: INFO/MainProcess] Task tasks.scrape_pending_urls[c1d4db5e-527d-4659-a267-535c98ed756d] succeeded in 2.4248978999676183s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:07:09,580: INFO/MainProcess] Task tasks.scrape_pending_urls[19b8be0e-6102-4201-9d6c-a75e71eb0b9d] received
[2026-03-23 02:07:09,584: INFO/MainProcess] Task tasks.scrape_pending_urls[19b8be0e-6102-4201-9d6c-a75e71eb0b9d] succeeded in 0.003966599993873388s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:07:33,473: INFO/MainProcess] Task tasks.scrape_pending_urls[fcf9a3c6-9981-4db5-b77e-68c2d1700d72] received
[2026-03-23 02:07:33,479: INFO/MainProcess] Task tasks.scrape_pending_urls[fcf9a3c6-9981-4db5-b77e-68c2d1700d72] succeeded in 0.005761700042057782s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:08:03,473: INFO/MainProcess] Task tasks.scrape_pending_urls[00b262cc-e60c-476f-b3ec-2cdef9d76c03] received
[2026-03-23 02:08:03,479: INFO/MainProcess] Task tasks.scrape_pending_urls[00b262cc-e60c-476f-b3ec-2cdef9d76c03] succeeded in 0.005867899977602065s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:08:33,474: INFO/MainProcess] Task tasks.scrape_pending_urls[8ab93422-6e1d-4203-8dfe-a334c3f1a3d3] received
[2026-03-23 02:08:33,481: INFO/MainProcess] Task tasks.scrape_pending_urls[8ab93422-6e1d-4203-8dfe-a334c3f1a3d3] succeeded in 0.006926300004124641s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:09:03,473: INFO/MainProcess] Task tasks.scrape_pending_urls[d1b7250b-6f45-4606-a960-2ee6398f95c1] received
[2026-03-23 02:09:03,480: INFO/MainProcess] Task tasks.scrape_pending_urls[d1b7250b-6f45-4606-a960-2ee6398f95c1] succeeded in 0.005905699974391609s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:09:33,474: INFO/MainProcess] Task tasks.scrape_pending_urls[05e7cdf9-139e-4bc4-a1d1-0e9eb27b9a78] received
[2026-03-23 02:09:33,490: INFO/MainProcess] Task tasks.scrape_pending_urls[05e7cdf9-139e-4bc4-a1d1-0e9eb27b9a78] succeeded in 0.014522899989970028s: {'status': 'idle', 'pending': 0}
[2026-03-23 02:10:03,473: INFO/MainProcess] Task tasks.scrape_pending_urls[2f86895b-3f1e-4523-849c-7d4536822de3] received
[2026-03-23 02:10:05,478: INFO/MainProcess] scrape_pending_urls: starting auto-batch, pending=13
[2026-03-23 02:10:05,995: INFO/MainProcess] VPN: original IP = 192.145.39.60
[2026-03-23 02:10:06,533: INFO/MainProcess] VPN: home country detected = ES
[2026-03-23 02:10:06,534: INFO/MainProcess] NordVPNManager initialised | interactive=False | original_ip=192.145.39.60 | home_country=ES
[2026-03-23 02:10:06,535: INFO/MainProcess] ScraperService INIT | VPN_ENABLED=True | HEADLESS_BROWSER=False | workers=2 | languages=es,en,de,it | vpn_interval=50s | vpn_countries=Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden
[2026-03-23 02:10:06,564: INFO/MainProcess] VPN: excluding home country ES from pool — remaining: DE,FR,NL,IT,CA,SE
[2026-03-23 02:10:06,565: INFO/MainProcess] VPN: connecting to France (FR)...
[2026-03-23 02:10:27,835: INFO/MainProcess] VPN connected to France — IP: 45.141.123.130
[2026-03-23 02:10:27,835: INFO/MainProcess] VPN connected OK before batch start.
[2026-03-23 02:10:27,836: INFO/MainProcess] Dispatching batch: urls=13 workers=2
[2026-03-23 02:10:27,836: INFO/MainProcess] Redis connection pool created: max_connections=20
[2026-03-23 02:10:32,778: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-23 02:10:32,788: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-23 02:10:45,831: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-23 02:10:47,534: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-23 02:10:50,426: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-23 02:10:51,718: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-23 02:11:01,681: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-23 02:11:02,699: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-23 02:11:08,312: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-23 02:11:08,904: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-23 02:11:18,079: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-23 02:11:18,080: INFO/MainProcess] CloudScraper failed for 32ff0590-e264-42f3-b475-e6fb68fe5287/es — trying Selenium.
[2026-03-23 02:11:18,542: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-23 02:11:18,543: INFO/MainProcess] CloudScraper failed for 0685c131-5969-4b78-b02e-a76c6357c6bb/es — trying Selenium.
[2026-03-23 02:11:21,192: INFO/MainProcess] Selenium: Brave started
[2026-03-23 02:12:54,044: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:13:06,373: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:13:11,010: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:13:19,254: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:13:25,457: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:13:40,226: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:13:40,227: INFO/MainProcess] CloudScraper failed for 32ff0590-e264-42f3-b475-e6fb68fe5287/en — trying Selenium.
[2026-03-23 02:14:13,576: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:14:23,909: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:14:28,539: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:14:36,838: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:14:43,028: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:15:09,208: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-23 02:15:09,209: INFO/MainProcess] CloudScraper failed for 0685c131-5969-4b78-b02e-a76c6357c6bb/en — trying Selenium.
[2026-03-23 02:16:30,464: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:16:32,367: INFO/MainProcess] Gallery: 131 images loaded after scroll
[2026-03-23 02:16:35,769: INFO/MainProcess] Gallery: 138 unique image URLs extracted
[2026-03-23 02:16:35,901: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 02:16:35,902: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:17:01,638: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 32ff0590-e264-42f3-b475-e6fb68fe5287
[2026-03-23 02:17:11,521: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel d0dc3b28-9a8e-44bb-8f11-54197e52fc69
[2026-03-23 02:17:11,521: WARNING/MainProcess] ImageDownloader failed for 32ff0590-e264-42f3-b475-e6fb68fe5287: too many values to unpack (expected 2, got 45)
[2026-03-23 02:17:14,524: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-23 02:17:26,327: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-23 02:17:30,986: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-23 02:17:43,186: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-23 02:17:49,381: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-23 02:18:03,762: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-23 02:18:03,763: INFO/MainProcess] CloudScraper failed for 32ff0590-e264-42f3-b475-e6fb68fe5287/de — trying Selenium.
[2026-03-23 02:19:21,502: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:19:23,442: INFO/MainProcess] Gallery: 137 images loaded after scroll
[2026-03-23 02:19:27,223: INFO/MainProcess] Gallery: 144 unique image URLs extracted
[2026-03-23 02:19:27,373: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 02:19:27,377: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:19:53,912: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 0685c131-5969-4b78-b02e-a76c6357c6bb
[2026-03-23 02:20:02,416: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 6c7f8422-cd3e-4467-90b8-2d7fc20dda67
[2026-03-23 02:20:02,417: WARNING/MainProcess] ImageDownloader failed for 0685c131-5969-4b78-b02e-a76c6357c6bb: too many values to unpack (expected 2, got 45)
[2026-03-23 02:20:05,234: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-23 02:20:17,958: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-23 02:20:22,878: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-23 02:20:31,194: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-23 02:20:37,589: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-23 02:20:49,950: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-23 02:20:49,950: INFO/MainProcess] CloudScraper failed for 0685c131-5969-4b78-b02e-a76c6357c6bb/de — trying Selenium.
[2026-03-23 02:21:16,076: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-23 02:21:26,295: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-23 02:21:30,982: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-23 02:21:42,533: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-23 02:21:48,721: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-23 02:22:03,556: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-23 02:22:03,556: INFO/MainProcess] CloudScraper failed for 32ff0590-e264-42f3-b475-e6fb68fe5287/it — trying Selenium.
[2026-03-23 02:22:34,343: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-23 02:22:59,644: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-23 02:23:04,349: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-23 02:23:12,701: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-23 02:23:18,904: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-23 02:23:31,794: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-23 02:23:31,795: INFO/MainProcess] CloudScraper failed for 0685c131-5969-4b78-b02e-a76c6357c6bb/it — trying Selenium.
[2026-03-23 02:23:52,227: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-23 02:24:04,691: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-23 02:24:09,417: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-23 02:24:17,469: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-23 02:24:23,669: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-23 02:24:36,707: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-23 02:24:36,707: INFO/MainProcess] CloudScraper failed for 82120e1b-3dd5-41a2-804b-86504d39fed6/es — trying Selenium.
[2026-03-23 02:25:25,333: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-23 02:25:35,798: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-23 02:25:40,481: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-23 02:25:51,371: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-23 02:25:57,565: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-23 02:26:06,847: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-23 02:26:06,847: INFO/MainProcess] CloudScraper failed for 6eb4d038-07d4-4b93-9a69-7aa19c4586b5/es — trying Selenium.
[2026-03-23 02:26:43,751: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-23 02:26:54,498: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-23 02:26:59,296: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-23 02:27:13,455: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-23 02:27:19,631: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-23 02:27:58,741: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-23 02:27:58,743: INFO/MainProcess] CloudScraper failed for 82120e1b-3dd5-41a2-804b-86504d39fed6/en — trying Selenium.
[2026-03-23 02:28:03,586: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-23 02:28:34,682: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-23 02:28:39,444: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-23 02:28:50,638: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-23 02:28:56,958: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-23 02:29:06,699: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-23 02:29:06,699: INFO/MainProcess] CloudScraper failed for 6eb4d038-07d4-4b93-9a69-7aa19c4586b5/en — trying Selenium.
[2026-03-23 02:30:22,071: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:30:23,991: INFO/MainProcess] Gallery: 87 images loaded after scroll
[2026-03-23 02:30:26,181: INFO/MainProcess] Gallery: 94 unique image URLs extracted
[2026-03-23 02:30:26,310: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 02:30:26,311: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:30:51,965: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 82120e1b-3dd5-41a2-804b-86504d39fed6
[2026-03-23 02:31:01,487: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel fba956fa-cb25-49f2-b483-16c49eea3a23
[2026-03-23 02:31:01,487: WARNING/MainProcess] ImageDownloader failed for 82120e1b-3dd5-41a2-804b-86504d39fed6: too many values to unpack (expected 2, got 45)
[2026-03-23 02:31:04,336: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-23 02:31:12,987: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-23 02:31:17,626: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-23 02:31:31,141: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-23 02:31:37,328: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-23 02:31:50,620: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-23 02:31:50,621: INFO/MainProcess] CloudScraper failed for 82120e1b-3dd5-41a2-804b-86504d39fed6/de — trying Selenium.
[2026-03-23 02:33:13,840: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:33:15,905: INFO/MainProcess] Gallery: 266 images loaded after scroll
[2026-03-23 02:33:21,102: INFO/MainProcess] Gallery: 273 unique image URLs extracted
[2026-03-23 02:33:21,279: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 02:33:21,280: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:33:48,778: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 6eb4d038-07d4-4b93-9a69-7aa19c4586b5
[2026-03-23 02:33:58,079: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel e266eeb3-d7c3-41a4-ae52-bf2300a60f25
[2026-03-23 02:33:58,080: WARNING/MainProcess] ImageDownloader failed for 6eb4d038-07d4-4b93-9a69-7aa19c4586b5: too many values to unpack (expected 2, got 45)
[2026-03-23 02:34:00,827: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-23 02:34:10,132: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-23 02:34:14,957: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-23 02:34:23,375: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-23 02:34:29,555: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-23 02:34:42,864: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-23 02:34:42,864: INFO/MainProcess] CloudScraper failed for 6eb4d038-07d4-4b93-9a69-7aa19c4586b5/de — trying Selenium.
[2026-03-23 02:35:10,543: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-23 02:35:24,423: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-23 02:35:29,225: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-23 02:36:08,473: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-23 02:36:14,653: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-23 02:36:23,262: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-23 02:36:23,263: INFO/MainProcess] CloudScraper failed for 82120e1b-3dd5-41a2-804b-86504d39fed6/it — trying Selenium.
[2026-03-23 02:36:27,426: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-23 02:36:38,403: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-23 02:36:43,091: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-23 02:36:55,074: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-23 02:37:01,251: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-23 02:37:15,211: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-23 02:37:15,211: INFO/MainProcess] CloudScraper failed for 6eb4d038-07d4-4b93-9a69-7aa19c4586b5/it — trying Selenium.
[2026-03-23 02:37:44,263: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-23 02:37:53,979: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-23 02:37:58,781: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-23 02:38:12,995: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-23 02:38:19,186: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-23 02:38:57,626: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-23 02:38:57,627: INFO/MainProcess] CloudScraper failed for e577917d-6ee3-4c33-a6dc-2b4d5662f142/es — trying Selenium.
[2026-03-23 02:39:14,924: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-23 02:39:29,417: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-23 02:39:34,114: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-23 02:39:45,753: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-23 02:39:51,931: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-23 02:40:01,837: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-23 02:40:01,837: INFO/MainProcess] CloudScraper failed for 1a54b67d-01db-4e6c-88fb-208392d58712/es — trying Selenium.
[2026-03-23 02:40:33,360: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-23 02:40:43,367: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-23 02:40:48,101: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-23 02:40:56,219: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-23 02:41:02,388: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-23 02:41:14,910: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-23 02:41:14,910: INFO/MainProcess] CloudScraper failed for e577917d-6ee3-4c33-a6dc-2b4d5662f142/en — trying Selenium.
[2026-03-23 02:41:51,814: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-23 02:42:01,703: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-23 02:42:06,444: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-23 02:42:19,102: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-23 02:42:25,285: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-23 02:42:40,167: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-23 02:42:40,172: INFO/MainProcess] CloudScraper failed for 1a54b67d-01db-4e6c-88fb-208392d58712/en — trying Selenium.
[2026-03-23 02:44:11,094: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:44:13,017: INFO/MainProcess] Gallery: 118 images loaded after scroll
[2026-03-23 02:44:17,004: INFO/MainProcess] Gallery: 125 unique image URLs extracted
[2026-03-23 02:44:17,198: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 02:44:17,199: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:44:44,617: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for e577917d-6ee3-4c33-a6dc-2b4d5662f142
[2026-03-23 02:44:53,049: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 3e3ed7cb-e0d5-4170-ba42-edbcf19a3f45
[2026-03-23 02:44:53,049: WARNING/MainProcess] ImageDownloader failed for e577917d-6ee3-4c33-a6dc-2b4d5662f142: too many values to unpack (expected 2, got 45)
[2026-03-23 02:44:55,855: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-23 02:45:05,609: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-23 02:45:10,413: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-23 02:45:20,897: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-23 02:45:27,074: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-23 02:45:37,986: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-23 02:45:37,986: INFO/MainProcess] CloudScraper failed for e577917d-6ee3-4c33-a6dc-2b4d5662f142/de — trying Selenium.
[2026-03-23 02:47:05,863: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:47:07,739: INFO/MainProcess] Gallery: 24 images loaded after scroll
[2026-03-23 02:47:09,037: INFO/MainProcess] Gallery: 31 unique image URLs extracted
[2026-03-23 02:47:09,151: INFO/MainProcess] hotelPhotos JS: 24 photos extracted from page source
[2026-03-23 02:47:09,151: INFO/MainProcess] Gallery: 24 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:47:35,706: INFO/MainProcess] Photos: 24 rich photo records (hotelPhotos JS) for 1a54b67d-01db-4e6c-88fb-208392d58712
[2026-03-23 02:47:41,616: INFO/MainProcess] download_photo_batch: 72/72 photo-files saved for hotel b243f790-9c5a-45f1-a17c-947d21e7a8f7
[2026-03-23 02:47:41,617: WARNING/MainProcess] ImageDownloader failed for 1a54b67d-01db-4e6c-88fb-208392d58712: too many values to unpack (expected 2, got 24)
[2026-03-23 02:47:44,852: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-23 02:47:55,287: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-23 02:47:59,903: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-23 02:48:10,974: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-23 02:48:17,151: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-23 02:48:30,530: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-23 02:48:30,530: INFO/MainProcess] CloudScraper failed for 1a54b67d-01db-4e6c-88fb-208392d58712/de — trying Selenium.
[2026-03-23 02:48:56,515: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-23 02:49:10,320: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-23 02:49:15,210: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-23 02:49:42,913: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-23 02:49:49,079: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-23 02:50:02,900: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-23 02:50:02,901: INFO/MainProcess] CloudScraper failed for e577917d-6ee3-4c33-a6dc-2b4d5662f142/it — trying Selenium.
[2026-03-23 02:50:14,350: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-23 02:50:25,298: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-23 02:50:30,076: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-23 02:50:44,515: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-23 02:50:50,686: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-23 02:50:59,465: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-23 02:50:59,465: INFO/MainProcess] CloudScraper failed for 1a54b67d-01db-4e6c-88fb-208392d58712/it — trying Selenium.
[2026-03-23 02:51:33,821: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-23 02:51:46,249: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-23 02:51:51,057: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-23 02:52:04,298: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-23 02:52:10,492: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-23 02:52:20,125: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-23 02:52:20,125: INFO/MainProcess] CloudScraper failed for 40cc1aa4-9785-4ec8-94e3-9d4b07107567/es — trying Selenium.
[2026-03-23 02:53:05,094: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-23 02:53:13,704: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-23 02:53:18,486: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-23 02:53:28,019: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-23 02:53:34,219: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-23 02:53:43,295: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-23 02:53:43,295: INFO/MainProcess] CloudScraper failed for 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/es — trying Selenium.
[2026-03-23 02:54:21,855: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-23 02:54:34,617: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-23 02:54:39,374: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-23 02:54:49,402: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-23 02:54:55,580: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-23 02:55:09,845: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-23 02:55:09,845: INFO/MainProcess] CloudScraper failed for 40cc1aa4-9785-4ec8-94e3-9d4b07107567/en — trying Selenium.
[2026-03-23 02:55:39,289: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 02:55:48,751: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 02:55:53,408: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 02:56:29,196: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 02:56:35,376: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 02:56:50,185: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 02:56:50,185: INFO/MainProcess] CloudScraper failed for 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/en — trying Selenium.
[2026-03-23 02:57:57,455: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 02:57:59,441: INFO/MainProcess] Gallery: 144 images loaded after scroll
[2026-03-23 02:58:03,485: INFO/MainProcess] Gallery: 151 unique image URLs extracted
[2026-03-23 02:58:03,677: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 02:58:03,679: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 02:58:30,397: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 40cc1aa4-9785-4ec8-94e3-9d4b07107567
[2026-03-23 02:58:39,857: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 1892bd25-91b3-4695-acd8-3d7165fca0b2
[2026-03-23 02:58:39,858: WARNING/MainProcess] ImageDownloader failed for 40cc1aa4-9785-4ec8-94e3-9d4b07107567: too many values to unpack (expected 2, got 45)
[2026-03-23 02:58:42,592: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-23 02:58:55,280: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-23 02:58:59,979: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-23 02:59:09,752: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-23 02:59:15,946: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-23 02:59:26,299: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-23 02:59:26,299: INFO/MainProcess] CloudScraper failed for 40cc1aa4-9785-4ec8-94e3-9d4b07107567/de — trying Selenium.
[2026-03-23 02:59:47,220: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-23 02:59:59,563: INFO/MainProcess] Selenium retry 2 -- waiting 11s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:01:25,117: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-23 03:01:35,130: INFO/MainProcess] Selenium retry 3 -- waiting 31s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:03:21,396: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-23 03:03:21,397: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:03:21,398: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/en
[2026-03-23 03:03:21,399: INFO/MainProcess] VPN: rotating (current=FR)...
[2026-03-23 03:03:22,330: INFO/MainProcess] VPN disconnected.
[2026-03-23 03:03:27,330: INFO/MainProcess] VPN: connecting to Netherlands (NL)...
[2026-03-23 03:03:46,371: INFO/MainProcess] VPN connected to Netherlands — IP: 176.97.206.65
[2026-03-23 03:03:46,371: INFO/MainProcess] VPN rotation successful → Netherlands
[2026-03-23 03:03:46,372: INFO/MainProcess] VPN rotated — retrying 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/en with CloudScraper.
[2026-03-23 03:03:49,075: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:03:57,854: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:03:57,854: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-23 03:04:43,624: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-23 03:04:53,894: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-23 03:04:58,600: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-23 03:05:11,826: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-23 03:05:18,007: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-23 03:05:32,164: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-23 03:05:32,164: INFO/MainProcess] CloudScraper failed for 40cc1aa4-9785-4ec8-94e3-9d4b07107567/it — trying Selenium.
[2026-03-23 03:05:59,655: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-23 03:06:08,392: INFO/MainProcess] Selenium retry 2 -- waiting 17s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:07:40,116: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-23 03:07:48,326: INFO/MainProcess] Selenium retry 3 -- waiting 33s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:09:35,702: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-23 03:09:35,703: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-23 03:09:38,386: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:09:51,623: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:09:56,402: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:10:10,191: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:10:16,993: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:10:27,070: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:10:27,070: INFO/MainProcess] CloudScraper failed for 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/de — trying Selenium.
[2026-03-23 03:10:56,435: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-23 03:11:06,432: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-23 03:11:11,077: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-23 03:11:19,623: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-23 03:11:25,791: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-23 03:11:35,168: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-23 03:11:35,169: INFO/MainProcess] CloudScraper failed for b134f561-ad2c-40b6-b858-9b9ad18f13e2/es — trying Selenium.
[2026-03-23 03:12:10,972: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-23 03:12:24,991: INFO/MainProcess] Selenium retry 2 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:14:02,594: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-23 03:14:11,181: INFO/MainProcess] Selenium retry 3 -- waiting 26s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:15:52,145: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-23 03:15:52,145: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:15:52,146: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/de
[2026-03-23 03:15:52,147: INFO/MainProcess] VPN: rotating (current=NL)...
[2026-03-23 03:15:53,111: INFO/MainProcess] VPN disconnected.
[2026-03-23 03:15:58,112: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-23 03:16:17,231: INFO/MainProcess] VPN connected to Sweden — IP: 194.5.154.216
[2026-03-23 03:16:17,231: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-23 03:16:17,232: INFO/MainProcess] VPN rotated — retrying 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/de with CloudScraper.
[2026-03-23 03:16:20,093: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:16:34,460: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:16:34,461: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-23 03:17:13,919: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-23 03:17:24,969: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-23 03:17:29,867: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-23 03:17:38,294: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-23 03:17:44,955: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-23 03:17:59,800: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-23 03:17:59,801: INFO/MainProcess] CloudScraper failed for b134f561-ad2c-40b6-b858-9b9ad18f13e2/en — trying Selenium.
[2026-03-23 03:18:28,470: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-23 03:18:41,168: INFO/MainProcess] Selenium retry 2 -- waiting 18s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:20:13,957: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-23 03:20:26,233: INFO/MainProcess] Selenium retry 3 -- waiting 35s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:22:16,009: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-23 03:22:16,009: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-23 03:22:19,025: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:22:39,495: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:22:44,293: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:22:52,302: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:22:58,511: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:23:12,201: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:23:12,201: INFO/MainProcess] CloudScraper failed for 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/it — trying Selenium.
[2026-03-23 03:24:35,902: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 03:24:37,804: INFO/MainProcess] Gallery: 77 images loaded after scroll
[2026-03-23 03:24:40,711: INFO/MainProcess] Gallery: 84 unique image URLs extracted
[2026-03-23 03:24:40,854: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 03:24:40,857: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 03:25:06,732: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for b134f561-ad2c-40b6-b858-9b9ad18f13e2
[2026-03-23 03:25:17,432: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 9c0f9103-6e28-4989-ac4a-c3f07c8b234d
[2026-03-23 03:25:17,433: WARNING/MainProcess] ImageDownloader failed for b134f561-ad2c-40b6-b858-9b9ad18f13e2: too many values to unpack (expected 2, got 45)
[2026-03-23 03:25:20,435: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-23 03:25:31,972: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-23 03:25:36,875: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-23 03:25:45,961: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-23 03:25:52,188: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-23 03:26:07,145: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-23 03:26:07,146: INFO/MainProcess] CloudScraper failed for b134f561-ad2c-40b6-b858-9b9ad18f13e2/de — trying Selenium.
[2026-03-23 03:26:24,901: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-23 03:26:35,500: INFO/MainProcess] Selenium retry 2 -- waiting 19s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:28:09,708: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-23 03:28:20,417: INFO/MainProcess] Selenium retry 3 -- waiting 35s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:30:10,210: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-23 03:30:10,210: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:30:10,211: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/it
[2026-03-23 03:30:10,212: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-23 03:30:11,092: INFO/MainProcess] VPN disconnected.
[2026-03-23 03:30:16,093: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-23 03:30:34,857: INFO/MainProcess] VPN connected to Sweden — IP: 194.5.154.31
[2026-03-23 03:30:34,857: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-23 03:30:34,858: INFO/MainProcess] VPN rotated — retrying 738af1b4-cc53-4b9c-b66a-6dd80b0168d2/it with CloudScraper.
[2026-03-23 03:30:37,641: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:30:49,291: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:30:49,292: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-23 03:31:32,894: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-23 03:31:41,079: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-23 03:31:45,876: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-23 03:31:56,588: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-23 03:32:02,807: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-23 03:32:12,764: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-23 03:32:12,764: INFO/MainProcess] CloudScraper failed for b134f561-ad2c-40b6-b858-9b9ad18f13e2/it — trying Selenium.
[2026-03-23 03:32:47,926: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-23 03:33:01,028: INFO/MainProcess] Selenium retry 2 -- waiting 12s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:34:28,264: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-23 03:34:40,218: INFO/MainProcess] Selenium retry 3 -- waiting 29s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:36:24,396: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-23 03:36:24,397: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-23 03:36:27,124: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-23 03:36:41,799: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-23 03:36:46,659: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-23 03:37:00,659: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-23 03:37:06,968: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-23 03:37:43,572: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-23 03:37:43,572: INFO/MainProcess] CloudScraper failed for 78b1b319-2fbf-4d1e-a4b3-81aa324836d8/es — trying Selenium.
[2026-03-23 03:37:45,423: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-23 03:37:58,219: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-23 03:38:03,044: WARNING/MainProcess] Block detected attempt 2 for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-23 03:38:26,131: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-23 03:38:32,360: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-23 03:38:42,163: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-23 03:38:42,163: INFO/MainProcess] CloudScraper failed for 3016cdeb-d26c-480f-8190-94db410648a6/es — trying Selenium.
[2026-03-23 03:39:12,755: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-23 03:39:25,140: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-23 03:39:32,084: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-23 03:39:45,437: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-23 03:39:51,655: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-23 03:40:05,739: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-23 03:40:05,739: INFO/MainProcess] CloudScraper failed for 78b1b319-2fbf-4d1e-a4b3-81aa324836d8/en — trying Selenium.
[2026-03-23 03:40:44,347: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-23 03:40:55,287: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-23 03:41:00,014: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-23 03:41:13,836: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-23 03:41:20,067: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-23 03:41:32,921: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-23 03:41:32,922: INFO/MainProcess] CloudScraper failed for 3016cdeb-d26c-480f-8190-94db410648a6/en — trying Selenium.
[2026-03-23 03:43:01,644: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 03:43:03,554: INFO/MainProcess] Gallery: 40 images loaded after scroll
[2026-03-23 03:43:05,852: INFO/MainProcess] Gallery: 47 unique image URLs extracted
[2026-03-23 03:43:05,984: INFO/MainProcess] hotelPhotos JS: 40 photos extracted from page source
[2026-03-23 03:43:05,985: INFO/MainProcess] Gallery: 40 photos with full metadata (hotelPhotos JS)
[2026-03-23 03:43:32,976: INFO/MainProcess] Photos: 40 rich photo records (hotelPhotos JS) for 78b1b319-2fbf-4d1e-a4b3-81aa324836d8
[2026-03-23 03:43:43,973: INFO/MainProcess] download_photo_batch: 120/120 photo-files saved for hotel deeb5cb1-5d3e-4911-8adc-5ae2abc7afe6
[2026-03-23 03:43:43,973: WARNING/MainProcess] ImageDownloader failed for 78b1b319-2fbf-4d1e-a4b3-81aa324836d8: too many values to unpack (expected 2, got 40)
[2026-03-23 03:43:46,797: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-23 03:44:01,478: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-23 03:44:06,327: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-23 03:44:16,574: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-23 03:44:22,798: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-23 03:44:31,592: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-23 03:44:31,593: INFO/MainProcess] CloudScraper failed for 78b1b319-2fbf-4d1e-a4b3-81aa324836d8/de — trying Selenium.
[2026-03-23 03:45:55,035: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 03:45:57,016: INFO/MainProcess] Gallery: 57 images loaded after scroll
[2026-03-23 03:45:58,880: INFO/MainProcess] Gallery: 64 unique image URLs extracted
[2026-03-23 03:45:59,023: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 03:45:59,023: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 03:46:25,231: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 3016cdeb-d26c-480f-8190-94db410648a6
[2026-03-23 03:46:36,291: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 5722a8c8-d6ac-4a23-923b-5772266693ad
[2026-03-23 03:46:36,292: WARNING/MainProcess] ImageDownloader failed for 3016cdeb-d26c-480f-8190-94db410648a6: too many values to unpack (expected 2, got 45)
[2026-03-23 03:46:39,257: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-23 03:46:53,589: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-23 03:46:58,407: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-23 03:47:11,968: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-23 03:47:18,193: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-23 03:47:44,353: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-23 03:47:44,353: INFO/MainProcess] CloudScraper failed for 3016cdeb-d26c-480f-8190-94db410648a6/de — trying Selenium.
[2026-03-23 03:47:45,212: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-23 03:48:18,924: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-23 03:48:23,816: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-23 03:48:35,321: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-23 03:48:41,545: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-23 03:49:06,520: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-23 03:49:12,551: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-23 03:49:12,552: INFO/MainProcess] CloudScraper failed for 78b1b319-2fbf-4d1e-a4b3-81aa324836d8/it — trying Selenium.
[2026-03-23 03:49:15,226: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-23 03:49:20,056: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-23 03:49:29,817: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-23 03:49:36,058: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-23 03:49:45,354: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-23 03:49:45,355: INFO/MainProcess] CloudScraper failed for 3016cdeb-d26c-480f-8190-94db410648a6/it — trying Selenium.
[2026-03-23 03:50:35,494: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-23 03:50:43,709: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-23 03:50:48,537: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-23 03:51:01,119: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-23 03:51:07,332: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-23 03:51:17,251: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-23 03:51:17,251: INFO/MainProcess] CloudScraper failed for 70306a8a-fa56-49d0-a20e-6e2b382707c3/es — trying Selenium.
[2026-03-23 03:51:54,751: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-23 03:52:05,749: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-23 03:52:10,579: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-23 03:52:18,804: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-23 03:52:25,228: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-23 03:52:35,008: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-23 03:52:35,009: INFO/MainProcess] CloudScraper failed for 23a78c52-eeb7-4cf9-9cea-1f0faa1fb4a9/es — trying Selenium.
[2026-03-23 03:53:13,728: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-23 03:53:28,009: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-23 03:53:32,924: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-23 03:53:42,565: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-23 03:53:48,793: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-23 03:53:57,028: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-23 03:53:57,029: INFO/MainProcess] CloudScraper failed for 70306a8a-fa56-49d0-a20e-6e2b382707c3/en — trying Selenium.
[2026-03-23 03:54:44,199: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-23 03:54:59,227: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-23 03:55:04,055: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-23 03:55:15,648: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-23 03:55:21,860: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-23 03:55:34,306: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-23 03:55:34,306: INFO/MainProcess] CloudScraper failed for 23a78c52-eeb7-4cf9-9cea-1f0faa1fb4a9/en — trying Selenium.
[2026-03-23 03:57:02,821: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 03:57:04,755: INFO/MainProcess] Gallery: 70 images loaded after scroll
[2026-03-23 03:57:07,500: INFO/MainProcess] Gallery: 77 unique image URLs extracted
[2026-03-23 03:57:07,638: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-23 03:57:07,638: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-23 03:57:34,863: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 70306a8a-fa56-49d0-a20e-6e2b382707c3
[2026-03-23 03:57:50,037: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel cc1d44a7-35d8-491d-8c7f-c484fcd917c9
[2026-03-23 03:57:50,038: WARNING/MainProcess] ImageDownloader failed for 70306a8a-fa56-49d0-a20e-6e2b382707c3: too many values to unpack (expected 2, got 45)
[2026-03-23 03:57:52,980: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-23 03:58:07,966: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-23 03:58:12,780: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-23 03:58:25,664: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-23 03:58:31,903: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-23 03:58:53,904: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-23 03:58:53,904: INFO/MainProcess] CloudScraper failed for 70306a8a-fa56-49d0-a20e-6e2b382707c3/de — trying Selenium.
[2026-03-23 03:59:55,874: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-23 03:59:57,779: INFO/MainProcess] Gallery: 34 images loaded after scroll
[2026-03-23 04:00:00,092: INFO/MainProcess] Gallery: 41 unique image URLs extracted
[2026-03-23 04:00:00,254: INFO/MainProcess] hotelPhotos JS: 34 photos extracted from page source
[2026-03-23 04:00:00,254: INFO/MainProcess] Gallery: 34 photos with full metadata (hotelPhotos JS)
[2026-03-23 04:00:26,300: INFO/MainProcess] Photos: 34 rich photo records (hotelPhotos JS) for 23a78c52-eeb7-4cf9-9cea-1f0faa1fb4a9
[2026-03-23 04:00:36,575: INFO/MainProcess] download_photo_batch: 102/102 photo-files saved for hotel 3218c499-3bd2-4020-8b0b-13411739bb4f
[2026-03-23 04:00:36,575: WARNING/MainProcess] ImageDownloader failed for 23a78c52-eeb7-4cf9-9cea-1f0faa1fb4a9: too many values to unpack (expected 2, got 34)
[2026-03-23 04:00:39,526: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-23 04:00:53,663: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-23 04:00:58,860: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-23 04:01:10,199: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-23 04:01:16,419: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-23 04:01:24,561: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-23 04:01:24,561: INFO/MainProcess] CloudScraper failed for 23a78c52-eeb7-4cf9-9cea-1f0faa1fb4a9/de — trying Selenium.
[2026-03-23 04:01:49,165: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-23 04:02:01,819: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-23 04:02:06,685: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-23 04:02:15,367: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-23 04:02:21,593: WARNING/MainProcess] Block detected attempt 3 for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-23 04:02:43,461: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-23 04:02:43,461: INFO/MainProcess] CloudScraper failed for 70306a8a-fa56-49d0-a20e-6e2b382707c3/it — trying Selenium.
[2026-03-23 04:03:08,354: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-23 04:03:22,856: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-23 04:03:27,998: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-23 04:03:40,970: INFO/MainProcess] CloudScraper retry 3/3 — waiting 6.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-23 04:03:47,194: WARNING/MainProcess] Short HTML (3962 bytes) for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-23 04:04:00,130: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-23 04:04:00,135: INFO/MainProcess] CloudScraper failed for 23a78c52-eeb7-4cf9-9cea-1f0faa1fb4a9/it — trying Selenium.
[2026-03-23 04:05:55,362: INFO/MainProcess] Selenium browser closed after batch completion.
[2026-03-23 04:05:55,362: INFO/MainProcess] scrape_pending_urls: batch complete — {'processed': 13, 'succeeded': 13, 'failed': 0, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-23 04:05:55,364: INFO/MainProcess] Task tasks.scrape_pending_urls[2f86895b-3f1e-4523-849c-7d4536822de3] succeeded in 6951.890481799957s: {'processed': 13, 'succeeded': 13, 'failed': 0, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-23 04:05:55,511: INFO/MainProcess] Task tasks.purge_old_debug_html[c6be76a4-0c83-445b-ad57-25f0f1726e3c] received
[2026-03-23 04:05:55,513: INFO/MainProcess] Task tasks.purge_old_debug_html[c6be76a4-0c83-445b-ad57-25f0f1726e3c] succeeded in 0.0018677999614737928s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 04:05:55,515: INFO/MainProcess] Task tasks.collect_system_metrics[a237a4ed-8fdd-4b33-b065-dfbf807d6d3d] received
[2026-03-23 04:05:56,039: INFO/MainProcess] Task tasks.collect_system_metrics[a237a4ed-8fdd-4b33-b065-dfbf807d6d3d] succeeded in 0.5239019999862649s: {'cpu': 12.5, 'memory': 40.2}
[2026-03-23 04:05:56,041: INFO/MainProcess] Task tasks.scrape_pending_urls[8fe6a94d-ec62-432c-89d6-a53d75377ec6] received
[2026-03-23 04:05:56,045: INFO/MainProcess] Task tasks.scrape_pending_urls[8fe6a94d-ec62-432c-89d6-a53d75377ec6] succeeded in 0.003757700033020228s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:56,047: INFO/MainProcess] Task tasks.reset_stale_processing_urls[edad152d-7df7-4b55-8e34-f22477365b9f] received
[2026-03-23 04:05:56,051: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 04:05:56,053: INFO/MainProcess] Task tasks.reset_stale_processing_urls[edad152d-7df7-4b55-8e34-f22477365b9f] succeeded in 0.0052958999876864254s: {'reset': 0}
[2026-03-23 04:05:56,055: INFO/MainProcess] Task tasks.collect_system_metrics[d6971823-7c40-459e-9caa-e0a0375f87b0] received
[2026-03-23 04:05:56,572: INFO/MainProcess] Task tasks.collect_system_metrics[d6971823-7c40-459e-9caa-e0a0375f87b0] succeeded in 0.5169417000142857s: {'cpu': 14.2, 'memory': 40.2}
[2026-03-23 04:05:56,574: INFO/MainProcess] Task tasks.scrape_pending_urls[32803e9e-54be-42a2-8395-b8e6bf6c8145] received
[2026-03-23 04:05:56,578: INFO/MainProcess] Task tasks.scrape_pending_urls[32803e9e-54be-42a2-8395-b8e6bf6c8145] succeeded in 0.003859399992506951s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:56,580: INFO/MainProcess] Task tasks.reset_stale_processing_urls[2d4fd1f3-0cce-4e9b-b6ae-6b8dced74550] received
[2026-03-23 04:05:56,583: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 04:05:56,584: INFO/MainProcess] Task tasks.reset_stale_processing_urls[2d4fd1f3-0cce-4e9b-b6ae-6b8dced74550] succeeded in 0.0034375000395812094s: {'reset': 0}
[2026-03-23 04:05:56,586: INFO/MainProcess] Task tasks.collect_system_metrics[cfb52994-20e0-44b3-a5cb-d8783c4fc8a4] received
[2026-03-23 04:05:57,092: INFO/MainProcess] Task tasks.collect_system_metrics[cfb52994-20e0-44b3-a5cb-d8783c4fc8a4] succeeded in 0.5060369999846444s: {'cpu': 0.8, 'memory': 40.2}
[2026-03-23 04:05:57,094: INFO/MainProcess] Task tasks.scrape_pending_urls[1d361c40-1aa6-4a7a-8bca-514064fb2b2c] received
[2026-03-23 04:05:57,098: INFO/MainProcess] Task tasks.scrape_pending_urls[1d361c40-1aa6-4a7a-8bca-514064fb2b2c] succeeded in 0.0037134999874979258s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:57,100: INFO/MainProcess] Task tasks.purge_old_debug_html[58581301-9eb1-49e6-a403-05aeac9c3a1a] received
[2026-03-23 04:05:57,102: INFO/MainProcess] Task tasks.purge_old_debug_html[58581301-9eb1-49e6-a403-05aeac9c3a1a] succeeded in 0.0015017999685369432s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 04:05:57,103: INFO/MainProcess] Task tasks.collect_system_metrics[ae0ab4a0-bb30-47b3-88c9-b533872f3a18] received
[2026-03-23 04:05:57,622: INFO/MainProcess] Task tasks.collect_system_metrics[ae0ab4a0-bb30-47b3-88c9-b533872f3a18] succeeded in 0.5183163000037894s: {'cpu': 7.0, 'memory': 40.2}
[2026-03-23 04:05:57,624: INFO/MainProcess] Task tasks.scrape_pending_urls[86005a23-d5af-42d5-ba19-00380d37e3f0] received
[2026-03-23 04:05:57,628: INFO/MainProcess] Task tasks.scrape_pending_urls[86005a23-d5af-42d5-ba19-00380d37e3f0] succeeded in 0.0038652000366710126s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:57,631: INFO/MainProcess] Task tasks.reset_stale_processing_urls[7a7e23e0-1dd0-484c-9984-9f17f09df0f2] received
[2026-03-23 04:05:57,633: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 04:05:57,635: INFO/MainProcess] Task tasks.reset_stale_processing_urls[7a7e23e0-1dd0-484c-9984-9f17f09df0f2] succeeded in 0.0039363999967463315s: {'reset': 0}
[2026-03-23 04:05:57,637: INFO/MainProcess] Task tasks.collect_system_metrics[e629c94e-07ba-4634-880c-54b0822af1e3] received
[2026-03-23 04:05:58,154: INFO/MainProcess] Task tasks.collect_system_metrics[e629c94e-07ba-4634-880c-54b0822af1e3] succeeded in 0.516937299980782s: {'cpu': 1.2, 'memory': 40.2}
[2026-03-23 04:05:58,157: INFO/MainProcess] Task tasks.scrape_pending_urls[369d9ad8-41e0-4136-9456-44ba580813f1] received
[2026-03-23 04:05:58,162: INFO/MainProcess] Task tasks.scrape_pending_urls[369d9ad8-41e0-4136-9456-44ba580813f1] succeeded in 0.004549100005533546s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:58,164: INFO/MainProcess] Task tasks.collect_system_metrics[a14d9133-22e1-4f99-9028-28c2f06baa3b] received
[2026-03-23 04:05:58,683: INFO/MainProcess] Task tasks.collect_system_metrics[a14d9133-22e1-4f99-9028-28c2f06baa3b] succeeded in 0.5184453999972902s: {'cpu': 9.5, 'memory': 40.3}
[2026-03-23 04:05:58,685: INFO/MainProcess] Task tasks.scrape_pending_urls[7744de6b-d4c8-4020-ae8b-a2a2ec273be0] received
[2026-03-23 04:05:58,689: INFO/MainProcess] Task tasks.scrape_pending_urls[7744de6b-d4c8-4020-ae8b-a2a2ec273be0] succeeded in 0.0038681000005453825s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:58,691: INFO/MainProcess] Task tasks.collect_system_metrics[ca2657e5-7936-4db2-abad-78dee59a2181] received
[2026-03-23 04:05:59,197: INFO/MainProcess] Task tasks.collect_system_metrics[ca2657e5-7936-4db2-abad-78dee59a2181] succeeded in 0.5060923999990337s: {'cpu': 2.3, 'memory': 40.4}
[2026-03-23 04:05:59,199: INFO/MainProcess] Task tasks.scrape_pending_urls[ce04ba6b-c928-4740-bf6b-9d08cb85cd19] received
[2026-03-23 04:05:59,203: INFO/MainProcess] Task tasks.scrape_pending_urls[ce04ba6b-c928-4740-bf6b-9d08cb85cd19] succeeded in 0.004127099993638694s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:59,206: INFO/MainProcess] Task tasks.collect_system_metrics[ccc54a93-a3ba-4c28-9337-d5db9a881d82] received
[2026-03-23 04:05:59,713: INFO/MainProcess] Task tasks.collect_system_metrics[ccc54a93-a3ba-4c28-9337-d5db9a881d82] succeeded in 0.5067465000320226s: {'cpu': 2.7, 'memory': 40.3}
[2026-03-23 04:05:59,715: INFO/MainProcess] Task tasks.scrape_pending_urls[470f4fdf-f976-4eac-b4b2-649d2f468366] received
[2026-03-23 04:05:59,719: INFO/MainProcess] Task tasks.scrape_pending_urls[470f4fdf-f976-4eac-b4b2-649d2f468366] succeeded in 0.0038321000174619257s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:05:59,721: INFO/MainProcess] Task tasks.collect_system_metrics[5254d883-1317-4dad-8ee9-28725fd590cd] received
[2026-03-23 04:06:00,239: INFO/MainProcess] Task tasks.collect_system_metrics[5254d883-1317-4dad-8ee9-28725fd590cd] succeeded in 0.5177196000004187s: {'cpu': 4.2, 'memory': 40.3}
[2026-03-23 04:06:00,241: INFO/MainProcess] Task tasks.scrape_pending_urls[0a487a4a-ba09-43b5-a64a-9f3c7df6e920] received
[2026-03-23 04:06:00,245: INFO/MainProcess] Task tasks.scrape_pending_urls[0a487a4a-ba09-43b5-a64a-9f3c7df6e920] succeeded in 0.0034500000183470547s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:00,247: INFO/MainProcess] Task tasks.collect_system_metrics[47499970-5a6a-4167-8796-35cf0177a30a] received
[2026-03-23 04:06:00,764: INFO/MainProcess] Task tasks.collect_system_metrics[47499970-5a6a-4167-8796-35cf0177a30a] succeeded in 0.5170047000283375s: {'cpu': 2.0, 'memory': 40.3}
[2026-03-23 04:06:00,767: INFO/MainProcess] Task tasks.scrape_pending_urls[a4d987e2-2b36-43a9-bdf5-afe0076ea9dc] received
[2026-03-23 04:06:00,771: INFO/MainProcess] Task tasks.scrape_pending_urls[a4d987e2-2b36-43a9-bdf5-afe0076ea9dc] succeeded in 0.003619000024627894s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:00,772: INFO/MainProcess] Task tasks.collect_system_metrics[07733741-7e30-4754-b408-8b2f2486e84f] received
[2026-03-23 04:06:01,291: INFO/MainProcess] Task tasks.collect_system_metrics[07733741-7e30-4754-b408-8b2f2486e84f] succeeded in 0.5180876000085846s: {'cpu': 11.5, 'memory': 40.3}
[2026-03-23 04:06:01,294: INFO/MainProcess] Task tasks.scrape_pending_urls[a8d3e840-cc44-450d-929a-599f4e4b3254] received
[2026-03-23 04:06:01,299: INFO/MainProcess] Task tasks.scrape_pending_urls[a8d3e840-cc44-450d-929a-599f4e4b3254] succeeded in 0.004482999967876822s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:01,301: INFO/MainProcess] Task tasks.collect_system_metrics[e0e2a670-0aec-4e56-a02a-3e2015f5edf1] received
[2026-03-23 04:06:01,819: INFO/MainProcess] Task tasks.collect_system_metrics[e0e2a670-0aec-4e56-a02a-3e2015f5edf1] succeeded in 0.5174435999942943s: {'cpu': 2.4, 'memory': 40.3}
[2026-03-23 04:06:01,821: INFO/MainProcess] Task tasks.scrape_pending_urls[80f3b111-e7c7-4e6f-b2df-dc729bcf0e7d] received
[2026-03-23 04:06:01,826: INFO/MainProcess] Task tasks.scrape_pending_urls[80f3b111-e7c7-4e6f-b2df-dc729bcf0e7d] succeeded in 0.004097800003364682s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:01,828: INFO/MainProcess] Task tasks.collect_system_metrics[1cdd2583-19c9-49ef-9354-e328bc535360] received
[2026-03-23 04:06:02,345: INFO/MainProcess] Task tasks.collect_system_metrics[1cdd2583-19c9-49ef-9354-e328bc535360] succeeded in 0.5170218999846838s: {'cpu': 4.0, 'memory': 40.3}
[2026-03-23 04:06:02,347: INFO/MainProcess] Task tasks.scrape_pending_urls[aacb07f0-abef-4826-bfee-f77032f45581] received
[2026-03-23 04:06:02,351: INFO/MainProcess] Task tasks.scrape_pending_urls[aacb07f0-abef-4826-bfee-f77032f45581] succeeded in 0.0034599999780766666s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:02,352: INFO/MainProcess] Task tasks.collect_system_metrics[bdf52c71-6cf4-479d-974c-244ef2831f31] received
[2026-03-23 04:06:02,871: INFO/MainProcess] Task tasks.collect_system_metrics[bdf52c71-6cf4-479d-974c-244ef2831f31] succeeded in 0.517919100006111s: {'cpu': 2.4, 'memory': 40.3}
[2026-03-23 04:06:02,873: INFO/MainProcess] Task tasks.scrape_pending_urls[8d6987f0-c5a7-44c7-816a-b2f2d619bb9a] received
[2026-03-23 04:06:02,877: INFO/MainProcess] Task tasks.scrape_pending_urls[8d6987f0-c5a7-44c7-816a-b2f2d619bb9a] succeeded in 0.003486700006760657s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:02,879: INFO/MainProcess] Task tasks.collect_system_metrics[97facb9f-9d50-4bd0-9a2d-8cb10d429d0b] received
[2026-03-23 04:06:03,396: INFO/MainProcess] Task tasks.collect_system_metrics[97facb9f-9d50-4bd0-9a2d-8cb10d429d0b] succeeded in 0.5171170000103302s: {'cpu': 8.6, 'memory': 40.3}
[2026-03-23 04:06:03,398: INFO/MainProcess] Task tasks.scrape_pending_urls[7a30023a-5a80-4372-b59c-75b0fa078ba4] received
[2026-03-23 04:06:03,403: INFO/MainProcess] Task tasks.scrape_pending_urls[7a30023a-5a80-4372-b59c-75b0fa078ba4] succeeded in 0.004005800001323223s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:03,405: INFO/MainProcess] Task tasks.collect_system_metrics[f0944ab0-e2e2-4e70-81ab-d8d803d09d85] received
[2026-03-23 04:06:03,911: INFO/MainProcess] Task tasks.collect_system_metrics[f0944ab0-e2e2-4e70-81ab-d8d803d09d85] succeeded in 0.5057468000450172s: {'cpu': 7.8, 'memory': 40.3}
[2026-03-23 04:06:03,913: INFO/MainProcess] Task tasks.scrape_pending_urls[b22eeb13-051d-481a-a972-b35f743876c1] received
[2026-03-23 04:06:03,917: INFO/MainProcess] Task tasks.scrape_pending_urls[b22eeb13-051d-481a-a972-b35f743876c1] succeeded in 0.003762899956200272s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:03,919: INFO/MainProcess] Task tasks.collect_system_metrics[c665175b-5db0-4174-8b33-62407a3b3e27] received
[2026-03-23 04:06:04,437: INFO/MainProcess] Task tasks.collect_system_metrics[c665175b-5db0-4174-8b33-62407a3b3e27] succeeded in 0.5172659000381827s: {'cpu': 0.0, 'memory': 40.3}
[2026-03-23 04:06:04,439: INFO/MainProcess] Task tasks.scrape_pending_urls[066613fa-3c5d-4dcd-91fb-312fa054dd60] received
[2026-03-23 04:06:04,443: INFO/MainProcess] Task tasks.scrape_pending_urls[066613fa-3c5d-4dcd-91fb-312fa054dd60] succeeded in 0.003512499970383942s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:04,445: INFO/MainProcess] Task tasks.collect_system_metrics[682c36df-15dc-4cf6-864b-5b70028317fd] received
[2026-03-23 04:06:04,962: INFO/MainProcess] Task tasks.collect_system_metrics[682c36df-15dc-4cf6-864b-5b70028317fd] succeeded in 0.5168905000318773s: {'cpu': 1.2, 'memory': 40.3}
[2026-03-23 04:06:04,964: INFO/MainProcess] Task tasks.scrape_pending_urls[04944d79-00b2-4064-a044-f6a2d29a8e12] received
[2026-03-23 04:06:04,968: INFO/MainProcess] Task tasks.scrape_pending_urls[04944d79-00b2-4064-a044-f6a2d29a8e12] succeeded in 0.0037544000078924s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:04,970: INFO/MainProcess] Task tasks.collect_system_metrics[7f27899d-8131-4b52-a336-458a05218fb3] received
[2026-03-23 04:06:05,488: INFO/MainProcess] Task tasks.collect_system_metrics[7f27899d-8131-4b52-a336-458a05218fb3] succeeded in 0.5169642000109889s: {'cpu': 1.2, 'memory': 40.3}
[2026-03-23 04:06:05,489: INFO/MainProcess] Task tasks.scrape_pending_urls[832ba469-2118-42a6-b809-e9620369b97f] received
[2026-03-23 04:06:05,493: INFO/MainProcess] Task tasks.scrape_pending_urls[832ba469-2118-42a6-b809-e9620369b97f] succeeded in 0.0032863999949768186s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:05,495: INFO/MainProcess] Task tasks.collect_system_metrics[478dffa5-098d-4638-9f90-20495e2b2b46] received
[2026-03-23 04:06:06,013: INFO/MainProcess] Task tasks.collect_system_metrics[478dffa5-098d-4638-9f90-20495e2b2b46] succeeded in 0.51743379997788s: {'cpu': 3.1, 'memory': 40.3}
[2026-03-23 04:06:06,015: INFO/MainProcess] Task tasks.scrape_pending_urls[229b04f0-7b20-47c5-88cd-1f8049b5ffcb] received
[2026-03-23 04:06:06,019: INFO/MainProcess] Task tasks.scrape_pending_urls[229b04f0-7b20-47c5-88cd-1f8049b5ffcb] succeeded in 0.0035945999552495778s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:06,021: INFO/MainProcess] Task tasks.collect_system_metrics[20cb9522-b882-4263-8530-11f46a97ba6f] received
[2026-03-23 04:06:06,538: INFO/MainProcess] Task tasks.collect_system_metrics[20cb9522-b882-4263-8530-11f46a97ba6f] succeeded in 0.5174069999484345s: {'cpu': 0.8, 'memory': 40.3}
[2026-03-23 04:06:06,541: INFO/MainProcess] Task tasks.scrape_pending_urls[7d737cd7-7da3-4255-b056-83ed4c5b6c1e] received
[2026-03-23 04:06:06,545: INFO/MainProcess] Task tasks.scrape_pending_urls[7d737cd7-7da3-4255-b056-83ed4c5b6c1e] succeeded in 0.0039644999778829515s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:06,547: INFO/MainProcess] Task tasks.collect_system_metrics[e5e29281-e4d8-4cf0-9976-bd21a632df62] received
[2026-03-23 04:06:07,065: INFO/MainProcess] Task tasks.collect_system_metrics[e5e29281-e4d8-4cf0-9976-bd21a632df62] succeeded in 0.5173683000029996s: {'cpu': 0.8, 'memory': 40.3}
[2026-03-23 04:06:07,067: INFO/MainProcess] Task tasks.scrape_pending_urls[0584435e-f910-4dc0-811b-eeaea1d0a095] received
[2026-03-23 04:06:07,071: INFO/MainProcess] Task tasks.scrape_pending_urls[0584435e-f910-4dc0-811b-eeaea1d0a095] succeeded in 0.0037391000078059733s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,073: INFO/MainProcess] Task tasks.collect_system_metrics[5c3a8e8b-e52b-45f3-afef-3e301476b7c4] received
[2026-03-23 04:06:07,591: INFO/MainProcess] Task tasks.collect_system_metrics[5c3a8e8b-e52b-45f3-afef-3e301476b7c4] succeeded in 0.5174399000243284s: {'cpu': 2.4, 'memory': 40.3}
[2026-03-23 04:06:07,593: INFO/MainProcess] Task tasks.scrape_pending_urls[d6e43dab-37ce-466c-8a97-4284002f7296] received
[2026-03-23 04:06:07,597: INFO/MainProcess] Task tasks.scrape_pending_urls[d6e43dab-37ce-466c-8a97-4284002f7296] succeeded in 0.0030881999991834164s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,598: INFO/MainProcess] Task tasks.scrape_pending_urls[c7aa1b63-6fe8-4bee-bedc-2342b0fe77dc] received
[2026-03-23 04:06:07,601: INFO/MainProcess] Task tasks.scrape_pending_urls[c7aa1b63-6fe8-4bee-bedc-2342b0fe77dc] succeeded in 0.0026599999982863665s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,603: INFO/MainProcess] Task tasks.scrape_pending_urls[5482134b-3311-4107-8fb9-c1d615ef3e2f] received
[2026-03-23 04:06:07,606: INFO/MainProcess] Task tasks.scrape_pending_urls[5482134b-3311-4107-8fb9-c1d615ef3e2f] succeeded in 0.002605199988465756s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,608: INFO/MainProcess] Task tasks.scrape_pending_urls[314c8277-48e8-4862-9780-9ed2eaf491d9] received
[2026-03-23 04:06:07,612: INFO/MainProcess] Task tasks.scrape_pending_urls[314c8277-48e8-4862-9780-9ed2eaf491d9] succeeded in 0.0029565999866463244s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,613: INFO/MainProcess] Task tasks.scrape_pending_urls[7a4894e1-80fa-4e26-93b1-ab8e98e8bc16] received
[2026-03-23 04:06:07,616: INFO/MainProcess] Task tasks.scrape_pending_urls[7a4894e1-80fa-4e26-93b1-ab8e98e8bc16] succeeded in 0.0026552999624982476s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,618: INFO/MainProcess] Task tasks.scrape_pending_urls[777f1219-8cf1-453f-950e-58e983c995eb] received
[2026-03-23 04:06:07,622: INFO/MainProcess] Task tasks.scrape_pending_urls[777f1219-8cf1-453f-950e-58e983c995eb] succeeded in 0.0033681000350043178s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,623: INFO/MainProcess] Task tasks.scrape_pending_urls[31404ef8-5fd5-4c32-965a-9cce60ab8a41] received
[2026-03-23 04:06:07,627: INFO/MainProcess] Task tasks.scrape_pending_urls[31404ef8-5fd5-4c32-965a-9cce60ab8a41] succeeded in 0.003545899991877377s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,629: INFO/MainProcess] Task tasks.scrape_pending_urls[edee5819-d02c-47f9-8ed9-c612c5b40694] received
[2026-03-23 04:06:07,632: INFO/MainProcess] Task tasks.scrape_pending_urls[edee5819-d02c-47f9-8ed9-c612c5b40694] succeeded in 0.002659299992956221s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,634: INFO/MainProcess] Task tasks.scrape_pending_urls[7f5e645d-9891-4e14-b41b-d0e66c345189] received
[2026-03-23 04:06:07,636: INFO/MainProcess] Task tasks.scrape_pending_urls[7f5e645d-9891-4e14-b41b-d0e66c345189] succeeded in 0.002600700012408197s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,638: INFO/MainProcess] Task tasks.scrape_pending_urls[9d5bf0b3-f891-4e33-824c-a63565cb493a] received
[2026-03-23 04:06:07,642: INFO/MainProcess] Task tasks.scrape_pending_urls[9d5bf0b3-f891-4e33-824c-a63565cb493a] succeeded in 0.0037690000026486814s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,644: INFO/MainProcess] Task tasks.scrape_pending_urls[ac373407-acc1-462d-8d0e-602c72493df0] received
[2026-03-23 04:06:07,648: INFO/MainProcess] Task tasks.scrape_pending_urls[ac373407-acc1-462d-8d0e-602c72493df0] succeeded in 0.003423199988901615s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,649: INFO/MainProcess] Task tasks.scrape_pending_urls[7c63439a-053b-4335-8ad2-2055344a4273] received
[2026-03-23 04:06:07,652: INFO/MainProcess] Task tasks.scrape_pending_urls[7c63439a-053b-4335-8ad2-2055344a4273] succeeded in 0.002687099971808493s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,654: INFO/MainProcess] Task tasks.scrape_pending_urls[4c6e0658-b222-4119-9000-469065349905] received
[2026-03-23 04:06:07,658: INFO/MainProcess] Task tasks.scrape_pending_urls[4c6e0658-b222-4119-9000-469065349905] succeeded in 0.0036239000037312508s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,660: INFO/MainProcess] Task tasks.scrape_pending_urls[5bef0254-5839-46b4-b0ce-d7f7a3b44c65] received
[2026-03-23 04:06:07,663: INFO/MainProcess] Task tasks.scrape_pending_urls[5bef0254-5839-46b4-b0ce-d7f7a3b44c65] succeeded in 0.0026836000033654273s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,664: INFO/MainProcess] Task tasks.scrape_pending_urls[920616ea-ff8c-4e81-be5c-a49a7f697227] received
[2026-03-23 04:06:07,667: INFO/MainProcess] Task tasks.scrape_pending_urls[920616ea-ff8c-4e81-be5c-a49a7f697227] succeeded in 0.0026070000021718442s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,669: INFO/MainProcess] Task tasks.scrape_pending_urls[eb304aad-308b-4d96-879f-677d8e408017] received
[2026-03-23 04:06:07,673: INFO/MainProcess] Task tasks.scrape_pending_urls[eb304aad-308b-4d96-879f-677d8e408017] succeeded in 0.003926299978047609s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,675: INFO/MainProcess] Task tasks.scrape_pending_urls[6306a871-0c89-414f-aca7-3edba0b91af2] received
[2026-03-23 04:06:07,678: INFO/MainProcess] Task tasks.scrape_pending_urls[6306a871-0c89-414f-aca7-3edba0b91af2] succeeded in 0.0027171000256203115s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,680: INFO/MainProcess] Task tasks.scrape_pending_urls[d38225ea-15e4-47b5-bde4-2fc1829c2d08] received
[2026-03-23 04:06:07,683: INFO/MainProcess] Task tasks.scrape_pending_urls[d38225ea-15e4-47b5-bde4-2fc1829c2d08] succeeded in 0.0026145000010728836s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,684: INFO/MainProcess] Task tasks.scrape_pending_urls[37a3e65c-1053-4f1b-8ae2-c65ef94f4e9d] received
[2026-03-23 04:06:07,687: INFO/MainProcess] Task tasks.scrape_pending_urls[37a3e65c-1053-4f1b-8ae2-c65ef94f4e9d] succeeded in 0.0028264999855309725s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,690: INFO/MainProcess] Task tasks.scrape_pending_urls[28ae06fa-f78f-4408-9b90-616642461fe9] received
[2026-03-23 04:06:07,694: INFO/MainProcess] Task tasks.scrape_pending_urls[28ae06fa-f78f-4408-9b90-616642461fe9] succeeded in 0.003446799993980676s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,696: INFO/MainProcess] Task tasks.scrape_pending_urls[e563180c-07b3-4f86-b256-c615b6532e5d] received
[2026-03-23 04:06:07,698: INFO/MainProcess] Task tasks.scrape_pending_urls[e563180c-07b3-4f86-b256-c615b6532e5d] succeeded in 0.0024183999630622566s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,700: INFO/MainProcess] Task tasks.scrape_pending_urls[90dfe4ed-57c6-4dd2-8ed0-addf9a109710] received
[2026-03-23 04:06:07,703: INFO/MainProcess] Task tasks.scrape_pending_urls[90dfe4ed-57c6-4dd2-8ed0-addf9a109710] succeeded in 0.0023308000527322292s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,705: INFO/MainProcess] Task tasks.scrape_pending_urls[950bd2db-f54a-4c58-88fb-47b32d30a872] received
[2026-03-23 04:06:07,708: INFO/MainProcess] Task tasks.scrape_pending_urls[950bd2db-f54a-4c58-88fb-47b32d30a872] succeeded in 0.002524699957575649s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,709: INFO/MainProcess] Task tasks.scrape_pending_urls[e054ddbd-670e-4dc2-b3a6-1232aec6167f] received
[2026-03-23 04:06:07,712: INFO/MainProcess] Task tasks.scrape_pending_urls[e054ddbd-670e-4dc2-b3a6-1232aec6167f] succeeded in 0.0023364999797195196s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,714: INFO/MainProcess] Task tasks.scrape_pending_urls[535d037a-3605-42aa-aff9-90ff5850439d] received
[2026-03-23 04:06:07,717: INFO/MainProcess] Task tasks.scrape_pending_urls[535d037a-3605-42aa-aff9-90ff5850439d] succeeded in 0.002960600017104298s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,719: INFO/MainProcess] Task tasks.scrape_pending_urls[b79eb783-bf4c-421e-bce0-60c3d0778c2e] received
[2026-03-23 04:06:07,722: INFO/MainProcess] Task tasks.scrape_pending_urls[b79eb783-bf4c-421e-bce0-60c3d0778c2e] succeeded in 0.00315440003760159s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,724: INFO/MainProcess] Task tasks.scrape_pending_urls[5bb45058-70c8-4aaf-b890-bca313bcfbc0] received
[2026-03-23 04:06:07,726: INFO/MainProcess] Task tasks.scrape_pending_urls[5bb45058-70c8-4aaf-b890-bca313bcfbc0] succeeded in 0.00235580001026392s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,728: INFO/MainProcess] Task tasks.scrape_pending_urls[dab4269a-ef0b-4752-8e11-8bd1d86f6607] received
[2026-03-23 04:06:07,730: INFO/MainProcess] Task tasks.scrape_pending_urls[dab4269a-ef0b-4752-8e11-8bd1d86f6607] succeeded in 0.002313499979209155s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,732: INFO/MainProcess] Task tasks.scrape_pending_urls[bc657d6a-9c7d-4c5b-9c23-9fd85a46e6ca] received
[2026-03-23 04:06:07,735: INFO/MainProcess] Task tasks.scrape_pending_urls[bc657d6a-9c7d-4c5b-9c23-9fd85a46e6ca] succeeded in 0.002275399980135262s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,738: INFO/MainProcess] Task tasks.scrape_pending_urls[9a80404c-141b-4f66-98ed-400bdaf5e3da] received
[2026-03-23 04:06:07,741: INFO/MainProcess] Task tasks.scrape_pending_urls[9a80404c-141b-4f66-98ed-400bdaf5e3da] succeeded in 0.003019800002221018s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,743: INFO/MainProcess] Task tasks.scrape_pending_urls[4c9ac9c0-09a7-477c-bdd0-e8d1c3adc72e] received
[2026-03-23 04:06:07,745: INFO/MainProcess] Task tasks.scrape_pending_urls[4c9ac9c0-09a7-477c-bdd0-e8d1c3adc72e] succeeded in 0.002413200039882213s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,747: INFO/MainProcess] Task tasks.scrape_pending_urls[04747771-c7c6-499f-975a-cc693663a14d] received
[2026-03-23 04:06:07,750: INFO/MainProcess] Task tasks.scrape_pending_urls[04747771-c7c6-499f-975a-cc693663a14d] succeeded in 0.0023314999998547137s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,752: INFO/MainProcess] Task tasks.scrape_pending_urls[d5ec0fe2-a205-495e-9792-3768a15d8f3b] received
[2026-03-23 04:06:07,755: INFO/MainProcess] Task tasks.scrape_pending_urls[d5ec0fe2-a205-495e-9792-3768a15d8f3b] succeeded in 0.0027942999731749296s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,756: INFO/MainProcess] Task tasks.scrape_pending_urls[d88b0cf4-9157-40ae-bc5f-9e6c1abbd7e8] received
[2026-03-23 04:06:07,759: INFO/MainProcess] Task tasks.scrape_pending_urls[d88b0cf4-9157-40ae-bc5f-9e6c1abbd7e8] succeeded in 0.002466499980073422s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,761: INFO/MainProcess] Task tasks.scrape_pending_urls[55020773-4205-4e0c-b3e4-09f45ca3b29d] received
[2026-03-23 04:06:07,764: INFO/MainProcess] Task tasks.scrape_pending_urls[55020773-4205-4e0c-b3e4-09f45ca3b29d] succeeded in 0.003013300010934472s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,766: INFO/MainProcess] Task tasks.scrape_pending_urls[8d8b9b75-a231-439c-abca-d6a98caaf908] received
[2026-03-23 04:06:07,769: INFO/MainProcess] Task tasks.scrape_pending_urls[8d8b9b75-a231-439c-abca-d6a98caaf908] succeeded in 0.0031498000025749207s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,771: INFO/MainProcess] Task tasks.scrape_pending_urls[7b6383ae-8775-4006-8247-72149c866bbf] received
[2026-03-23 04:06:07,774: INFO/MainProcess] Task tasks.scrape_pending_urls[7b6383ae-8775-4006-8247-72149c866bbf] succeeded in 0.002512299979571253s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,775: INFO/MainProcess] Task tasks.scrape_pending_urls[4ea1b63e-d4e1-429c-a761-3cc35581cee2] received
[2026-03-23 04:06:07,778: INFO/MainProcess] Task tasks.scrape_pending_urls[4ea1b63e-d4e1-429c-a761-3cc35581cee2] succeeded in 0.0024608999956399202s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,780: INFO/MainProcess] Task tasks.scrape_pending_urls[c0c3fb41-4437-4631-9b81-e1871a67c65a] received
[2026-03-23 04:06:07,782: INFO/MainProcess] Task tasks.scrape_pending_urls[c0c3fb41-4437-4631-9b81-e1871a67c65a] succeeded in 0.002465600031428039s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,785: INFO/MainProcess] Task tasks.scrape_pending_urls[8ae5fe35-8c88-446a-a699-0845f96e2372] received
[2026-03-23 04:06:07,788: INFO/MainProcess] Task tasks.scrape_pending_urls[8ae5fe35-8c88-446a-a699-0845f96e2372] succeeded in 0.0031449999660253525s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,790: INFO/MainProcess] Task tasks.scrape_pending_urls[a515665d-b3a4-42e6-a806-3a385933bef6] received
[2026-03-23 04:06:07,793: INFO/MainProcess] Task tasks.scrape_pending_urls[a515665d-b3a4-42e6-a806-3a385933bef6] succeeded in 0.002546300005633384s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,795: INFO/MainProcess] Task tasks.scrape_pending_urls[5aeaaf82-c7a6-4335-94fb-1afc3894f6d1] received
[2026-03-23 04:06:07,797: INFO/MainProcess] Task tasks.scrape_pending_urls[5aeaaf82-c7a6-4335-94fb-1afc3894f6d1] succeeded in 0.0024621000047773123s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,800: INFO/MainProcess] Task tasks.scrape_pending_urls[e260124c-085c-4df9-a3f8-a0d4136de29c] received
[2026-03-23 04:06:07,803: INFO/MainProcess] Task tasks.scrape_pending_urls[e260124c-085c-4df9-a3f8-a0d4136de29c] succeeded in 0.0026124000432901084s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,804: INFO/MainProcess] Task tasks.scrape_pending_urls[3b42eb63-2348-42da-bc4a-36353681725d] received
[2026-03-23 04:06:07,807: INFO/MainProcess] Task tasks.scrape_pending_urls[3b42eb63-2348-42da-bc4a-36353681725d] succeeded in 0.0024476000107824802s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,809: INFO/MainProcess] Task tasks.scrape_pending_urls[beb44581-e2d4-4e55-b82a-bdc093fd7ef1] received
[2026-03-23 04:06:07,812: INFO/MainProcess] Task tasks.scrape_pending_urls[beb44581-e2d4-4e55-b82a-bdc093fd7ef1] succeeded in 0.00300770002650097s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,814: INFO/MainProcess] Task tasks.scrape_pending_urls[a07383da-f2c2-4366-9b40-130e220af0df] received
[2026-03-23 04:06:07,817: INFO/MainProcess] Task tasks.scrape_pending_urls[a07383da-f2c2-4366-9b40-130e220af0df] succeeded in 0.0031475999858230352s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,819: INFO/MainProcess] Task tasks.scrape_pending_urls[50aaf9f3-009b-40ad-a45d-d496e167d8d5] received
[2026-03-23 04:06:07,822: INFO/MainProcess] Task tasks.scrape_pending_urls[50aaf9f3-009b-40ad-a45d-d496e167d8d5] succeeded in 0.002516200009267777s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,823: INFO/MainProcess] Task tasks.scrape_pending_urls[d8b36578-db4e-4adb-9753-47096aefdb2c] received
[2026-03-23 04:06:07,826: INFO/MainProcess] Task tasks.scrape_pending_urls[d8b36578-db4e-4adb-9753-47096aefdb2c] succeeded in 0.002451099979225546s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,828: INFO/MainProcess] Task tasks.scrape_pending_urls[5ad981d4-98c3-4f09-8555-83acb0ae305e] received
[2026-03-23 04:06:07,830: INFO/MainProcess] Task tasks.scrape_pending_urls[5ad981d4-98c3-4f09-8555-83acb0ae305e] succeeded in 0.0024227999965660274s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,834: INFO/MainProcess] Task tasks.scrape_pending_urls[851174f3-ade9-4c20-bf21-a769c087a1dc] received
[2026-03-23 04:06:07,837: INFO/MainProcess] Task tasks.scrape_pending_urls[851174f3-ade9-4c20-bf21-a769c087a1dc] succeeded in 0.003610099956858903s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,839: INFO/MainProcess] Task tasks.scrape_pending_urls[2a6e6c71-574d-4df8-bb88-40ceddd36e17] received
[2026-03-23 04:06:07,843: INFO/MainProcess] Task tasks.scrape_pending_urls[2a6e6c71-574d-4df8-bb88-40ceddd36e17] succeeded in 0.0032155000371858478s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,845: INFO/MainProcess] Task tasks.scrape_pending_urls[11f9af5f-5d4d-48fb-8411-3aed6e508588] received
[2026-03-23 04:06:07,849: INFO/MainProcess] Task tasks.scrape_pending_urls[11f9af5f-5d4d-48fb-8411-3aed6e508588] succeeded in 0.003945800010114908s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,851: INFO/MainProcess] Task tasks.scrape_pending_urls[737024d0-a795-4d38-8ea0-c88df6faa190] received
[2026-03-23 04:06:07,854: INFO/MainProcess] Task tasks.scrape_pending_urls[737024d0-a795-4d38-8ea0-c88df6faa190] succeeded in 0.0026098000234924257s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,855: INFO/MainProcess] Task tasks.scrape_pending_urls[6c4fc5c6-e7b1-4603-8769-f67ecc0e0d2e] received
[2026-03-23 04:06:07,858: INFO/MainProcess] Task tasks.scrape_pending_urls[6c4fc5c6-e7b1-4603-8769-f67ecc0e0d2e] succeeded in 0.0025239000096917152s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,860: INFO/MainProcess] Task tasks.scrape_pending_urls[41f8f7d0-6d2b-4d54-b922-0e86d27bf2e8] received
[2026-03-23 04:06:07,863: INFO/MainProcess] Task tasks.scrape_pending_urls[41f8f7d0-6d2b-4d54-b922-0e86d27bf2e8] succeeded in 0.0034844999900087714s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,865: INFO/MainProcess] Task tasks.scrape_pending_urls[ba444cd4-f15f-4ce4-9191-6fc779b2f132] received
[2026-03-23 04:06:07,868: INFO/MainProcess] Task tasks.scrape_pending_urls[ba444cd4-f15f-4ce4-9191-6fc779b2f132] succeeded in 0.002553400001488626s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,870: INFO/MainProcess] Task tasks.scrape_pending_urls[26f7d53b-4019-4685-85cc-5d2e5ef3d8dc] received
[2026-03-23 04:06:07,872: INFO/MainProcess] Task tasks.scrape_pending_urls[26f7d53b-4019-4685-85cc-5d2e5ef3d8dc] succeeded in 0.002445199992507696s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,874: INFO/MainProcess] Task tasks.scrape_pending_urls[3b1a7ee0-0677-4859-b638-9f8f4416ab58] received
[2026-03-23 04:06:07,877: INFO/MainProcess] Task tasks.scrape_pending_urls[3b1a7ee0-0677-4859-b638-9f8f4416ab58] succeeded in 0.002331600000616163s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,878: INFO/MainProcess] Task tasks.scrape_pending_urls[8f841a90-bf45-4b04-be65-4fc611990f8b] received
[2026-03-23 04:06:07,882: INFO/MainProcess] Task tasks.scrape_pending_urls[8f841a90-bf45-4b04-be65-4fc611990f8b] succeeded in 0.002932800038252026s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,884: INFO/MainProcess] Task tasks.scrape_pending_urls[f4fe08ae-2ef6-4680-aeac-1583ff4a535a] received
[2026-03-23 04:06:07,887: INFO/MainProcess] Task tasks.scrape_pending_urls[f4fe08ae-2ef6-4680-aeac-1583ff4a535a] succeeded in 0.0028676000074483454s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,888: INFO/MainProcess] Task tasks.scrape_pending_urls[ac48e99c-6fbd-4a80-a1fb-35b9886466d9] received
[2026-03-23 04:06:07,891: INFO/MainProcess] Task tasks.scrape_pending_urls[ac48e99c-6fbd-4a80-a1fb-35b9886466d9] succeeded in 0.0024577000294812024s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,893: INFO/MainProcess] Task tasks.scrape_pending_urls[5cd9cb75-9aaf-4e49-b266-25f736a4219f] received
[2026-03-23 04:06:07,896: INFO/MainProcess] Task tasks.scrape_pending_urls[5cd9cb75-9aaf-4e49-b266-25f736a4219f] succeeded in 0.0031776000396348536s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,898: INFO/MainProcess] Task tasks.scrape_pending_urls[51d268b0-27c0-4399-beae-cbbd9e40c9e0] received
[2026-03-23 04:06:07,901: INFO/MainProcess] Task tasks.scrape_pending_urls[51d268b0-27c0-4399-beae-cbbd9e40c9e0] succeeded in 0.0025334000238217413s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,902: INFO/MainProcess] Task tasks.scrape_pending_urls[9f983c55-fbe6-4497-ba49-827dbc192c08] received
[2026-03-23 04:06:07,905: INFO/MainProcess] Task tasks.scrape_pending_urls[9f983c55-fbe6-4497-ba49-827dbc192c08] succeeded in 0.0024660000344738364s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,907: INFO/MainProcess] Task tasks.scrape_pending_urls[bb30909b-99dd-4ab5-be94-6f1c82982864] received
[2026-03-23 04:06:07,911: INFO/MainProcess] Task tasks.scrape_pending_urls[bb30909b-99dd-4ab5-be94-6f1c82982864] succeeded in 0.0036145999911241233s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,913: INFO/MainProcess] Task tasks.scrape_pending_urls[07aa5fcf-9cce-468c-a131-f44def629606] received
[2026-03-23 04:06:07,916: INFO/MainProcess] Task tasks.scrape_pending_urls[07aa5fcf-9cce-468c-a131-f44def629606] succeeded in 0.0025879000313580036s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,917: INFO/MainProcess] Task tasks.scrape_pending_urls[652fdaef-6726-45a6-b996-6024a29544de] received
[2026-03-23 04:06:07,920: INFO/MainProcess] Task tasks.scrape_pending_urls[652fdaef-6726-45a6-b996-6024a29544de] succeeded in 0.002533899969421327s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,922: INFO/MainProcess] Task tasks.scrape_pending_urls[78535b5a-d2de-4283-9ced-21e9da64e405] received
[2026-03-23 04:06:07,924: INFO/MainProcess] Task tasks.scrape_pending_urls[78535b5a-d2de-4283-9ced-21e9da64e405] succeeded in 0.002480600029230118s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,926: INFO/MainProcess] Task tasks.scrape_pending_urls[ab418c2e-1b3d-4a31-830c-7be4f52b16b4] received
[2026-03-23 04:06:07,929: INFO/MainProcess] Task tasks.scrape_pending_urls[ab418c2e-1b3d-4a31-830c-7be4f52b16b4] succeeded in 0.002592999953776598s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,931: INFO/MainProcess] Task tasks.scrape_pending_urls[3ffe7df2-33e0-46dd-b976-94442e76bd73] received
[2026-03-23 04:06:07,934: INFO/MainProcess] Task tasks.scrape_pending_urls[3ffe7df2-33e0-46dd-b976-94442e76bd73] succeeded in 0.0030408999882638454s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,936: INFO/MainProcess] Task tasks.scrape_pending_urls[cf57cdb8-6d13-4d11-beca-976b2679e5db] received
[2026-03-23 04:06:07,939: INFO/MainProcess] Task tasks.scrape_pending_urls[cf57cdb8-6d13-4d11-beca-976b2679e5db] succeeded in 0.0025195000343956053s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,940: INFO/MainProcess] Task tasks.scrape_pending_urls[de498ac2-b172-445e-addc-4b140b7b7c20] received
[2026-03-23 04:06:07,944: INFO/MainProcess] Task tasks.scrape_pending_urls[de498ac2-b172-445e-addc-4b140b7b7c20] succeeded in 0.0026436999905854464s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,946: INFO/MainProcess] Task tasks.scrape_pending_urls[5594fed2-08bd-43da-8601-5d2811f67c0f] received
[2026-03-23 04:06:07,949: INFO/MainProcess] Task tasks.scrape_pending_urls[5594fed2-08bd-43da-8601-5d2811f67c0f] succeeded in 0.002525599964428693s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,951: INFO/MainProcess] Task tasks.scrape_pending_urls[d521ec37-cd43-424c-9359-3d3ddfa4d8be] received
[2026-03-23 04:06:07,953: INFO/MainProcess] Task tasks.scrape_pending_urls[d521ec37-cd43-424c-9359-3d3ddfa4d8be] succeeded in 0.0025194999761879444s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,955: INFO/MainProcess] Task tasks.scrape_pending_urls[9053a394-be4e-4927-9bd1-7e9dfea86478] received
[2026-03-23 04:06:07,959: INFO/MainProcess] Task tasks.scrape_pending_urls[9053a394-be4e-4927-9bd1-7e9dfea86478] succeeded in 0.003330899984575808s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,961: INFO/MainProcess] Task tasks.scrape_pending_urls[3966336e-1176-4a5e-b3ba-db00eccf9467] received
[2026-03-23 04:06:07,963: INFO/MainProcess] Task tasks.scrape_pending_urls[3966336e-1176-4a5e-b3ba-db00eccf9467] succeeded in 0.0025317000108771026s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,965: INFO/MainProcess] Task tasks.scrape_pending_urls[5e6c7512-2a62-42c6-a048-231473fd3676] received
[2026-03-23 04:06:07,968: INFO/MainProcess] Task tasks.scrape_pending_urls[5e6c7512-2a62-42c6-a048-231473fd3676] succeeded in 0.0024751999881118536s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,969: INFO/MainProcess] Task tasks.scrape_pending_urls[2e6f59d2-54d1-4fc6-83b9-e8fb05749e9a] received
[2026-03-23 04:06:07,973: INFO/MainProcess] Task tasks.scrape_pending_urls[2e6f59d2-54d1-4fc6-83b9-e8fb05749e9a] succeeded in 0.0027626000228337944s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,975: INFO/MainProcess] Task tasks.scrape_pending_urls[f888a433-c8a9-4bfb-9e11-9ff9e4bfb571] received
[2026-03-23 04:06:07,978: INFO/MainProcess] Task tasks.scrape_pending_urls[f888a433-c8a9-4bfb-9e11-9ff9e4bfb571] succeeded in 0.0030820000101812184s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,980: INFO/MainProcess] Task tasks.scrape_pending_urls[30448c77-0450-43d8-a123-c51d538b08c9] received
[2026-03-23 04:06:07,983: INFO/MainProcess] Task tasks.scrape_pending_urls[30448c77-0450-43d8-a123-c51d538b08c9] succeeded in 0.0027057999977841973s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,985: INFO/MainProcess] Task tasks.scrape_pending_urls[1250e6ea-8d77-4b83-99c7-39b495fc6db0] received
[2026-03-23 04:06:07,988: INFO/MainProcess] Task tasks.scrape_pending_urls[1250e6ea-8d77-4b83-99c7-39b495fc6db0] succeeded in 0.0027134999982081354s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,990: INFO/MainProcess] Task tasks.scrape_pending_urls[bb68fbc6-3d47-4fbb-aaa2-6d3cf15c486b] received
[2026-03-23 04:06:07,993: INFO/MainProcess] Task tasks.scrape_pending_urls[bb68fbc6-3d47-4fbb-aaa2-6d3cf15c486b] succeeded in 0.002653900010045618s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,995: INFO/MainProcess] Task tasks.scrape_pending_urls[6ffd4056-c544-43fd-b93a-7b2a313d1b55] received
[2026-03-23 04:06:07,998: INFO/MainProcess] Task tasks.scrape_pending_urls[6ffd4056-c544-43fd-b93a-7b2a313d1b55] succeeded in 0.002501599956303835s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:07,999: INFO/MainProcess] Task tasks.scrape_pending_urls[afb48557-4a41-41e7-bee5-89702930ea7a] received
[2026-03-23 04:06:08,003: INFO/MainProcess] Task tasks.scrape_pending_urls[afb48557-4a41-41e7-bee5-89702930ea7a] succeeded in 0.0029943999834358692s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,005: INFO/MainProcess] Task tasks.scrape_pending_urls[21535910-aa7b-404f-a2c3-5eb303b8343a] received
[2026-03-23 04:06:08,008: INFO/MainProcess] Task tasks.scrape_pending_urls[21535910-aa7b-404f-a2c3-5eb303b8343a] succeeded in 0.0025483000208623707s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,009: INFO/MainProcess] Task tasks.scrape_pending_urls[c096e5e3-c7ea-4714-a2d6-df82dbe2d328] received
[2026-03-23 04:06:08,012: INFO/MainProcess] Task tasks.scrape_pending_urls[c096e5e3-c7ea-4714-a2d6-df82dbe2d328] succeeded in 0.002463199954945594s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,014: INFO/MainProcess] Task tasks.scrape_pending_urls[42332066-1cc1-4f2c-b6dc-a127c3681856] received
[2026-03-23 04:06:08,017: INFO/MainProcess] Task tasks.scrape_pending_urls[42332066-1cc1-4f2c-b6dc-a127c3681856] succeeded in 0.0024993999977596104s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,018: INFO/MainProcess] Task tasks.scrape_pending_urls[2696bf1b-349a-4014-800b-48eb60237dcf] received
[2026-03-23 04:06:08,023: INFO/MainProcess] Task tasks.scrape_pending_urls[2696bf1b-349a-4014-800b-48eb60237dcf] succeeded in 0.00405520002823323s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,024: INFO/MainProcess] Task tasks.scrape_pending_urls[1c769ccd-2cdc-43aa-a9a9-08a02acc7113] received
[2026-03-23 04:06:08,028: INFO/MainProcess] Task tasks.scrape_pending_urls[1c769ccd-2cdc-43aa-a9a9-08a02acc7113] succeeded in 0.003077399975154549s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,029: INFO/MainProcess] Task tasks.scrape_pending_urls[58978ee5-b660-4ed9-ae5b-a6eb6010d035] received
[2026-03-23 04:06:08,032: INFO/MainProcess] Task tasks.scrape_pending_urls[58978ee5-b660-4ed9-ae5b-a6eb6010d035] succeeded in 0.002563200017903s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,034: INFO/MainProcess] Task tasks.scrape_pending_urls[27419239-5bb9-45e0-a537-a606613c7a80] received
[2026-03-23 04:06:08,037: INFO/MainProcess] Task tasks.scrape_pending_urls[27419239-5bb9-45e0-a537-a606613c7a80] succeeded in 0.003120600013062358s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,039: INFO/MainProcess] Task tasks.scrape_pending_urls[3bc78b47-a4ed-4ad3-ad53-151b50ae1848] received
[2026-03-23 04:06:08,042: INFO/MainProcess] Task tasks.scrape_pending_urls[3bc78b47-a4ed-4ad3-ad53-151b50ae1848] succeeded in 0.0024462000001221895s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,043: INFO/MainProcess] Task tasks.scrape_pending_urls[34dff62c-0321-46c5-a38c-c98b2d0630d6] received
[2026-03-23 04:06:08,046: INFO/MainProcess] Task tasks.scrape_pending_urls[34dff62c-0321-46c5-a38c-c98b2d0630d6] succeeded in 0.002499599999282509s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,048: INFO/MainProcess] Task tasks.scrape_pending_urls[c7e7e151-9c17-4b49-894d-45a3f518397c] received
[2026-03-23 04:06:08,051: INFO/MainProcess] Task tasks.scrape_pending_urls[c7e7e151-9c17-4b49-894d-45a3f518397c] succeeded in 0.0031241000397130847s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,054: INFO/MainProcess] Task tasks.scrape_pending_urls[30e403ca-4e48-46b0-9598-2ec9b41e6449] received
[2026-03-23 04:06:08,057: INFO/MainProcess] Task tasks.scrape_pending_urls[30e403ca-4e48-46b0-9598-2ec9b41e6449] succeeded in 0.0026919000083580613s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,058: INFO/MainProcess] Task tasks.scrape_pending_urls[fda4c8e6-3463-4dfe-b5a9-4ccfdc6290e5] received
[2026-03-23 04:06:08,061: INFO/MainProcess] Task tasks.scrape_pending_urls[fda4c8e6-3463-4dfe-b5a9-4ccfdc6290e5] succeeded in 0.0025962000363506377s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,063: INFO/MainProcess] Task tasks.scrape_pending_urls[3960a287-94c5-4b9a-9373-884052324507] received
[2026-03-23 04:06:08,066: INFO/MainProcess] Task tasks.scrape_pending_urls[3960a287-94c5-4b9a-9373-884052324507] succeeded in 0.002552300051320344s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,068: INFO/MainProcess] Task tasks.scrape_pending_urls[6828d929-a643-4a85-b3c1-9229012eb041] received
[2026-03-23 04:06:08,071: INFO/MainProcess] Task tasks.scrape_pending_urls[6828d929-a643-4a85-b3c1-9229012eb041] succeeded in 0.0030396999791264534s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,073: INFO/MainProcess] Task tasks.scrape_pending_urls[e7c65fcf-a993-4e55-ad86-9a2c470f1476] received
[2026-03-23 04:06:08,076: INFO/MainProcess] Task tasks.scrape_pending_urls[e7c65fcf-a993-4e55-ad86-9a2c470f1476] succeeded in 0.0028267999878153205s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,078: INFO/MainProcess] Task tasks.scrape_pending_urls[44960df0-aecd-43b7-8d07-d4229acc31e0] received
[2026-03-23 04:06:08,080: INFO/MainProcess] Task tasks.scrape_pending_urls[44960df0-aecd-43b7-8d07-d4229acc31e0] succeeded in 0.0023826000397093594s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,082: INFO/MainProcess] Task tasks.scrape_pending_urls[8d9979a6-ad6d-49bc-94de-898c5cbbbe91] received
[2026-03-23 04:06:08,085: INFO/MainProcess] Task tasks.scrape_pending_urls[8d9979a6-ad6d-49bc-94de-898c5cbbbe91] succeeded in 0.0031777999829500914s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,087: INFO/MainProcess] Task tasks.scrape_pending_urls[467b13d5-40ed-4885-8222-448cb9866dc7] received
[2026-03-23 04:06:08,090: INFO/MainProcess] Task tasks.scrape_pending_urls[467b13d5-40ed-4885-8222-448cb9866dc7] succeeded in 0.0024510000366717577s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,091: INFO/MainProcess] Task tasks.scrape_pending_urls[6d1c2955-e029-4d9e-bfa1-4c21c87e4084] received
[2026-03-23 04:06:08,094: INFO/MainProcess] Task tasks.scrape_pending_urls[6d1c2955-e029-4d9e-bfa1-4c21c87e4084] succeeded in 0.0024292999878525734s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,095: INFO/MainProcess] Task tasks.scrape_pending_urls[a97e5558-3e3c-42a0-b4a6-e138bcd16bbd] received
[2026-03-23 04:06:08,099: INFO/MainProcess] Task tasks.scrape_pending_urls[a97e5558-3e3c-42a0-b4a6-e138bcd16bbd] succeeded in 0.0028850999660789967s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,101: INFO/MainProcess] Task tasks.scrape_pending_urls[f4871039-ce00-4d9a-b1aa-a62af8336431] received
[2026-03-23 04:06:08,105: INFO/MainProcess] Task tasks.scrape_pending_urls[f4871039-ce00-4d9a-b1aa-a62af8336431] succeeded in 0.002805899945087731s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,106: INFO/MainProcess] Task tasks.scrape_pending_urls[a3e3407c-d61b-481a-bd97-a93c9b85ad76] received
[2026-03-23 04:06:08,110: INFO/MainProcess] Task tasks.scrape_pending_urls[a3e3407c-d61b-481a-bd97-a93c9b85ad76] succeeded in 0.0029388999682851136s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,111: INFO/MainProcess] Task tasks.scrape_pending_urls[46851584-ada9-481a-a83d-90cd1dfda6d8] received
[2026-03-23 04:06:08,116: INFO/MainProcess] Task tasks.scrape_pending_urls[46851584-ada9-481a-a83d-90cd1dfda6d8] succeeded in 0.0038443999947048724s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,119: INFO/MainProcess] Task tasks.scrape_pending_urls[4f67f4a1-31b9-43b8-ac21-797de6a0d193] received
[2026-03-23 04:06:08,123: INFO/MainProcess] Task tasks.scrape_pending_urls[4f67f4a1-31b9-43b8-ac21-797de6a0d193] succeeded in 0.0038531000027433038s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,125: INFO/MainProcess] Task tasks.scrape_pending_urls[2d244159-7bc9-44fa-be78-b01bf66ea949] received
[2026-03-23 04:06:08,129: INFO/MainProcess] Task tasks.scrape_pending_urls[2d244159-7bc9-44fa-be78-b01bf66ea949] succeeded in 0.0035923999967053533s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,133: INFO/MainProcess] Task tasks.scrape_pending_urls[5fa9cf0d-df6f-4ef5-93f5-9461ca945c90] received
[2026-03-23 04:06:08,136: INFO/MainProcess] Task tasks.scrape_pending_urls[5fa9cf0d-df6f-4ef5-93f5-9461ca945c90] succeeded in 0.0033181000035256147s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,138: INFO/MainProcess] Task tasks.scrape_pending_urls[3e0a6094-519f-4061-b72c-505c96cdb2cb] received
[2026-03-23 04:06:08,142: INFO/MainProcess] Task tasks.scrape_pending_urls[3e0a6094-519f-4061-b72c-505c96cdb2cb] succeeded in 0.003239799989387393s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,144: INFO/MainProcess] Task tasks.scrape_pending_urls[d4d80599-8225-4d70-8d07-6055710c176f] received
[2026-03-23 04:06:08,149: INFO/MainProcess] Task tasks.scrape_pending_urls[d4d80599-8225-4d70-8d07-6055710c176f] succeeded in 0.00477970001520589s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,151: INFO/MainProcess] Task tasks.scrape_pending_urls[f4f4c3dd-dba7-40a2-a173-d94c6ec738c2] received
[2026-03-23 04:06:08,155: INFO/MainProcess] Task tasks.scrape_pending_urls[f4f4c3dd-dba7-40a2-a173-d94c6ec738c2] succeeded in 0.003646400000434369s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,157: INFO/MainProcess] Task tasks.scrape_pending_urls[4aedcb53-bda1-4023-b86f-9bca5b039a92] received
[2026-03-23 04:06:08,161: INFO/MainProcess] Task tasks.scrape_pending_urls[4aedcb53-bda1-4023-b86f-9bca5b039a92] succeeded in 0.003479400009382516s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,163: INFO/MainProcess] Task tasks.scrape_pending_urls[653012de-c6e2-4e4b-9dab-7cc7e72ab5e1] received
[2026-03-23 04:06:08,167: INFO/MainProcess] Task tasks.scrape_pending_urls[653012de-c6e2-4e4b-9dab-7cc7e72ab5e1] succeeded in 0.0035191000206395984s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,169: INFO/MainProcess] Task tasks.scrape_pending_urls[9018a3bc-d053-49af-9944-3f964d67e8db] received
[2026-03-23 04:06:08,173: INFO/MainProcess] Task tasks.scrape_pending_urls[9018a3bc-d053-49af-9944-3f964d67e8db] succeeded in 0.0032556999940425158s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,175: INFO/MainProcess] Task tasks.scrape_pending_urls[d01bbfe7-4812-4709-b3b8-f8120653a4f1] received
[2026-03-23 04:06:08,178: INFO/MainProcess] Task tasks.scrape_pending_urls[d01bbfe7-4812-4709-b3b8-f8120653a4f1] succeeded in 0.0033634999999776483s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,181: INFO/MainProcess] Task tasks.scrape_pending_urls[f1dc07f9-6cc0-435c-9eb4-3539677882c3] received
[2026-03-23 04:06:08,185: INFO/MainProcess] Task tasks.scrape_pending_urls[f1dc07f9-6cc0-435c-9eb4-3539677882c3] succeeded in 0.0036831999896094203s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,187: INFO/MainProcess] Task tasks.scrape_pending_urls[e82a97ee-4042-4206-9ec7-74bae6479e48] received
[2026-03-23 04:06:08,191: INFO/MainProcess] Task tasks.scrape_pending_urls[e82a97ee-4042-4206-9ec7-74bae6479e48] succeeded in 0.003369299985934049s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,193: INFO/MainProcess] Task tasks.scrape_pending_urls[0803d8a8-7446-4d9c-be5f-c73bb92a5bcb] received
[2026-03-23 04:06:08,198: INFO/MainProcess] Task tasks.scrape_pending_urls[0803d8a8-7446-4d9c-be5f-c73bb92a5bcb] succeeded in 0.0036884999717585742s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,200: INFO/MainProcess] Task tasks.scrape_pending_urls[6639f3bf-5a50-42e7-aa65-16103d7e5141] received
[2026-03-23 04:06:08,203: INFO/MainProcess] Task tasks.scrape_pending_urls[6639f3bf-5a50-42e7-aa65-16103d7e5141] succeeded in 0.0032038000063039362s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,205: INFO/MainProcess] Task tasks.scrape_pending_urls[a9a354d8-11ba-4c6a-b0b4-4e835bfae2da] received
[2026-03-23 04:06:08,208: INFO/MainProcess] Task tasks.scrape_pending_urls[a9a354d8-11ba-4c6a-b0b4-4e835bfae2da] succeeded in 0.0029725999920628965s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,211: INFO/MainProcess] Task tasks.scrape_pending_urls[e745cf74-34ff-464a-ba69-7b8672eb8443] received
[2026-03-23 04:06:08,216: INFO/MainProcess] Task tasks.scrape_pending_urls[e745cf74-34ff-464a-ba69-7b8672eb8443] succeeded in 0.004210899991448969s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,218: INFO/MainProcess] Task tasks.scrape_pending_urls[0b40b7a3-0c85-40bb-9268-a1b26ade87c2] received
[2026-03-23 04:06:08,221: INFO/MainProcess] Task tasks.scrape_pending_urls[0b40b7a3-0c85-40bb-9268-a1b26ade87c2] succeeded in 0.0031054000137373805s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,223: INFO/MainProcess] Task tasks.scrape_pending_urls[9b59dec6-3574-4407-9722-c877002f47d0] received
[2026-03-23 04:06:08,227: INFO/MainProcess] Task tasks.scrape_pending_urls[9b59dec6-3574-4407-9722-c877002f47d0] succeeded in 0.003679599962197244s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,229: INFO/MainProcess] Task tasks.scrape_pending_urls[5593da82-536e-49b5-9f9d-c4b8e0dc2950] received
[2026-03-23 04:06:08,233: INFO/MainProcess] Task tasks.scrape_pending_urls[5593da82-536e-49b5-9f9d-c4b8e0dc2950] succeeded in 0.003172700002323836s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,234: INFO/MainProcess] Task tasks.scrape_pending_urls[52554507-0e2c-4c1e-bdc8-bdf91031e037] received
[2026-03-23 04:06:08,238: INFO/MainProcess] Task tasks.scrape_pending_urls[52554507-0e2c-4c1e-bdc8-bdf91031e037] succeeded in 0.0031755000236444175s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,240: INFO/MainProcess] Task tasks.scrape_pending_urls[90673196-07a9-4257-81f0-a79fbafad580] received
[2026-03-23 04:06:08,245: INFO/MainProcess] Task tasks.scrape_pending_urls[90673196-07a9-4257-81f0-a79fbafad580] succeeded in 0.004611200012732297s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,247: INFO/MainProcess] Task tasks.scrape_pending_urls[60e739c6-9b19-457c-9b5d-17e2a10d0dc9] received
[2026-03-23 04:06:08,250: INFO/MainProcess] Task tasks.scrape_pending_urls[60e739c6-9b19-457c-9b5d-17e2a10d0dc9] succeeded in 0.003222699975594878s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,252: INFO/MainProcess] Task tasks.scrape_pending_urls[85c9de48-6a1a-4fcf-9ed1-55991d55a956] received
[2026-03-23 04:06:08,256: INFO/MainProcess] Task tasks.scrape_pending_urls[85c9de48-6a1a-4fcf-9ed1-55991d55a956] succeeded in 0.0036374999908730388s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,259: INFO/MainProcess] Task tasks.scrape_pending_urls[facc90a1-8a7c-4259-a2e5-fc043a6edf23] received
[2026-03-23 04:06:08,263: INFO/MainProcess] Task tasks.scrape_pending_urls[facc90a1-8a7c-4259-a2e5-fc043a6edf23] succeeded in 0.0030808000010438263s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,265: INFO/MainProcess] Task tasks.scrape_pending_urls[1f7b7b1e-1758-4d4c-8b21-6feb49611f4f] received
[2026-03-23 04:06:08,269: INFO/MainProcess] Task tasks.scrape_pending_urls[1f7b7b1e-1758-4d4c-8b21-6feb49611f4f] succeeded in 0.0034683000412769616s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,271: INFO/MainProcess] Task tasks.scrape_pending_urls[ec65f63d-f225-4d86-a0f3-927b8f86590f] received
[2026-03-23 04:06:08,276: INFO/MainProcess] Task tasks.scrape_pending_urls[ec65f63d-f225-4d86-a0f3-927b8f86590f] succeeded in 0.004824900010135025s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,278: INFO/MainProcess] Task tasks.scrape_pending_urls[d111bb36-d80a-4546-bedb-231322186e8b] received
[2026-03-23 04:06:08,281: INFO/MainProcess] Task tasks.scrape_pending_urls[d111bb36-d80a-4546-bedb-231322186e8b] succeeded in 0.0031685999711044133s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,283: INFO/MainProcess] Task tasks.scrape_pending_urls[cc7fdc1c-9f0c-40b4-9f49-b4390b090de3] received
[2026-03-23 04:06:08,287: INFO/MainProcess] Task tasks.scrape_pending_urls[cc7fdc1c-9f0c-40b4-9f49-b4390b090de3] succeeded in 0.0030086999759078026s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,289: INFO/MainProcess] Task tasks.scrape_pending_urls[12c7f8da-15e2-415b-8aaa-4f6c2dfe614e] received
[2026-03-23 04:06:08,295: INFO/MainProcess] Task tasks.scrape_pending_urls[12c7f8da-15e2-415b-8aaa-4f6c2dfe614e] succeeded in 0.00497380003798753s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,298: INFO/MainProcess] Task tasks.scrape_pending_urls[e8a30d2f-9139-48ae-8aa1-ff7eba89eb7c] received
[2026-03-23 04:06:08,302: INFO/MainProcess] Task tasks.scrape_pending_urls[e8a30d2f-9139-48ae-8aa1-ff7eba89eb7c] succeeded in 0.004014600010123104s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,305: INFO/MainProcess] Task tasks.scrape_pending_urls[3c1b9f56-87e8-4cb7-b848-1074a645638a] received
[2026-03-23 04:06:08,309: INFO/MainProcess] Task tasks.scrape_pending_urls[3c1b9f56-87e8-4cb7-b848-1074a645638a] succeeded in 0.00412920000962913s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,311: INFO/MainProcess] Task tasks.scrape_pending_urls[ee7771c3-7bfa-44a2-8d8d-8781298b985f] received
[2026-03-23 04:06:08,315: INFO/MainProcess] Task tasks.scrape_pending_urls[ee7771c3-7bfa-44a2-8d8d-8781298b985f] succeeded in 0.0029393999720923603s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,317: INFO/MainProcess] Task tasks.scrape_pending_urls[815aaeaa-3ac5-4584-951a-6dfb3466090f] received
[2026-03-23 04:06:08,320: INFO/MainProcess] Task tasks.scrape_pending_urls[815aaeaa-3ac5-4584-951a-6dfb3466090f] succeeded in 0.003137800027616322s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,324: INFO/MainProcess] Task tasks.scrape_pending_urls[a0cd17ef-9c9f-43eb-8481-b68426a047ef] received
[2026-03-23 04:06:08,328: INFO/MainProcess] Task tasks.scrape_pending_urls[a0cd17ef-9c9f-43eb-8481-b68426a047ef] succeeded in 0.003928599995560944s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,330: INFO/MainProcess] Task tasks.scrape_pending_urls[514d737c-7942-4351-90ee-6d2806e2f964] received
[2026-03-23 04:06:08,333: INFO/MainProcess] Task tasks.scrape_pending_urls[514d737c-7942-4351-90ee-6d2806e2f964] succeeded in 0.0029956999933347106s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,335: INFO/MainProcess] Task tasks.scrape_pending_urls[20fa7da6-2fc7-43ad-a23b-a3076ed19795] received
[2026-03-23 04:06:08,339: INFO/MainProcess] Task tasks.scrape_pending_urls[20fa7da6-2fc7-43ad-a23b-a3076ed19795] succeeded in 0.004014000005554408s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,341: INFO/MainProcess] Task tasks.scrape_pending_urls[b0a04aa5-95fa-4d5d-a5f9-25994fea1790] received
[2026-03-23 04:06:08,345: INFO/MainProcess] Task tasks.scrape_pending_urls[b0a04aa5-95fa-4d5d-a5f9-25994fea1790] succeeded in 0.0029946999857202172s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,346: INFO/MainProcess] Task tasks.scrape_pending_urls[9390da6c-23fa-4444-8348-a7b235d7e060] received
[2026-03-23 04:06:08,350: INFO/MainProcess] Task tasks.scrape_pending_urls[9390da6c-23fa-4444-8348-a7b235d7e060] succeeded in 0.002924600034020841s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,352: INFO/MainProcess] Task tasks.scrape_pending_urls[05220c80-6c96-4fdf-866b-810463e74d80] received
[2026-03-23 04:06:08,357: INFO/MainProcess] Task tasks.scrape_pending_urls[05220c80-6c96-4fdf-866b-810463e74d80] succeeded in 0.004436600022017956s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,359: INFO/MainProcess] Task tasks.scrape_pending_urls[d53c1c78-c44d-4fe5-b69c-eef203bdedcf] received
[2026-03-23 04:06:08,363: INFO/MainProcess] Task tasks.scrape_pending_urls[d53c1c78-c44d-4fe5-b69c-eef203bdedcf] succeeded in 0.003308699990157038s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,365: INFO/MainProcess] Task tasks.scrape_pending_urls[0549aeca-86ad-4607-890d-716a0aa0b8f1] received
[2026-03-23 04:06:08,369: INFO/MainProcess] Task tasks.scrape_pending_urls[0549aeca-86ad-4607-890d-716a0aa0b8f1] succeeded in 0.0036774000036530197s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,371: INFO/MainProcess] Task tasks.scrape_pending_urls[a561aab9-a1d0-4600-be95-f7873d1e7efe] received
[2026-03-23 04:06:08,374: INFO/MainProcess] Task tasks.scrape_pending_urls[a561aab9-a1d0-4600-be95-f7873d1e7efe] succeeded in 0.003025100042577833s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,376: INFO/MainProcess] Task tasks.scrape_pending_urls[9a6a1f94-c561-4762-a5b4-4a826eb50615] received
[2026-03-23 04:06:08,380: INFO/MainProcess] Task tasks.scrape_pending_urls[9a6a1f94-c561-4762-a5b4-4a826eb50615] succeeded in 0.0032177999964915216s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,382: INFO/MainProcess] Task tasks.scrape_pending_urls[25aa331a-ae08-49fb-ad46-8e953931f9b2] received
[2026-03-23 04:06:08,386: INFO/MainProcess] Task tasks.scrape_pending_urls[25aa331a-ae08-49fb-ad46-8e953931f9b2] succeeded in 0.004422000027261674s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,388: INFO/MainProcess] Task tasks.scrape_pending_urls[7f231cb3-3894-4282-928b-c3f04182a6af] received
[2026-03-23 04:06:08,392: INFO/MainProcess] Task tasks.scrape_pending_urls[7f231cb3-3894-4282-928b-c3f04182a6af] succeeded in 0.0034700999967753887s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,394: INFO/MainProcess] Task tasks.scrape_pending_urls[81a298b5-36f3-4d25-9061-33b246c0059a] received
[2026-03-23 04:06:08,398: INFO/MainProcess] Task tasks.scrape_pending_urls[81a298b5-36f3-4d25-9061-33b246c0059a] succeeded in 0.0030994999688118696s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,399: INFO/MainProcess] Task tasks.scrape_pending_urls[1230de53-fa1b-4ff0-8a43-a699404823fa] received
[2026-03-23 04:06:08,405: INFO/MainProcess] Task tasks.scrape_pending_urls[1230de53-fa1b-4ff0-8a43-a699404823fa] succeeded in 0.0038105000276118517s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,407: INFO/MainProcess] Task tasks.scrape_pending_urls[a0044bf4-9f94-4437-8a38-37c83c5af94e] received
[2026-03-23 04:06:08,410: INFO/MainProcess] Task tasks.scrape_pending_urls[a0044bf4-9f94-4437-8a38-37c83c5af94e] succeeded in 0.003153499972540885s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,412: INFO/MainProcess] Task tasks.scrape_pending_urls[b69cd215-a3b1-4fce-82e9-1361fe7d336c] received
[2026-03-23 04:06:08,416: INFO/MainProcess] Task tasks.scrape_pending_urls[b69cd215-a3b1-4fce-82e9-1361fe7d336c] succeeded in 0.0035803000209853053s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,418: INFO/MainProcess] Task tasks.scrape_pending_urls[9ff78ac2-6ae0-45f6-b35e-67f974d75807] received
[2026-03-23 04:06:08,422: INFO/MainProcess] Task tasks.scrape_pending_urls[9ff78ac2-6ae0-45f6-b35e-67f974d75807] succeeded in 0.0033355000196024776s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,424: INFO/MainProcess] Task tasks.scrape_pending_urls[8b9a22ff-a085-48e9-9135-6321abbd7961] received
[2026-03-23 04:06:08,428: INFO/MainProcess] Task tasks.scrape_pending_urls[8b9a22ff-a085-48e9-9135-6321abbd7961] succeeded in 0.003050300001632422s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,429: INFO/MainProcess] Task tasks.scrape_pending_urls[3c5a7582-f033-4552-ad6b-3b67900199b4] received
[2026-03-23 04:06:08,434: INFO/MainProcess] Task tasks.scrape_pending_urls[3c5a7582-f033-4552-ad6b-3b67900199b4] succeeded in 0.0042773999739438295s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,436: INFO/MainProcess] Task tasks.scrape_pending_urls[19bc5325-e75e-4693-a83a-d35627687eae] received
[2026-03-23 04:06:08,440: INFO/MainProcess] Task tasks.scrape_pending_urls[19bc5325-e75e-4693-a83a-d35627687eae] succeeded in 0.0033224999788217247s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,442: INFO/MainProcess] Task tasks.scrape_pending_urls[c9366034-ab6e-46cf-862c-e9ff7b0b28fe] received
[2026-03-23 04:06:08,446: INFO/MainProcess] Task tasks.scrape_pending_urls[c9366034-ab6e-46cf-862c-e9ff7b0b28fe] succeeded in 0.0035183000145480037s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,448: INFO/MainProcess] Task tasks.scrape_pending_urls[8292f91a-37fe-4413-8a61-3b3f51cbb8f5] received
[2026-03-23 04:06:08,452: INFO/MainProcess] Task tasks.scrape_pending_urls[8292f91a-37fe-4413-8a61-3b3f51cbb8f5] succeeded in 0.0031346000032499433s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,454: INFO/MainProcess] Task tasks.scrape_pending_urls[9602490b-7035-487d-a0ab-1aad0db67544] received
[2026-03-23 04:06:08,457: INFO/MainProcess] Task tasks.scrape_pending_urls[9602490b-7035-487d-a0ab-1aad0db67544] succeeded in 0.002792100014630705s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,458: INFO/MainProcess] Task tasks.scrape_pending_urls[bb356804-d7a4-4d77-b369-5c4962bc66aa] received
[2026-03-23 04:06:08,462: INFO/MainProcess] Task tasks.scrape_pending_urls[bb356804-d7a4-4d77-b369-5c4962bc66aa] succeeded in 0.002973099995870143s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,465: INFO/MainProcess] Task tasks.scrape_pending_urls[93ddc0e4-0804-4ffe-8f83-70ff5babcaf5] received
[2026-03-23 04:06:08,468: INFO/MainProcess] Task tasks.scrape_pending_urls[93ddc0e4-0804-4ffe-8f83-70ff5babcaf5] succeeded in 0.003132399986498058s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,470: INFO/MainProcess] Task tasks.scrape_pending_urls[987dd07e-e84f-43db-b7d7-1b8c9d72903e] received
[2026-03-23 04:06:08,474: INFO/MainProcess] Task tasks.scrape_pending_urls[987dd07e-e84f-43db-b7d7-1b8c9d72903e] succeeded in 0.0030462000286206603s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,475: INFO/MainProcess] Task tasks.scrape_pending_urls[8ab7461d-149b-456e-95cf-ee37df0d0667] received
[2026-03-23 04:06:08,479: INFO/MainProcess] Task tasks.scrape_pending_urls[8ab7461d-149b-456e-95cf-ee37df0d0667] succeeded in 0.0034607999841682613s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,482: INFO/MainProcess] Task tasks.scrape_pending_urls[ec0bedb8-0c90-486d-ba4d-adf7dd0adb1b] received
[2026-03-23 04:06:08,486: INFO/MainProcess] Task tasks.scrape_pending_urls[ec0bedb8-0c90-486d-ba4d-adf7dd0adb1b] succeeded in 0.003751700045540929s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,488: INFO/MainProcess] Task tasks.scrape_pending_urls[9c4675c4-3ed2-4c73-8b54-902a0f6d89ca] received
[2026-03-23 04:06:08,491: INFO/MainProcess] Task tasks.scrape_pending_urls[9c4675c4-3ed2-4c73-8b54-902a0f6d89ca] succeeded in 0.0031006000353954732s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,493: INFO/MainProcess] Task tasks.scrape_pending_urls[20a7de51-605c-4f8d-b3c2-514b0acb94e9] received
[2026-03-23 04:06:08,498: INFO/MainProcess] Task tasks.scrape_pending_urls[20a7de51-605c-4f8d-b3c2-514b0acb94e9] succeeded in 0.004349099996034056s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,500: INFO/MainProcess] Task tasks.scrape_pending_urls[6449bcd4-674b-47bc-85a8-420b166eebcd] received
[2026-03-23 04:06:08,503: INFO/MainProcess] Task tasks.scrape_pending_urls[6449bcd4-674b-47bc-85a8-420b166eebcd] succeeded in 0.0029874000465497375s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,505: INFO/MainProcess] Task tasks.scrape_pending_urls[694f2426-3470-4b23-8be2-88b61775b1db] received
[2026-03-23 04:06:08,509: INFO/MainProcess] Task tasks.scrape_pending_urls[694f2426-3470-4b23-8be2-88b61775b1db] succeeded in 0.0031593000167049468s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,511: INFO/MainProcess] Task tasks.scrape_pending_urls[46860dd1-c76f-4439-9fcf-b789f066e015] received
[2026-03-23 04:06:08,516: INFO/MainProcess] Task tasks.scrape_pending_urls[46860dd1-c76f-4439-9fcf-b789f066e015] succeeded in 0.004639599996153265s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,518: INFO/MainProcess] Task tasks.scrape_pending_urls[929a10e0-d809-402b-be19-7eb8e2f5cd4f] received
[2026-03-23 04:06:08,521: INFO/MainProcess] Task tasks.scrape_pending_urls[929a10e0-d809-402b-be19-7eb8e2f5cd4f] succeeded in 0.0029429999995045364s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,523: INFO/MainProcess] Task tasks.scrape_pending_urls[fe8a7c89-b72c-4be3-8568-3bfd16bfb4bd] received
[2026-03-23 04:06:08,526: INFO/MainProcess] Task tasks.scrape_pending_urls[fe8a7c89-b72c-4be3-8568-3bfd16bfb4bd] succeeded in 0.0027280999929644167s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,529: INFO/MainProcess] Task tasks.scrape_pending_urls[8accd54d-084b-4de6-bf45-493528a8782c] received
[2026-03-23 04:06:08,532: INFO/MainProcess] Task tasks.scrape_pending_urls[8accd54d-084b-4de6-bf45-493528a8782c] succeeded in 0.003107599972281605s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,534: INFO/MainProcess] Task tasks.scrape_pending_urls[23e63815-b5f1-4791-877b-146a9ea9015e] received
[2026-03-23 04:06:08,538: INFO/MainProcess] Task tasks.scrape_pending_urls[23e63815-b5f1-4791-877b-146a9ea9015e] succeeded in 0.0030089999781921506s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,539: INFO/MainProcess] Task tasks.scrape_pending_urls[ac594b2d-cda5-4677-a90d-3b3750f17240] received
[2026-03-23 04:06:08,545: INFO/MainProcess] Task tasks.scrape_pending_urls[ac594b2d-cda5-4677-a90d-3b3750f17240] succeeded in 0.004788000020198524s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,547: INFO/MainProcess] Task tasks.scrape_pending_urls[da0ae43d-f58e-4d7c-a905-ecb7651e6956] received
[2026-03-23 04:06:08,550: INFO/MainProcess] Task tasks.scrape_pending_urls[da0ae43d-f58e-4d7c-a905-ecb7651e6956] succeeded in 0.003458099963609129s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,552: INFO/MainProcess] Task tasks.scrape_pending_urls[9e5ce5da-b46a-4784-8118-7a03f4976b7e] received
[2026-03-23 04:06:08,556: INFO/MainProcess] Task tasks.scrape_pending_urls[9e5ce5da-b46a-4784-8118-7a03f4976b7e] succeeded in 0.003191600029822439s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,558: INFO/MainProcess] Task tasks.scrape_pending_urls[eaca9529-70be-489d-8f92-86585e41f4d1] received
[2026-03-23 04:06:08,563: INFO/MainProcess] Task tasks.scrape_pending_urls[eaca9529-70be-489d-8f92-86585e41f4d1] succeeded in 0.003950500045903027s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,565: INFO/MainProcess] Task tasks.scrape_pending_urls[fd1f175a-ad14-4e8a-bc08-c9ad2fa8ee35] received
[2026-03-23 04:06:08,569: INFO/MainProcess] Task tasks.scrape_pending_urls[fd1f175a-ad14-4e8a-bc08-c9ad2fa8ee35] succeeded in 0.0034612000454217196s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,571: INFO/MainProcess] Task tasks.scrape_pending_urls[2c329ab2-eb41-441b-8ccf-ce345867b36e] received
[2026-03-23 04:06:08,575: INFO/MainProcess] Task tasks.scrape_pending_urls[2c329ab2-eb41-441b-8ccf-ce345867b36e] succeeded in 0.0033454999793320894s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,577: INFO/MainProcess] Task tasks.scrape_pending_urls[646cce1b-25dc-4ebc-937b-5ff046560022] received
[2026-03-23 04:06:08,580: INFO/MainProcess] Task tasks.scrape_pending_urls[646cce1b-25dc-4ebc-937b-5ff046560022] succeeded in 0.0030170000391080976s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,582: INFO/MainProcess] Task tasks.scrape_pending_urls[383921ff-eb77-4db7-8bd0-81efb4fec327] received
[2026-03-23 04:06:08,586: INFO/MainProcess] Task tasks.scrape_pending_urls[383921ff-eb77-4db7-8bd0-81efb4fec327] succeeded in 0.003341900010127574s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,588: INFO/MainProcess] Task tasks.scrape_pending_urls[337701b0-3b32-40af-9034-867658e57c3d] received
[2026-03-23 04:06:08,593: INFO/MainProcess] Task tasks.scrape_pending_urls[337701b0-3b32-40af-9034-867658e57c3d] succeeded in 0.004387799999676645s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,595: INFO/MainProcess] Task tasks.scrape_pending_urls[905bb06b-43c7-44dc-85f8-2d5c0fdc947e] received
[2026-03-23 04:06:08,598: INFO/MainProcess] Task tasks.scrape_pending_urls[905bb06b-43c7-44dc-85f8-2d5c0fdc947e] succeeded in 0.0030220000189729035s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,600: INFO/MainProcess] Task tasks.scrape_pending_urls[f03575c5-e44d-4119-9838-da46685d0bfe] received
[2026-03-23 04:06:08,602: INFO/MainProcess] Task tasks.scrape_pending_urls[f03575c5-e44d-4119-9838-da46685d0bfe] succeeded in 0.002262100053485483s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,603: INFO/MainProcess] Task tasks.scrape_pending_urls[2ba3e3b3-d058-4067-8d2f-1d656942d032] received
[2026-03-23 04:06:08,607: INFO/MainProcess] Task tasks.scrape_pending_urls[2ba3e3b3-d058-4067-8d2f-1d656942d032] succeeded in 0.00344030000269413s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,609: INFO/MainProcess] Task tasks.scrape_pending_urls[ec077ee0-097e-44a5-ad21-e7e8c758fa76] received
[2026-03-23 04:06:08,612: INFO/MainProcess] Task tasks.scrape_pending_urls[ec077ee0-097e-44a5-ad21-e7e8c758fa76] succeeded in 0.0029513000044971704s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,614: INFO/MainProcess] Task tasks.scrape_pending_urls[89a811a5-0499-4be8-a761-0f44503a9c33] received
[2026-03-23 04:06:08,617: INFO/MainProcess] Task tasks.scrape_pending_urls[89a811a5-0499-4be8-a761-0f44503a9c33] succeeded in 0.003069200029131025s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,619: INFO/MainProcess] Task tasks.scrape_pending_urls[d2e1c0c3-d4db-44c4-b380-42b5a8dadfbc] received
[2026-03-23 04:06:08,624: INFO/MainProcess] Task tasks.scrape_pending_urls[d2e1c0c3-d4db-44c4-b380-42b5a8dadfbc] succeeded in 0.004579400003422052s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,626: INFO/MainProcess] Task tasks.scrape_pending_urls[34f397e9-f950-4890-8d19-06b8cadb4073] received
[2026-03-23 04:06:08,629: INFO/MainProcess] Task tasks.scrape_pending_urls[34f397e9-f950-4890-8d19-06b8cadb4073] succeeded in 0.00287730002310127s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,631: INFO/MainProcess] Task tasks.scrape_pending_urls[175856b8-8645-412e-a75e-41643169b117] received
[2026-03-23 04:06:08,634: INFO/MainProcess] Task tasks.scrape_pending_urls[175856b8-8645-412e-a75e-41643169b117] succeeded in 0.0028415999840945005s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,636: INFO/MainProcess] Task tasks.scrape_pending_urls[c79a3a4f-1720-41bf-9f61-c77df745176a] received
[2026-03-23 04:06:08,640: INFO/MainProcess] Task tasks.scrape_pending_urls[c79a3a4f-1720-41bf-9f61-c77df745176a] succeeded in 0.004286800045520067s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,642: INFO/MainProcess] Task tasks.scrape_pending_urls[81653284-f1ac-4ebc-9a7d-629d339ce745] received
[2026-03-23 04:06:08,646: INFO/MainProcess] Task tasks.scrape_pending_urls[81653284-f1ac-4ebc-9a7d-629d339ce745] succeeded in 0.003698499989695847s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,648: INFO/MainProcess] Task tasks.scrape_pending_urls[9964423a-ea02-47e0-ba84-0690f886fb64] received
[2026-03-23 04:06:08,652: INFO/MainProcess] Task tasks.scrape_pending_urls[9964423a-ea02-47e0-ba84-0690f886fb64] succeeded in 0.0033378000371158123s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,654: INFO/MainProcess] Task tasks.scrape_pending_urls[4a9c0c56-716c-4744-90cf-d415f6bc6ee3] received
[2026-03-23 04:06:08,658: INFO/MainProcess] Task tasks.scrape_pending_urls[4a9c0c56-716c-4744-90cf-d415f6bc6ee3] succeeded in 0.0034379000426270068s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,660: INFO/MainProcess] Task tasks.scrape_pending_urls[04956a9b-da36-4680-ba5d-5f308d2c0a3a] received
[2026-03-23 04:06:08,664: INFO/MainProcess] Task tasks.scrape_pending_urls[04956a9b-da36-4680-ba5d-5f308d2c0a3a] succeeded in 0.003356900007929653s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,666: INFO/MainProcess] Task tasks.scrape_pending_urls[b12671c3-6793-4ec6-aa15-4cfe0ebfee0d] received
[2026-03-23 04:06:08,670: INFO/MainProcess] Task tasks.scrape_pending_urls[b12671c3-6793-4ec6-aa15-4cfe0ebfee0d] succeeded in 0.004113800008781254s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,672: INFO/MainProcess] Task tasks.scrape_pending_urls[380791ef-cd85-4a36-ab68-cd7472d44d23] received
[2026-03-23 04:06:08,676: INFO/MainProcess] Task tasks.scrape_pending_urls[380791ef-cd85-4a36-ab68-cd7472d44d23] succeeded in 0.0034966999664902687s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,678: INFO/MainProcess] Task tasks.scrape_pending_urls[42e653ff-5b14-4477-b3a4-cd38cca0e160] received
[2026-03-23 04:06:08,682: INFO/MainProcess] Task tasks.scrape_pending_urls[42e653ff-5b14-4477-b3a4-cd38cca0e160] succeeded in 0.0031423000036738813s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,683: INFO/MainProcess] Task tasks.scrape_pending_urls[17c62d14-7b83-48a5-8a4d-065a255622bc] received
[2026-03-23 04:06:08,688: INFO/MainProcess] Task tasks.scrape_pending_urls[17c62d14-7b83-48a5-8a4d-065a255622bc] succeeded in 0.004113300004974008s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,690: INFO/MainProcess] Task tasks.scrape_pending_urls[535fb092-fc69-4401-ac6f-8e5fc6ad88ed] received
[2026-03-23 04:06:08,692: INFO/MainProcess] Task tasks.scrape_pending_urls[535fb092-fc69-4401-ac6f-8e5fc6ad88ed] succeeded in 0.0025481999618932605s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,694: INFO/MainProcess] Task tasks.scrape_pending_urls[1140c2b2-7cd5-4be0-9362-babae00b915b] received
[2026-03-23 04:06:08,696: INFO/MainProcess] Task tasks.scrape_pending_urls[1140c2b2-7cd5-4be0-9362-babae00b915b] succeeded in 0.002315899997483939s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,698: INFO/MainProcess] Task tasks.scrape_pending_urls[01849901-41f2-45a1-bd1f-0a845b04f4c1] received
[2026-03-23 04:06:08,701: INFO/MainProcess] Task tasks.scrape_pending_urls[01849901-41f2-45a1-bd1f-0a845b04f4c1] succeeded in 0.0032961999531835318s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,703: INFO/MainProcess] Task tasks.scrape_pending_urls[78e9e47d-03d0-47f4-bf32-0fe49bcfedfd] received
[2026-03-23 04:06:08,705: INFO/MainProcess] Task tasks.scrape_pending_urls[78e9e47d-03d0-47f4-bf32-0fe49bcfedfd] succeeded in 0.002373000024817884s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,707: INFO/MainProcess] Task tasks.scrape_pending_urls[9a0dc4f1-85d8-4663-8a3f-945d0eb99967] received
[2026-03-23 04:06:08,709: INFO/MainProcess] Task tasks.scrape_pending_urls[9a0dc4f1-85d8-4663-8a3f-945d0eb99967] succeeded in 0.0022368000354617834s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,710: INFO/MainProcess] Task tasks.scrape_pending_urls[cba7d8b9-39b2-4d96-9b3a-2c0e5ff3cd2d] received
[2026-03-23 04:06:08,713: INFO/MainProcess] Task tasks.scrape_pending_urls[cba7d8b9-39b2-4d96-9b3a-2c0e5ff3cd2d] succeeded in 0.0022540000500157475s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:08,714: INFO/MainProcess] Task tasks.scrape_pending_urls[4dc812a3-b941-4ca7-81f7-5306b22d2c03] received
[2026-03-23 04:06:08,717: INFO/MainProcess] Task tasks.scrape_pending_urls[4dc812a3-b941-4ca7-81f7-5306b22d2c03] succeeded in 0.002763299969956279s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:06:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[055501fd-5ed9-468d-9e3e-c398b2edfd73] received
[2026-03-23 04:06:33,477: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 04:06:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[055501fd-5ed9-468d-9e3e-c398b2edfd73] succeeded in 0.004558200016617775s: {'reset': 0}
[2026-03-23 04:06:33,480: INFO/MainProcess] Task tasks.collect_system_metrics[9abc89e8-ba67-43ce-8b4d-fbc5198ed432] received
[2026-03-23 04:06:33,997: INFO/MainProcess] Task tasks.collect_system_metrics[9abc89e8-ba67-43ce-8b4d-fbc5198ed432] succeeded in 0.5167846999829635s: {'cpu': 16.3, 'memory': 40.3}
[2026-03-23 04:06:33,999: INFO/MainProcess] Task tasks.scrape_pending_urls[47ad751a-936c-44b7-955e-b6764c646e9b] received
[2026-03-23 04:06:34,003: INFO/MainProcess] Task tasks.scrape_pending_urls[47ad751a-936c-44b7-955e-b6764c646e9b] succeeded in 0.0032232999801635742s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:07:03,686: INFO/MainProcess] Task tasks.scrape_pending_urls[5b68bf36-c6a1-4033-af4d-366aa2d72e46] received
[2026-03-23 04:07:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[5b68bf36-c6a1-4033-af4d-366aa2d72e46] succeeded in 0.002888799994252622s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:07:33,686: INFO/MainProcess] Task tasks.scrape_pending_urls[f4b4abf8-e5df-4b98-bb73-83fa18899f15] received
[2026-03-23 04:07:33,689: INFO/MainProcess] Task tasks.scrape_pending_urls[f4b4abf8-e5df-4b98-bb73-83fa18899f15] succeeded in 0.003032499982509762s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:08:03,685: INFO/MainProcess] Task tasks.scrape_pending_urls[abd892fb-cbd4-4578-bb79-3087204800e6] received
[2026-03-23 04:08:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[abd892fb-cbd4-4578-bb79-3087204800e6] succeeded in 0.003106699965428561s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:08:33,686: INFO/MainProcess] Task tasks.scrape_pending_urls[5e2c9f2f-b36e-4b1a-bcaa-e7cbf91651cf] received
[2026-03-23 04:08:33,689: INFO/MainProcess] Task tasks.scrape_pending_urls[5e2c9f2f-b36e-4b1a-bcaa-e7cbf91651cf] succeeded in 0.003077699977438897s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:09:03,686: INFO/MainProcess] Task tasks.scrape_pending_urls[ba4feb51-630d-4881-a365-7df48bff2aaf] received
[2026-03-23 04:09:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[ba4feb51-630d-4881-a365-7df48bff2aaf] succeeded in 0.0030183999915607274s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:09:33,690: INFO/MainProcess] Task tasks.scrape_pending_urls[61a1da38-d9e7-49d3-8ca1-e2a48535c65c] received
[2026-03-23 04:09:33,693: INFO/MainProcess] Task tasks.scrape_pending_urls[61a1da38-d9e7-49d3-8ca1-e2a48535c65c] succeeded in 0.0030161000322550535s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:10:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[23128197-4448-444b-9f8c-9339c3c39a0f] received
[2026-03-23 04:10:03,693: INFO/MainProcess] Task tasks.scrape_pending_urls[23128197-4448-444b-9f8c-9339c3c39a0f] succeeded in 0.0030948000494390726s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:10:33,690: INFO/MainProcess] Task tasks.scrape_pending_urls[d760c6b2-8d79-4903-924a-8b4c476edebd] received
[2026-03-23 04:10:33,693: INFO/MainProcess] Task tasks.scrape_pending_urls[d760c6b2-8d79-4903-924a-8b4c476edebd] succeeded in 0.00315429997863248s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:11:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[a133b08a-affc-47fa-9809-e59509cbed05] received
[2026-03-23 04:11:03,758: INFO/MainProcess] Task tasks.scrape_pending_urls[a133b08a-affc-47fa-9809-e59509cbed05] succeeded in 0.06779789994470775s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:11:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[2224c01e-432a-42c6-8d30-088e42509fb1] received
[2026-03-23 04:11:33,995: INFO/MainProcess] Task tasks.collect_system_metrics[2224c01e-432a-42c6-8d30-088e42509fb1] succeeded in 0.5168764999834821s: {'cpu': 17.1, 'memory': 40.4}
[2026-03-23 04:11:33,997: INFO/MainProcess] Task tasks.scrape_pending_urls[00d7e789-905b-4ad1-b122-11b5a32157c4] received
[2026-03-23 04:11:34,066: INFO/MainProcess] Task tasks.scrape_pending_urls[00d7e789-905b-4ad1-b122-11b5a32157c4] succeeded in 0.06824890000279993s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:12:03,690: INFO/MainProcess] Task tasks.scrape_pending_urls[9360d2e3-b847-47a4-8af7-142ec6ce54c7] received
[2026-03-23 04:12:03,693: INFO/MainProcess] Task tasks.scrape_pending_urls[9360d2e3-b847-47a4-8af7-142ec6ce54c7] succeeded in 0.00329070002771914s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:12:33,690: INFO/MainProcess] Task tasks.scrape_pending_urls[c8593e53-66ec-4324-8e22-865fc67b77ff] received
[2026-03-23 04:12:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[c8593e53-66ec-4324-8e22-865fc67b77ff] succeeded in 0.0034691000473685563s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:13:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[78565d6b-e305-4435-ace8-644b54b3c722] received
[2026-03-23 04:13:03,693: INFO/MainProcess] Task tasks.scrape_pending_urls[78565d6b-e305-4435-ace8-644b54b3c722] succeeded in 0.0032818999607115984s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:13:33,689: INFO/MainProcess] Task tasks.scrape_pending_urls[26901354-c26c-4b2d-aef0-64d0c2ac7a8f] received
[2026-03-23 04:13:33,693: INFO/MainProcess] Task tasks.scrape_pending_urls[26901354-c26c-4b2d-aef0-64d0c2ac7a8f] succeeded in 0.0033571000094525516s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:14:03,690: INFO/MainProcess] Task tasks.scrape_pending_urls[c46ed526-d56d-417c-9cfa-976c16b9261d] received
[2026-03-23 04:14:03,693: INFO/MainProcess] Task tasks.scrape_pending_urls[c46ed526-d56d-417c-9cfa-976c16b9261d] succeeded in 0.0031294000218622386s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:14:33,690: INFO/MainProcess] Task tasks.scrape_pending_urls[8d4c9082-96e0-4585-8ea1-b1f64f11c4f7] received
[2026-03-23 04:14:33,693: INFO/MainProcess] Task tasks.scrape_pending_urls[8d4c9082-96e0-4585-8ea1-b1f64f11c4f7] succeeded in 0.0032818999607115984s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:15:03,689: INFO/MainProcess] Task tasks.scrape_pending_urls[9fb4165e-9c4c-42af-802e-2f7fc9d52c32] received
[2026-03-23 04:15:03,693: INFO/MainProcess] Task tasks.scrape_pending_urls[9fb4165e-9c4c-42af-802e-2f7fc9d52c32] succeeded in 0.003172400000039488s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:15:33,690: INFO/MainProcess] Task tasks.scrape_pending_urls[ca35fbcd-eead-4ac1-aeea-e958c539967f] received
[2026-03-23 04:15:33,693: INFO/MainProcess] Task tasks.scrape_pending_urls[ca35fbcd-eead-4ac1-aeea-e958c539967f] succeeded in 0.0031163000385276973s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:16:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[6f4b66c3-c2ff-4a9d-9325-f1641b4949ee] received
[2026-03-23 04:16:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[6f4b66c3-c2ff-4a9d-9325-f1641b4949ee] succeeded in 0.0033147999783977866s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:16:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[7826c861-f5fe-49eb-851e-1fa3a85bcb4b] received
[2026-03-23 04:16:33,988: INFO/MainProcess] Task tasks.collect_system_metrics[7826c861-f5fe-49eb-851e-1fa3a85bcb4b] succeeded in 0.5087290999945253s: {'cpu': 20.6, 'memory': 40.3}
[2026-03-23 04:16:33,990: INFO/MainProcess] Task tasks.scrape_pending_urls[aeaa8fc9-a7eb-448e-953c-ad7882f7c92a] received
[2026-03-23 04:16:33,994: INFO/MainProcess] Task tasks.scrape_pending_urls[aeaa8fc9-a7eb-448e-953c-ad7882f7c92a] succeeded in 0.003343600023072213s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:17:03,693: INFO/MainProcess] Task tasks.scrape_pending_urls[b8a673a5-864a-41c3-8858-a16c4dd47200] received
[2026-03-23 04:17:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[b8a673a5-864a-41c3-8858-a16c4dd47200] succeeded in 0.0033572999527677894s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:17:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[d1747a76-2559-4149-b57f-998ce0bd3024] received
[2026-03-23 04:17:33,697: INFO/MainProcess] Task tasks.scrape_pending_urls[d1747a76-2559-4149-b57f-998ce0bd3024] succeeded in 0.003064399992581457s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:18:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[50f83605-c868-43d6-81c4-eb3c905e8e62] received
[2026-03-23 04:18:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[50f83605-c868-43d6-81c4-eb3c905e8e62] succeeded in 0.062401400005910546s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:18:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[dd719187-60de-43df-936d-a937da873cd9] received
[2026-03-23 04:18:33,697: INFO/MainProcess] Task tasks.scrape_pending_urls[dd719187-60de-43df-936d-a937da873cd9] succeeded in 0.0032275000121444464s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:19:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[0d5499c0-6f21-4ad5-9166-e38788e9914f] received
[2026-03-23 04:19:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[0d5499c0-6f21-4ad5-9166-e38788e9914f] succeeded in 0.0030763999675400555s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:19:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[b54db567-d7a8-444a-8a6b-d05d89b58241] received
[2026-03-23 04:19:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[b54db567-d7a8-444a-8a6b-d05d89b58241] succeeded in 0.003268199972808361s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:20:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[cb83e59f-ff39-4ad5-b61e-28c2659442d7] received
[2026-03-23 04:20:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[cb83e59f-ff39-4ad5-b61e-28c2659442d7] succeeded in 0.003252199967391789s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:20:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[09d525be-b003-49b5-9373-4f46a45c8750] received
[2026-03-23 04:20:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[09d525be-b003-49b5-9373-4f46a45c8750] succeeded in 0.0033455999800935388s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:21:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[3b4d064d-f2c7-4dc8-b525-06dfd272a0eb] received
[2026-03-23 04:21:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[3b4d064d-f2c7-4dc8-b525-06dfd272a0eb] succeeded in 0.0036762000527232885s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:21:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[1274335b-4138-46fb-87da-001536bd61db] received
[2026-03-23 04:21:33,997: INFO/MainProcess] Task tasks.collect_system_metrics[1274335b-4138-46fb-87da-001536bd61db] succeeded in 0.5185323000187054s: {'cpu': 16.1, 'memory': 40.0}
[2026-03-23 04:21:33,999: INFO/MainProcess] Task tasks.scrape_pending_urls[cfae6f02-96a9-4b3b-ac3b-5250256cdf83] received
[2026-03-23 04:21:34,003: INFO/MainProcess] Task tasks.scrape_pending_urls[cfae6f02-96a9-4b3b-ac3b-5250256cdf83] succeeded in 0.0034886000212281942s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:22:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[ec162d30-46b8-49e6-b0d1-8e641e4b39ba] received
[2026-03-23 04:22:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[ec162d30-46b8-49e6-b0d1-8e641e4b39ba] succeeded in 0.0030911999638192356s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:22:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[e7b4ba9b-574d-45de-8799-49bca81a933a] received
[2026-03-23 04:22:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[e7b4ba9b-574d-45de-8799-49bca81a933a] succeeded in 0.0033292999723926187s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:23:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[1be16c17-fff1-4317-a71f-2e46a84235a6] received
[2026-03-23 04:23:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[1be16c17-fff1-4317-a71f-2e46a84235a6] succeeded in 0.003098800021689385s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:23:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[4de5daef-24c4-48c3-8091-985aee461dd7] received
[2026-03-23 04:23:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[4de5daef-24c4-48c3-8091-985aee461dd7] succeeded in 0.003466400026809424s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:24:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[b5648a0b-cdde-4bd9-be61-16893a78176d] received
[2026-03-23 04:24:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[b5648a0b-cdde-4bd9-be61-16893a78176d] succeeded in 0.0032495000050403178s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:24:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[de1abc4f-7cb8-4543-b20f-c05f74caf44a] received
[2026-03-23 04:24:33,697: INFO/MainProcess] Task tasks.scrape_pending_urls[de1abc4f-7cb8-4543-b20f-c05f74caf44a] succeeded in 0.0029625000315718353s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:25:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[a0aca6f2-284e-4b99-80b6-79a05e05806a] received
[2026-03-23 04:25:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[a0aca6f2-284e-4b99-80b6-79a05e05806a] succeeded in 0.0034291999763809144s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:25:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[3f8b5c72-aae5-456a-9217-dc28b7eea974] received
[2026-03-23 04:25:33,697: INFO/MainProcess] Task tasks.scrape_pending_urls[3f8b5c72-aae5-456a-9217-dc28b7eea974] succeeded in 0.00303429999621585s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:26:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[46e09744-ba97-4c22-8fed-e86608e2e174] received
[2026-03-23 04:26:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[46e09744-ba97-4c22-8fed-e86608e2e174] succeeded in 0.0032358000171370804s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:26:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[97a07b79-015a-434e-abb6-7094e2609016] received
[2026-03-23 04:26:33,997: INFO/MainProcess] Task tasks.collect_system_metrics[97a07b79-015a-434e-abb6-7094e2609016] succeeded in 0.5189325000392273s: {'cpu': 14.1, 'memory': 40.5}
[2026-03-23 04:26:33,999: INFO/MainProcess] Task tasks.scrape_pending_urls[b2676d28-e47c-40be-bf4c-663c1a256bcb] received
[2026-03-23 04:26:34,003: INFO/MainProcess] Task tasks.scrape_pending_urls[b2676d28-e47c-40be-bf4c-663c1a256bcb] succeeded in 0.0035880000214092433s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:27:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[40906c15-4f53-4de2-b17f-72c9e51ea419] received
[2026-03-23 04:27:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[40906c15-4f53-4de2-b17f-72c9e51ea419] succeeded in 0.003306900034658611s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:27:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[8caecd18-c913-4ad8-a7db-426162af794e] received
[2026-03-23 04:27:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[8caecd18-c913-4ad8-a7db-426162af794e] succeeded in 0.0034177000052295625s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:28:03,694: INFO/MainProcess] Task tasks.scrape_pending_urls[ef58885c-fb27-4330-8d5e-c7b70a77ddc6] received
[2026-03-23 04:28:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[ef58885c-fb27-4330-8d5e-c7b70a77ddc6] succeeded in 0.003151299955789s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:28:33,694: INFO/MainProcess] Task tasks.scrape_pending_urls[137de5f5-56d3-44e7-b31e-4a06da1603ed] received
[2026-03-23 04:28:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[137de5f5-56d3-44e7-b31e-4a06da1603ed] succeeded in 0.0032487999997101724s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:29:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[51d15538-d996-409f-aafa-cdb0360489a9] received
[2026-03-23 04:29:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[51d15538-d996-409f-aafa-cdb0360489a9] succeeded in 0.0031061999616213143s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:29:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[236519bb-2c24-4094-aa41-eef114000787] received
[2026-03-23 04:29:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[236519bb-2c24-4094-aa41-eef114000787] succeeded in 0.0030709999846294522s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[2aee7feb-bc7a-48ca-90eb-bdf69d9155d8] received
[2026-03-23 04:30:00,006: INFO/MainProcess] Task tasks.purge_old_debug_html[2aee7feb-bc7a-48ca-90eb-bdf69d9155d8] succeeded in 0.0024361000396311283s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 04:30:03,697: INFO/MainProcess] Task tasks.scrape_pending_urls[126f67ef-10f0-46eb-9fd6-891bdda7828d] received
[2026-03-23 04:30:03,701: INFO/MainProcess] Task tasks.scrape_pending_urls[126f67ef-10f0-46eb-9fd6-891bdda7828d] succeeded in 0.0032245999900624156s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:30:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[eae30600-d9fa-40ed-90ae-d457cea49978] received
[2026-03-23 04:30:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[eae30600-d9fa-40ed-90ae-d457cea49978] succeeded in 0.003416899999137968s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:31:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[c3000342-65a3-4950-8e33-4f43fb291c6e] received
[2026-03-23 04:31:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[c3000342-65a3-4950-8e33-4f43fb291c6e] succeeded in 0.0032973000197671354s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:31:33,479: INFO/MainProcess] Task tasks.collect_system_metrics[a64f9dc7-e3c4-49e8-96b3-4915911e1df2] received
[2026-03-23 04:31:33,996: INFO/MainProcess] Task tasks.collect_system_metrics[a64f9dc7-e3c4-49e8-96b3-4915911e1df2] succeeded in 0.5166415999992751s: {'cpu': 17.3, 'memory': 40.3}
[2026-03-23 04:31:33,998: INFO/MainProcess] Task tasks.scrape_pending_urls[a8c1cb02-6ef8-4e4a-b776-e0cdeabbd8a1] received
[2026-03-23 04:31:34,002: INFO/MainProcess] Task tasks.scrape_pending_urls[a8c1cb02-6ef8-4e4a-b776-e0cdeabbd8a1] succeeded in 0.003341900010127574s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:32:03,699: INFO/MainProcess] Task tasks.scrape_pending_urls[6e7aa9f3-a170-45ec-98fa-6091917df743] received
[2026-03-23 04:32:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[6e7aa9f3-a170-45ec-98fa-6091917df743] succeeded in 0.0032177999964915216s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:32:33,699: INFO/MainProcess] Task tasks.scrape_pending_urls[56ce4091-a897-496d-a406-8784385a23cd] received
[2026-03-23 04:32:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[56ce4091-a897-496d-a406-8784385a23cd] succeeded in 0.003333300002850592s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:33:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[2d3049c2-b262-4288-af1a-8a6b0c4d7203] received
[2026-03-23 04:33:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[2d3049c2-b262-4288-af1a-8a6b0c4d7203] succeeded in 0.0035812999703921378s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:33:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[2b55a510-29d3-4ccf-a7dd-2c2464c51e75] received
[2026-03-23 04:33:33,701: INFO/MainProcess] Task tasks.scrape_pending_urls[2b55a510-29d3-4ccf-a7dd-2c2464c51e75] succeeded in 0.00310550001449883s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:34:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[4ad34fb4-b65f-4b3e-87d1-ee2e6a6aaa97] received
[2026-03-23 04:34:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[4ad34fb4-b65f-4b3e-87d1-ee2e6a6aaa97] succeeded in 0.0032189000048674643s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:34:33,698: INFO/MainProcess] Task tasks.scrape_pending_urls[152e07f4-c92e-4ac8-88db-2e6356f6eae0] received
[2026-03-23 04:34:33,701: INFO/MainProcess] Task tasks.scrape_pending_urls[152e07f4-c92e-4ac8-88db-2e6356f6eae0] succeeded in 0.0030279000056907535s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:35:03,698: INFO/MainProcess] Task tasks.scrape_pending_urls[da766441-1bfa-4571-84b9-9907cc610c65] received
[2026-03-23 04:35:03,701: INFO/MainProcess] Task tasks.scrape_pending_urls[da766441-1bfa-4571-84b9-9907cc610c65] succeeded in 0.0031270000035874546s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:35:33,703: INFO/MainProcess] Task tasks.scrape_pending_urls[3f0386b6-b903-49d7-adb3-09edb693db72] received
[2026-03-23 04:35:33,706: INFO/MainProcess] Task tasks.scrape_pending_urls[3f0386b6-b903-49d7-adb3-09edb693db72] succeeded in 0.0031260999967344105s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:36:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[59fd237f-a555-4477-b89b-dd72a1cb4f7c] received
[2026-03-23 04:36:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[59fd237f-a555-4477-b89b-dd72a1cb4f7c] succeeded in 0.00313070003176108s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:36:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[84c32807-2f41-451e-96f6-64190c66422b] received
[2026-03-23 04:36:33,477: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 04:36:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[84c32807-2f41-451e-96f6-64190c66422b] succeeded in 0.004407400032505393s: {'reset': 0}
[2026-03-23 04:36:33,480: INFO/MainProcess] Task tasks.collect_system_metrics[17b445ab-45af-4f97-8f0b-4c5877350341] received
[2026-03-23 04:36:33,996: INFO/MainProcess] Task tasks.collect_system_metrics[17b445ab-45af-4f97-8f0b-4c5877350341] succeeded in 0.516582100011874s: {'cpu': 14.5, 'memory': 40.3}
[2026-03-23 04:36:33,999: INFO/MainProcess] Task tasks.scrape_pending_urls[4c29e070-754b-4c3f-95ff-cece3c642215] received
[2026-03-23 04:36:34,002: INFO/MainProcess] Task tasks.scrape_pending_urls[4c29e070-754b-4c3f-95ff-cece3c642215] succeeded in 0.003495900018606335s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:37:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[0342fed9-47f2-496f-a99b-a83c4ced58c2] received
[2026-03-23 04:37:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[0342fed9-47f2-496f-a99b-a83c4ced58c2] succeeded in 0.0032245999900624156s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:37:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[18d85041-ab55-4e2e-9194-c8e16d385cd6] received
[2026-03-23 04:37:33,706: INFO/MainProcess] Task tasks.scrape_pending_urls[18d85041-ab55-4e2e-9194-c8e16d385cd6] succeeded in 0.003072399995289743s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:38:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[a204b70b-29d9-40cc-8306-257120320331] received
[2026-03-23 04:38:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[a204b70b-29d9-40cc-8306-257120320331] succeeded in 0.003141299996059388s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:38:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[bb1b3d21-0ff2-4360-b189-c37934b2226a] received
[2026-03-23 04:38:33,706: INFO/MainProcess] Task tasks.scrape_pending_urls[bb1b3d21-0ff2-4360-b189-c37934b2226a] succeeded in 0.0033776999916881323s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:39:03,703: INFO/MainProcess] Task tasks.scrape_pending_urls[5585fa64-3bae-4b43-9df2-7a94b94f2383] received
[2026-03-23 04:39:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[5585fa64-3bae-4b43-9df2-7a94b94f2383] succeeded in 0.003077699977438897s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:39:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[10d26562-c4ad-47a1-b363-d6ecf105161a] received
[2026-03-23 04:39:33,706: INFO/MainProcess] Task tasks.scrape_pending_urls[10d26562-c4ad-47a1-b363-d6ecf105161a] succeeded in 0.0032860999926924706s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:40:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[a2c6519b-2acd-444e-8f91-9370a57be449] received
[2026-03-23 04:40:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[a2c6519b-2acd-444e-8f91-9370a57be449] succeeded in 0.002966600004583597s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:40:33,702: INFO/MainProcess] Task tasks.scrape_pending_urls[bd9258e3-2f15-4c8b-8ecc-061c6f1de901] received
[2026-03-23 04:40:33,706: INFO/MainProcess] Task tasks.scrape_pending_urls[bd9258e3-2f15-4c8b-8ecc-061c6f1de901] succeeded in 0.002930500020738691s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:41:03,702: INFO/MainProcess] Task tasks.scrape_pending_urls[c956b0ee-17d7-466b-b0ec-106ded0628f3] received
[2026-03-23 04:41:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[c956b0ee-17d7-466b-b0ec-106ded0628f3] succeeded in 0.002966000000014901s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:41:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[f2945b70-5d1b-4dd4-905a-ddfc26bdc387] received
[2026-03-23 04:41:33,996: INFO/MainProcess] Task tasks.collect_system_metrics[f2945b70-5d1b-4dd4-905a-ddfc26bdc387] succeeded in 0.5173769000102766s: {'cpu': 13.7, 'memory': 40.4}
[2026-03-23 04:41:33,998: INFO/MainProcess] Task tasks.scrape_pending_urls[d0fbae03-c49a-4e19-9c29-bb757d665619] received
[2026-03-23 04:41:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[d0fbae03-c49a-4e19-9c29-bb757d665619] succeeded in 0.0033186000073328614s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:42:03,707: INFO/MainProcess] Task tasks.scrape_pending_urls[73a26845-bba9-411f-8926-0ab7913e610b] received
[2026-03-23 04:42:03,710: INFO/MainProcess] Task tasks.scrape_pending_urls[73a26845-bba9-411f-8926-0ab7913e610b] succeeded in 0.0029958999948576093s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:42:33,707: INFO/MainProcess] Task tasks.scrape_pending_urls[5e26ef3c-825a-4621-a96e-87f6539784cf] received
[2026-03-23 04:42:33,710: INFO/MainProcess] Task tasks.scrape_pending_urls[5e26ef3c-825a-4621-a96e-87f6539784cf] succeeded in 0.0032692999811843038s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:43:03,707: INFO/MainProcess] Task tasks.scrape_pending_urls[b2c2dfc7-5252-4eb0-99bd-f419a550ac83] received
[2026-03-23 04:43:03,710: INFO/MainProcess] Task tasks.scrape_pending_urls[b2c2dfc7-5252-4eb0-99bd-f419a550ac83] succeeded in 0.0031377000268548727s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:43:33,706: INFO/MainProcess] Task tasks.scrape_pending_urls[8f8b08ab-1af2-4d19-a391-c0f4180eb31d] received
[2026-03-23 04:43:33,710: INFO/MainProcess] Task tasks.scrape_pending_urls[8f8b08ab-1af2-4d19-a391-c0f4180eb31d] succeeded in 0.0029488999862223864s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:44:03,707: INFO/MainProcess] Task tasks.scrape_pending_urls[2a077e42-9a70-4c73-8226-4106a7da5b73] received
[2026-03-23 04:44:03,710: INFO/MainProcess] Task tasks.scrape_pending_urls[2a077e42-9a70-4c73-8226-4106a7da5b73] succeeded in 0.003041599993593991s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:44:33,707: INFO/MainProcess] Task tasks.scrape_pending_urls[787f0921-1511-45ba-8be3-4993b932e32e] received
[2026-03-23 04:44:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[787f0921-1511-45ba-8be3-4993b932e32e] succeeded in 0.003310800006147474s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:45:03,707: INFO/MainProcess] Task tasks.scrape_pending_urls[2bcf13a4-248a-4570-8620-512294093f79] received
[2026-03-23 04:45:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[2bcf13a4-248a-4570-8620-512294093f79] succeeded in 0.003376099979504943s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:45:33,707: INFO/MainProcess] Task tasks.scrape_pending_urls[f8b5569e-1440-4399-9eb9-74d4fcd63b69] received
[2026-03-23 04:45:33,710: INFO/MainProcess] Task tasks.scrape_pending_urls[f8b5569e-1440-4399-9eb9-74d4fcd63b69] succeeded in 0.0030716999899595976s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:46:03,706: INFO/MainProcess] Task tasks.scrape_pending_urls[49f5177a-47a1-4d6c-8eed-07da070a9fd2] received
[2026-03-23 04:46:03,710: INFO/MainProcess] Task tasks.scrape_pending_urls[49f5177a-47a1-4d6c-8eed-07da070a9fd2] succeeded in 0.0032000999781303108s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:46:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[c4c05351-1804-407c-9a3a-6338f5d228f9] received
[2026-03-23 04:46:33,995: INFO/MainProcess] Task tasks.collect_system_metrics[c4c05351-1804-407c-9a3a-6338f5d228f9] succeeded in 0.5166303000296466s: {'cpu': 15.9, 'memory': 40.4}
[2026-03-23 04:46:33,997: INFO/MainProcess] Task tasks.scrape_pending_urls[bd368a05-bd7a-446d-87fe-160beecf3521] received
[2026-03-23 04:46:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[bd368a05-bd7a-446d-87fe-160beecf3521] succeeded in 0.003292499983217567s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:47:03,707: INFO/MainProcess] Task tasks.scrape_pending_urls[dc92cf37-0c4d-452c-91a7-beba975ac701] received
[2026-03-23 04:47:03,710: INFO/MainProcess] Task tasks.scrape_pending_urls[dc92cf37-0c4d-452c-91a7-beba975ac701] succeeded in 0.003159100015182048s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:47:33,707: INFO/MainProcess] Task tasks.scrape_pending_urls[715e94d1-c6b6-45ea-8956-e572885fb4ff] received
[2026-03-23 04:47:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[715e94d1-c6b6-45ea-8956-e572885fb4ff] succeeded in 0.0032943999976851046s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:48:03,707: INFO/MainProcess] Task tasks.scrape_pending_urls[68e603d6-96b0-4ac9-9dee-8312354e3705] received
[2026-03-23 04:48:03,710: INFO/MainProcess] Task tasks.scrape_pending_urls[68e603d6-96b0-4ac9-9dee-8312354e3705] succeeded in 0.0031931999837979674s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:48:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[a1ea0875-29a7-4138-a9f4-e481b4be5e8f] received
[2026-03-23 04:48:33,714: INFO/MainProcess] Task tasks.scrape_pending_urls[a1ea0875-29a7-4138-a9f4-e481b4be5e8f] succeeded in 0.0029895000043325126s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:49:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[ba07fe39-42c4-4e3a-8487-6c532a5aa879] received
[2026-03-23 04:49:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[ba07fe39-42c4-4e3a-8487-6c532a5aa879] succeeded in 0.0032275000121444464s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:49:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[174f2675-4ead-4c0f-8c8c-86cff7efb80a] received
[2026-03-23 04:49:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[174f2675-4ead-4c0f-8c8c-86cff7efb80a] succeeded in 0.0033855000510811806s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:50:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[0cda9906-05f5-457f-92a0-073defca9932] received
[2026-03-23 04:50:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[0cda9906-05f5-457f-92a0-073defca9932] succeeded in 0.002938800025731325s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:50:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[29f997ba-3ab4-464d-9f6f-ce3ee3a135fd] received
[2026-03-23 04:50:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[29f997ba-3ab4-464d-9f6f-ce3ee3a135fd] succeeded in 0.0029715000418946147s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:51:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[a5a8f421-0e20-4a66-a18f-b03d661cde42] received
[2026-03-23 04:51:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[a5a8f421-0e20-4a66-a18f-b03d661cde42] succeeded in 0.003128000011201948s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:51:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[792007c5-8194-4c6f-aa84-3e777ddcbcaa] received
[2026-03-23 04:51:33,995: INFO/MainProcess] Task tasks.collect_system_metrics[792007c5-8194-4c6f-aa84-3e777ddcbcaa] succeeded in 0.5163296000100672s: {'cpu': 14.8, 'memory': 40.2}
[2026-03-23 04:51:33,997: INFO/MainProcess] Task tasks.scrape_pending_urls[f5e62306-ec84-4155-9491-f6561ed2be6c] received
[2026-03-23 04:51:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[f5e62306-ec84-4155-9491-f6561ed2be6c] succeeded in 0.003334200009703636s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:52:03,712: INFO/MainProcess] Task tasks.scrape_pending_urls[2fa3e67e-9b34-4f14-953a-5380ef69438a] received
[2026-03-23 04:52:03,716: INFO/MainProcess] Task tasks.scrape_pending_urls[2fa3e67e-9b34-4f14-953a-5380ef69438a] succeeded in 0.003421999979764223s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:52:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[c1070096-4e93-4c08-9f76-fc2ebcd25317] received
[2026-03-23 04:52:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[c1070096-4e93-4c08-9f76-fc2ebcd25317] succeeded in 0.002971899986732751s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:53:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[43266b51-b5f9-4035-897f-2a0c7ff7ead6] received
[2026-03-23 04:53:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[43266b51-b5f9-4035-897f-2a0c7ff7ead6] succeeded in 0.0031116000027395785s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:53:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[d900671c-bd60-4ae8-b6e7-db3164b94c9f] received
[2026-03-23 04:53:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[d900671c-bd60-4ae8-b6e7-db3164b94c9f] succeeded in 0.0031303000287152827s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:54:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[bd82916d-2543-403f-af86-8045ac237ea7] received
[2026-03-23 04:54:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[bd82916d-2543-403f-af86-8045ac237ea7] succeeded in 0.0029282999457791448s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:54:33,711: INFO/MainProcess] Task tasks.scrape_pending_urls[d5f5ac35-69ff-4010-b0f3-0c18fe6045b1] received
[2026-03-23 04:54:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[d5f5ac35-69ff-4010-b0f3-0c18fe6045b1] succeeded in 0.0031577000045217574s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:55:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[ce9b32fa-d67e-4880-bcc5-af80af80b314] received
[2026-03-23 04:55:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[ce9b32fa-d67e-4880-bcc5-af80af80b314] succeeded in 0.0031758000259287655s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:55:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[3d209115-9aae-46c3-a3be-5d859f796008] received
[2026-03-23 04:55:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[3d209115-9aae-46c3-a3be-5d859f796008] succeeded in 0.003111700003501028s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:56:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[4cc45b83-c49f-4f62-8aa4-cb45333e4681] received
[2026-03-23 04:56:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[4cc45b83-c49f-4f62-8aa4-cb45333e4681] succeeded in 0.003444099973421544s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:56:33,478: INFO/MainProcess] Task tasks.collect_system_metrics[f4c8f9c7-7c5f-48b0-bd38-afc885d547dc] received
[2026-03-23 04:56:33,995: INFO/MainProcess] Task tasks.collect_system_metrics[f4c8f9c7-7c5f-48b0-bd38-afc885d547dc] succeeded in 0.516781100013759s: {'cpu': 15.0, 'memory': 40.5}
[2026-03-23 04:56:33,997: INFO/MainProcess] Task tasks.scrape_pending_urls[5a072520-d69f-4ed7-9b53-e397e5a1ece6] received
[2026-03-23 04:56:34,006: INFO/MainProcess] Task tasks.scrape_pending_urls[5a072520-d69f-4ed7-9b53-e397e5a1ece6] succeeded in 0.00728789996355772s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:57:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[8c01ee5c-b051-412d-ab8f-33bf06d49d47] received
[2026-03-23 04:57:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[8c01ee5c-b051-412d-ab8f-33bf06d49d47] succeeded in 0.003138699976261705s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:57:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[5e348348-bce9-4a72-8fed-140ea2924080] received
[2026-03-23 04:57:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[5e348348-bce9-4a72-8fed-140ea2924080] succeeded in 0.002960899961180985s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:58:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[ca87784b-25ac-42cd-9582-b15f816357cc] received
[2026-03-23 04:58:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[ca87784b-25ac-42cd-9582-b15f816357cc] succeeded in 0.003260199970100075s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:58:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[171b7e58-78ed-42a6-a79d-250f9fb3a4b4] received
[2026-03-23 04:58:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[171b7e58-78ed-42a6-a79d-250f9fb3a4b4] succeeded in 0.003159599960781634s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:59:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[acdda58a-3db0-4297-a9b9-43e82dc297c1] received
[2026-03-23 04:59:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[acdda58a-3db0-4297-a9b9-43e82dc297c1] succeeded in 0.003044299955945462s: {'status': 'idle', 'pending': 0}
[2026-03-23 04:59:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[aabe15bd-9ad7-44e7-a338-fb75d74c08c6] received
[2026-03-23 04:59:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[aabe15bd-9ad7-44e7-a338-fb75d74c08c6] succeeded in 0.0030411999905481935s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:00:03,716: INFO/MainProcess] Task tasks.scrape_pending_urls[7dd68adc-8ee8-413b-9412-0ba3b5e4fefb] received
[2026-03-23 05:00:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[7dd68adc-8ee8-413b-9412-0ba3b5e4fefb] succeeded in 0.0034777999971993268s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:00:33,716: INFO/MainProcess] Task tasks.scrape_pending_urls[9acb6857-d422-4865-bb89-f3445c4eacf1] received
[2026-03-23 05:00:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[9acb6857-d422-4865-bb89-f3445c4eacf1] succeeded in 0.0031101999920792878s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:01:03,716: INFO/MainProcess] Task tasks.scrape_pending_urls[93d753a2-2e49-440f-ab6c-af2def6e95ad] received
[2026-03-23 05:01:03,720: INFO/MainProcess] Task tasks.scrape_pending_urls[93d753a2-2e49-440f-ab6c-af2def6e95ad] succeeded in 0.003771600022446364s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:01:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[d1649311-43a0-446a-be27-f377f2b1aa65] received
[2026-03-23 05:01:33,999: INFO/MainProcess] Task tasks.collect_system_metrics[d1649311-43a0-446a-be27-f377f2b1aa65] succeeded in 0.5165360999526456s: {'cpu': 12.5, 'memory': 40.6}
[2026-03-23 05:01:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[ebdec5bc-551c-48e9-8a27-cf66da6cbbbf] received
[2026-03-23 05:01:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[ebdec5bc-551c-48e9-8a27-cf66da6cbbbf] succeeded in 0.0033947000047191978s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:02:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[1c63ecfe-2405-4bda-971e-6b7db79bcf50] received
[2026-03-23 05:02:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[1c63ecfe-2405-4bda-971e-6b7db79bcf50] succeeded in 0.0032211000216193497s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:02:33,715: INFO/MainProcess] Task tasks.scrape_pending_urls[439aaa1e-a7f3-4891-981f-465f75210214] received
[2026-03-23 05:02:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[439aaa1e-a7f3-4891-981f-465f75210214] succeeded in 0.0032482999959029257s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:03:03,716: INFO/MainProcess] Task tasks.scrape_pending_urls[f5256880-5582-443c-bc01-04480486393b] received
[2026-03-23 05:03:03,720: INFO/MainProcess] Task tasks.scrape_pending_urls[f5256880-5582-443c-bc01-04480486393b] succeeded in 0.003291799977887422s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:03:33,716: INFO/MainProcess] Task tasks.scrape_pending_urls[43155b6e-9866-4ed8-91f6-ca443793dbf3] received
[2026-03-23 05:03:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[43155b6e-9866-4ed8-91f6-ca443793dbf3] succeeded in 0.0030571999959647655s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:04:03,716: INFO/MainProcess] Task tasks.scrape_pending_urls[06a35153-fcb9-4ac0-bcb6-268bb00f9ed7] received
[2026-03-23 05:04:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[06a35153-fcb9-4ac0-bcb6-268bb00f9ed7] succeeded in 0.003138999978546053s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:04:33,720: INFO/MainProcess] Task tasks.scrape_pending_urls[af265bc7-737d-4263-9e94-78665d19a211] received
[2026-03-23 05:04:33,723: INFO/MainProcess] Task tasks.scrape_pending_urls[af265bc7-737d-4263-9e94-78665d19a211] succeeded in 0.0029477999778464437s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:05:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[73ea668d-557a-480b-9e40-8088bb0569e8] received
[2026-03-23 05:05:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[73ea668d-557a-480b-9e40-8088bb0569e8] succeeded in 0.0030658000032417476s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:05:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[989834c3-8db1-4d0b-9230-929a9c37e3de] received
[2026-03-23 05:05:33,722: INFO/MainProcess] Task tasks.scrape_pending_urls[989834c3-8db1-4d0b-9230-929a9c37e3de] succeeded in 0.002978599979542196s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:06:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[a1abc882-3d4d-45dc-a20e-136eac05344a] received
[2026-03-23 05:06:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[a1abc882-3d4d-45dc-a20e-136eac05344a] succeeded in 0.003115599974989891s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:06:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[49bf6f8d-d6c5-4d19-a4dd-650a00eda102] received
[2026-03-23 05:06:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 05:06:33,477: INFO/MainProcess] Task tasks.reset_stale_processing_urls[49bf6f8d-d6c5-4d19-a4dd-650a00eda102] succeeded in 0.004394699994008988s: {'reset': 0}
[2026-03-23 05:06:33,481: INFO/MainProcess] Task tasks.collect_system_metrics[5efdb87c-583c-4376-b852-254a1684cf43] received
[2026-03-23 05:06:33,998: INFO/MainProcess] Task tasks.collect_system_metrics[5efdb87c-583c-4376-b852-254a1684cf43] succeeded in 0.5162009000196122s: {'cpu': 16.0, 'memory': 40.6}
[2026-03-23 05:06:34,000: INFO/MainProcess] Task tasks.scrape_pending_urls[d537ee41-eb32-4964-b8e1-836724e2f5ba] received
[2026-03-23 05:06:34,003: INFO/MainProcess] Task tasks.scrape_pending_urls[d537ee41-eb32-4964-b8e1-836724e2f5ba] succeeded in 0.0034167999983765185s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:07:03,720: INFO/MainProcess] Task tasks.scrape_pending_urls[0db663d9-f163-4088-91bf-25760bbbb3e7] received
[2026-03-23 05:07:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[0db663d9-f163-4088-91bf-25760bbbb3e7] succeeded in 0.0033934000530280173s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:07:33,719: INFO/MainProcess] Task tasks.scrape_pending_urls[dc765bb0-82f8-4a7a-8c37-5f9c62db5c78] received
[2026-03-23 05:07:33,723: INFO/MainProcess] Task tasks.scrape_pending_urls[dc765bb0-82f8-4a7a-8c37-5f9c62db5c78] succeeded in 0.003555700008291751s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:08:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[933fd35e-ef86-4823-8058-2177ca738fb9] received
[2026-03-23 05:08:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[933fd35e-ef86-4823-8058-2177ca738fb9] succeeded in 0.0031080999760888517s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:08:33,720: INFO/MainProcess] Task tasks.scrape_pending_urls[afa76553-16d3-4115-a1d1-d8ce8a53f071] received
[2026-03-23 05:08:33,724: INFO/MainProcess] Task tasks.scrape_pending_urls[afa76553-16d3-4115-a1d1-d8ce8a53f071] succeeded in 0.0032267000060528517s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:09:03,719: INFO/MainProcess] Task tasks.scrape_pending_urls[4e2e8755-fa4b-4d8c-b21d-058491ef415d] received
[2026-03-23 05:09:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[4e2e8755-fa4b-4d8c-b21d-058491ef415d] succeeded in 0.003391800040844828s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:09:33,720: INFO/MainProcess] Task tasks.scrape_pending_urls[dc92d801-2471-47fb-8d60-58014938550c] received
[2026-03-23 05:09:33,723: INFO/MainProcess] Task tasks.scrape_pending_urls[dc92d801-2471-47fb-8d60-58014938550c] succeeded in 0.00290089996997267s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:10:03,720: INFO/MainProcess] Task tasks.scrape_pending_urls[739b1e4c-7369-4d60-b6ba-a87684a9a82a] received
[2026-03-23 05:10:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[739b1e4c-7369-4d60-b6ba-a87684a9a82a] succeeded in 0.003044300014153123s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:10:33,720: INFO/MainProcess] Task tasks.scrape_pending_urls[b5458a28-a84b-4661-94e7-bfa0cc57bde5] received
[2026-03-23 05:10:33,723: INFO/MainProcess] Task tasks.scrape_pending_urls[b5458a28-a84b-4661-94e7-bfa0cc57bde5] succeeded in 0.0032879000063985586s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:11:03,724: INFO/MainProcess] Task tasks.scrape_pending_urls[aea78792-c2ff-42f6-8b79-4a1f263b6ba6] received
[2026-03-23 05:11:03,729: INFO/MainProcess] Task tasks.scrape_pending_urls[aea78792-c2ff-42f6-8b79-4a1f263b6ba6] succeeded in 0.004348299989942461s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:11:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[a18dc2d1-9c8d-4bff-8b2d-2835dba3d8c1] received
[2026-03-23 05:11:34,049: INFO/MainProcess] Task tasks.collect_system_metrics[a18dc2d1-9c8d-4bff-8b2d-2835dba3d8c1] succeeded in 0.5665859999717213s: {'cpu': 15.2, 'memory': 40.6}
[2026-03-23 05:11:34,052: INFO/MainProcess] Task tasks.scrape_pending_urls[28467d35-b19f-43fd-8215-790264fa38b2] received
[2026-03-23 05:11:34,056: INFO/MainProcess] Task tasks.scrape_pending_urls[28467d35-b19f-43fd-8215-790264fa38b2] succeeded in 0.0034505000221543014s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:12:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[223e1a72-7d7b-425e-9bab-af42606607bd] received
[2026-03-23 05:12:03,788: INFO/MainProcess] Task tasks.scrape_pending_urls[223e1a72-7d7b-425e-9bab-af42606607bd] succeeded in 0.0641135000041686s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:12:33,724: INFO/MainProcess] Task tasks.scrape_pending_urls[a19204c6-aec3-4fb9-9416-86a7c757a7d7] received
[2026-03-23 05:12:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[a19204c6-aec3-4fb9-9416-86a7c757a7d7] succeeded in 0.003507999994326383s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:13:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[ab5d2006-7c06-44eb-a625-db8ddea777ea] received
[2026-03-23 05:13:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[ab5d2006-7c06-44eb-a625-db8ddea777ea] succeeded in 0.004365100001450628s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:13:33,723: INFO/MainProcess] Task tasks.scrape_pending_urls[da1cd052-064d-4d28-a0e5-148c7741fbec] received
[2026-03-23 05:13:33,727: INFO/MainProcess] Task tasks.scrape_pending_urls[da1cd052-064d-4d28-a0e5-148c7741fbec] succeeded in 0.0031570999999530613s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:14:03,724: INFO/MainProcess] Task tasks.scrape_pending_urls[bab06d5f-2a6a-411b-b236-a80bee841e1a] received
[2026-03-23 05:14:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[bab06d5f-2a6a-411b-b236-a80bee841e1a] succeeded in 0.0033174999989569187s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:14:33,723: INFO/MainProcess] Task tasks.scrape_pending_urls[e1e59161-3c46-4387-9223-156587538420] received
[2026-03-23 05:14:33,727: INFO/MainProcess] Task tasks.scrape_pending_urls[e1e59161-3c46-4387-9223-156587538420] succeeded in 0.0030785000417381525s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:15:03,723: INFO/MainProcess] Task tasks.scrape_pending_urls[b070b4d0-5348-4aaf-97f9-dd887384f120] received
[2026-03-23 05:15:03,727: INFO/MainProcess] Task tasks.scrape_pending_urls[b070b4d0-5348-4aaf-97f9-dd887384f120] succeeded in 0.003369599988218397s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:15:33,724: INFO/MainProcess] Task tasks.scrape_pending_urls[a810126a-5bcb-42b6-ac47-e24dc47d3364] received
[2026-03-23 05:15:33,727: INFO/MainProcess] Task tasks.scrape_pending_urls[a810126a-5bcb-42b6-ac47-e24dc47d3364] succeeded in 0.003152600023895502s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:16:03,724: INFO/MainProcess] Task tasks.scrape_pending_urls[1fac15dc-0165-46f8-a617-54a704ffe746] received
[2026-03-23 05:16:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[1fac15dc-0165-46f8-a617-54a704ffe746] succeeded in 0.0036936000105924904s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:16:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[0d056eb2-9fc6-46e1-90fb-32e1ac5b4cd9] received
[2026-03-23 05:16:33,991: INFO/MainProcess] Task tasks.collect_system_metrics[0d056eb2-9fc6-46e1-90fb-32e1ac5b4cd9] succeeded in 0.5080550000420772s: {'cpu': 15.2, 'memory': 40.5}
[2026-03-23 05:16:33,993: INFO/MainProcess] Task tasks.scrape_pending_urls[ba51a08d-7340-49bc-8de7-237e216b9978] received
[2026-03-23 05:16:33,997: INFO/MainProcess] Task tasks.scrape_pending_urls[ba51a08d-7340-49bc-8de7-237e216b9978] succeeded in 0.0035995999933220446s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:17:03,724: INFO/MainProcess] Task tasks.scrape_pending_urls[e18010f8-1348-4415-b7ec-2869e53177dc] received
[2026-03-23 05:17:03,729: INFO/MainProcess] Task tasks.scrape_pending_urls[e18010f8-1348-4415-b7ec-2869e53177dc] succeeded in 0.004599299980327487s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:17:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[03853a6a-d408-41ef-9279-86a196b127be] received
[2026-03-23 05:17:33,734: INFO/MainProcess] Task tasks.scrape_pending_urls[03853a6a-d408-41ef-9279-86a196b127be] succeeded in 0.00470270001096651s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:18:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[3ddf7b30-dbbf-494b-9144-54f3c718dd47] received
[2026-03-23 05:18:03,731: INFO/MainProcess] Task tasks.scrape_pending_urls[3ddf7b30-dbbf-494b-9144-54f3c718dd47] succeeded in 0.00333510001655668s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:18:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[61589aa7-c5cf-499d-b062-83cf89b22aee] received
[2026-03-23 05:18:33,792: INFO/MainProcess] Task tasks.scrape_pending_urls[61589aa7-c5cf-499d-b062-83cf89b22aee] succeeded in 0.06462010001996532s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:19:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[274e7bdd-37b4-4126-b56e-ade55c22ccc0] received
[2026-03-23 05:19:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[274e7bdd-37b4-4126-b56e-ade55c22ccc0] succeeded in 0.0034010999952442944s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:19:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[e1e02ff9-6e3d-4616-b113-46baf85195bb] received
[2026-03-23 05:19:33,734: INFO/MainProcess] Task tasks.scrape_pending_urls[e1e02ff9-6e3d-4616-b113-46baf85195bb] succeeded in 0.0051071000052616s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:20:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[bf206049-d89c-4d78-9b9f-7ca581c9ecb3] received
[2026-03-23 05:20:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[bf206049-d89c-4d78-9b9f-7ca581c9ecb3] succeeded in 0.0034706000005826354s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:20:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[8cf7d528-d216-4be9-8570-38c683090041] received
[2026-03-23 05:20:33,731: INFO/MainProcess] Task tasks.scrape_pending_urls[8cf7d528-d216-4be9-8570-38c683090041] succeeded in 0.003165000001899898s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:21:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[313ab2d5-f6f0-40d0-be82-e02fe67c3593] received
[2026-03-23 05:21:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[313ab2d5-f6f0-40d0-be82-e02fe67c3593] succeeded in 0.0032923000399023294s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:21:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[83ebcc16-9835-4510-a271-c97b76f2a175] received
[2026-03-23 05:21:34,002: INFO/MainProcess] Task tasks.collect_system_metrics[83ebcc16-9835-4510-a271-c97b76f2a175] succeeded in 0.5192438999656588s: {'cpu': 14.6, 'memory': 40.5}
[2026-03-23 05:21:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[49577777-7987-4320-96ad-928faf80fd94] received
[2026-03-23 05:21:34,008: INFO/MainProcess] Task tasks.scrape_pending_urls[49577777-7987-4320-96ad-928faf80fd94] succeeded in 0.0034639000077731907s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:22:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[56d40a9d-bb2c-479b-83f1-16724dce1a97] received
[2026-03-23 05:22:03,731: INFO/MainProcess] Task tasks.scrape_pending_urls[56d40a9d-bb2c-479b-83f1-16724dce1a97] succeeded in 0.0032414000015705824s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:22:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[16606c3c-5805-40e2-901d-ca5d1ac31914] received
[2026-03-23 05:22:33,731: INFO/MainProcess] Task tasks.scrape_pending_urls[16606c3c-5805-40e2-901d-ca5d1ac31914] succeeded in 0.0031516000162810087s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:23:03,728: INFO/MainProcess] Task tasks.scrape_pending_urls[0f000aae-10bf-4d50-9058-526c1988b190] received
[2026-03-23 05:23:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[0f000aae-10bf-4d50-9058-526c1988b190] succeeded in 0.0032839999767020345s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:23:33,728: INFO/MainProcess] Task tasks.scrape_pending_urls[9e213109-3033-4601-a228-f4e388ec2577] received
[2026-03-23 05:23:33,732: INFO/MainProcess] Task tasks.scrape_pending_urls[9e213109-3033-4601-a228-f4e388ec2577] succeeded in 0.0033214999712072313s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:24:03,733: INFO/MainProcess] Task tasks.scrape_pending_urls[0e8f539f-6e7d-4c1a-bc1d-90dd82a04413] received
[2026-03-23 05:24:03,739: INFO/MainProcess] Task tasks.scrape_pending_urls[0e8f539f-6e7d-4c1a-bc1d-90dd82a04413] succeeded in 0.005156600032933056s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:24:33,732: INFO/MainProcess] Task tasks.scrape_pending_urls[201a2e16-138a-4966-97b2-c912a4a47d48] received
[2026-03-23 05:24:33,737: INFO/MainProcess] Task tasks.scrape_pending_urls[201a2e16-138a-4966-97b2-c912a4a47d48] succeeded in 0.004353600030299276s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:25:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[2733d417-0670-4ec6-8045-ef93445b2acf] received
[2026-03-23 05:25:03,737: INFO/MainProcess] Task tasks.scrape_pending_urls[2733d417-0670-4ec6-8045-ef93445b2acf] succeeded in 0.004414099967107177s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:25:33,732: INFO/MainProcess] Task tasks.scrape_pending_urls[7c9acf73-1f3d-49db-917d-b6754ed70151] received
[2026-03-23 05:25:33,736: INFO/MainProcess] Task tasks.scrape_pending_urls[7c9acf73-1f3d-49db-917d-b6754ed70151] succeeded in 0.003245700034312904s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:26:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[e74e4fac-3226-4185-a50c-7e499ed785af] received
[2026-03-23 05:26:03,737: INFO/MainProcess] Task tasks.scrape_pending_urls[e74e4fac-3226-4185-a50c-7e499ed785af] succeeded in 0.00441380002303049s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:26:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[d22d5f93-4c6f-4257-9b4e-6294e4868ea7] received
[2026-03-23 05:26:34,000: INFO/MainProcess] Task tasks.collect_system_metrics[d22d5f93-4c6f-4257-9b4e-6294e4868ea7] succeeded in 0.5167724000057206s: {'cpu': 13.3, 'memory': 40.6}
[2026-03-23 05:26:34,002: INFO/MainProcess] Task tasks.scrape_pending_urls[d7b83500-94d2-4546-a5ce-153ca52d3859] received
[2026-03-23 05:26:34,006: INFO/MainProcess] Task tasks.scrape_pending_urls[d7b83500-94d2-4546-a5ce-153ca52d3859] succeeded in 0.0035472000017762184s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:27:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[39114594-7a4c-448a-b98b-6c7160de76bc] received
[2026-03-23 05:27:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[39114594-7a4c-448a-b98b-6c7160de76bc] succeeded in 0.003325300000142306s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:27:33,732: INFO/MainProcess] Task tasks.scrape_pending_urls[4096d34f-b99d-4861-8137-52b7baa24db0] received
[2026-03-23 05:27:33,736: INFO/MainProcess] Task tasks.scrape_pending_urls[4096d34f-b99d-4861-8137-52b7baa24db0] succeeded in 0.002916199970059097s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:28:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[770d0f00-c442-4d96-836a-dcc82c4946dc] received
[2026-03-23 05:28:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[770d0f00-c442-4d96-836a-dcc82c4946dc] succeeded in 0.0032462000381201506s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:28:33,732: INFO/MainProcess] Task tasks.scrape_pending_urls[a88470a8-b98e-4677-abdc-ffcb9c319641] received
[2026-03-23 05:28:33,736: INFO/MainProcess] Task tasks.scrape_pending_urls[a88470a8-b98e-4677-abdc-ffcb9c319641] succeeded in 0.0029513000044971704s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:29:03,733: INFO/MainProcess] Task tasks.scrape_pending_urls[ee25ed59-3512-410b-a084-00855d7b0209] received
[2026-03-23 05:29:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[ee25ed59-3512-410b-a084-00855d7b0209] succeeded in 0.003200799983460456s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:29:33,733: INFO/MainProcess] Task tasks.scrape_pending_urls[9aab8287-7f27-409a-9647-f401c638364f] received
[2026-03-23 05:29:33,736: INFO/MainProcess] Task tasks.scrape_pending_urls[9aab8287-7f27-409a-9647-f401c638364f] succeeded in 0.0035164000000804663s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[6c456412-0a98-400a-b743-3a76cc908c46] received
[2026-03-23 05:30:00,005: INFO/MainProcess] Task tasks.purge_old_debug_html[6c456412-0a98-400a-b743-3a76cc908c46] succeeded in 0.0016821000026538968s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 05:30:03,732: INFO/MainProcess] Task tasks.scrape_pending_urls[5a0fceb6-c1fc-498e-932e-8265c7f71b74] received
[2026-03-23 05:30:03,735: INFO/MainProcess] Task tasks.scrape_pending_urls[5a0fceb6-c1fc-498e-932e-8265c7f71b74] succeeded in 0.003119100001640618s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:30:33,737: INFO/MainProcess] Task tasks.scrape_pending_urls[1bc48625-a71e-4310-aa31-89582c9b15b0] received
[2026-03-23 05:30:33,740: INFO/MainProcess] Task tasks.scrape_pending_urls[1bc48625-a71e-4310-aa31-89582c9b15b0] succeeded in 0.0034266000147908926s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:31:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[ccbf1012-597f-4219-81e3-88228797f7a8] received
[2026-03-23 05:31:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[ccbf1012-597f-4219-81e3-88228797f7a8] succeeded in 0.0034613999887369573s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:31:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[1a33502d-7c8b-48fb-8efe-deed401eff0c] received
[2026-03-23 05:31:34,000: INFO/MainProcess] Task tasks.collect_system_metrics[1a33502d-7c8b-48fb-8efe-deed401eff0c] succeeded in 0.5178680999670178s: {'cpu': 20.6, 'memory': 40.8}
[2026-03-23 05:31:34,003: INFO/MainProcess] Task tasks.scrape_pending_urls[6a5df930-8ebb-412c-a2c1-460a776f2ae3] received
[2026-03-23 05:31:34,007: INFO/MainProcess] Task tasks.scrape_pending_urls[6a5df930-8ebb-412c-a2c1-460a776f2ae3] succeeded in 0.0033363000256940722s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:32:03,737: INFO/MainProcess] Task tasks.scrape_pending_urls[7f91d829-76b7-486a-b648-a06663b4c97b] received
[2026-03-23 05:32:03,741: INFO/MainProcess] Task tasks.scrape_pending_urls[7f91d829-76b7-486a-b648-a06663b4c97b] succeeded in 0.004094600037205964s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:32:33,737: INFO/MainProcess] Task tasks.scrape_pending_urls[d9084de8-df57-412a-9609-63c9321356ba] received
[2026-03-23 05:32:33,741: INFO/MainProcess] Task tasks.scrape_pending_urls[d9084de8-df57-412a-9609-63c9321356ba] succeeded in 0.003828299988526851s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:33:03,737: INFO/MainProcess] Task tasks.scrape_pending_urls[a9f96259-d82c-48dc-8d64-65ebf2f9d85c] received
[2026-03-23 05:33:03,741: INFO/MainProcess] Task tasks.scrape_pending_urls[a9f96259-d82c-48dc-8d64-65ebf2f9d85c] succeeded in 0.0034644000115804374s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:33:33,737: INFO/MainProcess] Task tasks.scrape_pending_urls[d74f2c0b-c269-45e5-bbb1-9ca5bf9c7460] received
[2026-03-23 05:33:33,741: INFO/MainProcess] Task tasks.scrape_pending_urls[d74f2c0b-c269-45e5-bbb1-9ca5bf9c7460] succeeded in 0.003377299988642335s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:34:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[fe93492d-5841-4e7b-a77c-b4018c75b227] received
[2026-03-23 05:34:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[fe93492d-5841-4e7b-a77c-b4018c75b227] succeeded in 0.0029818000039085746s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:34:33,737: INFO/MainProcess] Task tasks.scrape_pending_urls[d7886697-32e4-4070-88bc-4b4bc62ed96f] received
[2026-03-23 05:34:33,741: INFO/MainProcess] Task tasks.scrape_pending_urls[d7886697-32e4-4070-88bc-4b4bc62ed96f] succeeded in 0.0036797000211663544s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:35:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[8108be85-bbcc-4ca3-99bb-2b5d9cc1cc86] received
[2026-03-23 05:35:03,739: INFO/MainProcess] Task tasks.scrape_pending_urls[8108be85-bbcc-4ca3-99bb-2b5d9cc1cc86] succeeded in 0.0031086999806575477s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:35:33,737: INFO/MainProcess] Task tasks.scrape_pending_urls[3e5a6e55-8a60-40d0-9df4-74cdf4c4f3ae] received
[2026-03-23 05:35:33,740: INFO/MainProcess] Task tasks.scrape_pending_urls[3e5a6e55-8a60-40d0-9df4-74cdf4c4f3ae] succeeded in 0.0032428999547846615s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:36:03,736: INFO/MainProcess] Task tasks.scrape_pending_urls[94397dfa-4d81-4198-acf6-327aa051c067] received
[2026-03-23 05:36:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[94397dfa-4d81-4198-acf6-327aa051c067] succeeded in 0.002960899961180985s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:36:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[6c06936b-ed24-45f5-889e-e52505405acb] received
[2026-03-23 05:36:33,477: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 05:36:33,479: INFO/MainProcess] Task tasks.reset_stale_processing_urls[6c06936b-ed24-45f5-889e-e52505405acb] succeeded in 0.005001400015316904s: {'reset': 0}
[2026-03-23 05:36:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[f6bd777b-3af0-4463-8268-46cbb59e85d4] received
[2026-03-23 05:36:33,999: INFO/MainProcess] Task tasks.collect_system_metrics[f6bd777b-3af0-4463-8268-46cbb59e85d4] succeeded in 0.5167241999879479s: {'cpu': 16.7, 'memory': 40.7}
[2026-03-23 05:36:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[3301e931-f977-4201-a47e-1ac21732df27] received
[2026-03-23 05:36:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[3301e931-f977-4201-a47e-1ac21732df27] succeeded in 0.003424399998039007s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:37:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[c951442d-e19e-4287-9d9f-c20bbdeffffb] received
[2026-03-23 05:37:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[c951442d-e19e-4287-9d9f-c20bbdeffffb] succeeded in 0.003384500043466687s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:37:33,740: INFO/MainProcess] Task tasks.scrape_pending_urls[e971158a-5c94-4f5c-8e38-e3e1dc6138cf] received
[2026-03-23 05:37:33,744: INFO/MainProcess] Task tasks.scrape_pending_urls[e971158a-5c94-4f5c-8e38-e3e1dc6138cf] succeeded in 0.00344480003695935s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:38:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[78e4953c-887a-40bf-9443-c92020c28f07] received
[2026-03-23 05:38:03,745: INFO/MainProcess] Task tasks.scrape_pending_urls[78e4953c-887a-40bf-9443-c92020c28f07] succeeded in 0.0038947000284679234s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:38:33,740: INFO/MainProcess] Task tasks.scrape_pending_urls[0df53ecc-b881-485b-813a-d085b0db9144] received
[2026-03-23 05:38:33,746: INFO/MainProcess] Task tasks.scrape_pending_urls[0df53ecc-b881-485b-813a-d085b0db9144] succeeded in 0.004743899975437671s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:39:03,741: INFO/MainProcess] Task tasks.scrape_pending_urls[f6765216-d044-4588-9ff3-1dde8b950784] received
[2026-03-23 05:39:03,746: INFO/MainProcess] Task tasks.scrape_pending_urls[f6765216-d044-4588-9ff3-1dde8b950784] succeeded in 0.004708199994638562s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:39:33,741: INFO/MainProcess] Task tasks.scrape_pending_urls[98114a61-9cb0-4522-b0f9-76fe282013cc] received
[2026-03-23 05:39:33,745: INFO/MainProcess] Task tasks.scrape_pending_urls[98114a61-9cb0-4522-b0f9-76fe282013cc] succeeded in 0.004330700030550361s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:40:03,741: INFO/MainProcess] Task tasks.scrape_pending_urls[d79bf1ed-cb7f-4568-ace8-592c99afffb3] received
[2026-03-23 05:40:03,746: INFO/MainProcess] Task tasks.scrape_pending_urls[d79bf1ed-cb7f-4568-ace8-592c99afffb3] succeeded in 0.004333099990617484s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:40:33,740: INFO/MainProcess] Task tasks.scrape_pending_urls[731e3815-1948-4800-8469-5c123892098d] received
[2026-03-23 05:40:33,743: INFO/MainProcess] Task tasks.scrape_pending_urls[731e3815-1948-4800-8469-5c123892098d] succeeded in 0.0031177999917417765s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:41:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[1bd0e58e-c8ec-49a9-a6e9-8db47eb02f16] received
[2026-03-23 05:41:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[1bd0e58e-c8ec-49a9-a6e9-8db47eb02f16] succeeded in 0.0034070999827235937s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:41:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[c881458a-12a0-4dc2-9f81-7e550f31f26c] received
[2026-03-23 05:41:33,998: INFO/MainProcess] Task tasks.collect_system_metrics[c881458a-12a0-4dc2-9f81-7e550f31f26c] succeeded in 0.5160199999809265s: {'cpu': 15.4, 'memory': 40.8}
[2026-03-23 05:41:34,000: INFO/MainProcess] Task tasks.scrape_pending_urls[c13cba4c-9bb0-41a4-98d4-ae9d191d7038] received
[2026-03-23 05:41:34,004: INFO/MainProcess] Task tasks.scrape_pending_urls[c13cba4c-9bb0-41a4-98d4-ae9d191d7038] succeeded in 0.003397500026039779s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:42:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[efa594e0-08c8-4da5-a841-a41b9c593d07] received
[2026-03-23 05:42:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[efa594e0-08c8-4da5-a841-a41b9c593d07] succeeded in 0.00331579998601228s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:42:33,741: INFO/MainProcess] Task tasks.scrape_pending_urls[cd06bb5d-1672-48e5-b1d0-55b78023e151] received
[2026-03-23 05:42:33,744: INFO/MainProcess] Task tasks.scrape_pending_urls[cd06bb5d-1672-48e5-b1d0-55b78023e151] succeeded in 0.003207199973985553s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:43:03,740: INFO/MainProcess] Task tasks.scrape_pending_urls[958e3f83-9d7a-4730-8ce2-0f802ae0c45b] received
[2026-03-23 05:43:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[958e3f83-9d7a-4730-8ce2-0f802ae0c45b] succeeded in 0.003210499999113381s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:43:33,744: INFO/MainProcess] Task tasks.scrape_pending_urls[1e4bba78-22de-4dc2-a78b-7063be928825] received
[2026-03-23 05:43:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[1e4bba78-22de-4dc2-a78b-7063be928825] succeeded in 0.003472500015050173s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:44:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[7bc90dbf-9d08-4819-a755-5b2dd240a1c6] received
[2026-03-23 05:44:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[7bc90dbf-9d08-4819-a755-5b2dd240a1c6] succeeded in 0.004273400001693517s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:44:33,745: INFO/MainProcess] Task tasks.scrape_pending_urls[97bf0808-816f-4557-9133-687127c7ffc2] received
[2026-03-23 05:44:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[97bf0808-816f-4557-9133-687127c7ffc2] succeeded in 0.003111199999693781s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:45:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[f5e41711-e845-4aa6-8f82-d23f99a7865c] received
[2026-03-23 05:45:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[f5e41711-e845-4aa6-8f82-d23f99a7865c] succeeded in 0.003422599984332919s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:45:33,744: INFO/MainProcess] Task tasks.scrape_pending_urls[c381d7cd-d1b5-4339-9b98-8121111e3d9d] received
[2026-03-23 05:45:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[c381d7cd-d1b5-4339-9b98-8121111e3d9d] succeeded in 0.0032691999804228544s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:46:03,745: INFO/MainProcess] Task tasks.scrape_pending_urls[582769f8-d9ac-457c-8160-8ce237aebf3d] received
[2026-03-23 05:46:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[582769f8-d9ac-457c-8160-8ce237aebf3d] succeeded in 0.0037049000384286046s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:46:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[5e75a17c-12e5-4214-85f9-7597d8cd180d] received
[2026-03-23 05:46:33,999: INFO/MainProcess] Task tasks.collect_system_metrics[5e75a17c-12e5-4214-85f9-7597d8cd180d] succeeded in 0.5167600000277162s: {'cpu': 17.5, 'memory': 41.0}
[2026-03-23 05:46:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[e7b35210-b6e2-4a85-a586-b45077f4316a] received
[2026-03-23 05:46:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[e7b35210-b6e2-4a85-a586-b45077f4316a] succeeded in 0.0033390999888069928s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:47:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[2b9c697e-cbae-42d2-9a7d-6d479e0bb35b] received
[2026-03-23 05:47:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[2b9c697e-cbae-42d2-9a7d-6d479e0bb35b] succeeded in 0.0029979999526403844s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:47:33,744: INFO/MainProcess] Task tasks.scrape_pending_urls[0d6b831b-4435-49e5-83df-7f5c6772a6b4] received
[2026-03-23 05:47:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[0d6b831b-4435-49e5-83df-7f5c6772a6b4] succeeded in 0.0032288000220432878s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:48:03,745: INFO/MainProcess] Task tasks.scrape_pending_urls[44fcb31c-7ead-4dd8-b1d0-e48d016c34e4] received
[2026-03-23 05:48:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[44fcb31c-7ead-4dd8-b1d0-e48d016c34e4] succeeded in 0.0031658000079914927s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:48:33,745: INFO/MainProcess] Task tasks.scrape_pending_urls[2d80d4f5-7433-4c3b-8e8d-a5631fddf8b0] received
[2026-03-23 05:48:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[2d80d4f5-7433-4c3b-8e8d-a5631fddf8b0] succeeded in 0.0033229999826289713s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:49:03,745: INFO/MainProcess] Task tasks.scrape_pending_urls[4bc726e7-31a0-4c12-8bbe-106daff2411d] received
[2026-03-23 05:49:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[4bc726e7-31a0-4c12-8bbe-106daff2411d] succeeded in 0.003131199977360666s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:49:33,744: INFO/MainProcess] Task tasks.scrape_pending_urls[9d2cf760-6def-49c8-b093-8245139576c7] received
[2026-03-23 05:49:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[9d2cf760-6def-49c8-b093-8245139576c7] succeeded in 0.0032241999870166183s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:50:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[6877f96c-37b0-4ec8-939d-ee0679c23737] received
[2026-03-23 05:50:03,751: INFO/MainProcess] Task tasks.scrape_pending_urls[6877f96c-37b0-4ec8-939d-ee0679c23737] succeeded in 0.003056399989873171s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:50:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[391169d7-fa45-4426-b4bb-b27cc91e2f5f] received
[2026-03-23 05:50:33,751: INFO/MainProcess] Task tasks.scrape_pending_urls[391169d7-fa45-4426-b4bb-b27cc91e2f5f] succeeded in 0.003253100032452494s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:51:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[9bdeee3f-1f45-4663-96fc-536bcf9054e1] received
[2026-03-23 05:51:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[9bdeee3f-1f45-4663-96fc-536bcf9054e1] succeeded in 0.0033192000119015574s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:51:33,482: INFO/MainProcess] Task tasks.collect_system_metrics[480aa145-8e14-4156-afbc-ddbacfa39177] received
[2026-03-23 05:51:33,999: INFO/MainProcess] Task tasks.collect_system_metrics[480aa145-8e14-4156-afbc-ddbacfa39177] succeeded in 0.5166085999808274s: {'cpu': 16.6, 'memory': 40.8}
[2026-03-23 05:51:34,001: INFO/MainProcess] Task tasks.scrape_pending_urls[5aee299a-cb80-4ae0-b8e4-49558bf08f53] received
[2026-03-23 05:51:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[5aee299a-cb80-4ae0-b8e4-49558bf08f53] succeeded in 0.00362700002733618s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:52:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[7a12588a-56a8-49ed-ad82-7ea46be1c6b2] received
[2026-03-23 05:52:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[7a12588a-56a8-49ed-ad82-7ea46be1c6b2] succeeded in 0.003715700004249811s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:52:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[75854c25-5839-4348-8a69-7dde94c0a672] received
[2026-03-23 05:52:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[75854c25-5839-4348-8a69-7dde94c0a672] succeeded in 0.003116499981842935s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:53:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[ee55d1bf-8839-49c9-8c3a-9c05d8a7ee94] received
[2026-03-23 05:53:03,753: INFO/MainProcess] Task tasks.scrape_pending_urls[ee55d1bf-8839-49c9-8c3a-9c05d8a7ee94] succeeded in 0.0038278999854810536s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:53:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[c99bd669-891f-49a8-81b4-616f27fc9976] received
[2026-03-23 05:53:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[c99bd669-891f-49a8-81b4-616f27fc9976] succeeded in 0.0032107000006362796s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:54:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[88b4bfc6-3f9d-4d1a-a830-5a32f1adb2f2] received
[2026-03-23 05:54:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[88b4bfc6-3f9d-4d1a-a830-5a32f1adb2f2] succeeded in 0.003362000046763569s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:54:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[73ccac78-9d58-4807-a8a7-3c63a98e6e1d] received
[2026-03-23 05:54:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[73ccac78-9d58-4807-a8a7-3c63a98e6e1d] succeeded in 0.00304759998107329s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:55:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[c465f6df-4652-4230-b0e2-ca2ef8270979] received
[2026-03-23 05:55:03,753: INFO/MainProcess] Task tasks.scrape_pending_urls[c465f6df-4652-4230-b0e2-ca2ef8270979] succeeded in 0.003501200000755489s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:55:33,749: INFO/MainProcess] Task tasks.scrape_pending_urls[74804ace-a353-4c67-bdaa-473c781ca4b8] received
[2026-03-23 05:55:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[74804ace-a353-4c67-bdaa-473c781ca4b8] succeeded in 0.003311699954792857s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:56:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[408012e2-b61c-4947-bf4e-4028b47aeae8] received
[2026-03-23 05:56:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[408012e2-b61c-4947-bf4e-4028b47aeae8] succeeded in 0.0033616000437177718s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:56:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[8e3270bc-74fb-4c07-8881-9124725ac6d6] received
[2026-03-23 05:56:34,003: INFO/MainProcess] Task tasks.collect_system_metrics[8e3270bc-74fb-4c07-8881-9124725ac6d6] succeeded in 0.5163785999757238s: {'cpu': 14.1, 'memory': 40.8}
[2026-03-23 05:56:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[7ae382a5-1c43-4639-b30a-2c2e65d78bd7] received
[2026-03-23 05:56:34,009: INFO/MainProcess] Task tasks.scrape_pending_urls[7ae382a5-1c43-4639-b30a-2c2e65d78bd7] succeeded in 0.0033496000105515122s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:57:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[38bb8e49-bf32-42cf-8c6e-25546364e92d] received
[2026-03-23 05:57:03,753: INFO/MainProcess] Task tasks.scrape_pending_urls[38bb8e49-bf32-42cf-8c6e-25546364e92d] succeeded in 0.003573399968445301s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:57:33,748: INFO/MainProcess] Task tasks.scrape_pending_urls[69c1e86d-7378-4b5a-9b9f-cfce4cd15144] received
[2026-03-23 05:57:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[69c1e86d-7378-4b5a-9b9f-cfce4cd15144] succeeded in 0.003042199998162687s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:58:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[2b8f3b2e-33f6-4529-a0f0-c8d619f6e13a] received
[2026-03-23 05:58:03,753: INFO/MainProcess] Task tasks.scrape_pending_urls[2b8f3b2e-33f6-4529-a0f0-c8d619f6e13a] succeeded in 0.003729799995198846s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:58:33,749: INFO/MainProcess] Task tasks.scrape_pending_urls[2364d4d1-0e8e-4e1f-9b9b-5f8c75b30a92] received
[2026-03-23 05:58:33,755: INFO/MainProcess] Task tasks.scrape_pending_urls[2364d4d1-0e8e-4e1f-9b9b-5f8c75b30a92] succeeded in 0.004896000027656555s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:59:03,749: INFO/MainProcess] Task tasks.scrape_pending_urls[34f28963-20f1-4fb9-9e6c-fb207aa38cbd] received
[2026-03-23 05:59:03,753: INFO/MainProcess] Task tasks.scrape_pending_urls[34f28963-20f1-4fb9-9e6c-fb207aa38cbd] succeeded in 0.004075800010468811s: {'status': 'idle', 'pending': 0}
[2026-03-23 05:59:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[bb5928e3-c207-4b08-918a-418949a2cf98] received
[2026-03-23 05:59:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[bb5928e3-c207-4b08-918a-418949a2cf98] succeeded in 0.0031177999917417765s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:00:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[6667e33b-5484-437c-9349-32e7b0523a72] received
[2026-03-23 06:00:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[6667e33b-5484-437c-9349-32e7b0523a72] succeeded in 0.003050300001632422s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:00:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[c73e4cb4-4014-4a3a-af37-c4d761ec9265] received
[2026-03-23 06:00:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[c73e4cb4-4014-4a3a-af37-c4d761ec9265] succeeded in 0.003549200017005205s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:01:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[b1e533cc-3708-40a4-a7b6-41041e51661c] received
[2026-03-23 06:01:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[b1e533cc-3708-40a4-a7b6-41041e51661c] succeeded in 0.003293000045232475s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:01:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[a3566dce-64dc-4918-8711-f949d3d4bff0] received
[2026-03-23 06:01:34,003: INFO/MainProcess] Task tasks.collect_system_metrics[a3566dce-64dc-4918-8711-f949d3d4bff0] succeeded in 0.516517499985639s: {'cpu': 12.5, 'memory': 40.8}
[2026-03-23 06:01:34,006: INFO/MainProcess] Task tasks.scrape_pending_urls[cabda39f-fb2b-4997-9652-c2ff4db7745c] received
[2026-03-23 06:01:34,009: INFO/MainProcess] Task tasks.scrape_pending_urls[cabda39f-fb2b-4997-9652-c2ff4db7745c] succeeded in 0.0033705999958328903s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:02:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[a963db53-9d83-4751-bac7-8b2ca2890009] received
[2026-03-23 06:02:03,755: INFO/MainProcess] Task tasks.scrape_pending_urls[a963db53-9d83-4751-bac7-8b2ca2890009] succeeded in 0.0029814000008627772s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:02:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[491a6fa6-0189-4e5e-92c1-507cd9a0aec5] received
[2026-03-23 06:02:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[491a6fa6-0189-4e5e-92c1-507cd9a0aec5] succeeded in 0.0032829000265337527s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:03:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[56841479-9c22-4181-aae1-73eda6c12200] received
[2026-03-23 06:03:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[56841479-9c22-4181-aae1-73eda6c12200] succeeded in 0.003002000041306019s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:03:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[ac74facd-b9b1-4328-b6f9-0523d6427992] received
[2026-03-23 06:03:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[ac74facd-b9b1-4328-b6f9-0523d6427992] succeeded in 0.003118499997071922s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:04:03,753: INFO/MainProcess] Task tasks.scrape_pending_urls[1fb630b9-d8d2-456a-ac19-82f47485d2c9] received
[2026-03-23 06:04:03,757: INFO/MainProcess] Task tasks.scrape_pending_urls[1fb630b9-d8d2-456a-ac19-82f47485d2c9] succeeded in 0.003920599992852658s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:04:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[6e474e30-68a0-4aa0-996c-450af0ad55f2] received
[2026-03-23 06:04:33,755: INFO/MainProcess] Task tasks.scrape_pending_urls[6e474e30-68a0-4aa0-996c-450af0ad55f2] succeeded in 0.0030444999574683607s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:05:03,752: INFO/MainProcess] Task tasks.scrape_pending_urls[ae69ae60-0a2b-4ca4-b93a-cf4ef311c8f9] received
[2026-03-23 06:05:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[ae69ae60-0a2b-4ca4-b93a-cf4ef311c8f9] succeeded in 0.0032913999748416245s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:05:33,752: INFO/MainProcess] Task tasks.scrape_pending_urls[4b7fe966-6a96-48e1-9054-449d3035eb16] received
[2026-03-23 06:05:33,755: INFO/MainProcess] Task tasks.scrape_pending_urls[4b7fe966-6a96-48e1-9054-449d3035eb16] succeeded in 0.0029946999857202172s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:06:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[8862d0e1-dbe3-4e27-87ba-538293afbe8e] received
[2026-03-23 06:06:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[8862d0e1-dbe3-4e27-87ba-538293afbe8e] succeeded in 0.0031656999490223825s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:06:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[211f40d9-1ddf-441d-af3a-af66e81bcc40] received
[2026-03-23 06:06:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 06:06:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[211f40d9-1ddf-441d-af3a-af66e81bcc40] succeeded in 0.004253899969626218s: {'reset': 0}
[2026-03-23 06:06:33,486: INFO/MainProcess] Task tasks.collect_system_metrics[11ef60b5-36bc-4d2b-896c-4d1a54831e63] received
[2026-03-23 06:06:34,003: INFO/MainProcess] Task tasks.collect_system_metrics[11ef60b5-36bc-4d2b-896c-4d1a54831e63] succeeded in 0.5165003000292927s: {'cpu': 16.8, 'memory': 40.9}
[2026-03-23 06:06:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[07f96a10-ae2f-49c2-a792-abbf8d8dd391] received
[2026-03-23 06:06:34,009: INFO/MainProcess] Task tasks.scrape_pending_urls[07f96a10-ae2f-49c2-a792-abbf8d8dd391] succeeded in 0.0037857999559491873s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:07:03,757: INFO/MainProcess] Task tasks.scrape_pending_urls[6f780dc1-7678-4a8c-b027-bf35b1df6fc7] received
[2026-03-23 06:07:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[6f780dc1-7678-4a8c-b027-bf35b1df6fc7] succeeded in 0.0032739000162109733s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:07:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[05551064-8441-4a3f-a487-2bf6ee04e9d9] received
[2026-03-23 06:07:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[05551064-8441-4a3f-a487-2bf6ee04e9d9] succeeded in 0.0033754000323824584s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:08:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[62cf1373-b5c1-4e96-a531-b7980cfa97b1] received
[2026-03-23 06:08:03,759: INFO/MainProcess] Task tasks.scrape_pending_urls[62cf1373-b5c1-4e96-a531-b7980cfa97b1] succeeded in 0.0029612999642267823s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:08:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[bb4187aa-30cb-4d09-9b91-026086e3d769] received
[2026-03-23 06:08:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[bb4187aa-30cb-4d09-9b91-026086e3d769] succeeded in 0.003396500018425286s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:09:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[df27adb1-394d-4127-9146-e01f631c78d7] received
[2026-03-23 06:09:03,759: INFO/MainProcess] Task tasks.scrape_pending_urls[df27adb1-394d-4127-9146-e01f631c78d7] succeeded in 0.0030462999711744487s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:09:33,757: INFO/MainProcess] Task tasks.scrape_pending_urls[cfa186e7-37d8-4680-9cb4-f6ca9df08ba8] received
[2026-03-23 06:09:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[cfa186e7-37d8-4680-9cb4-f6ca9df08ba8] succeeded in 0.003208099980838597s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:10:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[a7a47665-66ad-443d-8e40-d8cc608516be] received
[2026-03-23 06:10:03,759: INFO/MainProcess] Task tasks.scrape_pending_urls[a7a47665-66ad-443d-8e40-d8cc608516be] succeeded in 0.0030397999798879027s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:10:33,756: INFO/MainProcess] Task tasks.scrape_pending_urls[d0a7a8fb-9900-4b2f-b75f-11ba16ed2e2e] received
[2026-03-23 06:10:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[d0a7a8fb-9900-4b2f-b75f-11ba16ed2e2e] succeeded in 0.003183000022545457s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:11:03,757: INFO/MainProcess] Task tasks.scrape_pending_urls[76968a16-c9da-4700-a314-809754fb1799] received
[2026-03-23 06:11:03,761: INFO/MainProcess] Task tasks.scrape_pending_urls[76968a16-c9da-4700-a314-809754fb1799] succeeded in 0.0037134999874979258s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:11:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[dac739ea-037c-46c9-9cc8-ab0e0fae1d0b] received
[2026-03-23 06:11:34,005: INFO/MainProcess] Task tasks.collect_system_metrics[dac739ea-037c-46c9-9cc8-ab0e0fae1d0b] succeeded in 0.5173224000027403s: {'cpu': 15.0, 'memory': 40.8}
[2026-03-23 06:11:34,007: INFO/MainProcess] Task tasks.scrape_pending_urls[76839868-e978-4bae-b4f9-120a3f647d4d] received
[2026-03-23 06:11:34,075: INFO/MainProcess] Task tasks.scrape_pending_urls[76839868-e978-4bae-b4f9-120a3f647d4d] succeeded in 0.06818189995829016s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:12:03,756: INFO/MainProcess] Task tasks.scrape_pending_urls[076c8269-5621-4114-96b5-774d4aab621a] received
[2026-03-23 06:12:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[076c8269-5621-4114-96b5-774d4aab621a] succeeded in 0.003327000013086945s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:12:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[42913608-d703-4b2c-95b2-98e9cf331027] received
[2026-03-23 06:12:33,918: INFO/MainProcess] Task tasks.scrape_pending_urls[42913608-d703-4b2c-95b2-98e9cf331027] succeeded in 0.15790290001314133s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:13:03,759: INFO/MainProcess] Task tasks.scrape_pending_urls[72d3b030-875c-479a-b8e0-9977d403622d] received
[2026-03-23 06:13:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[72d3b030-875c-479a-b8e0-9977d403622d] succeeded in 0.00360630004433915s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:13:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[55e0c880-2bc9-40d5-81ef-267af9a28879] received
[2026-03-23 06:13:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[55e0c880-2bc9-40d5-81ef-267af9a28879] succeeded in 0.0032042000093497336s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:14:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[824403da-1eb8-45ac-950b-105e9a414020] received
[2026-03-23 06:14:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[824403da-1eb8-45ac-950b-105e9a414020] succeeded in 0.0032192000071518123s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:14:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[0780ee83-a5ab-493b-8486-8ff1e0761418] received
[2026-03-23 06:14:33,764: INFO/MainProcess] Task tasks.scrape_pending_urls[0780ee83-a5ab-493b-8486-8ff1e0761418] succeeded in 0.0034645000123418868s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:15:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[07f4d967-9f39-459c-a187-9e298c5cc1e0] received
[2026-03-23 06:15:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[07f4d967-9f39-459c-a187-9e298c5cc1e0] succeeded in 0.0030485999886877835s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:15:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[f5f8cc7c-a7c7-4097-b155-4d65f888470f] received
[2026-03-23 06:15:33,764: INFO/MainProcess] Task tasks.scrape_pending_urls[f5f8cc7c-a7c7-4097-b155-4d65f888470f] succeeded in 0.0035368999815545976s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:16:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[e76b2ad0-aea8-443c-8e34-f1693baee4dc] received
[2026-03-23 06:16:03,764: INFO/MainProcess] Task tasks.scrape_pending_urls[e76b2ad0-aea8-443c-8e34-f1693baee4dc] succeeded in 0.003530200046952814s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:16:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[9224120d-e30e-4898-8a50-2d4455066229] received
[2026-03-23 06:16:34,003: INFO/MainProcess] Task tasks.collect_system_metrics[9224120d-e30e-4898-8a50-2d4455066229] succeeded in 0.5162754000048153s: {'cpu': 14.3, 'memory': 40.8}
[2026-03-23 06:16:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[5d6b0b30-e465-48a0-9210-38b1961c1cb9] received
[2026-03-23 06:16:34,009: INFO/MainProcess] Task tasks.scrape_pending_urls[5d6b0b30-e465-48a0-9210-38b1961c1cb9] succeeded in 0.0035241000005044043s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:17:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[b446bd78-6da7-40d2-98d7-0f35cae016aa] received
[2026-03-23 06:17:03,764: INFO/MainProcess] Task tasks.scrape_pending_urls[b446bd78-6da7-40d2-98d7-0f35cae016aa] succeeded in 0.0034132999717257917s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:17:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[912e44e5-e3ec-40a7-a21e-3987c38fcf6d] received
[2026-03-23 06:17:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[912e44e5-e3ec-40a7-a21e-3987c38fcf6d] succeeded in 0.0034016999998129904s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:18:03,760: INFO/MainProcess] Task tasks.scrape_pending_urls[d9c488ee-5305-4413-a91f-4bd0fa8999be] received
[2026-03-23 06:18:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[d9c488ee-5305-4413-a91f-4bd0fa8999be] succeeded in 0.0032327999942936003s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:18:33,760: INFO/MainProcess] Task tasks.scrape_pending_urls[c6c78186-afd3-4edd-9608-caab49d60821] received
[2026-03-23 06:18:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[c6c78186-afd3-4edd-9608-caab49d60821] succeeded in 0.003470199997536838s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:19:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[51d36c01-ac2a-4332-bcfb-b3e0393722e6] received
[2026-03-23 06:19:03,830: INFO/MainProcess] Task tasks.scrape_pending_urls[51d36c01-ac2a-4332-bcfb-b3e0393722e6] succeeded in 0.06599869998171926s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:19:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[cd252e03-9d71-403d-ba70-2dfe67085e19] received
[2026-03-23 06:19:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[cd252e03-9d71-403d-ba70-2dfe67085e19] succeeded in 0.0034904000349342823s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:20:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[e5300ffc-cdc6-4aa7-bd9c-bf2afa6c7ce1] received
[2026-03-23 06:20:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[e5300ffc-cdc6-4aa7-bd9c-bf2afa6c7ce1] succeeded in 0.0031636000494472682s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:20:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[0d0dd9b9-6e89-4862-9531-e46ec70b7ad8] received
[2026-03-23 06:20:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[0d0dd9b9-6e89-4862-9531-e46ec70b7ad8] succeeded in 0.003437699982896447s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:21:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[e678883c-dcee-4d4b-840a-3d04cdf8d157] received
[2026-03-23 06:21:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[e678883c-dcee-4d4b-840a-3d04cdf8d157] succeeded in 0.003476699988823384s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:21:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[edaab248-03e2-4af2-84e8-6e22d5575a65] received
[2026-03-23 06:21:34,007: INFO/MainProcess] Task tasks.collect_system_metrics[edaab248-03e2-4af2-84e8-6e22d5575a65] succeeded in 0.5197617000085302s: {'cpu': 13.2, 'memory': 40.8}
[2026-03-23 06:21:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[4dd234fe-8620-4186-a0e4-70729a9a33d8] received
[2026-03-23 06:21:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[4dd234fe-8620-4186-a0e4-70729a9a33d8] succeeded in 0.006980800011660904s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:22:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[14d0d53b-55c4-4d55-b60e-c61e0f5566d2] received
[2026-03-23 06:22:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[14d0d53b-55c4-4d55-b60e-c61e0f5566d2] succeeded in 0.0031156999757513404s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:22:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[847a702e-c72b-4a56-adcb-9a5dbc3069e1] received
[2026-03-23 06:22:33,766: INFO/MainProcess] Task tasks.scrape_pending_urls[847a702e-c72b-4a56-adcb-9a5dbc3069e1] succeeded in 0.0032415000023320317s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:23:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[002ba063-e9ef-46cc-9a52-a61107ceef7d] received
[2026-03-23 06:23:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[002ba063-e9ef-46cc-9a52-a61107ceef7d] succeeded in 0.0032730000093579292s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:23:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[eb3ebceb-df55-4a6e-9966-a018e90d80ed] received
[2026-03-23 06:23:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[eb3ebceb-df55-4a6e-9966-a018e90d80ed] succeeded in 0.0037134999874979258s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:24:03,763: INFO/MainProcess] Task tasks.scrape_pending_urls[d7b629b1-dbcb-40bc-88c2-76d982d62c4c] received
[2026-03-23 06:24:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[d7b629b1-dbcb-40bc-88c2-76d982d62c4c] succeeded in 0.003302199998870492s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:24:33,763: INFO/MainProcess] Task tasks.scrape_pending_urls[483860b9-9ce6-4193-9f36-f32d3a36a62e] received
[2026-03-23 06:24:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[483860b9-9ce6-4193-9f36-f32d3a36a62e] succeeded in 0.003308999992441386s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:25:03,764: INFO/MainProcess] Task tasks.scrape_pending_urls[1b8b61fb-39e4-4f68-b06d-e9f23160963e] received
[2026-03-23 06:25:03,768: INFO/MainProcess] Task tasks.scrape_pending_urls[1b8b61fb-39e4-4f68-b06d-e9f23160963e] succeeded in 0.003854100010357797s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:25:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[edfeceee-93ec-4660-8c32-c90c669f021b] received
[2026-03-23 06:25:33,770: INFO/MainProcess] Task tasks.scrape_pending_urls[edfeceee-93ec-4660-8c32-c90c669f021b] succeeded in 0.0030676000169478357s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:26:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[d4cfc99c-ada4-437d-8322-5271f47ec53f] received
[2026-03-23 06:26:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[d4cfc99c-ada4-437d-8322-5271f47ec53f] succeeded in 0.0035081999958492815s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:26:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[c47eddca-982a-48c2-ab18-bbdba60bd0ef] received
[2026-03-23 06:26:34,006: INFO/MainProcess] Task tasks.collect_system_metrics[c47eddca-982a-48c2-ab18-bbdba60bd0ef] succeeded in 0.5189694000291638s: {'cpu': 19.3, 'memory': 40.9}
[2026-03-23 06:26:34,008: INFO/MainProcess] Task tasks.scrape_pending_urls[2db667a9-9503-4a85-8d10-c672b86342c1] received
[2026-03-23 06:26:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[2db667a9-9503-4a85-8d10-c672b86342c1] succeeded in 0.0035247000050731003s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:27:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[c174011d-f514-4971-ab99-a9217eb0bf5d] received
[2026-03-23 06:27:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[c174011d-f514-4971-ab99-a9217eb0bf5d] succeeded in 0.0033958000130951405s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:27:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[ab543acb-d104-43fc-a03b-83e758bc2cfd] received
[2026-03-23 06:27:33,770: INFO/MainProcess] Task tasks.scrape_pending_urls[ab543acb-d104-43fc-a03b-83e758bc2cfd] succeeded in 0.0030301999649964273s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:28:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[86e714b4-0e68-41f8-90bc-77d3cbd2842d] received
[2026-03-23 06:28:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[86e714b4-0e68-41f8-90bc-77d3cbd2842d] succeeded in 0.003037000016774982s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:28:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[aae9e238-1585-4e6a-b879-637014dde0d5] received
[2026-03-23 06:28:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[aae9e238-1585-4e6a-b879-637014dde0d5] succeeded in 0.003278499993029982s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:29:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[4f27406d-601d-4dda-9d58-ec653d66d53e] received
[2026-03-23 06:29:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[4f27406d-601d-4dda-9d58-ec653d66d53e] succeeded in 0.0033195000141859055s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:29:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[032edabd-8246-454a-84f3-bbb5ffd90686] received
[2026-03-23 06:29:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[032edabd-8246-454a-84f3-bbb5ffd90686] succeeded in 0.003116799984127283s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[b37a9633-cf9e-43ea-a191-44a5f214389b] received
[2026-03-23 06:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[b37a9633-cf9e-43ea-a191-44a5f214389b] succeeded in 0.001721500011626631s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 06:30:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[6c93120d-42db-4a7b-a708-6e1938ccbd7f] received
[2026-03-23 06:30:03,770: INFO/MainProcess] Task tasks.scrape_pending_urls[6c93120d-42db-4a7b-a708-6e1938ccbd7f] succeeded in 0.0032464000396430492s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:30:33,767: INFO/MainProcess] Task tasks.scrape_pending_urls[1dad39a4-043e-43d4-99c1-d43f3ee0c852] received
[2026-03-23 06:30:33,770: INFO/MainProcess] Task tasks.scrape_pending_urls[1dad39a4-043e-43d4-99c1-d43f3ee0c852] succeeded in 0.0030765000265091658s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:31:03,768: INFO/MainProcess] Task tasks.scrape_pending_urls[1792fcea-04d7-4ac5-91e8-5fb05111da61] received
[2026-03-23 06:31:03,772: INFO/MainProcess] Task tasks.scrape_pending_urls[1792fcea-04d7-4ac5-91e8-5fb05111da61] succeeded in 0.003652299987152219s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:31:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[aed2a6ae-5c64-42ce-9ce2-6983abb41a15] received
[2026-03-23 06:31:34,006: INFO/MainProcess] Task tasks.collect_system_metrics[aed2a6ae-5c64-42ce-9ce2-6983abb41a15] succeeded in 0.5188198999967426s: {'cpu': 15.1, 'memory': 41.1}
[2026-03-23 06:31:34,008: INFO/MainProcess] Task tasks.scrape_pending_urls[0d5bb82a-fab0-4491-b8dd-cda0ebd86b50] received
[2026-03-23 06:31:34,011: INFO/MainProcess] Task tasks.scrape_pending_urls[0d5bb82a-fab0-4491-b8dd-cda0ebd86b50] succeeded in 0.0033540999866090715s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:32:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[c8060153-6915-429b-b985-9ad2be33928d] received
[2026-03-23 06:32:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[c8060153-6915-429b-b985-9ad2be33928d] succeeded in 0.003101699985563755s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:32:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[953537c8-4df6-4e54-bce7-91e4408a43ac] received
[2026-03-23 06:32:33,774: INFO/MainProcess] Task tasks.scrape_pending_urls[953537c8-4df6-4e54-bce7-91e4408a43ac] succeeded in 0.003070100035984069s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:33:03,770: INFO/MainProcess] Task tasks.scrape_pending_urls[f15f6db8-ac56-4d44-b900-a5e6e7b072dc] received
[2026-03-23 06:33:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[f15f6db8-ac56-4d44-b900-a5e6e7b072dc] succeeded in 0.0035711000091396272s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:33:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[62bfc9b2-25ba-4d2e-b9ab-83365e767824] received
[2026-03-23 06:33:33,774: INFO/MainProcess] Task tasks.scrape_pending_urls[62bfc9b2-25ba-4d2e-b9ab-83365e767824] succeeded in 0.0030717000481672585s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:34:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[bcb358df-78fd-459e-bf06-36437fdde61d] received
[2026-03-23 06:34:03,775: INFO/MainProcess] Task tasks.scrape_pending_urls[bcb358df-78fd-459e-bf06-36437fdde61d] succeeded in 0.004062599968165159s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:34:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[a2cdd5a4-f7c4-4b37-b8b1-517be7d75de0] received
[2026-03-23 06:34:33,775: INFO/MainProcess] Task tasks.scrape_pending_urls[a2cdd5a4-f7c4-4b37-b8b1-517be7d75de0] succeeded in 0.003255499992519617s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:35:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[58785124-d08f-45f8-a1c9-e301ff1e73d0] received
[2026-03-23 06:35:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[58785124-d08f-45f8-a1c9-e301ff1e73d0] succeeded in 0.003195700002834201s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:35:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[c9b60c90-f426-4156-b4a6-7463449fb9a0] received
[2026-03-23 06:35:33,774: INFO/MainProcess] Task tasks.scrape_pending_urls[c9b60c90-f426-4156-b4a6-7463449fb9a0] succeeded in 0.00309070001821965s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:36:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[4ef848dc-6417-461a-be50-733f0e97472b] received
[2026-03-23 06:36:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[4ef848dc-6417-461a-be50-733f0e97472b] succeeded in 0.0032039000070653856s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:36:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d2d574dd-b5b7-4aed-9d68-c8fdf7009590] received
[2026-03-23 06:36:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 06:36:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d2d574dd-b5b7-4aed-9d68-c8fdf7009590] succeeded in 0.003847600019071251s: {'reset': 0}
[2026-03-23 06:36:33,486: INFO/MainProcess] Task tasks.collect_system_metrics[c0a63091-2d82-4d09-a21b-0d11a36c97de] received
[2026-03-23 06:36:34,003: INFO/MainProcess] Task tasks.collect_system_metrics[c0a63091-2d82-4d09-a21b-0d11a36c97de] succeeded in 0.5162839000113308s: {'cpu': 15.6, 'memory': 40.9}
[2026-03-23 06:36:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[942d3a09-5095-4905-9e59-0ad481be7db5] received
[2026-03-23 06:36:34,008: INFO/MainProcess] Task tasks.scrape_pending_urls[942d3a09-5095-4905-9e59-0ad481be7db5] succeeded in 0.0033549999934621155s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:37:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[91d16612-dc63-45e8-b9a0-c93d3c74ada4] received
[2026-03-23 06:37:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[91d16612-dc63-45e8-b9a0-c93d3c74ada4] succeeded in 0.003091600025072694s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:37:33,771: INFO/MainProcess] Task tasks.scrape_pending_urls[1c39826b-1759-44fa-87e0-a64a01a12784] received
[2026-03-23 06:37:33,775: INFO/MainProcess] Task tasks.scrape_pending_urls[1c39826b-1759-44fa-87e0-a64a01a12784] succeeded in 0.0034873999538831413s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:38:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[b70dd4e2-4dd3-4565-8641-20344332c727] received
[2026-03-23 06:38:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[b70dd4e2-4dd3-4565-8641-20344332c727] succeeded in 0.0030081000295467675s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:38:33,774: INFO/MainProcess] Task tasks.scrape_pending_urls[f44527d1-8da9-428f-9138-dacafd3d3eee] received
[2026-03-23 06:38:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[f44527d1-8da9-428f-9138-dacafd3d3eee] succeeded in 0.00364319997606799s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:39:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[9b1595c1-cba6-4e1a-b7fc-a263e3f09fb7] received
[2026-03-23 06:39:03,777: INFO/MainProcess] Task tasks.scrape_pending_urls[9b1595c1-cba6-4e1a-b7fc-a263e3f09fb7] succeeded in 0.003047300036996603s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:39:33,774: INFO/MainProcess] Task tasks.scrape_pending_urls[ff67d38b-c6e7-4bf2-bdec-84f2d288e9cc] received
[2026-03-23 06:39:33,778: INFO/MainProcess] Task tasks.scrape_pending_urls[ff67d38b-c6e7-4bf2-bdec-84f2d288e9cc] succeeded in 0.0031288000172935426s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:40:03,775: INFO/MainProcess] Task tasks.scrape_pending_urls[81b393fa-3ed5-4d2d-bf6e-0314acbc7a97] received
[2026-03-23 06:40:03,778: INFO/MainProcess] Task tasks.scrape_pending_urls[81b393fa-3ed5-4d2d-bf6e-0314acbc7a97] succeeded in 0.003063000040128827s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:40:33,775: INFO/MainProcess] Task tasks.scrape_pending_urls[568f8e20-ac45-4a03-aba9-334e345ad3bd] received
[2026-03-23 06:40:33,778: INFO/MainProcess] Task tasks.scrape_pending_urls[568f8e20-ac45-4a03-aba9-334e345ad3bd] succeeded in 0.0030302999657578766s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:41:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[d03814c7-4df4-463a-b342-273ddbe87f57] received
[2026-03-23 06:41:03,778: INFO/MainProcess] Task tasks.scrape_pending_urls[d03814c7-4df4-463a-b342-273ddbe87f57] succeeded in 0.003583699988666922s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:41:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[413eee45-45c0-4c3e-ab1e-9f414348d8ea] received
[2026-03-23 06:41:34,005: INFO/MainProcess] Task tasks.collect_system_metrics[413eee45-45c0-4c3e-ab1e-9f414348d8ea] succeeded in 0.5173435999895446s: {'cpu': 13.8, 'memory': 41.0}
[2026-03-23 06:41:34,007: INFO/MainProcess] Task tasks.scrape_pending_urls[6122554b-3a40-4aed-8e1c-ee4ba0309529] received
[2026-03-23 06:41:34,011: INFO/MainProcess] Task tasks.scrape_pending_urls[6122554b-3a40-4aed-8e1c-ee4ba0309529] succeeded in 0.003351000021211803s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:42:03,775: INFO/MainProcess] Task tasks.scrape_pending_urls[768c16ad-06ac-4373-b4c1-97086647c7ec] received
[2026-03-23 06:42:03,778: INFO/MainProcess] Task tasks.scrape_pending_urls[768c16ad-06ac-4373-b4c1-97086647c7ec] succeeded in 0.003264600003603846s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:42:33,775: INFO/MainProcess] Task tasks.scrape_pending_urls[b4ca0317-5976-4e8d-8b06-c9c023c64262] received
[2026-03-23 06:42:33,778: INFO/MainProcess] Task tasks.scrape_pending_urls[b4ca0317-5976-4e8d-8b06-c9c023c64262] succeeded in 0.003214599972125143s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:43:03,775: INFO/MainProcess] Task tasks.scrape_pending_urls[2f9e189d-8238-47be-8440-3f3301891d3b] received
[2026-03-23 06:43:03,778: INFO/MainProcess] Task tasks.scrape_pending_urls[2f9e189d-8238-47be-8440-3f3301891d3b] succeeded in 0.003215199976693839s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:43:33,774: INFO/MainProcess] Task tasks.scrape_pending_urls[8d1b8a89-ce7e-4f9d-914c-267fce355add] received
[2026-03-23 06:43:33,778: INFO/MainProcess] Task tasks.scrape_pending_urls[8d1b8a89-ce7e-4f9d-914c-267fce355add] succeeded in 0.003204000007826835s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:44:03,775: INFO/MainProcess] Task tasks.scrape_pending_urls[64f9a0e5-6cf8-4553-98f2-db6fa9b07e8b] received
[2026-03-23 06:44:03,778: INFO/MainProcess] Task tasks.scrape_pending_urls[64f9a0e5-6cf8-4553-98f2-db6fa9b07e8b] succeeded in 0.0030004000291228294s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:44:33,775: INFO/MainProcess] Task tasks.scrape_pending_urls[a98fc24b-e200-435d-a193-b1b39a2050c2] received
[2026-03-23 06:44:33,778: INFO/MainProcess] Task tasks.scrape_pending_urls[a98fc24b-e200-435d-a193-b1b39a2050c2] succeeded in 0.0032016999903135s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:45:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[e3ed0800-cf47-4163-8f38-bc4f62bfb7f3] received
[2026-03-23 06:45:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[e3ed0800-cf47-4163-8f38-bc4f62bfb7f3] succeeded in 0.003023000026587397s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:45:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[77271fa1-8ce1-4fd4-8cb7-79b6f6d49105] received
[2026-03-23 06:45:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[77271fa1-8ce1-4fd4-8cb7-79b6f6d49105] succeeded in 0.0029830000130459666s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:46:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[2df931e9-c91e-4267-a5f1-2192265004e4] received
[2026-03-23 06:46:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[2df931e9-c91e-4267-a5f1-2192265004e4] succeeded in 0.003364300006069243s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:46:33,487: INFO/MainProcess] Task tasks.collect_system_metrics[d4b24aa2-7785-4c4e-b4bc-de08639160e0] received
[2026-03-23 06:46:34,004: INFO/MainProcess] Task tasks.collect_system_metrics[d4b24aa2-7785-4c4e-b4bc-de08639160e0] succeeded in 0.5161810999852605s: {'cpu': 13.1, 'memory': 41.0}
[2026-03-23 06:46:34,006: INFO/MainProcess] Task tasks.scrape_pending_urls[a6a65a3f-977b-420d-badb-a34830dd644d] received
[2026-03-23 06:46:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[a6a65a3f-977b-420d-badb-a34830dd644d] succeeded in 0.003371700004208833s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:47:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[ffca0e1f-0720-4b40-83d9-f2e971251eb7] received
[2026-03-23 06:47:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[ffca0e1f-0720-4b40-83d9-f2e971251eb7] succeeded in 0.0032219000277109444s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:47:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[aa68af80-e4a3-44be-83bf-155581db64f1] received
[2026-03-23 06:47:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[aa68af80-e4a3-44be-83bf-155581db64f1] succeeded in 0.0031410999945364892s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:48:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[5271429f-8e21-4657-9e34-188549b7d12c] received
[2026-03-23 06:48:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[5271429f-8e21-4657-9e34-188549b7d12c] succeeded in 0.0030747000128030777s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:48:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[d87683e5-9462-4391-b5e3-d535a8474a19] received
[2026-03-23 06:48:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[d87683e5-9462-4391-b5e3-d535a8474a19] succeeded in 0.0032103999983519316s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:49:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[56475cf8-05ba-4e21-b9af-1d1682df7ad3] received
[2026-03-23 06:49:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[56475cf8-05ba-4e21-b9af-1d1682df7ad3] succeeded in 0.003173000004608184s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:49:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[94f2158e-c076-4221-9790-c60607aa6a49] received
[2026-03-23 06:49:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[94f2158e-c076-4221-9790-c60607aa6a49] succeeded in 0.0029885999974794686s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:50:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[a03a4916-e4a0-4c86-8ce7-01aa2784eeb5] received
[2026-03-23 06:50:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[a03a4916-e4a0-4c86-8ce7-01aa2784eeb5] succeeded in 0.0029929999727755785s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:50:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[99d1855a-72fa-4bda-be28-fa62fce91c07] received
[2026-03-23 06:50:33,783: INFO/MainProcess] Task tasks.scrape_pending_urls[99d1855a-72fa-4bda-be28-fa62fce91c07] succeeded in 0.0035525000421330333s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:51:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[72456428-b7d0-4877-8813-ef349fceb1eb] received
[2026-03-23 06:51:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[72456428-b7d0-4877-8813-ef349fceb1eb] succeeded in 0.003226200002245605s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:51:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[4fee5997-747d-4546-ac83-64484b024c57] received
[2026-03-23 06:51:34,008: INFO/MainProcess] Task tasks.collect_system_metrics[4fee5997-747d-4546-ac83-64484b024c57] succeeded in 0.516663399990648s: {'cpu': 12.7, 'memory': 41.0}
[2026-03-23 06:51:34,011: INFO/MainProcess] Task tasks.scrape_pending_urls[1f7d0e4b-7707-4986-9b2e-6088e33b3da4] received
[2026-03-23 06:51:34,014: INFO/MainProcess] Task tasks.scrape_pending_urls[1f7d0e4b-7707-4986-9b2e-6088e33b3da4] succeeded in 0.0033135999692603946s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:52:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[b05a5c75-9458-4e94-8e12-e3a936915449] received
[2026-03-23 06:52:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[b05a5c75-9458-4e94-8e12-e3a936915449] succeeded in 0.003367499972227961s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:52:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[d1db9881-f0af-45ca-a792-a133ff8ec164] received
[2026-03-23 06:52:33,783: INFO/MainProcess] Task tasks.scrape_pending_urls[d1db9881-f0af-45ca-a792-a133ff8ec164] succeeded in 0.0033221000339835882s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:53:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[94530806-7541-4a46-b184-c016073a398b] received
[2026-03-23 06:53:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[94530806-7541-4a46-b184-c016073a398b] succeeded in 0.0031504000071436167s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:53:33,779: INFO/MainProcess] Task tasks.scrape_pending_urls[4aac0ad1-b2ab-4c03-aa3b-c47e96ce48bf] received
[2026-03-23 06:53:33,783: INFO/MainProcess] Task tasks.scrape_pending_urls[4aac0ad1-b2ab-4c03-aa3b-c47e96ce48bf] succeeded in 0.003118599997833371s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:54:03,779: INFO/MainProcess] Task tasks.scrape_pending_urls[1bb29131-0229-4101-9c73-47aec2d137d2] received
[2026-03-23 06:54:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[1bb29131-0229-4101-9c73-47aec2d137d2] succeeded in 0.0032711000530980527s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:54:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[536b17c0-8d11-4fd0-9106-f9cf4bd4bcad] received
[2026-03-23 06:54:33,786: INFO/MainProcess] Task tasks.scrape_pending_urls[536b17c0-8d11-4fd0-9106-f9cf4bd4bcad] succeeded in 0.0029015999753028154s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:55:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[f9a97d64-f3a8-446e-a76c-8e59ccfeced8] received
[2026-03-23 06:55:03,785: INFO/MainProcess] Task tasks.scrape_pending_urls[f9a97d64-f3a8-446e-a76c-8e59ccfeced8] succeeded in 0.0030648999963887036s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:55:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[d2312024-0611-48f4-821f-d3d6df85c310] received
[2026-03-23 06:55:33,786: INFO/MainProcess] Task tasks.scrape_pending_urls[d2312024-0611-48f4-821f-d3d6df85c310] succeeded in 0.0034733000211417675s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:56:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[80a6d877-5205-4530-86a1-4e2db3d91583] received
[2026-03-23 06:56:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[80a6d877-5205-4530-86a1-4e2db3d91583] succeeded in 0.003212300012819469s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:56:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[13b17b00-9abb-47e2-ace9-6d7347009054] received
[2026-03-23 06:56:34,008: INFO/MainProcess] Task tasks.collect_system_metrics[13b17b00-9abb-47e2-ace9-6d7347009054] succeeded in 0.5165819000103511s: {'cpu': 14.0, 'memory': 41.0}
[2026-03-23 06:56:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[aaab8d69-6295-4485-a4b1-f3ef6c81c81d] received
[2026-03-23 06:56:34,014: INFO/MainProcess] Task tasks.scrape_pending_urls[aaab8d69-6295-4485-a4b1-f3ef6c81c81d] succeeded in 0.0033626999938860536s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:57:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[45cf8cba-1642-4bd3-b474-f370bd31f941] received
[2026-03-23 06:57:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[45cf8cba-1642-4bd3-b474-f370bd31f941] succeeded in 0.0030140000162646174s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:57:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[82e97e69-e59c-4bfc-b9ff-708a1c9b2035] received
[2026-03-23 06:57:33,785: INFO/MainProcess] Task tasks.scrape_pending_urls[82e97e69-e59c-4bfc-b9ff-708a1c9b2035] succeeded in 0.002976299962028861s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:58:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[8461e198-912a-4521-b69c-42df39bced13] received
[2026-03-23 06:58:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[8461e198-912a-4521-b69c-42df39bced13] succeeded in 0.003124999988358468s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:58:33,782: INFO/MainProcess] Task tasks.scrape_pending_urls[0ef71d20-f8d1-4b88-a6d5-b52c7a3c9767] received
[2026-03-23 06:58:33,786: INFO/MainProcess] Task tasks.scrape_pending_urls[0ef71d20-f8d1-4b88-a6d5-b52c7a3c9767] succeeded in 0.0030051000067032874s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:59:03,782: INFO/MainProcess] Task tasks.scrape_pending_urls[42100ac6-de43-4d7c-9b20-f1956bd0dad7] received
[2026-03-23 06:59:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[42100ac6-de43-4d7c-9b20-f1956bd0dad7] succeeded in 0.003231199982110411s: {'status': 'idle', 'pending': 0}
[2026-03-23 06:59:33,783: INFO/MainProcess] Task tasks.scrape_pending_urls[6bded610-5bb3-49eb-872e-fa8624afa2d4] received
[2026-03-23 06:59:33,786: INFO/MainProcess] Task tasks.scrape_pending_urls[6bded610-5bb3-49eb-872e-fa8624afa2d4] succeeded in 0.0032822999637573957s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:00:03,783: INFO/MainProcess] Task tasks.scrape_pending_urls[0ae7460a-11cc-4410-b24b-8c4860a04f3f] received
[2026-03-23 07:00:03,787: INFO/MainProcess] Task tasks.scrape_pending_urls[0ae7460a-11cc-4410-b24b-8c4860a04f3f] succeeded in 0.0035969000309705734s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:00:33,783: INFO/MainProcess] Task tasks.scrape_pending_urls[f1b807fc-a069-4a6d-b1a5-2ab760abb6f3] received
[2026-03-23 07:00:33,787: INFO/MainProcess] Task tasks.scrape_pending_urls[f1b807fc-a069-4a6d-b1a5-2ab760abb6f3] succeeded in 0.0035170000046491623s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:01:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[2ce18733-106a-4669-9438-4bb5b93cd2ec] received
[2026-03-23 07:01:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[2ce18733-106a-4669-9438-4bb5b93cd2ec] succeeded in 0.003279700002167374s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:01:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[20768e56-e0a3-4028-8d11-90e1c936dc35] received
[2026-03-23 07:01:34,008: INFO/MainProcess] Task tasks.collect_system_metrics[20768e56-e0a3-4028-8d11-90e1c936dc35] succeeded in 0.5168163999915123s: {'cpu': 14.5, 'memory': 41.2}
[2026-03-23 07:01:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[7bbf1850-78e0-4ffe-9cb4-dceefa81a91d] received
[2026-03-23 07:01:34,014: INFO/MainProcess] Task tasks.scrape_pending_urls[7bbf1850-78e0-4ffe-9cb4-dceefa81a91d] succeeded in 0.0037748999893665314s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:02:03,785: INFO/MainProcess] Task tasks.scrape_pending_urls[25f351c0-7a17-480a-b5d4-f4c631bc5720] received
[2026-03-23 07:02:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[25f351c0-7a17-480a-b5d4-f4c631bc5720] succeeded in 0.002996700000949204s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:02:33,785: INFO/MainProcess] Task tasks.scrape_pending_urls[a62f4c72-bc3b-47ca-be34-e5a6c0b1fc90] received
[2026-03-23 07:02:33,789: INFO/MainProcess] Task tasks.scrape_pending_urls[a62f4c72-bc3b-47ca-be34-e5a6c0b1fc90] succeeded in 0.0031760999700054526s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:03:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[7cb9d0ac-1980-4df7-9028-ea5333fbaa4e] received
[2026-03-23 07:03:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[7cb9d0ac-1980-4df7-9028-ea5333fbaa4e] succeeded in 0.002927499997895211s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:03:33,785: INFO/MainProcess] Task tasks.scrape_pending_urls[d656cf7e-4b5a-4262-ad34-0dc3adc0e4b9] received
[2026-03-23 07:03:33,789: INFO/MainProcess] Task tasks.scrape_pending_urls[d656cf7e-4b5a-4262-ad34-0dc3adc0e4b9] succeeded in 0.003041599993593991s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:04:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[c56683ec-06cb-4fd6-a822-a32611150517] received
[2026-03-23 07:04:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[c56683ec-06cb-4fd6-a822-a32611150517] succeeded in 0.003028300008736551s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:04:33,786: INFO/MainProcess] Task tasks.scrape_pending_urls[672acc7f-579f-4428-b38b-28d89d9fcae6] received
[2026-03-23 07:04:33,789: INFO/MainProcess] Task tasks.scrape_pending_urls[672acc7f-579f-4428-b38b-28d89d9fcae6] succeeded in 0.0031543999793939292s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:05:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[c512e7d3-35c5-4401-a786-b35882acff5c] received
[2026-03-23 07:05:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[c512e7d3-35c5-4401-a786-b35882acff5c] succeeded in 0.003132499987259507s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:05:33,786: INFO/MainProcess] Task tasks.scrape_pending_urls[2bc8082f-6057-41b6-a4db-d148f32d1e4a] received
[2026-03-23 07:05:33,789: INFO/MainProcess] Task tasks.scrape_pending_urls[2bc8082f-6057-41b6-a4db-d148f32d1e4a] succeeded in 0.0032097999937832355s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:06:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[0e3df800-d9c0-428a-965b-82f7ba09f7e2] received
[2026-03-23 07:06:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[0e3df800-d9c0-428a-965b-82f7ba09f7e2] succeeded in 0.00319429999217391s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:06:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[46451267-db7e-4638-9cc9-a7257cddcc7e] received
[2026-03-23 07:06:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 07:06:33,477: INFO/MainProcess] Task tasks.reset_stale_processing_urls[46451267-db7e-4638-9cc9-a7257cddcc7e] succeeded in 0.0036330000148154795s: {'reset': 0}
[2026-03-23 07:06:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[0e99c296-91a2-48b9-a97d-352d91d5e23f] received
[2026-03-23 07:06:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[0e99c296-91a2-48b9-a97d-352d91d5e23f] succeeded in 0.51705480000237s: {'cpu': 15.2, 'memory': 41.2}
[2026-03-23 07:06:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[bce11596-9ddb-4377-a86a-42d27a7a1670] received
[2026-03-23 07:06:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[bce11596-9ddb-4377-a86a-42d27a7a1670] succeeded in 0.0036504999734461308s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:07:03,786: INFO/MainProcess] Task tasks.scrape_pending_urls[04fcac16-fe67-4ba1-94cd-d067720092ca] received
[2026-03-23 07:07:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[04fcac16-fe67-4ba1-94cd-d067720092ca] succeeded in 0.0030064000166021287s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:07:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[462cc260-2085-41a9-af00-1a434e4f42de] received
[2026-03-23 07:07:33,793: INFO/MainProcess] Task tasks.scrape_pending_urls[462cc260-2085-41a9-af00-1a434e4f42de] succeeded in 0.003079000045545399s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:08:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[151b32e3-e11c-4551-925b-9a0b30552d0d] received
[2026-03-23 07:08:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[151b32e3-e11c-4551-925b-9a0b30552d0d] succeeded in 0.003056999994441867s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:08:33,789: INFO/MainProcess] Task tasks.scrape_pending_urls[82659158-484f-4e38-91e1-cfb2907cd3be] received
[2026-03-23 07:08:33,793: INFO/MainProcess] Task tasks.scrape_pending_urls[82659158-484f-4e38-91e1-cfb2907cd3be] succeeded in 0.003114099963568151s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:09:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[91898de3-d4ea-4efe-9d6b-074066e68854] received
[2026-03-23 07:09:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[91898de3-d4ea-4efe-9d6b-074066e68854] succeeded in 0.003097499953582883s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:09:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[4d07ec36-2b9c-430e-a3f4-39ae1dadb1e4] received
[2026-03-23 07:09:33,793: INFO/MainProcess] Task tasks.scrape_pending_urls[4d07ec36-2b9c-430e-a3f4-39ae1dadb1e4] succeeded in 0.0029637000407092273s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:10:03,789: INFO/MainProcess] Task tasks.scrape_pending_urls[7cd98b24-7db0-457f-926b-bd742bea147b] received
[2026-03-23 07:10:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[7cd98b24-7db0-457f-926b-bd742bea147b] succeeded in 0.003194199991412461s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:10:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[515451e9-6b07-488a-8430-b3a59d869c08] received
[2026-03-23 07:10:33,793: INFO/MainProcess] Task tasks.scrape_pending_urls[515451e9-6b07-488a-8430-b3a59d869c08] succeeded in 0.003267600026447326s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:11:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[088e84da-98ec-44f9-811b-8e53b2398a43] received
[2026-03-23 07:11:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[088e84da-98ec-44f9-811b-8e53b2398a43] succeeded in 0.0030399999814108014s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:11:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[14157f47-8386-4a05-ac6a-4b51bbf1f4d5] received
[2026-03-23 07:11:34,007: INFO/MainProcess] Task tasks.collect_system_metrics[14157f47-8386-4a05-ac6a-4b51bbf1f4d5] succeeded in 0.5158352999715135s: {'cpu': 16.6, 'memory': 41.2}
[2026-03-23 07:11:34,009: INFO/MainProcess] Task tasks.scrape_pending_urls[258913ac-72bb-404d-8304-5ab28f1c57eb] received
[2026-03-23 07:11:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[258913ac-72bb-404d-8304-5ab28f1c57eb] succeeded in 0.0029267999925650656s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:12:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[71d5e0f3-8f36-4be8-a78d-f101505f89d2] received
[2026-03-23 07:12:03,856: INFO/MainProcess] Task tasks.scrape_pending_urls[71d5e0f3-8f36-4be8-a78d-f101505f89d2] succeeded in 0.06568420003168285s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:12:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[f2702819-e09e-405c-bf72-be46382b63e7] received
[2026-03-23 07:12:33,793: INFO/MainProcess] Task tasks.scrape_pending_urls[f2702819-e09e-405c-bf72-be46382b63e7] succeeded in 0.0032822000212036073s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:13:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[0824c30a-2a1f-4cf3-b79f-a63ec881f46e] received
[2026-03-23 07:13:03,863: INFO/MainProcess] Task tasks.scrape_pending_urls[0824c30a-2a1f-4cf3-b79f-a63ec881f46e] succeeded in 0.07274500001221895s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:13:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[a07eee28-4775-4990-b445-ece5d0e14a1b] received
[2026-03-23 07:13:33,793: INFO/MainProcess] Task tasks.scrape_pending_urls[a07eee28-4775-4990-b445-ece5d0e14a1b] succeeded in 0.0032795000006444752s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:14:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[1888df9d-344a-4f16-97cf-41aabd5227e2] received
[2026-03-23 07:14:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[1888df9d-344a-4f16-97cf-41aabd5227e2] succeeded in 0.0032217000261880457s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:14:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[152a96be-40e1-4f99-be3b-9b3537733d9f] received
[2026-03-23 07:14:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[152a96be-40e1-4f99-be3b-9b3537733d9f] succeeded in 0.003245100029744208s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:15:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[a9336958-11f1-45ba-94ea-d48eb8f54648] received
[2026-03-23 07:15:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[a9336958-11f1-45ba-94ea-d48eb8f54648] succeeded in 0.003457800019532442s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:15:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[16689dc4-5999-40ea-a91b-ed5dc342cae7] received
[2026-03-23 07:15:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[16689dc4-5999-40ea-a91b-ed5dc342cae7] succeeded in 0.0035362999769859016s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:16:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[99123ef6-5428-4d0f-bb4b-ced0bab9896d] received
[2026-03-23 07:16:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[99123ef6-5428-4d0f-bb4b-ced0bab9896d] succeeded in 0.0032949000014923513s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:16:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[f90e646a-f00b-48e8-b39c-b9d413371c4b] received
[2026-03-23 07:16:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[f90e646a-f00b-48e8-b39c-b9d413371c4b] succeeded in 0.5187542000203393s: {'cpu': 12.7, 'memory': 41.3}
[2026-03-23 07:16:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[30f2947d-9922-4370-91b8-c81957ec7f75] received
[2026-03-23 07:16:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[30f2947d-9922-4370-91b8-c81957ec7f75] succeeded in 0.003348700003698468s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:17:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[8205bb2f-3bb8-45ce-8cff-cae6ccb51e2a] received
[2026-03-23 07:17:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[8205bb2f-3bb8-45ce-8cff-cae6ccb51e2a] succeeded in 0.0036821000394411385s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:17:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[aae53b29-4868-45b1-bec0-1af4328d8497] received
[2026-03-23 07:17:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[aae53b29-4868-45b1-bec0-1af4328d8497] succeeded in 0.0034425000194460154s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:18:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[b873c186-ead7-4b73-99a4-ee87085b21eb] received
[2026-03-23 07:18:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[b873c186-ead7-4b73-99a4-ee87085b21eb] succeeded in 0.0032479999936185777s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:18:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[4f9892b9-a66a-4313-83a1-0883973e7120] received
[2026-03-23 07:18:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[4f9892b9-a66a-4313-83a1-0883973e7120] succeeded in 0.0034981000353582203s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:19:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[8456b8c7-3f08-4b34-8206-06b68bcc8fbf] received
[2026-03-23 07:19:03,793: INFO/MainProcess] Task tasks.scrape_pending_urls[8456b8c7-3f08-4b34-8206-06b68bcc8fbf] succeeded in 0.0032173999934457242s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:19:33,790: INFO/MainProcess] Task tasks.scrape_pending_urls[aaf55cbb-7b43-4a73-8bab-7db65f1880e7] received
[2026-03-23 07:19:33,857: INFO/MainProcess] Task tasks.scrape_pending_urls[aaf55cbb-7b43-4a73-8bab-7db65f1880e7] succeeded in 0.06702999997651204s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:20:03,790: INFO/MainProcess] Task tasks.scrape_pending_urls[58d1edc7-b19a-490d-8d67-afe8b89afb62] received
[2026-03-23 07:20:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[58d1edc7-b19a-490d-8d67-afe8b89afb62] succeeded in 0.0033793000038713217s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:20:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[f66ca882-4186-4f2a-9f2b-d3be8a03849d] received
[2026-03-23 07:20:33,797: INFO/MainProcess] Task tasks.scrape_pending_urls[f66ca882-4186-4f2a-9f2b-d3be8a03849d] succeeded in 0.0030949999927543104s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:21:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[56f88428-c994-4ee5-a0ee-f7669fe91d0f] received
[2026-03-23 07:21:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[56f88428-c994-4ee5-a0ee-f7669fe91d0f] succeeded in 0.003530499991029501s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:21:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[6112b33c-1eec-4370-9a49-a476639f6e70] received
[2026-03-23 07:21:34,011: INFO/MainProcess] Task tasks.collect_system_metrics[6112b33c-1eec-4370-9a49-a476639f6e70] succeeded in 0.5191923000384122s: {'cpu': 13.6, 'memory': 41.2}
[2026-03-23 07:21:34,013: INFO/MainProcess] Task tasks.scrape_pending_urls[15982ace-9586-46c7-b700-1f0429151d82] received
[2026-03-23 07:21:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[15982ace-9586-46c7-b700-1f0429151d82] succeeded in 0.0034796999534592032s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:22:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[b44e9841-2185-4f36-8bea-6aa155914977] received
[2026-03-23 07:22:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[b44e9841-2185-4f36-8bea-6aa155914977] succeeded in 0.0034117999603040516s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:22:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[eb097e61-38ba-405c-bba5-a78346ba2899] received
[2026-03-23 07:22:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[eb097e61-38ba-405c-bba5-a78346ba2899] succeeded in 0.003341500007081777s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:23:03,795: INFO/MainProcess] Task tasks.scrape_pending_urls[5bd634e3-ff1d-4135-b360-d7cdab54102e] received
[2026-03-23 07:23:03,799: INFO/MainProcess] Task tasks.scrape_pending_urls[5bd634e3-ff1d-4135-b360-d7cdab54102e] succeeded in 0.0035396000021137297s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:23:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[c889c343-d8c0-4816-a7e9-af20d5ed484f] received
[2026-03-23 07:23:33,797: INFO/MainProcess] Task tasks.scrape_pending_urls[c889c343-d8c0-4816-a7e9-af20d5ed484f] succeeded in 0.0031732000061310828s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:24:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[f923de88-c2b8-4415-b6a7-96dbf50844e4] received
[2026-03-23 07:24:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[f923de88-c2b8-4415-b6a7-96dbf50844e4] succeeded in 0.0032632999937050045s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:24:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[a0fc3c28-950e-4704-840c-fcb99ffd76ea] received
[2026-03-23 07:24:33,797: INFO/MainProcess] Task tasks.scrape_pending_urls[a0fc3c28-950e-4704-840c-fcb99ffd76ea] succeeded in 0.003258200013078749s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:25:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[adcade2c-76e8-4b29-b298-71ca49ac1517] received
[2026-03-23 07:25:03,797: INFO/MainProcess] Task tasks.scrape_pending_urls[adcade2c-76e8-4b29-b298-71ca49ac1517] succeeded in 0.0032186000025831163s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:25:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[3cac9667-13b6-4366-8f09-806a65d53cd9] received
[2026-03-23 07:25:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[3cac9667-13b6-4366-8f09-806a65d53cd9] succeeded in 0.0032416999456472695s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:26:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[f0101e6c-a05b-4436-8f8f-67182b62deba] received
[2026-03-23 07:26:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[f0101e6c-a05b-4436-8f8f-67182b62deba] succeeded in 0.0036105000181123614s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:26:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[83ce3c8b-69bb-4487-a418-cca5f8e8edba] received
[2026-03-23 07:26:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[83ce3c8b-69bb-4487-a418-cca5f8e8edba] succeeded in 0.5191313999821432s: {'cpu': 13.9, 'memory': 41.2}
[2026-03-23 07:26:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[2cb3915c-3941-4576-82b8-7bc02a514cfe] received
[2026-03-23 07:26:34,019: INFO/MainProcess] Task tasks.scrape_pending_urls[2cb3915c-3941-4576-82b8-7bc02a514cfe] succeeded in 0.003161399974487722s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:27:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[e9d5f9f5-117c-4312-8b22-0c7ac7c0480e] received
[2026-03-23 07:27:03,797: INFO/MainProcess] Task tasks.scrape_pending_urls[e9d5f9f5-117c-4312-8b22-0c7ac7c0480e] succeeded in 0.002899700019042939s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:27:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[02bbadd1-557f-4630-a2ba-ac3583012ce8] received
[2026-03-23 07:27:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[02bbadd1-557f-4630-a2ba-ac3583012ce8] succeeded in 0.003340600000228733s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:28:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[9fd7be65-c385-4da3-9371-bb00cc14c159] received
[2026-03-23 07:28:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[9fd7be65-c385-4da3-9371-bb00cc14c159] succeeded in 0.0032814000151120126s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:28:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[cbeb0a90-7c6e-4234-8aa6-c244fc98a760] received
[2026-03-23 07:28:33,797: INFO/MainProcess] Task tasks.scrape_pending_urls[cbeb0a90-7c6e-4234-8aa6-c244fc98a760] succeeded in 0.0031268999446183443s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:29:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[a7d15fd0-4981-40c9-b42c-9590507eae23] received
[2026-03-23 07:29:03,797: INFO/MainProcess] Task tasks.scrape_pending_urls[a7d15fd0-4981-40c9-b42c-9590507eae23] succeeded in 0.003180400002747774s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:29:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[2c3df00c-5580-49f6-984b-e33d05e076c3] received
[2026-03-23 07:29:33,797: INFO/MainProcess] Task tasks.scrape_pending_urls[2c3df00c-5580-49f6-984b-e33d05e076c3] succeeded in 0.002979899989441037s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:30:00,003: INFO/MainProcess] Task tasks.purge_old_debug_html[3a440f20-cd50-4175-8a26-368f7de6ca03] received
[2026-03-23 07:30:00,005: INFO/MainProcess] Task tasks.purge_old_debug_html[3a440f20-cd50-4175-8a26-368f7de6ca03] succeeded in 0.0018353000050410628s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 07:30:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[4f3b7b26-2a37-40d8-b543-501b7962be5c] received
[2026-03-23 07:30:03,797: INFO/MainProcess] Task tasks.scrape_pending_urls[4f3b7b26-2a37-40d8-b543-501b7962be5c] succeeded in 0.003072999999858439s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:30:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[e979e384-a2b6-4fb6-bc20-7e832f90508b] received
[2026-03-23 07:30:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[e979e384-a2b6-4fb6-bc20-7e832f90508b] succeeded in 0.0034214999759569764s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:31:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[2db6488e-574d-45e6-85e6-9f04f313f6fc] received
[2026-03-23 07:31:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[2db6488e-574d-45e6-85e6-9f04f313f6fc] succeeded in 0.003222699975594878s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:31:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[0fe80dda-edb9-42cd-85af-3599862fb5f6] received
[2026-03-23 07:31:34,008: INFO/MainProcess] Task tasks.collect_system_metrics[0fe80dda-edb9-42cd-85af-3599862fb5f6] succeeded in 0.517257800034713s: {'cpu': 13.8, 'memory': 41.2}
[2026-03-23 07:31:34,011: INFO/MainProcess] Task tasks.scrape_pending_urls[22367c5d-4cd4-4806-b3d8-9adc99dfe70e] received
[2026-03-23 07:31:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[22367c5d-4cd4-4806-b3d8-9adc99dfe70e] succeeded in 0.0035407000104896724s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:32:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[b656e382-00fd-4f90-9f2d-9ae2b94f46c0] received
[2026-03-23 07:32:03,797: INFO/MainProcess] Task tasks.scrape_pending_urls[b656e382-00fd-4f90-9f2d-9ae2b94f46c0] succeeded in 0.0031457000295631588s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:32:33,794: INFO/MainProcess] Task tasks.scrape_pending_urls[990811fb-d947-43e1-bba5-f21ee28ef971] received
[2026-03-23 07:32:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[990811fb-d947-43e1-bba5-f21ee28ef971] succeeded in 0.0031285000150091946s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:33:03,795: INFO/MainProcess] Task tasks.scrape_pending_urls[e6a7da28-ea7c-49a6-af8f-eeaae690b9f3] received
[2026-03-23 07:33:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[e6a7da28-ea7c-49a6-af8f-eeaae690b9f3] succeeded in 0.0032361000194214284s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:33:33,799: INFO/MainProcess] Task tasks.scrape_pending_urls[fc703882-2f57-42fa-a5eb-e857e7b71d4f] received
[2026-03-23 07:33:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[fc703882-2f57-42fa-a5eb-e857e7b71d4f] succeeded in 0.003380300011485815s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:34:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[01c4270b-c0c5-40fe-a3af-6ff5a9952b20] received
[2026-03-23 07:34:03,801: INFO/MainProcess] Task tasks.scrape_pending_urls[01c4270b-c0c5-40fe-a3af-6ff5a9952b20] succeeded in 0.003155499987769872s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:34:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[ca0bf452-2481-4aae-a20b-98062e59f58d] received
[2026-03-23 07:34:33,801: INFO/MainProcess] Task tasks.scrape_pending_urls[ca0bf452-2481-4aae-a20b-98062e59f58d] succeeded in 0.0030317999771796167s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:35:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[39541248-9584-4bac-beeb-edeea3530100] received
[2026-03-23 07:35:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[39541248-9584-4bac-beeb-edeea3530100] succeeded in 0.0032657000119797885s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:35:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[39eb3ccd-4a35-4419-8f3e-a1570caf6af0] received
[2026-03-23 07:35:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[39eb3ccd-4a35-4419-8f3e-a1570caf6af0] succeeded in 0.003316100046504289s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:36:03,799: INFO/MainProcess] Task tasks.scrape_pending_urls[e8e41bc8-f4c0-4f7d-b263-2ea19fdfca40] received
[2026-03-23 07:36:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[e8e41bc8-f4c0-4f7d-b263-2ea19fdfca40] succeeded in 0.0031789999920874834s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:36:33,474: INFO/MainProcess] Task tasks.reset_stale_processing_urls[7c68f917-cf69-4634-a96b-a3797f989263] received
[2026-03-23 07:36:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 07:36:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[7c68f917-cf69-4634-a96b-a3797f989263] succeeded in 0.003580200020223856s: {'reset': 0}
[2026-03-23 07:36:33,490: INFO/MainProcess] Task tasks.collect_system_metrics[c1191994-caa4-4df6-a99a-55be90f970e3] received
[2026-03-23 07:36:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[c1191994-caa4-4df6-a99a-55be90f970e3] succeeded in 0.516688100004103s: {'cpu': 13.5, 'memory': 41.2}
[2026-03-23 07:36:34,012: INFO/MainProcess] Task tasks.scrape_pending_urls[600d7f8f-6d6d-4dbc-9f3c-456c69df0860] received
[2026-03-23 07:36:34,019: INFO/MainProcess] Task tasks.scrape_pending_urls[600d7f8f-6d6d-4dbc-9f3c-456c69df0860] succeeded in 0.006692199967801571s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:37:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[f9568ca1-6d8b-480d-9b36-b39a7bd17172] received
[2026-03-23 07:37:03,801: INFO/MainProcess] Task tasks.scrape_pending_urls[f9568ca1-6d8b-480d-9b36-b39a7bd17172] succeeded in 0.002885500027332455s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:37:33,799: INFO/MainProcess] Task tasks.scrape_pending_urls[64fdf281-9456-4829-b8ee-889b8c699c52] received
[2026-03-23 07:37:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[64fdf281-9456-4829-b8ee-889b8c699c52] succeeded in 0.0031988000264391303s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:38:03,799: INFO/MainProcess] Task tasks.scrape_pending_urls[aa1c828e-ffbd-479f-b8b3-f8b01eed7456] received
[2026-03-23 07:38:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[aa1c828e-ffbd-479f-b8b3-f8b01eed7456] succeeded in 0.003366399963852018s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:38:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[fb7838f8-e216-409d-a5af-7e4fef51b5e4] received
[2026-03-23 07:38:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[fb7838f8-e216-409d-a5af-7e4fef51b5e4] succeeded in 0.002964799990877509s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:39:03,798: INFO/MainProcess] Task tasks.scrape_pending_urls[a3c49bc1-7c8e-4379-bd23-49be13c3151c] received
[2026-03-23 07:39:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[a3c49bc1-7c8e-4379-bd23-49be13c3151c] succeeded in 0.0030925999744795263s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:39:33,798: INFO/MainProcess] Task tasks.scrape_pending_urls[aa2d661a-9409-4d5e-951b-60bed1b0a201] received
[2026-03-23 07:39:33,801: INFO/MainProcess] Task tasks.scrape_pending_urls[aa2d661a-9409-4d5e-951b-60bed1b0a201] succeeded in 0.0030003999709151685s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:40:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[40ced580-e119-480a-9302-e521af07e1d3] received
[2026-03-23 07:40:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[40ced580-e119-480a-9302-e521af07e1d3] succeeded in 0.0036178999580442905s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:40:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[f071031a-0798-4ddc-8442-a1f719e09a45] received
[2026-03-23 07:40:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[f071031a-0798-4ddc-8442-a1f719e09a45] succeeded in 0.0035379999899305403s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:41:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[06d37161-1a6d-4690-ab2a-716277744cd0] received
[2026-03-23 07:41:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[06d37161-1a6d-4690-ab2a-716277744cd0] succeeded in 0.00344920001225546s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:41:33,491: INFO/MainProcess] Task tasks.collect_system_metrics[5ee6e415-f92c-45ec-a2a7-fbb62f0995d0] received
[2026-03-23 07:41:34,008: INFO/MainProcess] Task tasks.collect_system_metrics[5ee6e415-f92c-45ec-a2a7-fbb62f0995d0] succeeded in 0.5165815000073053s: {'cpu': 13.1, 'memory': 41.2}
[2026-03-23 07:41:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[f8eb0edd-a853-49e0-881c-fcd74447bf91] received
[2026-03-23 07:41:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[f8eb0edd-a853-49e0-881c-fcd74447bf91] succeeded in 0.0037573999725282192s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:42:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[a2a0c485-5b89-48dd-8e36-c58d11d041b6] received
[2026-03-23 07:42:03,805: INFO/MainProcess] Task tasks.scrape_pending_urls[a2a0c485-5b89-48dd-8e36-c58d11d041b6] succeeded in 0.003125699993688613s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:42:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[372d422c-5fef-4497-94f8-e752ab3bbab0] received
[2026-03-23 07:42:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[372d422c-5fef-4497-94f8-e752ab3bbab0] succeeded in 0.00334689998999238s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:43:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[3fd3bcae-18d4-4ab2-aebd-960259d61a0a] received
[2026-03-23 07:43:03,805: INFO/MainProcess] Task tasks.scrape_pending_urls[3fd3bcae-18d4-4ab2-aebd-960259d61a0a] succeeded in 0.0030128000071272254s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:43:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[9a697272-d401-4667-8575-ae736df41f32] received
[2026-03-23 07:43:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[9a697272-d401-4667-8575-ae736df41f32] succeeded in 0.0032396999886259437s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:44:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[c1afec48-72a6-4495-9a05-5f6b70655f29] received
[2026-03-23 07:44:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[c1afec48-72a6-4495-9a05-5f6b70655f29] succeeded in 0.003144900023471564s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:44:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[09463fe2-aaa0-4437-a519-56c3021ee81a] received
[2026-03-23 07:44:33,805: INFO/MainProcess] Task tasks.scrape_pending_urls[09463fe2-aaa0-4437-a519-56c3021ee81a] succeeded in 0.00299279997125268s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:45:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[1b1ada45-9647-45e7-90d3-f1344a8de886] received
[2026-03-23 07:45:03,805: INFO/MainProcess] Task tasks.scrape_pending_urls[1b1ada45-9647-45e7-90d3-f1344a8de886] succeeded in 0.002972799993585795s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:45:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[128c4cb0-ad3e-4b21-b547-727227818dfd] received
[2026-03-23 07:45:33,805: INFO/MainProcess] Task tasks.scrape_pending_urls[128c4cb0-ad3e-4b21-b547-727227818dfd] succeeded in 0.0031088999821804464s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:46:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[ace779f3-c5d6-4f22-9d1f-371ab12ec936] received
[2026-03-23 07:46:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[ace779f3-c5d6-4f22-9d1f-371ab12ec936] succeeded in 0.003353299980517477s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:46:33,494: INFO/MainProcess] Task tasks.collect_system_metrics[fcd1862b-13b6-4490-8bf0-cc088a731f92] received
[2026-03-23 07:46:34,011: INFO/MainProcess] Task tasks.collect_system_metrics[fcd1862b-13b6-4490-8bf0-cc088a731f92] succeeded in 0.5161602000007406s: {'cpu': 17.4, 'memory': 41.1}
[2026-03-23 07:46:34,013: INFO/MainProcess] Task tasks.scrape_pending_urls[b2dabe6d-d9f2-45a1-a681-4e0957ae8836] received
[2026-03-23 07:46:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[b2dabe6d-d9f2-45a1-a681-4e0957ae8836] succeeded in 0.0033504999591968954s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:47:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[47c96fe9-ce82-4ac6-bcc5-95e5d82b62ee] received
[2026-03-23 07:47:03,805: INFO/MainProcess] Task tasks.scrape_pending_urls[47c96fe9-ce82-4ac6-bcc5-95e5d82b62ee] succeeded in 0.0029055000049993396s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:47:33,803: INFO/MainProcess] Task tasks.scrape_pending_urls[4ebcb3fa-dff5-45cf-af43-3f4158450dec] received
[2026-03-23 07:47:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[4ebcb3fa-dff5-45cf-af43-3f4158450dec] succeeded in 0.003104300005361438s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:48:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[f98f9863-9f8f-4611-9efa-4435277a990c] received
[2026-03-23 07:48:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[f98f9863-9f8f-4611-9efa-4435277a990c] succeeded in 0.0030401999829337s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:48:33,802: INFO/MainProcess] Task tasks.scrape_pending_urls[c9265520-d5e0-4fb8-a3af-2fc5c057c3bd] received
[2026-03-23 07:48:33,805: INFO/MainProcess] Task tasks.scrape_pending_urls[c9265520-d5e0-4fb8-a3af-2fc5c057c3bd] succeeded in 0.0030768000287935138s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:49:03,803: INFO/MainProcess] Task tasks.scrape_pending_urls[67c69490-5ed1-41e6-83e9-1deb3a5f0e3b] received
[2026-03-23 07:49:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[67c69490-5ed1-41e6-83e9-1deb3a5f0e3b] succeeded in 0.003174400015268475s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:49:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[8327b222-3796-418a-9012-45054bb921a3] received
[2026-03-23 07:49:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[8327b222-3796-418a-9012-45054bb921a3] succeeded in 0.0030966000049374998s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:50:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[8cb89de4-9dbe-4505-92ec-bdef928d9aa9] received
[2026-03-23 07:50:03,809: INFO/MainProcess] Task tasks.scrape_pending_urls[8cb89de4-9dbe-4505-92ec-bdef928d9aa9] succeeded in 0.003132799989543855s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:50:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[291715ba-7ae2-424f-b87a-4c3cbadb5d8e] received
[2026-03-23 07:50:33,809: INFO/MainProcess] Task tasks.scrape_pending_urls[291715ba-7ae2-424f-b87a-4c3cbadb5d8e] succeeded in 0.0030799999949522316s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:51:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[5cf39311-6016-4476-8187-e25adfc7ec08] received
[2026-03-23 07:51:03,809: INFO/MainProcess] Task tasks.scrape_pending_urls[5cf39311-6016-4476-8187-e25adfc7ec08] succeeded in 0.0032039000070653856s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:51:33,494: INFO/MainProcess] Task tasks.collect_system_metrics[fd48fc4d-d330-462f-9eeb-91fceca7aa46] received
[2026-03-23 07:51:34,010: INFO/MainProcess] Task tasks.collect_system_metrics[fd48fc4d-d330-462f-9eeb-91fceca7aa46] succeeded in 0.5164332999847829s: {'cpu': 19.8, 'memory': 41.1}
[2026-03-23 07:51:34,013: INFO/MainProcess] Task tasks.scrape_pending_urls[5e9ac7d4-492b-4c08-ab0e-c8d052de2250] received
[2026-03-23 07:51:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[5e9ac7d4-492b-4c08-ab0e-c8d052de2250] succeeded in 0.0033715000026859343s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:52:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[a6fea1df-d78d-454c-985f-1d4548155b31] received
[2026-03-23 07:52:03,809: INFO/MainProcess] Task tasks.scrape_pending_urls[a6fea1df-d78d-454c-985f-1d4548155b31] succeeded in 0.0029578999965451658s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:52:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[a6b5e703-7380-4fd0-a5e4-fa541166890b] received
[2026-03-23 07:52:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[a6b5e703-7380-4fd0-a5e4-fa541166890b] succeeded in 0.0031837000278756022s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:53:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[68ec2277-abf1-4477-b380-5ddd79851859] received
[2026-03-23 07:53:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[68ec2277-abf1-4477-b380-5ddd79851859] succeeded in 0.003160299966111779s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:53:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[6c0321f2-bde2-45d8-90ae-e9d8353234d0] received
[2026-03-23 07:53:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[6c0321f2-bde2-45d8-90ae-e9d8353234d0] succeeded in 0.003433199948631227s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:54:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[b727a005-35c4-4a95-9292-6531e579d7de] received
[2026-03-23 07:54:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[b727a005-35c4-4a95-9292-6531e579d7de] succeeded in 0.00326399999903515s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:54:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[695215d5-eae8-4b91-99d6-6998a36587e4] received
[2026-03-23 07:54:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[695215d5-eae8-4b91-99d6-6998a36587e4] succeeded in 0.0032334999996237457s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:55:03,806: INFO/MainProcess] Task tasks.scrape_pending_urls[831218a0-30b9-42fd-86f1-45433d46146b] received
[2026-03-23 07:55:03,809: INFO/MainProcess] Task tasks.scrape_pending_urls[831218a0-30b9-42fd-86f1-45433d46146b] succeeded in 0.0030373000190593302s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:55:33,806: INFO/MainProcess] Task tasks.scrape_pending_urls[d79f1da1-c40e-47f3-a038-74156d152e97] received
[2026-03-23 07:55:33,809: INFO/MainProcess] Task tasks.scrape_pending_urls[d79f1da1-c40e-47f3-a038-74156d152e97] succeeded in 0.002985800034366548s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:56:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[a9d0787e-f8d7-4c92-9f5e-ca17159fb7a3] received
[2026-03-23 07:56:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[a9d0787e-f8d7-4c92-9f5e-ca17159fb7a3] succeeded in 0.002913000003900379s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:56:33,495: INFO/MainProcess] Task tasks.collect_system_metrics[1cacb95f-04c1-4706-bef5-a227e5526837] received
[2026-03-23 07:56:34,014: INFO/MainProcess] Task tasks.collect_system_metrics[1cacb95f-04c1-4706-bef5-a227e5526837] succeeded in 0.5183630000101402s: {'cpu': 15.4, 'memory': 41.3}
[2026-03-23 07:56:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[fbd8f168-9ed8-4ae1-acd8-c1faa23d7dc2] received
[2026-03-23 07:56:34,024: INFO/MainProcess] Task tasks.scrape_pending_urls[fbd8f168-9ed8-4ae1-acd8-c1faa23d7dc2] succeeded in 0.006759800016880035s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:57:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[d8abbf81-dfee-451a-b0c0-693a2be06c61] received
[2026-03-23 07:57:03,813: INFO/MainProcess] Task tasks.scrape_pending_urls[d8abbf81-dfee-451a-b0c0-693a2be06c61] succeeded in 0.002938400022685528s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:57:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[138e4f34-ef62-4e66-bad7-eaf491a233b8] received
[2026-03-23 07:57:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[138e4f34-ef62-4e66-bad7-eaf491a233b8] succeeded in 0.002979900047648698s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:58:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[ab1d1619-bc3f-494b-8d6d-05c5c0d069b2] received
[2026-03-23 07:58:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[ab1d1619-bc3f-494b-8d6d-05c5c0d069b2] succeeded in 0.003115300030913204s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:58:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[15236d63-1c1c-497d-b4b0-cb8b5a74590a] received
[2026-03-23 07:58:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[15236d63-1c1c-497d-b4b0-cb8b5a74590a] succeeded in 0.003107899974565953s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:59:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[dfb34ffb-7f4b-4fcb-abe3-d177f521d518] received
[2026-03-23 07:59:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[dfb34ffb-7f4b-4fcb-abe3-d177f521d518] succeeded in 0.0034514000290073454s: {'status': 'idle', 'pending': 0}
[2026-03-23 07:59:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[4469774c-63e5-4dd4-9551-6adadafb870c] received
[2026-03-23 07:59:33,813: INFO/MainProcess] Task tasks.scrape_pending_urls[4469774c-63e5-4dd4-9551-6adadafb870c] succeeded in 0.002964500046800822s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:00:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[803ce9da-2642-4860-947a-8fd646df33e0] received
[2026-03-23 08:00:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[803ce9da-2642-4860-947a-8fd646df33e0] succeeded in 0.00327590003143996s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:00:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[a59514f8-9421-46f6-b426-c0dc668d9a9f] received
[2026-03-23 08:00:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[a59514f8-9421-46f6-b426-c0dc668d9a9f] succeeded in 0.0034951000125147402s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:01:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[1ce30307-19bf-40d1-8972-008474d355c8] received
[2026-03-23 08:01:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[1ce30307-19bf-40d1-8972-008474d355c8] succeeded in 0.002887600043322891s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:01:33,495: INFO/MainProcess] Task tasks.collect_system_metrics[b83b6a53-9e42-485a-9656-09a208eda822] received
[2026-03-23 08:01:34,012: INFO/MainProcess] Task tasks.collect_system_metrics[b83b6a53-9e42-485a-9656-09a208eda822] succeeded in 0.5164743000059389s: {'cpu': 13.7, 'memory': 41.3}
[2026-03-23 08:01:34,014: INFO/MainProcess] Task tasks.scrape_pending_urls[0a0dd8f5-c96a-468b-9496-ecebcba9137b] received
[2026-03-23 08:01:34,018: INFO/MainProcess] Task tasks.scrape_pending_urls[0a0dd8f5-c96a-468b-9496-ecebcba9137b] succeeded in 0.003320000017993152s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:02:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[fa79409a-d6b6-46fb-91c4-a532722cbb68] received
[2026-03-23 08:02:03,822: INFO/MainProcess] Task tasks.scrape_pending_urls[fa79409a-d6b6-46fb-91c4-a532722cbb68] succeeded in 0.01033130002906546s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:02:33,811: INFO/MainProcess] Task tasks.scrape_pending_urls[e9d04ceb-3cc9-43c2-a118-7ca785a2a326] received
[2026-03-23 08:02:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[e9d04ceb-3cc9-43c2-a118-7ca785a2a326] succeeded in 0.0032470999867655337s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:03:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[56a18f2f-1702-4326-90be-7935015b104d] received
[2026-03-23 08:03:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[56a18f2f-1702-4326-90be-7935015b104d] succeeded in 0.0029704999760724604s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:03:33,810: INFO/MainProcess] Task tasks.scrape_pending_urls[3678bb03-d42e-47c6-8430-925115c35709] received
[2026-03-23 08:03:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[3678bb03-d42e-47c6-8430-925115c35709] succeeded in 0.0032112000044435263s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:04:03,810: INFO/MainProcess] Task tasks.scrape_pending_urls[f2555e37-bbea-40d9-8780-dacafe3810a1] received
[2026-03-23 08:04:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[f2555e37-bbea-40d9-8780-dacafe3810a1] succeeded in 0.0029005000251345336s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:04:33,811: INFO/MainProcess] Task tasks.scrape_pending_urls[c57c2d6b-fc8e-4fb5-a278-5ae031840a31] received
[2026-03-23 08:04:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[c57c2d6b-fc8e-4fb5-a278-5ae031840a31] succeeded in 0.0032260000007227063s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:05:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[b4daf16e-4fd0-418c-b28b-04cc722f73f8] received
[2026-03-23 08:05:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[b4daf16e-4fd0-418c-b28b-04cc722f73f8] succeeded in 0.003391600039321929s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:05:33,811: INFO/MainProcess] Task tasks.scrape_pending_urls[d40480d0-26bd-4d90-bd6a-4105cb9c2fc1] received
[2026-03-23 08:05:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[d40480d0-26bd-4d90-bd6a-4105cb9c2fc1] succeeded in 0.003093399980571121s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:06:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[1dd58be2-6a7b-4407-a6b5-d3f8b80b42b0] received
[2026-03-23 08:06:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[1dd58be2-6a7b-4407-a6b5-d3f8b80b42b0] succeeded in 0.00319279998075217s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:06:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[5e979f52-6650-4730-a4a4-f90d6725147f] received
[2026-03-23 08:06:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 08:06:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[5e979f52-6650-4730-a4a4-f90d6725147f] succeeded in 0.003856399969663471s: {'reset': 0}
[2026-03-23 08:06:33,494: INFO/MainProcess] Task tasks.collect_system_metrics[0e17d6c8-4f97-439f-ad57-a14237d93a72] received
[2026-03-23 08:06:34,012: INFO/MainProcess] Task tasks.collect_system_metrics[0e17d6c8-4f97-439f-ad57-a14237d93a72] succeeded in 0.5168436000240035s: {'cpu': 17.8, 'memory': 41.4}
[2026-03-23 08:06:34,014: INFO/MainProcess] Task tasks.scrape_pending_urls[281ae052-7aa1-4d57-8b99-ea256410ff12] received
[2026-03-23 08:06:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[281ae052-7aa1-4d57-8b99-ea256410ff12] succeeded in 0.0032114999485202134s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:07:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[de61f114-d290-4fdb-870e-01fe75163981] received
[2026-03-23 08:07:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[de61f114-d290-4fdb-870e-01fe75163981] succeeded in 0.0032110000029206276s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:07:33,811: INFO/MainProcess] Task tasks.scrape_pending_urls[37f8ae49-2017-4f7f-b8d2-853ede09aa6f] received
[2026-03-23 08:07:33,815: INFO/MainProcess] Task tasks.scrape_pending_urls[37f8ae49-2017-4f7f-b8d2-853ede09aa6f] succeeded in 0.0033715000026859343s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:08:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[fc249848-6500-4714-9bee-6eca27b8413a] received
[2026-03-23 08:08:03,814: INFO/MainProcess] Task tasks.scrape_pending_urls[fc249848-6500-4714-9bee-6eca27b8413a] succeeded in 0.003205200016964227s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:08:33,811: INFO/MainProcess] Task tasks.scrape_pending_urls[14b561e3-f073-4a84-bb69-5ed7762407b6] received
[2026-03-23 08:08:33,815: INFO/MainProcess] Task tasks.scrape_pending_urls[14b561e3-f073-4a84-bb69-5ed7762407b6] succeeded in 0.0032654000096954405s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:09:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[ba484514-36df-4219-bf40-e705cc10d238] received
[2026-03-23 08:09:03,818: INFO/MainProcess] Task tasks.scrape_pending_urls[ba484514-36df-4219-bf40-e705cc10d238] succeeded in 0.0029818000039085746s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:09:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[1e1e8650-cf01-4f54-996f-97bd8b35202d] received
[2026-03-23 08:09:33,818: INFO/MainProcess] Task tasks.scrape_pending_urls[1e1e8650-cf01-4f54-996f-97bd8b35202d] succeeded in 0.002976599964313209s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:10:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[fc91e335-b63f-4d57-bca5-2ec3b7a0bba7] received
[2026-03-23 08:10:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[fc91e335-b63f-4d57-bca5-2ec3b7a0bba7] succeeded in 0.0033735999604687095s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:10:33,814: INFO/MainProcess] Task tasks.scrape_pending_urls[0e9362ce-5526-4adf-8351-967929579dd2] received
[2026-03-23 08:10:33,818: INFO/MainProcess] Task tasks.scrape_pending_urls[0e9362ce-5526-4adf-8351-967929579dd2] succeeded in 0.0032145000295713544s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:11:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[7ee53cc8-d33b-4923-980c-8fb7e4a9e567] received
[2026-03-23 08:11:03,818: INFO/MainProcess] Task tasks.scrape_pending_urls[7ee53cc8-d33b-4923-980c-8fb7e4a9e567] succeeded in 0.0029421999934129417s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:11:33,494: INFO/MainProcess] Task tasks.collect_system_metrics[e4204b46-4093-452a-baba-ff58a58b6ab1] received
[2026-03-23 08:11:34,011: INFO/MainProcess] Task tasks.collect_system_metrics[e4204b46-4093-452a-baba-ff58a58b6ab1] succeeded in 0.5164656999986619s: {'cpu': 12.5, 'memory': 41.4}
[2026-03-23 08:11:34,013: INFO/MainProcess] Task tasks.scrape_pending_urls[9d574ee8-1ae2-4b4a-a13b-812a0f16dddf] received
[2026-03-23 08:11:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[9d574ee8-1ae2-4b4a-a13b-812a0f16dddf] succeeded in 0.0033260000054724514s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:12:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[a4e3ae9c-729a-421a-a03e-87879a6d8cd0] received
[2026-03-23 08:12:03,818: INFO/MainProcess] Task tasks.scrape_pending_urls[a4e3ae9c-729a-421a-a03e-87879a6d8cd0] succeeded in 0.003163500048685819s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:12:33,815: INFO/MainProcess] Task tasks.scrape_pending_urls[ebc05f48-0cab-4032-8f71-7bf2b229b2d1] received
[2026-03-23 08:12:33,884: INFO/MainProcess] Task tasks.scrape_pending_urls[ebc05f48-0cab-4032-8f71-7bf2b229b2d1] succeeded in 0.0690419000457041s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:13:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[1311737d-eb9e-4e1b-85c5-a382691021b0] received
[2026-03-23 08:13:03,818: INFO/MainProcess] Task tasks.scrape_pending_urls[1311737d-eb9e-4e1b-85c5-a382691021b0] succeeded in 0.0032448999700136483s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:13:33,815: INFO/MainProcess] Task tasks.scrape_pending_urls[5083c523-30b3-46a5-92e1-8b888f05c71f] received
[2026-03-23 08:13:33,885: INFO/MainProcess] Task tasks.scrape_pending_urls[5083c523-30b3-46a5-92e1-8b888f05c71f] succeeded in 0.07005119998939335s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:14:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[c6ece441-d50d-4be7-8215-88d2c7c28fbd] received
[2026-03-23 08:14:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[c6ece441-d50d-4be7-8215-88d2c7c28fbd] succeeded in 0.0033917000400833786s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:14:33,815: INFO/MainProcess] Task tasks.scrape_pending_urls[b5d6649d-ba9f-4399-a5c7-acc695ec382f] received
[2026-03-23 08:14:33,818: INFO/MainProcess] Task tasks.scrape_pending_urls[b5d6649d-ba9f-4399-a5c7-acc695ec382f] succeeded in 0.003039000032003969s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:15:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[9cc2b205-7f89-4f60-9ecc-84d312eafb94] received
[2026-03-23 08:15:03,818: INFO/MainProcess] Task tasks.scrape_pending_urls[9cc2b205-7f89-4f60-9ecc-84d312eafb94] succeeded in 0.0032159999827854335s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:15:33,819: INFO/MainProcess] Task tasks.scrape_pending_urls[6ecdd36f-8bee-41b6-b057-7f09f915aa6c] received
[2026-03-23 08:15:33,823: INFO/MainProcess] Task tasks.scrape_pending_urls[6ecdd36f-8bee-41b6-b057-7f09f915aa6c] succeeded in 0.003359000023920089s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:16:03,818: INFO/MainProcess] Task tasks.scrape_pending_urls[24bef48c-35aa-44e7-ac0b-c987d1e12145] received
[2026-03-23 08:16:03,822: INFO/MainProcess] Task tasks.scrape_pending_urls[24bef48c-35aa-44e7-ac0b-c987d1e12145] succeeded in 0.003335000015795231s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:16:33,494: INFO/MainProcess] Task tasks.collect_system_metrics[ffed20c1-1734-4a7d-be37-bc3902233e3e] received
[2026-03-23 08:16:34,014: INFO/MainProcess] Task tasks.collect_system_metrics[ffed20c1-1734-4a7d-be37-bc3902233e3e] succeeded in 0.5189781000372022s: {'cpu': 14.1, 'memory': 41.3}
[2026-03-23 08:16:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[3e3bbb31-c1dd-48e2-8691-9bca95ccbb58] received
[2026-03-23 08:16:34,020: INFO/MainProcess] Task tasks.scrape_pending_urls[3e3bbb31-c1dd-48e2-8691-9bca95ccbb58] succeeded in 0.0035151999909430742s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:17:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[605e9dbb-5740-4d3d-abc5-07b96a202971] received
[2026-03-23 08:17:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[605e9dbb-5740-4d3d-abc5-07b96a202971] succeeded in 0.003440600004978478s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:17:33,818: INFO/MainProcess] Task tasks.scrape_pending_urls[c072c722-49b0-46e5-9d66-0ce4c1a1697f] received
[2026-03-23 08:17:33,822: INFO/MainProcess] Task tasks.scrape_pending_urls[c072c722-49b0-46e5-9d66-0ce4c1a1697f] succeeded in 0.003270599991083145s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:18:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[722cb368-61cf-4d08-8e6c-e7fe81655379] received
[2026-03-23 08:18:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[722cb368-61cf-4d08-8e6c-e7fe81655379] succeeded in 0.0036628999514505267s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:18:33,818: INFO/MainProcess] Task tasks.scrape_pending_urls[3b69107f-145f-4164-a83a-0fafc826b8bc] received
[2026-03-23 08:18:33,822: INFO/MainProcess] Task tasks.scrape_pending_urls[3b69107f-145f-4164-a83a-0fafc826b8bc] succeeded in 0.0031775999814271927s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:19:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[36c39c64-f9e9-417a-9296-3869dfd514a1] received
[2026-03-23 08:19:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[36c39c64-f9e9-417a-9296-3869dfd514a1] succeeded in 0.0035033999592997134s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:19:33,818: INFO/MainProcess] Task tasks.scrape_pending_urls[0af77efa-af1d-4653-9b95-574f531abba4] received
[2026-03-23 08:19:33,822: INFO/MainProcess] Task tasks.scrape_pending_urls[0af77efa-af1d-4653-9b95-574f531abba4] succeeded in 0.003584399993997067s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:20:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[2abd1ad4-b308-4de0-9ba6-b83ba117735f] received
[2026-03-23 08:20:03,907: INFO/MainProcess] Task tasks.scrape_pending_urls[2abd1ad4-b308-4de0-9ba6-b83ba117735f] succeeded in 0.08776599995326251s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:20:33,819: INFO/MainProcess] Task tasks.scrape_pending_urls[08367e82-92bb-4478-942d-8bb97faccf01] received
[2026-03-23 08:20:33,823: INFO/MainProcess] Task tasks.scrape_pending_urls[08367e82-92bb-4478-942d-8bb97faccf01] succeeded in 0.0033232999849133193s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:21:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[0e2602db-0ac9-48ff-aeb0-7fb263da6fa8] received
[2026-03-23 08:21:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[0e2602db-0ac9-48ff-aeb0-7fb263da6fa8] succeeded in 0.0036512999795377254s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:21:33,494: INFO/MainProcess] Task tasks.collect_system_metrics[d60ff8c8-f0fd-46f3-bb1a-3d7d60700455] received
[2026-03-23 08:21:34,013: INFO/MainProcess] Task tasks.collect_system_metrics[d60ff8c8-f0fd-46f3-bb1a-3d7d60700455] succeeded in 0.5186478000250645s: {'cpu': 14.7, 'memory': 41.2}
[2026-03-23 08:21:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[91a704a7-8b64-4ff2-875e-c32eaf701cf6] received
[2026-03-23 08:21:34,019: INFO/MainProcess] Task tasks.scrape_pending_urls[91a704a7-8b64-4ff2-875e-c32eaf701cf6] succeeded in 0.0034561000065878034s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:22:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[d9bdbfc6-c782-42a9-bd53-3fa3c19ab2e2] received
[2026-03-23 08:22:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[d9bdbfc6-c782-42a9-bd53-3fa3c19ab2e2] succeeded in 0.0030672000139020383s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:22:33,823: INFO/MainProcess] Task tasks.scrape_pending_urls[2af8a66e-f61e-44dd-b9ef-c644ddad7eb6] received
[2026-03-23 08:22:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[2af8a66e-f61e-44dd-b9ef-c644ddad7eb6] succeeded in 0.0032475999905727804s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:23:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[8a61d14c-824f-4efd-8587-45f46549fa11] received
[2026-03-23 08:23:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[8a61d14c-824f-4efd-8587-45f46549fa11] succeeded in 0.0033296000328846276s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:23:33,823: INFO/MainProcess] Task tasks.scrape_pending_urls[356311a6-8e06-4968-bd56-ff81a2dd85ad] received
[2026-03-23 08:23:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[356311a6-8e06-4968-bd56-ff81a2dd85ad] succeeded in 0.0033239999902434647s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:24:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[ce19aaec-ffe5-4c50-85cf-c17aa05dccbf] received
[2026-03-23 08:24:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[ce19aaec-ffe5-4c50-85cf-c17aa05dccbf] succeeded in 0.003525800013449043s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:24:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[8bfaedd1-7499-49b7-b66c-71e63538fdf4] received
[2026-03-23 08:24:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[8bfaedd1-7499-49b7-b66c-71e63538fdf4] succeeded in 0.0035157999955117702s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:25:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[65a26199-ba02-48c2-ab65-be7afff738c2] received
[2026-03-23 08:25:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[65a26199-ba02-48c2-ab65-be7afff738c2] succeeded in 0.0031276000081561506s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:25:33,823: INFO/MainProcess] Task tasks.scrape_pending_urls[97aa3477-a751-4647-a7b4-edad08034371] received
[2026-03-23 08:25:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[97aa3477-a751-4647-a7b4-edad08034371] succeeded in 0.00348469999153167s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:26:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[23c37c58-7a51-4e2b-8b33-138ace1e5b2b] received
[2026-03-23 08:26:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[23c37c58-7a51-4e2b-8b33-138ace1e5b2b] succeeded in 0.0031181000522337854s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:26:33,495: INFO/MainProcess] Task tasks.collect_system_metrics[d9706ac0-982a-4492-bd35-a8ff48f086b4] received
[2026-03-23 08:26:34,013: INFO/MainProcess] Task tasks.collect_system_metrics[d9706ac0-982a-4492-bd35-a8ff48f086b4] succeeded in 0.5180684999795631s: {'cpu': 18.0, 'memory': 41.4}
[2026-03-23 08:26:34,015: INFO/MainProcess] Task tasks.scrape_pending_urls[e35bf868-451b-4d65-b4eb-23a7f7d56217] received
[2026-03-23 08:26:34,018: INFO/MainProcess] Task tasks.scrape_pending_urls[e35bf868-451b-4d65-b4eb-23a7f7d56217] succeeded in 0.003352800034917891s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:27:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[9a1f1fbb-95dc-45cf-9d98-f082c7cb392d] received
[2026-03-23 08:27:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[9a1f1fbb-95dc-45cf-9d98-f082c7cb392d] succeeded in 0.00317949999589473s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:27:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[395b8873-36c5-4aa5-b53c-d970f07b1ee0] received
[2026-03-23 08:27:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[395b8873-36c5-4aa5-b53c-d970f07b1ee0] succeeded in 0.003161399974487722s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:28:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[ac71c200-47c1-4c03-bbce-92833319e02e] received
[2026-03-23 08:28:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[ac71c200-47c1-4c03-bbce-92833319e02e] succeeded in 0.003085500036831945s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:28:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[cd38d2b1-ed35-4c55-b950-79ecb88b5fff] received
[2026-03-23 08:28:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[cd38d2b1-ed35-4c55-b950-79ecb88b5fff] succeeded in 0.003252000024076551s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:29:03,824: INFO/MainProcess] Task tasks.scrape_pending_urls[c0921d73-bf53-4f82-a698-b5e008a4ce1c] received
[2026-03-23 08:29:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[c0921d73-bf53-4f82-a698-b5e008a4ce1c] succeeded in 0.0032061999663710594s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:29:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[c5a889a1-3f0a-4801-a9f4-2c286722ed10] received
[2026-03-23 08:29:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[c5a889a1-3f0a-4801-a9f4-2c286722ed10] succeeded in 0.0031510000117123127s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[7d2450db-e897-43f4-96a7-0dfc0fafe4f8] received
[2026-03-23 08:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[7d2450db-e897-43f4-96a7-0dfc0fafe4f8] succeeded in 0.0017160000279545784s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-23 08:30:03,823: INFO/MainProcess] Task tasks.scrape_pending_urls[d160fc15-365c-4951-9eea-6fbbcb74b13a] received
[2026-03-23 08:30:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[d160fc15-365c-4951-9eea-6fbbcb74b13a] succeeded in 0.003201400046236813s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:30:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[c7e066b6-f309-4d36-a0ec-87f906967b4b] received
[2026-03-23 08:30:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[c7e066b6-f309-4d36-a0ec-87f906967b4b] succeeded in 0.003418200009036809s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:31:03,824: INFO/MainProcess] Task tasks.scrape_pending_urls[8215fed3-9065-4473-8411-fe86ccf816b4] received
[2026-03-23 08:31:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[8215fed3-9065-4473-8411-fe86ccf816b4] succeeded in 0.003467500035185367s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:31:33,495: INFO/MainProcess] Task tasks.collect_system_metrics[b0952e00-27a8-4757-9214-c9510dfd3dbd] received
[2026-03-23 08:31:34,007: INFO/MainProcess] Task tasks.collect_system_metrics[b0952e00-27a8-4757-9214-c9510dfd3dbd] succeeded in 0.511359199997969s: {'cpu': 15.2, 'memory': 41.2}
[2026-03-23 08:31:34,009: INFO/MainProcess] Task tasks.scrape_pending_urls[4f9ff35a-c87f-42bc-9c58-8dea3992baa3] received
[2026-03-23 08:31:34,013: INFO/MainProcess] Task tasks.scrape_pending_urls[4f9ff35a-c87f-42bc-9c58-8dea3992baa3] succeeded in 0.003386199998203665s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:32:03,824: INFO/MainProcess] Task tasks.scrape_pending_urls[af4335b4-e67b-432b-8cac-3e00bb56faa1] received
[2026-03-23 08:32:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[af4335b4-e67b-432b-8cac-3e00bb56faa1] succeeded in 0.003513399977236986s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:32:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[934b6be2-cacb-4d4a-b99f-447d4b15fdb1] received
[2026-03-23 08:32:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[934b6be2-cacb-4d4a-b99f-447d4b15fdb1] succeeded in 0.003002400044351816s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:33:03,824: INFO/MainProcess] Task tasks.scrape_pending_urls[e4b4d22a-e2be-426c-b0f5-0191ff743e28] received
[2026-03-23 08:33:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[e4b4d22a-e2be-426c-b0f5-0191ff743e28] succeeded in 0.002968300017528236s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:33:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[5e11d7eb-e4b4-4901-a59e-2b91b513ee10] received
[2026-03-23 08:33:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[5e11d7eb-e4b4-4901-a59e-2b91b513ee10] succeeded in 0.003526399959810078s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:34:03,824: INFO/MainProcess] Task tasks.scrape_pending_urls[1e0fddc8-3bd2-4c89-ac8d-ace786b4ee1c] received
[2026-03-23 08:34:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[1e0fddc8-3bd2-4c89-ac8d-ace786b4ee1c] succeeded in 0.0032326000509783626s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:34:33,824: INFO/MainProcess] Task tasks.scrape_pending_urls[84e13770-d9a7-49de-a77c-61cb6e85fda0] received
[2026-03-23 08:34:33,827: INFO/MainProcess] Task tasks.scrape_pending_urls[84e13770-d9a7-49de-a77c-61cb6e85fda0] succeeded in 0.0029562999843619764s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:35:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[7fd78f3a-b84a-41d0-97f4-7166b6393dbb] received
[2026-03-23 08:35:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[7fd78f3a-b84a-41d0-97f4-7166b6393dbb] succeeded in 0.003362499992363155s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:35:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[cd4e0428-65db-43c7-8fe2-e33428ff7eac] received
[2026-03-23 08:35:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[cd4e0428-65db-43c7-8fe2-e33428ff7eac] succeeded in 0.0031999999773688614s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:36:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[0d7b4254-9114-4168-a693-ed54bf790a02] received
[2026-03-23 08:36:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[0d7b4254-9114-4168-a693-ed54bf790a02] succeeded in 0.0032685999758541584s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:36:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[494fa48c-12fa-4695-94eb-3f68f5ec5593] received
[2026-03-23 08:36:33,476: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 08:36:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[494fa48c-12fa-4695-94eb-3f68f5ec5593] succeeded in 0.004072000039741397s: {'reset': 0}
[2026-03-23 08:36:33,495: INFO/MainProcess] Task tasks.collect_system_metrics[bd4dfbab-b682-45bb-90b8-58446b9f091e] received
[2026-03-23 08:36:34,002: INFO/MainProcess] Task tasks.collect_system_metrics[bd4dfbab-b682-45bb-90b8-58446b9f091e] succeeded in 0.5062112999730743s: {'cpu': 16.8, 'memory': 41.2}
[2026-03-23 08:36:34,004: INFO/MainProcess] Task tasks.scrape_pending_urls[445afb37-b09b-49c4-a506-34201a996bdb] received
[2026-03-23 08:36:34,007: INFO/MainProcess] Task tasks.scrape_pending_urls[445afb37-b09b-49c4-a506-34201a996bdb] succeeded in 0.0031718999962322414s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:37:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[6a454eb7-9e1b-4aec-bc49-45ee858bd904] received
[2026-03-23 08:37:03,831: INFO/MainProcess] Task tasks.scrape_pending_urls[6a454eb7-9e1b-4aec-bc49-45ee858bd904] succeeded in 0.003052300016861409s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:37:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[e67067a2-df3f-42ed-b0d9-456ff87971f9] received
[2026-03-23 08:37:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[e67067a2-df3f-42ed-b0d9-456ff87971f9] succeeded in 0.0031795999966561794s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:38:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[73506480-1595-4fb4-9f41-6f12d6422ae3] received
[2026-03-23 08:38:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[73506480-1595-4fb4-9f41-6f12d6422ae3] succeeded in 0.0032137000234797597s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:38:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[f621a41a-5c5a-449a-9f57-9f2aec74c829] received
[2026-03-23 08:38:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[f621a41a-5c5a-449a-9f57-9f2aec74c829] succeeded in 0.0030308000277727842s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:39:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[56abe04a-386d-442d-9bda-f3360491df54] received
[2026-03-23 08:39:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[56abe04a-386d-442d-9bda-f3360491df54] succeeded in 0.003238600038457662s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:39:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[e5c8f4b2-5a2d-4b5b-a060-ef516171f011] received
[2026-03-23 08:39:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[e5c8f4b2-5a2d-4b5b-a060-ef516171f011] succeeded in 0.002982200006954372s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:40:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[a50c4184-1857-41bb-8b55-6f85e06b5c2b] received
[2026-03-23 08:40:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[a50c4184-1857-41bb-8b55-6f85e06b5c2b] succeeded in 0.0032241999870166183s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:40:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[c41998a9-853f-4efe-bcd0-32be57735099] received
[2026-03-23 08:40:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[c41998a9-853f-4efe-bcd0-32be57735099] succeeded in 0.003111700003501028s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:41:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[9352d4e6-5bab-40d7-912a-6d01bcbcf7ff] received
[2026-03-23 08:41:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[9352d4e6-5bab-40d7-912a-6d01bcbcf7ff] succeeded in 0.003282699966803193s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:41:33,497: INFO/MainProcess] Task tasks.collect_system_metrics[b1b075fa-3fea-4bd2-9b47-b49bf853a37e] received
[2026-03-23 08:41:34,014: INFO/MainProcess] Task tasks.collect_system_metrics[b1b075fa-3fea-4bd2-9b47-b49bf853a37e] succeeded in 0.5163004999631085s: {'cpu': 12.4, 'memory': 41.2}
[2026-03-23 08:41:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[449eb23b-5363-4354-9d8c-3f93bcf29368] received
[2026-03-23 08:41:34,023: INFO/MainProcess] Task tasks.scrape_pending_urls[449eb23b-5363-4354-9d8c-3f93bcf29368] succeeded in 0.006504999997559935s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:42:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[7a461c61-bc11-4e6b-be00-bc638ee1a484] received
[2026-03-23 08:42:03,831: INFO/MainProcess] Task tasks.scrape_pending_urls[7a461c61-bc11-4e6b-be00-bc638ee1a484] succeeded in 0.0029939000378362834s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:42:33,828: INFO/MainProcess] Task tasks.scrape_pending_urls[1c79e3be-fc90-4086-960e-2c8e751bae14] received
[2026-03-23 08:42:33,831: INFO/MainProcess] Task tasks.scrape_pending_urls[1c79e3be-fc90-4086-960e-2c8e751bae14] succeeded in 0.0031479999888688326s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:43:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[a5716f44-34bc-43cc-bcf6-7e087ad1531b] received
[2026-03-23 08:43:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[a5716f44-34bc-43cc-bcf6-7e087ad1531b] succeeded in 0.0033434999641031027s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:43:33,829: INFO/MainProcess] Task tasks.scrape_pending_urls[84afb5d2-abcf-4a11-8ac9-23f40e11d336] received
[2026-03-23 08:43:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[84afb5d2-abcf-4a11-8ac9-23f40e11d336] succeeded in 0.0033094999962486327s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:44:03,828: INFO/MainProcess] Task tasks.scrape_pending_urls[d5a98edf-b511-4622-a08f-a09dfd550382] received
[2026-03-23 08:44:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[d5a98edf-b511-4622-a08f-a09dfd550382] succeeded in 0.0030915000243112445s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:44:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[d71dc69c-9a2c-4e3b-807e-bfc47b2f419f] received
[2026-03-23 08:44:33,835: INFO/MainProcess] Task tasks.scrape_pending_urls[d71dc69c-9a2c-4e3b-807e-bfc47b2f419f] succeeded in 0.003176500031258911s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:45:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[d2f53ce5-3d4a-4f50-904e-0460c7d98e9c] received
[2026-03-23 08:45:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[d2f53ce5-3d4a-4f50-904e-0460c7d98e9c] succeeded in 0.0032599999685771763s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:45:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[a319f5af-31fd-4ae7-a846-7559d9528eef] received
[2026-03-23 08:45:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[a319f5af-31fd-4ae7-a846-7559d9528eef] succeeded in 0.0033322999952360988s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:46:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[a6ec25bb-4620-4677-8091-514620a54934] received
[2026-03-23 08:46:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[a6ec25bb-4620-4677-8091-514620a54934] succeeded in 0.003171200049109757s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:46:33,497: INFO/MainProcess] Task tasks.collect_system_metrics[97bca1bc-c5a1-4a0f-994d-0258c6cebcab] received
[2026-03-23 08:46:34,015: INFO/MainProcess] Task tasks.collect_system_metrics[97bca1bc-c5a1-4a0f-994d-0258c6cebcab] succeeded in 0.5169064999790862s: {'cpu': 13.2, 'memory': 41.6}
[2026-03-23 08:46:34,020: INFO/MainProcess] Task tasks.scrape_pending_urls[099335f9-2500-4f1a-a4d7-16f0a7390b25] received
[2026-03-23 08:46:34,024: INFO/MainProcess] Task tasks.scrape_pending_urls[099335f9-2500-4f1a-a4d7-16f0a7390b25] succeeded in 0.003147499985061586s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:47:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[454d1c00-51a3-4e57-a6d9-e56e7415e59b] received
[2026-03-23 08:47:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[454d1c00-51a3-4e57-a6d9-e56e7415e59b] succeeded in 0.0032035000040195882s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:47:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[77f3a391-28bc-4f81-9f7e-750633a58d58] received
[2026-03-23 08:47:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[77f3a391-28bc-4f81-9f7e-750633a58d58] succeeded in 0.0037422000314109027s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:48:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[98601902-2bb4-4616-9548-bd2db16d568e] received
[2026-03-23 08:48:03,835: INFO/MainProcess] Task tasks.scrape_pending_urls[98601902-2bb4-4616-9548-bd2db16d568e] succeeded in 0.003123000031337142s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:48:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[66e3fc55-e92c-4991-9d0b-283f5a1ba4e2] received
[2026-03-23 08:48:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[66e3fc55-e92c-4991-9d0b-283f5a1ba4e2] succeeded in 0.0030937999836169183s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:49:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[526da6af-3d80-4e59-9749-40f9e3da4cdc] received
[2026-03-23 08:49:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[526da6af-3d80-4e59-9749-40f9e3da4cdc] succeeded in 0.003243100014515221s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:49:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[10fe7d47-2ce3-4153-b287-0eb9debca540] received
[2026-03-23 08:49:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[10fe7d47-2ce3-4153-b287-0eb9debca540] succeeded in 0.003155199985485524s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:50:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[cbf9a5da-2cc4-4ae4-9b43-ae7530ef8d1a] received
[2026-03-23 08:50:03,835: INFO/MainProcess] Task tasks.scrape_pending_urls[cbf9a5da-2cc4-4ae4-9b43-ae7530ef8d1a] succeeded in 0.003212299954611808s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:50:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[6b11caea-aba4-42dd-b98a-0ca8eba83df8] received
[2026-03-23 08:50:33,835: INFO/MainProcess] Task tasks.scrape_pending_urls[6b11caea-aba4-42dd-b98a-0ca8eba83df8] succeeded in 0.0030512000084854662s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:51:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[e0641f94-b579-494b-a150-1222322ac86f] received
[2026-03-23 08:51:03,835: INFO/MainProcess] Task tasks.scrape_pending_urls[e0641f94-b579-494b-a150-1222322ac86f] succeeded in 0.003014400019310415s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:51:33,497: INFO/MainProcess] Task tasks.collect_system_metrics[b1877b4b-b513-4146-947e-086186cb1f00] received
[2026-03-23 08:51:34,014: INFO/MainProcess] Task tasks.collect_system_metrics[b1877b4b-b513-4146-947e-086186cb1f00] succeeded in 0.5165240000351332s: {'cpu': 15.6, 'memory': 41.3}
[2026-03-23 08:51:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[195488c6-9188-4c91-bf04-d8cdc766dcfe] received
[2026-03-23 08:51:34,020: INFO/MainProcess] Task tasks.scrape_pending_urls[195488c6-9188-4c91-bf04-d8cdc766dcfe] succeeded in 0.003339799994137138s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:52:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[7ab185f5-49e6-4607-8090-e474849fa18b] received
[2026-03-23 08:52:03,835: INFO/MainProcess] Task tasks.scrape_pending_urls[7ab185f5-49e6-4607-8090-e474849fa18b] succeeded in 0.003136899962555617s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:52:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[17fa6086-e549-453f-b9ed-1391dcf1ccd1] received
[2026-03-23 08:52:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[17fa6086-e549-453f-b9ed-1391dcf1ccd1] succeeded in 0.003278499993029982s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:53:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[3de6e4f6-9199-4a3a-8a6c-fc7a91294645] received
[2026-03-23 08:53:03,835: INFO/MainProcess] Task tasks.scrape_pending_urls[3de6e4f6-9199-4a3a-8a6c-fc7a91294645] succeeded in 0.0031142000225372612s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:53:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[4dfe24dd-705f-469c-bdca-14c95e7d9776] received
[2026-03-23 08:53:33,835: INFO/MainProcess] Task tasks.scrape_pending_urls[4dfe24dd-705f-469c-bdca-14c95e7d9776] succeeded in 0.003183000022545457s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:54:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[00e89156-8858-45bc-8d3e-1668862ad6d2] received
[2026-03-23 08:54:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[00e89156-8858-45bc-8d3e-1668862ad6d2] succeeded in 0.003002100042067468s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:54:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[3031c52b-1889-4c09-ba67-22a3e1c7e896] received
[2026-03-23 08:54:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[3031c52b-1889-4c09-ba67-22a3e1c7e896] succeeded in 0.0039017999661155045s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:55:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[0b773ca7-af1f-42c0-8642-01d5e145a898] received
[2026-03-23 08:55:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[0b773ca7-af1f-42c0-8642-01d5e145a898] succeeded in 0.0034139000345021486s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:55:33,832: INFO/MainProcess] Task tasks.scrape_pending_urls[e7e6fe79-f1f2-4619-b121-4c98b6a0ccdd] received
[2026-03-23 08:55:33,836: INFO/MainProcess] Task tasks.scrape_pending_urls[e7e6fe79-f1f2-4619-b121-4c98b6a0ccdd] succeeded in 0.0031272000051103532s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:56:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[23e9d1cb-bfe4-4842-ac43-f9e448a42b58] received
[2026-03-23 08:56:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[23e9d1cb-bfe4-4842-ac43-f9e448a42b58] succeeded in 0.003167300019413233s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:56:33,498: INFO/MainProcess] Task tasks.collect_system_metrics[6edb0581-db68-424b-9a78-6ddefe09dce2] received
[2026-03-23 08:56:34,015: INFO/MainProcess] Task tasks.collect_system_metrics[6edb0581-db68-424b-9a78-6ddefe09dce2] succeeded in 0.5164436000050046s: {'cpu': 13.3, 'memory': 41.3}
[2026-03-23 08:56:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[94256145-c14a-4950-a6cb-e44c2303027c] received
[2026-03-23 08:56:34,020: INFO/MainProcess] Task tasks.scrape_pending_urls[94256145-c14a-4950-a6cb-e44c2303027c] succeeded in 0.003346299985423684s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:57:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[f3e086df-4f5c-40a4-b731-c2c4cd08ca7b] received
[2026-03-23 08:57:03,836: INFO/MainProcess] Task tasks.scrape_pending_urls[f3e086df-4f5c-40a4-b731-c2c4cd08ca7b] succeeded in 0.0035103000118397176s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:57:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[c10babaa-1a7c-4271-8dce-d3d2d799102b] received
[2026-03-23 08:57:33,840: INFO/MainProcess] Task tasks.scrape_pending_urls[c10babaa-1a7c-4271-8dce-d3d2d799102b] succeeded in 0.0031014999840408564s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:58:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[8559fa62-33e7-47e8-bdd2-7e0af64fd794] received
[2026-03-23 08:58:03,840: INFO/MainProcess] Task tasks.scrape_pending_urls[8559fa62-33e7-47e8-bdd2-7e0af64fd794] succeeded in 0.0031093000434339046s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:58:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[5e208afb-1b64-411e-aa7f-d4e8dc6e2d49] received
[2026-03-23 08:58:33,841: INFO/MainProcess] Task tasks.scrape_pending_urls[5e208afb-1b64-411e-aa7f-d4e8dc6e2d49] succeeded in 0.003536099975463003s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:59:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[e49f5cff-2337-47dc-a2e7-d2d74b0de1f6] received
[2026-03-23 08:59:03,841: INFO/MainProcess] Task tasks.scrape_pending_urls[e49f5cff-2337-47dc-a2e7-d2d74b0de1f6] succeeded in 0.003221500024665147s: {'status': 'idle', 'pending': 0}
[2026-03-23 08:59:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[b0569e42-550a-469e-b9b4-034386996559] received
[2026-03-23 08:59:33,841: INFO/MainProcess] Task tasks.scrape_pending_urls[b0569e42-550a-469e-b9b4-034386996559] succeeded in 0.0032478999928571284s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:00:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[d5235df2-da3f-409d-91df-8c21c6f4154a] received
[2026-03-23 09:00:03,841: INFO/MainProcess] Task tasks.scrape_pending_urls[d5235df2-da3f-409d-91df-8c21c6f4154a] succeeded in 0.0033009999897331s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:00:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[93944123-d17e-441e-a28b-e9796bcdf42e] received
[2026-03-23 09:00:33,840: INFO/MainProcess] Task tasks.scrape_pending_urls[93944123-d17e-441e-a28b-e9796bcdf42e] succeeded in 0.003147799987345934s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:01:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[909a159e-85ca-43fa-af9b-5e8037f65f72] received
[2026-03-23 09:01:03,840: INFO/MainProcess] Task tasks.scrape_pending_urls[909a159e-85ca-43fa-af9b-5e8037f65f72] succeeded in 0.0031155000324361026s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:01:33,497: INFO/MainProcess] Task tasks.collect_system_metrics[72f05c47-e1ed-44ae-a811-b61cf15f19bf] received
[2026-03-23 09:01:34,014: INFO/MainProcess] Task tasks.collect_system_metrics[72f05c47-e1ed-44ae-a811-b61cf15f19bf] succeeded in 0.5168543999898247s: {'cpu': 12.5, 'memory': 41.5}
[2026-03-23 09:01:34,017: INFO/MainProcess] Task tasks.scrape_pending_urls[c4825b1e-b467-4b2a-9da9-dddc04ee953f] received
[2026-03-23 09:01:34,020: INFO/MainProcess] Task tasks.scrape_pending_urls[c4825b1e-b467-4b2a-9da9-dddc04ee953f] succeeded in 0.0033438000245951116s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:02:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[cff0f8b8-73f2-4349-b2cd-d91cb0250239] received
[2026-03-23 09:02:03,841: INFO/MainProcess] Task tasks.scrape_pending_urls[cff0f8b8-73f2-4349-b2cd-d91cb0250239] succeeded in 0.003232099988963455s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:02:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[c4917a56-4a27-4e1b-af34-f4f8064762f4] received
[2026-03-23 09:02:33,841: INFO/MainProcess] Task tasks.scrape_pending_urls[c4917a56-4a27-4e1b-af34-f4f8064762f4] succeeded in 0.0030322999809868634s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:03:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[d3a18507-c213-4a25-bc5e-8cf92f869ea6] received
[2026-03-23 09:03:03,841: INFO/MainProcess] Task tasks.scrape_pending_urls[d3a18507-c213-4a25-bc5e-8cf92f869ea6] succeeded in 0.003694099956192076s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:03:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[2ae3139a-50ef-43e0-bf7e-eb36e67b1343] received
[2026-03-23 09:03:33,841: INFO/MainProcess] Task tasks.scrape_pending_urls[2ae3139a-50ef-43e0-bf7e-eb36e67b1343] succeeded in 0.0031467999797314405s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:04:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[ce94810e-ba67-495a-9caf-ef7e615fecaa] received
[2026-03-23 09:04:03,840: INFO/MainProcess] Task tasks.scrape_pending_urls[ce94810e-ba67-495a-9caf-ef7e615fecaa] succeeded in 0.0029179000412113965s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:04:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[9ef22058-d9eb-4ca2-bc4a-d2495922b6e2] received
[2026-03-23 09:04:33,843: INFO/MainProcess] Task tasks.scrape_pending_urls[9ef22058-d9eb-4ca2-bc4a-d2495922b6e2] succeeded in 0.005604800011496991s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:05:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[1c3620a4-deac-44c6-b7c5-aa306c9f0b70] received
[2026-03-23 09:05:03,844: INFO/MainProcess] Task tasks.scrape_pending_urls[1c3620a4-deac-44c6-b7c5-aa306c9f0b70] succeeded in 0.005134899984113872s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:05:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[8c15bb23-0948-4123-9e26-59654649a022] received
[2026-03-23 09:05:33,843: INFO/MainProcess] Task tasks.scrape_pending_urls[8c15bb23-0948-4123-9e26-59654649a022] succeeded in 0.005186299968045205s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:06:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[463ecd94-d906-44fd-87a1-4d62b36fc265] received
[2026-03-23 09:06:03,842: INFO/MainProcess] Task tasks.scrape_pending_urls[463ecd94-d906-44fd-87a1-4d62b36fc265] succeeded in 0.005134999984875321s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:06:33,473: INFO/MainProcess] Task tasks.reset_stale_processing_urls[88419558-ce28-4bcf-a211-22135b0a9382] received
[2026-03-23 09:06:33,477: INFO/MainProcess] Reset 0 stale processing URLs.
[2026-03-23 09:06:33,478: INFO/MainProcess] Task tasks.reset_stale_processing_urls[88419558-ce28-4bcf-a211-22135b0a9382] succeeded in 0.003900200012139976s: {'reset': 0}
[2026-03-23 09:06:33,497: INFO/MainProcess] Task tasks.collect_system_metrics[fe92fb4b-11de-4f5f-b978-db403c962218] received
[2026-03-23 09:06:34,003: INFO/MainProcess] Task tasks.collect_system_metrics[fe92fb4b-11de-4f5f-b978-db403c962218] succeeded in 0.5057947000022978s: {'cpu': 13.3, 'memory': 44.8}
[2026-03-23 09:06:34,005: INFO/MainProcess] Task tasks.scrape_pending_urls[f907b359-9db3-4488-af33-0c0cf3ed78a1] received
[2026-03-23 09:06:34,010: INFO/MainProcess] Task tasks.scrape_pending_urls[f907b359-9db3-4488-af33-0c0cf3ed78a1] succeeded in 0.003915300010703504s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:07:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[bc63ee51-8ce2-4024-b13f-aea277ebdee1] received
[2026-03-23 09:07:03,843: INFO/MainProcess] Task tasks.scrape_pending_urls[bc63ee51-8ce2-4024-b13f-aea277ebdee1] succeeded in 0.005059400049503893s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:07:33,838: INFO/MainProcess] Task tasks.scrape_pending_urls[66f676d4-8d4f-46f4-8a98-6c7f391829d3] received
[2026-03-23 09:07:33,843: INFO/MainProcess] Task tasks.scrape_pending_urls[66f676d4-8d4f-46f4-8a98-6c7f391829d3] succeeded in 0.00452179997228086s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:08:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[9807cde3-96b8-4b95-9f1b-c2ddfd19f635] received
[2026-03-23 09:08:03,843: INFO/MainProcess] Task tasks.scrape_pending_urls[9807cde3-96b8-4b95-9f1b-c2ddfd19f635] succeeded in 0.00487750000320375s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:08:33,837: INFO/MainProcess] Task tasks.scrape_pending_urls[e0fabd05-12a9-4acd-a14e-71ab84b10ef1] received
[2026-03-23 09:08:33,842: INFO/MainProcess] Task tasks.scrape_pending_urls[e0fabd05-12a9-4acd-a14e-71ab84b10ef1] succeeded in 0.0043181999935768545s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:09:03,838: INFO/MainProcess] Task tasks.scrape_pending_urls[ccbf3aee-7c19-43fc-8992-c5f7b7da2e01] received
[2026-03-23 09:09:03,842: INFO/MainProcess] Task tasks.scrape_pending_urls[ccbf3aee-7c19-43fc-8992-c5f7b7da2e01] succeeded in 0.003754700010176748s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:09:33,838: INFO/MainProcess] Task tasks.scrape_pending_urls[b230c61d-114a-4b8e-ba54-05515df93b4d] received
[2026-03-23 09:09:33,843: INFO/MainProcess] Task tasks.scrape_pending_urls[b230c61d-114a-4b8e-ba54-05515df93b4d] succeeded in 0.004859199980273843s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:10:03,838: INFO/MainProcess] Task tasks.scrape_pending_urls[69e5ba67-7172-491d-b081-1fc32e41d260] received
[2026-03-23 09:10:03,842: INFO/MainProcess] Task tasks.scrape_pending_urls[69e5ba67-7172-491d-b081-1fc32e41d260] succeeded in 0.0042280000052414834s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:10:33,841: INFO/MainProcess] Task tasks.scrape_pending_urls[aa019820-de14-4e05-aa78-b308ff739bff] received
[2026-03-23 09:10:33,845: INFO/MainProcess] Task tasks.scrape_pending_urls[aa019820-de14-4e05-aa78-b308ff739bff] succeeded in 0.0030750000150874257s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:11:03,841: INFO/MainProcess] Task tasks.scrape_pending_urls[17be5985-cdf4-409a-b85f-29aec985c9b8] received
[2026-03-23 09:11:03,845: INFO/MainProcess] Task tasks.scrape_pending_urls[17be5985-cdf4-409a-b85f-29aec985c9b8] succeeded in 0.003472500015050173s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:11:33,497: INFO/MainProcess] Task tasks.collect_system_metrics[ef61f3e1-dcfb-403b-8c85-adc66da37086] received
[2026-03-23 09:11:34,014: INFO/MainProcess] Task tasks.collect_system_metrics[ef61f3e1-dcfb-403b-8c85-adc66da37086] succeeded in 0.5170428000274114s: {'cpu': 12.3, 'memory': 45.4}
[2026-03-23 09:11:34,016: INFO/MainProcess] Task tasks.scrape_pending_urls[07c84b34-a3a6-4f9f-9f17-4ea271827790] received
[2026-03-23 09:11:34,021: INFO/MainProcess] Task tasks.scrape_pending_urls[07c84b34-a3a6-4f9f-9f17-4ea271827790] succeeded in 0.0039524000021629035s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:12:03,841: INFO/MainProcess] Task tasks.scrape_pending_urls[9fb054fe-68f9-46e2-9f0a-2a62dc28c38c] received
[2026-03-23 09:12:03,845: INFO/MainProcess] Task tasks.scrape_pending_urls[9fb054fe-68f9-46e2-9f0a-2a62dc28c38c] succeeded in 0.0036085000028833747s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:12:33,841: INFO/MainProcess] Task tasks.scrape_pending_urls[9d037f8c-fcb1-4950-ab9f-9b58985b2246] received
[2026-03-23 09:12:33,844: INFO/MainProcess] Task tasks.scrape_pending_urls[9d037f8c-fcb1-4950-ab9f-9b58985b2246] succeeded in 0.0030678000184707344s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:13:03,842: INFO/MainProcess] Task tasks.scrape_pending_urls[bb9db602-beed-42ac-a4b2-0292788c0365] received
[2026-03-23 09:13:03,904: INFO/MainProcess] Task tasks.scrape_pending_urls[bb9db602-beed-42ac-a4b2-0292788c0365] succeeded in 0.061057499959133565s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:13:33,845: INFO/MainProcess] Task tasks.scrape_pending_urls[b5e8d299-eb6a-4655-ae88-e38b82c12cc6] received
[2026-03-23 09:13:33,848: INFO/MainProcess] Task tasks.scrape_pending_urls[b5e8d299-eb6a-4655-ae88-e38b82c12cc6] succeeded in 0.0031050999532453716s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:14:03,847: INFO/MainProcess] Task tasks.scrape_pending_urls[80570ae0-841f-44de-90b8-4713b4b77587] received
[2026-03-23 09:14:04,031: INFO/MainProcess] Task tasks.scrape_pending_urls[80570ae0-841f-44de-90b8-4713b4b77587] succeeded in 0.1832472999813035s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:14:33,845: INFO/MainProcess] Task tasks.scrape_pending_urls[3196899c-c245-49e2-a957-4736536c5fe7] received
[2026-03-23 09:14:33,849: INFO/MainProcess] Task tasks.scrape_pending_urls[3196899c-c245-49e2-a957-4736536c5fe7] succeeded in 0.0039100999711081386s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:15:03,845: INFO/MainProcess] Task tasks.scrape_pending_urls[075d0063-1e7c-4da4-bb98-7d4fb8022392] received
[2026-03-23 09:15:03,849: INFO/MainProcess] Task tasks.scrape_pending_urls[075d0063-1e7c-4da4-bb98-7d4fb8022392] succeeded in 0.0036190999671816826s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:15:33,845: INFO/MainProcess] Task tasks.scrape_pending_urls[8d8e980f-3edb-4296-8d2a-98161bbb2d87] received
[2026-03-23 09:15:33,850: INFO/MainProcess] Task tasks.scrape_pending_urls[8d8e980f-3edb-4296-8d2a-98161bbb2d87] succeeded in 0.0043203000095672905s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:16:03,845: INFO/MainProcess] Task tasks.scrape_pending_urls[b01d9075-d742-469f-8a1a-2a6381ef2621] received
[2026-03-23 09:16:03,851: INFO/MainProcess] Task tasks.scrape_pending_urls[b01d9075-d742-469f-8a1a-2a6381ef2621] succeeded in 0.005617299990262836s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:16:33,498: INFO/MainProcess] Task tasks.collect_system_metrics[f376f1d2-3953-43b6-b684-b1ac1394aaf6] received
[2026-03-23 09:16:34,024: INFO/MainProcess] Task tasks.collect_system_metrics[f376f1d2-3953-43b6-b684-b1ac1394aaf6] succeeded in 0.5262146999593824s: {'cpu': 29.6, 'memory': 44.9}
[2026-03-23 09:16:34,028: INFO/MainProcess] Task tasks.scrape_pending_urls[5d035b2c-47e7-468e-a059-5f7d26c7bd10] received
[2026-03-23 09:16:34,033: INFO/MainProcess] Task tasks.scrape_pending_urls[5d035b2c-47e7-468e-a059-5f7d26c7bd10] succeeded in 0.004901500011328608s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:17:03,848: INFO/MainProcess] Task tasks.scrape_pending_urls[b661efe1-eec1-4803-8deb-8a29d1a50987] received
[2026-03-23 09:17:03,851: INFO/MainProcess] Task tasks.scrape_pending_urls[b661efe1-eec1-4803-8deb-8a29d1a50987] succeeded in 0.003299800038803369s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:17:33,848: INFO/MainProcess] Task tasks.scrape_pending_urls[940f7492-1b79-461b-b306-d73b6471dbbd] received
[2026-03-23 09:17:33,851: INFO/MainProcess] Task tasks.scrape_pending_urls[940f7492-1b79-461b-b306-d73b6471dbbd] succeeded in 0.002743499993812293s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:18:03,849: INFO/MainProcess] Task tasks.scrape_pending_urls[21184c70-ac6f-48ca-aafa-9d619bbed603] received
[2026-03-23 09:18:03,856: INFO/MainProcess] Task tasks.scrape_pending_urls[21184c70-ac6f-48ca-aafa-9d619bbed603] succeeded in 0.0064353999914601445s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:18:33,848: INFO/MainProcess] Task tasks.scrape_pending_urls[78585558-53fd-4495-aaf4-390d423a616c] received
[2026-03-23 09:18:33,852: INFO/MainProcess] Task tasks.scrape_pending_urls[78585558-53fd-4495-aaf4-390d423a616c] succeeded in 0.004001700028311461s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:19:03,874: INFO/MainProcess] Task tasks.scrape_pending_urls[9096851b-8abe-4f95-b804-37deface64ac] received
[2026-03-23 09:19:03,879: INFO/MainProcess] Task tasks.scrape_pending_urls[9096851b-8abe-4f95-b804-37deface64ac] succeeded in 0.0045000999816693366s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:19:33,854: INFO/MainProcess] Task tasks.scrape_pending_urls[6df5668d-c732-459c-9f57-7d13e538b6ef] received
[2026-03-23 09:19:33,861: INFO/MainProcess] Task tasks.scrape_pending_urls[6df5668d-c732-459c-9f57-7d13e538b6ef] succeeded in 0.0068607000284828246s: {'status': 'idle', 'pending': 0}
[2026-03-23 09:20:03,849: INFO/MainProcess] Task tasks.scrape_pending_urls[1a09af3c-8e54-4a07-8089-8063d04d3bd9] received
[2026-03-23 09:20:03,854: INFO/MainProcess] Task tasks.scrape_pending_urls[1a09af3c-8e54-4a07-8089-8063d04d3bd9] succeeded in 0.004910299961920828s: {'status': 'idle', 'pending': 0}
