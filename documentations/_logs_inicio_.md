===  BookingScraper Celery Worker  ===


 -------------- worker@HOUSE v5.4.0 (opalescent)
--- ***** -----
-- ******* ---- Windows-11-10.0.26200-SP0 2026-03-29 23:18:47
- *** --- * ---
- ** ---------- [config]
- ** ---------- .> app:         bookingscraper:0x282ea9c86e0
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

[2026-03-29 23:18:50,044: INFO/MainProcess] Connected to redis://localhost:6379/0
[2026-03-29 23:18:54,142: INFO/MainProcess] mingle: searching for neighbors
[2026-03-29 23:19:01,272: INFO/MainProcess] mingle: all alone
[2026-03-29 23:19:09,456: INFO/MainProcess] worker@HOUSE ready.
[2026-03-29 23:19:23,616: INFO/MainProcess] Task tasks.scrape_pending_urls[fac5e7aa-885d-4d78-b31a-b6503edb4821] received
[2026-03-29 23:19:25,781: INFO/MainProcess] Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5
[2026-03-29 23:19:25,863: INFO/MainProcess] Task tasks.scrape_pending_urls[fac5e7aa-885d-4d78-b31a-b6503edb4821] succeeded in 2.246823100023903s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:19:47,486: INFO/MainProcess] Task tasks.scrape_pending_urls[23af3831-5846-463b-b785-3c95d1707ee7] received
[2026-03-29 23:19:47,489: INFO/MainProcess] Task tasks.scrape_pending_urls[23af3831-5846-463b-b785-3c95d1707ee7] succeeded in 0.0030713999876752496s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:20:17,486: INFO/MainProcess] Task tasks.scrape_pending_urls[6425eacb-bd82-4c9d-b89c-b861a2f973c6] received
[2026-03-29 23:20:17,489: INFO/MainProcess] Task tasks.scrape_pending_urls[6425eacb-bd82-4c9d-b89c-b861a2f973c6] succeeded in 0.0031821999000385404s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:20:47,486: INFO/MainProcess] Task tasks.scrape_pending_urls[38c1b26b-29bd-49fc-8a0f-21280704decb] received
[2026-03-29 23:20:47,489: INFO/MainProcess] Task tasks.scrape_pending_urls[38c1b26b-29bd-49fc-8a0f-21280704decb] succeeded in 0.003069399972446263s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:21:17,488: INFO/MainProcess] Task tasks.scrape_pending_urls[62d131f4-c7f2-4464-b266-a8ebbcb96c03] received
[2026-03-29 23:21:17,496: INFO/MainProcess] Task tasks.scrape_pending_urls[62d131f4-c7f2-4464-b266-a8ebbcb96c03] succeeded in 0.007587200030684471s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:21:47,486: INFO/MainProcess] Task tasks.scrape_pending_urls[b428975d-78b7-4a86-a3fe-1f95a39307e4] received
[2026-03-29 23:21:47,489: INFO/MainProcess] Task tasks.scrape_pending_urls[b428975d-78b7-4a86-a3fe-1f95a39307e4] succeeded in 0.003119200002402067s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:22:17,486: INFO/MainProcess] Task tasks.scrape_pending_urls[fd7d2e5c-ece0-4957-a7e4-d370e01cd367] received
[2026-03-29 23:22:17,491: INFO/MainProcess] Task tasks.scrape_pending_urls[fd7d2e5c-ece0-4957-a7e4-d370e01cd367] succeeded in 0.004083200008608401s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:22:47,486: INFO/MainProcess] Task tasks.scrape_pending_urls[44e2cc1a-a842-457e-9b69-06a60921a12f] received
[2026-03-29 23:22:47,490: INFO/MainProcess] Task tasks.scrape_pending_urls[44e2cc1a-a842-457e-9b69-06a60921a12f] succeeded in 0.0029728999361395836s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:23:17,486: INFO/MainProcess] Task tasks.scrape_pending_urls[8fb097ed-158e-4788-90aa-6d5ca30e11f6] received
[2026-03-29 23:23:17,491: INFO/MainProcess] Task tasks.scrape_pending_urls[8fb097ed-158e-4788-90aa-6d5ca30e11f6] succeeded in 0.004409799934364855s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:23:47,483: INFO/MainProcess] Task tasks.collect_system_metrics[b4dcc7e7-aa77-44cb-9d21-bbd73546dcf3] received
[2026-03-29 23:23:48,003: INFO/MainProcess] Task tasks.collect_system_metrics[b4dcc7e7-aa77-44cb-9d21-bbd73546dcf3] succeeded in 0.5197329000802711s: {'cpu': 13.2, 'memory': 48.5}
[2026-03-29 23:23:48,005: INFO/MainProcess] Task tasks.scrape_pending_urls[909a0a03-2b42-44a0-afe5-efb7950bf8da] received
[2026-03-29 23:23:48,008: INFO/MainProcess] Task tasks.scrape_pending_urls[909a0a03-2b42-44a0-afe5-efb7950bf8da] succeeded in 0.003489400027319789s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:24:17,486: INFO/MainProcess] Task tasks.scrape_pending_urls[9d8b43ac-1825-43cf-9ab6-11efec3b9c7d] received
[2026-03-29 23:24:17,490: INFO/MainProcess] Task tasks.scrape_pending_urls[9d8b43ac-1825-43cf-9ab6-11efec3b9c7d] succeeded in 0.003669800003990531s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:24:47,486: INFO/MainProcess] Task tasks.scrape_pending_urls[d0880177-77ae-4595-99be-ed96b68c9e98] received
[2026-03-29 23:24:47,490: INFO/MainProcess] Task tasks.scrape_pending_urls[d0880177-77ae-4595-99be-ed96b68c9e98] succeeded in 0.0035629000049084425s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:25:17,487: INFO/MainProcess] Task tasks.scrape_pending_urls[cc15e97e-c142-400b-9ec3-7230f71ea00e] received
[2026-03-29 23:25:17,492: INFO/MainProcess] Task tasks.scrape_pending_urls[cc15e97e-c142-400b-9ec3-7230f71ea00e] succeeded in 0.0047351999673992395s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:25:47,491: INFO/MainProcess] Task tasks.scrape_pending_urls[00ac47de-ca27-411e-92b6-f5e4d70ef19c] received
[2026-03-29 23:25:47,495: INFO/MainProcess] Task tasks.scrape_pending_urls[00ac47de-ca27-411e-92b6-f5e4d70ef19c] succeeded in 0.0030119000002741814s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:26:17,491: INFO/MainProcess] Task tasks.scrape_pending_urls[b1384e40-6739-4900-984d-bc4a840bff5c] received
[2026-03-29 23:26:17,494: INFO/MainProcess] Task tasks.scrape_pending_urls[b1384e40-6739-4900-984d-bc4a840bff5c] succeeded in 0.002761899959295988s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:26:47,492: INFO/MainProcess] Task tasks.scrape_pending_urls[daca2cda-3f7a-4e81-85cc-489c077dc779] received
[2026-03-29 23:26:47,500: INFO/MainProcess] Task tasks.scrape_pending_urls[daca2cda-3f7a-4e81-85cc-489c077dc779] succeeded in 0.006895800004713237s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:27:17,492: INFO/MainProcess] Task tasks.scrape_pending_urls[c4894bc8-676b-47d2-ba43-bb5be9a9fe9b] received
[2026-03-29 23:27:17,498: INFO/MainProcess] Task tasks.scrape_pending_urls[c4894bc8-676b-47d2-ba43-bb5be9a9fe9b] succeeded in 0.005240500089712441s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:27:47,493: INFO/MainProcess] Task tasks.scrape_pending_urls[ea09b812-adbd-4194-898d-2bae8a5e833f] received
[2026-03-29 23:27:47,502: INFO/MainProcess] Task tasks.scrape_pending_urls[ea09b812-adbd-4194-898d-2bae8a5e833f] succeeded in 0.007001099991612136s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:28:17,492: INFO/MainProcess] Task tasks.scrape_pending_urls[846a81fd-ab2a-4751-9e5b-dc8ef887b66c] received
[2026-03-29 23:28:17,495: INFO/MainProcess] Task tasks.scrape_pending_urls[846a81fd-ab2a-4751-9e5b-dc8ef887b66c] succeeded in 0.003233899944461882s: {'status': 'idle', 'pending': 0}
[2026-03-29 23:28:47,482: INFO/MainProcess] Task tasks.collect_system_metrics[fb1ca9e2-7e64-4143-86a5-9edeeec889fd] received
[2026-03-29 23:28:47,999: INFO/MainProcess] Task tasks.collect_system_metrics[fb1ca9e2-7e64-4143-86a5-9edeeec889fd] succeeded in 0.5163911998970434s: {'cpu': 17.8, 'memory': 47.1}
[2026-03-29 23:28:48,001: INFO/MainProcess] Task tasks.scrape_pending_urls[47946296-0fae-4710-a9ec-b900643ad95f] received
[2026-03-29 23:28:50,009: INFO/MainProcess] scrape_pending_urls: starting auto-batch, pending=13
[2026-03-29 23:28:51,692: INFO/MainProcess] VPN: original IP = 185.197.248.123
[2026-03-29 23:28:53,292: INFO/MainProcess] VPN: home country detected = AR
[2026-03-29 23:28:53,297: INFO/MainProcess] NordVPNManager initialised | interactive=False | original_ip=185.197.248.123 | home_country=AR
[2026-03-29 23:28:53,297: INFO/MainProcess] ScraperService INIT | VPN_ENABLED=True | HEADLESS_BROWSER=False | workers=2 | languages=en,es,de,it,fr,pt | vpn_interval=50s | vpn_countries=Spain,Germany,France,Netherlands,Italy,United_Kingdom,Canada,Sweden
[2026-03-29 23:28:53,334: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-29 23:29:16,374: INFO/MainProcess] VPN connected to Germany — IP: 212.23.215.41
[2026-03-29 23:29:16,374: INFO/MainProcess] VPN connected OK before batch start.
[2026-03-29 23:29:16,376: INFO/MainProcess] Dispatching batch: urls=13 workers=2
[2026-03-29 23:29:16,377: INFO/MainProcess] Redis connection pool created: max_connections=20
[2026-03-29 23:29:21,308: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.en-gb.html?lang=en-gb
[2026-03-29 23:29:21,308: INFO/MainProcess] CloudScraper failed for 1517f2fc-0c45-4db0-8339-888c17831571/en — trying Selenium.
[2026-03-29 23:29:21,317: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.en-gb.html?lang=en-gb
[2026-03-29 23:29:21,318: INFO/MainProcess] CloudScraper failed for 08c9481e-c70e-490d-9ee4-46dcae52b82e/en — trying Selenium.
[2026-03-29 23:29:24,654: INFO/MainProcess] Selenium: Brave started
[2026-03-29 23:31:42,192: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 23:31:44,136: INFO/MainProcess] Gallery: 137 images loaded after scroll
[2026-03-29 23:31:47,411: INFO/MainProcess] Gallery: 144 unique image URLs extracted
[2026-03-29 23:31:47,536: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 23:31:47,537: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 23:32:13,966: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 1517f2fc-0c45-4db0-8339-888c17831571
[2026-03-29 23:32:26,744: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 98fcc3e0-6949-4c45-8800-3ffa24b3559e
[2026-03-29 23:32:26,744: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 98fcc3e0-6949-4c45-8800-3ffa24b3559e
[2026-03-29 23:32:26,753: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571 lang=en: SUCCESS
[2026-03-29 23:32:26,753: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.6s (base=10.0 jitter=4.6) before 1517f2fc-0c45-4db0-8339-888c17831571/es
[2026-03-29 23:32:43,998: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.es.html?lang=es
[2026-03-29 23:32:43,999: INFO/MainProcess] CloudScraper failed for 1517f2fc-0c45-4db0-8339-888c17831571/es — trying Selenium.
[2026-03-29 23:34:36,821: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 23:34:39,066: INFO/MainProcess] Gallery: 131 images loaded after scroll
[2026-03-29 23:34:42,585: INFO/MainProcess] Gallery: 138 unique image URLs extracted
[2026-03-29 23:34:42,756: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 23:34:42,756: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 23:35:10,844: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 08c9481e-c70e-490d-9ee4-46dcae52b82e
[2026-03-29 23:35:18,742: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel a43eff5f-3dc2-46a9-9df5-bb9ccefe37d4
[2026-03-29 23:35:18,742: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel a43eff5f-3dc2-46a9-9df5-bb9ccefe37d4
[2026-03-29 23:35:18,750: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e lang=en: SUCCESS
[2026-03-29 23:35:18,751: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 15.0s (base=10.0 jitter=5.0) before 08c9481e-c70e-490d-9ee4-46dcae52b82e/es
[2026-03-29 23:35:36,385: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 23:35:57,640: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 23:36:02,208: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.es.html?lang=es
[2026-03-29 23:36:02,208: INFO/MainProcess] CloudScraper failed for 08c9481e-c70e-490d-9ee4-46dcae52b82e/es — trying Selenium.
[2026-03-29 23:36:28,969: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571 lang=es: SUCCESS
[2026-03-29 23:36:28,969: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.5s (base=10.0 jitter=0.5) before 1517f2fc-0c45-4db0-8339-888c17831571/de
[2026-03-29 23:36:42,529: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.de.html?lang=de
[2026-03-29 23:36:42,530: INFO/MainProcess] CloudScraper failed for 1517f2fc-0c45-4db0-8339-888c17831571/de — trying Selenium.
[2026-03-29 23:37:47,403: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e lang=es: SUCCESS
[2026-03-29 23:37:47,403: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.9s (base=10.0 jitter=4.9) before 08c9481e-c70e-490d-9ee4-46dcae52b82e/de
[2026-03-29 23:38:05,009: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.de.html?lang=de
[2026-03-29 23:38:05,009: INFO/MainProcess] CloudScraper failed for 08c9481e-c70e-490d-9ee4-46dcae52b82e/de — trying Selenium.
[2026-03-29 23:39:06,619: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571 lang=de: SUCCESS
[2026-03-29 23:39:06,619: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.9s (base=10.0 jitter=2.9) before 1517f2fc-0c45-4db0-8339-888c17831571/it
[2026-03-29 23:39:22,274: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.it.html?lang=it
[2026-03-29 23:39:22,275: INFO/MainProcess] CloudScraper failed for 1517f2fc-0c45-4db0-8339-888c17831571/it — trying Selenium.
[2026-03-29 23:40:38,277: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e lang=de: SUCCESS
[2026-03-29 23:40:38,277: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.9s (base=10.0 jitter=0.9) before 08c9481e-c70e-490d-9ee4-46dcae52b82e/it
[2026-03-29 23:40:51,848: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 23:41:17,643: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 23:41:22,424: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.it.html?lang=it
[2026-03-29 23:41:22,425: INFO/MainProcess] CloudScraper failed for 08c9481e-c70e-490d-9ee4-46dcae52b82e/it — trying Selenium.
[2026-03-29 23:41:57,119: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571 lang=it: SUCCESS
[2026-03-29 23:41:57,119: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.5s (base=10.0 jitter=2.5) before 1517f2fc-0c45-4db0-8339-888c17831571/fr
[2026-03-29 23:42:12,367: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.fr.html?lang=fr
[2026-03-29 23:42:12,367: INFO/MainProcess] CloudScraper failed for 1517f2fc-0c45-4db0-8339-888c17831571/fr — trying Selenium.
[2026-03-29 23:43:14,229: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e lang=it: SUCCESS
[2026-03-29 23:43:14,229: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.9s (base=10.0 jitter=0.9) before 08c9481e-c70e-490d-9ee4-46dcae52b82e/fr
[2026-03-29 23:43:27,734: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.fr.html?lang=fr
[2026-03-29 23:43:27,734: INFO/MainProcess] CloudScraper failed for 08c9481e-c70e-490d-9ee4-46dcae52b82e/fr — trying Selenium.
[2026-03-29 23:44:31,501: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571 lang=fr: SUCCESS
[2026-03-29 23:44:31,502: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.5s (base=10.0 jitter=3.5) before 1517f2fc-0c45-4db0-8339-888c17831571/pt
[2026-03-29 23:44:47,744: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/centara-grand-lagoon-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 23:44:47,745: INFO/MainProcess] CloudScraper failed for 1517f2fc-0c45-4db0-8339-888c17831571/pt — trying Selenium.
[2026-03-29 23:46:03,556: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e lang=fr: SUCCESS
[2026-03-29 23:46:03,556: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.5s (base=10.0 jitter=3.5) before 08c9481e-c70e-490d-9ee4-46dcae52b82e/pt
[2026-03-29 23:46:19,812: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/mv/niyama-private-islands-maldives.pt-pt.html?lang=pt-pt
[2026-03-29 23:46:19,812: INFO/MainProcess] CloudScraper failed for 08c9481e-c70e-490d-9ee4-46dcae52b82e/pt — trying Selenium.
[2026-03-29 23:47:21,822: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571 lang=pt: SUCCESS
[2026-03-29 23:47:21,826: INFO/MainProcess] URL 1517f2fc-0c45-4db0-8339-888c17831571: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 23:47:24,681: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/vc/the-pink-sands-club.en-gb.html?lang=en-gb
[2026-03-29 23:47:24,681: INFO/MainProcess] CloudScraper failed for 522e3b47-253b-428a-8372-19b6fdf3b111/en — trying Selenium.
[2026-03-29 23:48:39,598: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e lang=pt: SUCCESS
[2026-03-29 23:48:39,601: INFO/MainProcess] URL 08c9481e-c70e-490d-9ee4-46dcae52b82e: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-29 23:48:42,457: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/south-bank.en-gb.html?lang=en-gb
[2026-03-29 23:48:42,457: INFO/MainProcess] CloudScraper failed for deb01fc5-4915-4dc5-aef1-0e53286eef80/en — trying Selenium.
[2026-03-29 23:50:59,084: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 23:51:01,001: INFO/MainProcess] Gallery: 87 images loaded after scroll
[2026-03-29 23:51:03,215: INFO/MainProcess] Gallery: 94 unique image URLs extracted
[2026-03-29 23:51:03,354: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 23:51:03,354: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 23:51:29,105: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 522e3b47-253b-428a-8372-19b6fdf3b111
[2026-03-29 23:51:42,564: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 6a60a10e-fa11-4ccd-881d-ca7c2778bdcd
[2026-03-29 23:51:42,564: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 6a60a10e-fa11-4ccd-881d-ca7c2778bdcd
[2026-03-29 23:51:42,571: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111 lang=en: SUCCESS
[2026-03-29 23:51:42,571: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.9s (base=10.0 jitter=4.9) before 522e3b47-253b-428a-8372-19b6fdf3b111/es
[2026-03-29 23:52:00,253: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 23:52:22,211: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 23:52:27,001: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/vc/the-pink-sands-club.es.html?lang=es
[2026-03-29 23:52:27,001: INFO/MainProcess] CloudScraper failed for 522e3b47-253b-428a-8372-19b6fdf3b111/es — trying Selenium.
[2026-03-29 23:53:50,419: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-29 23:53:52,427: INFO/MainProcess] Gallery: 266 images loaded after scroll
[2026-03-29 23:53:58,106: INFO/MainProcess] Gallery: 273 unique image URLs extracted
[2026-03-29 23:53:58,319: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-29 23:53:59,284: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-29 23:54:27,862: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for deb01fc5-4915-4dc5-aef1-0e53286eef80
[2026-03-29 23:54:35,868: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel f3824d23-2647-49d2-a790-9f7d75285cc4
[2026-03-29 23:54:35,868: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel f3824d23-2647-49d2-a790-9f7d75285cc4
[2026-03-29 23:54:35,875: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80 lang=en: SUCCESS
[2026-03-29 23:54:35,875: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.5s (base=10.0 jitter=2.5) before deb01fc5-4915-4dc5-aef1-0e53286eef80/es
[2026-03-29 23:54:51,126: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/south-bank.es.html?lang=es
[2026-03-29 23:54:51,127: INFO/MainProcess] CloudScraper failed for deb01fc5-4915-4dc5-aef1-0e53286eef80/es — trying Selenium.
[2026-03-29 23:55:46,259: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111 lang=es: SUCCESS
[2026-03-29 23:55:46,259: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.3s (base=10.0 jitter=0.3) before 522e3b47-253b-428a-8372-19b6fdf3b111/de
[2026-03-29 23:55:59,296: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/vc/the-pink-sands-club.de.html?lang=de
[2026-03-29 23:55:59,297: INFO/MainProcess] CloudScraper failed for 522e3b47-253b-428a-8372-19b6fdf3b111/de — trying Selenium.
[2026-03-29 23:57:03,302: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80 lang=es: SUCCESS
[2026-03-29 23:57:03,302: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.0s (base=10.0 jitter=3.0) before deb01fc5-4915-4dc5-aef1-0e53286eef80/de
[2026-03-29 23:57:19,229: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 23:57:45,000: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 23:57:49,849: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/south-bank.de.html?lang=de
[2026-03-29 23:57:49,850: INFO/MainProcess] CloudScraper failed for deb01fc5-4915-4dc5-aef1-0e53286eef80/de — trying Selenium.
[2026-03-29 23:58:22,725: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111 lang=de: SUCCESS
[2026-03-29 23:58:22,725: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 11.5s (base=10.0 jitter=1.5) before 522e3b47-253b-428a-8372-19b6fdf3b111/it
[2026-03-29 23:58:37,106: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/vc/the-pink-sands-club.it.html?lang=it
[2026-03-29 23:58:37,107: INFO/MainProcess] CloudScraper failed for 522e3b47-253b-428a-8372-19b6fdf3b111/it — trying Selenium.
[2026-03-29 23:59:54,478: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80 lang=de: SUCCESS
[2026-03-29 23:59:54,478: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 11.7s (base=10.0 jitter=1.7) before deb01fc5-4915-4dc5-aef1-0e53286eef80/it
[2026-03-30 00:00:08,912: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/south-bank.it.html?lang=it
[2026-03-30 00:00:08,913: INFO/MainProcess] CloudScraper failed for deb01fc5-4915-4dc5-aef1-0e53286eef80/it — trying Selenium.
[2026-03-30 00:01:11,161: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111 lang=it: SUCCESS
[2026-03-30 00:01:11,161: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.7s (base=10.0 jitter=3.7) before 522e3b47-253b-428a-8372-19b6fdf3b111/fr
[2026-03-30 00:01:27,621: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/vc/the-pink-sands-club.fr.html?lang=fr
[2026-03-30 00:01:27,622: INFO/MainProcess] CloudScraper failed for 522e3b47-253b-428a-8372-19b6fdf3b111/fr — trying Selenium.
[2026-03-30 00:02:30,909: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80 lang=it: SUCCESS
[2026-03-30 00:02:30,909: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 11.1s (base=10.0 jitter=1.1) before deb01fc5-4915-4dc5-aef1-0e53286eef80/fr
[2026-03-30 00:02:44,816: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/south-bank.fr.html?lang=fr
[2026-03-30 00:02:44,817: INFO/MainProcess] CloudScraper failed for deb01fc5-4915-4dc5-aef1-0e53286eef80/fr — trying Selenium.
[2026-03-30 00:03:47,999: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111 lang=fr: SUCCESS
[2026-03-30 00:03:48,000: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.9s (base=10.0 jitter=3.9) before 522e3b47-253b-428a-8372-19b6fdf3b111/pt
[2026-03-30 00:04:05,522: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/vc/the-pink-sands-club.pt-pt.html?lang=pt-pt
[2026-03-30 00:04:05,523: INFO/MainProcess] CloudScraper failed for 522e3b47-253b-428a-8372-19b6fdf3b111/pt — trying Selenium.
[2026-03-30 00:05:22,077: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80 lang=fr: SUCCESS
[2026-03-30 00:05:22,078: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.8s (base=10.0 jitter=2.8) before deb01fc5-4915-4dc5-aef1-0e53286eef80/pt
[2026-03-30 00:05:37,556: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/south-bank.pt-pt.html?lang=pt-pt
[2026-03-30 00:05:37,557: INFO/MainProcess] CloudScraper failed for deb01fc5-4915-4dc5-aef1-0e53286eef80/pt — trying Selenium.
[2026-03-30 00:06:40,536: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111 lang=pt: SUCCESS
[2026-03-30 00:06:40,538: INFO/MainProcess] URL 522e3b47-253b-428a-8372-19b6fdf3b111: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 00:06:43,363: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/grace-bay-club.en-gb.html?lang=en-gb
[2026-03-30 00:06:43,363: INFO/MainProcess] CloudScraper failed for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/en — trying Selenium.
[2026-03-30 00:07:59,854: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80 lang=pt: SUCCESS
[2026-03-30 00:07:59,857: INFO/MainProcess] URL deb01fc5-4915-4dc5-aef1-0e53286eef80: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 00:08:02,615: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bs/the-island-garden.en-gb.html?lang=en-gb
[2026-03-30 00:08:02,616: INFO/MainProcess] CloudScraper failed for 2ffa0b26-b82e-4751-9da0-9bd058266e48/en — trying Selenium.
[2026-03-30 00:10:22,044: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 00:10:23,971: INFO/MainProcess] Gallery: 118 images loaded after scroll
[2026-03-30 00:10:27,675: INFO/MainProcess] Gallery: 125 unique image URLs extracted
[2026-03-30 00:10:27,872: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-30 00:10:27,873: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-30 00:10:55,727: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e
[2026-03-30 00:11:03,419: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel af422ba4-8ce0-443a-8cd7-0f07b9aada6f
[2026-03-30 00:11:03,420: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel af422ba4-8ce0-443a-8cd7-0f07b9aada6f
[2026-03-30 00:11:03,427: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e lang=en: SUCCESS
[2026-03-30 00:11:03,427: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.3s (base=10.0 jitter=4.3) before ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/es
[2026-03-30 00:11:20,494: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/grace-bay-club.es.html?lang=es
[2026-03-30 00:11:20,494: INFO/MainProcess] CloudScraper failed for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/es — trying Selenium.
[2026-03-30 00:13:15,144: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 00:13:17,047: INFO/MainProcess] Gallery: 24 images loaded after scroll
[2026-03-30 00:13:18,215: INFO/MainProcess] Gallery: 31 unique image URLs extracted
[2026-03-30 00:13:18,345: INFO/MainProcess] hotelPhotos JS: 24 photos extracted from page source
[2026-03-30 00:13:18,346: INFO/MainProcess] Gallery: 24 photos with full metadata (hotelPhotos JS)
[2026-03-30 00:13:43,842: INFO/MainProcess] Photos: 24 rich photo records (hotelPhotos JS) for 2ffa0b26-b82e-4751-9da0-9bd058266e48
[2026-03-30 00:13:48,714: INFO/MainProcess] download_photo_batch: 72/72 photo-files saved for hotel 0b147834-3dec-4ee7-b132-631e8552361f
[2026-03-30 00:13:48,714: INFO/MainProcess] ImageDownloader (photo_batch): 72/24 photos saved for hotel 0b147834-3dec-4ee7-b132-631e8552361f
[2026-03-30 00:13:48,720: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48 lang=en: SUCCESS
[2026-03-30 00:13:48,721: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.8s (base=10.0 jitter=3.8) before 2ffa0b26-b82e-4751-9da0-9bd058266e48/es
[2026-03-30 00:14:05,348: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bs/the-island-garden.es.html?lang=es
[2026-03-30 00:14:05,348: INFO/MainProcess] CloudScraper failed for 2ffa0b26-b82e-4751-9da0-9bd058266e48/es — trying Selenium.
[2026-03-30 00:15:02,847: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e lang=es: SUCCESS
[2026-03-30 00:15:02,848: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.5s (base=10.0 jitter=3.5) before ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/de
[2026-03-30 00:15:19,108: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/grace-bay-club.de.html?lang=de
[2026-03-30 00:15:19,109: INFO/MainProcess] CloudScraper failed for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/de — trying Selenium.
[2026-03-30 00:16:22,221: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48 lang=es: SUCCESS
[2026-03-30 00:16:22,221: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.4s (base=10.0 jitter=3.4) before 2ffa0b26-b82e-4751-9da0-9bd058266e48/de
[2026-03-30 00:16:38,339: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bs/the-island-garden.de.html?lang=de
[2026-03-30 00:16:38,339: INFO/MainProcess] CloudScraper failed for 2ffa0b26-b82e-4751-9da0-9bd058266e48/de — trying Selenium.
[2026-03-30 00:17:41,122: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e lang=de: SUCCESS
[2026-03-30 00:17:41,123: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 11.3s (base=10.0 jitter=1.3) before ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/it
[2026-03-30 00:17:55,187: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/grace-bay-club.it.html?lang=it
[2026-03-30 00:17:55,188: INFO/MainProcess] CloudScraper failed for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/it — trying Selenium.
[2026-03-30 00:19:13,350: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48 lang=de: SUCCESS
[2026-03-30 00:19:13,350: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.2s (base=10.0 jitter=3.2) before 2ffa0b26-b82e-4751-9da0-9bd058266e48/it
[2026-03-30 00:19:29,256: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bs/the-island-garden.it.html?lang=it
[2026-03-30 00:19:29,257: INFO/MainProcess] CloudScraper failed for 2ffa0b26-b82e-4751-9da0-9bd058266e48/it — trying Selenium.
[2026-03-30 00:20:31,074: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e lang=it: SUCCESS
[2026-03-30 00:20:31,074: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.2s (base=10.0 jitter=2.2) before ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/fr
[2026-03-30 00:20:45,930: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/grace-bay-club.fr.html?lang=fr
[2026-03-30 00:20:45,930: INFO/MainProcess] CloudScraper failed for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/fr — trying Selenium.
[2026-03-30 00:21:48,963: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48 lang=it: SUCCESS
[2026-03-30 00:21:48,963: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.2s (base=10.0 jitter=2.2) before 2ffa0b26-b82e-4751-9da0-9bd058266e48/fr
[2026-03-30 00:22:03,837: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bs/the-island-garden.fr.html?lang=fr
[2026-03-30 00:22:03,837: INFO/MainProcess] CloudScraper failed for 2ffa0b26-b82e-4751-9da0-9bd058266e48/fr — trying Selenium.
[2026-03-30 00:23:08,002: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e lang=fr: SUCCESS
[2026-03-30 00:23:08,002: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.2s (base=10.0 jitter=3.2) before ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/pt
[2026-03-30 00:23:23,826: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/tc/grace-bay-club.pt-pt.html?lang=pt-pt
[2026-03-30 00:23:23,827: INFO/MainProcess] CloudScraper failed for ff5a49c6-5be7-48cf-bf46-88b9fe9c571e/pt — trying Selenium.
[2026-03-30 00:24:39,368: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48 lang=fr: SUCCESS
[2026-03-30 00:24:39,369: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.2s (base=10.0 jitter=2.2) before 2ffa0b26-b82e-4751-9da0-9bd058266e48/pt
[2026-03-30 00:24:54,603: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bs/the-island-garden.pt-pt.html?lang=pt-pt
[2026-03-30 00:24:54,603: INFO/MainProcess] CloudScraper failed for 2ffa0b26-b82e-4751-9da0-9bd058266e48/pt — trying Selenium.
[2026-03-30 00:25:59,072: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e lang=pt: SUCCESS
[2026-03-30 00:25:59,074: INFO/MainProcess] URL ff5a49c6-5be7-48cf-bf46-88b9fe9c571e: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 00:26:01,821: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bb/leroy.en-gb.html?lang=en-gb
[2026-03-30 00:26:01,821: INFO/MainProcess] CloudScraper failed for 29628e9c-cf8e-48fc-b19e-8d873698c579/en — trying Selenium.
[2026-03-30 00:27:16,410: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48 lang=pt: SUCCESS
[2026-03-30 00:27:16,414: INFO/MainProcess] URL 2ffa0b26-b82e-4751-9da0-9bd058266e48: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 00:27:19,116: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:27:19,117: INFO/MainProcess] CloudScraper failed for 2982685e-b5c1-4b7a-851c-7a34c7209076/en — trying Selenium.
[2026-03-30 00:29:38,555: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 00:29:40,514: INFO/MainProcess] Gallery: 144 images loaded after scroll
[2026-03-30 00:29:44,617: INFO/MainProcess] Gallery: 151 unique image URLs extracted
[2026-03-30 00:29:44,802: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-30 00:29:44,803: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-30 00:30:11,727: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 29628e9c-cf8e-48fc-b19e-8d873698c579
[2026-03-30 00:30:17,829: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 0ffe29e2-5320-45d3-80f6-3d017019e26c
[2026-03-30 00:30:17,829: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 0ffe29e2-5320-45d3-80f6-3d017019e26c
[2026-03-30 00:30:17,834: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579 lang=en: SUCCESS
[2026-03-30 00:30:17,835: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.1s (base=10.0 jitter=3.1) before 29628e9c-cf8e-48fc-b19e-8d873698c579/es
[2026-03-30 00:30:33,689: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bb/leroy.es.html?lang=es
[2026-03-30 00:30:33,693: INFO/MainProcess] CloudScraper failed for 29628e9c-cf8e-48fc-b19e-8d873698c579/es — trying Selenium.
[2026-03-30 00:31:30,547: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-30 00:31:42,694: INFO/MainProcess] Selenium retry 2 -- waiting 18s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:33:15,725: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-30 00:33:27,264: INFO/MainProcess] Selenium retry 3 -- waiting 28s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:35:10,058: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-30 00:35:10,058: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:35:10,060: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 2982685e-b5c1-4b7a-851c-7a34c7209076/en
[2026-03-30 00:35:10,061: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-30 00:35:11,096: INFO/MainProcess] VPN disconnected.
[2026-03-30 00:35:16,097: INFO/MainProcess] VPN: connecting to Germany (DE)...
[2026-03-30 00:35:35,748: INFO/MainProcess] VPN connected to Germany — IP: 5.253.115.119
[2026-03-30 00:35:35,748: INFO/MainProcess] VPN rotation successful → Germany
[2026-03-30 00:35:35,749: INFO/MainProcess] VPN rotated — retrying 2982685e-b5c1-4b7a-851c-7a34c7209076/en with CloudScraper.
[2026-03-30 00:35:38,669: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:35:38,669: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-30 00:36:27,749: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579 lang=es: SUCCESS
[2026-03-30 00:36:27,750: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.1s (base=10.0 jitter=4.1) before 29628e9c-cf8e-48fc-b19e-8d873698c579/de
[2026-03-30 00:36:45,549: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bb/leroy.de.html?lang=de
[2026-03-30 00:36:45,549: INFO/MainProcess] CloudScraper failed for 29628e9c-cf8e-48fc-b19e-8d873698c579/de — trying Selenium.
[2026-03-30 00:37:45,051: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-30 00:37:56,459: INFO/MainProcess] Selenium retry 2 -- waiting 14s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:39:27,976: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-30 00:39:40,491: INFO/MainProcess] Selenium retry 3 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:41:25,086: WARNING/MainProcess] Selenium language mismatch: requested=en got=es
[2026-03-30 00:41:25,086: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.en-gb.html?lang=en-gb
[2026-03-30 00:41:25,109: WARNING/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 lang=en: FAILED
[2026-03-30 00:41:25,109: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.1s (base=10.0 jitter=4.1) before 2982685e-b5c1-4b7a-851c-7a34c7209076/es
[2026-03-30 00:41:42,867: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.es.html?lang=es
[2026-03-30 00:41:42,868: INFO/MainProcess] CloudScraper failed for 2982685e-b5c1-4b7a-851c-7a34c7209076/es — trying Selenium.
[2026-03-30 00:42:42,421: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579 lang=de: SUCCESS
[2026-03-30 00:42:42,421: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.8s (base=10.0 jitter=0.8) before 29628e9c-cf8e-48fc-b19e-8d873698c579/it
[2026-03-30 00:42:56,167: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bb/leroy.it.html?lang=it
[2026-03-30 00:42:56,167: INFO/MainProcess] CloudScraper failed for 29628e9c-cf8e-48fc-b19e-8d873698c579/it — trying Selenium.
[2026-03-30 00:44:01,294: INFO/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 lang=es: SUCCESS
[2026-03-30 00:44:01,295: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.8s (base=10.0 jitter=2.8) before 2982685e-b5c1-4b7a-851c-7a34c7209076/de
[2026-03-30 00:44:19,907: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:44:19,907: INFO/MainProcess] CloudScraper failed for 2982685e-b5c1-4b7a-851c-7a34c7209076/de — trying Selenium.
[2026-03-30 00:45:48,291: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579 lang=it: SUCCESS
[2026-03-30 00:45:48,291: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.4s (base=10.0 jitter=2.4) before 29628e9c-cf8e-48fc-b19e-8d873698c579/fr
[2026-03-30 00:46:03,310: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bb/leroy.fr.html?lang=fr
[2026-03-30 00:46:03,310: INFO/MainProcess] CloudScraper failed for 29628e9c-cf8e-48fc-b19e-8d873698c579/fr — trying Selenium.
[2026-03-30 00:47:06,271: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-30 00:47:20,534: INFO/MainProcess] Selenium retry 2 -- waiting 17s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:48:53,488: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-30 00:49:05,857: INFO/MainProcess] Selenium retry 3 -- waiting 27s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:50:48,006: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-30 00:50:48,007: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:50:48,009: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 2982685e-b5c1-4b7a-851c-7a34c7209076/de
[2026-03-30 00:50:48,009: INFO/MainProcess] VPN: rotating (current=DE)...
[2026-03-30 00:50:48,978: INFO/MainProcess] VPN disconnected.
[2026-03-30 00:50:53,979: INFO/MainProcess] VPN: connecting to France (FR)...
[2026-03-30 00:51:12,302: INFO/MainProcess] VPN connected to France — IP: 155.133.65.38
[2026-03-30 00:51:12,303: INFO/MainProcess] VPN rotation successful → France
[2026-03-30 00:51:12,304: INFO/MainProcess] VPN rotated — retrying 2982685e-b5c1-4b7a-851c-7a34c7209076/de with CloudScraper.
[2026-03-30 00:51:15,176: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:51:49,910: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:51:49,910: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-30 00:52:30,582: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579 lang=fr: SUCCESS
[2026-03-30 00:52:30,582: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.3s (base=10.0 jitter=0.3) before 29628e9c-cf8e-48fc-b19e-8d873698c579/pt
[2026-03-30 00:52:43,593: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/bb/leroy.pt-pt.html?lang=pt-pt
[2026-03-30 00:52:43,593: INFO/MainProcess] CloudScraper failed for 29628e9c-cf8e-48fc-b19e-8d873698c579/pt — trying Selenium.
[2026-03-30 00:53:49,108: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-30 00:53:58,618: INFO/MainProcess] Selenium retry 2 -- waiting 12s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:55:25,531: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-30 00:55:35,204: INFO/MainProcess] Selenium retry 3 -- waiting 34s -- https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:57:23,774: WARNING/MainProcess] Selenium language mismatch: requested=de got=es
[2026-03-30 00:57:23,774: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.de.html?lang=de
[2026-03-30 00:57:23,795: WARNING/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 lang=de: FAILED
[2026-03-30 00:57:23,797: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.6s (base=10.0 jitter=3.6) before 2982685e-b5c1-4b7a-851c-7a34c7209076/it
[2026-03-30 00:57:40,071: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 00:57:40,071: INFO/MainProcess] CloudScraper failed for 2982685e-b5c1-4b7a-851c-7a34c7209076/it — trying Selenium.
[2026-03-30 00:58:41,288: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579 lang=pt: SUCCESS
[2026-03-30 00:58:41,291: INFO/MainProcess] URL 29628e9c-cf8e-48fc-b19e-8d873698c579: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 00:58:44,060: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.en-gb.html?lang=en-gb
[2026-03-30 00:58:44,060: INFO/MainProcess] CloudScraper failed for f1613873-d173-4549-bd63-80dab968dc8b/en — trying Selenium.
[2026-03-30 00:59:57,881: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-30 01:00:12,102: INFO/MainProcess] Selenium retry 2 -- waiting 11s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:01:38,082: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-30 01:01:49,461: INFO/MainProcess] Selenium retry 3 -- waiting 25s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:03:28,829: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-30 01:03:28,829: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:03:28,831: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 2982685e-b5c1-4b7a-851c-7a34c7209076/it
[2026-03-30 01:03:28,831: INFO/MainProcess] VPN: rotating (current=FR)...
[2026-03-30 01:03:29,867: INFO/MainProcess] VPN disconnected.
[2026-03-30 01:03:34,868: INFO/MainProcess] VPN: connecting to Spain (ES)...
[2026-03-30 01:03:53,966: INFO/MainProcess] VPN connected to Spain — IP: 77.243.86.58
[2026-03-30 01:03:53,966: INFO/MainProcess] VPN rotation successful → Spain
[2026-03-30 01:03:53,968: INFO/MainProcess] VPN rotated — retrying 2982685e-b5c1-4b7a-851c-7a34c7209076/it with CloudScraper.
[2026-03-30 01:03:56,450: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (2024 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:03:56,451: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-30 01:05:50,772: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 01:05:52,700: INFO/MainProcess] Gallery: 113 images loaded after scroll
[2026-03-30 01:05:56,229: INFO/MainProcess] Gallery: 120 unique image URLs extracted
[2026-03-30 01:05:56,398: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-30 01:05:56,399: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-30 01:06:23,187: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for f1613873-d173-4549-bd63-80dab968dc8b
[2026-03-30 01:06:29,327: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel dfb57dc6-bbb1-4713-b1f9-33d93253dc91
[2026-03-30 01:06:29,328: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel dfb57dc6-bbb1-4713-b1f9-33d93253dc91
[2026-03-30 01:06:29,339: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b lang=en: SUCCESS
[2026-03-30 01:06:29,339: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.5s (base=10.0 jitter=3.5) before f1613873-d173-4549-bd63-80dab968dc8b/es
[2026-03-30 01:06:45,291: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (2024 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.es.html?lang=es
[2026-03-30 01:06:45,291: INFO/MainProcess] CloudScraper failed for f1613873-d173-4549-bd63-80dab968dc8b/es — trying Selenium.
[2026-03-30 01:07:43,292: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-30 01:07:55,182: INFO/MainProcess] Selenium retry 2 -- waiting 20s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:09:30,659: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-30 01:09:41,266: INFO/MainProcess] Selenium retry 3 -- waiting 35s -- https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:11:31,347: WARNING/MainProcess] Selenium language mismatch: requested=it got=es
[2026-03-30 01:11:31,347: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.it.html?lang=it
[2026-03-30 01:11:31,375: WARNING/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 lang=it: FAILED
[2026-03-30 01:11:31,376: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.4s (base=10.0 jitter=4.4) before 2982685e-b5c1-4b7a-851c-7a34c7209076/fr
[2026-03-30 01:11:45,773: WARNING/MainProcess] BUG-LANG-001-FIX: 2 consecutive failures for URL 2982685e-b5c1-4b7a-851c-7a34c7209076 — forcing VPN rotation before fr
[2026-03-30 01:11:45,773: INFO/MainProcess] VPN: rotating (current=ES)...
[2026-03-30 01:11:46,774: INFO/MainProcess] VPN disconnected.
[2026-03-30 01:11:51,775: INFO/MainProcess] VPN: connecting to Sweden (SE)...
[2026-03-30 01:12:10,460: INFO/MainProcess] VPN connected to Sweden — IP: 193.203.13.24
[2026-03-30 01:12:10,460: INFO/MainProcess] VPN rotation successful → Sweden
[2026-03-30 01:12:10,462: INFO/MainProcess] BUG-LANG-001-FIX: VPN rotated (forced) — consecutive_failures reset. Continuing with 2982685e-b5c1-4b7a-851c-7a34c7209076/fr
[2026-03-30 01:12:13,256: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (2024 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:12:13,256: INFO/MainProcess] CloudScraper failed for 2982685e-b5c1-4b7a-851c-7a34c7209076/fr — trying Selenium.
[2026-03-30 01:12:50,408: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b lang=es: SUCCESS
[2026-03-30 01:12:50,408: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.3s (base=10.0 jitter=2.3) before f1613873-d173-4549-bd63-80dab968dc8b/de
[2026-03-30 01:13:05,451: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (2024 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.de.html?lang=de
[2026-03-30 01:13:05,452: INFO/MainProcess] CloudScraper failed for f1613873-d173-4549-bd63-80dab968dc8b/de — trying Selenium.
[2026-03-30 01:14:09,354: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-30 01:14:18,276: INFO/MainProcess] Selenium retry 2 -- waiting 22s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:15:56,132: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-30 01:16:11,106: INFO/MainProcess] Selenium retry 3 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:17:49,369: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-30 01:17:49,370: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:17:49,373: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 2982685e-b5c1-4b7a-851c-7a34c7209076/fr
[2026-03-30 01:17:49,374: INFO/MainProcess] VPN: rotating (current=SE)...
[2026-03-30 01:17:50,476: INFO/MainProcess] VPN disconnected.
[2026-03-30 01:17:55,477: INFO/MainProcess] VPN: connecting to Italy (IT)...
[2026-03-30 01:18:14,420: INFO/MainProcess] VPN connected to Italy — IP: 185.81.127.26
[2026-03-30 01:18:14,420: INFO/MainProcess] VPN rotation successful → Italy
[2026-03-30 01:18:14,424: INFO/MainProcess] VPN rotated — retrying 2982685e-b5c1-4b7a-851c-7a34c7209076/fr with CloudScraper.
[2026-03-30 01:18:17,244: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:18:17,244: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-30 01:19:08,203: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b lang=de: SUCCESS
[2026-03-30 01:19:08,204: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.9s (base=10.0 jitter=2.9) before f1613873-d173-4549-bd63-80dab968dc8b/it
[2026-03-30 01:19:23,829: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.it.html?lang=it
[2026-03-30 01:19:23,829: INFO/MainProcess] CloudScraper failed for f1613873-d173-4549-bd63-80dab968dc8b/it — trying Selenium.
[2026-03-30 01:20:28,088: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-30 01:20:40,078: INFO/MainProcess] Selenium retry 2 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:22:10,764: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-30 01:22:21,228: INFO/MainProcess] Selenium retry 3 -- waiting 29s -- https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:24:04,842: WARNING/MainProcess] Selenium language mismatch: requested=fr got=es
[2026-03-30 01:24:04,842: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.fr.html?lang=fr
[2026-03-30 01:24:04,862: WARNING/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 lang=fr: FAILED
[2026-03-30 01:24:04,863: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.3s (base=10.0 jitter=0.3) before 2982685e-b5c1-4b7a-851c-7a34c7209076/pt
[2026-03-30 01:24:17,915: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:24:17,921: INFO/MainProcess] CloudScraper failed for 2982685e-b5c1-4b7a-851c-7a34c7209076/pt — trying Selenium.
[2026-03-30 01:25:22,772: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b lang=it: SUCCESS
[2026-03-30 01:25:22,772: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.5s (base=10.0 jitter=0.5) before f1613873-d173-4549-bd63-80dab968dc8b/fr
[2026-03-30 01:25:35,993: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.fr.html?lang=fr
[2026-03-30 01:25:35,994: INFO/MainProcess] CloudScraper failed for f1613873-d173-4549-bd63-80dab968dc8b/fr — trying Selenium.
[2026-03-30 01:26:40,593: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-30 01:26:48,646: INFO/MainProcess] Selenium retry 2 -- waiting 12s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:28:15,737: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-30 01:28:25,861: INFO/MainProcess] Selenium retry 3 -- waiting 23s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:30:04,014: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-30 01:30:04,015: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:30:04,017: INFO/MainProcess] VPN rotating (interval=50s elapsed) after failure 2982685e-b5c1-4b7a-851c-7a34c7209076/pt
[2026-03-30 01:30:04,017: INFO/MainProcess] VPN: rotating (current=IT)...
[2026-03-30 01:30:05,028: INFO/MainProcess] VPN disconnected.
[2026-03-30 01:30:10,029: INFO/MainProcess] VPN: connecting to Netherlands (NL)...
[2026-03-30 01:30:29,354: INFO/MainProcess] VPN connected to Netherlands — IP: 89.46.8.130
[2026-03-30 01:30:29,355: INFO/MainProcess] VPN rotation successful → Netherlands
[2026-03-30 01:30:29,356: INFO/MainProcess] VPN rotated — retrying 2982685e-b5c1-4b7a-851c-7a34c7209076/pt with CloudScraper.
[2026-03-30 01:30:32,097: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:31:09,114: ERROR/MainProcess] CloudScraper exhausted retries for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:31:09,115: INFO/MainProcess] CloudScraper still blocked — retrying Selenium after VPN rotate.
[2026-03-30 01:31:22,533: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b lang=fr: SUCCESS
[2026-03-30 01:31:22,534: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.4s (base=10.0 jitter=3.4) before f1613873-d173-4549-bd63-80dab968dc8b/pt
[2026-03-30 01:31:38,687: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/sc/garden-hill-resort-amp-spa.pt-pt.html?lang=pt-pt
[2026-03-30 01:31:38,688: INFO/MainProcess] CloudScraper failed for f1613873-d173-4549-bd63-80dab968dc8b/pt — trying Selenium.
[2026-03-30 01:32:40,108: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-30 01:32:51,096: INFO/MainProcess] Selenium retry 2 -- waiting 10s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:34:16,648: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-30 01:34:27,985: INFO/MainProcess] Selenium retry 3 -- waiting 16s -- https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:35:58,261: WARNING/MainProcess] Selenium language mismatch: requested=pt got=es
[2026-03-30 01:35:58,262: ERROR/MainProcess] Selenium language retries exhausted for https://www.booking.com/hotel/sc/cb-seychelles.pt-pt.html?lang=pt-pt
[2026-03-30 01:35:58,285: WARNING/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 lang=pt: FAILED
[2026-03-30 01:35:58,288: WARNING/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076: PARTIAL — Incomplete: 1/6 languages. OK=['es'] FAILED=['en', 'de', 'it', 'fr', 'pt']
[2026-03-30 01:35:58,293: INFO/MainProcess] URL 2982685e-b5c1-4b7a-851c-7a34c7209076 marked incomplete — data PRESERVED. ok=['es'] fail=['en', 'de', 'it', 'fr', 'pt']
[2026-03-30 01:36:00,946: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.en-gb.html?lang=en-gb
[2026-03-30 01:36:00,946: INFO/MainProcess] CloudScraper failed for aa494df6-fbc8-4156-9058-e5c89700bbf5/en — trying Selenium.
[2026-03-30 01:37:17,404: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b lang=pt: SUCCESS
[2026-03-30 01:37:17,408: INFO/MainProcess] URL f1613873-d173-4549-bd63-80dab968dc8b: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 01:37:20,090: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/atlac-ntico-rio.en-gb.html?lang=en-gb
[2026-03-30 01:37:20,090: INFO/MainProcess] CloudScraper failed for ce4998db-d93c-4620-a032-25d1cc45dbcf/en — trying Selenium.
[2026-03-30 01:39:37,920: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 01:39:39,828: INFO/MainProcess] Gallery: 40 images loaded after scroll
[2026-03-30 01:39:42,033: INFO/MainProcess] Gallery: 47 unique image URLs extracted
[2026-03-30 01:39:42,175: INFO/MainProcess] hotelPhotos JS: 40 photos extracted from page source
[2026-03-30 01:39:42,176: INFO/MainProcess] Gallery: 40 photos with full metadata (hotelPhotos JS)
[2026-03-30 01:40:08,221: INFO/MainProcess] Photos: 40 rich photo records (hotelPhotos JS) for aa494df6-fbc8-4156-9058-e5c89700bbf5
[2026-03-30 01:40:13,824: INFO/MainProcess] download_photo_batch: 120/120 photo-files saved for hotel 78d50167-9a28-4b41-b0fd-c4963a5787da
[2026-03-30 01:40:13,824: INFO/MainProcess] ImageDownloader (photo_batch): 120/40 photos saved for hotel 78d50167-9a28-4b41-b0fd-c4963a5787da
[2026-03-30 01:40:13,830: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5 lang=en: SUCCESS
[2026-03-30 01:40:13,831: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.7s (base=10.0 jitter=4.7) before aa494df6-fbc8-4156-9058-e5c89700bbf5/es
[2026-03-30 01:40:31,223: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.es.html?lang=es
[2026-03-30 01:40:31,224: INFO/MainProcess] CloudScraper failed for aa494df6-fbc8-4156-9058-e5c89700bbf5/es — trying Selenium.
[2026-03-30 01:42:30,098: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 01:42:31,993: INFO/MainProcess] Gallery: 57 images loaded after scroll
[2026-03-30 01:42:33,789: INFO/MainProcess] Gallery: 64 unique image URLs extracted
[2026-03-30 01:42:33,907: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-30 01:42:33,907: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-30 01:43:00,573: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for ce4998db-d93c-4620-a032-25d1cc45dbcf
[2026-03-30 01:43:06,842: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel f63923fc-ecb5-489e-9ab9-af14f473925d
[2026-03-30 01:43:06,842: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel f63923fc-ecb5-489e-9ab9-af14f473925d
[2026-03-30 01:43:06,849: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf lang=en: SUCCESS
[2026-03-30 01:43:06,850: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.5s (base=10.0 jitter=0.5) before ce4998db-d93c-4620-a032-25d1cc45dbcf/es
[2026-03-30 01:43:20,139: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/atlac-ntico-rio.es.html?lang=es
[2026-03-30 01:43:20,140: INFO/MainProcess] CloudScraper failed for ce4998db-d93c-4620-a032-25d1cc45dbcf/es — trying Selenium.
[2026-03-30 01:44:18,641: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5 lang=es: SUCCESS
[2026-03-30 01:44:18,642: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.9s (base=10.0 jitter=4.9) before aa494df6-fbc8-4156-9058-e5c89700bbf5/de
[2026-03-30 01:44:36,269: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.de.html?lang=de
[2026-03-30 01:44:36,269: INFO/MainProcess] CloudScraper failed for aa494df6-fbc8-4156-9058-e5c89700bbf5/de — trying Selenium.
[2026-03-30 01:45:37,575: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf lang=es: SUCCESS
[2026-03-30 01:45:37,576: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 11.8s (base=10.0 jitter=1.8) before ce4998db-d93c-4620-a032-25d1cc45dbcf/de
[2026-03-30 01:45:52,093: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-30 01:46:32,120: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-30 01:46:36,784: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/atlac-ntico-rio.de.html?lang=de
[2026-03-30 01:46:36,784: INFO/MainProcess] CloudScraper failed for ce4998db-d93c-4620-a032-25d1cc45dbcf/de — trying Selenium.
[2026-03-30 01:46:56,911: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5 lang=de: SUCCESS
[2026-03-30 01:46:56,911: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.1s (base=10.0 jitter=0.1) before aa494df6-fbc8-4156-9058-e5c89700bbf5/it
[2026-03-30 01:47:09,740: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.it.html?lang=it
[2026-03-30 01:47:09,741: INFO/MainProcess] CloudScraper failed for aa494df6-fbc8-4156-9058-e5c89700bbf5/it — trying Selenium.
[2026-03-30 01:48:28,350: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf lang=de: SUCCESS
[2026-03-30 01:48:28,350: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.2s (base=10.0 jitter=2.2) before ce4998db-d93c-4620-a032-25d1cc45dbcf/it
[2026-03-30 01:48:43,155: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/atlac-ntico-rio.it.html?lang=it
[2026-03-30 01:48:43,156: INFO/MainProcess] CloudScraper failed for ce4998db-d93c-4620-a032-25d1cc45dbcf/it — trying Selenium.
[2026-03-30 01:49:46,942: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5 lang=it: SUCCESS
[2026-03-30 01:49:46,942: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.0s (base=10.0 jitter=2.0) before aa494df6-fbc8-4156-9058-e5c89700bbf5/fr
[2026-03-30 01:50:01,628: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.fr.html?lang=fr
[2026-03-30 01:50:01,628: INFO/MainProcess] CloudScraper failed for aa494df6-fbc8-4156-9058-e5c89700bbf5/fr — trying Selenium.
[2026-03-30 01:51:04,016: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf lang=it: SUCCESS
[2026-03-30 01:51:04,016: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.9s (base=10.0 jitter=0.9) before ce4998db-d93c-4620-a032-25d1cc45dbcf/fr
[2026-03-30 01:51:17,638: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-30 01:51:43,188: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-30 01:51:48,336: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/atlac-ntico-rio.fr.html?lang=fr
[2026-03-30 01:51:48,337: INFO/MainProcess] CloudScraper failed for ce4998db-d93c-4620-a032-25d1cc45dbcf/fr — trying Selenium.
[2026-03-30 01:52:22,965: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5 lang=fr: SUCCESS
[2026-03-30 01:52:22,965: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.4s (base=10.0 jitter=3.4) before aa494df6-fbc8-4156-9058-e5c89700bbf5/pt
[2026-03-30 01:52:39,122: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/uy/golden-beach-resort-spa.pt-pt.html?lang=pt-pt
[2026-03-30 01:52:39,122: INFO/MainProcess] CloudScraper failed for aa494df6-fbc8-4156-9058-e5c89700bbf5/pt — trying Selenium.
[2026-03-30 01:53:55,942: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf lang=fr: SUCCESS
[2026-03-30 01:53:55,943: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 11.2s (base=10.0 jitter=1.2) before ce4998db-d93c-4620-a032-25d1cc45dbcf/pt
[2026-03-30 01:54:09,929: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/atlac-ntico-rio.pt-pt.html?lang=pt-pt
[2026-03-30 01:54:09,929: INFO/MainProcess] CloudScraper failed for ce4998db-d93c-4620-a032-25d1cc45dbcf/pt — trying Selenium.
[2026-03-30 01:55:14,276: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5 lang=pt: SUCCESS
[2026-03-30 01:55:14,278: INFO/MainProcess] URL aa494df6-fbc8-4156-9058-e5c89700bbf5: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 01:55:17,108: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/colonna-park.en-gb.html?lang=en-gb
[2026-03-30 01:55:17,108: INFO/MainProcess] CloudScraper failed for 851db3af-d710-4c37-a21e-af098178f7ff/en — trying Selenium.
[2026-03-30 01:56:33,213: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf lang=pt: SUCCESS
[2026-03-30 01:56:33,216: INFO/MainProcess] URL ce4998db-d93c-4620-a032-25d1cc45dbcf: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 01:56:35,819: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.en-gb.html?lang=en-gb
[2026-03-30 01:56:35,819: INFO/MainProcess] CloudScraper failed for 82f04a25-996b-4050-a529-a796746ca340/en — trying Selenium.
[2026-03-30 01:58:54,209: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 01:58:56,123: INFO/MainProcess] Gallery: 70 images loaded after scroll
[2026-03-30 01:58:58,910: INFO/MainProcess] Gallery: 77 unique image URLs extracted
[2026-03-30 01:58:59,071: INFO/MainProcess] hotelPhotos JS: 45 photos extracted from page source
[2026-03-30 01:58:59,072: INFO/MainProcess] Gallery: 45 photos with full metadata (hotelPhotos JS)
[2026-03-30 01:59:25,237: INFO/MainProcess] Photos: 45 rich photo records (hotelPhotos JS) for 851db3af-d710-4c37-a21e-af098178f7ff
[2026-03-30 01:59:32,121: INFO/MainProcess] download_photo_batch: 135/135 photo-files saved for hotel 4d959712-f8b5-4c70-96e6-cc488edb9c93
[2026-03-30 01:59:32,121: INFO/MainProcess] ImageDownloader (photo_batch): 135/45 photos saved for hotel 4d959712-f8b5-4c70-96e6-cc488edb9c93
[2026-03-30 01:59:32,130: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff lang=en: SUCCESS
[2026-03-30 01:59:32,131: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.5s (base=10.0 jitter=3.5) before 851db3af-d710-4c37-a21e-af098178f7ff/es
[2026-03-30 01:59:48,331: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/colonna-park.es.html?lang=es
[2026-03-30 01:59:48,332: INFO/MainProcess] CloudScraper failed for 851db3af-d710-4c37-a21e-af098178f7ff/es — trying Selenium.
[2026-03-30 02:01:46,869: INFO/MainProcess] Gallery opened via: img[src*='bstatic.com/xdata/images/hotel/']
[2026-03-30 02:01:48,765: INFO/MainProcess] Gallery: 34 images loaded after scroll
[2026-03-30 02:01:51,078: INFO/MainProcess] Gallery: 41 unique image URLs extracted
[2026-03-30 02:01:51,182: INFO/MainProcess] hotelPhotos JS: 34 photos extracted from page source
[2026-03-30 02:01:51,182: INFO/MainProcess] Gallery: 34 photos with full metadata (hotelPhotos JS)
[2026-03-30 02:02:17,529: INFO/MainProcess] Photos: 34 rich photo records (hotelPhotos JS) for 82f04a25-996b-4050-a529-a796746ca340
[2026-03-30 02:02:23,349: INFO/MainProcess] download_photo_batch: 102/102 photo-files saved for hotel 44a8cf23-65f5-46eb-9926-eea4776bfb26
[2026-03-30 02:02:23,349: INFO/MainProcess] ImageDownloader (photo_batch): 102/34 photos saved for hotel 44a8cf23-65f5-46eb-9926-eea4776bfb26
[2026-03-30 02:02:23,355: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340 lang=en: SUCCESS
[2026-03-30 02:02:23,355: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.3s (base=10.0 jitter=2.3) before 82f04a25-996b-4050-a529-a796746ca340/es
[2026-03-30 02:02:38,390: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.es.html?lang=es
[2026-03-30 02:02:38,391: INFO/MainProcess] CloudScraper failed for 82f04a25-996b-4050-a529-a796746ca340/es — trying Selenium.
[2026-03-30 02:03:37,234: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff lang=es: SUCCESS
[2026-03-30 02:03:37,235: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.3s (base=10.0 jitter=3.3) before 851db3af-d710-4c37-a21e-af098178f7ff/de
[2026-03-30 02:03:53,129: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/colonna-park.de.html?lang=de
[2026-03-30 02:03:53,129: INFO/MainProcess] CloudScraper failed for 851db3af-d710-4c37-a21e-af098178f7ff/de — trying Selenium.
[2026-03-30 02:04:56,581: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340 lang=es: SUCCESS
[2026-03-30 02:04:56,581: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.2s (base=10.0 jitter=0.2) before 82f04a25-996b-4050-a529-a796746ca340/de
[2026-03-30 02:05:09,416: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.de.html?lang=de
[2026-03-30 02:05:09,416: INFO/MainProcess] CloudScraper failed for 82f04a25-996b-4050-a529-a796746ca340/de — trying Selenium.
[2026-03-30 02:06:14,642: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff lang=de: SUCCESS
[2026-03-30 02:06:14,642: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.9s (base=10.0 jitter=2.9) before 851db3af-d710-4c37-a21e-af098178f7ff/it
[2026-03-30 02:06:30,254: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/colonna-park.it.html?lang=it
[2026-03-30 02:06:30,254: INFO/MainProcess] CloudScraper failed for 851db3af-d710-4c37-a21e-af098178f7ff/it — trying Selenium.
[2026-03-30 02:07:45,616: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340 lang=de: SUCCESS
[2026-03-30 02:07:45,616: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.8s (base=10.0 jitter=2.8) before 82f04a25-996b-4050-a529-a796746ca340/it
[2026-03-30 02:08:01,133: WARNING/MainProcess] Block detected attempt 1 for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-30 02:08:32,598: INFO/MainProcess] CloudScraper retry 2/3 — waiting 4.0s — https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-30 02:08:37,322: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.it.html?lang=it
[2026-03-30 02:08:37,322: INFO/MainProcess] CloudScraper failed for 82f04a25-996b-4050-a529-a796746ca340/it — trying Selenium.
[2026-03-30 02:09:02,501: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff lang=it: SUCCESS
[2026-03-30 02:09:02,501: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 10.1s (base=10.0 jitter=0.1) before 851db3af-d710-4c37-a21e-af098178f7ff/fr
[2026-03-30 02:09:15,293: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/colonna-park.fr.html?lang=fr
[2026-03-30 02:09:15,293: INFO/MainProcess] CloudScraper failed for 851db3af-d710-4c37-a21e-af098178f7ff/fr — trying Selenium.
[2026-03-30 02:10:20,918: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340 lang=it: SUCCESS
[2026-03-30 02:10:20,918: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 13.5s (base=10.0 jitter=3.5) before 82f04a25-996b-4050-a529-a796746ca340/fr
[2026-03-30 02:10:37,107: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.fr.html?lang=fr
[2026-03-30 02:10:37,107: INFO/MainProcess] CloudScraper failed for 82f04a25-996b-4050-a529-a796746ca340/fr — trying Selenium.
[2026-03-30 02:11:38,063: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff lang=fr: SUCCESS
[2026-03-30 02:11:38,063: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 12.1s (base=10.0 jitter=2.1) before 851db3af-d710-4c37-a21e-af098178f7ff/pt
[2026-03-30 02:11:52,797: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/colonna-park.pt-pt.html?lang=pt-pt
[2026-03-30 02:11:52,797: INFO/MainProcess] CloudScraper failed for 851db3af-d710-4c37-a21e-af098178f7ff/pt — trying Selenium.
[2026-03-30 02:13:09,115: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340 lang=fr: SUCCESS
[2026-03-30 02:13:09,116: INFO/MainProcess] BUG-LANG-001-FIX: inter-language delay 14.0s (base=10.0 jitter=4.0) before 82f04a25-996b-4050-a529-a796746ca340/pt
[2026-03-30 02:13:25,794: WARNING/MainProcess] BUG-LANG-001-FIX: Short HTML (3962 bytes) — block page detected, skipping remaining retries for https://www.booking.com/hotel/br/manaus-hoteis-millennium.pt-pt.html?lang=pt-pt
[2026-03-30 02:13:25,794: INFO/MainProcess] CloudScraper failed for 82f04a25-996b-4050-a529-a796746ca340/pt — trying Selenium.
[2026-03-30 02:14:27,363: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff lang=pt: SUCCESS
[2026-03-30 02:14:27,366: INFO/MainProcess] URL 851db3af-d710-4c37-a21e-af098178f7ff: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 02:15:43,847: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340 lang=pt: SUCCESS
[2026-03-30 02:15:43,849: INFO/MainProcess] URL 82f04a25-996b-4050-a529-a796746ca340: COMPLETE (6/6) langs=['en', 'es', 'de', 'it', 'fr', 'pt']
[2026-03-30 02:15:46,101: INFO/MainProcess] Selenium browser closed after batch completion.
[2026-03-30 02:15:46,102: INFO/MainProcess] scrape_pending_urls: batch complete — {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-30 02:15:46,104: INFO/MainProcess] Task tasks.scrape_pending_urls[47946296-0fae-4710-a9ec-b900643ad95f] succeeded in 10018.103475300013s: {'processed': 13, 'succeeded': 12, 'failed': 1, 'skipped': 0, 'status': 'complete', 'pending_before': 13, 'trigger': 'auto_beat_30s'}
[2026-03-30 02:15:46,360: INFO/MainProcess] Task tasks.purge_old_debug_html[1b078754-16e7-4a7b-bb6d-85f038407c65] received
[2026-03-30 02:15:46,361: INFO/MainProcess] Task tasks.purge_old_debug_html[1b078754-16e7-4a7b-bb6d-85f038407c65] succeeded in 0.0014593000523746014s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 02:15:46,363: INFO/MainProcess] Task tasks.collect_system_metrics[5547d4b0-cd94-47ff-be3c-7bd574d40661] received
[2026-03-30 02:15:46,880: INFO/MainProcess] Task tasks.collect_system_metrics[5547d4b0-cd94-47ff-be3c-7bd574d40661] succeeded in 0.5172287999885157s: {'cpu': 20.0, 'memory': 45.8}
[2026-03-30 02:15:46,882: INFO/MainProcess] Task tasks.scrape_pending_urls[5b52c3c6-6d53-4d7a-b032-90d33ce44780] received
[2026-03-30 02:15:46,886: INFO/MainProcess] Task tasks.scrape_pending_urls[5b52c3c6-6d53-4d7a-b032-90d33ce44780] succeeded in 0.00280930008739233s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:46,887: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d55286ec-18b6-4d1c-a8f3-323b6fd12cce] received
[2026-03-30 02:15:46,890: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:15:46,891: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d55286ec-18b6-4d1c-a8f3-323b6fd12cce] succeeded in 0.003514499985612929s: {'reset': 0}
[2026-03-30 02:15:46,892: INFO/MainProcess] Task tasks.collect_system_metrics[ac92c40c-a08e-4a02-91b0-82433f531548] received
[2026-03-30 02:15:47,409: INFO/MainProcess] Task tasks.collect_system_metrics[ac92c40c-a08e-4a02-91b0-82433f531548] succeeded in 0.5161628000205383s: {'cpu': 13.4, 'memory': 45.8}
[2026-03-30 02:15:47,410: INFO/MainProcess] Task tasks.scrape_pending_urls[81ddd5f3-8f9b-4020-ac05-83b30955bc4b] received
[2026-03-30 02:15:47,413: INFO/MainProcess] Task tasks.scrape_pending_urls[81ddd5f3-8f9b-4020-ac05-83b30955bc4b] succeeded in 0.002859200001694262s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:47,415: INFO/MainProcess] Task tasks.reset_stale_processing_urls[30020711-10b0-4b9d-8d28-0a1267186f02] received
[2026-03-30 02:15:47,417: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:15:47,418: INFO/MainProcess] Task tasks.reset_stale_processing_urls[30020711-10b0-4b9d-8d28-0a1267186f02] succeeded in 0.0028144000098109245s: {'reset': 0}
[2026-03-30 02:15:47,419: INFO/MainProcess] Task tasks.collect_system_metrics[c2062f8c-2fe7-4efe-89c9-d762c516ebe3] received
[2026-03-30 02:15:47,938: INFO/MainProcess] Task tasks.collect_system_metrics[c2062f8c-2fe7-4efe-89c9-d762c516ebe3] succeeded in 0.5170025000115857s: {'cpu': 5.1, 'memory': 45.8}
[2026-03-30 02:15:47,939: INFO/MainProcess] Task tasks.scrape_pending_urls[c1db3352-24f2-46fd-80a6-c1a7d5a329c2] received
[2026-03-30 02:15:47,943: INFO/MainProcess] Task tasks.scrape_pending_urls[c1db3352-24f2-46fd-80a6-c1a7d5a329c2] succeeded in 0.003046099911443889s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:47,944: INFO/MainProcess] Task tasks.purge_old_debug_html[7e20594b-29b7-48f7-8288-b5836fa43a45] received
[2026-03-30 02:15:47,946: INFO/MainProcess] Task tasks.purge_old_debug_html[7e20594b-29b7-48f7-8288-b5836fa43a45] succeeded in 0.00091409997548908s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 02:15:47,947: INFO/MainProcess] Task tasks.collect_system_metrics[c0333dc8-3c67-468c-8443-eecb373c2d7d] received
[2026-03-30 02:15:48,464: INFO/MainProcess] Task tasks.collect_system_metrics[c0333dc8-3c67-468c-8443-eecb373c2d7d] succeeded in 0.516794899944216s: {'cpu': 6.6, 'memory': 45.8}
[2026-03-30 02:15:48,466: INFO/MainProcess] Task tasks.scrape_pending_urls[aae7a22a-c11d-400d-ab01-cf7db8be6276] received
[2026-03-30 02:15:48,469: INFO/MainProcess] Task tasks.scrape_pending_urls[aae7a22a-c11d-400d-ab01-cf7db8be6276] succeeded in 0.0028298000106588006s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:48,470: INFO/MainProcess] Task tasks.reset_stale_processing_urls[5cd0bbae-1894-40b4-a887-c4db74884b1f] received
[2026-03-30 02:15:48,473: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:15:48,474: INFO/MainProcess] Task tasks.reset_stale_processing_urls[5cd0bbae-1894-40b4-a887-c4db74884b1f] succeeded in 0.0030136998975649476s: {'reset': 0}
[2026-03-30 02:15:48,475: INFO/MainProcess] Task tasks.collect_system_metrics[55898902-afaf-489d-8cae-eb0f7e48bd79] received
[2026-03-30 02:15:48,993: INFO/MainProcess] Task tasks.collect_system_metrics[55898902-afaf-489d-8cae-eb0f7e48bd79] succeeded in 0.5176713999826461s: {'cpu': 4.7, 'memory': 45.8}
[2026-03-30 02:15:48,995: INFO/MainProcess] Task tasks.scrape_pending_urls[2db3e0e7-2a9f-4627-8e19-084fbfbbdb0e] received
[2026-03-30 02:15:48,998: INFO/MainProcess] Task tasks.scrape_pending_urls[2db3e0e7-2a9f-4627-8e19-084fbfbbdb0e] succeeded in 0.002327099908143282s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:48,999: INFO/MainProcess] Task tasks.ensure_log_partitions[3d938e5c-1cae-4614-9cd4-889d5f78d0af] received
[2026-03-30 02:15:49,016: INFO/MainProcess] Task tasks.ensure_log_partitions[3d938e5c-1cae-4614-9cd4-889d5f78d0af] succeeded in 0.016454899916425347s: {'created': [], 'skipped': ['scraping_logs_2026_03', 'scraping_logs_2026_04', 'scraping_logs_2026_05'], 'errors': []}
[2026-03-30 02:15:49,018: INFO/MainProcess] Task tasks.collect_system_metrics[35b27437-71f1-48dd-bea6-330935e209ba] received
[2026-03-30 02:15:49,525: INFO/MainProcess] Task tasks.collect_system_metrics[35b27437-71f1-48dd-bea6-330935e209ba] succeeded in 0.5069308000383899s: {'cpu': 14.8, 'memory': 45.7}
[2026-03-30 02:15:49,527: INFO/MainProcess] Task tasks.scrape_pending_urls[70a080ce-67dc-4f9b-bf0f-65916ee4121f] received
[2026-03-30 02:15:49,530: INFO/MainProcess] Task tasks.scrape_pending_urls[70a080ce-67dc-4f9b-bf0f-65916ee4121f] succeeded in 0.002830500015988946s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:49,531: INFO/MainProcess] Task tasks.reset_stale_processing_urls[bcc760cb-4627-4108-9fe0-baee5d6cf871] received
[2026-03-30 02:15:49,534: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:15:49,536: INFO/MainProcess] Task tasks.reset_stale_processing_urls[bcc760cb-4627-4108-9fe0-baee5d6cf871] succeeded in 0.004245300078764558s: {'reset': 0}
[2026-03-30 02:15:49,538: INFO/MainProcess] Task tasks.collect_system_metrics[a9da39f2-e604-45f3-ba5c-4d23b5ef670a] received
[2026-03-30 02:15:50,055: INFO/MainProcess] Task tasks.collect_system_metrics[a9da39f2-e604-45f3-ba5c-4d23b5ef670a] succeeded in 0.5171176999574527s: {'cpu': 3.2, 'memory': 45.9}
[2026-03-30 02:15:50,057: INFO/MainProcess] Task tasks.scrape_pending_urls[05a628cf-2e61-444d-8e0e-910a52652799] received
[2026-03-30 02:15:50,060: INFO/MainProcess] Task tasks.scrape_pending_urls[05a628cf-2e61-444d-8e0e-910a52652799] succeeded in 0.0023566000163555145s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:50,061: INFO/MainProcess] Task tasks.purge_old_debug_html[5a65614c-4aef-43a7-9755-d0fc7b5eac06] received
[2026-03-30 02:15:50,062: INFO/MainProcess] Task tasks.purge_old_debug_html[5a65614c-4aef-43a7-9755-d0fc7b5eac06] succeeded in 0.0009129999671131372s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 02:15:50,064: INFO/MainProcess] Task tasks.collect_system_metrics[c14af5f0-67d5-4f25-aac8-9033e363c3ca] received
[2026-03-30 02:15:50,582: INFO/MainProcess] Task tasks.collect_system_metrics[c14af5f0-67d5-4f25-aac8-9033e363c3ca] succeeded in 0.5176358999451622s: {'cpu': 4.4, 'memory': 45.9}
[2026-03-30 02:15:50,584: INFO/MainProcess] Task tasks.scrape_pending_urls[f6cfb43a-05ce-4e22-bc04-88c771933328] received
[2026-03-30 02:15:50,587: INFO/MainProcess] Task tasks.scrape_pending_urls[f6cfb43a-05ce-4e22-bc04-88c771933328] succeeded in 0.002815700019709766s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:50,588: INFO/MainProcess] Task tasks.reset_stale_processing_urls[fbf56879-bfa3-4125-a3ed-a0ff79e8efa4] received
[2026-03-30 02:15:50,590: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:15:50,591: INFO/MainProcess] Task tasks.reset_stale_processing_urls[fbf56879-bfa3-4125-a3ed-a0ff79e8efa4] succeeded in 0.002796199987642467s: {'reset': 0}
[2026-03-30 02:15:50,593: INFO/MainProcess] Task tasks.collect_system_metrics[9f831bf8-96ac-4785-9890-7f2813d0a227] received
[2026-03-30 02:15:51,110: INFO/MainProcess] Task tasks.collect_system_metrics[9f831bf8-96ac-4785-9890-7f2813d0a227] succeeded in 0.5170202000299469s: {'cpu': 7.0, 'memory': 45.8}
[2026-03-30 02:15:51,112: INFO/MainProcess] Task tasks.scrape_pending_urls[b16fd37a-7b6c-406f-9a84-c0aed59c543f] received
[2026-03-30 02:15:51,115: INFO/MainProcess] Task tasks.scrape_pending_urls[b16fd37a-7b6c-406f-9a84-c0aed59c543f] succeeded in 0.0028147000120952725s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:51,116: INFO/MainProcess] Task tasks.collect_system_metrics[36a0c280-3cfc-432c-ad1d-4791513426f0] received
[2026-03-30 02:15:51,634: INFO/MainProcess] Task tasks.collect_system_metrics[36a0c280-3cfc-432c-ad1d-4791513426f0] succeeded in 0.517835000064224s: {'cpu': 7.5, 'memory': 45.8}
[2026-03-30 02:15:51,637: INFO/MainProcess] Task tasks.scrape_pending_urls[82c5c1da-7499-47c6-98fe-5ebb38251207] received
[2026-03-30 02:15:51,640: INFO/MainProcess] Task tasks.scrape_pending_urls[82c5c1da-7499-47c6-98fe-5ebb38251207] succeeded in 0.0024164000060409307s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:51,641: INFO/MainProcess] Task tasks.collect_system_metrics[9d8530c4-027b-4334-92d0-43ee7c12ebaa] received
[2026-03-30 02:15:52,158: INFO/MainProcess] Task tasks.collect_system_metrics[9d8530c4-027b-4334-92d0-43ee7c12ebaa] succeeded in 0.5161068999441341s: {'cpu': 1.6, 'memory': 45.8}
[2026-03-30 02:15:52,159: INFO/MainProcess] Task tasks.scrape_pending_urls[084a8950-2fe7-4f3f-8556-15b4b9f6b0dd] received
[2026-03-30 02:15:52,162: INFO/MainProcess] Task tasks.scrape_pending_urls[084a8950-2fe7-4f3f-8556-15b4b9f6b0dd] succeeded in 0.0027372000040486455s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:52,164: INFO/MainProcess] Task tasks.collect_system_metrics[bea5a5df-15ff-4244-b0b1-431ea8185eb5] received
[2026-03-30 02:15:52,681: INFO/MainProcess] Task tasks.collect_system_metrics[bea5a5df-15ff-4244-b0b1-431ea8185eb5] succeeded in 0.5159358000382781s: {'cpu': 7.1, 'memory': 45.8}
[2026-03-30 02:15:52,682: INFO/MainProcess] Task tasks.scrape_pending_urls[38dbb8ef-ef95-41e1-a0ce-4857f34141f0] received
[2026-03-30 02:15:52,685: INFO/MainProcess] Task tasks.scrape_pending_urls[38dbb8ef-ef95-41e1-a0ce-4857f34141f0] succeeded in 0.002198799978941679s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:52,686: INFO/MainProcess] Task tasks.collect_system_metrics[2880c120-7e2d-4b67-a31c-1ef00a985751] received
[2026-03-30 02:15:53,203: INFO/MainProcess] Task tasks.collect_system_metrics[2880c120-7e2d-4b67-a31c-1ef00a985751] succeeded in 0.5161829000571743s: {'cpu': 3.9, 'memory': 45.8}
[2026-03-30 02:15:53,205: INFO/MainProcess] Task tasks.scrape_pending_urls[eb625004-b3f2-4d29-9ecd-3f24c714eee1] received
[2026-03-30 02:15:53,208: INFO/MainProcess] Task tasks.scrape_pending_urls[eb625004-b3f2-4d29-9ecd-3f24c714eee1] succeeded in 0.0031630999874323606s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:53,210: INFO/MainProcess] Task tasks.collect_system_metrics[ab102144-6d90-43d8-a0b6-88ca06ecb52b] received
[2026-03-30 02:15:53,726: INFO/MainProcess] Task tasks.collect_system_metrics[ab102144-6d90-43d8-a0b6-88ca06ecb52b] succeeded in 0.5163239000830799s: {'cpu': 6.3, 'memory': 45.8}
[2026-03-30 02:15:53,728: INFO/MainProcess] Task tasks.scrape_pending_urls[673a6683-d1b3-4ab3-9216-8f8b9dfe542a] received
[2026-03-30 02:15:53,730: INFO/MainProcess] Task tasks.scrape_pending_urls[673a6683-d1b3-4ab3-9216-8f8b9dfe542a] succeeded in 0.002198499976657331s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:53,732: INFO/MainProcess] Task tasks.collect_system_metrics[77a75168-5e33-4b7f-ae91-c815826653aa] received
[2026-03-30 02:15:54,250: INFO/MainProcess] Task tasks.collect_system_metrics[77a75168-5e33-4b7f-ae91-c815826653aa] succeeded in 0.5175400000298396s: {'cpu': 8.1, 'memory': 45.8}
[2026-03-30 02:15:54,251: INFO/MainProcess] Task tasks.scrape_pending_urls[865d3873-85c3-4ade-920e-fac0ba966997] received
[2026-03-30 02:15:54,254: INFO/MainProcess] Task tasks.scrape_pending_urls[865d3873-85c3-4ade-920e-fac0ba966997] succeeded in 0.0026483999099582434s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:54,256: INFO/MainProcess] Task tasks.collect_system_metrics[2965fb9b-3cb7-492a-8004-9eb4607c1f91] received
[2026-03-30 02:15:54,772: INFO/MainProcess] Task tasks.collect_system_metrics[2965fb9b-3cb7-492a-8004-9eb4607c1f91] succeeded in 0.5162387000164017s: {'cpu': 16.3, 'memory': 45.7}
[2026-03-30 02:15:54,774: INFO/MainProcess] Task tasks.scrape_pending_urls[e0b9dd59-bdf3-457c-9ca1-6f8ec76041dc] received
[2026-03-30 02:15:54,777: INFO/MainProcess] Task tasks.scrape_pending_urls[e0b9dd59-bdf3-457c-9ca1-6f8ec76041dc] succeeded in 0.0024575000861659646s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:54,779: INFO/MainProcess] Task tasks.collect_system_metrics[635d66b6-7478-4b53-be8f-284c07ada9cd] received
[2026-03-30 02:15:55,295: INFO/MainProcess] Task tasks.collect_system_metrics[635d66b6-7478-4b53-be8f-284c07ada9cd] succeeded in 0.5165155000286177s: {'cpu': 6.2, 'memory': 45.7}
[2026-03-30 02:15:55,297: INFO/MainProcess] Task tasks.scrape_pending_urls[a829c4fa-f8b8-45b4-846a-0fa661314ab0] received
[2026-03-30 02:15:55,300: INFO/MainProcess] Task tasks.scrape_pending_urls[a829c4fa-f8b8-45b4-846a-0fa661314ab0] succeeded in 0.0026788999093696475s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:55,302: INFO/MainProcess] Task tasks.collect_system_metrics[aa89de6b-e3f1-43f0-b4c4-a820a295d453] received
[2026-03-30 02:15:55,819: INFO/MainProcess] Task tasks.collect_system_metrics[aa89de6b-e3f1-43f0-b4c4-a820a295d453] succeeded in 0.51708779996261s: {'cpu': 5.8, 'memory': 45.7}
[2026-03-30 02:15:55,821: INFO/MainProcess] Task tasks.scrape_pending_urls[bda789d6-850f-48a0-9cf0-07ef2dcc7d98] received
[2026-03-30 02:15:55,823: INFO/MainProcess] Task tasks.scrape_pending_urls[bda789d6-850f-48a0-9cf0-07ef2dcc7d98] succeeded in 0.002190300030633807s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:55,825: INFO/MainProcess] Task tasks.collect_system_metrics[eec9024c-875b-4276-8ed1-310a55a541b4] received
[2026-03-30 02:15:56,330: INFO/MainProcess] Task tasks.collect_system_metrics[eec9024c-875b-4276-8ed1-310a55a541b4] succeeded in 0.5050760000012815s: {'cpu': 9.3, 'memory': 45.5}
[2026-03-30 02:15:56,332: INFO/MainProcess] Task tasks.scrape_pending_urls[28815a0a-1ae7-42f1-8697-f1949fb1821e] received
[2026-03-30 02:15:56,335: INFO/MainProcess] Task tasks.scrape_pending_urls[28815a0a-1ae7-42f1-8697-f1949fb1821e] succeeded in 0.002635000040754676s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:56,336: INFO/MainProcess] Task tasks.collect_system_metrics[bf9c7e03-8b1e-4dd7-afd7-baf36ee92643] received
[2026-03-30 02:15:56,853: INFO/MainProcess] Task tasks.collect_system_metrics[bf9c7e03-8b1e-4dd7-afd7-baf36ee92643] succeeded in 0.5159507999196649s: {'cpu': 0.8, 'memory': 45.5}
[2026-03-30 02:15:56,854: INFO/MainProcess] Task tasks.scrape_pending_urls[37b400c1-d959-4785-8deb-112971930c39] received
[2026-03-30 02:15:56,857: INFO/MainProcess] Task tasks.scrape_pending_urls[37b400c1-d959-4785-8deb-112971930c39] succeeded in 0.0022006999934092164s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:56,858: INFO/MainProcess] Task tasks.collect_system_metrics[fda34529-e2b9-46bd-8a9f-f6a718cec013] received
[2026-03-30 02:15:57,374: INFO/MainProcess] Task tasks.collect_system_metrics[fda34529-e2b9-46bd-8a9f-f6a718cec013] succeeded in 0.5159263999667019s: {'cpu': 5.7, 'memory': 45.5}
[2026-03-30 02:15:57,376: INFO/MainProcess] Task tasks.scrape_pending_urls[e5f5aa6e-6327-42c8-a8fb-027526f498e0] received
[2026-03-30 02:15:57,379: INFO/MainProcess] Task tasks.scrape_pending_urls[e5f5aa6e-6327-42c8-a8fb-027526f498e0] succeeded in 0.0027262000367045403s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:57,380: INFO/MainProcess] Task tasks.collect_system_metrics[00e878a3-2b5f-4cd3-8e04-f6d61887b7c0] received
[2026-03-30 02:15:57,897: INFO/MainProcess] Task tasks.collect_system_metrics[00e878a3-2b5f-4cd3-8e04-f6d61887b7c0] succeeded in 0.5160285000456497s: {'cpu': 7.1, 'memory': 45.5}
[2026-03-30 02:15:57,898: INFO/MainProcess] Task tasks.scrape_pending_urls[32b954a8-83fb-47af-bad0-e7387aa30b95] received
[2026-03-30 02:15:57,901: INFO/MainProcess] Task tasks.scrape_pending_urls[32b954a8-83fb-47af-bad0-e7387aa30b95] succeeded in 0.0021777000511065125s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:57,903: INFO/MainProcess] Task tasks.collect_system_metrics[cfc29712-0f9b-462f-8b88-e1b5b642957e] received
[2026-03-30 02:15:58,420: INFO/MainProcess] Task tasks.collect_system_metrics[cfc29712-0f9b-462f-8b88-e1b5b642957e] succeeded in 0.5166389999212697s: {'cpu': 5.1, 'memory': 45.5}
[2026-03-30 02:15:58,421: INFO/MainProcess] Task tasks.scrape_pending_urls[1685a2fe-0933-4775-9948-70c4aee8657f] received
[2026-03-30 02:15:58,424: INFO/MainProcess] Task tasks.scrape_pending_urls[1685a2fe-0933-4775-9948-70c4aee8657f] succeeded in 0.0026928000152111053s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:58,426: INFO/MainProcess] Task tasks.collect_system_metrics[4c757938-d2ab-453e-b2f7-47b26c40ab7f] received
[2026-03-30 02:15:58,943: INFO/MainProcess] Task tasks.collect_system_metrics[4c757938-d2ab-453e-b2f7-47b26c40ab7f] succeeded in 0.5164886000566185s: {'cpu': 4.0, 'memory': 45.5}
[2026-03-30 02:15:58,944: INFO/MainProcess] Task tasks.scrape_pending_urls[d1835d6d-111e-4272-b8e2-817a34e32480] received
[2026-03-30 02:15:58,948: INFO/MainProcess] Task tasks.scrape_pending_urls[d1835d6d-111e-4272-b8e2-817a34e32480] succeeded in 0.003220799961127341s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:58,949: INFO/MainProcess] Task tasks.collect_system_metrics[d0df7311-cb55-421f-8e2a-b1c411c7bc8e] received
[2026-03-30 02:15:59,466: INFO/MainProcess] Task tasks.collect_system_metrics[d0df7311-cb55-421f-8e2a-b1c411c7bc8e] succeeded in 0.5168739999644458s: {'cpu': 8.6, 'memory': 45.4}
[2026-03-30 02:15:59,468: INFO/MainProcess] Task tasks.scrape_pending_urls[0b390a3b-e162-4323-8479-e273f18c6b6c] received
[2026-03-30 02:15:59,472: INFO/MainProcess] Task tasks.scrape_pending_urls[0b390a3b-e162-4323-8479-e273f18c6b6c] succeeded in 0.003445600043050945s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:59,474: INFO/MainProcess] Task tasks.collect_system_metrics[b03afa70-a58f-4818-a847-cd40c7fd7a7d] received
[2026-03-30 02:15:59,991: INFO/MainProcess] Task tasks.collect_system_metrics[b03afa70-a58f-4818-a847-cd40c7fd7a7d] succeeded in 0.5162749999435619s: {'cpu': 4.8, 'memory': 45.6}
[2026-03-30 02:15:59,993: INFO/MainProcess] Task tasks.scrape_pending_urls[ebfed10f-b2bc-4f5e-9d0d-fb9654409905] received
[2026-03-30 02:15:59,995: INFO/MainProcess] Task tasks.scrape_pending_urls[ebfed10f-b2bc-4f5e-9d0d-fb9654409905] succeeded in 0.002190000028349459s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:15:59,997: INFO/MainProcess] Task tasks.collect_system_metrics[0e363ce4-33dd-4719-848d-0df67f004e2b] received
[2026-03-30 02:16:00,513: INFO/MainProcess] Task tasks.collect_system_metrics[0e363ce4-33dd-4719-848d-0df67f004e2b] succeeded in 0.5162391999037936s: {'cpu': 8.4, 'memory': 45.6}
[2026-03-30 02:16:00,515: INFO/MainProcess] Task tasks.scrape_pending_urls[d46294b1-f986-4f3c-ad3c-9d43003a2283] received
[2026-03-30 02:16:00,518: INFO/MainProcess] Task tasks.scrape_pending_urls[d46294b1-f986-4f3c-ad3c-9d43003a2283] succeeded in 0.002733600093051791s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:00,519: INFO/MainProcess] Task tasks.collect_system_metrics[f0c7d662-80c5-487c-95d2-c3991e6f7f6d] received
[2026-03-30 02:16:01,036: INFO/MainProcess] Task tasks.collect_system_metrics[f0c7d662-80c5-487c-95d2-c3991e6f7f6d] succeeded in 0.5161000000080094s: {'cpu': 7.5, 'memory': 45.6}
[2026-03-30 02:16:01,038: INFO/MainProcess] Task tasks.scrape_pending_urls[7fd10cf1-9dc3-4004-9c90-d3446e5856ae] received
[2026-03-30 02:16:01,040: INFO/MainProcess] Task tasks.scrape_pending_urls[7fd10cf1-9dc3-4004-9c90-d3446e5856ae] succeeded in 0.0021933000534772873s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:01,042: INFO/MainProcess] Task tasks.collect_system_metrics[e9efc23d-72e9-435e-92c4-c2386d55d28d] received
[2026-03-30 02:16:01,559: INFO/MainProcess] Task tasks.collect_system_metrics[e9efc23d-72e9-435e-92c4-c2386d55d28d] succeeded in 0.5164868000429124s: {'cpu': 8.6, 'memory': 45.6}
[2026-03-30 02:16:01,561: INFO/MainProcess] Task tasks.scrape_pending_urls[6d7b14f3-72f5-40e1-ad00-46fdaace369a] received
[2026-03-30 02:16:01,564: INFO/MainProcess] Task tasks.scrape_pending_urls[6d7b14f3-72f5-40e1-ad00-46fdaace369a] succeeded in 0.0025964999804273248s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:01,565: INFO/MainProcess] Task tasks.collect_system_metrics[e68a4eb6-6c93-4767-8f59-948a75e376b1] received
[2026-03-30 02:16:02,082: INFO/MainProcess] Task tasks.collect_system_metrics[e68a4eb6-6c93-4767-8f59-948a75e376b1] succeeded in 0.5169733000220731s: {'cpu': 7.3, 'memory': 45.6}
[2026-03-30 02:16:02,084: INFO/MainProcess] Task tasks.scrape_pending_urls[f8cde219-0234-4b1f-8560-372a8041ae9b] received
[2026-03-30 02:16:02,087: INFO/MainProcess] Task tasks.scrape_pending_urls[f8cde219-0234-4b1f-8560-372a8041ae9b] succeeded in 0.0021765000419691205s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:02,088: INFO/MainProcess] Task tasks.collect_system_metrics[ac606cdd-2db8-4791-9efb-006a787df8ee] received
[2026-03-30 02:16:02,605: INFO/MainProcess] Task tasks.collect_system_metrics[ac606cdd-2db8-4791-9efb-006a787df8ee] succeeded in 0.5166621999815106s: {'cpu': 3.5, 'memory': 45.6}
[2026-03-30 02:16:02,607: INFO/MainProcess] Task tasks.scrape_pending_urls[f81171e1-8080-4299-a263-df38a22f31be] received
[2026-03-30 02:16:02,610: INFO/MainProcess] Task tasks.scrape_pending_urls[f81171e1-8080-4299-a263-df38a22f31be] succeeded in 0.002597399987280369s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:02,611: INFO/MainProcess] Task tasks.collect_system_metrics[78a43719-5769-4839-9757-284c7da6577c] received
[2026-03-30 02:16:03,120: INFO/MainProcess] Task tasks.collect_system_metrics[78a43719-5769-4839-9757-284c7da6577c] succeeded in 0.5083778999978676s: {'cpu': 0.0, 'memory': 45.6}
[2026-03-30 02:16:03,122: INFO/MainProcess] Task tasks.scrape_pending_urls[17cf669d-aa40-444d-92c6-06b86b191fee] received
[2026-03-30 02:16:03,125: INFO/MainProcess] Task tasks.scrape_pending_urls[17cf669d-aa40-444d-92c6-06b86b191fee] succeeded in 0.003209899994544685s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,127: INFO/MainProcess] Task tasks.collect_system_metrics[a12c5659-fa6f-4415-8a5c-f8e553018ce5] received
[2026-03-30 02:16:03,632: INFO/MainProcess] Task tasks.collect_system_metrics[a12c5659-fa6f-4415-8a5c-f8e553018ce5] succeeded in 0.5048846000572667s: {'cpu': 7.5, 'memory': 45.6}
[2026-03-30 02:16:03,634: INFO/MainProcess] Task tasks.scrape_pending_urls[86964d09-b66f-4d4e-80d9-fb24b0d605f2] received
[2026-03-30 02:16:03,637: INFO/MainProcess] Task tasks.scrape_pending_urls[86964d09-b66f-4d4e-80d9-fb24b0d605f2] succeeded in 0.0029834999004378915s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,639: INFO/MainProcess] Task tasks.scrape_pending_urls[fa320b07-f975-480d-ae23-90e537b1bf38] received
[2026-03-30 02:16:03,641: INFO/MainProcess] Task tasks.scrape_pending_urls[fa320b07-f975-480d-ae23-90e537b1bf38] succeeded in 0.0021476999390870333s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,643: INFO/MainProcess] Task tasks.scrape_pending_urls[e878912b-ca51-495b-8dd7-34f8f87cecc3] received
[2026-03-30 02:16:03,645: INFO/MainProcess] Task tasks.scrape_pending_urls[e878912b-ca51-495b-8dd7-34f8f87cecc3] succeeded in 0.0020249999361112714s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,646: INFO/MainProcess] Task tasks.scrape_pending_urls[01103ad9-3375-4373-9f96-9f85a47cc5e4] received
[2026-03-30 02:16:03,649: INFO/MainProcess] Task tasks.scrape_pending_urls[01103ad9-3375-4373-9f96-9f85a47cc5e4] succeeded in 0.0020147000905126333s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,650: INFO/MainProcess] Task tasks.scrape_pending_urls[ca3b22b8-1e4e-4e3f-9aad-36e6e7537b13] received
[2026-03-30 02:16:03,652: INFO/MainProcess] Task tasks.scrape_pending_urls[ca3b22b8-1e4e-4e3f-9aad-36e6e7537b13] succeeded in 0.0020182000007480383s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,656: INFO/MainProcess] Task tasks.scrape_pending_urls[2dc7e456-8839-4e4f-8046-aa3fced744ce] received
[2026-03-30 02:16:03,659: INFO/MainProcess] Task tasks.scrape_pending_urls[2dc7e456-8839-4e4f-8046-aa3fced744ce] succeeded in 0.002919499995186925s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,661: INFO/MainProcess] Task tasks.scrape_pending_urls[a19fe9a1-5238-43ad-9ad3-eda931f69d22] received
[2026-03-30 02:16:03,664: INFO/MainProcess] Task tasks.scrape_pending_urls[a19fe9a1-5238-43ad-9ad3-eda931f69d22] succeeded in 0.0026076999492943287s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,665: INFO/MainProcess] Task tasks.scrape_pending_urls[4e0b85ba-57b8-4e96-bbdb-4da716d21621] received
[2026-03-30 02:16:03,667: INFO/MainProcess] Task tasks.scrape_pending_urls[4e0b85ba-57b8-4e96-bbdb-4da716d21621] succeeded in 0.0020952000049874187s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,670: INFO/MainProcess] Task tasks.scrape_pending_urls[359622cf-97e3-41b9-982c-2eef0c83649f] received
[2026-03-30 02:16:03,674: INFO/MainProcess] Task tasks.scrape_pending_urls[359622cf-97e3-41b9-982c-2eef0c83649f] succeeded in 0.0029909000732004642s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,675: INFO/MainProcess] Task tasks.scrape_pending_urls[71136204-664f-46c9-a85f-d3a617b61876] received
[2026-03-30 02:16:03,678: INFO/MainProcess] Task tasks.scrape_pending_urls[71136204-664f-46c9-a85f-d3a617b61876] succeeded in 0.0021180000621825457s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,679: INFO/MainProcess] Task tasks.scrape_pending_urls[8b2cdf27-23dc-468d-992c-10239bc51b2e] received
[2026-03-30 02:16:03,682: INFO/MainProcess] Task tasks.scrape_pending_urls[8b2cdf27-23dc-468d-992c-10239bc51b2e] succeeded in 0.0021968999644741416s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,683: INFO/MainProcess] Task tasks.scrape_pending_urls[88a2293f-d173-4b9f-9eaf-9466b11207dd] received
[2026-03-30 02:16:03,687: INFO/MainProcess] Task tasks.scrape_pending_urls[88a2293f-d173-4b9f-9eaf-9466b11207dd] succeeded in 0.003572600078769028s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,688: INFO/MainProcess] Task tasks.scrape_pending_urls[b10d2828-9a74-4022-9be2-a13c287c7070] received
[2026-03-30 02:16:03,691: INFO/MainProcess] Task tasks.scrape_pending_urls[b10d2828-9a74-4022-9be2-a13c287c7070] succeeded in 0.0022207999136298895s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,692: INFO/MainProcess] Task tasks.scrape_pending_urls[411bf661-1b45-43de-aa89-1ccbf670a4cd] received
[2026-03-30 02:16:03,695: INFO/MainProcess] Task tasks.scrape_pending_urls[411bf661-1b45-43de-aa89-1ccbf670a4cd] succeeded in 0.002151799970306456s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,696: INFO/MainProcess] Task tasks.scrape_pending_urls[35d88c6a-30c9-4fd1-af90-40b0ef645044] received
[2026-03-30 02:16:03,699: INFO/MainProcess] Task tasks.scrape_pending_urls[35d88c6a-30c9-4fd1-af90-40b0ef645044] succeeded in 0.0025810999795794487s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,701: INFO/MainProcess] Task tasks.scrape_pending_urls[880c4fc7-0fde-4689-a6a4-4ccf1011b658] received
[2026-03-30 02:16:03,704: INFO/MainProcess] Task tasks.scrape_pending_urls[880c4fc7-0fde-4689-a6a4-4ccf1011b658] succeeded in 0.002487200079485774s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,705: INFO/MainProcess] Task tasks.scrape_pending_urls[33ad4f52-30c1-4f01-9d67-b737374fc08f] received
[2026-03-30 02:16:03,708: INFO/MainProcess] Task tasks.scrape_pending_urls[33ad4f52-30c1-4f01-9d67-b737374fc08f] succeeded in 0.002039699931629002s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,709: INFO/MainProcess] Task tasks.scrape_pending_urls[44727002-1554-4ea0-a69a-249ded0bd35a] received
[2026-03-30 02:16:03,711: INFO/MainProcess] Task tasks.scrape_pending_urls[44727002-1554-4ea0-a69a-249ded0bd35a] succeeded in 0.001993000041693449s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,713: INFO/MainProcess] Task tasks.scrape_pending_urls[b6d2f152-0d77-405e-94b9-b994ea471fc9] received
[2026-03-30 02:16:03,715: INFO/MainProcess] Task tasks.scrape_pending_urls[b6d2f152-0d77-405e-94b9-b994ea471fc9] succeeded in 0.0019537999760359526s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,716: INFO/MainProcess] Task tasks.scrape_pending_urls[1e82b059-babe-481f-bc42-f76bbcd03b07] received
[2026-03-30 02:16:03,721: INFO/MainProcess] Task tasks.scrape_pending_urls[1e82b059-babe-481f-bc42-f76bbcd03b07] succeeded in 0.0041655999375507236s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,722: INFO/MainProcess] Task tasks.scrape_pending_urls[dfc1a399-1e39-47f2-b7fb-9c607ffb67df] received
[2026-03-30 02:16:03,725: INFO/MainProcess] Task tasks.scrape_pending_urls[dfc1a399-1e39-47f2-b7fb-9c607ffb67df] succeeded in 0.002764799981378019s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,726: INFO/MainProcess] Task tasks.scrape_pending_urls[a3dc0ea1-5457-4f6a-bf24-e583dcec48a0] received
[2026-03-30 02:16:03,729: INFO/MainProcess] Task tasks.scrape_pending_urls[a3dc0ea1-5457-4f6a-bf24-e583dcec48a0] succeeded in 0.002126400009728968s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,730: INFO/MainProcess] Task tasks.scrape_pending_urls[2e6415d0-cf26-4802-9320-20be7f221953] received
[2026-03-30 02:16:03,733: INFO/MainProcess] Task tasks.scrape_pending_urls[2e6415d0-cf26-4802-9320-20be7f221953] succeeded in 0.0022824000334367156s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,735: INFO/MainProcess] Task tasks.scrape_pending_urls[ea1ba4be-4158-4d2b-9588-33fcbe4483d4] received
[2026-03-30 02:16:03,737: INFO/MainProcess] Task tasks.scrape_pending_urls[ea1ba4be-4158-4d2b-9588-33fcbe4483d4] succeeded in 0.002138199983164668s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,738: INFO/MainProcess] Task tasks.scrape_pending_urls[9667091e-78ad-4a69-9c55-215579513402] received
[2026-03-30 02:16:03,741: INFO/MainProcess] Task tasks.scrape_pending_urls[9667091e-78ad-4a69-9c55-215579513402] succeeded in 0.001991200027987361s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,742: INFO/MainProcess] Task tasks.scrape_pending_urls[f794e84c-cc83-444b-adc6-864f151d9d88] received
[2026-03-30 02:16:03,744: INFO/MainProcess] Task tasks.scrape_pending_urls[f794e84c-cc83-444b-adc6-864f151d9d88] succeeded in 0.001977600040845573s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,746: INFO/MainProcess] Task tasks.scrape_pending_urls[b388db96-b220-4bbc-95a8-1ce89dabd2ec] received
[2026-03-30 02:16:03,748: INFO/MainProcess] Task tasks.scrape_pending_urls[b388db96-b220-4bbc-95a8-1ce89dabd2ec] succeeded in 0.002067199908196926s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,750: INFO/MainProcess] Task tasks.scrape_pending_urls[e9312d13-50a4-4e60-b81e-e94b8936bec4] received
[2026-03-30 02:16:03,754: INFO/MainProcess] Task tasks.scrape_pending_urls[e9312d13-50a4-4e60-b81e-e94b8936bec4] succeeded in 0.002956800046376884s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,755: INFO/MainProcess] Task tasks.scrape_pending_urls[b8460ed4-e70a-46ef-a8b7-398acfa5a256] received
[2026-03-30 02:16:03,758: INFO/MainProcess] Task tasks.scrape_pending_urls[b8460ed4-e70a-46ef-a8b7-398acfa5a256] succeeded in 0.0022329000057652593s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,759: INFO/MainProcess] Task tasks.scrape_pending_urls[3edff88a-a849-4c24-8990-3a90d466f3b2] received
[2026-03-30 02:16:03,761: INFO/MainProcess] Task tasks.scrape_pending_urls[3edff88a-a849-4c24-8990-3a90d466f3b2] succeeded in 0.0020320999901741743s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,762: INFO/MainProcess] Task tasks.scrape_pending_urls[892e8727-2a85-4b1a-918a-81d8cd9e1116] received
[2026-03-30 02:16:03,765: INFO/MainProcess] Task tasks.scrape_pending_urls[892e8727-2a85-4b1a-918a-81d8cd9e1116] succeeded in 0.002413300098851323s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,767: INFO/MainProcess] Task tasks.scrape_pending_urls[fe815d58-7cd7-4620-bfbe-9e3aa81e51ec] received
[2026-03-30 02:16:03,769: INFO/MainProcess] Task tasks.scrape_pending_urls[fe815d58-7cd7-4620-bfbe-9e3aa81e51ec] succeeded in 0.0022179000079631805s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,771: INFO/MainProcess] Task tasks.scrape_pending_urls[3889a67b-1193-4ad7-a93b-c2e924d9c911] received
[2026-03-30 02:16:03,773: INFO/MainProcess] Task tasks.scrape_pending_urls[3889a67b-1193-4ad7-a93b-c2e924d9c911] succeeded in 0.0020299000898376107s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,774: INFO/MainProcess] Task tasks.scrape_pending_urls[874f411f-da7e-4947-bec1-63470b3011a6] received
[2026-03-30 02:16:03,777: INFO/MainProcess] Task tasks.scrape_pending_urls[874f411f-da7e-4947-bec1-63470b3011a6] succeeded in 0.0019895998993888497s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,778: INFO/MainProcess] Task tasks.scrape_pending_urls[158a20ed-218d-41ca-9743-c34bb2553cf2] received
[2026-03-30 02:16:03,781: INFO/MainProcess] Task tasks.scrape_pending_urls[158a20ed-218d-41ca-9743-c34bb2553cf2] succeeded in 0.0030044999439269304s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,784: INFO/MainProcess] Task tasks.scrape_pending_urls[e15e5af4-9636-4543-ab55-2ee8d436b090] received
[2026-03-30 02:16:03,787: INFO/MainProcess] Task tasks.scrape_pending_urls[e15e5af4-9636-4543-ab55-2ee8d436b090] succeeded in 0.00291300006210804s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,788: INFO/MainProcess] Task tasks.scrape_pending_urls[bfebfd86-2ab3-4e18-a403-8f8fc0a4dc03] received
[2026-03-30 02:16:03,791: INFO/MainProcess] Task tasks.scrape_pending_urls[bfebfd86-2ab3-4e18-a403-8f8fc0a4dc03] succeeded in 0.0021845001028850675s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,792: INFO/MainProcess] Task tasks.scrape_pending_urls[e045c50c-19e1-4e6e-9709-1de57bb894d8] received
[2026-03-30 02:16:03,794: INFO/MainProcess] Task tasks.scrape_pending_urls[e045c50c-19e1-4e6e-9709-1de57bb894d8] succeeded in 0.0020320999901741743s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,795: INFO/MainProcess] Task tasks.scrape_pending_urls[9f056782-7183-4510-9fcc-1f7c6891930a] received
[2026-03-30 02:16:03,799: INFO/MainProcess] Task tasks.scrape_pending_urls[9f056782-7183-4510-9fcc-1f7c6891930a] succeeded in 0.002987800049595535s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,800: INFO/MainProcess] Task tasks.scrape_pending_urls[901caaa1-58f7-4685-9812-006a9b60032e] received
[2026-03-30 02:16:03,802: INFO/MainProcess] Task tasks.scrape_pending_urls[901caaa1-58f7-4685-9812-006a9b60032e] succeeded in 0.0021452000364661217s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,804: INFO/MainProcess] Task tasks.scrape_pending_urls[d0cbac32-4a56-45b1-9ee3-394ab9588d69] received
[2026-03-30 02:16:03,807: INFO/MainProcess] Task tasks.scrape_pending_urls[d0cbac32-4a56-45b1-9ee3-394ab9588d69] succeeded in 0.0025651000905781984s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,808: INFO/MainProcess] Task tasks.scrape_pending_urls[9a6812c9-9a14-4e5a-89e3-0b9b467b1457] received
[2026-03-30 02:16:03,811: INFO/MainProcess] Task tasks.scrape_pending_urls[9a6812c9-9a14-4e5a-89e3-0b9b467b1457] succeeded in 0.0020117999520152807s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,812: INFO/MainProcess] Task tasks.scrape_pending_urls[c365e88b-178a-4631-b0f0-f846c423f17f] received
[2026-03-30 02:16:03,815: INFO/MainProcess] Task tasks.scrape_pending_urls[c365e88b-178a-4631-b0f0-f846c423f17f] succeeded in 0.0031785001046955585s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,817: INFO/MainProcess] Task tasks.scrape_pending_urls[fd5b844f-91e6-4622-851e-a912b750eba7] received
[2026-03-30 02:16:03,819: INFO/MainProcess] Task tasks.scrape_pending_urls[fd5b844f-91e6-4622-851e-a912b750eba7] succeeded in 0.002099200035445392s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,820: INFO/MainProcess] Task tasks.scrape_pending_urls[abdc17e5-a24a-4c0f-974a-ea58bf477427] received
[2026-03-30 02:16:03,822: INFO/MainProcess] Task tasks.scrape_pending_urls[abdc17e5-a24a-4c0f-974a-ea58bf477427] succeeded in 0.002020500018261373s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,824: INFO/MainProcess] Task tasks.scrape_pending_urls[8d7335d8-fa0e-4f60-aff9-d5c292b3a5dc] received
[2026-03-30 02:16:03,826: INFO/MainProcess] Task tasks.scrape_pending_urls[8d7335d8-fa0e-4f60-aff9-d5c292b3a5dc] succeeded in 0.0019763000309467316s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,827: INFO/MainProcess] Task tasks.scrape_pending_urls[d3698f2c-4eb4-410b-b572-fa0e4ca37dd7] received
[2026-03-30 02:16:03,831: INFO/MainProcess] Task tasks.scrape_pending_urls[d3698f2c-4eb4-410b-b572-fa0e4ca37dd7] succeeded in 0.003363399999216199s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,832: INFO/MainProcess] Task tasks.scrape_pending_urls[04ae4cb0-2aba-4d02-8186-caf3e3ce08d1] received
[2026-03-30 02:16:03,835: INFO/MainProcess] Task tasks.scrape_pending_urls[04ae4cb0-2aba-4d02-8186-caf3e3ce08d1] succeeded in 0.002613999997265637s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,837: INFO/MainProcess] Task tasks.scrape_pending_urls[1f56d148-c978-4415-a221-d143522cb682] received
[2026-03-30 02:16:03,839: INFO/MainProcess] Task tasks.scrape_pending_urls[1f56d148-c978-4415-a221-d143522cb682] succeeded in 0.002028499962761998s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,840: INFO/MainProcess] Task tasks.scrape_pending_urls[2ca8ed38-76a6-4a39-bb2f-892cfd14d444] received
[2026-03-30 02:16:03,843: INFO/MainProcess] Task tasks.scrape_pending_urls[2ca8ed38-76a6-4a39-bb2f-892cfd14d444] succeeded in 0.0019954999443143606s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,844: INFO/MainProcess] Task tasks.scrape_pending_urls[bbf024e2-fb75-4d7f-a99b-e8e3b7bcaf41] received
[2026-03-30 02:16:03,848: INFO/MainProcess] Task tasks.scrape_pending_urls[bbf024e2-fb75-4d7f-a99b-e8e3b7bcaf41] succeeded in 0.0035287999780848622s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,849: INFO/MainProcess] Task tasks.scrape_pending_urls[aa721512-3f97-4fed-86c9-23486288cc10] received
[2026-03-30 02:16:03,851: INFO/MainProcess] Task tasks.scrape_pending_urls[aa721512-3f97-4fed-86c9-23486288cc10] succeeded in 0.002073400071822107s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,853: INFO/MainProcess] Task tasks.scrape_pending_urls[007d3e63-0ac0-4e5a-80ed-a03f3f8b8c02] received
[2026-03-30 02:16:03,855: INFO/MainProcess] Task tasks.scrape_pending_urls[007d3e63-0ac0-4e5a-80ed-a03f3f8b8c02] succeeded in 0.001977600040845573s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,856: INFO/MainProcess] Task tasks.scrape_pending_urls[dd0698db-5c90-4d4b-b9fb-e40a22fa30de] received
[2026-03-30 02:16:03,858: INFO/MainProcess] Task tasks.scrape_pending_urls[dd0698db-5c90-4d4b-b9fb-e40a22fa30de] succeeded in 0.0019791999366134405s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,860: INFO/MainProcess] Task tasks.scrape_pending_urls[fe2026e5-c8f4-4330-8ab3-1ebc15ee5685] received
[2026-03-30 02:16:03,863: INFO/MainProcess] Task tasks.scrape_pending_urls[fe2026e5-c8f4-4330-8ab3-1ebc15ee5685] succeeded in 0.0032888000132516026s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,865: INFO/MainProcess] Task tasks.scrape_pending_urls[dddf498c-18ae-455c-b393-d711abaa706f] received
[2026-03-30 02:16:03,867: INFO/MainProcess] Task tasks.scrape_pending_urls[dddf498c-18ae-455c-b393-d711abaa706f] succeeded in 0.0020262999460101128s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,868: INFO/MainProcess] Task tasks.scrape_pending_urls[207e3d85-445d-428e-8eaa-d8d4ea4e347f] received
[2026-03-30 02:16:03,870: INFO/MainProcess] Task tasks.scrape_pending_urls[207e3d85-445d-428e-8eaa-d8d4ea4e347f] succeeded in 0.00197199999820441s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,872: INFO/MainProcess] Task tasks.scrape_pending_urls[bb3868e5-3bc0-42c4-99bf-a5247df1ca04] received
[2026-03-30 02:16:03,874: INFO/MainProcess] Task tasks.scrape_pending_urls[bb3868e5-3bc0-42c4-99bf-a5247df1ca04] succeeded in 0.0019907000241801143s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,875: INFO/MainProcess] Task tasks.scrape_pending_urls[ede89473-c524-491e-b6a5-ab18fb539065] received
[2026-03-30 02:16:03,880: INFO/MainProcess] Task tasks.scrape_pending_urls[ede89473-c524-491e-b6a5-ab18fb539065] succeeded in 0.004328500013798475s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,881: INFO/MainProcess] Task tasks.scrape_pending_urls[726dff6f-3818-4066-a388-77844eaa3191] received
[2026-03-30 02:16:03,884: INFO/MainProcess] Task tasks.scrape_pending_urls[726dff6f-3818-4066-a388-77844eaa3191] succeeded in 0.0021111000096425414s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,885: INFO/MainProcess] Task tasks.scrape_pending_urls[b9108fd1-c399-467f-bb62-cb57ed015846] received
[2026-03-30 02:16:03,888: INFO/MainProcess] Task tasks.scrape_pending_urls[b9108fd1-c399-467f-bb62-cb57ed015846] succeeded in 0.002559100044891238s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,889: INFO/MainProcess] Task tasks.scrape_pending_urls[a9768450-3284-4dd2-b452-e38aab104942] received
[2026-03-30 02:16:03,892: INFO/MainProcess] Task tasks.scrape_pending_urls[a9768450-3284-4dd2-b452-e38aab104942] succeeded in 0.002291399985551834s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,894: INFO/MainProcess] Task tasks.scrape_pending_urls[9642e298-51ef-4bf4-aaef-993d9ffa18b5] received
[2026-03-30 02:16:03,896: INFO/MainProcess] Task tasks.scrape_pending_urls[9642e298-51ef-4bf4-aaef-993d9ffa18b5] succeeded in 0.002332499949261546s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,898: INFO/MainProcess] Task tasks.scrape_pending_urls[cc6b703c-0b14-4c6e-ad84-b3ca9b36d584] received
[2026-03-30 02:16:03,900: INFO/MainProcess] Task tasks.scrape_pending_urls[cc6b703c-0b14-4c6e-ad84-b3ca9b36d584] succeeded in 0.0021793999476358294s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,901: INFO/MainProcess] Task tasks.scrape_pending_urls[40677f3a-c6dd-4a1b-b114-482a6e3590e4] received
[2026-03-30 02:16:03,904: INFO/MainProcess] Task tasks.scrape_pending_urls[40677f3a-c6dd-4a1b-b114-482a6e3590e4] succeeded in 0.002162700053304434s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,905: INFO/MainProcess] Task tasks.scrape_pending_urls[06524581-fc69-47a4-bc1f-a59dc7b97cd9] received
[2026-03-30 02:16:03,907: INFO/MainProcess] Task tasks.scrape_pending_urls[06524581-fc69-47a4-bc1f-a59dc7b97cd9] succeeded in 0.0021374999778345227s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,909: INFO/MainProcess] Task tasks.scrape_pending_urls[41999a82-4e47-44e4-a7a1-445803f7337d] received
[2026-03-30 02:16:03,913: INFO/MainProcess] Task tasks.scrape_pending_urls[41999a82-4e47-44e4-a7a1-445803f7337d] succeeded in 0.0029713999247178435s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,915: INFO/MainProcess] Task tasks.scrape_pending_urls[42203eaf-0b53-439b-973e-69065703efbd] received
[2026-03-30 02:16:03,917: INFO/MainProcess] Task tasks.scrape_pending_urls[42203eaf-0b53-439b-973e-69065703efbd] succeeded in 0.0025516999885439873s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,919: INFO/MainProcess] Task tasks.scrape_pending_urls[8a69f26a-a792-4301-848f-7be2f8364a88] received
[2026-03-30 02:16:03,921: INFO/MainProcess] Task tasks.scrape_pending_urls[8a69f26a-a792-4301-848f-7be2f8364a88] succeeded in 0.0023352999705821276s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,923: INFO/MainProcess] Task tasks.scrape_pending_urls[d0966897-de0b-4eff-97c6-a4ad580be61c] received
[2026-03-30 02:16:03,926: INFO/MainProcess] Task tasks.scrape_pending_urls[d0966897-de0b-4eff-97c6-a4ad580be61c] succeeded in 0.003154599922709167s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,927: INFO/MainProcess] Task tasks.scrape_pending_urls[1ecfabdf-2678-4fd0-a0c3-558a19b27423] received
[2026-03-30 02:16:03,930: INFO/MainProcess] Task tasks.scrape_pending_urls[1ecfabdf-2678-4fd0-a0c3-558a19b27423] succeeded in 0.0021712000016123056s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,931: INFO/MainProcess] Task tasks.scrape_pending_urls[fdd3ece9-3411-48c6-8516-b921be82ff0b] received
[2026-03-30 02:16:03,933: INFO/MainProcess] Task tasks.scrape_pending_urls[fdd3ece9-3411-48c6-8516-b921be82ff0b] succeeded in 0.0019968999549746513s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,935: INFO/MainProcess] Task tasks.scrape_pending_urls[53c03ddc-b6cc-4833-bf3e-be09cd905e05] received
[2026-03-30 02:16:03,937: INFO/MainProcess] Task tasks.scrape_pending_urls[53c03ddc-b6cc-4833-bf3e-be09cd905e05] succeeded in 0.001971699995920062s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,938: INFO/MainProcess] Task tasks.scrape_pending_urls[fe193085-d49a-4986-9ba0-e6a8183b6812] received
[2026-03-30 02:16:03,942: INFO/MainProcess] Task tasks.scrape_pending_urls[fe193085-d49a-4986-9ba0-e6a8183b6812] succeeded in 0.0033119000727310777s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,943: INFO/MainProcess] Task tasks.scrape_pending_urls[e50b8017-4532-46a5-85a4-db9d80e856ba] received
[2026-03-30 02:16:03,946: INFO/MainProcess] Task tasks.scrape_pending_urls[e50b8017-4532-46a5-85a4-db9d80e856ba] succeeded in 0.0023387999972328544s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,947: INFO/MainProcess] Task tasks.scrape_pending_urls[329bdfb1-18d8-4ec9-8847-4dd671360277] received
[2026-03-30 02:16:03,949: INFO/MainProcess] Task tasks.scrape_pending_urls[329bdfb1-18d8-4ec9-8847-4dd671360277] succeeded in 0.002202700008638203s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,951: INFO/MainProcess] Task tasks.scrape_pending_urls[012dc9c1-774e-4f0c-8811-71c530bcd959] received
[2026-03-30 02:16:03,953: INFO/MainProcess] Task tasks.scrape_pending_urls[012dc9c1-774e-4f0c-8811-71c530bcd959] succeeded in 0.0021767999278381467s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,954: INFO/MainProcess] Task tasks.scrape_pending_urls[94ab72e2-089d-4894-b33e-eb943abbabbd] received
[2026-03-30 02:16:03,957: INFO/MainProcess] Task tasks.scrape_pending_urls[94ab72e2-089d-4894-b33e-eb943abbabbd] succeeded in 0.002218100009486079s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,960: INFO/MainProcess] Task tasks.scrape_pending_urls[2b07b639-152b-447c-bc93-ba426771eeaf] received
[2026-03-30 02:16:03,962: INFO/MainProcess] Task tasks.scrape_pending_urls[2b07b639-152b-447c-bc93-ba426771eeaf] succeeded in 0.0021971999667584896s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,964: INFO/MainProcess] Task tasks.scrape_pending_urls[c9282252-7a5e-45b2-a4fc-eb3cd7892c63] received
[2026-03-30 02:16:03,966: INFO/MainProcess] Task tasks.scrape_pending_urls[c9282252-7a5e-45b2-a4fc-eb3cd7892c63] succeeded in 0.0025118000339716673s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,968: INFO/MainProcess] Task tasks.scrape_pending_urls[de19a662-af31-4d87-bbaf-ace2522a8ac6] received
[2026-03-30 02:16:03,970: INFO/MainProcess] Task tasks.scrape_pending_urls[de19a662-af31-4d87-bbaf-ace2522a8ac6] succeeded in 0.0020812000147998333s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,971: INFO/MainProcess] Task tasks.scrape_pending_urls[3314080d-acee-46c7-a093-14d8a036b1da] received
[2026-03-30 02:16:03,975: INFO/MainProcess] Task tasks.scrape_pending_urls[3314080d-acee-46c7-a093-14d8a036b1da] succeeded in 0.003237999975681305s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,976: INFO/MainProcess] Task tasks.scrape_pending_urls[b1c83851-9e33-406d-b32e-b09bb1c417df] received
[2026-03-30 02:16:03,978: INFO/MainProcess] Task tasks.scrape_pending_urls[b1c83851-9e33-406d-b32e-b09bb1c417df] succeeded in 0.0020895999623462558s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,980: INFO/MainProcess] Task tasks.scrape_pending_urls[cc6b5a2b-0597-4df0-9727-b118ade1094b] received
[2026-03-30 02:16:03,982: INFO/MainProcess] Task tasks.scrape_pending_urls[cc6b5a2b-0597-4df0-9727-b118ade1094b] succeeded in 0.002023400040343404s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,983: INFO/MainProcess] Task tasks.scrape_pending_urls[a54e21d1-76e2-43cb-a64b-d915dd13c007] received
[2026-03-30 02:16:03,985: INFO/MainProcess] Task tasks.scrape_pending_urls[a54e21d1-76e2-43cb-a64b-d915dd13c007] succeeded in 0.0020131999626755714s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,987: INFO/MainProcess] Task tasks.scrape_pending_urls[705ceaf6-3678-46f6-8021-06da588f6792] received
[2026-03-30 02:16:03,991: INFO/MainProcess] Task tasks.scrape_pending_urls[705ceaf6-3678-46f6-8021-06da588f6792] succeeded in 0.003937000059522688s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,993: INFO/MainProcess] Task tasks.scrape_pending_urls[289a89ed-ef66-41ac-a871-005a260e60bf] received
[2026-03-30 02:16:03,996: INFO/MainProcess] Task tasks.scrape_pending_urls[289a89ed-ef66-41ac-a871-005a260e60bf] succeeded in 0.002647200017236173s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:03,997: INFO/MainProcess] Task tasks.scrape_pending_urls[fc10e2e2-ab5c-4cc6-9428-c07f4e47c173] received
[2026-03-30 02:16:03,999: INFO/MainProcess] Task tasks.scrape_pending_urls[fc10e2e2-ab5c-4cc6-9428-c07f4e47c173] succeeded in 0.0021578000159934163s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,001: INFO/MainProcess] Task tasks.scrape_pending_urls[f6cbeca5-4347-4f62-bfdf-aba7c5d7b28a] received
[2026-03-30 02:16:04,003: INFO/MainProcess] Task tasks.scrape_pending_urls[f6cbeca5-4347-4f62-bfdf-aba7c5d7b28a] succeeded in 0.0021530999802052975s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,005: INFO/MainProcess] Task tasks.scrape_pending_urls[90e6d3fd-204a-4e62-a35c-7043ad6481b4] received
[2026-03-30 02:16:04,008: INFO/MainProcess] Task tasks.scrape_pending_urls[90e6d3fd-204a-4e62-a35c-7043ad6481b4] succeeded in 0.002379300072789192s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,009: INFO/MainProcess] Task tasks.scrape_pending_urls[83f3f7fe-6e0e-4289-9b9b-f5ae0d267fa9] received
[2026-03-30 02:16:04,011: INFO/MainProcess] Task tasks.scrape_pending_urls[83f3f7fe-6e0e-4289-9b9b-f5ae0d267fa9] succeeded in 0.0021970999659970403s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,012: INFO/MainProcess] Task tasks.scrape_pending_urls[8c672c6d-93d0-4dd9-8d87-4417928c95d7] received
[2026-03-30 02:16:04,015: INFO/MainProcess] Task tasks.scrape_pending_urls[8c672c6d-93d0-4dd9-8d87-4417928c95d7] succeeded in 0.0021504999604076147s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,016: INFO/MainProcess] Task tasks.scrape_pending_urls[cf99d18b-4300-4631-a2f4-631f55fd2d10] received
[2026-03-30 02:16:04,019: INFO/MainProcess] Task tasks.scrape_pending_urls[cf99d18b-4300-4631-a2f4-631f55fd2d10] succeeded in 0.0026196000399068s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,021: INFO/MainProcess] Task tasks.scrape_pending_urls[efd251e0-309b-4ee6-80da-39362cd00b02] received
[2026-03-30 02:16:04,024: INFO/MainProcess] Task tasks.scrape_pending_urls[efd251e0-309b-4ee6-80da-39362cd00b02] succeeded in 0.0023948000743985176s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,025: INFO/MainProcess] Task tasks.scrape_pending_urls[7426fa9d-0a7b-4c43-b515-63f25d2ec07e] received
[2026-03-30 02:16:04,027: INFO/MainProcess] Task tasks.scrape_pending_urls[7426fa9d-0a7b-4c43-b515-63f25d2ec07e] succeeded in 0.002181899966672063s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,028: INFO/MainProcess] Task tasks.scrape_pending_urls[11e13fc1-9f59-4a30-964b-c54a7382981f] received
[2026-03-30 02:16:04,031: INFO/MainProcess] Task tasks.scrape_pending_urls[11e13fc1-9f59-4a30-964b-c54a7382981f] succeeded in 0.0021467999322339892s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,032: INFO/MainProcess] Task tasks.scrape_pending_urls[93436b7f-cb81-47d2-af16-e1976e7310dd] received
[2026-03-30 02:16:04,034: INFO/MainProcess] Task tasks.scrape_pending_urls[93436b7f-cb81-47d2-af16-e1976e7310dd] succeeded in 0.0021422000136226416s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,036: INFO/MainProcess] Task tasks.scrape_pending_urls[5995d888-da2f-4caf-a55b-383e7c955308] received
[2026-03-30 02:16:04,040: INFO/MainProcess] Task tasks.scrape_pending_urls[5995d888-da2f-4caf-a55b-383e7c955308] succeeded in 0.002619899925775826s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,041: INFO/MainProcess] Task tasks.scrape_pending_urls[929a62e6-dd8a-41d5-92ea-ee192c6923cb] received
[2026-03-30 02:16:04,044: INFO/MainProcess] Task tasks.scrape_pending_urls[929a62e6-dd8a-41d5-92ea-ee192c6923cb] succeeded in 0.002138799987733364s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,045: INFO/MainProcess] Task tasks.scrape_pending_urls[8f248038-8853-4552-bb02-41303dac235a] received
[2026-03-30 02:16:04,048: INFO/MainProcess] Task tasks.scrape_pending_urls[8f248038-8853-4552-bb02-41303dac235a] succeeded in 0.002401100005954504s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,049: INFO/MainProcess] Task tasks.scrape_pending_urls[ef907feb-e25e-4832-8ba5-d31b4c12d918] received
[2026-03-30 02:16:04,052: INFO/MainProcess] Task tasks.scrape_pending_urls[ef907feb-e25e-4832-8ba5-d31b4c12d918] succeeded in 0.002851499943062663s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,054: INFO/MainProcess] Task tasks.scrape_pending_urls[be0b30e1-93c4-4055-b1bc-9a7cfab8704c] received
[2026-03-30 02:16:04,056: INFO/MainProcess] Task tasks.scrape_pending_urls[be0b30e1-93c4-4055-b1bc-9a7cfab8704c] succeeded in 0.002140600001439452s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,057: INFO/MainProcess] Task tasks.scrape_pending_urls[f30c27bd-c4da-4d2e-8a5b-7d2114b4588f] received
[2026-03-30 02:16:04,060: INFO/MainProcess] Task tasks.scrape_pending_urls[f30c27bd-c4da-4d2e-8a5b-7d2114b4588f] succeeded in 0.0020239000441506505s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,061: INFO/MainProcess] Task tasks.scrape_pending_urls[5d89e61e-5737-41da-bcf0-b6fb6dda038b] received
[2026-03-30 02:16:04,063: INFO/MainProcess] Task tasks.scrape_pending_urls[5d89e61e-5737-41da-bcf0-b6fb6dda038b] succeeded in 0.001999799977056682s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,064: INFO/MainProcess] Task tasks.scrape_pending_urls[d7a32a63-8155-4a6c-9727-e883571471c8] received
[2026-03-30 02:16:04,067: INFO/MainProcess] Task tasks.scrape_pending_urls[d7a32a63-8155-4a6c-9727-e883571471c8] succeeded in 0.0019487999379634857s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,068: INFO/MainProcess] Task tasks.scrape_pending_urls[ca70f489-5fb6-4e3e-a54f-22f8ece0f09a] received
[2026-03-30 02:16:04,072: INFO/MainProcess] Task tasks.scrape_pending_urls[ca70f489-5fb6-4e3e-a54f-22f8ece0f09a] succeeded in 0.002862399909645319s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,073: INFO/MainProcess] Task tasks.scrape_pending_urls[5ab96149-cb41-4a07-8c9d-3f1fa1f1fa29] received
[2026-03-30 02:16:04,075: INFO/MainProcess] Task tasks.scrape_pending_urls[5ab96149-cb41-4a07-8c9d-3f1fa1f1fa29] succeeded in 0.002113900030963123s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,077: INFO/MainProcess] Task tasks.scrape_pending_urls[e0c8c96c-6cd2-4c01-a861-0866f82ddade] received
[2026-03-30 02:16:04,079: INFO/MainProcess] Task tasks.scrape_pending_urls[e0c8c96c-6cd2-4c01-a861-0866f82ddade] succeeded in 0.002035799901932478s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,080: INFO/MainProcess] Task tasks.scrape_pending_urls[fa4211ab-aa71-4973-8cac-8c8ecbf80065] received
[2026-03-30 02:16:04,082: INFO/MainProcess] Task tasks.scrape_pending_urls[fa4211ab-aa71-4973-8cac-8c8ecbf80065] succeeded in 0.0019662000704556704s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,084: INFO/MainProcess] Task tasks.scrape_pending_urls[8e4fc7e6-0131-4bf7-9a41-a39778f4163b] received
[2026-03-30 02:16:04,087: INFO/MainProcess] Task tasks.scrape_pending_urls[8e4fc7e6-0131-4bf7-9a41-a39778f4163b] succeeded in 0.002409299951978028s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,088: INFO/MainProcess] Task tasks.scrape_pending_urls[4b4d4810-8e38-4301-adf6-a45b8fea2066] received
[2026-03-30 02:16:04,091: INFO/MainProcess] Task tasks.scrape_pending_urls[4b4d4810-8e38-4301-adf6-a45b8fea2066] succeeded in 0.002070500049740076s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,092: INFO/MainProcess] Task tasks.scrape_pending_urls[cb727dbe-c02a-415c-8a48-5109c4033b09] received
[2026-03-30 02:16:04,094: INFO/MainProcess] Task tasks.scrape_pending_urls[cb727dbe-c02a-415c-8a48-5109c4033b09] succeeded in 0.001986699993722141s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,095: INFO/MainProcess] Task tasks.scrape_pending_urls[76489433-3de8-4087-961c-4d937ab38897] received
[2026-03-30 02:16:04,098: INFO/MainProcess] Task tasks.scrape_pending_urls[76489433-3de8-4087-961c-4d937ab38897] succeeded in 0.002016299986280501s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,100: INFO/MainProcess] Task tasks.scrape_pending_urls[38fc7ada-897c-419a-85ca-3a2a200ffe22] received
[2026-03-30 02:16:04,103: INFO/MainProcess] Task tasks.scrape_pending_urls[38fc7ada-897c-419a-85ca-3a2a200ffe22] succeeded in 0.0024514999240636826s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,104: INFO/MainProcess] Task tasks.scrape_pending_urls[880e4ba9-d01d-4716-b521-880b3122c9f1] received
[2026-03-30 02:16:04,106: INFO/MainProcess] Task tasks.scrape_pending_urls[880e4ba9-d01d-4716-b521-880b3122c9f1] succeeded in 0.001998000079765916s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,107: INFO/MainProcess] Task tasks.scrape_pending_urls[632e8210-5369-4da4-86a6-1ec9d98d68cc] received
[2026-03-30 02:16:04,110: INFO/MainProcess] Task tasks.scrape_pending_urls[632e8210-5369-4da4-86a6-1ec9d98d68cc] succeeded in 0.0020514000207185745s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,111: INFO/MainProcess] Task tasks.scrape_pending_urls[d8b7f446-be68-4103-8176-4ed2e7913b0f] received
[2026-03-30 02:16:04,113: INFO/MainProcess] Task tasks.scrape_pending_urls[d8b7f446-be68-4103-8176-4ed2e7913b0f] succeeded in 0.001968099968507886s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,114: INFO/MainProcess] Task tasks.scrape_pending_urls[fb832389-aefa-4986-9226-0da4dac46d15] received
[2026-03-30 02:16:04,119: INFO/MainProcess] Task tasks.scrape_pending_urls[fb832389-aefa-4986-9226-0da4dac46d15] succeeded in 0.0027404000284150243s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,120: INFO/MainProcess] Task tasks.scrape_pending_urls[2e1850d9-9021-474f-b172-b6a50364d3b1] received
[2026-03-30 02:16:04,123: INFO/MainProcess] Task tasks.scrape_pending_urls[2e1850d9-9021-474f-b172-b6a50364d3b1] succeeded in 0.002655099960975349s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,125: INFO/MainProcess] Task tasks.scrape_pending_urls[df9531dc-2d14-4250-a13f-04764c16987d] received
[2026-03-30 02:16:04,127: INFO/MainProcess] Task tasks.scrape_pending_urls[df9531dc-2d14-4250-a13f-04764c16987d] succeeded in 0.002171000000089407s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,128: INFO/MainProcess] Task tasks.scrape_pending_urls[dfa4205a-0be4-4800-8a18-44b46b6f32d7] received
[2026-03-30 02:16:04,131: INFO/MainProcess] Task tasks.scrape_pending_urls[dfa4205a-0be4-4800-8a18-44b46b6f32d7] succeeded in 0.002707500010728836s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,133: INFO/MainProcess] Task tasks.scrape_pending_urls[32aff7bd-f23c-4279-b2a9-ac9e4100272c] received
[2026-03-30 02:16:04,135: INFO/MainProcess] Task tasks.scrape_pending_urls[32aff7bd-f23c-4279-b2a9-ac9e4100272c] succeeded in 0.0022220000391826034s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,136: INFO/MainProcess] Task tasks.scrape_pending_urls[41c80134-c911-4a9c-882f-661990741313] received
[2026-03-30 02:16:04,139: INFO/MainProcess] Task tasks.scrape_pending_urls[41c80134-c911-4a9c-882f-661990741313] succeeded in 0.0020378000335767865s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,140: INFO/MainProcess] Task tasks.scrape_pending_urls[c3e97f61-a63a-431a-9550-b0cf10f83696] received
[2026-03-30 02:16:04,142: INFO/MainProcess] Task tasks.scrape_pending_urls[c3e97f61-a63a-431a-9550-b0cf10f83696] succeeded in 0.0020001999801024795s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,143: INFO/MainProcess] Task tasks.scrape_pending_urls[9b09f677-ea50-4cfb-be12-7658b43ce8d3] received
[2026-03-30 02:16:04,146: INFO/MainProcess] Task tasks.scrape_pending_urls[9b09f677-ea50-4cfb-be12-7658b43ce8d3] succeeded in 0.0020641000010073185s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,149: INFO/MainProcess] Task tasks.scrape_pending_urls[df4e9803-982b-4004-ae72-d3afc7d66f62] received
[2026-03-30 02:16:04,153: INFO/MainProcess] Task tasks.scrape_pending_urls[df4e9803-982b-4004-ae72-d3afc7d66f62] succeeded in 0.0035258999560028315s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,154: INFO/MainProcess] Task tasks.scrape_pending_urls[85b9b1e1-79c0-489b-ab51-6b0c468df724] received
[2026-03-30 02:16:04,157: INFO/MainProcess] Task tasks.scrape_pending_urls[85b9b1e1-79c0-489b-ab51-6b0c468df724] succeeded in 0.0022268000757321715s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,158: INFO/MainProcess] Task tasks.scrape_pending_urls[07e43632-cf86-41a7-9b78-5db8d479355a] received
[2026-03-30 02:16:04,160: INFO/MainProcess] Task tasks.scrape_pending_urls[07e43632-cf86-41a7-9b78-5db8d479355a] succeeded in 0.0020679000299423933s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,161: INFO/MainProcess] Task tasks.scrape_pending_urls[ecb104cc-f9cc-457e-95b5-ca0bc89eb2dd] received
[2026-03-30 02:16:04,166: INFO/MainProcess] Task tasks.scrape_pending_urls[ecb104cc-f9cc-457e-95b5-ca0bc89eb2dd] succeeded in 0.0045816999627277255s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,168: INFO/MainProcess] Task tasks.scrape_pending_urls[1deeffa4-2b62-450c-bf7c-8d38c29ca2cd] received
[2026-03-30 02:16:04,171: INFO/MainProcess] Task tasks.scrape_pending_urls[1deeffa4-2b62-450c-bf7c-8d38c29ca2cd] succeeded in 0.0025252000195905566s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,172: INFO/MainProcess] Task tasks.scrape_pending_urls[30ec4403-e835-4830-9b9c-1309914c7ab7] received
[2026-03-30 02:16:04,175: INFO/MainProcess] Task tasks.scrape_pending_urls[30ec4403-e835-4830-9b9c-1309914c7ab7] succeeded in 0.002449900028295815s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,176: INFO/MainProcess] Task tasks.scrape_pending_urls[29a97363-1999-4b1f-b06a-5717a1151740] received
[2026-03-30 02:16:04,179: INFO/MainProcess] Task tasks.scrape_pending_urls[29a97363-1999-4b1f-b06a-5717a1151740] succeeded in 0.0027836000081151724s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,182: INFO/MainProcess] Task tasks.scrape_pending_urls[005818b3-87da-4822-9fd7-be1da3e20a74] received
[2026-03-30 02:16:04,185: INFO/MainProcess] Task tasks.scrape_pending_urls[005818b3-87da-4822-9fd7-be1da3e20a74] succeeded in 0.002169799990952015s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,186: INFO/MainProcess] Task tasks.scrape_pending_urls[7b38f60e-fd9f-4160-8415-144d1697d41e] received
[2026-03-30 02:16:04,188: INFO/MainProcess] Task tasks.scrape_pending_urls[7b38f60e-fd9f-4160-8415-144d1697d41e] succeeded in 0.001996799954213202s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,189: INFO/MainProcess] Task tasks.scrape_pending_urls[75f6ae53-1585-4981-97cb-ed4dfb7a16d4] received
[2026-03-30 02:16:04,191: INFO/MainProcess] Task tasks.scrape_pending_urls[75f6ae53-1585-4981-97cb-ed4dfb7a16d4] succeeded in 0.001975199906155467s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,193: INFO/MainProcess] Task tasks.scrape_pending_urls[c0b1289e-46bb-412b-bd79-c3511100f6ec] received
[2026-03-30 02:16:04,196: INFO/MainProcess] Task tasks.scrape_pending_urls[c0b1289e-46bb-412b-bd79-c3511100f6ec] succeeded in 0.00353789993096143s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,198: INFO/MainProcess] Task tasks.scrape_pending_urls[b71e79f9-24ac-4fce-bfc9-c4cc8e238d8a] received
[2026-03-30 02:16:04,200: INFO/MainProcess] Task tasks.scrape_pending_urls[b71e79f9-24ac-4fce-bfc9-c4cc8e238d8a] succeeded in 0.002086500055156648s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,201: INFO/MainProcess] Task tasks.scrape_pending_urls[3d443ad1-44a9-4324-8ecb-61c35588b9c6] received
[2026-03-30 02:16:04,204: INFO/MainProcess] Task tasks.scrape_pending_urls[3d443ad1-44a9-4324-8ecb-61c35588b9c6] succeeded in 0.0020403999369591475s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,205: INFO/MainProcess] Task tasks.scrape_pending_urls[897b5e45-bb5e-4488-9b39-c023543ffb01] received
[2026-03-30 02:16:04,208: INFO/MainProcess] Task tasks.scrape_pending_urls[897b5e45-bb5e-4488-9b39-c023543ffb01] succeeded in 0.002697099931538105s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,209: INFO/MainProcess] Task tasks.scrape_pending_urls[7619edfd-0615-48fe-9504-e542e97b008a] received
[2026-03-30 02:16:04,213: INFO/MainProcess] Task tasks.scrape_pending_urls[7619edfd-0615-48fe-9504-e542e97b008a] succeeded in 0.0023802999639883637s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,214: INFO/MainProcess] Task tasks.scrape_pending_urls[4e1d3c02-1fc3-4233-8e95-ea5d25d2acc9] received
[2026-03-30 02:16:04,216: INFO/MainProcess] Task tasks.scrape_pending_urls[4e1d3c02-1fc3-4233-8e95-ea5d25d2acc9] succeeded in 0.002007500035688281s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,218: INFO/MainProcess] Task tasks.scrape_pending_urls[4555ec98-8853-4bfd-b0c2-a346a61dd932] received
[2026-03-30 02:16:04,220: INFO/MainProcess] Task tasks.scrape_pending_urls[4555ec98-8853-4bfd-b0c2-a346a61dd932] succeeded in 0.0019937000470235944s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,221: INFO/MainProcess] Task tasks.scrape_pending_urls[54caa90f-8aa7-4270-a0a4-14197f50edcf] received
[2026-03-30 02:16:04,223: INFO/MainProcess] Task tasks.scrape_pending_urls[54caa90f-8aa7-4270-a0a4-14197f50edcf] succeeded in 0.001975300023332238s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,225: INFO/MainProcess] Task tasks.scrape_pending_urls[214a5f24-4bba-46ce-b90a-3b4c35ac251c] received
[2026-03-30 02:16:04,229: INFO/MainProcess] Task tasks.scrape_pending_urls[214a5f24-4bba-46ce-b90a-3b4c35ac251c] succeeded in 0.003771199961192906s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,230: INFO/MainProcess] Task tasks.scrape_pending_urls[d67360ef-cae9-4c32-b551-0d4c1cb5f1bd] received
[2026-03-30 02:16:04,233: INFO/MainProcess] Task tasks.scrape_pending_urls[d67360ef-cae9-4c32-b551-0d4c1cb5f1bd] succeeded in 0.002486499957740307s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,234: INFO/MainProcess] Task tasks.scrape_pending_urls[ee70b275-61e5-48fb-a416-2f07b537b043] received
[2026-03-30 02:16:04,237: INFO/MainProcess] Task tasks.scrape_pending_urls[ee70b275-61e5-48fb-a416-2f07b537b043] succeeded in 0.00201339996419847s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,238: INFO/MainProcess] Task tasks.scrape_pending_urls[8cf36b19-a207-4cd8-8638-59cede23f4c5] received
[2026-03-30 02:16:04,240: INFO/MainProcess] Task tasks.scrape_pending_urls[8cf36b19-a207-4cd8-8638-59cede23f4c5] succeeded in 0.0019905000226572156s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,242: INFO/MainProcess] Task tasks.scrape_pending_urls[b05ea0a5-a1d3-41b0-b0fe-9c980e2ac3d6] received
[2026-03-30 02:16:04,244: INFO/MainProcess] Task tasks.scrape_pending_urls[b05ea0a5-a1d3-41b0-b0fe-9c980e2ac3d6] succeeded in 0.002178699942305684s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,246: INFO/MainProcess] Task tasks.scrape_pending_urls[c6bab17f-851f-4cea-a49c-f5d75075e49a] received
[2026-03-30 02:16:04,248: INFO/MainProcess] Task tasks.scrape_pending_urls[c6bab17f-851f-4cea-a49c-f5d75075e49a] succeeded in 0.0020114999497309327s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,249: INFO/MainProcess] Task tasks.scrape_pending_urls[48c42ea3-f34c-42ff-87f8-a121811fc833] received
[2026-03-30 02:16:04,251: INFO/MainProcess] Task tasks.scrape_pending_urls[48c42ea3-f34c-42ff-87f8-a121811fc833] succeeded in 0.0019903999054804444s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,253: INFO/MainProcess] Task tasks.scrape_pending_urls[056f3ccb-3387-4ab7-b82e-f41135af03ef] received
[2026-03-30 02:16:04,255: INFO/MainProcess] Task tasks.scrape_pending_urls[056f3ccb-3387-4ab7-b82e-f41135af03ef] succeeded in 0.001984999980777502s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,256: INFO/MainProcess] Task tasks.scrape_pending_urls[00fc9ed8-dd44-4232-9db2-e2c5ec6e6bb1] received
[2026-03-30 02:16:04,261: INFO/MainProcess] Task tasks.scrape_pending_urls[00fc9ed8-dd44-4232-9db2-e2c5ec6e6bb1] succeeded in 0.002742100041359663s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,262: INFO/MainProcess] Task tasks.scrape_pending_urls[190b3d11-b563-4b04-9eeb-41bd18b509ca] received
[2026-03-30 02:16:04,265: INFO/MainProcess] Task tasks.scrape_pending_urls[190b3d11-b563-4b04-9eeb-41bd18b509ca] succeeded in 0.00223129999358207s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,266: INFO/MainProcess] Task tasks.scrape_pending_urls[6f252dc0-408d-47c1-b8ad-78aafd24d40f] received
[2026-03-30 02:16:04,268: INFO/MainProcess] Task tasks.scrape_pending_urls[6f252dc0-408d-47c1-b8ad-78aafd24d40f] succeeded in 0.002179300063289702s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,269: INFO/MainProcess] Task tasks.scrape_pending_urls[65aecfd9-be7a-4b95-86e7-fa22dbc1aa13] received
[2026-03-30 02:16:04,272: INFO/MainProcess] Task tasks.scrape_pending_urls[65aecfd9-be7a-4b95-86e7-fa22dbc1aa13] succeeded in 0.002175700035877526s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,275: INFO/MainProcess] Task tasks.scrape_pending_urls[df35baee-6977-4c3c-9c59-1cbaf0aaa4b8] received
[2026-03-30 02:16:04,277: INFO/MainProcess] Task tasks.scrape_pending_urls[df35baee-6977-4c3c-9c59-1cbaf0aaa4b8] succeeded in 0.0021997999865561724s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,278: INFO/MainProcess] Task tasks.scrape_pending_urls[ff5d55a2-e120-4a3a-a817-89d5fe67a6fa] received
[2026-03-30 02:16:04,281: INFO/MainProcess] Task tasks.scrape_pending_urls[ff5d55a2-e120-4a3a-a817-89d5fe67a6fa] succeeded in 0.002547499956563115s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,283: INFO/MainProcess] Task tasks.scrape_pending_urls[e4f27570-d9bd-494d-ab15-d415d215e14a] received
[2026-03-30 02:16:04,285: INFO/MainProcess] Task tasks.scrape_pending_urls[e4f27570-d9bd-494d-ab15-d415d215e14a] succeeded in 0.0021044000750407577s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,286: INFO/MainProcess] Task tasks.scrape_pending_urls[d1205d94-5a41-4bca-9edd-25a76ffb58d6] received
[2026-03-30 02:16:04,290: INFO/MainProcess] Task tasks.scrape_pending_urls[d1205d94-5a41-4bca-9edd-25a76ffb58d6] succeeded in 0.0030058000702410936s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,291: INFO/MainProcess] Task tasks.scrape_pending_urls[35c1a04b-015e-41c2-90b5-dc33c1211f96] received
[2026-03-30 02:16:04,295: INFO/MainProcess] Task tasks.scrape_pending_urls[35c1a04b-015e-41c2-90b5-dc33c1211f96] succeeded in 0.003360399976372719s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,297: INFO/MainProcess] Task tasks.scrape_pending_urls[360d9d5d-954a-4950-ab80-03a4bcd1dacf] received
[2026-03-30 02:16:04,301: INFO/MainProcess] Task tasks.scrape_pending_urls[360d9d5d-954a-4950-ab80-03a4bcd1dacf] succeeded in 0.0031970998970791698s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,302: INFO/MainProcess] Task tasks.scrape_pending_urls[8902cbab-a034-44a8-a4b4-1f8717888975] received
[2026-03-30 02:16:04,307: INFO/MainProcess] Task tasks.scrape_pending_urls[8902cbab-a034-44a8-a4b4-1f8717888975] succeeded in 0.0043796999379992485s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,309: INFO/MainProcess] Task tasks.scrape_pending_urls[46096c5a-21f3-4a80-a0ab-38d430f2acb7] received
[2026-03-30 02:16:04,312: INFO/MainProcess] Task tasks.scrape_pending_urls[46096c5a-21f3-4a80-a0ab-38d430f2acb7] succeeded in 0.0031496998853981495s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,314: INFO/MainProcess] Task tasks.scrape_pending_urls[f79de505-755a-4af0-bea0-60149865ed15] received
[2026-03-30 02:16:04,318: INFO/MainProcess] Task tasks.scrape_pending_urls[f79de505-755a-4af0-bea0-60149865ed15] succeeded in 0.003386999946087599s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,321: INFO/MainProcess] Task tasks.scrape_pending_urls[606c4c2a-e32d-44d5-9df1-f79cd1f787a8] received
[2026-03-30 02:16:04,325: INFO/MainProcess] Task tasks.scrape_pending_urls[606c4c2a-e32d-44d5-9df1-f79cd1f787a8] succeeded in 0.003572799963876605s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,327: INFO/MainProcess] Task tasks.scrape_pending_urls[bd317bab-a317-4f8f-a5fa-c92917d06776] received
[2026-03-30 02:16:04,331: INFO/MainProcess] Task tasks.scrape_pending_urls[bd317bab-a317-4f8f-a5fa-c92917d06776] succeeded in 0.0036844999995082617s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,332: INFO/MainProcess] Task tasks.scrape_pending_urls[0be182e4-665f-415c-b013-4d9cec66af6e] received
[2026-03-30 02:16:04,336: INFO/MainProcess] Task tasks.scrape_pending_urls[0be182e4-665f-415c-b013-4d9cec66af6e] succeeded in 0.0036173000698909163s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,340: INFO/MainProcess] Task tasks.scrape_pending_urls[95c08bc8-3833-4015-8baf-40d816669be4] received
[2026-03-30 02:16:04,343: INFO/MainProcess] Task tasks.scrape_pending_urls[95c08bc8-3833-4015-8baf-40d816669be4] succeeded in 0.002772300038486719s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,344: INFO/MainProcess] Task tasks.scrape_pending_urls[62861f72-414e-4322-84d7-7f9bb2c52ea9] received
[2026-03-30 02:16:04,348: INFO/MainProcess] Task tasks.scrape_pending_urls[62861f72-414e-4322-84d7-7f9bb2c52ea9] succeeded in 0.0032395999878644943s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,350: INFO/MainProcess] Task tasks.scrape_pending_urls[d93e6144-f7a6-47e5-b853-96cf51cf9eda] received
[2026-03-30 02:16:04,354: INFO/MainProcess] Task tasks.scrape_pending_urls[d93e6144-f7a6-47e5-b853-96cf51cf9eda] succeeded in 0.0035943000111728907s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,356: INFO/MainProcess] Task tasks.scrape_pending_urls[064397da-e08e-47b0-87fe-505cd13e8079] received
[2026-03-30 02:16:04,360: INFO/MainProcess] Task tasks.scrape_pending_urls[064397da-e08e-47b0-87fe-505cd13e8079] succeeded in 0.0032444000244140625s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,361: INFO/MainProcess] Task tasks.scrape_pending_urls[2ef0949c-5b0e-4bf3-b4d0-f6c22e35c619] received
[2026-03-30 02:16:04,364: INFO/MainProcess] Task tasks.scrape_pending_urls[2ef0949c-5b0e-4bf3-b4d0-f6c22e35c619] succeeded in 0.002794099971652031s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,366: INFO/MainProcess] Task tasks.scrape_pending_urls[c7afb5ae-c80f-4e71-b6c7-a743bb12c1a3] received
[2026-03-30 02:16:04,371: INFO/MainProcess] Task tasks.scrape_pending_urls[c7afb5ae-c80f-4e71-b6c7-a743bb12c1a3] succeeded in 0.004513500025495887s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,373: INFO/MainProcess] Task tasks.scrape_pending_urls[70c883a1-e7df-4116-9d70-61c7cb00b2a9] received
[2026-03-30 02:16:04,376: INFO/MainProcess] Task tasks.scrape_pending_urls[70c883a1-e7df-4116-9d70-61c7cb00b2a9] succeeded in 0.0033212999114766717s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,378: INFO/MainProcess] Task tasks.scrape_pending_urls[136907d5-ea14-460d-87a7-24a84af6e789] received
[2026-03-30 02:16:04,381: INFO/MainProcess] Task tasks.scrape_pending_urls[136907d5-ea14-460d-87a7-24a84af6e789] succeeded in 0.002709300024434924s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,383: INFO/MainProcess] Task tasks.scrape_pending_urls[f50d3fd6-b72f-468e-bbfc-b1a322d6c345] received
[2026-03-30 02:16:04,388: INFO/MainProcess] Task tasks.scrape_pending_urls[f50d3fd6-b72f-468e-bbfc-b1a322d6c345] succeeded in 0.0034896000288426876s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,390: INFO/MainProcess] Task tasks.scrape_pending_urls[0fadc8a9-f292-4383-a634-e3d2db215137] received
[2026-03-30 02:16:04,393: INFO/MainProcess] Task tasks.scrape_pending_urls[0fadc8a9-f292-4383-a634-e3d2db215137] succeeded in 0.0027448999462649226s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,394: INFO/MainProcess] Task tasks.scrape_pending_urls[04c9b870-5a9d-4b84-9157-bdedcc2897f0] received
[2026-03-30 02:16:04,397: INFO/MainProcess] Task tasks.scrape_pending_urls[04c9b870-5a9d-4b84-9157-bdedcc2897f0] succeeded in 0.0025978999910876155s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,399: INFO/MainProcess] Task tasks.scrape_pending_urls[0daf87c7-8de6-4c15-9a28-7178edded0bb] received
[2026-03-30 02:16:04,404: INFO/MainProcess] Task tasks.scrape_pending_urls[0daf87c7-8de6-4c15-9a28-7178edded0bb] succeeded in 0.00318829994648695s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,406: INFO/MainProcess] Task tasks.scrape_pending_urls[26a10890-bfde-49a6-86a5-02ebe6c8231c] received
[2026-03-30 02:16:04,409: INFO/MainProcess] Task tasks.scrape_pending_urls[26a10890-bfde-49a6-86a5-02ebe6c8231c] succeeded in 0.0028220999520272017s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,411: INFO/MainProcess] Task tasks.scrape_pending_urls[04fa8564-ea94-4efe-b7ce-0ccca6933787] received
[2026-03-30 02:16:04,414: INFO/MainProcess] Task tasks.scrape_pending_urls[04fa8564-ea94-4efe-b7ce-0ccca6933787] succeeded in 0.0032940999371930957s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,416: INFO/MainProcess] Task tasks.scrape_pending_urls[e34b357b-4fac-4265-a00f-f66110864b6e] received
[2026-03-30 02:16:04,420: INFO/MainProcess] Task tasks.scrape_pending_urls[e34b357b-4fac-4265-a00f-f66110864b6e] succeeded in 0.0031626999843865633s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,422: INFO/MainProcess] Task tasks.scrape_pending_urls[d4e65ee0-b0d7-4c2d-9c80-4b416d991921] received
[2026-03-30 02:16:04,425: INFO/MainProcess] Task tasks.scrape_pending_urls[d4e65ee0-b0d7-4c2d-9c80-4b416d991921] succeeded in 0.002952600014396012s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,427: INFO/MainProcess] Task tasks.scrape_pending_urls[2a8fbde5-ed4d-4e93-a842-761a55ab927b] received
[2026-03-30 02:16:04,430: INFO/MainProcess] Task tasks.scrape_pending_urls[2a8fbde5-ed4d-4e93-a842-761a55ab927b] succeeded in 0.0032944000558927655s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,433: INFO/MainProcess] Task tasks.scrape_pending_urls[600eb928-6315-41fc-9311-a7d26747d782] received
[2026-03-30 02:16:04,436: INFO/MainProcess] Task tasks.scrape_pending_urls[600eb928-6315-41fc-9311-a7d26747d782] succeeded in 0.003336500027216971s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,438: INFO/MainProcess] Task tasks.scrape_pending_urls[ce75c0e1-8fc5-421e-91fe-3fc9c6cdc894] received
[2026-03-30 02:16:04,441: INFO/MainProcess] Task tasks.scrape_pending_urls[ce75c0e1-8fc5-421e-91fe-3fc9c6cdc894] succeeded in 0.0026838999474421144s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,443: INFO/MainProcess] Task tasks.scrape_pending_urls[0bb99850-de4f-4e41-8eef-eb735f93d89b] received
[2026-03-30 02:16:04,446: INFO/MainProcess] Task tasks.scrape_pending_urls[0bb99850-de4f-4e41-8eef-eb735f93d89b] succeeded in 0.0032483000541105866s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,450: INFO/MainProcess] Task tasks.scrape_pending_urls[17f7a47e-07b2-4488-acd1-6f1cdee7d532] received
[2026-03-30 02:16:04,454: INFO/MainProcess] Task tasks.scrape_pending_urls[17f7a47e-07b2-4488-acd1-6f1cdee7d532] succeeded in 0.0024837000528350472s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,456: INFO/MainProcess] Task tasks.scrape_pending_urls[fa23e7f2-d625-43cd-a3f9-45a8c577d754] received
[2026-03-30 02:16:04,458: INFO/MainProcess] Task tasks.scrape_pending_urls[fa23e7f2-d625-43cd-a3f9-45a8c577d754] succeeded in 0.002276400104165077s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,460: INFO/MainProcess] Task tasks.scrape_pending_urls[108d3a81-30b0-4977-b31b-b0007b53a3ba] received
[2026-03-30 02:16:04,462: INFO/MainProcess] Task tasks.scrape_pending_urls[108d3a81-30b0-4977-b31b-b0007b53a3ba] succeeded in 0.0021943000610917807s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,464: INFO/MainProcess] Task tasks.scrape_pending_urls[9c044096-7a02-4256-8fc1-6e9e7ce90612] received
[2026-03-30 02:16:04,467: INFO/MainProcess] Task tasks.scrape_pending_urls[9c044096-7a02-4256-8fc1-6e9e7ce90612] succeeded in 0.0026860000798478723s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,468: INFO/MainProcess] Task tasks.scrape_pending_urls[d0b0b60d-6e09-49fc-b811-e5eff9ec77d2] received
[2026-03-30 02:16:04,471: INFO/MainProcess] Task tasks.scrape_pending_urls[d0b0b60d-6e09-49fc-b811-e5eff9ec77d2] succeeded in 0.0027199999894946814s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,473: INFO/MainProcess] Task tasks.scrape_pending_urls[5bac0ad4-76ce-4ddd-90db-023eac936043] received
[2026-03-30 02:16:04,476: INFO/MainProcess] Task tasks.scrape_pending_urls[5bac0ad4-76ce-4ddd-90db-023eac936043] succeeded in 0.0032790000550448895s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,478: INFO/MainProcess] Task tasks.scrape_pending_urls[f5d3130a-62ce-467c-bf2b-3ddbf16be974] received
[2026-03-30 02:16:04,483: INFO/MainProcess] Task tasks.scrape_pending_urls[f5d3130a-62ce-467c-bf2b-3ddbf16be974] succeeded in 0.004599600099027157s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,485: INFO/MainProcess] Task tasks.scrape_pending_urls[6ff3c5c7-33e7-4478-9e84-c89625bf9c34] received
[2026-03-30 02:16:04,488: INFO/MainProcess] Task tasks.scrape_pending_urls[6ff3c5c7-33e7-4478-9e84-c89625bf9c34] succeeded in 0.0030360999517142773s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,490: INFO/MainProcess] Task tasks.scrape_pending_urls[f1555d8c-bead-464f-9766-c85f914618e8] received
[2026-03-30 02:16:04,493: INFO/MainProcess] Task tasks.scrape_pending_urls[f1555d8c-bead-464f-9766-c85f914618e8] succeeded in 0.002975500072352588s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,496: INFO/MainProcess] Task tasks.scrape_pending_urls[82f1a975-3c23-44fa-a96d-7d7ed02e6424] received
[2026-03-30 02:16:04,500: INFO/MainProcess] Task tasks.scrape_pending_urls[82f1a975-3c23-44fa-a96d-7d7ed02e6424] succeeded in 0.004061699961312115s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,503: INFO/MainProcess] Task tasks.scrape_pending_urls[edf2242f-421e-4c5f-a5c9-1d739b4bfbaa] received
[2026-03-30 02:16:04,506: INFO/MainProcess] Task tasks.scrape_pending_urls[edf2242f-421e-4c5f-a5c9-1d739b4bfbaa] succeeded in 0.0030816999496892095s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,508: INFO/MainProcess] Task tasks.scrape_pending_urls[9a081155-58b6-479f-b96c-c173ffa25d83] received
[2026-03-30 02:16:04,513: INFO/MainProcess] Task tasks.scrape_pending_urls[9a081155-58b6-479f-b96c-c173ffa25d83] succeeded in 0.004978800076059997s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,516: INFO/MainProcess] Task tasks.scrape_pending_urls[4c6009da-861a-43e5-9705-78c45de0b4cb] received
[2026-03-30 02:16:04,519: INFO/MainProcess] Task tasks.scrape_pending_urls[4c6009da-861a-43e5-9705-78c45de0b4cb] succeeded in 0.0031367000192403793s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,521: INFO/MainProcess] Task tasks.scrape_pending_urls[2865c8d7-e12c-496f-9a1b-a9536b0f8372] received
[2026-03-30 02:16:04,524: INFO/MainProcess] Task tasks.scrape_pending_urls[2865c8d7-e12c-496f-9a1b-a9536b0f8372] succeeded in 0.0029961999971419573s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,526: INFO/MainProcess] Task tasks.scrape_pending_urls[696b3016-a6f2-4388-810d-ce3afcf15ef0] received
[2026-03-30 02:16:04,530: INFO/MainProcess] Task tasks.scrape_pending_urls[696b3016-a6f2-4388-810d-ce3afcf15ef0] succeeded in 0.0033922999864444137s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,532: INFO/MainProcess] Task tasks.scrape_pending_urls[413a8333-652e-4a7a-b595-644f196c52e8] received
[2026-03-30 02:16:04,536: INFO/MainProcess] Task tasks.scrape_pending_urls[413a8333-652e-4a7a-b595-644f196c52e8] succeeded in 0.002993099973537028s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,538: INFO/MainProcess] Task tasks.scrape_pending_urls[ed38c76e-fec6-4b33-89e2-1d9356aecd1a] received
[2026-03-30 02:16:04,541: INFO/MainProcess] Task tasks.scrape_pending_urls[ed38c76e-fec6-4b33-89e2-1d9356aecd1a] succeeded in 0.002959200064651668s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,544: INFO/MainProcess] Task tasks.scrape_pending_urls[101dfb2c-f6da-40e4-bd3a-48d4aef25d76] received
[2026-03-30 02:16:04,548: INFO/MainProcess] Task tasks.scrape_pending_urls[101dfb2c-f6da-40e4-bd3a-48d4aef25d76] succeeded in 0.0030782000394538045s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,550: INFO/MainProcess] Task tasks.scrape_pending_urls[06122c71-c69d-4d3c-819c-fdbe6bac919b] received
[2026-03-30 02:16:04,554: INFO/MainProcess] Task tasks.scrape_pending_urls[06122c71-c69d-4d3c-819c-fdbe6bac919b] succeeded in 0.002927200053818524s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,555: INFO/MainProcess] Task tasks.scrape_pending_urls[81818e66-0365-4b6d-a082-2b1355bf8604] received
[2026-03-30 02:16:04,559: INFO/MainProcess] Task tasks.scrape_pending_urls[81818e66-0365-4b6d-a082-2b1355bf8604] succeeded in 0.0035186000168323517s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,561: INFO/MainProcess] Task tasks.scrape_pending_urls[fd2384fd-4065-4bee-ae9a-a153aafe78b0] received
[2026-03-30 02:16:04,564: INFO/MainProcess] Task tasks.scrape_pending_urls[fd2384fd-4065-4bee-ae9a-a153aafe78b0] succeeded in 0.002980499994009733s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,566: INFO/MainProcess] Task tasks.scrape_pending_urls[d8f6519b-7d65-4924-9041-03651b1b6f23] received
[2026-03-30 02:16:04,569: INFO/MainProcess] Task tasks.scrape_pending_urls[d8f6519b-7d65-4924-9041-03651b1b6f23] succeeded in 0.0027965999906882644s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,571: INFO/MainProcess] Task tasks.scrape_pending_urls[c5a77796-4d90-44d0-a8b6-c36f02d478b7] received
[2026-03-30 02:16:04,574: INFO/MainProcess] Task tasks.scrape_pending_urls[c5a77796-4d90-44d0-a8b6-c36f02d478b7] succeeded in 0.003002400044351816s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,578: INFO/MainProcess] Task tasks.scrape_pending_urls[de839f38-94d7-4dd1-9382-836d90956b89] received
[2026-03-30 02:16:04,581: INFO/MainProcess] Task tasks.scrape_pending_urls[de839f38-94d7-4dd1-9382-836d90956b89] succeeded in 0.0030746000120416284s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,583: INFO/MainProcess] Task tasks.scrape_pending_urls[6d209734-0df9-4e11-b9f1-05ed15d78744] received
[2026-03-30 02:16:04,586: INFO/MainProcess] Task tasks.scrape_pending_urls[6d209734-0df9-4e11-b9f1-05ed15d78744] succeeded in 0.0029610999627038836s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,588: INFO/MainProcess] Task tasks.scrape_pending_urls[e386af92-e0db-4e02-9b8f-5ff886943339] received
[2026-03-30 02:16:04,592: INFO/MainProcess] Task tasks.scrape_pending_urls[e386af92-e0db-4e02-9b8f-5ff886943339] succeeded in 0.00368780002463609s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,593: INFO/MainProcess] Task tasks.scrape_pending_urls[09614f2e-e149-4043-8633-4b86049a2b25] received
[2026-03-30 02:16:04,596: INFO/MainProcess] Task tasks.scrape_pending_urls[09614f2e-e149-4043-8633-4b86049a2b25] succeeded in 0.0028135000029578805s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,598: INFO/MainProcess] Task tasks.scrape_pending_urls[1e690cb9-d80b-41d4-a183-ac40de814543] received
[2026-03-30 02:16:04,600: INFO/MainProcess] Task tasks.scrape_pending_urls[1e690cb9-d80b-41d4-a183-ac40de814543] succeeded in 0.002153599984012544s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,601: INFO/MainProcess] Task tasks.scrape_pending_urls[c3b8e56e-fd44-40e6-86c3-e763ee0f3863] received
[2026-03-30 02:16:04,603: INFO/MainProcess] Task tasks.scrape_pending_urls[c3b8e56e-fd44-40e6-86c3-e763ee0f3863] succeeded in 0.0020733000710606575s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,605: INFO/MainProcess] Task tasks.scrape_pending_urls[662a2683-2aec-46d9-b592-a70c9ac80a21] received
[2026-03-30 02:16:04,610: INFO/MainProcess] Task tasks.scrape_pending_urls[662a2683-2aec-46d9-b592-a70c9ac80a21] succeeded in 0.004439999931491911s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,611: INFO/MainProcess] Task tasks.scrape_pending_urls[9be867d2-497d-4fc0-af17-4de1a77383f4] received
[2026-03-30 02:16:04,615: INFO/MainProcess] Task tasks.scrape_pending_urls[9be867d2-497d-4fc0-af17-4de1a77383f4] succeeded in 0.0030404001008719206s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,616: INFO/MainProcess] Task tasks.scrape_pending_urls[092eb3c7-f9e8-45c0-9b6f-bd3cad75a52b] received
[2026-03-30 02:16:04,620: INFO/MainProcess] Task tasks.scrape_pending_urls[092eb3c7-f9e8-45c0-9b6f-bd3cad75a52b] succeeded in 0.00292449991684407s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,622: INFO/MainProcess] Task tasks.scrape_pending_urls[98528330-648c-446b-96c4-ea54a5eaa4ce] received
[2026-03-30 02:16:04,626: INFO/MainProcess] Task tasks.scrape_pending_urls[98528330-648c-446b-96c4-ea54a5eaa4ce] succeeded in 0.003530000103637576s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,628: INFO/MainProcess] Task tasks.scrape_pending_urls[b5b3963d-c2ae-4657-ba7c-43d829a252a6] received
[2026-03-30 02:16:04,632: INFO/MainProcess] Task tasks.scrape_pending_urls[b5b3963d-c2ae-4657-ba7c-43d829a252a6] succeeded in 0.002908000024035573s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,633: INFO/MainProcess] Task tasks.scrape_pending_urls[2e7651f6-8bc0-491d-88ce-7ab3e5810ee2] received
[2026-03-30 02:16:04,636: INFO/MainProcess] Task tasks.scrape_pending_urls[2e7651f6-8bc0-491d-88ce-7ab3e5810ee2] succeeded in 0.0027800999814644456s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,640: INFO/MainProcess] Task tasks.scrape_pending_urls[37f9364e-a2c5-4b48-9937-9145dc5a2323] received
[2026-03-30 02:16:04,644: INFO/MainProcess] Task tasks.scrape_pending_urls[37f9364e-a2c5-4b48-9937-9145dc5a2323] succeeded in 0.0038629999617114663s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,646: INFO/MainProcess] Task tasks.scrape_pending_urls[cfc81a34-d90e-4eca-a2ec-4eec997f6efd] received
[2026-03-30 02:16:04,649: INFO/MainProcess] Task tasks.scrape_pending_urls[cfc81a34-d90e-4eca-a2ec-4eec997f6efd] succeeded in 0.0029737999429926276s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,651: INFO/MainProcess] Task tasks.scrape_pending_urls[d03167c7-b7d9-42eb-8525-7a2ed030c907] received
[2026-03-30 02:16:04,655: INFO/MainProcess] Task tasks.scrape_pending_urls[d03167c7-b7d9-42eb-8525-7a2ed030c907] succeeded in 0.003629899933002889s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,657: INFO/MainProcess] Task tasks.scrape_pending_urls[7f402a7b-2605-4336-9fae-0997f56ca650] received
[2026-03-30 02:16:04,660: INFO/MainProcess] Task tasks.scrape_pending_urls[7f402a7b-2605-4336-9fae-0997f56ca650] succeeded in 0.00299579999409616s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,662: INFO/MainProcess] Task tasks.scrape_pending_urls[53b55e22-03c3-47d0-8cc7-bd83ea402ad9] received
[2026-03-30 02:16:04,665: INFO/MainProcess] Task tasks.scrape_pending_urls[53b55e22-03c3-47d0-8cc7-bd83ea402ad9] succeeded in 0.0029904000693932176s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,667: INFO/MainProcess] Task tasks.scrape_pending_urls[baaf51c1-f1b0-48e0-9f50-70e42d14686c] received
[2026-03-30 02:16:04,673: INFO/MainProcess] Task tasks.scrape_pending_urls[baaf51c1-f1b0-48e0-9f50-70e42d14686c] succeeded in 0.005747399991378188s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,675: INFO/MainProcess] Task tasks.scrape_pending_urls[d4c1f15e-974c-4d01-9780-3630fd137679] received
[2026-03-30 02:16:04,678: INFO/MainProcess] Task tasks.scrape_pending_urls[d4c1f15e-974c-4d01-9780-3630fd137679] succeeded in 0.0033064999151974916s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,680: INFO/MainProcess] Task tasks.scrape_pending_urls[21d07215-c2ab-45da-a086-823917589174] received
[2026-03-30 02:16:04,683: INFO/MainProcess] Task tasks.scrape_pending_urls[21d07215-c2ab-45da-a086-823917589174] succeeded in 0.002980799996294081s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,686: INFO/MainProcess] Task tasks.scrape_pending_urls[34b624dd-2f49-4493-9968-4cbe837219b9] received
[2026-03-30 02:16:04,690: INFO/MainProcess] Task tasks.scrape_pending_urls[34b624dd-2f49-4493-9968-4cbe837219b9] succeeded in 0.0029676000121980906s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,692: INFO/MainProcess] Task tasks.scrape_pending_urls[303c636c-fbd1-4a7a-b516-6aaeaf1856ad] received
[2026-03-30 02:16:04,695: INFO/MainProcess] Task tasks.scrape_pending_urls[303c636c-fbd1-4a7a-b516-6aaeaf1856ad] succeeded in 0.0034353999653831124s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,697: INFO/MainProcess] Task tasks.scrape_pending_urls[bba27851-5ccc-4cb2-aa8f-d3b89b50f2ef] received
[2026-03-30 02:16:04,701: INFO/MainProcess] Task tasks.scrape_pending_urls[bba27851-5ccc-4cb2-aa8f-d3b89b50f2ef] succeeded in 0.0038831999991089106s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,703: INFO/MainProcess] Task tasks.scrape_pending_urls[5ddc30e1-e974-4f4a-b655-46dd9823db82] received
[2026-03-30 02:16:04,706: INFO/MainProcess] Task tasks.scrape_pending_urls[5ddc30e1-e974-4f4a-b655-46dd9823db82] succeeded in 0.0024902999866753817s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,708: INFO/MainProcess] Task tasks.scrape_pending_urls[6dc90723-489e-43b9-b34a-585f380a068e] received
[2026-03-30 02:16:04,710: INFO/MainProcess] Task tasks.scrape_pending_urls[6dc90723-489e-43b9-b34a-585f380a068e] succeeded in 0.0020326999947428703s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,711: INFO/MainProcess] Task tasks.scrape_pending_urls[3ae59ad1-5ba4-428e-a519-bd0af76c4419] received
[2026-03-30 02:16:04,713: INFO/MainProcess] Task tasks.scrape_pending_urls[3ae59ad1-5ba4-428e-a519-bd0af76c4419] succeeded in 0.001990600023418665s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,715: INFO/MainProcess] Task tasks.scrape_pending_urls[549f9116-898f-4580-b1b9-8863be3915de] received
[2026-03-30 02:16:04,719: INFO/MainProcess] Task tasks.scrape_pending_urls[549f9116-898f-4580-b1b9-8863be3915de] succeeded in 0.0039296000031754375s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,720: INFO/MainProcess] Task tasks.scrape_pending_urls[d60ebb92-5c29-430e-93e3-9c3fc3422d0c] received
[2026-03-30 02:16:04,723: INFO/MainProcess] Task tasks.scrape_pending_urls[d60ebb92-5c29-430e-93e3-9c3fc3422d0c] succeeded in 0.002661600010469556s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,725: INFO/MainProcess] Task tasks.scrape_pending_urls[9057a88b-4868-47bf-8c9b-ae36610754d2] received
[2026-03-30 02:16:04,728: INFO/MainProcess] Task tasks.scrape_pending_urls[9057a88b-4868-47bf-8c9b-ae36610754d2] succeeded in 0.002753300010226667s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,729: INFO/MainProcess] Task tasks.scrape_pending_urls[ad9b92c1-71d5-41ff-abf2-a1c234db8a74] received
[2026-03-30 02:16:04,733: INFO/MainProcess] Task tasks.scrape_pending_urls[ad9b92c1-71d5-41ff-abf2-a1c234db8a74] succeeded in 0.003573399968445301s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,735: INFO/MainProcess] Task tasks.scrape_pending_urls[7036d597-c2d1-4e2f-9ce5-a9e544cd2007] received
[2026-03-30 02:16:04,738: INFO/MainProcess] Task tasks.scrape_pending_urls[7036d597-c2d1-4e2f-9ce5-a9e544cd2007] succeeded in 0.0028478000313043594s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,740: INFO/MainProcess] Task tasks.scrape_pending_urls[9736ba75-eaa3-4284-805b-ffb6b9940c01] received
[2026-03-30 02:16:04,743: INFO/MainProcess] Task tasks.scrape_pending_urls[9736ba75-eaa3-4284-805b-ffb6b9940c01] succeeded in 0.00271869997959584s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,744: INFO/MainProcess] Task tasks.scrape_pending_urls[316dbbaf-ffc8-4f6c-9e18-affb0724581f] received
[2026-03-30 02:16:04,748: INFO/MainProcess] Task tasks.scrape_pending_urls[316dbbaf-ffc8-4f6c-9e18-affb0724581f] succeeded in 0.0032322999322786927s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,750: INFO/MainProcess] Task tasks.scrape_pending_urls[35c3cc92-febc-4168-91e5-807a771811b9] received
[2026-03-30 02:16:04,753: INFO/MainProcess] Task tasks.scrape_pending_urls[35c3cc92-febc-4168-91e5-807a771811b9] succeeded in 0.0027289000572636724s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,754: INFO/MainProcess] Task tasks.scrape_pending_urls[8c49ca94-4a59-4f65-b9ca-cf56aab3e04c] received
[2026-03-30 02:16:04,757: INFO/MainProcess] Task tasks.scrape_pending_urls[8c49ca94-4a59-4f65-b9ca-cf56aab3e04c] succeeded in 0.0026194999227300286s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,758: INFO/MainProcess] Task tasks.scrape_pending_urls[2bc63ca2-b05b-4cf3-b525-4a0d4c443e09] received
[2026-03-30 02:16:04,761: INFO/MainProcess] Task tasks.scrape_pending_urls[2bc63ca2-b05b-4cf3-b525-4a0d4c443e09] succeeded in 0.00269210000988096s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,763: INFO/MainProcess] Task tasks.scrape_pending_urls[003c7204-8d16-4027-b051-40b82b10b6dc] received
[2026-03-30 02:16:04,769: INFO/MainProcess] Task tasks.scrape_pending_urls[003c7204-8d16-4027-b051-40b82b10b6dc] succeeded in 0.004139799973927438s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,771: INFO/MainProcess] Task tasks.scrape_pending_urls[ce5198d3-18f8-45c4-99fb-b5ef7e3c184b] received
[2026-03-30 02:16:04,775: INFO/MainProcess] Task tasks.scrape_pending_urls[ce5198d3-18f8-45c4-99fb-b5ef7e3c184b] succeeded in 0.0036032000789418817s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,777: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d82f49-c97f-45a5-a62a-29f2aaf3d405] received
[2026-03-30 02:16:04,782: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d82f49-c97f-45a5-a62a-29f2aaf3d405] succeeded in 0.0045362000819295645s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,784: INFO/MainProcess] Task tasks.scrape_pending_urls[a63ffff8-8e5a-4de8-aa6b-79f9f4fc8a09] received
[2026-03-30 02:16:04,787: INFO/MainProcess] Task tasks.scrape_pending_urls[a63ffff8-8e5a-4de8-aa6b-79f9f4fc8a09] succeeded in 0.0026379000628367066s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,788: INFO/MainProcess] Task tasks.scrape_pending_urls[a91b2447-5698-4483-9c8f-156074ce5315] received
[2026-03-30 02:16:04,791: INFO/MainProcess] Task tasks.scrape_pending_urls[a91b2447-5698-4483-9c8f-156074ce5315] succeeded in 0.002704199985601008s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,793: INFO/MainProcess] Task tasks.scrape_pending_urls[010dd1d0-473f-4523-8c47-512c0736649d] received
[2026-03-30 02:16:04,798: INFO/MainProcess] Task tasks.scrape_pending_urls[010dd1d0-473f-4523-8c47-512c0736649d] succeeded in 0.004723599995486438s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,800: INFO/MainProcess] Task tasks.scrape_pending_urls[692229b8-3122-4762-8241-d40466fb5909] received
[2026-03-30 02:16:04,803: INFO/MainProcess] Task tasks.scrape_pending_urls[692229b8-3122-4762-8241-d40466fb5909] succeeded in 0.003468800103291869s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,805: INFO/MainProcess] Task tasks.scrape_pending_urls[c11eba35-9225-4046-ba3c-5d81b38027c8] received
[2026-03-30 02:16:04,809: INFO/MainProcess] Task tasks.scrape_pending_urls[c11eba35-9225-4046-ba3c-5d81b38027c8] succeeded in 0.00341189990285784s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,812: INFO/MainProcess] Task tasks.scrape_pending_urls[d9db8017-2791-473d-8707-d421d04e3427] received
[2026-03-30 02:16:04,815: INFO/MainProcess] Task tasks.scrape_pending_urls[d9db8017-2791-473d-8707-d421d04e3427] succeeded in 0.002897599944844842s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,817: INFO/MainProcess] Task tasks.scrape_pending_urls[2d83c526-b718-4393-9b83-bef443bd1af1] received
[2026-03-30 02:16:04,821: INFO/MainProcess] Task tasks.scrape_pending_urls[2d83c526-b718-4393-9b83-bef443bd1af1] succeeded in 0.003701400011777878s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,823: INFO/MainProcess] Task tasks.scrape_pending_urls[06b04f8b-0894-4076-a7e6-33daa332dd04] received
[2026-03-30 02:16:04,828: INFO/MainProcess] Task tasks.scrape_pending_urls[06b04f8b-0894-4076-a7e6-33daa332dd04] succeeded in 0.005088999983854592s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,831: INFO/MainProcess] Task tasks.scrape_pending_urls[fc7aad39-5b63-46d7-afe5-ea16a1b92e3d] received
[2026-03-30 02:16:04,835: INFO/MainProcess] Task tasks.scrape_pending_urls[fc7aad39-5b63-46d7-afe5-ea16a1b92e3d] succeeded in 0.003778400016017258s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,838: INFO/MainProcess] Task tasks.scrape_pending_urls[6944feff-02d1-4a0e-be50-622abbf9b786] received
[2026-03-30 02:16:04,841: INFO/MainProcess] Task tasks.scrape_pending_urls[6944feff-02d1-4a0e-be50-622abbf9b786] succeeded in 0.0034361000871285796s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,845: INFO/MainProcess] Task tasks.scrape_pending_urls[e541c579-7119-4973-b559-94744e76ac3e] received
[2026-03-30 02:16:04,849: INFO/MainProcess] Task tasks.scrape_pending_urls[e541c579-7119-4973-b559-94744e76ac3e] succeeded in 0.0038013000739738345s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,851: INFO/MainProcess] Task tasks.scrape_pending_urls[45a81889-3be3-4347-87b0-aacf1d68ee61] received
[2026-03-30 02:16:04,853: INFO/MainProcess] Task tasks.scrape_pending_urls[45a81889-3be3-4347-87b0-aacf1d68ee61] succeeded in 0.002566699986346066s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,855: INFO/MainProcess] Task tasks.scrape_pending_urls[331b44a1-d56b-4ed6-b07b-9557d3b422a0] received
[2026-03-30 02:16:04,859: INFO/MainProcess] Task tasks.scrape_pending_urls[331b44a1-d56b-4ed6-b07b-9557d3b422a0] succeeded in 0.0033928999910131097s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,861: INFO/MainProcess] Task tasks.scrape_pending_urls[ec8ad0d0-1b17-44c7-9ee5-bae0f86adb74] received
[2026-03-30 02:16:04,864: INFO/MainProcess] Task tasks.scrape_pending_urls[ec8ad0d0-1b17-44c7-9ee5-bae0f86adb74] succeeded in 0.003233299939893186s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,866: INFO/MainProcess] Task tasks.scrape_pending_urls[e9abe8d4-b4bf-45bb-b291-085b4683f40e] received
[2026-03-30 02:16:04,869: INFO/MainProcess] Task tasks.scrape_pending_urls[e9abe8d4-b4bf-45bb-b291-085b4683f40e] succeeded in 0.002683199942111969s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,871: INFO/MainProcess] Task tasks.scrape_pending_urls[bf838c4b-aa1d-46db-a6f3-099c2e2b7b51] received
[2026-03-30 02:16:04,875: INFO/MainProcess] Task tasks.scrape_pending_urls[bf838c4b-aa1d-46db-a6f3-099c2e2b7b51] succeeded in 0.003974199993535876s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,877: INFO/MainProcess] Task tasks.scrape_pending_urls[7e7a7f7c-a3e8-4f5b-a342-9172bf65080e] received
[2026-03-30 02:16:04,880: INFO/MainProcess] Task tasks.scrape_pending_urls[7e7a7f7c-a3e8-4f5b-a342-9172bf65080e] succeeded in 0.0030768000287935138s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,882: INFO/MainProcess] Task tasks.scrape_pending_urls[790a556e-f73c-4745-bf6b-3999bb2b1cc7] received
[2026-03-30 02:16:04,886: INFO/MainProcess] Task tasks.scrape_pending_urls[790a556e-f73c-4745-bf6b-3999bb2b1cc7] succeeded in 0.00306079990696162s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,888: INFO/MainProcess] Task tasks.scrape_pending_urls[154595a5-15e5-4e10-81b7-cae967502411] received
[2026-03-30 02:16:04,893: INFO/MainProcess] Task tasks.scrape_pending_urls[154595a5-15e5-4e10-81b7-cae967502411] succeeded in 0.005447199917398393s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,895: INFO/MainProcess] Task tasks.scrape_pending_urls[ebc40914-8d74-44a8-afbd-e22f0ec78ad3] received
[2026-03-30 02:16:04,898: INFO/MainProcess] Task tasks.scrape_pending_urls[ebc40914-8d74-44a8-afbd-e22f0ec78ad3] succeeded in 0.002373899915255606s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,899: INFO/MainProcess] Task tasks.scrape_pending_urls[a8a283be-861b-40cc-8f6f-64e883107979] received
[2026-03-30 02:16:04,902: INFO/MainProcess] Task tasks.scrape_pending_urls[a8a283be-861b-40cc-8f6f-64e883107979] succeeded in 0.002574999933131039s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,903: INFO/MainProcess] Task tasks.scrape_pending_urls[d2e0f5a0-b654-4d29-b47b-ebc67ab1ab2c] received
[2026-03-30 02:16:04,907: INFO/MainProcess] Task tasks.scrape_pending_urls[d2e0f5a0-b654-4d29-b47b-ebc67ab1ab2c] succeeded in 0.003291000030003488s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,908: INFO/MainProcess] Task tasks.scrape_pending_urls[18b7436c-f6e2-4b0f-9d8d-edd1e2fb18fb] received
[2026-03-30 02:16:04,910: INFO/MainProcess] Task tasks.scrape_pending_urls[18b7436c-f6e2-4b0f-9d8d-edd1e2fb18fb] succeeded in 0.0021825999720022082s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,912: INFO/MainProcess] Task tasks.scrape_pending_urls[5cf24a6f-13c6-4e2f-bd35-5bc6e5e5d3d8] received
[2026-03-30 02:16:04,914: INFO/MainProcess] Task tasks.scrape_pending_urls[5cf24a6f-13c6-4e2f-bd35-5bc6e5e5d3d8] succeeded in 0.0021782000549137592s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,915: INFO/MainProcess] Task tasks.scrape_pending_urls[fe454f3b-4f13-4541-8717-6fabdd256b88] received
[2026-03-30 02:16:04,918: INFO/MainProcess] Task tasks.scrape_pending_urls[fe454f3b-4f13-4541-8717-6fabdd256b88] succeeded in 0.0021212000865489244s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,919: INFO/MainProcess] Task tasks.scrape_pending_urls[0f1e9653-532b-49f9-829c-26f421152d63] received
[2026-03-30 02:16:04,923: INFO/MainProcess] Task tasks.scrape_pending_urls[0f1e9653-532b-49f9-829c-26f421152d63] succeeded in 0.003737600054591894s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,925: INFO/MainProcess] Task tasks.scrape_pending_urls[8ca385af-02e5-4c62-81f0-396f737c2c22] received
[2026-03-30 02:16:04,928: INFO/MainProcess] Task tasks.scrape_pending_urls[8ca385af-02e5-4c62-81f0-396f737c2c22] succeeded in 0.0028918000170961022s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,930: INFO/MainProcess] Task tasks.scrape_pending_urls[9b9d81b4-06aa-4df7-ad21-1da70c52bf47] received
[2026-03-30 02:16:04,932: INFO/MainProcess] Task tasks.scrape_pending_urls[9b9d81b4-06aa-4df7-ad21-1da70c52bf47] succeeded in 0.002687099971808493s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,934: INFO/MainProcess] Task tasks.scrape_pending_urls[29416e90-96f4-4efa-a0cf-7a05fa9d7f46] received
[2026-03-30 02:16:04,936: INFO/MainProcess] Task tasks.scrape_pending_urls[29416e90-96f4-4efa-a0cf-7a05fa9d7f46] succeeded in 0.002504599979147315s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,938: INFO/MainProcess] Task tasks.scrape_pending_urls[e658faba-1860-48b6-b8f9-277af5beedd0] received
[2026-03-30 02:16:04,940: INFO/MainProcess] Task tasks.scrape_pending_urls[e658faba-1860-48b6-b8f9-277af5beedd0] succeeded in 0.002295200014486909s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,942: INFO/MainProcess] Task tasks.scrape_pending_urls[b8e68fd2-7c1d-4063-a96c-c8b162a75ea7] received
[2026-03-30 02:16:04,944: INFO/MainProcess] Task tasks.scrape_pending_urls[b8e68fd2-7c1d-4063-a96c-c8b162a75ea7] succeeded in 0.0021727000130340457s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,945: INFO/MainProcess] Task tasks.scrape_pending_urls[a783df55-1950-4c70-9a7a-f3e5cfba7dcd] received
[2026-03-30 02:16:04,948: INFO/MainProcess] Task tasks.scrape_pending_urls[a783df55-1950-4c70-9a7a-f3e5cfba7dcd] succeeded in 0.002111600013449788s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,949: INFO/MainProcess] Task tasks.scrape_pending_urls[5efbb897-4686-43f5-b807-0b13c077bb39] received
[2026-03-30 02:16:04,951: INFO/MainProcess] Task tasks.scrape_pending_urls[5efbb897-4686-43f5-b807-0b13c077bb39] succeeded in 0.0020755999721586704s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,954: INFO/MainProcess] Task tasks.scrape_pending_urls[4bc098f2-9649-456d-861e-e5fc0eb3955b] received
[2026-03-30 02:16:04,957: INFO/MainProcess] Task tasks.scrape_pending_urls[4bc098f2-9649-456d-861e-e5fc0eb3955b] succeeded in 0.002498699934221804s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,959: INFO/MainProcess] Task tasks.scrape_pending_urls[853a9a49-0f99-445c-8a92-e28bfb33c565] received
[2026-03-30 02:16:04,961: INFO/MainProcess] Task tasks.scrape_pending_urls[853a9a49-0f99-445c-8a92-e28bfb33c565] succeeded in 0.0021471999352797866s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,962: INFO/MainProcess] Task tasks.scrape_pending_urls[e5e79dc4-c9f9-4ee0-90c2-44caf3d0663a] received
[2026-03-30 02:16:04,965: INFO/MainProcess] Task tasks.scrape_pending_urls[e5e79dc4-c9f9-4ee0-90c2-44caf3d0663a] succeeded in 0.002127800020389259s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,966: INFO/MainProcess] Task tasks.scrape_pending_urls[c508d604-c708-4a28-9651-a76b51a50c66] received
[2026-03-30 02:16:04,969: INFO/MainProcess] Task tasks.scrape_pending_urls[c508d604-c708-4a28-9651-a76b51a50c66] succeeded in 0.0025511999847367406s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,970: INFO/MainProcess] Task tasks.scrape_pending_urls[fd23c10f-5388-4105-a57f-36d9b2ea23a5] received
[2026-03-30 02:16:04,972: INFO/MainProcess] Task tasks.scrape_pending_urls[fd23c10f-5388-4105-a57f-36d9b2ea23a5] succeeded in 0.0021898000268265605s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,973: INFO/MainProcess] Task tasks.scrape_pending_urls[c8d6a990-9bac-4f78-9646-a5d12dcecbd9] received
[2026-03-30 02:16:04,976: INFO/MainProcess] Task tasks.scrape_pending_urls[c8d6a990-9bac-4f78-9646-a5d12dcecbd9] succeeded in 0.0021030999487265944s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,977: INFO/MainProcess] Task tasks.scrape_pending_urls[bb936799-237d-4b3e-8f12-3d3bbcd1942b] received
[2026-03-30 02:16:04,979: INFO/MainProcess] Task tasks.scrape_pending_urls[bb936799-237d-4b3e-8f12-3d3bbcd1942b] succeeded in 0.0020984000293537974s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,981: INFO/MainProcess] Task tasks.scrape_pending_urls[9655354d-4489-4d26-a7ee-6ba5480bc964] received
[2026-03-30 02:16:04,984: INFO/MainProcess] Task tasks.scrape_pending_urls[9655354d-4489-4d26-a7ee-6ba5480bc964] succeeded in 0.0032885000109672546s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,986: INFO/MainProcess] Task tasks.scrape_pending_urls[ca01d43a-484d-4364-9680-837240c1308e] received
[2026-03-30 02:16:04,988: INFO/MainProcess] Task tasks.scrape_pending_urls[ca01d43a-484d-4364-9680-837240c1308e] succeeded in 0.002261799992993474s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,989: INFO/MainProcess] Task tasks.scrape_pending_urls[db82817c-381f-47f6-b5fb-d954bdb2eed2] received
[2026-03-30 02:16:04,992: INFO/MainProcess] Task tasks.scrape_pending_urls[db82817c-381f-47f6-b5fb-d954bdb2eed2] succeeded in 0.0021364999702200294s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,993: INFO/MainProcess] Task tasks.scrape_pending_urls[bd5043f0-9f17-4bf5-a9e6-80b11ba59f92] received
[2026-03-30 02:16:04,995: INFO/MainProcess] Task tasks.scrape_pending_urls[bd5043f0-9f17-4bf5-a9e6-80b11ba59f92] succeeded in 0.002159200026653707s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:04,996: INFO/MainProcess] Task tasks.scrape_pending_urls[ee18f822-50ec-4c02-877c-9bb346049c45] received
[2026-03-30 02:16:04,999: INFO/MainProcess] Task tasks.scrape_pending_urls[ee18f822-50ec-4c02-877c-9bb346049c45] succeeded in 0.002170200110413134s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,002: INFO/MainProcess] Task tasks.scrape_pending_urls[b139c5b6-fe30-47b9-afcf-213fb6199851] received
[2026-03-30 02:16:05,004: INFO/MainProcess] Task tasks.scrape_pending_urls[b139c5b6-fe30-47b9-afcf-213fb6199851] succeeded in 0.002201499999500811s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,005: INFO/MainProcess] Task tasks.scrape_pending_urls[31cfd802-0e68-449e-83e7-6bc83d540efe] received
[2026-03-30 02:16:05,008: INFO/MainProcess] Task tasks.scrape_pending_urls[31cfd802-0e68-449e-83e7-6bc83d540efe] succeeded in 0.002737000002525747s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,010: INFO/MainProcess] Task tasks.scrape_pending_urls[0a013b5f-05e4-4e25-b45a-f78a9ddf8a38] received
[2026-03-30 02:16:05,012: INFO/MainProcess] Task tasks.scrape_pending_urls[0a013b5f-05e4-4e25-b45a-f78a9ddf8a38] succeeded in 0.0020880999509245157s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,013: INFO/MainProcess] Task tasks.scrape_pending_urls[58124eca-20c3-496e-bf05-749e6d1eb2ac] received
[2026-03-30 02:16:05,016: INFO/MainProcess] Task tasks.scrape_pending_urls[58124eca-20c3-496e-bf05-749e6d1eb2ac] succeeded in 0.002502499963156879s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,017: INFO/MainProcess] Task tasks.scrape_pending_urls[d369aa91-78fa-4d0f-849c-f2dd3a87574d] received
[2026-03-30 02:16:05,020: INFO/MainProcess] Task tasks.scrape_pending_urls[d369aa91-78fa-4d0f-849c-f2dd3a87574d] succeeded in 0.0020602999720722437s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,021: INFO/MainProcess] Task tasks.scrape_pending_urls[fae64b09-03bd-4210-90f7-b17ab1d7ff8e] received
[2026-03-30 02:16:05,023: INFO/MainProcess] Task tasks.scrape_pending_urls[fae64b09-03bd-4210-90f7-b17ab1d7ff8e] succeeded in 0.002052400028333068s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,024: INFO/MainProcess] Task tasks.scrape_pending_urls[81547caa-5cb8-4b68-916f-45a93491a77b] received
[2026-03-30 02:16:05,027: INFO/MainProcess] Task tasks.scrape_pending_urls[81547caa-5cb8-4b68-916f-45a93491a77b] succeeded in 0.001981500070542097s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:05,028: INFO/MainProcess] Task tasks.scrape_pending_urls[458f88e4-8e8e-4018-b4df-fe3a50ecf713] received
[2026-03-30 02:16:05,030: INFO/MainProcess] Task tasks.scrape_pending_urls[458f88e4-8e8e-4018-b4df-fe3a50ecf713] succeeded in 0.0019410999957472086s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[312dfa2a-334e-4c96-8196-c0f0c2dc648c] received
[2026-03-30 02:16:17,586: INFO/MainProcess] Task tasks.scrape_pending_urls[312dfa2a-334e-4c96-8196-c0f0c2dc648c] succeeded in 0.003515399992465973s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:16:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[f510318d-fbf8-440f-8ea7-e79cd45cc53d] received
[2026-03-30 02:16:47,585: INFO/MainProcess] Task tasks.scrape_pending_urls[f510318d-fbf8-440f-8ea7-e79cd45cc53d] succeeded in 0.002641600091010332s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:17:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[855cdb1e-fe14-4247-8094-36ebc0b21d33] received
[2026-03-30 02:17:17,585: INFO/MainProcess] Task tasks.scrape_pending_urls[855cdb1e-fe14-4247-8094-36ebc0b21d33] succeeded in 0.0027411000337451696s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:17:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[3d55c9bc-65e6-4abe-bebb-c118109747ba] received
[2026-03-30 02:17:47,585: INFO/MainProcess] Task tasks.scrape_pending_urls[3d55c9bc-65e6-4abe-bebb-c118109747ba] succeeded in 0.0025375999975949526s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:18:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[ee5ec75c-60b2-4105-87b4-d8212c403059] received
[2026-03-30 02:18:17,585: INFO/MainProcess] Task tasks.scrape_pending_urls[ee5ec75c-60b2-4105-87b4-d8212c403059] succeeded in 0.0029944999841973186s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:18:47,482: INFO/MainProcess] Task tasks.reset_stale_processing_urls[9afb5f47-317b-4fcb-8ef8-977b922d38f0] received
[2026-03-30 02:18:47,485: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:18:47,486: INFO/MainProcess] Task tasks.reset_stale_processing_urls[9afb5f47-317b-4fcb-8ef8-977b922d38f0] succeeded in 0.0031186999985948205s: {'reset': 0}
[2026-03-30 02:18:47,490: INFO/MainProcess] Task tasks.collect_system_metrics[ce958ab2-6cdc-4e12-b300-e124df5b6f42] received
[2026-03-30 02:18:48,006: INFO/MainProcess] Task tasks.collect_system_metrics[ce958ab2-6cdc-4e12-b300-e124df5b6f42] succeeded in 0.5154638999374583s: {'cpu': 17.4, 'memory': 46.0}
[2026-03-30 02:18:48,008: INFO/MainProcess] Task tasks.scrape_pending_urls[4b3cab8c-a339-4eb1-afdc-43350370cf5b] received
[2026-03-30 02:18:48,015: INFO/MainProcess] Task tasks.scrape_pending_urls[4b3cab8c-a339-4eb1-afdc-43350370cf5b] succeeded in 0.0065744000021368265s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:19:17,583: INFO/MainProcess] Task tasks.scrape_pending_urls[013582da-357b-4f16-8226-660e76c0860a] received
[2026-03-30 02:19:17,586: INFO/MainProcess] Task tasks.scrape_pending_urls[013582da-357b-4f16-8226-660e76c0860a] succeeded in 0.0026852000737562776s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:19:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[5435f467-88a8-4150-a7d8-cc562befdcbc] received
[2026-03-30 02:19:47,585: INFO/MainProcess] Task tasks.scrape_pending_urls[5435f467-88a8-4150-a7d8-cc562befdcbc] succeeded in 0.002807099954225123s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:20:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[a2de5278-5f31-4b22-87eb-0559d74ba9f0] received
[2026-03-30 02:20:17,586: INFO/MainProcess] Task tasks.scrape_pending_urls[a2de5278-5f31-4b22-87eb-0559d74ba9f0] succeeded in 0.002854499965906143s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:20:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b88d3a-50ec-4055-af6e-068af63d66e5] received
[2026-03-30 02:20:47,585: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b88d3a-50ec-4055-af6e-068af63d66e5] succeeded in 0.002799699897877872s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:21:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[01e82a49-9b9d-425d-bfdd-4f9a3e308512] received
[2026-03-30 02:21:17,585: INFO/MainProcess] Task tasks.scrape_pending_urls[01e82a49-9b9d-425d-bfdd-4f9a3e308512] succeeded in 0.002762200077995658s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:21:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[51c5ee4e-c490-4bff-b4fb-4671c1b45a71] received
[2026-03-30 02:21:47,585: INFO/MainProcess] Task tasks.scrape_pending_urls[51c5ee4e-c490-4bff-b4fb-4671c1b45a71] succeeded in 0.0027396000223234296s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:22:17,583: INFO/MainProcess] Task tasks.scrape_pending_urls[77eba6d7-cfb6-407b-bf77-34a01bb1df69] received
[2026-03-30 02:22:17,586: INFO/MainProcess] Task tasks.scrape_pending_urls[77eba6d7-cfb6-407b-bf77-34a01bb1df69] succeeded in 0.0026889999862760305s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:22:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[5b5741f4-b42c-4aa5-ac2d-4cce1174f235] received
[2026-03-30 02:22:47,585: INFO/MainProcess] Task tasks.scrape_pending_urls[5b5741f4-b42c-4aa5-ac2d-4cce1174f235] succeeded in 0.002605200046673417s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:23:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[6f13115b-a37e-4f07-bffd-57c71e959b49] received
[2026-03-30 02:23:17,585: INFO/MainProcess] Task tasks.scrape_pending_urls[6f13115b-a37e-4f07-bffd-57c71e959b49] succeeded in 0.002626699977554381s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:23:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[f81c5644-99fb-4b1c-a2d4-beacd69b9190] received
[2026-03-30 02:23:48,013: INFO/MainProcess] Task tasks.collect_system_metrics[f81c5644-99fb-4b1c-a2d4-beacd69b9190] succeeded in 0.5162052999949083s: {'cpu': 10.2, 'memory': 46.2}
[2026-03-30 02:23:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[bcc8c721-7c02-45e1-a6f7-da115459f97c] received
[2026-03-30 02:23:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[bcc8c721-7c02-45e1-a6f7-da115459f97c] succeeded in 0.00233189994469285s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:24:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[625f6f0a-885b-478f-8159-6e12228715a4] received
[2026-03-30 02:24:17,585: INFO/MainProcess] Task tasks.scrape_pending_urls[625f6f0a-885b-478f-8159-6e12228715a4] succeeded in 0.0026926000136882067s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:24:47,582: INFO/MainProcess] Task tasks.scrape_pending_urls[00483057-b5c6-4ec1-a581-a7fccaead450] received
[2026-03-30 02:24:47,586: INFO/MainProcess] Task tasks.scrape_pending_urls[00483057-b5c6-4ec1-a581-a7fccaead450] succeeded in 0.0029105000430718064s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:25:17,583: INFO/MainProcess] Task tasks.scrape_pending_urls[b7d6c90e-2d90-404d-8f3d-b73b311ef3ab] received
[2026-03-30 02:25:17,586: INFO/MainProcess] Task tasks.scrape_pending_urls[b7d6c90e-2d90-404d-8f3d-b73b311ef3ab] succeeded in 0.0030661000637337565s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:25:47,583: INFO/MainProcess] Task tasks.scrape_pending_urls[32f07392-b11d-408c-8db1-9414c91c5388] received
[2026-03-30 02:25:47,586: INFO/MainProcess] Task tasks.scrape_pending_urls[32f07392-b11d-408c-8db1-9414c91c5388] succeeded in 0.0028162000235170126s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:26:17,582: INFO/MainProcess] Task tasks.scrape_pending_urls[ff5b9c3b-975d-4744-99b1-31435f03696c] received
[2026-03-30 02:26:17,585: INFO/MainProcess] Task tasks.scrape_pending_urls[ff5b9c3b-975d-4744-99b1-31435f03696c] succeeded in 0.002832300029695034s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:26:47,587: INFO/MainProcess] Task tasks.scrape_pending_urls[47706461-ad18-44dc-9d98-82eb6c5246df] received
[2026-03-30 02:26:47,671: INFO/MainProcess] Task tasks.scrape_pending_urls[47706461-ad18-44dc-9d98-82eb6c5246df] succeeded in 0.08363350003492087s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:27:17,587: INFO/MainProcess] Task tasks.scrape_pending_urls[b5b8510e-6102-4f25-99bb-4340eb28552a] received
[2026-03-30 02:27:17,590: INFO/MainProcess] Task tasks.scrape_pending_urls[b5b8510e-6102-4f25-99bb-4340eb28552a] succeeded in 0.0027434000512585044s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:27:47,588: INFO/MainProcess] Task tasks.scrape_pending_urls[ce40b60c-6e34-478e-9e56-58b209684b9a] received
[2026-03-30 02:27:47,591: INFO/MainProcess] Task tasks.scrape_pending_urls[ce40b60c-6e34-478e-9e56-58b209684b9a] succeeded in 0.002747500082477927s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:28:17,587: INFO/MainProcess] Task tasks.scrape_pending_urls[e45e91ad-66b9-426a-bbb3-705a84655d0d] received
[2026-03-30 02:28:17,590: INFO/MainProcess] Task tasks.scrape_pending_urls[e45e91ad-66b9-426a-bbb3-705a84655d0d] succeeded in 0.0027142000617459416s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:28:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[477c63ea-ea4b-4929-ba4a-7479ec581cf7] received
[2026-03-30 02:28:48,012: INFO/MainProcess] Task tasks.collect_system_metrics[477c63ea-ea4b-4929-ba4a-7479ec581cf7] succeeded in 0.5160318000707775s: {'cpu': 13.3, 'memory': 46.1}
[2026-03-30 02:28:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[95665a7c-047d-425a-9d57-df103bf2f3b3] received
[2026-03-30 02:28:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[95665a7c-047d-425a-9d57-df103bf2f3b3] succeeded in 0.0022239000536501408s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:29:17,587: INFO/MainProcess] Task tasks.scrape_pending_urls[abe6ebf2-91ef-4dc2-b34b-ac7b1365fc8b] received
[2026-03-30 02:29:17,590: INFO/MainProcess] Task tasks.scrape_pending_urls[abe6ebf2-91ef-4dc2-b34b-ac7b1365fc8b] succeeded in 0.0028380000730976462s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:29:47,587: INFO/MainProcess] Task tasks.scrape_pending_urls[5f0918ec-712f-4807-887d-288ff1444f07] received
[2026-03-30 02:29:47,590: INFO/MainProcess] Task tasks.scrape_pending_urls[5f0918ec-712f-4807-887d-288ff1444f07] succeeded in 0.0025927999522536993s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[54f84f6b-cc8d-4d5f-936c-ee44d5831d20] received
[2026-03-30 02:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[54f84f6b-cc8d-4d5f-936c-ee44d5831d20] succeeded in 0.001470100018195808s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 02:30:17,586: INFO/MainProcess] Task tasks.scrape_pending_urls[beddf2f3-3f6b-4bf3-b6a3-0ca3d8f264a9] received
[2026-03-30 02:30:17,589: INFO/MainProcess] Task tasks.scrape_pending_urls[beddf2f3-3f6b-4bf3-b6a3-0ca3d8f264a9] succeeded in 0.002613699994981289s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:30:47,587: INFO/MainProcess] Task tasks.scrape_pending_urls[8a3a79c5-83b9-40ae-b2da-ae9670178cee] received
[2026-03-30 02:30:47,590: INFO/MainProcess] Task tasks.scrape_pending_urls[8a3a79c5-83b9-40ae-b2da-ae9670178cee] succeeded in 0.002939100028015673s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:31:17,587: INFO/MainProcess] Task tasks.scrape_pending_urls[5cfbd914-8827-4246-bffd-d7b9f9d033bc] received
[2026-03-30 02:31:17,590: INFO/MainProcess] Task tasks.scrape_pending_urls[5cfbd914-8827-4246-bffd-d7b9f9d033bc] succeeded in 0.002876899903640151s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:31:47,587: INFO/MainProcess] Task tasks.scrape_pending_urls[797d453b-a7ac-4f85-9028-4ccb945a5a61] received
[2026-03-30 02:31:47,649: INFO/MainProcess] Task tasks.scrape_pending_urls[797d453b-a7ac-4f85-9028-4ccb945a5a61] succeeded in 0.06196550000458956s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:32:17,587: INFO/MainProcess] Task tasks.scrape_pending_urls[04669118-8679-4fa1-a9c5-a9f56e6843ad] received
[2026-03-30 02:32:17,590: INFO/MainProcess] Task tasks.scrape_pending_urls[04669118-8679-4fa1-a9c5-a9f56e6843ad] succeeded in 0.002695900038816035s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:32:47,587: INFO/MainProcess] Task tasks.scrape_pending_urls[aecc7e2c-a358-48e3-a431-b00fa1517035] received
[2026-03-30 02:32:47,590: INFO/MainProcess] Task tasks.scrape_pending_urls[aecc7e2c-a358-48e3-a431-b00fa1517035] succeeded in 0.0028980999486520886s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:33:17,591: INFO/MainProcess] Task tasks.scrape_pending_urls[053ed01a-de98-4da2-b1c9-9e9aae8bb46d] received
[2026-03-30 02:33:17,595: INFO/MainProcess] Task tasks.scrape_pending_urls[053ed01a-de98-4da2-b1c9-9e9aae8bb46d] succeeded in 0.003131199977360666s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:33:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[0f7aa2d1-50ef-4686-9243-96e1305fe425] received
[2026-03-30 02:33:48,015: INFO/MainProcess] Task tasks.collect_system_metrics[0f7aa2d1-50ef-4686-9243-96e1305fe425] succeeded in 0.5190480999881402s: {'cpu': 10.2, 'memory': 46.3}
[2026-03-30 02:33:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[e20a0db1-efd4-4b7a-b1de-7c98da60fe38] received
[2026-03-30 02:33:48,020: INFO/MainProcess] Task tasks.scrape_pending_urls[e20a0db1-efd4-4b7a-b1de-7c98da60fe38] succeeded in 0.0022108000703155994s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:34:17,592: INFO/MainProcess] Task tasks.scrape_pending_urls[596859b5-d82c-4cf0-b1a0-8f4a0dd9072e] received
[2026-03-30 02:34:17,595: INFO/MainProcess] Task tasks.scrape_pending_urls[596859b5-d82c-4cf0-b1a0-8f4a0dd9072e] succeeded in 0.003106200019828975s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:34:47,591: INFO/MainProcess] Task tasks.scrape_pending_urls[609cd882-d94e-4ade-941b-e704fac2ee92] received
[2026-03-30 02:34:47,594: INFO/MainProcess] Task tasks.scrape_pending_urls[609cd882-d94e-4ade-941b-e704fac2ee92] succeeded in 0.0027975999983027577s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:35:17,591: INFO/MainProcess] Task tasks.scrape_pending_urls[b1188a0b-d110-4b03-b6d1-734e6398fe0b] received
[2026-03-30 02:35:17,595: INFO/MainProcess] Task tasks.scrape_pending_urls[b1188a0b-d110-4b03-b6d1-734e6398fe0b] succeeded in 0.0026914000045508146s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:35:47,591: INFO/MainProcess] Task tasks.scrape_pending_urls[0343aaca-8681-490a-8d4d-5798fa720c66] received
[2026-03-30 02:35:47,595: INFO/MainProcess] Task tasks.scrape_pending_urls[0343aaca-8681-490a-8d4d-5798fa720c66] succeeded in 0.003142499946989119s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:36:17,591: INFO/MainProcess] Task tasks.scrape_pending_urls[4a6a5a4d-0162-4e20-83cd-106b293a062f] received
[2026-03-30 02:36:17,594: INFO/MainProcess] Task tasks.scrape_pending_urls[4a6a5a4d-0162-4e20-83cd-106b293a062f] succeeded in 0.0027771000750362873s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:36:47,591: INFO/MainProcess] Task tasks.scrape_pending_urls[ec0839e8-827b-4401-b2d9-4db232f086a8] received
[2026-03-30 02:36:47,594: INFO/MainProcess] Task tasks.scrape_pending_urls[ec0839e8-827b-4401-b2d9-4db232f086a8] succeeded in 0.0026722000911831856s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:37:17,591: INFO/MainProcess] Task tasks.scrape_pending_urls[2c60ce2c-0e05-4abd-bf6c-3d53a5838090] received
[2026-03-30 02:37:17,595: INFO/MainProcess] Task tasks.scrape_pending_urls[2c60ce2c-0e05-4abd-bf6c-3d53a5838090] succeeded in 0.003017400042153895s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:37:47,591: INFO/MainProcess] Task tasks.scrape_pending_urls[e1e4f564-b598-4837-a463-5bfe190d53db] received
[2026-03-30 02:37:47,595: INFO/MainProcess] Task tasks.scrape_pending_urls[e1e4f564-b598-4837-a463-5bfe190d53db] succeeded in 0.0030814000638201833s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:38:17,591: INFO/MainProcess] Task tasks.scrape_pending_urls[a6110558-a621-43f4-87e5-36d5dea34ea3] received
[2026-03-30 02:38:17,660: INFO/MainProcess] Task tasks.scrape_pending_urls[a6110558-a621-43f4-87e5-36d5dea34ea3] succeeded in 0.06796879996545613s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:38:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[228d9302-c2f7-4880-b1d1-0ab0ccb164b1] received
[2026-03-30 02:38:48,014: INFO/MainProcess] Task tasks.collect_system_metrics[228d9302-c2f7-4880-b1d1-0ab0ccb164b1] succeeded in 0.518045200034976s: {'cpu': 17.4, 'memory': 45.9}
[2026-03-30 02:38:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[6c3929a3-1070-4ecc-9d3a-903ed2ad2f26] received
[2026-03-30 02:38:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[6c3929a3-1070-4ecc-9d3a-903ed2ad2f26] succeeded in 0.002731200074777007s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:39:17,591: INFO/MainProcess] Task tasks.scrape_pending_urls[168de3ee-8b38-4f0c-b303-163f26c50521] received
[2026-03-30 02:39:17,594: INFO/MainProcess] Task tasks.scrape_pending_urls[168de3ee-8b38-4f0c-b303-163f26c50521] succeeded in 0.0027262000367045403s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:39:47,597: INFO/MainProcess] Task tasks.scrape_pending_urls[b84a31a4-9b69-400a-9a55-209cc15d1898] received
[2026-03-30 02:39:47,603: INFO/MainProcess] Task tasks.scrape_pending_urls[b84a31a4-9b69-400a-9a55-209cc15d1898] succeeded in 0.004905200097709894s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:40:17,597: INFO/MainProcess] Task tasks.scrape_pending_urls[bd188e6a-9a20-4499-90df-80f6638f1c0b] received
[2026-03-30 02:40:17,600: INFO/MainProcess] Task tasks.scrape_pending_urls[bd188e6a-9a20-4499-90df-80f6638f1c0b] succeeded in 0.00287279998883605s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:40:47,597: INFO/MainProcess] Task tasks.scrape_pending_urls[b50e89ac-2a72-434b-b85f-1211c30dec0d] received
[2026-03-30 02:40:47,600: INFO/MainProcess] Task tasks.scrape_pending_urls[b50e89ac-2a72-434b-b85f-1211c30dec0d] succeeded in 0.0029311999678611755s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:41:17,597: INFO/MainProcess] Task tasks.scrape_pending_urls[f2fdf614-84c6-4662-bba7-665aa32d7657] received
[2026-03-30 02:41:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[f2fdf614-84c6-4662-bba7-665aa32d7657] succeeded in 0.004057299927808344s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:41:47,597: INFO/MainProcess] Task tasks.scrape_pending_urls[6bdb7e5f-2100-4ffb-a383-785c24c430e7] received
[2026-03-30 02:41:47,600: INFO/MainProcess] Task tasks.scrape_pending_urls[6bdb7e5f-2100-4ffb-a383-785c24c430e7] succeeded in 0.0027953999815508723s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:42:17,597: INFO/MainProcess] Task tasks.scrape_pending_urls[6b0ab497-3654-4e6b-b68f-ec9fbd14b459] received
[2026-03-30 02:42:17,600: INFO/MainProcess] Task tasks.scrape_pending_urls[6b0ab497-3654-4e6b-b68f-ec9fbd14b459] succeeded in 0.0031765999738126993s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:42:47,597: INFO/MainProcess] Task tasks.scrape_pending_urls[60916a1d-da59-4aac-a82a-936b44a005c3] received
[2026-03-30 02:42:47,601: INFO/MainProcess] Task tasks.scrape_pending_urls[60916a1d-da59-4aac-a82a-936b44a005c3] succeeded in 0.0032227999763563275s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:43:17,597: INFO/MainProcess] Task tasks.scrape_pending_urls[143a2c8c-641c-420c-901a-e2444d10f456] received
[2026-03-30 02:43:17,600: INFO/MainProcess] Task tasks.scrape_pending_urls[143a2c8c-641c-420c-901a-e2444d10f456] succeeded in 0.0027944999746978283s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:43:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[44d20105-83f9-4a46-b0c5-813164b69307] received
[2026-03-30 02:43:48,016: INFO/MainProcess] Task tasks.collect_system_metrics[44d20105-83f9-4a46-b0c5-813164b69307] succeeded in 0.5198222000617534s: {'cpu': 10.9, 'memory': 45.8}
[2026-03-30 02:43:48,018: INFO/MainProcess] Task tasks.scrape_pending_urls[883fef90-17b5-4b9f-a510-56f601c6d1b1] received
[2026-03-30 02:43:48,021: INFO/MainProcess] Task tasks.scrape_pending_urls[883fef90-17b5-4b9f-a510-56f601c6d1b1] succeeded in 0.0026011000154539943s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:44:17,597: INFO/MainProcess] Task tasks.scrape_pending_urls[0d985a81-82eb-4143-86fb-c31bf810fb51] received
[2026-03-30 02:44:17,600: INFO/MainProcess] Task tasks.scrape_pending_urls[0d985a81-82eb-4143-86fb-c31bf810fb51] succeeded in 0.0025405000196769834s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:44:47,597: INFO/MainProcess] Task tasks.scrape_pending_urls[4a3e9073-28bd-4be0-be84-cea0bb8262b5] received
[2026-03-30 02:44:47,600: INFO/MainProcess] Task tasks.scrape_pending_urls[4a3e9073-28bd-4be0-be84-cea0bb8262b5] succeeded in 0.0026251000817865133s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:45:17,597: INFO/MainProcess] Task tasks.scrape_pending_urls[45dd8907-3f4f-478b-afcd-82a0104f3323] received
[2026-03-30 02:45:17,600: INFO/MainProcess] Task tasks.scrape_pending_urls[45dd8907-3f4f-478b-afcd-82a0104f3323] succeeded in 0.0027534000109881163s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:45:47,597: INFO/MainProcess] Task tasks.scrape_pending_urls[47036cdf-380e-4c26-9d58-c535729df615] received
[2026-03-30 02:45:47,600: INFO/MainProcess] Task tasks.scrape_pending_urls[47036cdf-380e-4c26-9d58-c535729df615] succeeded in 0.002797099994495511s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:46:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[ff07b178-7016-4f52-b7ee-64399cc75fc5] received
[2026-03-30 02:46:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[ff07b178-7016-4f52-b7ee-64399cc75fc5] succeeded in 0.002868700074031949s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:46:47,601: INFO/MainProcess] Task tasks.scrape_pending_urls[461e8f9e-3e31-422d-966f-6fdda0426008] received
[2026-03-30 02:46:47,604: INFO/MainProcess] Task tasks.scrape_pending_urls[461e8f9e-3e31-422d-966f-6fdda0426008] succeeded in 0.0031052998965606093s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:47:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[2f8d43d7-0131-49cf-8f8f-0c28bb7b05d8] received
[2026-03-30 02:47:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[2f8d43d7-0131-49cf-8f8f-0c28bb7b05d8] succeeded in 0.002603100030682981s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:47:47,601: INFO/MainProcess] Task tasks.scrape_pending_urls[21ef5c7c-867d-41f3-8187-4efcdf72b7c2] received
[2026-03-30 02:47:47,604: INFO/MainProcess] Task tasks.scrape_pending_urls[21ef5c7c-867d-41f3-8187-4efcdf72b7c2] succeeded in 0.002890200004912913s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:48:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[e3e5265d-e1fb-466f-8c06-30bca164242d] received
[2026-03-30 02:48:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[e3e5265d-e1fb-466f-8c06-30bca164242d] succeeded in 0.0027776999631896615s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:48:47,482: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d7a806fd-257e-40f3-be52-da1da5b9e284] received
[2026-03-30 02:48:47,485: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 02:48:47,486: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d7a806fd-257e-40f3-be52-da1da5b9e284] succeeded in 0.003500899998471141s: {'reset': 0}
[2026-03-30 02:48:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[a1ac9784-b56a-42bd-8060-c31fc7056961] received
[2026-03-30 02:48:48,114: INFO/MainProcess] Task tasks.collect_system_metrics[a1ac9784-b56a-42bd-8060-c31fc7056961] succeeded in 0.5173306000651792s: {'cpu': 21.6, 'memory': 45.8}
[2026-03-30 02:48:48,116: INFO/MainProcess] Task tasks.scrape_pending_urls[7736d4a6-f42b-4bc2-9ea7-eb451575faa2] received
[2026-03-30 02:48:48,120: INFO/MainProcess] Task tasks.scrape_pending_urls[7736d4a6-f42b-4bc2-9ea7-eb451575faa2] succeeded in 0.004380600061267614s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:49:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[936860a3-0e73-46d2-8fbb-be71409d5dba] received
[2026-03-30 02:49:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[936860a3-0e73-46d2-8fbb-be71409d5dba] succeeded in 0.002653899951837957s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:49:47,601: INFO/MainProcess] Task tasks.scrape_pending_urls[4f5c4b75-f425-4494-bdcd-3899a70b3afd] received
[2026-03-30 02:49:47,604: INFO/MainProcess] Task tasks.scrape_pending_urls[4f5c4b75-f425-4494-bdcd-3899a70b3afd] succeeded in 0.0027048999909311533s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:50:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[663074c8-a274-4794-a2bd-24a5269930c9] received
[2026-03-30 02:50:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[663074c8-a274-4794-a2bd-24a5269930c9] succeeded in 0.002733799978159368s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:50:47,601: INFO/MainProcess] Task tasks.scrape_pending_urls[878ce668-be7a-41ae-9d1b-6612cf544a99] received
[2026-03-30 02:50:47,604: INFO/MainProcess] Task tasks.scrape_pending_urls[878ce668-be7a-41ae-9d1b-6612cf544a99] succeeded in 0.00268759997561574s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:51:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[1b843a7a-8ff4-4da3-ae88-e46dacecd652] received
[2026-03-30 02:51:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[1b843a7a-8ff4-4da3-ae88-e46dacecd652] succeeded in 0.0027658999897539616s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:51:47,601: INFO/MainProcess] Task tasks.scrape_pending_urls[6fe75416-09b5-4325-ae8c-408679d3178f] received
[2026-03-30 02:51:47,604: INFO/MainProcess] Task tasks.scrape_pending_urls[6fe75416-09b5-4325-ae8c-408679d3178f] succeeded in 0.002702099969610572s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:52:17,601: INFO/MainProcess] Task tasks.scrape_pending_urls[44cdb2ce-272c-47e3-87c1-ca80b3a7d2a0] received
[2026-03-30 02:52:17,604: INFO/MainProcess] Task tasks.scrape_pending_urls[44cdb2ce-272c-47e3-87c1-ca80b3a7d2a0] succeeded in 0.0025819999864324927s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:52:47,606: INFO/MainProcess] Task tasks.scrape_pending_urls[b39a1f12-b362-40a7-99f8-ec07219e93dd] received
[2026-03-30 02:52:47,609: INFO/MainProcess] Task tasks.scrape_pending_urls[b39a1f12-b362-40a7-99f8-ec07219e93dd] succeeded in 0.002628199988976121s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:53:17,606: INFO/MainProcess] Task tasks.scrape_pending_urls[67340b60-15b2-4e45-8015-eaf4c50bbf9f] received
[2026-03-30 02:53:17,609: INFO/MainProcess] Task tasks.scrape_pending_urls[67340b60-15b2-4e45-8015-eaf4c50bbf9f] succeeded in 0.0027632000856101513s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:53:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[e4ecf411-c14a-4ac2-932a-93e078c41a01] received
[2026-03-30 02:53:48,013: INFO/MainProcess] Task tasks.collect_system_metrics[e4ecf411-c14a-4ac2-932a-93e078c41a01] succeeded in 0.5167073000920936s: {'cpu': 10.6, 'memory': 45.9}
[2026-03-30 02:53:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[7a0455bf-2921-45b1-92f1-81614d04d381] received
[2026-03-30 02:53:48,018: INFO/MainProcess] Task tasks.scrape_pending_urls[7a0455bf-2921-45b1-92f1-81614d04d381] succeeded in 0.0026479000225663185s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:54:17,605: INFO/MainProcess] Task tasks.scrape_pending_urls[d50092e6-b614-4268-bdc9-dd846cbd10e2] received
[2026-03-30 02:54:17,608: INFO/MainProcess] Task tasks.scrape_pending_urls[d50092e6-b614-4268-bdc9-dd846cbd10e2] succeeded in 0.0025173999601975083s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:54:47,606: INFO/MainProcess] Task tasks.scrape_pending_urls[116a6f4c-8f97-49ba-95cb-b9508d4151dd] received
[2026-03-30 02:54:47,609: INFO/MainProcess] Task tasks.scrape_pending_urls[116a6f4c-8f97-49ba-95cb-b9508d4151dd] succeeded in 0.0027739000506699085s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:55:17,606: INFO/MainProcess] Task tasks.scrape_pending_urls[962cb8af-bb00-414d-af0f-f60a0ff51afd] received
[2026-03-30 02:55:17,609: INFO/MainProcess] Task tasks.scrape_pending_urls[962cb8af-bb00-414d-af0f-f60a0ff51afd] succeeded in 0.0027872000355273485s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:55:47,606: INFO/MainProcess] Task tasks.scrape_pending_urls[7ae35134-2137-428d-bfa6-d3679897bb82] received
[2026-03-30 02:55:47,609: INFO/MainProcess] Task tasks.scrape_pending_urls[7ae35134-2137-428d-bfa6-d3679897bb82] succeeded in 0.0026724000927060843s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:56:17,606: INFO/MainProcess] Task tasks.scrape_pending_urls[30ee1723-7807-4017-bcc8-9e23d48e32dd] received
[2026-03-30 02:56:17,608: INFO/MainProcess] Task tasks.scrape_pending_urls[30ee1723-7807-4017-bcc8-9e23d48e32dd] succeeded in 0.0026223999448120594s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:56:47,606: INFO/MainProcess] Task tasks.scrape_pending_urls[9abe2d40-d645-4683-b85c-97301372cdd6] received
[2026-03-30 02:56:47,609: INFO/MainProcess] Task tasks.scrape_pending_urls[9abe2d40-d645-4683-b85c-97301372cdd6] succeeded in 0.0028252999763935804s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:57:17,606: INFO/MainProcess] Task tasks.scrape_pending_urls[52462fa2-ea91-4d8e-a356-0b938ad9421c] received
[2026-03-30 02:57:17,609: INFO/MainProcess] Task tasks.scrape_pending_urls[52462fa2-ea91-4d8e-a356-0b938ad9421c] succeeded in 0.0026102999690920115s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:57:47,606: INFO/MainProcess] Task tasks.scrape_pending_urls[b7542977-ae28-42dd-bc38-0697ffd9c976] received
[2026-03-30 02:57:47,609: INFO/MainProcess] Task tasks.scrape_pending_urls[b7542977-ae28-42dd-bc38-0697ffd9c976] succeeded in 0.002602800028398633s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:58:17,605: INFO/MainProcess] Task tasks.scrape_pending_urls[9bf55b7c-1f7d-4ef9-a5d1-ae224dbe1371] received
[2026-03-30 02:58:17,608: INFO/MainProcess] Task tasks.scrape_pending_urls[9bf55b7c-1f7d-4ef9-a5d1-ae224dbe1371] succeeded in 0.0028421999886631966s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:58:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[e84beca9-d3c0-454a-98ea-9fd094aad65e] received
[2026-03-30 02:58:48,012: INFO/MainProcess] Task tasks.collect_system_metrics[e84beca9-d3c0-454a-98ea-9fd094aad65e] succeeded in 0.5162427000468597s: {'cpu': 16.0, 'memory': 45.5}
[2026-03-30 02:58:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[8c8fa298-a09f-4a74-b945-bdffd141a94a] received
[2026-03-30 02:58:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[8c8fa298-a09f-4a74-b945-bdffd141a94a] succeeded in 0.0022456999868154526s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:59:17,611: INFO/MainProcess] Task tasks.scrape_pending_urls[3e0fbdff-b26e-4de2-926c-0187f062a9f9] received
[2026-03-30 02:59:17,614: INFO/MainProcess] Task tasks.scrape_pending_urls[3e0fbdff-b26e-4de2-926c-0187f062a9f9] succeeded in 0.002538300002925098s: {'status': 'idle', 'pending': 0}
[2026-03-30 02:59:47,611: INFO/MainProcess] Task tasks.scrape_pending_urls[c3068b4d-1cb7-4941-84d1-be7491ce8ab1] received
[2026-03-30 02:59:47,614: INFO/MainProcess] Task tasks.scrape_pending_urls[c3068b4d-1cb7-4941-84d1-be7491ce8ab1] succeeded in 0.002685000072233379s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:00:17,610: INFO/MainProcess] Task tasks.scrape_pending_urls[8e4aac77-faaa-45fb-9f60-49316e30c2b5] received
[2026-03-30 03:00:17,613: INFO/MainProcess] Task tasks.scrape_pending_urls[8e4aac77-faaa-45fb-9f60-49316e30c2b5] succeeded in 0.002743199933320284s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:00:47,610: INFO/MainProcess] Task tasks.scrape_pending_urls[f52fee42-80f7-42c3-aa67-8b717a07fe37] received
[2026-03-30 03:00:47,614: INFO/MainProcess] Task tasks.scrape_pending_urls[f52fee42-80f7-42c3-aa67-8b717a07fe37] succeeded in 0.0029693000251427293s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:01:17,610: INFO/MainProcess] Task tasks.scrape_pending_urls[4c3f6b23-1c2a-47c1-ae3c-8c9aef4999a3] received
[2026-03-30 03:01:17,613: INFO/MainProcess] Task tasks.scrape_pending_urls[4c3f6b23-1c2a-47c1-ae3c-8c9aef4999a3] succeeded in 0.00257210002746433s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:01:47,610: INFO/MainProcess] Task tasks.scrape_pending_urls[11ea8270-836b-443f-a15f-06f9e8c7a5f7] received
[2026-03-30 03:01:47,614: INFO/MainProcess] Task tasks.scrape_pending_urls[11ea8270-836b-443f-a15f-06f9e8c7a5f7] succeeded in 0.00279150006826967s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:02:17,611: INFO/MainProcess] Task tasks.scrape_pending_urls[487da3c4-809a-4097-8270-035c47e9f2fb] received
[2026-03-30 03:02:17,614: INFO/MainProcess] Task tasks.scrape_pending_urls[487da3c4-809a-4097-8270-035c47e9f2fb] succeeded in 0.0028415999840945005s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:02:47,611: INFO/MainProcess] Task tasks.scrape_pending_urls[13f654ad-ec9f-4be7-9866-e2693037eadb] received
[2026-03-30 03:02:47,614: INFO/MainProcess] Task tasks.scrape_pending_urls[13f654ad-ec9f-4be7-9866-e2693037eadb] succeeded in 0.0028201999375596642s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:03:17,610: INFO/MainProcess] Task tasks.scrape_pending_urls[8aef0bde-e902-4dd0-ae98-e16c2ddc54fb] received
[2026-03-30 03:03:17,614: INFO/MainProcess] Task tasks.scrape_pending_urls[8aef0bde-e902-4dd0-ae98-e16c2ddc54fb] succeeded in 0.0028016000287607312s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:03:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[eab2edcc-e764-44bc-abb7-9b0858bf5707] received
[2026-03-30 03:03:48,012: INFO/MainProcess] Task tasks.collect_system_metrics[eab2edcc-e764-44bc-abb7-9b0858bf5707] succeeded in 0.5160841000033543s: {'cpu': 10.8, 'memory': 45.7}
[2026-03-30 03:03:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[f0f08288-7521-46b1-aad8-364ee2152845] received
[2026-03-30 03:03:48,018: INFO/MainProcess] Task tasks.scrape_pending_urls[f0f08288-7521-46b1-aad8-364ee2152845] succeeded in 0.003351000021211803s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:04:17,611: INFO/MainProcess] Task tasks.scrape_pending_urls[1614c008-bdeb-4ee4-8289-c0d1b13cd767] received
[2026-03-30 03:04:17,614: INFO/MainProcess] Task tasks.scrape_pending_urls[1614c008-bdeb-4ee4-8289-c0d1b13cd767] succeeded in 0.0027879999252036214s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:04:47,611: INFO/MainProcess] Task tasks.scrape_pending_urls[10400d47-4c00-4aa1-8c25-2fc4fd7827e9] received
[2026-03-30 03:04:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[10400d47-4c00-4aa1-8c25-2fc4fd7827e9] succeeded in 0.003287100000306964s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:05:17,611: INFO/MainProcess] Task tasks.scrape_pending_urls[1e00b2be-c415-402f-9b7b-26bceb3cefd4] received
[2026-03-30 03:05:17,614: INFO/MainProcess] Task tasks.scrape_pending_urls[1e00b2be-c415-402f-9b7b-26bceb3cefd4] succeeded in 0.0027652999851852655s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:05:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[1db72383-a8c7-4f38-b33e-b4254bf72b90] received
[2026-03-30 03:05:47,618: INFO/MainProcess] Task tasks.scrape_pending_urls[1db72383-a8c7-4f38-b33e-b4254bf72b90] succeeded in 0.002764000091701746s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:06:17,615: INFO/MainProcess] Task tasks.scrape_pending_urls[9e4b1e19-41d3-414f-a47f-98b386a9bbc6] received
[2026-03-30 03:06:17,618: INFO/MainProcess] Task tasks.scrape_pending_urls[9e4b1e19-41d3-414f-a47f-98b386a9bbc6] succeeded in 0.0028609000146389008s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:06:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[15f804fd-86f4-4f7f-9634-74b0d6a755cb] received
[2026-03-30 03:06:47,618: INFO/MainProcess] Task tasks.scrape_pending_urls[15f804fd-86f4-4f7f-9634-74b0d6a755cb] succeeded in 0.00292749993968755s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:07:17,615: INFO/MainProcess] Task tasks.scrape_pending_urls[299bf601-f561-4be3-a10a-1a4e4abad58f] received
[2026-03-30 03:07:17,618: INFO/MainProcess] Task tasks.scrape_pending_urls[299bf601-f561-4be3-a10a-1a4e4abad58f] succeeded in 0.003268200089223683s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:07:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[cb224d2c-e9c8-4d0f-bc52-4860980aea07] received
[2026-03-30 03:07:47,618: INFO/MainProcess] Task tasks.scrape_pending_urls[cb224d2c-e9c8-4d0f-bc52-4860980aea07] succeeded in 0.0027692000148817897s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:08:17,615: INFO/MainProcess] Task tasks.scrape_pending_urls[dfcd9f30-3d84-46ac-a28e-c1f899950dbc] received
[2026-03-30 03:08:17,618: INFO/MainProcess] Task tasks.scrape_pending_urls[dfcd9f30-3d84-46ac-a28e-c1f899950dbc] succeeded in 0.0026708999648690224s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:08:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[d11b7d3d-f69c-4264-ae76-4f8a3ad0026a] received
[2026-03-30 03:08:48,013: INFO/MainProcess] Task tasks.collect_system_metrics[d11b7d3d-f69c-4264-ae76-4f8a3ad0026a] succeeded in 0.516437100013718s: {'cpu': 11.7, 'memory': 45.9}
[2026-03-30 03:08:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[aa900ef0-bbad-4cb6-9819-76c73e80e1e3] received
[2026-03-30 03:08:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[aa900ef0-bbad-4cb6-9819-76c73e80e1e3] succeeded in 0.0038799999747425318s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:09:17,615: INFO/MainProcess] Task tasks.scrape_pending_urls[81dda894-8e45-490a-9a35-f1ed78d91755] received
[2026-03-30 03:09:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[81dda894-8e45-490a-9a35-f1ed78d91755] succeeded in 0.002748900093138218s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:09:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[7879a178-c8aa-4eb1-ae72-ae6557fb9151] received
[2026-03-30 03:09:47,618: INFO/MainProcess] Task tasks.scrape_pending_urls[7879a178-c8aa-4eb1-ae72-ae6557fb9151] succeeded in 0.00267730001360178s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:10:17,615: INFO/MainProcess] Task tasks.scrape_pending_urls[509dbe2c-78c6-4aba-b9dc-ee83187b563b] received
[2026-03-30 03:10:17,618: INFO/MainProcess] Task tasks.scrape_pending_urls[509dbe2c-78c6-4aba-b9dc-ee83187b563b] succeeded in 0.0030576999997720122s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:10:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[cdc1bc5e-e7a5-4995-add1-bdd86df7c12c] received
[2026-03-30 03:10:47,618: INFO/MainProcess] Task tasks.scrape_pending_urls[cdc1bc5e-e7a5-4995-add1-bdd86df7c12c] succeeded in 0.0027402000268921256s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:11:17,615: INFO/MainProcess] Task tasks.scrape_pending_urls[b74cd773-4e59-43cf-8726-ba775bff4a61] received
[2026-03-30 03:11:17,618: INFO/MainProcess] Task tasks.scrape_pending_urls[b74cd773-4e59-43cf-8726-ba775bff4a61] succeeded in 0.0025858000153675675s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:11:47,615: INFO/MainProcess] Task tasks.scrape_pending_urls[6ab88a69-39c5-42d8-b72d-d042e1e39677] received
[2026-03-30 03:11:47,618: INFO/MainProcess] Task tasks.scrape_pending_urls[6ab88a69-39c5-42d8-b72d-d042e1e39677] succeeded in 0.0028174000326544046s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:12:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[fb95f38e-81a5-4c29-9483-93421612eb9f] received
[2026-03-30 03:12:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[fb95f38e-81a5-4c29-9483-93421612eb9f] succeeded in 0.002806499949656427s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:12:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[d62827df-6d61-4eaa-8f79-483e57c8ab43] received
[2026-03-30 03:12:47,623: INFO/MainProcess] Task tasks.scrape_pending_urls[d62827df-6d61-4eaa-8f79-483e57c8ab43] succeeded in 0.003033899934962392s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:13:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[9d5c27cf-cd2a-4466-861b-5b3c48de25da] received
[2026-03-30 03:13:17,622: INFO/MainProcess] Task tasks.scrape_pending_urls[9d5c27cf-cd2a-4466-861b-5b3c48de25da] succeeded in 0.002585300011560321s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:13:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[c97ebecf-5941-45e6-be43-019c2317c0f6] received
[2026-03-30 03:13:48,012: INFO/MainProcess] Task tasks.collect_system_metrics[c97ebecf-5941-45e6-be43-019c2317c0f6] succeeded in 0.5160303000593558s: {'cpu': 12.9, 'memory': 45.8}
[2026-03-30 03:13:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[58ca0ed6-0155-4e39-a946-289d75ea2913] received
[2026-03-30 03:13:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[58ca0ed6-0155-4e39-a946-289d75ea2913] succeeded in 0.007554899901151657s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:14:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[3d3efdb5-db31-4a30-a4c8-2d833971b5f6] received
[2026-03-30 03:14:17,622: INFO/MainProcess] Task tasks.scrape_pending_urls[3d3efdb5-db31-4a30-a4c8-2d833971b5f6] succeeded in 0.0027185999788343906s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:14:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[39e75576-d466-44cb-bc57-c52212873c29] received
[2026-03-30 03:14:47,622: INFO/MainProcess] Task tasks.scrape_pending_urls[39e75576-d466-44cb-bc57-c52212873c29] succeeded in 0.002620800049044192s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:15:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[b7cc0fb7-c105-4a5d-95f1-ded77f4f8cb6] received
[2026-03-30 03:15:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[b7cc0fb7-c105-4a5d-95f1-ded77f4f8cb6] succeeded in 0.0032027000561356544s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:15:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[93e9d37c-7746-4586-84e2-e20c604d0487] received
[2026-03-30 03:15:47,622: INFO/MainProcess] Task tasks.scrape_pending_urls[93e9d37c-7746-4586-84e2-e20c604d0487] succeeded in 0.00258239998947829s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:16:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[56e60ba4-1c12-47de-a03a-aa295b2f5a34] received
[2026-03-30 03:16:17,622: INFO/MainProcess] Task tasks.scrape_pending_urls[56e60ba4-1c12-47de-a03a-aa295b2f5a34] succeeded in 0.0026996000669896603s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:16:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[b95a96f5-6279-4637-83cb-118f4a7fb802] received
[2026-03-30 03:16:47,622: INFO/MainProcess] Task tasks.scrape_pending_urls[b95a96f5-6279-4637-83cb-118f4a7fb802] succeeded in 0.0027673000004142523s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:17:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[1f22a568-a2ef-44ca-91ec-72215bf9d3e0] received
[2026-03-30 03:17:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[1f22a568-a2ef-44ca-91ec-72215bf9d3e0] succeeded in 0.003277599927969277s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:17:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[33bfcb30-277e-48c5-b027-2f205f6e51af] received
[2026-03-30 03:17:47,622: INFO/MainProcess] Task tasks.scrape_pending_urls[33bfcb30-277e-48c5-b027-2f205f6e51af] succeeded in 0.0026307000080123544s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:18:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[4556b54f-00bb-4e8f-9481-9a06a2060267] received
[2026-03-30 03:18:17,622: INFO/MainProcess] Task tasks.scrape_pending_urls[4556b54f-00bb-4e8f-9481-9a06a2060267] succeeded in 0.0027534000109881163s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:18:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[c67cf5c4-8e0d-426c-9872-b40bb4c19f50] received
[2026-03-30 03:18:47,489: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 03:18:47,490: INFO/MainProcess] Task tasks.reset_stale_processing_urls[c67cf5c4-8e0d-426c-9872-b40bb4c19f50] succeeded in 0.003179199993610382s: {'reset': 0}
[2026-03-30 03:18:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[146ba501-d436-46b2-88ef-c4c54b9e29e4] received
[2026-03-30 03:18:48,013: INFO/MainProcess] Task tasks.collect_system_metrics[146ba501-d436-46b2-88ef-c4c54b9e29e4] succeeded in 0.5161602000007406s: {'cpu': 15.6, 'memory': 45.9}
[2026-03-30 03:18:48,015: INFO/MainProcess] Task tasks.scrape_pending_urls[04b4688e-d7be-439f-9c4d-90f2bae26346] received
[2026-03-30 03:18:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[04b4688e-d7be-439f-9c4d-90f2bae26346] succeeded in 0.002215099986642599s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:19:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[928ab7d6-4690-4b98-b75a-fb2cbb432abd] received
[2026-03-30 03:19:17,622: INFO/MainProcess] Task tasks.scrape_pending_urls[928ab7d6-4690-4b98-b75a-fb2cbb432abd] succeeded in 0.0026289999950677156s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:19:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[487504d6-d98d-4ee1-8c8e-09aa68b0be5c] received
[2026-03-30 03:19:47,622: INFO/MainProcess] Task tasks.scrape_pending_urls[487504d6-d98d-4ee1-8c8e-09aa68b0be5c] succeeded in 0.0026929000159725547s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:20:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[a52232b0-9bd7-40e9-ba4d-f9728c3009b2] received
[2026-03-30 03:20:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[a52232b0-9bd7-40e9-ba4d-f9728c3009b2] succeeded in 0.003201400046236813s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:20:47,619: INFO/MainProcess] Task tasks.scrape_pending_urls[a969f4de-99c0-462f-ad9f-5509db31e84b] received
[2026-03-30 03:20:47,622: INFO/MainProcess] Task tasks.scrape_pending_urls[a969f4de-99c0-462f-ad9f-5509db31e84b] succeeded in 0.00286979996599257s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:21:17,619: INFO/MainProcess] Task tasks.scrape_pending_urls[254feab8-aaf0-4b4a-95c5-9704d4e0399a] received
[2026-03-30 03:21:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[254feab8-aaf0-4b4a-95c5-9704d4e0399a] succeeded in 0.003040499985218048s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:21:47,624: INFO/MainProcess] Task tasks.scrape_pending_urls[7c5d15c3-8177-4aeb-b92e-acf8cd80710c] received
[2026-03-30 03:21:47,627: INFO/MainProcess] Task tasks.scrape_pending_urls[7c5d15c3-8177-4aeb-b92e-acf8cd80710c] succeeded in 0.0026893001049757004s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:22:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[0ff3b9bf-d068-4d2b-8bc6-ea3b380ba4be] received
[2026-03-30 03:22:17,626: INFO/MainProcess] Task tasks.scrape_pending_urls[0ff3b9bf-d068-4d2b-8bc6-ea3b380ba4be] succeeded in 0.002598599996417761s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:22:47,623: INFO/MainProcess] Task tasks.scrape_pending_urls[45ad2cd5-57b3-41e5-90a4-47bb5d030fb5] received
[2026-03-30 03:22:47,627: INFO/MainProcess] Task tasks.scrape_pending_urls[45ad2cd5-57b3-41e5-90a4-47bb5d030fb5] succeeded in 0.002868699957616627s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:23:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[411805e2-20f4-480a-9757-926c48774375] received
[2026-03-30 03:23:17,627: INFO/MainProcess] Task tasks.scrape_pending_urls[411805e2-20f4-480a-9757-926c48774375] succeeded in 0.0027730000438168645s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:23:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[b76a504a-889b-4fd6-b207-4aa1d3f09214] received
[2026-03-30 03:23:48,014: INFO/MainProcess] Task tasks.collect_system_metrics[b76a504a-889b-4fd6-b207-4aa1d3f09214] succeeded in 0.5180785999400541s: {'cpu': 9.8, 'memory': 45.9}
[2026-03-30 03:23:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[28daf0f5-e8f7-441c-8d58-28b2a8b7b728] received
[2026-03-30 03:23:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[28daf0f5-e8f7-441c-8d58-28b2a8b7b728] succeeded in 0.0026093999622389674s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:24:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[4dc116c3-caba-4b78-8021-4bd1066c90a8] received
[2026-03-30 03:24:17,626: INFO/MainProcess] Task tasks.scrape_pending_urls[4dc116c3-caba-4b78-8021-4bd1066c90a8] succeeded in 0.00258239998947829s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:24:47,624: INFO/MainProcess] Task tasks.scrape_pending_urls[fa3994a6-f97d-4c20-af9f-88d5c2231d56] received
[2026-03-30 03:24:47,627: INFO/MainProcess] Task tasks.scrape_pending_urls[fa3994a6-f97d-4c20-af9f-88d5c2231d56] succeeded in 0.002831100020557642s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:25:17,623: INFO/MainProcess] Task tasks.scrape_pending_urls[e2b4ffcb-d196-49de-8f2d-89399780d313] received
[2026-03-30 03:25:17,626: INFO/MainProcess] Task tasks.scrape_pending_urls[e2b4ffcb-d196-49de-8f2d-89399780d313] succeeded in 0.002521399990655482s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:25:47,624: INFO/MainProcess] Task tasks.scrape_pending_urls[cf7d3003-147b-404b-b044-059229d5030e] received
[2026-03-30 03:25:47,627: INFO/MainProcess] Task tasks.scrape_pending_urls[cf7d3003-147b-404b-b044-059229d5030e] succeeded in 0.003062700037844479s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:26:17,624: INFO/MainProcess] Task tasks.scrape_pending_urls[a84127af-c646-439f-bb9f-735c902dbf44] received
[2026-03-30 03:26:17,627: INFO/MainProcess] Task tasks.scrape_pending_urls[a84127af-c646-439f-bb9f-735c902dbf44] succeeded in 0.002707200008444488s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:26:47,624: INFO/MainProcess] Task tasks.scrape_pending_urls[b7a916a2-cc54-47ad-afef-1998e3afa8ca] received
[2026-03-30 03:26:47,627: INFO/MainProcess] Task tasks.scrape_pending_urls[b7a916a2-cc54-47ad-afef-1998e3afa8ca] succeeded in 0.0026767998933792114s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:27:17,624: INFO/MainProcess] Task tasks.scrape_pending_urls[8a4a263a-87c8-4f6d-a9fb-585c8d495929] received
[2026-03-30 03:27:17,692: INFO/MainProcess] Task tasks.scrape_pending_urls[8a4a263a-87c8-4f6d-a9fb-585c8d495929] succeeded in 0.06740749999880791s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:27:47,624: INFO/MainProcess] Task tasks.scrape_pending_urls[65a9a122-8ca1-4c7d-a569-31ba520d9d32] received
[2026-03-30 03:27:47,627: INFO/MainProcess] Task tasks.scrape_pending_urls[65a9a122-8ca1-4c7d-a569-31ba520d9d32] succeeded in 0.0028612000169232488s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:28:17,629: INFO/MainProcess] Task tasks.scrape_pending_urls[7277dffe-d942-4d68-836c-73a675db91db] received
[2026-03-30 03:28:17,632: INFO/MainProcess] Task tasks.scrape_pending_urls[7277dffe-d942-4d68-836c-73a675db91db] succeeded in 0.0027118000434711576s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:28:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[3bc3d568-6f7c-4712-98d4-c15237e29782] received
[2026-03-30 03:28:48,015: INFO/MainProcess] Task tasks.collect_system_metrics[3bc3d568-6f7c-4712-98d4-c15237e29782] succeeded in 0.5182014999445528s: {'cpu': 10.5, 'memory': 45.9}
[2026-03-30 03:28:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[a3728f8e-12e5-4ed0-a568-229572e5314d] received
[2026-03-30 03:28:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[a3728f8e-12e5-4ed0-a568-229572e5314d] succeeded in 0.0026711999671533704s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:29:17,628: INFO/MainProcess] Task tasks.scrape_pending_urls[add7db43-e12a-493b-9716-615f800f8a3f] received
[2026-03-30 03:29:17,631: INFO/MainProcess] Task tasks.scrape_pending_urls[add7db43-e12a-493b-9716-615f800f8a3f] succeeded in 0.0024879000848159194s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:29:47,629: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d7b0a1-185d-453a-abbf-0b7ae7ac4770] received
[2026-03-30 03:29:47,632: INFO/MainProcess] Task tasks.scrape_pending_urls[f9d7b0a1-185d-453a-abbf-0b7ae7ac4770] succeeded in 0.002795899985358119s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[889a569e-23da-4948-9efa-13bf8ed4f2a5] received
[2026-03-30 03:30:00,005: INFO/MainProcess] Task tasks.purge_old_debug_html[889a569e-23da-4948-9efa-13bf8ed4f2a5] succeeded in 0.00244309997651726s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 03:30:17,629: INFO/MainProcess] Task tasks.scrape_pending_urls[e4c63e0d-e6ed-406a-acaa-792bc2fca6df] received
[2026-03-30 03:30:17,632: INFO/MainProcess] Task tasks.scrape_pending_urls[e4c63e0d-e6ed-406a-acaa-792bc2fca6df] succeeded in 0.002790900063700974s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:30:47,629: INFO/MainProcess] Task tasks.scrape_pending_urls[f17fc20f-058d-425c-8310-eaad896fe808] received
[2026-03-30 03:30:47,632: INFO/MainProcess] Task tasks.scrape_pending_urls[f17fc20f-058d-425c-8310-eaad896fe808] succeeded in 0.002839399967342615s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:31:17,628: INFO/MainProcess] Task tasks.scrape_pending_urls[acdb9e5b-e0d6-4909-b2f2-699a9b90d8fa] received
[2026-03-30 03:31:17,632: INFO/MainProcess] Task tasks.scrape_pending_urls[acdb9e5b-e0d6-4909-b2f2-699a9b90d8fa] succeeded in 0.0029554999200627208s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:31:47,629: INFO/MainProcess] Task tasks.scrape_pending_urls[85c2903d-5f31-4952-ac45-a75fd15e508e] received
[2026-03-30 03:31:47,632: INFO/MainProcess] Task tasks.scrape_pending_urls[85c2903d-5f31-4952-ac45-a75fd15e508e] succeeded in 0.0027046999894082546s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:32:17,629: INFO/MainProcess] Task tasks.scrape_pending_urls[4fddf4d4-f392-4a0d-8857-ffc5f95c2d8e] received
[2026-03-30 03:32:17,699: INFO/MainProcess] Task tasks.scrape_pending_urls[4fddf4d4-f392-4a0d-8857-ffc5f95c2d8e] succeeded in 0.06954619998577982s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:32:47,629: INFO/MainProcess] Task tasks.scrape_pending_urls[1e5274e0-bf1d-4268-b489-3354e070a45e] received
[2026-03-30 03:32:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[1e5274e0-bf1d-4268-b489-3354e070a45e] succeeded in 0.003698799991980195s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:33:17,629: INFO/MainProcess] Task tasks.scrape_pending_urls[94a67a87-5e47-46b1-977d-b261bba10515] received
[2026-03-30 03:33:17,632: INFO/MainProcess] Task tasks.scrape_pending_urls[94a67a87-5e47-46b1-977d-b261bba10515] succeeded in 0.0029192999936640263s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:33:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[0080b211-cbc9-44d1-aad6-96ab91341420] received
[2026-03-30 03:33:48,015: INFO/MainProcess] Task tasks.collect_system_metrics[0080b211-cbc9-44d1-aad6-96ab91341420] succeeded in 0.5182562000118196s: {'cpu': 16.9, 'memory': 46.0}
[2026-03-30 03:33:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[ecf86b64-a15c-43d6-958b-e720e6b22712] received
[2026-03-30 03:33:48,020: INFO/MainProcess] Task tasks.scrape_pending_urls[ecf86b64-a15c-43d6-958b-e720e6b22712] succeeded in 0.0027442999416962266s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:34:17,629: INFO/MainProcess] Task tasks.scrape_pending_urls[f63e0be4-664f-44c8-ae58-762df006018c] received
[2026-03-30 03:34:17,633: INFO/MainProcess] Task tasks.scrape_pending_urls[f63e0be4-664f-44c8-ae58-762df006018c] succeeded in 0.0035375000443309546s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:34:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[942ae94e-04ff-4f52-b9ff-014b24ad00d0] received
[2026-03-30 03:34:47,637: INFO/MainProcess] Task tasks.scrape_pending_urls[942ae94e-04ff-4f52-b9ff-014b24ad00d0] succeeded in 0.0030091999797150493s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:35:17,633: INFO/MainProcess] Task tasks.scrape_pending_urls[41c3520b-8e57-46cd-883a-f9d719931381] received
[2026-03-30 03:35:17,636: INFO/MainProcess] Task tasks.scrape_pending_urls[41c3520b-8e57-46cd-883a-f9d719931381] succeeded in 0.0029989000177010894s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:35:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[93e4b060-42ec-4e88-9ea6-1f02d1ba5937] received
[2026-03-30 03:35:47,636: INFO/MainProcess] Task tasks.scrape_pending_urls[93e4b060-42ec-4e88-9ea6-1f02d1ba5937] succeeded in 0.0028593000024557114s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:36:17,633: INFO/MainProcess] Task tasks.scrape_pending_urls[d9d09908-c1a5-4af2-817f-5ea46c261f29] received
[2026-03-30 03:36:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[d9d09908-c1a5-4af2-817f-5ea46c261f29] succeeded in 0.0028253999771550298s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:36:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[d0586c99-f23f-4046-ab71-38b2e3676e70] received
[2026-03-30 03:36:47,636: INFO/MainProcess] Task tasks.scrape_pending_urls[d0586c99-f23f-4046-ab71-38b2e3676e70] succeeded in 0.002823700080625713s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:37:17,633: INFO/MainProcess] Task tasks.scrape_pending_urls[1d9c62ea-d056-4606-9448-474962f06b83] received
[2026-03-30 03:37:17,636: INFO/MainProcess] Task tasks.scrape_pending_urls[1d9c62ea-d056-4606-9448-474962f06b83] succeeded in 0.0027350999880582094s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:37:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[978cd5a9-c911-4639-a2ee-39b76c8163ea] received
[2026-03-30 03:37:47,636: INFO/MainProcess] Task tasks.scrape_pending_urls[978cd5a9-c911-4639-a2ee-39b76c8163ea] succeeded in 0.0028888999950140715s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:38:17,634: INFO/MainProcess] Task tasks.scrape_pending_urls[4e564e5f-b5bc-47d9-98c1-99671b09eb66] received
[2026-03-30 03:38:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[4e564e5f-b5bc-47d9-98c1-99671b09eb66] succeeded in 0.0029055000049993396s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:38:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[d2e7e8e7-b482-41aa-b9fb-c124cbdd3556] received
[2026-03-30 03:38:48,071: INFO/MainProcess] Task tasks.collect_system_metrics[d2e7e8e7-b482-41aa-b9fb-c124cbdd3556] succeeded in 0.5746330000692979s: {'cpu': 10.6, 'memory': 46.1}
[2026-03-30 03:38:48,073: INFO/MainProcess] Task tasks.scrape_pending_urls[02a5d8ad-04c6-4783-926d-0b523bb5b49c] received
[2026-03-30 03:38:48,076: INFO/MainProcess] Task tasks.scrape_pending_urls[02a5d8ad-04c6-4783-926d-0b523bb5b49c] succeeded in 0.002342000021599233s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:39:17,633: INFO/MainProcess] Task tasks.scrape_pending_urls[31fd366c-4044-4e34-a7f2-62335a97b98d] received
[2026-03-30 03:39:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[31fd366c-4044-4e34-a7f2-62335a97b98d] succeeded in 0.00349980010651052s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:39:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[8ce95e8e-25ae-4424-a73e-f63dceb3c761] received
[2026-03-30 03:39:47,636: INFO/MainProcess] Task tasks.scrape_pending_urls[8ce95e8e-25ae-4424-a73e-f63dceb3c761] succeeded in 0.002684500068426132s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:40:17,633: INFO/MainProcess] Task tasks.scrape_pending_urls[b2c3987e-cec0-4d4f-a1ba-a394918dec9d] received
[2026-03-30 03:40:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[b2c3987e-cec0-4d4f-a1ba-a394918dec9d] succeeded in 0.0029008000856265426s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:40:47,633: INFO/MainProcess] Task tasks.scrape_pending_urls[8dbe470a-f5f6-41f0-90fa-5e491330576a] received
[2026-03-30 03:40:47,636: INFO/MainProcess] Task tasks.scrape_pending_urls[8dbe470a-f5f6-41f0-90fa-5e491330576a] succeeded in 0.002563699963502586s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:41:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[c5802572-2a61-48b5-94fd-d59a503f5ca9] received
[2026-03-30 03:41:17,640: INFO/MainProcess] Task tasks.scrape_pending_urls[c5802572-2a61-48b5-94fd-d59a503f5ca9] succeeded in 0.0029308000812307s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:41:47,637: INFO/MainProcess] Task tasks.scrape_pending_urls[dde2a12d-b583-4782-bdd0-0e5f664d5f44] received
[2026-03-30 03:41:47,640: INFO/MainProcess] Task tasks.scrape_pending_urls[dde2a12d-b583-4782-bdd0-0e5f664d5f44] succeeded in 0.002796499989926815s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:42:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[b405e01a-a880-4fed-8652-4eb74b6c4dd9] received
[2026-03-30 03:42:17,640: INFO/MainProcess] Task tasks.scrape_pending_urls[b405e01a-a880-4fed-8652-4eb74b6c4dd9] succeeded in 0.003154100035317242s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:42:47,636: INFO/MainProcess] Task tasks.scrape_pending_urls[84dbd8f6-c181-487c-a3bc-0fd8fd2dd8a1] received
[2026-03-30 03:42:47,640: INFO/MainProcess] Task tasks.scrape_pending_urls[84dbd8f6-c181-487c-a3bc-0fd8fd2dd8a1] succeeded in 0.002962999977171421s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:43:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[d5c3f394-dcac-4c21-96b3-a0e0021f6452] received
[2026-03-30 03:43:17,640: INFO/MainProcess] Task tasks.scrape_pending_urls[d5c3f394-dcac-4c21-96b3-a0e0021f6452] succeeded in 0.002843499998562038s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:43:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[54b9008a-373d-4ad3-8faa-3aa80c6b5e58] received
[2026-03-30 03:43:48,014: INFO/MainProcess] Task tasks.collect_system_metrics[54b9008a-373d-4ad3-8faa-3aa80c6b5e58] succeeded in 0.5173863999079913s: {'cpu': 11.1, 'memory': 45.9}
[2026-03-30 03:43:48,015: INFO/MainProcess] Task tasks.scrape_pending_urls[55588553-9160-43b9-90f2-16af8aa86625] received
[2026-03-30 03:43:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[55588553-9160-43b9-90f2-16af8aa86625] succeeded in 0.0034344999585300684s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:44:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[f53f0428-22eb-4b2e-a3a0-39ff3543ff3d] received
[2026-03-30 03:44:17,641: INFO/MainProcess] Task tasks.scrape_pending_urls[f53f0428-22eb-4b2e-a3a0-39ff3543ff3d] succeeded in 0.002951700007542968s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:44:47,637: INFO/MainProcess] Task tasks.scrape_pending_urls[c60cd897-76bc-470a-9e9f-8892ecd65ffa] received
[2026-03-30 03:44:47,640: INFO/MainProcess] Task tasks.scrape_pending_urls[c60cd897-76bc-470a-9e9f-8892ecd65ffa] succeeded in 0.002590899937786162s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:45:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[a32131b1-8dfd-4baf-8a15-69116a3b45c3] received
[2026-03-30 03:45:17,640: INFO/MainProcess] Task tasks.scrape_pending_urls[a32131b1-8dfd-4baf-8a15-69116a3b45c3] succeeded in 0.00327590003143996s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:45:47,637: INFO/MainProcess] Task tasks.scrape_pending_urls[783b21bb-9b82-41e2-b253-beb1cd7dbc96] received
[2026-03-30 03:45:47,640: INFO/MainProcess] Task tasks.scrape_pending_urls[783b21bb-9b82-41e2-b253-beb1cd7dbc96] succeeded in 0.0030592000111937523s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:46:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[a3f369e4-72d9-4e6e-9d86-a994627ac4fc] received
[2026-03-30 03:46:17,640: INFO/MainProcess] Task tasks.scrape_pending_urls[a3f369e4-72d9-4e6e-9d86-a994627ac4fc] succeeded in 0.002948499983176589s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:46:47,638: INFO/MainProcess] Task tasks.scrape_pending_urls[6c3ad0d0-f79a-454a-bcbe-884dbbc05083] received
[2026-03-30 03:46:47,642: INFO/MainProcess] Task tasks.scrape_pending_urls[6c3ad0d0-f79a-454a-bcbe-884dbbc05083] succeeded in 0.003475499921478331s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:47:17,637: INFO/MainProcess] Task tasks.scrape_pending_urls[8bde4eeb-0596-444e-8546-0d2e64705785] received
[2026-03-30 03:47:17,640: INFO/MainProcess] Task tasks.scrape_pending_urls[8bde4eeb-0596-444e-8546-0d2e64705785] succeeded in 0.0027262000367045403s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:47:47,641: INFO/MainProcess] Task tasks.scrape_pending_urls[086037f4-ebbe-4ee5-8182-a240898f4a1f] received
[2026-03-30 03:47:47,645: INFO/MainProcess] Task tasks.scrape_pending_urls[086037f4-ebbe-4ee5-8182-a240898f4a1f] succeeded in 0.002778499969281256s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:48:17,641: INFO/MainProcess] Task tasks.scrape_pending_urls[7b4d2dc9-4017-4a06-8910-7568ae7ad727] received
[2026-03-30 03:48:17,644: INFO/MainProcess] Task tasks.scrape_pending_urls[7b4d2dc9-4017-4a06-8910-7568ae7ad727] succeeded in 0.002676400006748736s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:48:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[17363098-7c13-4220-9b17-3491aa869f7f] received
[2026-03-30 03:48:47,490: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 03:48:47,491: INFO/MainProcess] Task tasks.reset_stale_processing_urls[17363098-7c13-4220-9b17-3491aa869f7f] succeeded in 0.004054800025187433s: {'reset': 0}
[2026-03-30 03:48:47,495: INFO/MainProcess] Task tasks.collect_system_metrics[35734dc6-ca46-4445-b294-dedad1a46002] received
[2026-03-30 03:48:48,011: INFO/MainProcess] Task tasks.collect_system_metrics[35734dc6-ca46-4445-b294-dedad1a46002] succeeded in 0.5159447999903932s: {'cpu': 10.0, 'memory': 45.7}
[2026-03-30 03:48:48,013: INFO/MainProcess] Task tasks.scrape_pending_urls[0cfdfc25-a60e-4b12-9392-d02066cbf68e] received
[2026-03-30 03:48:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[0cfdfc25-a60e-4b12-9392-d02066cbf68e] succeeded in 0.002722600009292364s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:49:17,642: INFO/MainProcess] Task tasks.scrape_pending_urls[5ab45daf-6cf3-4abe-8068-016fc9505a6c] received
[2026-03-30 03:49:17,645: INFO/MainProcess] Task tasks.scrape_pending_urls[5ab45daf-6cf3-4abe-8068-016fc9505a6c] succeeded in 0.0027985000051558018s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:49:47,642: INFO/MainProcess] Task tasks.scrape_pending_urls[02a9f015-9ec0-447a-83a4-57e688f5578e] received
[2026-03-30 03:49:47,645: INFO/MainProcess] Task tasks.scrape_pending_urls[02a9f015-9ec0-447a-83a4-57e688f5578e] succeeded in 0.002728200051933527s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:50:17,641: INFO/MainProcess] Task tasks.scrape_pending_urls[bddbc8ab-ba3c-4770-9009-28f0696f649b] received
[2026-03-30 03:50:17,644: INFO/MainProcess] Task tasks.scrape_pending_urls[bddbc8ab-ba3c-4770-9009-28f0696f649b] succeeded in 0.0027205999940633774s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:50:47,641: INFO/MainProcess] Task tasks.scrape_pending_urls[f23e8e69-8fe4-467f-9601-4810cc154e70] received
[2026-03-30 03:50:47,645: INFO/MainProcess] Task tasks.scrape_pending_urls[f23e8e69-8fe4-467f-9601-4810cc154e70] succeeded in 0.0028539999620988965s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:51:17,642: INFO/MainProcess] Task tasks.scrape_pending_urls[f8a7633b-ebd5-4da1-b10d-afd3672e47ed] received
[2026-03-30 03:51:17,645: INFO/MainProcess] Task tasks.scrape_pending_urls[f8a7633b-ebd5-4da1-b10d-afd3672e47ed] succeeded in 0.0027380998944863677s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:51:47,641: INFO/MainProcess] Task tasks.scrape_pending_urls[e542a8f7-c0d2-4836-908d-b785b9efa7da] received
[2026-03-30 03:51:47,644: INFO/MainProcess] Task tasks.scrape_pending_urls[e542a8f7-c0d2-4836-908d-b785b9efa7da] succeeded in 0.0027171999681741s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:52:17,641: INFO/MainProcess] Task tasks.scrape_pending_urls[40653a64-bd53-41ae-966c-e042511acb28] received
[2026-03-30 03:52:17,644: INFO/MainProcess] Task tasks.scrape_pending_urls[40653a64-bd53-41ae-966c-e042511acb28] succeeded in 0.0026322000194340944s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:52:47,641: INFO/MainProcess] Task tasks.scrape_pending_urls[28e7f331-aab7-4992-8f80-774368cba7f5] received
[2026-03-30 03:52:47,644: INFO/MainProcess] Task tasks.scrape_pending_urls[28e7f331-aab7-4992-8f80-774368cba7f5] succeeded in 0.002691500005312264s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:53:17,641: INFO/MainProcess] Task tasks.scrape_pending_urls[2367e5c4-70df-471c-9976-12abdf353a86] received
[2026-03-30 03:53:17,644: INFO/MainProcess] Task tasks.scrape_pending_urls[2367e5c4-70df-471c-9976-12abdf353a86] succeeded in 0.00266519992146641s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:53:47,497: INFO/MainProcess] Task tasks.collect_system_metrics[25668400-cc10-4261-aa41-b1014c57a1e8] received
[2026-03-30 03:53:48,014: INFO/MainProcess] Task tasks.collect_system_metrics[25668400-cc10-4261-aa41-b1014c57a1e8] succeeded in 0.517338200006634s: {'cpu': 15.2, 'memory': 45.8}
[2026-03-30 03:53:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[13b2ab20-3511-4010-8ef3-393ca4116867] received
[2026-03-30 03:53:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[13b2ab20-3511-4010-8ef3-393ca4116867] succeeded in 0.0026363000506535172s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:54:17,646: INFO/MainProcess] Task tasks.scrape_pending_urls[16921425-5730-426a-a9be-4b08df06bcb0] received
[2026-03-30 03:54:17,649: INFO/MainProcess] Task tasks.scrape_pending_urls[16921425-5730-426a-a9be-4b08df06bcb0] succeeded in 0.0027094000251963735s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:54:47,645: INFO/MainProcess] Task tasks.scrape_pending_urls[847063a1-4d8f-4645-8cd1-598460cd1fe8] received
[2026-03-30 03:54:47,648: INFO/MainProcess] Task tasks.scrape_pending_urls[847063a1-4d8f-4645-8cd1-598460cd1fe8] succeeded in 0.0025954999728128314s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:55:17,645: INFO/MainProcess] Task tasks.scrape_pending_urls[c68a9bd7-401e-4a31-9465-20af48738b04] received
[2026-03-30 03:55:17,648: INFO/MainProcess] Task tasks.scrape_pending_urls[c68a9bd7-401e-4a31-9465-20af48738b04] succeeded in 0.0028102999785915017s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:55:47,646: INFO/MainProcess] Task tasks.scrape_pending_urls[707fcc51-9b77-4fb7-8e5c-00763aee2b16] received
[2026-03-30 03:55:47,649: INFO/MainProcess] Task tasks.scrape_pending_urls[707fcc51-9b77-4fb7-8e5c-00763aee2b16] succeeded in 0.002679100027307868s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:56:17,646: INFO/MainProcess] Task tasks.scrape_pending_urls[62a012e6-1544-495f-ae22-da241c378d77] received
[2026-03-30 03:56:17,649: INFO/MainProcess] Task tasks.scrape_pending_urls[62a012e6-1544-495f-ae22-da241c378d77] succeeded in 0.0027061000000685453s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:56:47,646: INFO/MainProcess] Task tasks.scrape_pending_urls[00537e07-07d3-483a-a5bd-96287a8db298] received
[2026-03-30 03:56:47,649: INFO/MainProcess] Task tasks.scrape_pending_urls[00537e07-07d3-483a-a5bd-96287a8db298] succeeded in 0.002623800071887672s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:57:17,646: INFO/MainProcess] Task tasks.scrape_pending_urls[25d77dfc-72e6-431b-b73f-0bec083bf6e1] received
[2026-03-30 03:57:17,649: INFO/MainProcess] Task tasks.scrape_pending_urls[25d77dfc-72e6-431b-b73f-0bec083bf6e1] succeeded in 0.002782299998216331s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:57:47,646: INFO/MainProcess] Task tasks.scrape_pending_urls[cfeaa11c-b35b-4461-888d-207ae5cb0ebf] received
[2026-03-30 03:57:47,649: INFO/MainProcess] Task tasks.scrape_pending_urls[cfeaa11c-b35b-4461-888d-207ae5cb0ebf] succeeded in 0.0026322000194340944s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:58:17,645: INFO/MainProcess] Task tasks.scrape_pending_urls[f00ef55e-b58e-4d21-b360-1706b992050a] received
[2026-03-30 03:58:17,648: INFO/MainProcess] Task tasks.scrape_pending_urls[f00ef55e-b58e-4d21-b360-1706b992050a] succeeded in 0.0025186999700963497s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:58:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[b4b92e69-3d61-4562-845c-43c7d047df4a] received
[2026-03-30 03:58:48,014: INFO/MainProcess] Task tasks.collect_system_metrics[b4b92e69-3d61-4562-845c-43c7d047df4a] succeeded in 0.5177587000653148s: {'cpu': 10.5, 'memory': 45.8}
[2026-03-30 03:58:48,016: INFO/MainProcess] Task tasks.scrape_pending_urls[ca474e8c-4117-4fc1-9531-2462a038ef98] received
[2026-03-30 03:58:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[ca474e8c-4117-4fc1-9531-2462a038ef98] succeeded in 0.002236700034700334s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:59:17,646: INFO/MainProcess] Task tasks.scrape_pending_urls[297a4590-255d-4372-8509-acbbd16fb88f] received
[2026-03-30 03:59:17,649: INFO/MainProcess] Task tasks.scrape_pending_urls[297a4590-255d-4372-8509-acbbd16fb88f] succeeded in 0.002714899950660765s: {'status': 'idle', 'pending': 0}
[2026-03-30 03:59:47,646: INFO/MainProcess] Task tasks.scrape_pending_urls[27e36595-2a8f-4782-8770-2b1945650677] received
[2026-03-30 03:59:47,649: INFO/MainProcess] Task tasks.scrape_pending_urls[27e36595-2a8f-4782-8770-2b1945650677] succeeded in 0.002795299980789423s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:00:17,646: INFO/MainProcess] Task tasks.scrape_pending_urls[4ee65096-0a6c-4a5c-8569-edd638294b25] received
[2026-03-30 04:00:17,649: INFO/MainProcess] Task tasks.scrape_pending_urls[4ee65096-0a6c-4a5c-8569-edd638294b25] succeeded in 0.003159399959258735s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:00:47,650: INFO/MainProcess] Task tasks.scrape_pending_urls[a9741a4d-e479-4ced-91e7-db9438f2e81b] received
[2026-03-30 04:00:47,653: INFO/MainProcess] Task tasks.scrape_pending_urls[a9741a4d-e479-4ced-91e7-db9438f2e81b] succeeded in 0.002521399990655482s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:01:17,650: INFO/MainProcess] Task tasks.scrape_pending_urls[3783a942-3035-4389-95d9-455aa8e581f6] received
[2026-03-30 04:01:17,653: INFO/MainProcess] Task tasks.scrape_pending_urls[3783a942-3035-4389-95d9-455aa8e581f6] succeeded in 0.0028370999498292804s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:01:47,650: INFO/MainProcess] Task tasks.scrape_pending_urls[a1d89d13-23ef-47d0-bbb1-92d5182027cc] received
[2026-03-30 04:01:47,653: INFO/MainProcess] Task tasks.scrape_pending_urls[a1d89d13-23ef-47d0-bbb1-92d5182027cc] succeeded in 0.0027092999080196023s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:02:17,650: INFO/MainProcess] Task tasks.scrape_pending_urls[dfe10293-1741-4a57-8138-4f40826a190b] received
[2026-03-30 04:02:17,653: INFO/MainProcess] Task tasks.scrape_pending_urls[dfe10293-1741-4a57-8138-4f40826a190b] succeeded in 0.002742700045928359s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:02:47,650: INFO/MainProcess] Task tasks.scrape_pending_urls[55ec4f34-fb58-42c2-9124-b8cc3b3a5ba8] received
[2026-03-30 04:02:47,653: INFO/MainProcess] Task tasks.scrape_pending_urls[55ec4f34-fb58-42c2-9124-b8cc3b3a5ba8] succeeded in 0.0031429000664502382s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:03:17,650: INFO/MainProcess] Task tasks.scrape_pending_urls[579ff7e2-ff5c-4674-82d5-9175edab95dc] received
[2026-03-30 04:03:17,653: INFO/MainProcess] Task tasks.scrape_pending_urls[579ff7e2-ff5c-4674-82d5-9175edab95dc] succeeded in 0.0027073000092059374s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:03:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[4dde65de-5bbd-410d-95df-84b23d48de27] received
[2026-03-30 04:03:48,013: INFO/MainProcess] Task tasks.collect_system_metrics[4dde65de-5bbd-410d-95df-84b23d48de27] succeeded in 0.5160901000490412s: {'cpu': 13.7, 'memory': 45.9}
[2026-03-30 04:03:48,014: INFO/MainProcess] Task tasks.scrape_pending_urls[6b323af1-2cd4-4acc-9315-2e18ac4bd080] received
[2026-03-30 04:03:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[6b323af1-2cd4-4acc-9315-2e18ac4bd080] succeeded in 0.002667300053872168s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:04:17,650: INFO/MainProcess] Task tasks.scrape_pending_urls[9db9a29d-d5a9-4a3b-8b32-b95f76a9fa3e] received
[2026-03-30 04:04:17,653: INFO/MainProcess] Task tasks.scrape_pending_urls[9db9a29d-d5a9-4a3b-8b32-b95f76a9fa3e] succeeded in 0.0025521001080051064s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:04:47,650: INFO/MainProcess] Task tasks.scrape_pending_urls[99c9b49c-38d1-4460-975f-50aa19110234] received
[2026-03-30 04:04:47,653: INFO/MainProcess] Task tasks.scrape_pending_urls[99c9b49c-38d1-4460-975f-50aa19110234] succeeded in 0.002635899931192398s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:05:17,650: INFO/MainProcess] Task tasks.scrape_pending_urls[f597bb9b-6669-46da-986d-f9588b1935e4] received
[2026-03-30 04:05:17,653: INFO/MainProcess] Task tasks.scrape_pending_urls[f597bb9b-6669-46da-986d-f9588b1935e4] succeeded in 0.002676400006748736s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:05:47,650: INFO/MainProcess] Task tasks.scrape_pending_urls[035b9627-2a7f-4b42-b008-d13cb834a8eb] received
[2026-03-30 04:05:47,653: INFO/MainProcess] Task tasks.scrape_pending_urls[035b9627-2a7f-4b42-b008-d13cb834a8eb] succeeded in 0.002780499984510243s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:06:17,650: INFO/MainProcess] Task tasks.scrape_pending_urls[8f9b131d-7a64-4600-a708-146a39f2373c] received
[2026-03-30 04:06:17,653: INFO/MainProcess] Task tasks.scrape_pending_urls[8f9b131d-7a64-4600-a708-146a39f2373c] succeeded in 0.0028264999855309725s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:06:47,650: INFO/MainProcess] Task tasks.scrape_pending_urls[3dacaa31-099e-43a3-baf3-1978352735e4] received
[2026-03-30 04:06:47,653: INFO/MainProcess] Task tasks.scrape_pending_urls[3dacaa31-099e-43a3-baf3-1978352735e4] succeeded in 0.002582400105893612s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:07:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[779b457a-9b79-4a08-ab3c-dfd943168628] received
[2026-03-30 04:07:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[779b457a-9b79-4a08-ab3c-dfd943168628] succeeded in 0.0027112000389024615s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:07:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[bb9aec7e-0cd4-4f01-8cd7-cd5c9222fd7f] received
[2026-03-30 04:07:47,657: INFO/MainProcess] Task tasks.scrape_pending_urls[bb9aec7e-0cd4-4f01-8cd7-cd5c9222fd7f] succeeded in 0.0029741000616922975s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:08:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[5a8fb194-8251-49d2-bd20-7efe22e5ea7d] received
[2026-03-30 04:08:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[5a8fb194-8251-49d2-bd20-7efe22e5ea7d] succeeded in 0.002523500006645918s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:08:47,496: INFO/MainProcess] Task tasks.collect_system_metrics[f191a414-eb78-46f4-8a8a-27fa82b233e5] received
[2026-03-30 04:08:48,013: INFO/MainProcess] Task tasks.collect_system_metrics[f191a414-eb78-46f4-8a8a-27fa82b233e5] succeeded in 0.5164030999876559s: {'cpu': 16.7, 'memory': 46.2}
[2026-03-30 04:08:48,015: INFO/MainProcess] Task tasks.scrape_pending_urls[bcbd6100-0323-4efd-adc7-46210b07cff3] received
[2026-03-30 04:08:48,017: INFO/MainProcess] Task tasks.scrape_pending_urls[bcbd6100-0323-4efd-adc7-46210b07cff3] succeeded in 0.002216599998064339s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:09:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[f1dd7cbc-c44b-40e1-9442-9280360584f1] received
[2026-03-30 04:09:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[f1dd7cbc-c44b-40e1-9442-9280360584f1] succeeded in 0.002700399956665933s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:09:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[e7c26137-248e-4831-8dd4-c1af6c37e661] received
[2026-03-30 04:09:47,657: INFO/MainProcess] Task tasks.scrape_pending_urls[e7c26137-248e-4831-8dd4-c1af6c37e661] succeeded in 0.0025156999472528696s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:10:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[b92b6f59-73b0-4841-aa90-413dff8045c5] received
[2026-03-30 04:10:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[b92b6f59-73b0-4841-aa90-413dff8045c5] succeeded in 0.0026542999548837543s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:10:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[d575c914-3746-4536-9203-5486f45ef259] received
[2026-03-30 04:10:47,657: INFO/MainProcess] Task tasks.scrape_pending_urls[d575c914-3746-4536-9203-5486f45ef259] succeeded in 0.002533299964852631s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:11:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[00a29fd7-3be1-4f94-87a7-48ed7a1ee26f] received
[2026-03-30 04:11:17,658: INFO/MainProcess] Task tasks.scrape_pending_urls[00a29fd7-3be1-4f94-87a7-48ed7a1ee26f] succeeded in 0.0031843000324442983s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:11:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[b402640f-4a54-4579-808a-2949a86fac5a] received
[2026-03-30 04:11:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[b402640f-4a54-4579-808a-2949a86fac5a] succeeded in 0.0031277999514713883s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:12:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[9249af0d-126b-4bbb-90c5-c2368fbd8710] received
[2026-03-30 04:12:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[9249af0d-126b-4bbb-90c5-c2368fbd8710] succeeded in 0.002695400035008788s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:12:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[f54ca8c7-5579-4063-89db-cd23eaba6fb2] received
[2026-03-30 04:12:47,657: INFO/MainProcess] Task tasks.scrape_pending_urls[f54ca8c7-5579-4063-89db-cd23eaba6fb2] succeeded in 0.0026753999991342425s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:13:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[44d6ba60-079c-4070-b40d-08514b7747d6] received
[2026-03-30 04:13:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[44d6ba60-079c-4070-b40d-08514b7747d6] succeeded in 0.0027483999729156494s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:13:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[fcecaeba-a028-4180-a788-f165d17da78c] received
[2026-03-30 04:13:48,017: INFO/MainProcess] Task tasks.collect_system_metrics[fcecaeba-a028-4180-a788-f165d17da78c] succeeded in 0.5159060000441968s: {'cpu': 10.9, 'memory': 45.9}
[2026-03-30 04:13:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[7068f533-d113-43b6-af29-12631d52257b] received
[2026-03-30 04:13:48,022: INFO/MainProcess] Task tasks.scrape_pending_urls[7068f533-d113-43b6-af29-12631d52257b] succeeded in 0.0026325000217184424s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:14:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[29e9d94e-303b-476f-86d0-d0cb01023efa] received
[2026-03-30 04:14:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[29e9d94e-303b-476f-86d0-d0cb01023efa] succeeded in 0.0027027000905945897s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:14:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[785f9bac-2274-4663-8ea1-e6959459cc9e] received
[2026-03-30 04:14:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[785f9bac-2274-4663-8ea1-e6959459cc9e] succeeded in 0.0028732999926432967s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:15:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[2e66dc33-b4d9-43ac-bed5-3212d9019ab3] received
[2026-03-30 04:15:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[2e66dc33-b4d9-43ac-bed5-3212d9019ab3] succeeded in 0.0025396000128239393s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:15:47,654: INFO/MainProcess] Task tasks.scrape_pending_urls[b45182f6-e18c-45d3-901e-3002acaaf7d8] received
[2026-03-30 04:15:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[b45182f6-e18c-45d3-901e-3002acaaf7d8] succeeded in 0.0029317999724298716s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:16:17,654: INFO/MainProcess] Task tasks.scrape_pending_urls[958066d1-df16-4c30-98f6-18587f5772ad] received
[2026-03-30 04:16:17,657: INFO/MainProcess] Task tasks.scrape_pending_urls[958066d1-df16-4c30-98f6-18587f5772ad] succeeded in 0.002769300015643239s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:16:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[d6431a31-267d-4694-96c5-6b744baa57f2] received
[2026-03-30 04:16:47,661: INFO/MainProcess] Task tasks.scrape_pending_urls[d6431a31-267d-4694-96c5-6b744baa57f2] succeeded in 0.0026328000240027905s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:17:17,658: INFO/MainProcess] Task tasks.scrape_pending_urls[8106328c-6f26-4a0f-8843-62bae966f9b1] received
[2026-03-30 04:17:17,661: INFO/MainProcess] Task tasks.scrape_pending_urls[8106328c-6f26-4a0f-8843-62bae966f9b1] succeeded in 0.002625899971462786s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:17:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[4a47299c-3878-4831-b179-90a023e3ee5f] received
[2026-03-30 04:17:47,661: INFO/MainProcess] Task tasks.scrape_pending_urls[4a47299c-3878-4831-b179-90a023e3ee5f] succeeded in 0.0027939999708905816s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:18:17,658: INFO/MainProcess] Task tasks.scrape_pending_urls[bc837a55-3900-4fde-b784-1a195226a952] received
[2026-03-30 04:18:17,661: INFO/MainProcess] Task tasks.scrape_pending_urls[bc837a55-3900-4fde-b784-1a195226a952] succeeded in 0.002535699983127415s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:18:47,486: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d3ed710a-4061-4eaf-bc8a-737bb460f8f7] received
[2026-03-30 04:18:47,489: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 04:18:47,490: INFO/MainProcess] Task tasks.reset_stale_processing_urls[d3ed710a-4061-4eaf-bc8a-737bb460f8f7] succeeded in 0.003152000019326806s: {'reset': 0}
[2026-03-30 04:18:47,500: INFO/MainProcess] Task tasks.collect_system_metrics[b71d4ed7-4be0-427a-a760-368af203a2e0] received
[2026-03-30 04:18:48,016: INFO/MainProcess] Task tasks.collect_system_metrics[b71d4ed7-4be0-427a-a760-368af203a2e0] succeeded in 0.5160348999779671s: {'cpu': 12.5, 'memory': 46.1}
[2026-03-30 04:18:48,018: INFO/MainProcess] Task tasks.scrape_pending_urls[2617ff8a-2436-4910-9af2-b3a5e60e5f3c] received
[2026-03-30 04:18:48,021: INFO/MainProcess] Task tasks.scrape_pending_urls[2617ff8a-2436-4910-9af2-b3a5e60e5f3c] succeeded in 0.00282689998857677s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:19:17,659: INFO/MainProcess] Task tasks.scrape_pending_urls[fd99d4b9-40c5-46be-979d-9f1df9846593] received
[2026-03-30 04:19:17,662: INFO/MainProcess] Task tasks.scrape_pending_urls[fd99d4b9-40c5-46be-979d-9f1df9846593] succeeded in 0.002801500027999282s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:19:47,659: INFO/MainProcess] Task tasks.scrape_pending_urls[b86267bd-52fe-4693-b0ed-b86558745cb7] received
[2026-03-30 04:19:47,662: INFO/MainProcess] Task tasks.scrape_pending_urls[b86267bd-52fe-4693-b0ed-b86558745cb7] succeeded in 0.0027700000209733844s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:20:17,658: INFO/MainProcess] Task tasks.scrape_pending_urls[e2bd1eff-a70e-4fda-a7ba-3647f62dbc99] received
[2026-03-30 04:20:17,661: INFO/MainProcess] Task tasks.scrape_pending_urls[e2bd1eff-a70e-4fda-a7ba-3647f62dbc99] succeeded in 0.002613399992696941s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:20:47,659: INFO/MainProcess] Task tasks.scrape_pending_urls[71aa0c8b-4ab1-4c6a-ac13-3823d78de9d5] received
[2026-03-30 04:20:47,662: INFO/MainProcess] Task tasks.scrape_pending_urls[71aa0c8b-4ab1-4c6a-ac13-3823d78de9d5] succeeded in 0.0027117999270558357s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:21:17,658: INFO/MainProcess] Task tasks.scrape_pending_urls[83e560ac-5302-4379-97de-377a538c7362] received
[2026-03-30 04:21:17,662: INFO/MainProcess] Task tasks.scrape_pending_urls[83e560ac-5302-4379-97de-377a538c7362] succeeded in 0.0027762000681832433s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:21:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[a2bbcf2f-57cc-48d5-b135-69f278aaad95] received
[2026-03-30 04:21:47,662: INFO/MainProcess] Task tasks.scrape_pending_urls[a2bbcf2f-57cc-48d5-b135-69f278aaad95] succeeded in 0.002814300009049475s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:22:17,659: INFO/MainProcess] Task tasks.scrape_pending_urls[37b3ea7b-2963-411c-988b-7f69f88644f3] received
[2026-03-30 04:22:17,662: INFO/MainProcess] Task tasks.scrape_pending_urls[37b3ea7b-2963-411c-988b-7f69f88644f3] succeeded in 0.0028469000244513154s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:22:47,658: INFO/MainProcess] Task tasks.scrape_pending_urls[a837beeb-1c18-4b22-ad2f-fbbae7e19720] received
[2026-03-30 04:22:47,661: INFO/MainProcess] Task tasks.scrape_pending_urls[a837beeb-1c18-4b22-ad2f-fbbae7e19720] succeeded in 0.002520899986848235s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:23:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[b5277e1b-03ab-4d5d-b306-3ad35a5b74eb] received
[2026-03-30 04:23:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[b5277e1b-03ab-4d5d-b306-3ad35a5b74eb] succeeded in 0.002975700073875487s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:23:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[52678ec3-4070-41e0-80c4-4b0a9e9fef6f] received
[2026-03-30 04:23:48,018: INFO/MainProcess] Task tasks.collect_system_metrics[52678ec3-4070-41e0-80c4-4b0a9e9fef6f] succeeded in 0.516655300045386s: {'cpu': 14.2, 'memory': 46.0}
[2026-03-30 04:23:48,020: INFO/MainProcess] Task tasks.scrape_pending_urls[777eb0dc-e908-49f5-8c26-c26c981972e0] received
[2026-03-30 04:23:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[777eb0dc-e908-49f5-8c26-c26c981972e0] succeeded in 0.0028111999854445457s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:24:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[529c53db-2959-413b-ac1e-1a80781160d2] received
[2026-03-30 04:24:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[529c53db-2959-413b-ac1e-1a80781160d2] succeeded in 0.002492800005711615s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:24:47,664: INFO/MainProcess] Task tasks.scrape_pending_urls[ffd9d60e-902a-472c-97a5-985eac48b587] received
[2026-03-30 04:24:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[ffd9d60e-902a-472c-97a5-985eac48b587] succeeded in 0.0029157999670132995s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:25:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[7ea38c03-49f9-4a29-91d4-f0cac8bc4970] received
[2026-03-30 04:25:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[7ea38c03-49f9-4a29-91d4-f0cac8bc4970] succeeded in 0.0027107999194413424s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:25:47,664: INFO/MainProcess] Task tasks.scrape_pending_urls[d4ab5f59-9ad2-409a-b701-208e0e1cf6c7] received
[2026-03-30 04:25:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[d4ab5f59-9ad2-409a-b701-208e0e1cf6c7] succeeded in 0.002883999957703054s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:26:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[a2a4e156-0316-4300-a301-bf3a89ff3787] received
[2026-03-30 04:26:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[a2a4e156-0316-4300-a301-bf3a89ff3787] succeeded in 0.0027194999856874347s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:26:47,664: INFO/MainProcess] Task tasks.scrape_pending_urls[55640865-d0cc-4e2d-821c-76564dd7c101] received
[2026-03-30 04:26:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[55640865-d0cc-4e2d-821c-76564dd7c101] succeeded in 0.002798300003632903s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:27:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[5689db0a-4e57-4d08-94a7-6ab881106296] received
[2026-03-30 04:27:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[5689db0a-4e57-4d08-94a7-6ab881106296] succeeded in 0.002722000004723668s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:27:47,663: INFO/MainProcess] Task tasks.scrape_pending_urls[e1c83839-3f3e-436d-910d-843c80d56271] received
[2026-03-30 04:27:47,732: INFO/MainProcess] Task tasks.scrape_pending_urls[e1c83839-3f3e-436d-910d-843c80d56271] succeeded in 0.06772789999376982s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:28:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[646455d4-8e45-4af8-b29d-7e7f8e510f5a] received
[2026-03-30 04:28:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[646455d4-8e45-4af8-b29d-7e7f8e510f5a] succeeded in 0.0026830999413505197s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:28:47,500: INFO/MainProcess] Task tasks.collect_system_metrics[22a3897b-46b1-4623-b09c-707a07097b94] received
[2026-03-30 04:28:48,017: INFO/MainProcess] Task tasks.collect_system_metrics[22a3897b-46b1-4623-b09c-707a07097b94] succeeded in 0.5163375000702217s: {'cpu': 11.5, 'memory': 45.8}
[2026-03-30 04:28:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[b6db9340-02ae-411a-aa9e-f4d87a38337c] received
[2026-03-30 04:28:48,022: INFO/MainProcess] Task tasks.scrape_pending_urls[b6db9340-02ae-411a-aa9e-f4d87a38337c] succeeded in 0.0024108000798150897s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:29:17,664: INFO/MainProcess] Task tasks.scrape_pending_urls[144fa23a-e455-4694-b9f8-c2e7665b0ceb] received
[2026-03-30 04:29:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[144fa23a-e455-4694-b9f8-c2e7665b0ceb] succeeded in 0.002749399980530143s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:29:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[49edbbf3-2ef5-4f12-a494-05db75866a76] received
[2026-03-30 04:29:47,670: INFO/MainProcess] Task tasks.scrape_pending_urls[49edbbf3-2ef5-4f12-a494-05db75866a76] succeeded in 0.002563500078395009s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[72216ca5-5b15-4a6d-9710-cc39aca95b38] received
[2026-03-30 04:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[72216ca5-5b15-4a6d-9710-cc39aca95b38] succeeded in 0.0014158999547362328s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 04:30:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[76860671-5e4c-4568-ab18-c107e181777b] received
[2026-03-30 04:30:17,670: INFO/MainProcess] Task tasks.scrape_pending_urls[76860671-5e4c-4568-ab18-c107e181777b] succeeded in 0.002999100019223988s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:30:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[3dee5b75-b978-4151-8734-59df4f716051] received
[2026-03-30 04:30:47,670: INFO/MainProcess] Task tasks.scrape_pending_urls[3dee5b75-b978-4151-8734-59df4f716051] succeeded in 0.002584200003184378s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:31:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[90bbef84-b205-4c14-8e3a-38848a4796be] received
[2026-03-30 04:31:17,670: INFO/MainProcess] Task tasks.scrape_pending_urls[90bbef84-b205-4c14-8e3a-38848a4796be] succeeded in 0.003070299979299307s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:31:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[367bb3fd-45d3-435e-ae71-8931ccf97965] received
[2026-03-30 04:31:47,670: INFO/MainProcess] Task tasks.scrape_pending_urls[367bb3fd-45d3-435e-ae71-8931ccf97965] succeeded in 0.002738500013947487s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:32:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[e26b668f-3e6c-45be-8169-d0531525d353] received
[2026-03-30 04:32:17,670: INFO/MainProcess] Task tasks.scrape_pending_urls[e26b668f-3e6c-45be-8169-d0531525d353] succeeded in 0.002681699930690229s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:32:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[c1c1d598-1710-4dac-b378-ad815c99d9f7] received
[2026-03-30 04:32:47,735: INFO/MainProcess] Task tasks.scrape_pending_urls[c1c1d598-1710-4dac-b378-ad815c99d9f7] succeeded in 0.06795890000648797s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:33:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[2be3fabd-3e9f-4e3e-a78b-b018e6ac4dc1] received
[2026-03-30 04:33:17,670: INFO/MainProcess] Task tasks.scrape_pending_urls[2be3fabd-3e9f-4e3e-a78b-b018e6ac4dc1] succeeded in 0.002700299955904484s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:33:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[4f613b85-6a33-4918-8760-1487bc0bf445] received
[2026-03-30 04:33:48,017: INFO/MainProcess] Task tasks.collect_system_metrics[4f613b85-6a33-4918-8760-1487bc0bf445] succeeded in 0.5162477000849321s: {'cpu': 11.2, 'memory': 46.0}
[2026-03-30 04:33:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[e4eb1ee1-c67e-4177-8973-9197df8a321f] received
[2026-03-30 04:33:48,022: INFO/MainProcess] Task tasks.scrape_pending_urls[e4eb1ee1-c67e-4177-8973-9197df8a321f] succeeded in 0.0024468000046908855s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:34:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[7ae7976b-7911-40e5-8d98-75acb9f928f5] received
[2026-03-30 04:34:17,670: INFO/MainProcess] Task tasks.scrape_pending_urls[7ae7976b-7911-40e5-8d98-75acb9f928f5] succeeded in 0.003038399969227612s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:34:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[12cf5a6d-9e26-463f-8e03-c76bf368a374] received
[2026-03-30 04:34:47,670: INFO/MainProcess] Task tasks.scrape_pending_urls[12cf5a6d-9e26-463f-8e03-c76bf368a374] succeeded in 0.0025927999522536993s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:35:17,667: INFO/MainProcess] Task tasks.scrape_pending_urls[e1d3efec-d251-4092-afba-b7b75d9825cf] received
[2026-03-30 04:35:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[e1d3efec-d251-4092-afba-b7b75d9825cf] succeeded in 0.002979199984110892s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:35:47,667: INFO/MainProcess] Task tasks.scrape_pending_urls[655b93d4-079e-467d-92d3-29981a981276] received
[2026-03-30 04:35:47,670: INFO/MainProcess] Task tasks.scrape_pending_urls[655b93d4-079e-467d-92d3-29981a981276] succeeded in 0.0028470000252127647s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:36:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[9b05b864-857a-4687-96d1-0f28c42645d2] received
[2026-03-30 04:36:17,674: INFO/MainProcess] Task tasks.scrape_pending_urls[9b05b864-857a-4687-96d1-0f28c42645d2] succeeded in 0.0027882999274879694s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:36:47,671: INFO/MainProcess] Task tasks.scrape_pending_urls[6345114c-013f-4461-a923-60b8e9fad4f7] received
[2026-03-30 04:36:47,674: INFO/MainProcess] Task tasks.scrape_pending_urls[6345114c-013f-4461-a923-60b8e9fad4f7] succeeded in 0.0029862000374123454s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:37:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[690127d1-4b79-486e-a67a-57e2eb84a40a] received
[2026-03-30 04:37:17,675: INFO/MainProcess] Task tasks.scrape_pending_urls[690127d1-4b79-486e-a67a-57e2eb84a40a] succeeded in 0.002954700030386448s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:37:47,671: INFO/MainProcess] Task tasks.scrape_pending_urls[c628b1b3-fa69-40bc-a705-8d44d0b5e3cc] received
[2026-03-30 04:37:47,674: INFO/MainProcess] Task tasks.scrape_pending_urls[c628b1b3-fa69-40bc-a705-8d44d0b5e3cc] succeeded in 0.002609000075608492s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:38:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[c2e555cc-df74-4ed8-a71a-c76aac956110] received
[2026-03-30 04:38:17,675: INFO/MainProcess] Task tasks.scrape_pending_urls[c2e555cc-df74-4ed8-a71a-c76aac956110] succeeded in 0.0031234000343829393s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:38:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[b343d2e5-4448-4a99-a4cb-8875a788a971] received
[2026-03-30 04:38:48,009: INFO/MainProcess] Task tasks.collect_system_metrics[b343d2e5-4448-4a99-a4cb-8875a788a971] succeeded in 0.5079601999605075s: {'cpu': 11.2, 'memory': 46.0}
[2026-03-30 04:38:48,011: INFO/MainProcess] Task tasks.scrape_pending_urls[e3f61a86-3a63-4676-85a7-e3bd523003c4] received
[2026-03-30 04:38:48,086: INFO/MainProcess] Task tasks.scrape_pending_urls[e3f61a86-3a63-4676-85a7-e3bd523003c4] succeeded in 0.07473210000898689s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:39:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[db8efcfe-cff7-4ce9-91b5-605f40dac855] received
[2026-03-30 04:39:17,675: INFO/MainProcess] Task tasks.scrape_pending_urls[db8efcfe-cff7-4ce9-91b5-605f40dac855] succeeded in 0.0034266000147908926s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:39:47,671: INFO/MainProcess] Task tasks.scrape_pending_urls[f28292b3-dfcb-42e8-b357-0dd700efcae7] received
[2026-03-30 04:39:47,675: INFO/MainProcess] Task tasks.scrape_pending_urls[f28292b3-dfcb-42e8-b357-0dd700efcae7] succeeded in 0.0028519999468699098s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:40:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[7f0a89a9-6502-4350-9940-2e02430ccf22] received
[2026-03-30 04:40:17,675: INFO/MainProcess] Task tasks.scrape_pending_urls[7f0a89a9-6502-4350-9940-2e02430ccf22] succeeded in 0.00309070001821965s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:40:47,671: INFO/MainProcess] Task tasks.scrape_pending_urls[7e0d4f3f-0987-4be9-86d9-8c781a7385c9] received
[2026-03-30 04:40:47,674: INFO/MainProcess] Task tasks.scrape_pending_urls[7e0d4f3f-0987-4be9-86d9-8c781a7385c9] succeeded in 0.0026944000273942947s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:41:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[601756f4-4aff-4fc2-a6d2-f9107d02d957] received
[2026-03-30 04:41:17,674: INFO/MainProcess] Task tasks.scrape_pending_urls[601756f4-4aff-4fc2-a6d2-f9107d02d957] succeeded in 0.0027680000057443976s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:41:47,671: INFO/MainProcess] Task tasks.scrape_pending_urls[b86fe80e-d592-470e-a807-f8b94b8675a3] received
[2026-03-30 04:41:47,674: INFO/MainProcess] Task tasks.scrape_pending_urls[b86fe80e-d592-470e-a807-f8b94b8675a3] succeeded in 0.002705099992454052s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:42:17,671: INFO/MainProcess] Task tasks.scrape_pending_urls[3d1da232-151d-4f27-8756-ccf2a43c65da] received
[2026-03-30 04:42:17,674: INFO/MainProcess] Task tasks.scrape_pending_urls[3d1da232-151d-4f27-8756-ccf2a43c65da] succeeded in 0.0027982000028714538s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:42:47,716: INFO/MainProcess] Task tasks.scrape_pending_urls[ee861ddf-dfaa-4df8-a501-05510a06f425] received
[2026-03-30 04:42:47,719: INFO/MainProcess] Task tasks.scrape_pending_urls[ee861ddf-dfaa-4df8-a501-05510a06f425] succeeded in 0.00255129998549819s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:43:17,715: INFO/MainProcess] Task tasks.scrape_pending_urls[2ca08b29-5526-4b17-bbfe-084448ffa7c8] received
[2026-03-30 04:43:17,719: INFO/MainProcess] Task tasks.scrape_pending_urls[2ca08b29-5526-4b17-bbfe-084448ffa7c8] succeeded in 0.0027890000492334366s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:43:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[36361efd-4408-44a3-a0d3-3154bc8115d5] received
[2026-03-30 04:43:48,019: INFO/MainProcess] Task tasks.collect_system_metrics[36361efd-4408-44a3-a0d3-3154bc8115d5] succeeded in 0.5184212001040578s: {'cpu': 14.3, 'memory': 46.0}
[2026-03-30 04:43:48,021: INFO/MainProcess] Task tasks.scrape_pending_urls[6dd34406-a807-4ce7-b2da-56d8b3856d8c] received
[2026-03-30 04:43:48,024: INFO/MainProcess] Task tasks.scrape_pending_urls[6dd34406-a807-4ce7-b2da-56d8b3856d8c] succeeded in 0.0026591999921947718s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:44:17,717: INFO/MainProcess] Task tasks.scrape_pending_urls[e8a95862-fdaf-4bf4-b2a9-1621d3f9c817] received
[2026-03-30 04:44:17,720: INFO/MainProcess] Task tasks.scrape_pending_urls[e8a95862-fdaf-4bf4-b2a9-1621d3f9c817] succeeded in 0.002723700017668307s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:44:47,716: INFO/MainProcess] Task tasks.scrape_pending_urls[88277bae-eb45-49c9-ade0-bd1738fa9ec8] received
[2026-03-30 04:44:47,719: INFO/MainProcess] Task tasks.scrape_pending_urls[88277bae-eb45-49c9-ade0-bd1738fa9ec8] succeeded in 0.0026931000174954534s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:45:17,716: INFO/MainProcess] Task tasks.scrape_pending_urls[d47fce59-7ea6-47ff-bb8b-5219f7567b99] received
[2026-03-30 04:45:17,719: INFO/MainProcess] Task tasks.scrape_pending_urls[d47fce59-7ea6-47ff-bb8b-5219f7567b99] succeeded in 0.0031443999614566565s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:45:47,716: INFO/MainProcess] Task tasks.scrape_pending_urls[08a419dd-c409-4576-ae01-57f3821bc982] received
[2026-03-30 04:45:47,719: INFO/MainProcess] Task tasks.scrape_pending_urls[08a419dd-c409-4576-ae01-57f3821bc982] succeeded in 0.0028505000518634915s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:46:17,716: INFO/MainProcess] Task tasks.scrape_pending_urls[3f9a818a-be3f-452d-9751-ea60482d2edc] received
[2026-03-30 04:46:17,719: INFO/MainProcess] Task tasks.scrape_pending_urls[3f9a818a-be3f-452d-9751-ea60482d2edc] succeeded in 0.002880999934859574s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:46:47,716: INFO/MainProcess] Task tasks.scrape_pending_urls[85314303-410e-4664-aa13-ce3cbdf32ecd] received
[2026-03-30 04:46:47,719: INFO/MainProcess] Task tasks.scrape_pending_urls[85314303-410e-4664-aa13-ce3cbdf32ecd] succeeded in 0.0027612000703811646s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:47:17,716: INFO/MainProcess] Task tasks.scrape_pending_urls[fe13f84e-5530-4a19-a282-8ac55574a06c] received
[2026-03-30 04:47:17,719: INFO/MainProcess] Task tasks.scrape_pending_urls[fe13f84e-5530-4a19-a282-8ac55574a06c] succeeded in 0.0029088000301271677s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:47:47,716: INFO/MainProcess] Task tasks.scrape_pending_urls[fd264c53-328f-414d-8766-014b9d1759b1] received
[2026-03-30 04:47:47,719: INFO/MainProcess] Task tasks.scrape_pending_urls[fd264c53-328f-414d-8766-014b9d1759b1] succeeded in 0.002607799950055778s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:48:17,716: INFO/MainProcess] Task tasks.scrape_pending_urls[ebd6fb75-6f03-4f35-bb9e-5f2e97d9bf73] received
[2026-03-30 04:48:17,719: INFO/MainProcess] Task tasks.scrape_pending_urls[ebd6fb75-6f03-4f35-bb9e-5f2e97d9bf73] succeeded in 0.002784400014206767s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:48:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[0753275b-53b5-4a64-ab57-5fcae74038b1] received
[2026-03-30 04:48:47,490: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 04:48:47,491: INFO/MainProcess] Task tasks.reset_stale_processing_urls[0753275b-53b5-4a64-ab57-5fcae74038b1] succeeded in 0.0040862999157980084s: {'reset': 0}
[2026-03-30 04:48:47,499: INFO/MainProcess] Task tasks.collect_system_metrics[8c85bc45-a01a-4471-a639-8dd4ddc53bd5] received
[2026-03-30 04:48:48,016: INFO/MainProcess] Task tasks.collect_system_metrics[8c85bc45-a01a-4471-a639-8dd4ddc53bd5] succeeded in 0.5159488000208512s: {'cpu': 13.6, 'memory': 45.9}
[2026-03-30 04:48:48,018: INFO/MainProcess] Task tasks.scrape_pending_urls[6b9a0813-b602-4213-a7ab-d98c2e913647] received
[2026-03-30 04:48:48,020: INFO/MainProcess] Task tasks.scrape_pending_urls[6b9a0813-b602-4213-a7ab-d98c2e913647] succeeded in 0.0022098999470472336s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:49:17,721: INFO/MainProcess] Task tasks.scrape_pending_urls[2fd12403-b24b-4357-a166-6b61466b4f39] received
[2026-03-30 04:49:17,724: INFO/MainProcess] Task tasks.scrape_pending_urls[2fd12403-b24b-4357-a166-6b61466b4f39] succeeded in 0.002789999940432608s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:49:47,720: INFO/MainProcess] Task tasks.scrape_pending_urls[a9c24a0b-a289-4bde-8141-1588fa7677ae] received
[2026-03-30 04:49:47,724: INFO/MainProcess] Task tasks.scrape_pending_urls[a9c24a0b-a289-4bde-8141-1588fa7677ae] succeeded in 0.0026910000015050173s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:50:17,720: INFO/MainProcess] Task tasks.scrape_pending_urls[250e4f76-a3ec-4b32-bc0e-8254dea80dbf] received
[2026-03-30 04:50:17,723: INFO/MainProcess] Task tasks.scrape_pending_urls[250e4f76-a3ec-4b32-bc0e-8254dea80dbf] succeeded in 0.0026470000157132745s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:50:47,720: INFO/MainProcess] Task tasks.scrape_pending_urls[382c2cb9-01ce-4d12-93cc-dfaadb672a5c] received
[2026-03-30 04:50:47,723: INFO/MainProcess] Task tasks.scrape_pending_urls[382c2cb9-01ce-4d12-93cc-dfaadb672a5c] succeeded in 0.0026410999707877636s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:51:17,720: INFO/MainProcess] Task tasks.scrape_pending_urls[7b2f5063-2adb-4525-8131-fa5e23a7cf21] received
[2026-03-30 04:51:17,723: INFO/MainProcess] Task tasks.scrape_pending_urls[7b2f5063-2adb-4525-8131-fa5e23a7cf21] succeeded in 0.002587399911135435s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:51:47,721: INFO/MainProcess] Task tasks.scrape_pending_urls[1d9cfff2-5272-4cbf-816f-e5a0a76040b8] received
[2026-03-30 04:51:47,724: INFO/MainProcess] Task tasks.scrape_pending_urls[1d9cfff2-5272-4cbf-816f-e5a0a76040b8] succeeded in 0.002915599965490401s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:52:17,721: INFO/MainProcess] Task tasks.scrape_pending_urls[94852019-255f-4c38-b2ee-56d2ff5fb020] received
[2026-03-30 04:52:17,724: INFO/MainProcess] Task tasks.scrape_pending_urls[94852019-255f-4c38-b2ee-56d2ff5fb020] succeeded in 0.0029109000461176038s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:52:47,720: INFO/MainProcess] Task tasks.scrape_pending_urls[b590b142-073e-4767-b764-f2426793cace] received
[2026-03-30 04:52:47,723: INFO/MainProcess] Task tasks.scrape_pending_urls[b590b142-073e-4767-b764-f2426793cace] succeeded in 0.00255129998549819s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:53:17,721: INFO/MainProcess] Task tasks.scrape_pending_urls[1aea64ac-50c0-4ecc-9ad4-0d2cf926fdb0] received
[2026-03-30 04:53:17,724: INFO/MainProcess] Task tasks.scrape_pending_urls[1aea64ac-50c0-4ecc-9ad4-0d2cf926fdb0] succeeded in 0.003126199939288199s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:53:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[8ae4c05a-4d9e-461c-8df6-661ed335a627] received
[2026-03-30 04:53:48,019: INFO/MainProcess] Task tasks.collect_system_metrics[8ae4c05a-4d9e-461c-8df6-661ed335a627] succeeded in 0.5180486000608653s: {'cpu': 10.4, 'memory': 46.0}
[2026-03-30 04:53:48,021: INFO/MainProcess] Task tasks.scrape_pending_urls[22861b91-5933-4143-822b-79094294d548] received
[2026-03-30 04:53:48,024: INFO/MainProcess] Task tasks.scrape_pending_urls[22861b91-5933-4143-822b-79094294d548] succeeded in 0.0027000000700354576s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:54:17,721: INFO/MainProcess] Task tasks.scrape_pending_urls[06ad7f39-ec2b-4578-aa2c-7573dcb696ce] received
[2026-03-30 04:54:17,724: INFO/MainProcess] Task tasks.scrape_pending_urls[06ad7f39-ec2b-4578-aa2c-7573dcb696ce] succeeded in 0.002744699944742024s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:54:47,721: INFO/MainProcess] Task tasks.scrape_pending_urls[a6580537-9582-4861-b704-2a798799f57a] received
[2026-03-30 04:54:47,724: INFO/MainProcess] Task tasks.scrape_pending_urls[a6580537-9582-4861-b704-2a798799f57a] succeeded in 0.002611099975183606s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:55:17,721: INFO/MainProcess] Task tasks.scrape_pending_urls[798278cd-e246-421f-a2c6-74efafedd339] received
[2026-03-30 04:55:17,724: INFO/MainProcess] Task tasks.scrape_pending_urls[798278cd-e246-421f-a2c6-74efafedd339] succeeded in 0.003002599929459393s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:55:47,725: INFO/MainProcess] Task tasks.scrape_pending_urls[1483d0a9-92b4-4df8-8553-046ae3bee7ab] received
[2026-03-30 04:55:47,728: INFO/MainProcess] Task tasks.scrape_pending_urls[1483d0a9-92b4-4df8-8553-046ae3bee7ab] succeeded in 0.0028068999527022243s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:56:17,725: INFO/MainProcess] Task tasks.scrape_pending_urls[06fa3cda-2067-4c1f-96f2-45604526baee] received
[2026-03-30 04:56:17,727: INFO/MainProcess] Task tasks.scrape_pending_urls[06fa3cda-2067-4c1f-96f2-45604526baee] succeeded in 0.0025468000676482916s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:56:47,725: INFO/MainProcess] Task tasks.scrape_pending_urls[69809b43-116c-4c5d-b1d4-718654db27db] received
[2026-03-30 04:56:47,728: INFO/MainProcess] Task tasks.scrape_pending_urls[69809b43-116c-4c5d-b1d4-718654db27db] succeeded in 0.002796500106342137s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:57:17,725: INFO/MainProcess] Task tasks.scrape_pending_urls[0a8581bc-2adc-4458-a6b1-7adec9c6a0a1] received
[2026-03-30 04:57:17,728: INFO/MainProcess] Task tasks.scrape_pending_urls[0a8581bc-2adc-4458-a6b1-7adec9c6a0a1] succeeded in 0.002562900073826313s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:57:47,725: INFO/MainProcess] Task tasks.scrape_pending_urls[df98fca8-d74e-4f27-9e5e-f0e58ec4b0e3] received
[2026-03-30 04:57:47,728: INFO/MainProcess] Task tasks.scrape_pending_urls[df98fca8-d74e-4f27-9e5e-f0e58ec4b0e3] succeeded in 0.002649799920618534s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:58:17,725: INFO/MainProcess] Task tasks.scrape_pending_urls[0ce9637e-448e-49cd-bcc3-5ab1788a6b7c] received
[2026-03-30 04:58:17,728: INFO/MainProcess] Task tasks.scrape_pending_urls[0ce9637e-448e-49cd-bcc3-5ab1788a6b7c] succeeded in 0.0026694999542087317s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:58:47,501: INFO/MainProcess] Task tasks.collect_system_metrics[dbdbd59e-8bdc-4028-a7d9-0b67c443cd0c] received
[2026-03-30 04:58:48,017: INFO/MainProcess] Task tasks.collect_system_metrics[dbdbd59e-8bdc-4028-a7d9-0b67c443cd0c] succeeded in 0.5159694000612944s: {'cpu': 12.5, 'memory': 45.8}
[2026-03-30 04:58:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[ee5acca5-c841-48f1-96c3-cf4b6b1d6a06] received
[2026-03-30 04:58:48,022: INFO/MainProcess] Task tasks.scrape_pending_urls[ee5acca5-c841-48f1-96c3-cf4b6b1d6a06] succeeded in 0.0022501000203192234s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:59:17,725: INFO/MainProcess] Task tasks.scrape_pending_urls[25068582-8b20-45b8-826c-16a988a1c3d8] received
[2026-03-30 04:59:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[25068582-8b20-45b8-826c-16a988a1c3d8] succeeded in 0.003283899975940585s: {'status': 'idle', 'pending': 0}
[2026-03-30 04:59:47,725: INFO/MainProcess] Task tasks.scrape_pending_urls[3ab26c83-845f-4603-a02c-d32f49df1631] received
[2026-03-30 04:59:47,728: INFO/MainProcess] Task tasks.scrape_pending_urls[3ab26c83-845f-4603-a02c-d32f49df1631] succeeded in 0.002785000018775463s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:00:17,725: INFO/MainProcess] Task tasks.scrape_pending_urls[b33ef89f-da30-4231-8274-762f6208fd7a] received
[2026-03-30 05:00:17,728: INFO/MainProcess] Task tasks.scrape_pending_urls[b33ef89f-da30-4231-8274-762f6208fd7a] succeeded in 0.0026140999980270863s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:00:47,725: INFO/MainProcess] Task tasks.scrape_pending_urls[77c75e0e-fd09-4b14-9ab0-bfaff1e084e9] received
[2026-03-30 05:00:47,728: INFO/MainProcess] Task tasks.scrape_pending_urls[77c75e0e-fd09-4b14-9ab0-bfaff1e084e9] succeeded in 0.002727600047364831s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:01:17,725: INFO/MainProcess] Task tasks.scrape_pending_urls[92fb9d3b-d1db-431e-be14-e07bcab62390] received
[2026-03-30 05:01:17,728: INFO/MainProcess] Task tasks.scrape_pending_urls[92fb9d3b-d1db-431e-be14-e07bcab62390] succeeded in 0.0026996000669896603s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:01:47,725: INFO/MainProcess] Task tasks.scrape_pending_urls[d979f100-5e83-443d-bc09-72b2ae43c880] received
[2026-03-30 05:01:47,728: INFO/MainProcess] Task tasks.scrape_pending_urls[d979f100-5e83-443d-bc09-72b2ae43c880] succeeded in 0.00268909998703748s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:02:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[fe80982c-9bd7-45f5-975c-1170e86891af] received
[2026-03-30 05:02:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[fe80982c-9bd7-45f5-975c-1170e86891af] succeeded in 0.0030109999934211373s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:02:47,729: INFO/MainProcess] Task tasks.scrape_pending_urls[f3220396-de04-43bd-8275-84cfd46432f3] received
[2026-03-30 05:02:47,732: INFO/MainProcess] Task tasks.scrape_pending_urls[f3220396-de04-43bd-8275-84cfd46432f3] succeeded in 0.002548700082115829s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:03:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[091bdbe8-7fb3-48e9-8a57-08c30d0712b1] received
[2026-03-30 05:03:17,731: INFO/MainProcess] Task tasks.scrape_pending_urls[091bdbe8-7fb3-48e9-8a57-08c30d0712b1] succeeded in 0.0026030000299215317s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:03:47,500: INFO/MainProcess] Task tasks.collect_system_metrics[3c4da02f-4114-48af-b072-732b87c28d95] received
[2026-03-30 05:03:48,017: INFO/MainProcess] Task tasks.collect_system_metrics[3c4da02f-4114-48af-b072-732b87c28d95] succeeded in 0.5165653000585735s: {'cpu': 13.1, 'memory': 45.9}
[2026-03-30 05:03:48,019: INFO/MainProcess] Task tasks.scrape_pending_urls[1cf15ba2-ca56-4e83-8bfb-55edbee87a3e] received
[2026-03-30 05:03:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[1cf15ba2-ca56-4e83-8bfb-55edbee87a3e] succeeded in 0.003300099982880056s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:04:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[79f383e6-2282-45e2-91dc-f5e7bda1667a] received
[2026-03-30 05:04:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[79f383e6-2282-45e2-91dc-f5e7bda1667a] succeeded in 0.0031111000571399927s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:04:47,730: INFO/MainProcess] Task tasks.scrape_pending_urls[abc6b57e-41a2-400f-8c5b-ba1b0053e5d4] received
[2026-03-30 05:04:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[abc6b57e-41a2-400f-8c5b-ba1b0053e5d4] succeeded in 0.0028313000220805407s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:05:17,730: INFO/MainProcess] Task tasks.scrape_pending_urls[28eb0232-9768-4b9b-87fb-c944d8abdd13] received
[2026-03-30 05:05:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[28eb0232-9768-4b9b-87fb-c944d8abdd13] succeeded in 0.0027236000169068575s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:05:47,729: INFO/MainProcess] Task tasks.scrape_pending_urls[03259ba6-cce5-4ad3-9bb8-a372af72b745] received
[2026-03-30 05:05:47,732: INFO/MainProcess] Task tasks.scrape_pending_urls[03259ba6-cce5-4ad3-9bb8-a372af72b745] succeeded in 0.0026326000224798918s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:06:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[b3d863ce-467e-4b0a-91ae-28ab9017cdca] received
[2026-03-30 05:06:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[b3d863ce-467e-4b0a-91ae-28ab9017cdca] succeeded in 0.0026822000509127975s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:06:47,729: INFO/MainProcess] Task tasks.scrape_pending_urls[718e70b4-0ecf-4555-a296-0d37cc6a8633] received
[2026-03-30 05:06:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[718e70b4-0ecf-4555-a296-0d37cc6a8633] succeeded in 0.0030480000423267484s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:07:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[eed2c9e5-ffc4-4280-be06-427ce6331364] received
[2026-03-30 05:07:17,732: INFO/MainProcess] Task tasks.scrape_pending_urls[eed2c9e5-ffc4-4280-be06-427ce6331364] succeeded in 0.002823699964210391s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:07:47,729: INFO/MainProcess] Task tasks.scrape_pending_urls[d7143e03-67ac-4e59-b45b-b2059d44d746] received
[2026-03-30 05:07:47,732: INFO/MainProcess] Task tasks.scrape_pending_urls[d7143e03-67ac-4e59-b45b-b2059d44d746] succeeded in 0.0026914000045508146s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:08:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[c7e6bb13-416e-4c9f-8847-85ef618561ea] received
[2026-03-30 05:08:17,732: INFO/MainProcess] Task tasks.scrape_pending_urls[c7e6bb13-416e-4c9f-8847-85ef618561ea] succeeded in 0.002513500046916306s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:08:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[bbc66c26-400a-4a8e-9a7b-55110cdbe3b9] received
[2026-03-30 05:08:48,021: INFO/MainProcess] Task tasks.collect_system_metrics[bbc66c26-400a-4a8e-9a7b-55110cdbe3b9] succeeded in 0.5161055999342352s: {'cpu': 11.5, 'memory': 46.1}
[2026-03-30 05:08:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[9f8600c4-ffd3-4524-a15a-891e3e7c6fe7] received
[2026-03-30 05:08:48,025: INFO/MainProcess] Task tasks.scrape_pending_urls[9f8600c4-ffd3-4524-a15a-891e3e7c6fe7] succeeded in 0.0022091999417170882s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:09:17,730: INFO/MainProcess] Task tasks.scrape_pending_urls[f9368602-eea1-421e-a0e4-6b29048fba76] received
[2026-03-30 05:09:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[f9368602-eea1-421e-a0e4-6b29048fba76] succeeded in 0.0028215000638738275s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:09:47,730: INFO/MainProcess] Task tasks.scrape_pending_urls[280391a3-ae01-4eaf-8e32-e7da167b1643] received
[2026-03-30 05:09:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[280391a3-ae01-4eaf-8e32-e7da167b1643] succeeded in 0.002728200051933527s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:10:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[882fe4d2-d8b4-4a5e-b7aa-a586a5df6a57] received
[2026-03-30 05:10:17,732: INFO/MainProcess] Task tasks.scrape_pending_urls[882fe4d2-d8b4-4a5e-b7aa-a586a5df6a57] succeeded in 0.0027123000472784042s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:10:47,730: INFO/MainProcess] Task tasks.scrape_pending_urls[1e00b5c9-21df-4751-8557-eecce4bfd676] received
[2026-03-30 05:10:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[1e00b5c9-21df-4751-8557-eecce4bfd676] succeeded in 0.002707500010728836s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:11:17,729: INFO/MainProcess] Task tasks.scrape_pending_urls[e84cf5da-342a-4948-b7e1-8fbc22911046] received
[2026-03-30 05:11:17,732: INFO/MainProcess] Task tasks.scrape_pending_urls[e84cf5da-342a-4948-b7e1-8fbc22911046] succeeded in 0.0028380999574437737s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:11:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[5f64af48-33ba-4806-a669-9de86df46939] received
[2026-03-30 05:11:47,736: INFO/MainProcess] Task tasks.scrape_pending_urls[5f64af48-33ba-4806-a669-9de86df46939] succeeded in 0.002701199962757528s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:12:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[71cc4b7a-3980-4b4c-852f-92a63e945782] received
[2026-03-30 05:12:17,736: INFO/MainProcess] Task tasks.scrape_pending_urls[71cc4b7a-3980-4b4c-852f-92a63e945782] succeeded in 0.0026302000042051077s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:12:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[25b4ffba-24da-4dd3-b11a-de895bd772d3] received
[2026-03-30 05:12:47,736: INFO/MainProcess] Task tasks.scrape_pending_urls[25b4ffba-24da-4dd3-b11a-de895bd772d3] succeeded in 0.0025644999695941806s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:13:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[a4c52b97-fff5-42aa-ab23-d03d320ca5b6] received
[2026-03-30 05:13:17,737: INFO/MainProcess] Task tasks.scrape_pending_urls[a4c52b97-fff5-42aa-ab23-d03d320ca5b6] succeeded in 0.002999400021508336s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:13:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[9a79ef20-5cb9-4770-9d44-bb635f9fb9b7] received
[2026-03-30 05:13:48,021: INFO/MainProcess] Task tasks.collect_system_metrics[9a79ef20-5cb9-4770-9d44-bb635f9fb9b7] succeeded in 0.5159820000408217s: {'cpu': 15.1, 'memory': 45.9}
[2026-03-30 05:13:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[eff3cb7d-1745-4b08-87e3-e639f4d8eb56] received
[2026-03-30 05:13:48,026: INFO/MainProcess] Task tasks.scrape_pending_urls[eff3cb7d-1745-4b08-87e3-e639f4d8eb56] succeeded in 0.002662000013515353s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:14:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[abc2ea34-5088-46af-af2c-9b11063aaa77] received
[2026-03-30 05:14:17,737: INFO/MainProcess] Task tasks.scrape_pending_urls[abc2ea34-5088-46af-af2c-9b11063aaa77] succeeded in 0.0031922999769449234s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:14:47,734: INFO/MainProcess] Task tasks.scrape_pending_urls[cf49f0d5-7e99-46dd-844c-2db3a9806cd5] received
[2026-03-30 05:14:47,737: INFO/MainProcess] Task tasks.scrape_pending_urls[cf49f0d5-7e99-46dd-844c-2db3a9806cd5] succeeded in 0.003301299992017448s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:15:17,734: INFO/MainProcess] Task tasks.scrape_pending_urls[bb9242b8-5802-4f5f-801e-f7d4d0d88b7c] received
[2026-03-30 05:15:17,737: INFO/MainProcess] Task tasks.scrape_pending_urls[bb9242b8-5802-4f5f-801e-f7d4d0d88b7c] succeeded in 0.0026498999213799834s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:15:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[5381c849-7fd0-4f9a-a299-58301a345ca0] received
[2026-03-30 05:15:47,736: INFO/MainProcess] Task tasks.scrape_pending_urls[5381c849-7fd0-4f9a-a299-58301a345ca0] succeeded in 0.0026333999121561646s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:16:17,733: INFO/MainProcess] Task tasks.scrape_pending_urls[9cb84f98-9f37-4bac-9c5d-785317ace9dc] received
[2026-03-30 05:16:17,736: INFO/MainProcess] Task tasks.scrape_pending_urls[9cb84f98-9f37-4bac-9c5d-785317ace9dc] succeeded in 0.0026625000173226s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:16:47,733: INFO/MainProcess] Task tasks.scrape_pending_urls[a845f818-7850-4220-b5c5-235b6b7e6f48] received
[2026-03-30 05:16:47,736: INFO/MainProcess] Task tasks.scrape_pending_urls[a845f818-7850-4220-b5c5-235b6b7e6f48] succeeded in 0.00256910000462085s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:17:17,734: INFO/MainProcess] Task tasks.scrape_pending_urls[4efa0538-a0cc-4aa0-81c1-9956d0bebeda] received
[2026-03-30 05:17:17,737: INFO/MainProcess] Task tasks.scrape_pending_urls[4efa0538-a0cc-4aa0-81c1-9956d0bebeda] succeeded in 0.002682300051674247s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:17:47,734: INFO/MainProcess] Task tasks.scrape_pending_urls[dd518c62-94c7-40ba-b3a2-2bd5cbd46249] received
[2026-03-30 05:17:47,737: INFO/MainProcess] Task tasks.scrape_pending_urls[dd518c62-94c7-40ba-b3a2-2bd5cbd46249] succeeded in 0.002598999999463558s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:18:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[3f68c6fc-9f5a-4802-bacc-892d9f963a94] received
[2026-03-30 05:18:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[3f68c6fc-9f5a-4802-bacc-892d9f963a94] succeeded in 0.002678500022739172s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:18:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[b9889b63-3958-4e8e-bde9-f6eddb3ad846] received
[2026-03-30 05:18:47,489: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 05:18:47,490: INFO/MainProcess] Task tasks.reset_stale_processing_urls[b9889b63-3958-4e8e-bde9-f6eddb3ad846] succeeded in 0.0032884000102058053s: {'reset': 0}
[2026-03-30 05:18:47,504: INFO/MainProcess] Task tasks.collect_system_metrics[8bbba781-12b4-478b-a135-ba5e3cdc34a5] received
[2026-03-30 05:18:48,020: INFO/MainProcess] Task tasks.collect_system_metrics[8bbba781-12b4-478b-a135-ba5e3cdc34a5] succeeded in 0.5157303999876603s: {'cpu': 15.4, 'memory': 46.0}
[2026-03-30 05:18:48,022: INFO/MainProcess] Task tasks.scrape_pending_urls[175e0dce-a1ad-4ebd-b851-3ec26ed2eda9] received
[2026-03-30 05:18:48,025: INFO/MainProcess] Task tasks.scrape_pending_urls[175e0dce-a1ad-4ebd-b851-3ec26ed2eda9] succeeded in 0.0022225999273359776s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:19:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[56798949-7801-45fb-9b6d-d51985d040c2] received
[2026-03-30 05:19:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[56798949-7801-45fb-9b6d-d51985d040c2] succeeded in 0.0026150000048801303s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:19:47,738: INFO/MainProcess] Task tasks.scrape_pending_urls[b78200e7-4347-45a0-a061-c8ac2f2bf742] received
[2026-03-30 05:19:47,741: INFO/MainProcess] Task tasks.scrape_pending_urls[b78200e7-4347-45a0-a061-c8ac2f2bf742] succeeded in 0.0025314000668004155s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:20:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[72bbb077-e40a-48a8-a7e7-822158168b9d] received
[2026-03-30 05:20:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[72bbb077-e40a-48a8-a7e7-822158168b9d] succeeded in 0.0027878000400960445s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:20:47,738: INFO/MainProcess] Task tasks.scrape_pending_urls[5f4a7491-5d84-40af-8c1e-95eda6c27c12] received
[2026-03-30 05:20:47,741: INFO/MainProcess] Task tasks.scrape_pending_urls[5f4a7491-5d84-40af-8c1e-95eda6c27c12] succeeded in 0.002797099994495511s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:21:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[5f3a38fd-3bd1-4ad3-af96-327ef0b120a7] received
[2026-03-30 05:21:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[5f3a38fd-3bd1-4ad3-af96-327ef0b120a7] succeeded in 0.0027626999653875828s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:21:47,738: INFO/MainProcess] Task tasks.scrape_pending_urls[787924f9-d15a-4e07-b7cb-060d7e616827] received
[2026-03-30 05:21:47,741: INFO/MainProcess] Task tasks.scrape_pending_urls[787924f9-d15a-4e07-b7cb-060d7e616827] succeeded in 0.0028216999489814043s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:22:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[85fcc149-97f0-42aa-b6da-ea1942b60484] received
[2026-03-30 05:22:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[85fcc149-97f0-42aa-b6da-ea1942b60484] succeeded in 0.0027636000886559486s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:22:47,738: INFO/MainProcess] Task tasks.scrape_pending_urls[39bbb85b-b8ef-4667-9173-0df6a0dadb02] received
[2026-03-30 05:22:47,741: INFO/MainProcess] Task tasks.scrape_pending_urls[39bbb85b-b8ef-4667-9173-0df6a0dadb02] succeeded in 0.0026975999353453517s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:23:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[a605e1ba-0997-4af3-9c94-f2d6803e653c] received
[2026-03-30 05:23:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[a605e1ba-0997-4af3-9c94-f2d6803e653c] succeeded in 0.0027714999159798026s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:23:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[4740b396-5aa2-4f22-9651-49ec059de5e5] received
[2026-03-30 05:23:48,022: INFO/MainProcess] Task tasks.collect_system_metrics[4740b396-5aa2-4f22-9651-49ec059de5e5] succeeded in 0.5160666999872774s: {'cpu': 11.6, 'memory': 45.9}
[2026-03-30 05:23:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[51e1b439-3b8a-46be-890a-f02e43e1f220] received
[2026-03-30 05:23:48,026: INFO/MainProcess] Task tasks.scrape_pending_urls[51e1b439-3b8a-46be-890a-f02e43e1f220] succeeded in 0.0026864000828936696s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:24:17,738: INFO/MainProcess] Task tasks.scrape_pending_urls[8923361f-25a4-485c-a3e2-4cd70ee03d6f] received
[2026-03-30 05:24:17,741: INFO/MainProcess] Task tasks.scrape_pending_urls[8923361f-25a4-485c-a3e2-4cd70ee03d6f] succeeded in 0.0025576999178156257s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:24:47,742: INFO/MainProcess] Task tasks.scrape_pending_urls[1e357592-4b96-4268-9a2d-b38bbb885695] received
[2026-03-30 05:24:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[1e357592-4b96-4268-9a2d-b38bbb885695] succeeded in 0.0032780999317765236s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:25:17,742: INFO/MainProcess] Task tasks.scrape_pending_urls[e5ca45bd-e591-411c-a807-167afb81c737] received
[2026-03-30 05:25:17,745: INFO/MainProcess] Task tasks.scrape_pending_urls[e5ca45bd-e591-411c-a807-167afb81c737] succeeded in 0.0026921998942270875s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:25:47,742: INFO/MainProcess] Task tasks.scrape_pending_urls[bfdc6f4a-9e50-4006-a72c-658ffccf43c4] received
[2026-03-30 05:25:47,745: INFO/MainProcess] Task tasks.scrape_pending_urls[bfdc6f4a-9e50-4006-a72c-658ffccf43c4] succeeded in 0.0026021000230684876s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:26:17,742: INFO/MainProcess] Task tasks.scrape_pending_urls[f65954e2-ad36-4c58-9c6f-30c72956f4ef] received
[2026-03-30 05:26:17,745: INFO/MainProcess] Task tasks.scrape_pending_urls[f65954e2-ad36-4c58-9c6f-30c72956f4ef] succeeded in 0.0025044999783858657s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:26:47,743: INFO/MainProcess] Task tasks.scrape_pending_urls[5dc87f6e-33a0-4302-8fcb-002a19d4b476] received
[2026-03-30 05:26:47,747: INFO/MainProcess] Task tasks.scrape_pending_urls[5dc87f6e-33a0-4302-8fcb-002a19d4b476] succeeded in 0.0033416999503970146s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:27:17,742: INFO/MainProcess] Task tasks.scrape_pending_urls[6abd9c0a-2bd0-4572-9cec-53851ec3c274] received
[2026-03-30 05:27:17,745: INFO/MainProcess] Task tasks.scrape_pending_urls[6abd9c0a-2bd0-4572-9cec-53851ec3c274] succeeded in 0.002940500038675964s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:27:47,742: INFO/MainProcess] Task tasks.scrape_pending_urls[1ecec744-58e0-43d6-a59a-c3ce57f294d1] received
[2026-03-30 05:27:47,745: INFO/MainProcess] Task tasks.scrape_pending_urls[1ecec744-58e0-43d6-a59a-c3ce57f294d1] succeeded in 0.002733199973590672s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:28:17,742: INFO/MainProcess] Task tasks.scrape_pending_urls[5a66f259-7d02-438c-bf9a-ce73771a8ba7] received
[2026-03-30 05:28:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[5a66f259-7d02-438c-bf9a-ce73771a8ba7] succeeded in 0.06337629992049187s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:28:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[d8178464-2cfb-4a3c-9037-f0fab2e6d03c] received
[2026-03-30 05:28:48,021: INFO/MainProcess] Task tasks.collect_system_metrics[d8178464-2cfb-4a3c-9037-f0fab2e6d03c] succeeded in 0.5159556999569759s: {'cpu': 17.4, 'memory': 45.9}
[2026-03-30 05:28:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[9d644b17-3d2a-49e8-aa87-834b4dce03d0] received
[2026-03-30 05:28:48,026: INFO/MainProcess] Task tasks.scrape_pending_urls[9d644b17-3d2a-49e8-aa87-834b4dce03d0] succeeded in 0.002633600030094385s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:29:17,742: INFO/MainProcess] Task tasks.scrape_pending_urls[c39944a5-1d48-4223-8736-25a09685a923] received
[2026-03-30 05:29:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[c39944a5-1d48-4223-8736-25a09685a923] succeeded in 0.0029445000691339374s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:29:47,743: INFO/MainProcess] Task tasks.scrape_pending_urls[4299ea5b-6327-40a4-878a-3bbfb7820a49] received
[2026-03-30 05:29:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[4299ea5b-6327-40a4-878a-3bbfb7820a49] succeeded in 0.0026798000326380134s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[c3bd2e9f-ad19-478f-bc18-ec34f5ff4604] received
[2026-03-30 05:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[c3bd2e9f-ad19-478f-bc18-ec34f5ff4604] succeeded in 0.001679199980571866s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 05:30:17,742: INFO/MainProcess] Task tasks.scrape_pending_urls[78f0f261-0b79-4139-bfd6-3174d5baa182] received
[2026-03-30 05:30:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[78f0f261-0b79-4139-bfd6-3174d5baa182] succeeded in 0.0034501999616622925s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:30:47,742: INFO/MainProcess] Task tasks.scrape_pending_urls[912ae7e6-01b4-4d37-be1d-a0a2cb1465d6] received
[2026-03-30 05:30:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[912ae7e6-01b4-4d37-be1d-a0a2cb1465d6] succeeded in 0.0029691000236198306s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:31:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[e0a11c3b-9759-4ad8-8ea3-908a629f7e6f] received
[2026-03-30 05:31:17,749: INFO/MainProcess] Task tasks.scrape_pending_urls[e0a11c3b-9759-4ad8-8ea3-908a629f7e6f] succeeded in 0.0026796000311151147s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:31:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[6565dfbe-44a4-4571-8ff0-d4395614f711] received
[2026-03-30 05:31:47,750: INFO/MainProcess] Task tasks.scrape_pending_urls[6565dfbe-44a4-4571-8ff0-d4395614f711] succeeded in 0.0031530000269412994s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:32:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[97132015-e39c-4773-ac4f-2a8e701562f5] received
[2026-03-30 05:32:17,749: INFO/MainProcess] Task tasks.scrape_pending_urls[97132015-e39c-4773-ac4f-2a8e701562f5] succeeded in 0.002969500026665628s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:32:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[68d4ea1f-b38e-43ee-b260-f00e843b5eed] received
[2026-03-30 05:32:47,749: INFO/MainProcess] Task tasks.scrape_pending_urls[68d4ea1f-b38e-43ee-b260-f00e843b5eed] succeeded in 0.0025716000236570835s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:33:17,747: INFO/MainProcess] Task tasks.scrape_pending_urls[7daa5f0e-cf36-4d2b-81bf-934e34008814] received
[2026-03-30 05:33:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[7daa5f0e-cf36-4d2b-81bf-934e34008814] succeeded in 0.06572269997559488s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:33:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[a9369230-b8a1-4583-b4a7-b607f41023c9] received
[2026-03-30 05:33:48,023: INFO/MainProcess] Task tasks.collect_system_metrics[a9369230-b8a1-4583-b4a7-b607f41023c9] succeeded in 0.5181900000898167s: {'cpu': 11.6, 'memory': 46.0}
[2026-03-30 05:33:48,025: INFO/MainProcess] Task tasks.scrape_pending_urls[557e4a20-0eb6-4a51-a402-e21bbf2fc7d3] received
[2026-03-30 05:33:48,028: INFO/MainProcess] Task tasks.scrape_pending_urls[557e4a20-0eb6-4a51-a402-e21bbf2fc7d3] succeeded in 0.0022484000073745847s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:34:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[a68ac064-1b32-419b-bac3-654792f6456b] received
[2026-03-30 05:34:17,750: INFO/MainProcess] Task tasks.scrape_pending_urls[a68ac064-1b32-419b-bac3-654792f6456b] succeeded in 0.0031973000150173903s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:34:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[39e2ddc1-fbfc-4e04-8184-fafe5ac2c014] received
[2026-03-30 05:34:47,749: INFO/MainProcess] Task tasks.scrape_pending_urls[39e2ddc1-fbfc-4e04-8184-fafe5ac2c014] succeeded in 0.0029134999494999647s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:35:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[1c5c9bad-69c3-453e-8ac7-197ee00c2df8] received
[2026-03-30 05:35:17,750: INFO/MainProcess] Task tasks.scrape_pending_urls[1c5c9bad-69c3-453e-8ac7-197ee00c2df8] succeeded in 0.0030639999313279986s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:35:47,747: INFO/MainProcess] Task tasks.scrape_pending_urls[e0db5a0e-488a-4320-a266-7fde735ecde9] received
[2026-03-30 05:35:47,750: INFO/MainProcess] Task tasks.scrape_pending_urls[e0db5a0e-488a-4320-a266-7fde735ecde9] succeeded in 0.003006399958394468s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:36:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[7a7a6847-cade-490c-af20-dfa6a2b18bef] received
[2026-03-30 05:36:17,750: INFO/MainProcess] Task tasks.scrape_pending_urls[7a7a6847-cade-490c-af20-dfa6a2b18bef] succeeded in 0.0028662000549957156s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:36:47,746: INFO/MainProcess] Task tasks.scrape_pending_urls[7e9141dc-7b0e-439d-85d1-0bf0d3ec1d74] received
[2026-03-30 05:36:47,749: INFO/MainProcess] Task tasks.scrape_pending_urls[7e9141dc-7b0e-439d-85d1-0bf0d3ec1d74] succeeded in 0.0025312999496236444s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:37:17,746: INFO/MainProcess] Task tasks.scrape_pending_urls[6ab633dd-d309-46ba-9452-6f86811ee280] received
[2026-03-30 05:37:17,749: INFO/MainProcess] Task tasks.scrape_pending_urls[6ab633dd-d309-46ba-9452-6f86811ee280] succeeded in 0.002843800000846386s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:37:47,751: INFO/MainProcess] Task tasks.scrape_pending_urls[ddb2828c-9359-4250-b162-fd5c6ec6765a] received
[2026-03-30 05:37:47,754: INFO/MainProcess] Task tasks.scrape_pending_urls[ddb2828c-9359-4250-b162-fd5c6ec6765a] succeeded in 0.002624599961563945s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:38:17,751: INFO/MainProcess] Task tasks.scrape_pending_urls[ee0e5cd9-6bb4-4b4f-8b1d-a244fc2134da] received
[2026-03-30 05:38:17,754: INFO/MainProcess] Task tasks.scrape_pending_urls[ee0e5cd9-6bb4-4b4f-8b1d-a244fc2134da] succeeded in 0.0027677000034600496s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:38:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[a27f8993-34a9-4c60-99c0-8089fd7b4a4b] received
[2026-03-30 05:38:48,023: INFO/MainProcess] Task tasks.collect_system_metrics[a27f8993-34a9-4c60-99c0-8089fd7b4a4b] succeeded in 0.5182022999506444s: {'cpu': 16.0, 'memory': 46.0}
[2026-03-30 05:38:48,025: INFO/MainProcess] Task tasks.scrape_pending_urls[23692d24-e0d3-4236-b6de-c0a995d03c1b] received
[2026-03-30 05:38:48,028: INFO/MainProcess] Task tasks.scrape_pending_urls[23692d24-e0d3-4236-b6de-c0a995d03c1b] succeeded in 0.002721099997870624s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:39:17,751: INFO/MainProcess] Task tasks.scrape_pending_urls[69e2575c-3d0e-4f8b-8973-8998ba7ce9c0] received
[2026-03-30 05:39:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[69e2575c-3d0e-4f8b-8973-8998ba7ce9c0] succeeded in 0.06568480003625154s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:39:47,751: INFO/MainProcess] Task tasks.scrape_pending_urls[95ea9221-38f4-401f-a56b-1744c3a8309a] received
[2026-03-30 05:39:47,754: INFO/MainProcess] Task tasks.scrape_pending_urls[95ea9221-38f4-401f-a56b-1744c3a8309a] succeeded in 0.0027622999623417854s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:40:17,751: INFO/MainProcess] Task tasks.scrape_pending_urls[02a712a2-9cca-4992-a41d-7067ad106757] received
[2026-03-30 05:40:17,754: INFO/MainProcess] Task tasks.scrape_pending_urls[02a712a2-9cca-4992-a41d-7067ad106757] succeeded in 0.002623200067318976s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:40:47,751: INFO/MainProcess] Task tasks.scrape_pending_urls[0212dece-7b4d-44f6-bc51-4d03359dd049] received
[2026-03-30 05:40:47,755: INFO/MainProcess] Task tasks.scrape_pending_urls[0212dece-7b4d-44f6-bc51-4d03359dd049] succeeded in 0.003101099980995059s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:41:17,751: INFO/MainProcess] Task tasks.scrape_pending_urls[642ddd58-af7f-48c8-a5fe-7a601203cafc] received
[2026-03-30 05:41:17,754: INFO/MainProcess] Task tasks.scrape_pending_urls[642ddd58-af7f-48c8-a5fe-7a601203cafc] succeeded in 0.0027166000800207257s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:41:47,751: INFO/MainProcess] Task tasks.scrape_pending_urls[4e66d719-3955-4869-ad15-6a3824664b05] received
[2026-03-30 05:41:47,754: INFO/MainProcess] Task tasks.scrape_pending_urls[4e66d719-3955-4869-ad15-6a3824664b05] succeeded in 0.0027760000666603446s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:42:17,752: INFO/MainProcess] Task tasks.scrape_pending_urls[7e24e6bd-1ed7-42c0-9013-7c5f627269dc] received
[2026-03-30 05:42:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[7e24e6bd-1ed7-42c0-9013-7c5f627269dc] succeeded in 0.0028774000238627195s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:42:47,752: INFO/MainProcess] Task tasks.scrape_pending_urls[8a117d30-b67d-4722-ba9e-2c429331fe47] received
[2026-03-30 05:42:47,755: INFO/MainProcess] Task tasks.scrape_pending_urls[8a117d30-b67d-4722-ba9e-2c429331fe47] succeeded in 0.0028406999772414565s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:43:17,752: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b00a28-88cc-41d7-a8cf-7a99182eb53e] received
[2026-03-30 05:43:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[a7b00a28-88cc-41d7-a8cf-7a99182eb53e] succeeded in 0.002581499982625246s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:43:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[29cfc9b2-e701-4740-80de-3973b7e92c40] received
[2026-03-30 05:43:48,024: INFO/MainProcess] Task tasks.collect_system_metrics[29cfc9b2-e701-4740-80de-3973b7e92c40] succeeded in 0.5187340999254957s: {'cpu': 11.2, 'memory': 45.9}
[2026-03-30 05:43:48,026: INFO/MainProcess] Task tasks.scrape_pending_urls[74c3f56e-62a6-428f-beb6-2ebe3a921334] received
[2026-03-30 05:43:48,029: INFO/MainProcess] Task tasks.scrape_pending_urls[74c3f56e-62a6-428f-beb6-2ebe3a921334] succeeded in 0.0027649999829009175s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:44:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[fd3b0fc1-9fd0-43b4-b2b6-3198e96b9a75] received
[2026-03-30 05:44:17,758: INFO/MainProcess] Task tasks.scrape_pending_urls[fd3b0fc1-9fd0-43b4-b2b6-3198e96b9a75] succeeded in 0.002691500005312264s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:44:47,756: INFO/MainProcess] Task tasks.scrape_pending_urls[54450a89-bd8a-432c-8fa5-7264aa3eea72] received
[2026-03-30 05:44:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[54450a89-bd8a-432c-8fa5-7264aa3eea72] succeeded in 0.0030651999404653907s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:45:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[6e998f7a-46d1-4dc3-ad2b-ef99ea133730] received
[2026-03-30 05:45:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[6e998f7a-46d1-4dc3-ad2b-ef99ea133730] succeeded in 0.0030363999539986253s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:45:47,755: INFO/MainProcess] Task tasks.scrape_pending_urls[3d7fa6c5-e1c3-4ea7-b80e-05c2325573fc] received
[2026-03-30 05:45:47,758: INFO/MainProcess] Task tasks.scrape_pending_urls[3d7fa6c5-e1c3-4ea7-b80e-05c2325573fc] succeeded in 0.002924900036305189s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:46:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[40bf3709-1049-4175-9ce5-7c3029f56ea3] received
[2026-03-30 05:46:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[40bf3709-1049-4175-9ce5-7c3029f56ea3] succeeded in 0.0027944999746978283s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:46:47,755: INFO/MainProcess] Task tasks.scrape_pending_urls[2dee6185-1d08-457e-a80b-eec70ac59cdf] received
[2026-03-30 05:46:47,758: INFO/MainProcess] Task tasks.scrape_pending_urls[2dee6185-1d08-457e-a80b-eec70ac59cdf] succeeded in 0.0026577000971883535s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:47:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[7383d1a4-deb5-47c1-8773-214fe58728a2] received
[2026-03-30 05:47:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[7383d1a4-deb5-47c1-8773-214fe58728a2] succeeded in 0.003145099966786802s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:47:47,755: INFO/MainProcess] Task tasks.scrape_pending_urls[02427853-ce8a-4120-9f77-9af2816ddc26] received
[2026-03-30 05:47:47,758: INFO/MainProcess] Task tasks.scrape_pending_urls[02427853-ce8a-4120-9f77-9af2816ddc26] succeeded in 0.0026970000471919775s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:48:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[0c9316e5-db33-47e8-b3e8-04fb2670cf42] received
[2026-03-30 05:48:17,758: INFO/MainProcess] Task tasks.scrape_pending_urls[0c9316e5-db33-47e8-b3e8-04fb2670cf42] succeeded in 0.002506399992853403s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:48:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[8547fb4f-4f95-43f1-b3f7-0d7c72389505] received
[2026-03-30 05:48:47,489: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 05:48:47,490: INFO/MainProcess] Task tasks.reset_stale_processing_urls[8547fb4f-4f95-43f1-b3f7-0d7c72389505] succeeded in 0.0032027000561356544s: {'reset': 0}
[2026-03-30 05:48:47,504: INFO/MainProcess] Task tasks.collect_system_metrics[7ca13faf-50d0-4dc9-a3be-6a723b7d7379] received
[2026-03-30 05:48:48,120: INFO/MainProcess] Task tasks.collect_system_metrics[7ca13faf-50d0-4dc9-a3be-6a723b7d7379] succeeded in 0.5170214000390843s: {'cpu': 17.7, 'memory': 45.8}
[2026-03-30 05:48:48,122: INFO/MainProcess] Task tasks.scrape_pending_urls[a24aa7dd-4e41-4230-aa33-2174e9264468] received
[2026-03-30 05:48:48,125: INFO/MainProcess] Task tasks.scrape_pending_urls[a24aa7dd-4e41-4230-aa33-2174e9264468] succeeded in 0.0027253000298514962s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:49:17,755: INFO/MainProcess] Task tasks.scrape_pending_urls[1ed0d18c-a3ca-430f-872b-47a50a016a47] received
[2026-03-30 05:49:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[1ed0d18c-a3ca-430f-872b-47a50a016a47] succeeded in 0.002687299973331392s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:49:47,756: INFO/MainProcess] Task tasks.scrape_pending_urls[b089095e-8e8f-448b-914e-928ee0cc91c0] received
[2026-03-30 05:49:47,760: INFO/MainProcess] Task tasks.scrape_pending_urls[b089095e-8e8f-448b-914e-928ee0cc91c0] succeeded in 0.0031916999723762274s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:50:17,756: INFO/MainProcess] Task tasks.scrape_pending_urls[e03cd733-3c64-4aac-b21e-dd953155eba3] received
[2026-03-30 05:50:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[e03cd733-3c64-4aac-b21e-dd953155eba3] succeeded in 0.0027447999455034733s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:50:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[75e195f3-f1a1-4ba3-afc4-a8c79d7d2e74] received
[2026-03-30 05:50:47,763: INFO/MainProcess] Task tasks.scrape_pending_urls[75e195f3-f1a1-4ba3-afc4-a8c79d7d2e74] succeeded in 0.003574599977582693s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:51:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[56962985-a37c-4181-abac-8a503b17e1c0] received
[2026-03-30 05:51:17,762: INFO/MainProcess] Task tasks.scrape_pending_urls[56962985-a37c-4181-abac-8a503b17e1c0] succeeded in 0.0028247999725863338s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:51:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[c767aad1-d71e-4476-8075-2da735f016bb] received
[2026-03-30 05:51:47,763: INFO/MainProcess] Task tasks.scrape_pending_urls[c767aad1-d71e-4476-8075-2da735f016bb] succeeded in 0.0028472000267356634s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:52:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[691d1af5-bc9e-4b66-ab4c-ce1f9d6b4fe8] received
[2026-03-30 05:52:17,762: INFO/MainProcess] Task tasks.scrape_pending_urls[691d1af5-bc9e-4b66-ab4c-ce1f9d6b4fe8] succeeded in 0.002780900103971362s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:52:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[4d307997-ca51-434b-acc6-160aa2135714] received
[2026-03-30 05:52:47,763: INFO/MainProcess] Task tasks.scrape_pending_urls[4d307997-ca51-434b-acc6-160aa2135714] succeeded in 0.003038399969227612s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:53:17,760: INFO/MainProcess] Task tasks.scrape_pending_urls[67655138-674c-45ca-b4fe-d411f4729e05] received
[2026-03-30 05:53:17,762: INFO/MainProcess] Task tasks.scrape_pending_urls[67655138-674c-45ca-b4fe-d411f4729e05] succeeded in 0.0025236000074073672s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:53:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[56bd2abf-e6de-4fc1-b8da-a3a6f8adde1b] received
[2026-03-30 05:53:48,021: INFO/MainProcess] Task tasks.collect_system_metrics[56bd2abf-e6de-4fc1-b8da-a3a6f8adde1b] succeeded in 0.5160003999480978s: {'cpu': 17.1, 'memory': 46.1}
[2026-03-30 05:53:48,024: INFO/MainProcess] Task tasks.scrape_pending_urls[a47cf170-757a-4c15-9606-3712eeda1b87] received
[2026-03-30 05:53:48,026: INFO/MainProcess] Task tasks.scrape_pending_urls[a47cf170-757a-4c15-9606-3712eeda1b87] succeeded in 0.0022438999731093645s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:54:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[e44a34a4-6deb-466c-b28c-f0481f427083] received
[2026-03-30 05:54:17,762: INFO/MainProcess] Task tasks.scrape_pending_urls[e44a34a4-6deb-466c-b28c-f0481f427083] succeeded in 0.002538600005209446s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:54:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[be9e6939-cfe5-4ff9-9960-c1da64f995e9] received
[2026-03-30 05:54:47,763: INFO/MainProcess] Task tasks.scrape_pending_urls[be9e6939-cfe5-4ff9-9960-c1da64f995e9] succeeded in 0.0027687998954206705s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:55:17,759: INFO/MainProcess] Task tasks.scrape_pending_urls[c99634de-be92-4a7c-86c3-64bfd09024a4] received
[2026-03-30 05:55:17,762: INFO/MainProcess] Task tasks.scrape_pending_urls[c99634de-be92-4a7c-86c3-64bfd09024a4] succeeded in 0.002602399908937514s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:55:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[03ebb5a7-2a67-410c-8d7d-09b4a770d640] received
[2026-03-30 05:55:47,763: INFO/MainProcess] Task tasks.scrape_pending_urls[03ebb5a7-2a67-410c-8d7d-09b4a770d640] succeeded in 0.002840899978764355s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:56:17,760: INFO/MainProcess] Task tasks.scrape_pending_urls[f075ff54-e4ab-4fd5-8ee4-3d6453fbecfd] received
[2026-03-30 05:56:17,763: INFO/MainProcess] Task tasks.scrape_pending_urls[f075ff54-e4ab-4fd5-8ee4-3d6453fbecfd] succeeded in 0.0026780000189319253s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:56:47,759: INFO/MainProcess] Task tasks.scrape_pending_urls[a7125e09-bc4d-4f7a-b6b1-481b7397e7c6] received
[2026-03-30 05:56:47,762: INFO/MainProcess] Task tasks.scrape_pending_urls[a7125e09-bc4d-4f7a-b6b1-481b7397e7c6] succeeded in 0.002518199966289103s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:57:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[7596f488-2516-4067-a328-30b95dfd7edd] received
[2026-03-30 05:57:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[7596f488-2516-4067-a328-30b95dfd7edd] succeeded in 0.002900299965403974s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:57:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[35533941-80c1-42d3-bcc4-594a22267754] received
[2026-03-30 05:57:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[35533941-80c1-42d3-bcc4-594a22267754] succeeded in 0.00269810005556792s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:58:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[af26843e-4001-4b84-ad27-3f011702fe7c] received
[2026-03-30 05:58:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[af26843e-4001-4b84-ad27-3f011702fe7c] succeeded in 0.0031476999865844846s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:58:47,505: INFO/MainProcess] Task tasks.collect_system_metrics[4749019e-40c3-4228-ae6f-890ce9077a81] received
[2026-03-30 05:58:48,021: INFO/MainProcess] Task tasks.collect_system_metrics[4749019e-40c3-4228-ae6f-890ce9077a81] succeeded in 0.5158954999642447s: {'cpu': 14.7, 'memory': 45.9}
[2026-03-30 05:58:48,023: INFO/MainProcess] Task tasks.scrape_pending_urls[da3c2745-3e93-476b-aec5-d57b5043b174] received
[2026-03-30 05:58:48,026: INFO/MainProcess] Task tasks.scrape_pending_urls[da3c2745-3e93-476b-aec5-d57b5043b174] succeeded in 0.0032574000069871545s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:59:17,763: INFO/MainProcess] Task tasks.scrape_pending_urls[7827a920-a41b-47fa-bf3d-30fbfb44a02b] received
[2026-03-30 05:59:17,766: INFO/MainProcess] Task tasks.scrape_pending_urls[7827a920-a41b-47fa-bf3d-30fbfb44a02b] succeeded in 0.0026160000124946237s: {'status': 'idle', 'pending': 0}
[2026-03-30 05:59:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[5a0edd65-ab24-41ca-bbf1-49257ff913f5] received
[2026-03-30 05:59:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[5a0edd65-ab24-41ca-bbf1-49257ff913f5] succeeded in 0.002585100010037422s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:00:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[8a54ef85-511e-45ce-b00c-43c2939fcdc7] received
[2026-03-30 06:00:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[8a54ef85-511e-45ce-b00c-43c2939fcdc7] succeeded in 0.0032134000211954117s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:00:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[2e6852d2-094e-4725-bb6a-6064f190c9a7] received
[2026-03-30 06:00:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[2e6852d2-094e-4725-bb6a-6064f190c9a7] succeeded in 0.0025845998898148537s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:01:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[a5555c4a-776c-47f8-873d-9d8924e3206c] received
[2026-03-30 06:01:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[a5555c4a-776c-47f8-873d-9d8924e3206c] succeeded in 0.0027525000041350722s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:01:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[7cc23da4-91fb-45fb-88e4-f646303a48d8] received
[2026-03-30 06:01:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[7cc23da4-91fb-45fb-88e4-f646303a48d8] succeeded in 0.0027966999914497137s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:02:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[d6acb7a4-1809-4bdb-9670-2134a16f221b] received
[2026-03-30 06:02:17,766: INFO/MainProcess] Task tasks.scrape_pending_urls[d6acb7a4-1809-4bdb-9670-2134a16f221b] succeeded in 0.0025303999427706003s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:02:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[5af3c8fa-9c57-45de-ac8c-6925c224a75d] received
[2026-03-30 06:02:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[5af3c8fa-9c57-45de-ac8c-6925c224a75d] succeeded in 0.0029510000022128224s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:03:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[23e81723-2d23-4383-96c0-58a7f0f24e12] received
[2026-03-30 06:03:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[23e81723-2d23-4383-96c0-58a7f0f24e12] succeeded in 0.002506399992853403s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:03:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[2333e916-ae0f-435d-894e-f6a73a4984cf] received
[2026-03-30 06:03:48,025: INFO/MainProcess] Task tasks.collect_system_metrics[2333e916-ae0f-435d-894e-f6a73a4984cf] succeeded in 0.515929999994114s: {'cpu': 13.3, 'memory': 45.8}
[2026-03-30 06:03:48,027: INFO/MainProcess] Task tasks.scrape_pending_urls[88acddba-c501-4eb4-b593-bf66527df09c] received
[2026-03-30 06:03:48,030: INFO/MainProcess] Task tasks.scrape_pending_urls[88acddba-c501-4eb4-b593-bf66527df09c] succeeded in 0.0022058000322431326s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:04:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[7e36e722-8d07-4d56-b847-34a1c2a03e57] received
[2026-03-30 06:04:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[7e36e722-8d07-4d56-b847-34a1c2a03e57] succeeded in 0.002537200110964477s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:04:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[fc153703-8303-46ba-96ec-51af004d9cb5] received
[2026-03-30 06:04:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[fc153703-8303-46ba-96ec-51af004d9cb5] succeeded in 0.0025288999313488603s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:05:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[9914a1bf-d6e5-41a0-b732-214486c23795] received
[2026-03-30 06:05:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[9914a1bf-d6e5-41a0-b732-214486c23795] succeeded in 0.00296920002438128s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:05:47,764: INFO/MainProcess] Task tasks.scrape_pending_urls[b7c658d1-d076-4542-b577-d6f03b0bea50] received
[2026-03-30 06:05:47,767: INFO/MainProcess] Task tasks.scrape_pending_urls[b7c658d1-d076-4542-b577-d6f03b0bea50] succeeded in 0.0030469000339508057s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:06:17,764: INFO/MainProcess] Task tasks.scrape_pending_urls[86a4acc9-03a5-4b33-99f5-f4e264d39366] received
[2026-03-30 06:06:17,767: INFO/MainProcess] Task tasks.scrape_pending_urls[86a4acc9-03a5-4b33-99f5-f4e264d39366] succeeded in 0.0026062000542879105s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:06:47,768: INFO/MainProcess] Task tasks.scrape_pending_urls[0606492e-3b52-4f71-9918-f629ba818d1a] received
[2026-03-30 06:06:47,771: INFO/MainProcess] Task tasks.scrape_pending_urls[0606492e-3b52-4f71-9918-f629ba818d1a] succeeded in 0.002704800106585026s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:07:17,768: INFO/MainProcess] Task tasks.scrape_pending_urls[3f0e8b7f-dbb3-416c-8745-084c0386a59f] received
[2026-03-30 06:07:17,771: INFO/MainProcess] Task tasks.scrape_pending_urls[3f0e8b7f-dbb3-416c-8745-084c0386a59f] succeeded in 0.002770500024780631s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:07:47,768: INFO/MainProcess] Task tasks.scrape_pending_urls[8dbbc6de-5cc5-4a16-8230-83ed31e59dae] received
[2026-03-30 06:07:47,771: INFO/MainProcess] Task tasks.scrape_pending_urls[8dbbc6de-5cc5-4a16-8230-83ed31e59dae] succeeded in 0.0025596999330446124s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:08:17,768: INFO/MainProcess] Task tasks.scrape_pending_urls[7bf7774f-fcff-4fb6-8dc8-68fc79bc8517] received
[2026-03-30 06:08:17,771: INFO/MainProcess] Task tasks.scrape_pending_urls[7bf7774f-fcff-4fb6-8dc8-68fc79bc8517] succeeded in 0.0028855999698862433s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:08:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[18ebe8f9-f4d8-4800-b92f-d3532fabc1fe] received
[2026-03-30 06:08:48,026: INFO/MainProcess] Task tasks.collect_system_metrics[18ebe8f9-f4d8-4800-b92f-d3532fabc1fe] succeeded in 0.5165404999861494s: {'cpu': 15.9, 'memory': 46.0}
[2026-03-30 06:08:48,028: INFO/MainProcess] Task tasks.scrape_pending_urls[689e88db-1680-4b66-8d6f-a78d79964a79] received
[2026-03-30 06:08:48,031: INFO/MainProcess] Task tasks.scrape_pending_urls[689e88db-1680-4b66-8d6f-a78d79964a79] succeeded in 0.0026367000536993146s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:09:17,768: INFO/MainProcess] Task tasks.scrape_pending_urls[17551cfd-40e8-4462-bece-1b0e806210df] received
[2026-03-30 06:09:17,771: INFO/MainProcess] Task tasks.scrape_pending_urls[17551cfd-40e8-4462-bece-1b0e806210df] succeeded in 0.002690299996174872s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:09:47,768: INFO/MainProcess] Task tasks.scrape_pending_urls[0b7519ab-1f9b-4a84-aa76-18090872e580] received
[2026-03-30 06:09:47,771: INFO/MainProcess] Task tasks.scrape_pending_urls[0b7519ab-1f9b-4a84-aa76-18090872e580] succeeded in 0.0028185000410303473s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:10:17,768: INFO/MainProcess] Task tasks.scrape_pending_urls[3f398b81-36ee-49ae-a9b0-575d692ac71e] received
[2026-03-30 06:10:17,771: INFO/MainProcess] Task tasks.scrape_pending_urls[3f398b81-36ee-49ae-a9b0-575d692ac71e] succeeded in 0.00268759997561574s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:10:47,768: INFO/MainProcess] Task tasks.scrape_pending_urls[defb2458-9035-4f4f-9eae-a45fc00d32a0] received
[2026-03-30 06:10:47,771: INFO/MainProcess] Task tasks.scrape_pending_urls[defb2458-9035-4f4f-9eae-a45fc00d32a0] succeeded in 0.0028986999532207847s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:11:17,768: INFO/MainProcess] Task tasks.scrape_pending_urls[81db7df7-a8ae-495e-9177-e5d9e790879d] received
[2026-03-30 06:11:17,772: INFO/MainProcess] Task tasks.scrape_pending_urls[81db7df7-a8ae-495e-9177-e5d9e790879d] succeeded in 0.0033236000454053283s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:11:47,768: INFO/MainProcess] Task tasks.scrape_pending_urls[0d7aba59-756d-4a3b-997d-902ee9f91c17] received
[2026-03-30 06:11:47,771: INFO/MainProcess] Task tasks.scrape_pending_urls[0d7aba59-756d-4a3b-997d-902ee9f91c17] succeeded in 0.0028190999291837215s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:12:17,768: INFO/MainProcess] Task tasks.scrape_pending_urls[4d5d774a-b516-4b32-ae65-14b1ff62ff85] received
[2026-03-30 06:12:17,771: INFO/MainProcess] Task tasks.scrape_pending_urls[4d5d774a-b516-4b32-ae65-14b1ff62ff85] succeeded in 0.002668399945832789s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:12:47,768: INFO/MainProcess] Task tasks.scrape_pending_urls[df9180c4-aeac-4de1-b62e-e3c97200c97e] received
[2026-03-30 06:12:47,771: INFO/MainProcess] Task tasks.scrape_pending_urls[df9180c4-aeac-4de1-b62e-e3c97200c97e] succeeded in 0.002601000014692545s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:13:17,772: INFO/MainProcess] Task tasks.scrape_pending_urls[b746f0d5-9abb-4471-a0fd-dfd2d802f2b5] received
[2026-03-30 06:13:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[b746f0d5-9abb-4471-a0fd-dfd2d802f2b5] succeeded in 0.0028336000395938754s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:13:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[40e168ee-547d-4ae6-bb28-11e2c52211c0] received
[2026-03-30 06:13:48,026: INFO/MainProcess] Task tasks.collect_system_metrics[40e168ee-547d-4ae6-bb28-11e2c52211c0] succeeded in 0.5163586999988183s: {'cpu': 16.7, 'memory': 46.0}
[2026-03-30 06:13:48,028: INFO/MainProcess] Task tasks.scrape_pending_urls[6bf900cc-b105-43ad-be04-f9c094fd0493] received
[2026-03-30 06:13:48,031: INFO/MainProcess] Task tasks.scrape_pending_urls[6bf900cc-b105-43ad-be04-f9c094fd0493] succeeded in 0.0022421999601647258s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:14:17,772: INFO/MainProcess] Task tasks.scrape_pending_urls[63287726-922f-4106-ab9a-1f5f5130d070] received
[2026-03-30 06:14:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[63287726-922f-4106-ab9a-1f5f5130d070] succeeded in 0.0029442000668495893s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:14:47,772: INFO/MainProcess] Task tasks.scrape_pending_urls[fa587d47-d061-43cb-9628-4a4e52fcbae0] received
[2026-03-30 06:14:47,775: INFO/MainProcess] Task tasks.scrape_pending_urls[fa587d47-d061-43cb-9628-4a4e52fcbae0] succeeded in 0.002865700051188469s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:15:17,772: INFO/MainProcess] Task tasks.scrape_pending_urls[5bba649c-dc31-4b51-8937-39052d75c63c] received
[2026-03-30 06:15:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[5bba649c-dc31-4b51-8937-39052d75c63c] succeeded in 0.0027758999494835734s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:15:47,772: INFO/MainProcess] Task tasks.scrape_pending_urls[968b2144-069f-4aea-87b4-2b9ba48e1774] received
[2026-03-30 06:15:47,775: INFO/MainProcess] Task tasks.scrape_pending_urls[968b2144-069f-4aea-87b4-2b9ba48e1774] succeeded in 0.00264040008187294s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:16:17,772: INFO/MainProcess] Task tasks.scrape_pending_urls[cafcad93-fb44-4e6e-b29d-35b0fcbed97f] received
[2026-03-30 06:16:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[cafcad93-fb44-4e6e-b29d-35b0fcbed97f] succeeded in 0.0028222999535501003s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:16:47,772: INFO/MainProcess] Task tasks.scrape_pending_urls[3fec394c-2ab5-4a0e-8a15-ffc8c40c4d43] received
[2026-03-30 06:16:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[3fec394c-2ab5-4a0e-8a15-ffc8c40c4d43] succeeded in 0.0026944000273942947s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:17:17,773: INFO/MainProcess] Task tasks.scrape_pending_urls[ef2daa69-8530-4f42-a082-67dbb6e14b06] received
[2026-03-30 06:17:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[ef2daa69-8530-4f42-a082-67dbb6e14b06] succeeded in 0.002759500057436526s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:17:47,772: INFO/MainProcess] Task tasks.scrape_pending_urls[96fe0b0c-9b92-442c-9ad2-6d6450dede7e] received
[2026-03-30 06:17:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[96fe0b0c-9b92-442c-9ad2-6d6450dede7e] succeeded in 0.002807399956509471s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:18:17,772: INFO/MainProcess] Task tasks.scrape_pending_urls[eee9c76b-9791-49d7-b31f-3f02d90d78bc] received
[2026-03-30 06:18:17,775: INFO/MainProcess] Task tasks.scrape_pending_urls[eee9c76b-9791-49d7-b31f-3f02d90d78bc] succeeded in 0.002623500069603324s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:18:47,486: INFO/MainProcess] Task tasks.reset_stale_processing_urls[8a8cce00-710c-4a7a-9d93-7c10fa948001] received
[2026-03-30 06:18:47,489: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 06:18:47,490: INFO/MainProcess] Task tasks.reset_stale_processing_urls[8a8cce00-710c-4a7a-9d93-7c10fa948001] succeeded in 0.00352490006480366s: {'reset': 0}
[2026-03-30 06:18:47,508: INFO/MainProcess] Task tasks.collect_system_metrics[9ece9756-c595-4fcd-a3b9-85dbd9cba991] received
[2026-03-30 06:18:48,025: INFO/MainProcess] Task tasks.collect_system_metrics[9ece9756-c595-4fcd-a3b9-85dbd9cba991] succeeded in 0.5164146000752226s: {'cpu': 14.7, 'memory': 46.0}
[2026-03-30 06:18:48,027: INFO/MainProcess] Task tasks.scrape_pending_urls[371d650b-7897-4afe-bd18-8a9c1138ff1b] received
[2026-03-30 06:18:48,029: INFO/MainProcess] Task tasks.scrape_pending_urls[371d650b-7897-4afe-bd18-8a9c1138ff1b] succeeded in 0.002205900033004582s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:19:17,773: INFO/MainProcess] Task tasks.scrape_pending_urls[aff3bb3b-382e-419d-8e85-0d3e192f9bb8] received
[2026-03-30 06:19:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[aff3bb3b-382e-419d-8e85-0d3e192f9bb8] succeeded in 0.0029482999816536903s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:19:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[38fd4f53-8b98-4fb0-9c02-d96090cf26de] received
[2026-03-30 06:19:47,779: INFO/MainProcess] Task tasks.scrape_pending_urls[38fd4f53-8b98-4fb0-9c02-d96090cf26de] succeeded in 0.0027597000589594245s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:20:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[528a30b5-2363-4bef-be3f-c33384c36145] received
[2026-03-30 06:20:17,779: INFO/MainProcess] Task tasks.scrape_pending_urls[528a30b5-2363-4bef-be3f-c33384c36145] succeeded in 0.0028741999994963408s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:20:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[39944c11-2dc8-48b3-a441-400e07e94311] received
[2026-03-30 06:20:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[39944c11-2dc8-48b3-a441-400e07e94311] succeeded in 0.003086599987000227s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:21:17,777: INFO/MainProcess] Task tasks.scrape_pending_urls[740a5c4d-061a-4b4e-8f0b-d478417688e7] received
[2026-03-30 06:21:17,781: INFO/MainProcess] Task tasks.scrape_pending_urls[740a5c4d-061a-4b4e-8f0b-d478417688e7] succeeded in 0.004429300082847476s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:21:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[df4a25c1-e553-49c2-a03e-64a282de95b3] received
[2026-03-30 06:21:47,779: INFO/MainProcess] Task tasks.scrape_pending_urls[df4a25c1-e553-49c2-a03e-64a282de95b3] succeeded in 0.002662800019606948s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:22:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[85e1c696-88b0-4367-95b7-460f28a485f0] received
[2026-03-30 06:22:17,779: INFO/MainProcess] Task tasks.scrape_pending_urls[85e1c696-88b0-4367-95b7-460f28a485f0] succeeded in 0.0028581999940797687s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:22:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[d02a79b4-eafe-40ab-b9a6-11c64a5fd9f5] received
[2026-03-30 06:22:47,779: INFO/MainProcess] Task tasks.scrape_pending_urls[d02a79b4-eafe-40ab-b9a6-11c64a5fd9f5] succeeded in 0.0027018000837415457s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:23:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[1d33ce84-09f4-49c8-ad6f-cce57a496466] received
[2026-03-30 06:23:17,779: INFO/MainProcess] Task tasks.scrape_pending_urls[1d33ce84-09f4-49c8-ad6f-cce57a496466] succeeded in 0.0026941999094560742s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:23:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[58d52f2d-3639-4c01-ace6-013e66262db1] received
[2026-03-30 06:23:48,025: INFO/MainProcess] Task tasks.collect_system_metrics[58d52f2d-3639-4c01-ace6-013e66262db1] succeeded in 0.5156141000334173s: {'cpu': 13.2, 'memory': 46.0}
[2026-03-30 06:23:48,027: INFO/MainProcess] Task tasks.scrape_pending_urls[150b06d7-840d-428e-b080-b9827896b833] received
[2026-03-30 06:23:48,030: INFO/MainProcess] Task tasks.scrape_pending_urls[150b06d7-840d-428e-b080-b9827896b833] succeeded in 0.0027068000053986907s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:24:17,777: INFO/MainProcess] Task tasks.scrape_pending_urls[9b83449b-27aa-44fd-86b3-392970165e93] received
[2026-03-30 06:24:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[9b83449b-27aa-44fd-86b3-392970165e93] succeeded in 0.0033090999349951744s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:24:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[2ab2f807-a46b-4f8d-8d4c-70d5d58ac264] received
[2026-03-30 06:24:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[2ab2f807-a46b-4f8d-8d4c-70d5d58ac264] succeeded in 0.0030276000034064054s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:25:17,776: INFO/MainProcess] Task tasks.scrape_pending_urls[2eb8b835-0aa0-4ba0-b447-be08377fb75b] received
[2026-03-30 06:25:17,779: INFO/MainProcess] Task tasks.scrape_pending_urls[2eb8b835-0aa0-4ba0-b447-be08377fb75b] succeeded in 0.002700299955904484s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:25:47,776: INFO/MainProcess] Task tasks.scrape_pending_urls[216d0901-9d1a-4e21-b2c6-32015e0d071c] received
[2026-03-30 06:25:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[216d0901-9d1a-4e21-b2c6-32015e0d071c] succeeded in 0.003351600025780499s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:26:17,781: INFO/MainProcess] Task tasks.scrape_pending_urls[9764000c-447f-4ad7-87b6-8c8864be6ba0] received
[2026-03-30 06:26:17,784: INFO/MainProcess] Task tasks.scrape_pending_urls[9764000c-447f-4ad7-87b6-8c8864be6ba0] succeeded in 0.0026798000326380134s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:26:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[0a39c6f8-c595-4932-8597-bb68afc0bffd] received
[2026-03-30 06:26:47,784: INFO/MainProcess] Task tasks.scrape_pending_urls[0a39c6f8-c595-4932-8597-bb68afc0bffd] succeeded in 0.003339500050060451s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:27:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[8745682f-c3f9-4858-b6d9-f15aea1e6dcd] received
[2026-03-30 06:27:17,783: INFO/MainProcess] Task tasks.scrape_pending_urls[8745682f-c3f9-4858-b6d9-f15aea1e6dcd] succeeded in 0.0028803000459447503s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:27:47,781: INFO/MainProcess] Task tasks.scrape_pending_urls[a48fea1f-86dd-438f-9a2c-e7ba5d2dc83a] received
[2026-03-30 06:27:47,784: INFO/MainProcess] Task tasks.scrape_pending_urls[a48fea1f-86dd-438f-9a2c-e7ba5d2dc83a] succeeded in 0.0028354000532999635s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:28:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[9e5f98e8-9d8b-4103-a3ba-8521935d899c] received
[2026-03-30 06:28:17,784: INFO/MainProcess] Task tasks.scrape_pending_urls[9e5f98e8-9d8b-4103-a3ba-8521935d899c] succeeded in 0.003599800053052604s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:28:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[4851e11f-4411-4896-9ba4-96675f2cde15] received
[2026-03-30 06:28:48,116: INFO/MainProcess] Task tasks.collect_system_metrics[4851e11f-4411-4896-9ba4-96675f2cde15] succeeded in 0.6070863999193534s: {'cpu': 17.6, 'memory': 45.8}
[2026-03-30 06:28:48,118: INFO/MainProcess] Task tasks.scrape_pending_urls[83e684f8-8099-47f6-b755-9281aac3b1ab] received
[2026-03-30 06:28:48,121: INFO/MainProcess] Task tasks.scrape_pending_urls[83e684f8-8099-47f6-b755-9281aac3b1ab] succeeded in 0.0023548000026494265s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:29:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[6c5649fe-aaeb-48d0-b608-5c704bfbc688] received
[2026-03-30 06:29:17,784: INFO/MainProcess] Task tasks.scrape_pending_urls[6c5649fe-aaeb-48d0-b608-5c704bfbc688] succeeded in 0.002917799982242286s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:29:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[ca35f32e-acc0-4e6a-8170-16ae064ebd0a] received
[2026-03-30 06:29:47,783: INFO/MainProcess] Task tasks.scrape_pending_urls[ca35f32e-acc0-4e6a-8170-16ae064ebd0a] succeeded in 0.002667600056156516s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[ec784c19-3542-48f7-a8bc-280b3c6cba31] received
[2026-03-30 06:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[ec784c19-3542-48f7-a8bc-280b3c6cba31] succeeded in 0.0014040999813005328s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 06:30:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[742199e5-971d-401e-96b5-53ebed37e4ed] received
[2026-03-30 06:30:17,783: INFO/MainProcess] Task tasks.scrape_pending_urls[742199e5-971d-401e-96b5-53ebed37e4ed] succeeded in 0.0027251000283285975s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:30:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[f3fd400f-a113-42aa-a700-8731a02c3ad0] received
[2026-03-30 06:30:47,784: INFO/MainProcess] Task tasks.scrape_pending_urls[f3fd400f-a113-42aa-a700-8731a02c3ad0] succeeded in 0.0027985000051558018s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:31:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[44e10fde-ab47-43e6-a3e2-78ea0de830f6] received
[2026-03-30 06:31:17,783: INFO/MainProcess] Task tasks.scrape_pending_urls[44e10fde-ab47-43e6-a3e2-78ea0de830f6] succeeded in 0.0026980999391525984s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:31:47,780: INFO/MainProcess] Task tasks.scrape_pending_urls[e4c85c96-5a43-4a0f-90a9-b1d0b74cf4cf] received
[2026-03-30 06:31:47,785: INFO/MainProcess] Task tasks.scrape_pending_urls[e4c85c96-5a43-4a0f-90a9-b1d0b74cf4cf] succeeded in 0.0038717000279575586s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:32:17,780: INFO/MainProcess] Task tasks.scrape_pending_urls[bdaaa94d-a5f8-49e0-80fc-3f608ea5c1f7] received
[2026-03-30 06:32:17,783: INFO/MainProcess] Task tasks.scrape_pending_urls[bdaaa94d-a5f8-49e0-80fc-3f608ea5c1f7] succeeded in 0.0026710000820457935s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:32:47,785: INFO/MainProcess] Task tasks.scrape_pending_urls[1d41427b-a180-41ca-84ea-6f6ec72a6d84] received
[2026-03-30 06:32:47,788: INFO/MainProcess] Task tasks.scrape_pending_urls[1d41427b-a180-41ca-84ea-6f6ec72a6d84] succeeded in 0.002748899976722896s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:33:17,785: INFO/MainProcess] Task tasks.scrape_pending_urls[6bf997bf-672c-41d1-bdd4-ab91ab840e79] received
[2026-03-30 06:33:17,788: INFO/MainProcess] Task tasks.scrape_pending_urls[6bf997bf-672c-41d1-bdd4-ab91ab840e79] succeeded in 0.0026632000226527452s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:33:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[aa99c51b-db5d-4b9b-ba27-d5f8cd749215] received
[2026-03-30 06:33:48,081: INFO/MainProcess] Task tasks.collect_system_metrics[aa99c51b-db5d-4b9b-ba27-d5f8cd749215] succeeded in 0.571819799952209s: {'cpu': 12.0, 'memory': 46.1}
[2026-03-30 06:33:48,083: INFO/MainProcess] Task tasks.scrape_pending_urls[777e0c13-bf11-409c-8efb-2bb7ff962d67] received
[2026-03-30 06:33:48,086: INFO/MainProcess] Task tasks.scrape_pending_urls[777e0c13-bf11-409c-8efb-2bb7ff962d67] succeeded in 0.0026410999707877636s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:34:17,785: INFO/MainProcess] Task tasks.scrape_pending_urls[f80c9b66-8371-4b56-bb1d-1ab38be97eba] received
[2026-03-30 06:34:17,788: INFO/MainProcess] Task tasks.scrape_pending_urls[f80c9b66-8371-4b56-bb1d-1ab38be97eba] succeeded in 0.0029572000494226813s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:34:47,785: INFO/MainProcess] Task tasks.scrape_pending_urls[d16d28c1-213c-4df1-b30f-3fc94d3861fd] received
[2026-03-30 06:34:47,788: INFO/MainProcess] Task tasks.scrape_pending_urls[d16d28c1-213c-4df1-b30f-3fc94d3861fd] succeeded in 0.0027247000252828s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:35:17,785: INFO/MainProcess] Task tasks.scrape_pending_urls[3fd82584-99b8-4d3d-8e4b-899ff9e4f14b] received
[2026-03-30 06:35:17,789: INFO/MainProcess] Task tasks.scrape_pending_urls[3fd82584-99b8-4d3d-8e4b-899ff9e4f14b] succeeded in 0.0027029000921174884s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:35:47,785: INFO/MainProcess] Task tasks.scrape_pending_urls[699133f3-4a9d-44e3-a9e3-d6b015fef556] received
[2026-03-30 06:35:47,789: INFO/MainProcess] Task tasks.scrape_pending_urls[699133f3-4a9d-44e3-a9e3-d6b015fef556] succeeded in 0.002749499981291592s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:36:17,785: INFO/MainProcess] Task tasks.scrape_pending_urls[846c2c7e-23f1-44dc-93f3-c68fe6b4cd6b] received
[2026-03-30 06:36:17,788: INFO/MainProcess] Task tasks.scrape_pending_urls[846c2c7e-23f1-44dc-93f3-c68fe6b4cd6b] succeeded in 0.002929899957962334s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:36:47,785: INFO/MainProcess] Task tasks.scrape_pending_urls[2259bd49-81de-47d2-a286-3976df2d0465] received
[2026-03-30 06:36:47,788: INFO/MainProcess] Task tasks.scrape_pending_urls[2259bd49-81de-47d2-a286-3976df2d0465] succeeded in 0.002639199956320226s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:37:17,785: INFO/MainProcess] Task tasks.scrape_pending_urls[21743945-f638-46ee-aeb8-35e3f34699cf] received
[2026-03-30 06:37:17,789: INFO/MainProcess] Task tasks.scrape_pending_urls[21743945-f638-46ee-aeb8-35e3f34699cf] succeeded in 0.0032110000029206276s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:37:47,785: INFO/MainProcess] Task tasks.scrape_pending_urls[d72798f7-672c-482c-9547-5cf13432a340] received
[2026-03-30 06:37:47,788: INFO/MainProcess] Task tasks.scrape_pending_urls[d72798f7-672c-482c-9547-5cf13432a340] succeeded in 0.0028759000124409795s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:38:17,785: INFO/MainProcess] Task tasks.scrape_pending_urls[9bf228a0-36d5-4cec-885d-c276dfac9670] received
[2026-03-30 06:38:17,788: INFO/MainProcess] Task tasks.scrape_pending_urls[9bf228a0-36d5-4cec-885d-c276dfac9670] succeeded in 0.0028276999946683645s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:38:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[52c8dc07-308f-47d3-8dbb-3e4f511a796a] received
[2026-03-30 06:38:48,026: INFO/MainProcess] Task tasks.collect_system_metrics[52c8dc07-308f-47d3-8dbb-3e4f511a796a] succeeded in 0.5162762000691146s: {'cpu': 15.2, 'memory': 46.0}
[2026-03-30 06:38:48,028: INFO/MainProcess] Task tasks.scrape_pending_urls[2d47dac0-5ddc-46ce-976f-261ba869db20] received
[2026-03-30 06:38:48,032: INFO/MainProcess] Task tasks.scrape_pending_urls[2d47dac0-5ddc-46ce-976f-261ba869db20] succeeded in 0.003278199932537973s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:39:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[6b953f8b-ad89-4b3f-9116-dee89305305b] received
[2026-03-30 06:39:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[6b953f8b-ad89-4b3f-9116-dee89305305b] succeeded in 0.002823999966494739s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:39:47,790: INFO/MainProcess] Task tasks.scrape_pending_urls[d29eab2e-6207-4546-bbe4-0caa2ba24565] received
[2026-03-30 06:39:47,854: INFO/MainProcess] Task tasks.scrape_pending_urls[d29eab2e-6207-4546-bbe4-0caa2ba24565] succeeded in 0.06353949999902397s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:40:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[5da41ec2-6d6a-45f8-ad86-139542930cd9] received
[2026-03-30 06:40:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[5da41ec2-6d6a-45f8-ad86-139542930cd9] succeeded in 0.0028109000995755196s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:40:47,790: INFO/MainProcess] Task tasks.scrape_pending_urls[4521794e-6fbd-48d3-9fb4-e0bd7b1ca056] received
[2026-03-30 06:40:47,793: INFO/MainProcess] Task tasks.scrape_pending_urls[4521794e-6fbd-48d3-9fb4-e0bd7b1ca056] succeeded in 0.0027289000572636724s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:41:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[deb942c6-95e9-495a-bc2d-7dae2077ae62] received
[2026-03-30 06:41:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[deb942c6-95e9-495a-bc2d-7dae2077ae62] succeeded in 0.0027094000251963735s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:41:47,790: INFO/MainProcess] Task tasks.scrape_pending_urls[1ee976e7-f077-4d11-86ef-2f8facb71be1] received
[2026-03-30 06:41:47,793: INFO/MainProcess] Task tasks.scrape_pending_urls[1ee976e7-f077-4d11-86ef-2f8facb71be1] succeeded in 0.0027289999416098s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:42:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[805e9122-aae9-43fe-ac62-ea042f573013] received
[2026-03-30 06:42:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[805e9122-aae9-43fe-ac62-ea042f573013] succeeded in 0.0025606999406591058s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:42:47,790: INFO/MainProcess] Task tasks.scrape_pending_urls[12f800ff-36ae-4d73-b151-d03846706b58] received
[2026-03-30 06:42:47,793: INFO/MainProcess] Task tasks.scrape_pending_urls[12f800ff-36ae-4d73-b151-d03846706b58] succeeded in 0.0031593000749126077s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:43:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[d3c3bc91-c694-4078-961d-94ef8154b62c] received
[2026-03-30 06:43:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[d3c3bc91-c694-4078-961d-94ef8154b62c] succeeded in 0.0027938000857830048s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:43:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[bf251932-1815-4f40-9fe2-7c9779fedbdf] received
[2026-03-30 06:43:48,027: INFO/MainProcess] Task tasks.collect_system_metrics[bf251932-1815-4f40-9fe2-7c9779fedbdf] succeeded in 0.517204700037837s: {'cpu': 14.8, 'memory': 46.0}
[2026-03-30 06:43:48,029: INFO/MainProcess] Task tasks.scrape_pending_urls[22ffe584-bdd7-4ac6-a5c4-c2aa8faff8d6] received
[2026-03-30 06:43:48,031: INFO/MainProcess] Task tasks.scrape_pending_urls[22ffe584-bdd7-4ac6-a5c4-c2aa8faff8d6] succeeded in 0.0025101000210270286s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:44:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[3a10a3b9-0b07-4d04-869e-99748bd2ceeb] received
[2026-03-30 06:44:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[3a10a3b9-0b07-4d04-869e-99748bd2ceeb] succeeded in 0.002641000086441636s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:44:47,790: INFO/MainProcess] Task tasks.scrape_pending_urls[e4b94dcf-306f-4d22-bd57-89d81faa85b7] received
[2026-03-30 06:44:47,793: INFO/MainProcess] Task tasks.scrape_pending_urls[e4b94dcf-306f-4d22-bd57-89d81faa85b7] succeeded in 0.002688300097361207s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:45:17,790: INFO/MainProcess] Task tasks.scrape_pending_urls[6b9219d4-bd58-4913-8926-e05c3aa1f291] received
[2026-03-30 06:45:17,793: INFO/MainProcess] Task tasks.scrape_pending_urls[6b9219d4-bd58-4913-8926-e05c3aa1f291] succeeded in 0.0028087999671697617s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:45:47,794: INFO/MainProcess] Task tasks.scrape_pending_urls[d6f73b09-c867-4986-9b81-0695f8b2b164] received
[2026-03-30 06:45:47,797: INFO/MainProcess] Task tasks.scrape_pending_urls[d6f73b09-c867-4986-9b81-0695f8b2b164] succeeded in 0.002840599976480007s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:46:17,794: INFO/MainProcess] Task tasks.scrape_pending_urls[67d527b9-068d-4455-a879-83e5fd1499d1] received
[2026-03-30 06:46:17,797: INFO/MainProcess] Task tasks.scrape_pending_urls[67d527b9-068d-4455-a879-83e5fd1499d1] succeeded in 0.0028816000558435917s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:46:47,794: INFO/MainProcess] Task tasks.scrape_pending_urls[37a040a6-2f89-4a12-838f-870c46c72eae] received
[2026-03-30 06:46:47,797: INFO/MainProcess] Task tasks.scrape_pending_urls[37a040a6-2f89-4a12-838f-870c46c72eae] succeeded in 0.0027706000255420804s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:47:17,795: INFO/MainProcess] Task tasks.scrape_pending_urls[93d4f826-ed36-46f7-9cc2-f7a8f3f934a0] received
[2026-03-30 06:47:17,799: INFO/MainProcess] Task tasks.scrape_pending_urls[93d4f826-ed36-46f7-9cc2-f7a8f3f934a0] succeeded in 0.003365200012922287s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:47:47,794: INFO/MainProcess] Task tasks.scrape_pending_urls[53ecc95a-1396-4404-895a-1a9398d6afe5] received
[2026-03-30 06:47:47,797: INFO/MainProcess] Task tasks.scrape_pending_urls[53ecc95a-1396-4404-895a-1a9398d6afe5] succeeded in 0.0025138999335467815s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:48:17,794: INFO/MainProcess] Task tasks.scrape_pending_urls[5f1df855-9780-4931-bf35-29ba83c6636b] received
[2026-03-30 06:48:17,797: INFO/MainProcess] Task tasks.scrape_pending_urls[5f1df855-9780-4931-bf35-29ba83c6636b] succeeded in 0.0027868999168276787s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:48:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[3eb2da12-603f-4295-8a0a-dffe7e3ce52e] received
[2026-03-30 06:48:47,490: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 06:48:47,491: INFO/MainProcess] Task tasks.reset_stale_processing_urls[3eb2da12-603f-4295-8a0a-dffe7e3ce52e] succeeded in 0.003414600039832294s: {'reset': 0}
[2026-03-30 06:48:47,508: INFO/MainProcess] Task tasks.collect_system_metrics[3e135c7c-8895-4975-9a46-4f93f8bcf51d] received
[2026-03-30 06:48:48,025: INFO/MainProcess] Task tasks.collect_system_metrics[3e135c7c-8895-4975-9a46-4f93f8bcf51d] succeeded in 0.515889799920842s: {'cpu': 10.8, 'memory': 46.1}
[2026-03-30 06:48:48,027: INFO/MainProcess] Task tasks.scrape_pending_urls[f5d0e8eb-86be-4afb-8119-58901349ef12] received
[2026-03-30 06:48:48,031: INFO/MainProcess] Task tasks.scrape_pending_urls[f5d0e8eb-86be-4afb-8119-58901349ef12] succeeded in 0.003961600014008582s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:49:17,794: INFO/MainProcess] Task tasks.scrape_pending_urls[a51caae1-b164-41c3-a6cf-3bc0b942af95] received
[2026-03-30 06:49:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[a51caae1-b164-41c3-a6cf-3bc0b942af95] succeeded in 0.0031840000301599503s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:49:47,794: INFO/MainProcess] Task tasks.scrape_pending_urls[4802304d-7d5c-4d03-82b5-5e8ea86292af] received
[2026-03-30 06:49:47,797: INFO/MainProcess] Task tasks.scrape_pending_urls[4802304d-7d5c-4d03-82b5-5e8ea86292af] succeeded in 0.002732599969021976s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:50:17,794: INFO/MainProcess] Task tasks.scrape_pending_urls[a203c1c1-311b-4a6c-bd8c-94ddc6d01df6] received
[2026-03-30 06:50:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[a203c1c1-311b-4a6c-bd8c-94ddc6d01df6] succeeded in 0.0029879999347031116s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:50:47,794: INFO/MainProcess] Task tasks.scrape_pending_urls[8fbd62cd-6ad3-4ef2-9ecc-220e6d1f187e] received
[2026-03-30 06:50:47,797: INFO/MainProcess] Task tasks.scrape_pending_urls[8fbd62cd-6ad3-4ef2-9ecc-220e6d1f187e] succeeded in 0.0026848999550566077s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:51:17,794: INFO/MainProcess] Task tasks.scrape_pending_urls[cb0946e7-bc0c-44d9-938a-42dbf14548d3] received
[2026-03-30 06:51:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[cb0946e7-bc0c-44d9-938a-42dbf14548d3] succeeded in 0.002839699969626963s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:51:47,794: INFO/MainProcess] Task tasks.scrape_pending_urls[c07a9bee-f59d-4219-aa88-e58b8512bd9e] received
[2026-03-30 06:51:47,798: INFO/MainProcess] Task tasks.scrape_pending_urls[c07a9bee-f59d-4219-aa88-e58b8512bd9e] succeeded in 0.003872099914588034s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:52:17,799: INFO/MainProcess] Task tasks.scrape_pending_urls[dc054abc-454b-46da-9a6e-c75483908311] received
[2026-03-30 06:52:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[dc054abc-454b-46da-9a6e-c75483908311] succeeded in 0.002706300001591444s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:52:47,798: INFO/MainProcess] Task tasks.scrape_pending_urls[5fac937f-2f81-45ec-9438-abe8a1767353] received
[2026-03-30 06:52:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[5fac937f-2f81-45ec-9438-abe8a1767353] succeeded in 0.0031864000484347343s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:53:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[e5a44195-afc5-4ed8-b1a6-522eace941eb] received
[2026-03-30 06:53:17,801: INFO/MainProcess] Task tasks.scrape_pending_urls[e5a44195-afc5-4ed8-b1a6-522eace941eb] succeeded in 0.0027138000587001443s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:53:47,509: INFO/MainProcess] Task tasks.collect_system_metrics[c73651d6-c6d5-40f8-94bc-c68425df3006] received
[2026-03-30 06:53:48,035: INFO/MainProcess] Task tasks.collect_system_metrics[c73651d6-c6d5-40f8-94bc-c68425df3006] succeeded in 0.5253340000053868s: {'cpu': 10.4, 'memory': 46.1}
[2026-03-30 06:53:48,037: INFO/MainProcess] Task tasks.scrape_pending_urls[d50e4870-3967-4d78-a43f-54056364f18e] received
[2026-03-30 06:53:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[d50e4870-3967-4d78-a43f-54056364f18e] succeeded in 0.0026625000173226s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:54:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[efe931e8-6a43-4044-becf-148ae0fbec4a] received
[2026-03-30 06:54:17,801: INFO/MainProcess] Task tasks.scrape_pending_urls[efe931e8-6a43-4044-becf-148ae0fbec4a] succeeded in 0.0025089000118896365s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:54:47,798: INFO/MainProcess] Task tasks.scrape_pending_urls[0e23b261-3069-4bfe-a0ce-a6d7783f15ca] received
[2026-03-30 06:54:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[0e23b261-3069-4bfe-a0ce-a6d7783f15ca] succeeded in 0.0029269999358803034s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:55:17,799: INFO/MainProcess] Task tasks.scrape_pending_urls[3113eca1-46a5-47c5-af90-da4b41afb80c] received
[2026-03-30 06:55:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[3113eca1-46a5-47c5-af90-da4b41afb80c] succeeded in 0.0028606000123545527s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:55:47,798: INFO/MainProcess] Task tasks.scrape_pending_urls[d0ba0a1f-3828-4717-b437-968e09492da2] received
[2026-03-30 06:55:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[d0ba0a1f-3828-4717-b437-968e09492da2] succeeded in 0.002907400019466877s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:56:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[6c1b3556-a1a1-4fd6-aa56-f1b3527e3601] received
[2026-03-30 06:56:17,801: INFO/MainProcess] Task tasks.scrape_pending_urls[6c1b3556-a1a1-4fd6-aa56-f1b3527e3601] succeeded in 0.002543300040997565s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:56:47,798: INFO/MainProcess] Task tasks.scrape_pending_urls[b356e698-8aa6-4751-baf8-0f5b83228358] received
[2026-03-30 06:56:47,801: INFO/MainProcess] Task tasks.scrape_pending_urls[b356e698-8aa6-4751-baf8-0f5b83228358] succeeded in 0.0026368999388068914s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:57:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[223b08a2-5ebd-4d1a-9220-86070293668d] received
[2026-03-30 06:57:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[223b08a2-5ebd-4d1a-9220-86070293668d] succeeded in 0.003104100003838539s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:57:47,798: INFO/MainProcess] Task tasks.scrape_pending_urls[32c893ac-53a2-461f-b59e-4d0f11cf29ff] received
[2026-03-30 06:57:47,801: INFO/MainProcess] Task tasks.scrape_pending_urls[32c893ac-53a2-461f-b59e-4d0f11cf29ff] succeeded in 0.002639799960888922s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:58:17,799: INFO/MainProcess] Task tasks.scrape_pending_urls[dc387e2e-27e6-432f-8937-cbb439c0441a] received
[2026-03-30 06:58:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[dc387e2e-27e6-432f-8937-cbb439c0441a] succeeded in 0.0027172999689355493s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:58:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[04fed585-1734-4c79-92ac-cd3589673855] received
[2026-03-30 06:58:48,033: INFO/MainProcess] Task tasks.collect_system_metrics[04fed585-1734-4c79-92ac-cd3589673855] succeeded in 0.5187499000458047s: {'cpu': 13.7, 'memory': 46.1}
[2026-03-30 06:58:48,035: INFO/MainProcess] Task tasks.scrape_pending_urls[c209820c-fdb7-4442-953f-b069c9d15ec9] received
[2026-03-30 06:58:48,038: INFO/MainProcess] Task tasks.scrape_pending_urls[c209820c-fdb7-4442-953f-b069c9d15ec9] succeeded in 0.0024470000062137842s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:59:17,799: INFO/MainProcess] Task tasks.scrape_pending_urls[c9d28b69-595e-4b84-aed1-839319a69c75] received
[2026-03-30 06:59:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[c9d28b69-595e-4b84-aed1-839319a69c75] succeeded in 0.0025987999979406595s: {'status': 'idle', 'pending': 0}
[2026-03-30 06:59:47,799: INFO/MainProcess] Task tasks.scrape_pending_urls[eecb9b82-f1ab-4be3-a047-916f39439327] received
[2026-03-30 06:59:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[eecb9b82-f1ab-4be3-a047-916f39439327] succeeded in 0.002883500070311129s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:00:17,799: INFO/MainProcess] Task tasks.scrape_pending_urls[ffbcd9f9-3726-487e-829d-45096beda27e] received
[2026-03-30 07:00:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[ffbcd9f9-3726-487e-829d-45096beda27e] succeeded in 0.0028844999615103006s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:00:47,799: INFO/MainProcess] Task tasks.scrape_pending_urls[b3dbcba4-10e9-4ebc-8b3f-8d3ce9020aa3] received
[2026-03-30 07:00:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[b3dbcba4-10e9-4ebc-8b3f-8d3ce9020aa3] succeeded in 0.00269210000988096s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:01:17,798: INFO/MainProcess] Task tasks.scrape_pending_urls[3698e527-7679-4665-b406-c2bd32c0f665] received
[2026-03-30 07:01:17,801: INFO/MainProcess] Task tasks.scrape_pending_urls[3698e527-7679-4665-b406-c2bd32c0f665] succeeded in 0.0026676999405026436s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:01:47,803: INFO/MainProcess] Task tasks.scrape_pending_urls[8a61c976-aea0-4ebb-9bfd-6dc5ac90d9e7] received
[2026-03-30 07:01:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[8a61c976-aea0-4ebb-9bfd-6dc5ac90d9e7] succeeded in 0.0026805000379681587s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:02:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[214500f2-f8f7-4a5a-979f-1a9bc4c00948] received
[2026-03-30 07:02:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[214500f2-f8f7-4a5a-979f-1a9bc4c00948] succeeded in 0.0027938999701291323s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:02:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[7aa37a9b-b2a6-457c-8e35-2af654426908] received
[2026-03-30 07:02:47,805: INFO/MainProcess] Task tasks.scrape_pending_urls[7aa37a9b-b2a6-457c-8e35-2af654426908] succeeded in 0.0028810000512748957s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:03:17,802: INFO/MainProcess] Task tasks.scrape_pending_urls[844bf315-21bc-46b6-8589-8cf7e7bf612a] received
[2026-03-30 07:03:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[844bf315-21bc-46b6-8589-8cf7e7bf612a] succeeded in 0.002824300085194409s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:03:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[36870c03-d8e1-442a-905c-d278d21ad587] received
[2026-03-30 07:03:48,030: INFO/MainProcess] Task tasks.collect_system_metrics[36870c03-d8e1-442a-905c-d278d21ad587] succeeded in 0.5158555000089109s: {'cpu': 17.0, 'memory': 45.9}
[2026-03-30 07:03:48,032: INFO/MainProcess] Task tasks.scrape_pending_urls[53c7481e-d318-405b-b916-0674d708f01e] received
[2026-03-30 07:03:48,035: INFO/MainProcess] Task tasks.scrape_pending_urls[53c7481e-d318-405b-b916-0674d708f01e] succeeded in 0.002664199913851917s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:04:17,803: INFO/MainProcess] Task tasks.scrape_pending_urls[dd58f107-6243-4a4a-8698-1a884e15b91c] received
[2026-03-30 07:04:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[dd58f107-6243-4a4a-8698-1a884e15b91c] succeeded in 0.0027248000260442495s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:04:47,802: INFO/MainProcess] Task tasks.scrape_pending_urls[0e824991-e30d-45fb-aabc-6cdd74e5ada8] received
[2026-03-30 07:04:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[0e824991-e30d-45fb-aabc-6cdd74e5ada8] succeeded in 0.0031557000475004315s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:05:17,803: INFO/MainProcess] Task tasks.scrape_pending_urls[971f8dd8-2514-4b5f-87e4-373b8c396417] received
[2026-03-30 07:05:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[971f8dd8-2514-4b5f-87e4-373b8c396417] succeeded in 0.002877500024624169s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:05:47,803: INFO/MainProcess] Task tasks.scrape_pending_urls[718f57f8-13d6-4b70-9f56-f48b3413220d] received
[2026-03-30 07:05:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[718f57f8-13d6-4b70-9f56-f48b3413220d] succeeded in 0.003098399960435927s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:06:17,803: INFO/MainProcess] Task tasks.scrape_pending_urls[eb46c174-5a6c-4fea-ba2c-8da042ea0cc8] received
[2026-03-30 07:06:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[eb46c174-5a6c-4fea-ba2c-8da042ea0cc8] succeeded in 0.003149600001052022s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:06:47,803: INFO/MainProcess] Task tasks.scrape_pending_urls[b48b579f-fa13-43b3-aa52-b4c28c4c7aa3] received
[2026-03-30 07:06:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[b48b579f-fa13-43b3-aa52-b4c28c4c7aa3] succeeded in 0.0027498999843373895s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:07:17,803: INFO/MainProcess] Task tasks.scrape_pending_urls[0ede9815-a5ae-4971-8798-6d57aa149c26] received
[2026-03-30 07:07:17,807: INFO/MainProcess] Task tasks.scrape_pending_urls[0ede9815-a5ae-4971-8798-6d57aa149c26] succeeded in 0.003354900050908327s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:07:47,803: INFO/MainProcess] Task tasks.scrape_pending_urls[880c91ba-1e72-40e6-ba70-a53d27697b19] received
[2026-03-30 07:07:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[880c91ba-1e72-40e6-ba70-a53d27697b19] succeeded in 0.0029875999316573143s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:08:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[f5c46e70-c455-4a5d-9aa7-bba7c18d9ff4] received
[2026-03-30 07:08:17,809: INFO/MainProcess] Task tasks.scrape_pending_urls[f5c46e70-c455-4a5d-9aa7-bba7c18d9ff4] succeeded in 0.0026085999561473727s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:08:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[51b1e3a9-910e-423f-abe1-13bd9e67cb59] received
[2026-03-30 07:08:48,031: INFO/MainProcess] Task tasks.collect_system_metrics[51b1e3a9-910e-423f-abe1-13bd9e67cb59] succeeded in 0.5163948000408709s: {'cpu': 23.8, 'memory': 46.1}
[2026-03-30 07:08:48,033: INFO/MainProcess] Task tasks.scrape_pending_urls[b4b67b7e-3d9e-4904-88d7-a1da1334248a] received
[2026-03-30 07:08:48,036: INFO/MainProcess] Task tasks.scrape_pending_urls[b4b67b7e-3d9e-4904-88d7-a1da1334248a] succeeded in 0.0028805999318137765s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:09:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[28260b6a-434e-4d75-9cc9-b7b51b7fead9] received
[2026-03-30 07:09:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[28260b6a-434e-4d75-9cc9-b7b51b7fead9] succeeded in 0.003297699964605272s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:09:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[3cf61331-5828-4b81-ae1f-ebaa194e0b27] received
[2026-03-30 07:09:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[3cf61331-5828-4b81-ae1f-ebaa194e0b27] succeeded in 0.0027972999960184097s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:10:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[f629de53-dad5-44fe-bdca-b8fc36966665] received
[2026-03-30 07:10:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[f629de53-dad5-44fe-bdca-b8fc36966665] succeeded in 0.0033047000179067254s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:10:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[1433d6f7-ff92-49b2-87cf-4dc2343715e6] received
[2026-03-30 07:10:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[1433d6f7-ff92-49b2-87cf-4dc2343715e6] succeeded in 0.003172100055962801s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:11:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[56936501-1875-46df-80ee-c078b671e471] received
[2026-03-30 07:11:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[56936501-1875-46df-80ee-c078b671e471] succeeded in 0.0034271000185981393s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:11:47,807: INFO/MainProcess] Task tasks.scrape_pending_urls[d9a90632-cb81-410b-9e5c-6ff011f5ab61] received
[2026-03-30 07:11:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[d9a90632-cb81-410b-9e5c-6ff011f5ab61] succeeded in 0.002866199938580394s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:12:17,806: INFO/MainProcess] Task tasks.scrape_pending_urls[20666973-ed4e-4ede-a1c4-50e981579ca0] received
[2026-03-30 07:12:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[20666973-ed4e-4ede-a1c4-50e981579ca0] succeeded in 0.0033378000371158123s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:12:47,806: INFO/MainProcess] Task tasks.scrape_pending_urls[5e8a5cfe-8db7-4f79-9d89-9306f52b3b52] received
[2026-03-30 07:12:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[5e8a5cfe-8db7-4f79-9d89-9306f52b3b52] succeeded in 0.0031504000071436167s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:13:17,807: INFO/MainProcess] Task tasks.scrape_pending_urls[6f3c5688-7fec-41b7-b5a9-b24c03f61c9c] received
[2026-03-30 07:13:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[6f3c5688-7fec-41b7-b5a9-b24c03f61c9c] succeeded in 0.002823200076818466s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:13:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[98951975-b047-468c-8ef5-0106f35f5538] received
[2026-03-30 07:13:48,033: INFO/MainProcess] Task tasks.collect_system_metrics[98951975-b047-468c-8ef5-0106f35f5538] succeeded in 0.5187230999581516s: {'cpu': 30.4, 'memory': 46.1}
[2026-03-30 07:13:48,035: INFO/MainProcess] Task tasks.scrape_pending_urls[13c64899-e5d3-42a8-8148-b08995ddf55e] received
[2026-03-30 07:13:48,043: INFO/MainProcess] Task tasks.scrape_pending_urls[13c64899-e5d3-42a8-8148-b08995ddf55e] succeeded in 0.0066781999776139855s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:14:17,807: INFO/MainProcess] Task tasks.scrape_pending_urls[d50e882e-f903-4d76-b522-9f3a11a7561f] received
[2026-03-30 07:14:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[d50e882e-f903-4d76-b522-9f3a11a7561f] succeeded in 0.002876700018532574s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:14:47,809: INFO/MainProcess] Task tasks.scrape_pending_urls[44edc715-54d9-42e0-a00b-73d7cb6aef22] received
[2026-03-30 07:14:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[44edc715-54d9-42e0-a00b-73d7cb6aef22] succeeded in 0.0033499000128358603s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:15:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[bcd5409b-9b55-449d-ac47-b41c23b29d1a] received
[2026-03-30 07:15:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[bcd5409b-9b55-449d-ac47-b41c23b29d1a] succeeded in 0.003049400052987039s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:15:47,809: INFO/MainProcess] Task tasks.scrape_pending_urls[e189ca48-019a-4406-83c1-dde962be80d0] received
[2026-03-30 07:15:47,812: INFO/MainProcess] Task tasks.scrape_pending_urls[e189ca48-019a-4406-83c1-dde962be80d0] succeeded in 0.002799500012770295s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:16:17,809: INFO/MainProcess] Task tasks.scrape_pending_urls[e941a7fc-525e-4d45-a48a-2798ee6c517f] received
[2026-03-30 07:16:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[e941a7fc-525e-4d45-a48a-2798ee6c517f] succeeded in 0.0031030999962240458s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:16:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[b46fdf8a-f3c6-40c2-859a-4d0e526db0a5] received
[2026-03-30 07:16:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[b46fdf8a-f3c6-40c2-859a-4d0e526db0a5] succeeded in 0.0032209999626502395s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:17:17,809: INFO/MainProcess] Task tasks.scrape_pending_urls[771bcb67-ef22-4c84-84a2-f90cf3999614] received
[2026-03-30 07:17:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[771bcb67-ef22-4c84-84a2-f90cf3999614] succeeded in 0.0032689999788999557s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:17:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[e7965d91-041e-4920-b6b6-9800419ab980] received
[2026-03-30 07:17:47,815: INFO/MainProcess] Task tasks.scrape_pending_urls[e7965d91-041e-4920-b6b6-9800419ab980] succeeded in 0.00403289997484535s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:18:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[b0fa4743-7043-4e62-995b-886efd448fe8] received
[2026-03-30 07:18:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[b0fa4743-7043-4e62-995b-886efd448fe8] succeeded in 0.003006399958394468s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:18:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[bde35e0c-717f-483b-9565-78975f2f77e5] received
[2026-03-30 07:18:47,490: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 07:18:47,491: INFO/MainProcess] Task tasks.reset_stale_processing_urls[bde35e0c-717f-483b-9565-78975f2f77e5] succeeded in 0.0033762999810278416s: {'reset': 0}
[2026-03-30 07:18:47,602: INFO/MainProcess] Task tasks.collect_system_metrics[3a2bc8fd-84fb-4412-a696-568fc7864fc5] received
[2026-03-30 07:18:48,120: INFO/MainProcess] Task tasks.collect_system_metrics[3a2bc8fd-84fb-4412-a696-568fc7864fc5] succeeded in 0.5177963000023738s: {'cpu': 25.4, 'memory': 46.2}
[2026-03-30 07:18:48,122: INFO/MainProcess] Task tasks.scrape_pending_urls[7769ff52-5b25-47f3-9ce9-f6e3bf3676a1] received
[2026-03-30 07:18:48,126: INFO/MainProcess] Task tasks.scrape_pending_urls[7769ff52-5b25-47f3-9ce9-f6e3bf3676a1] succeeded in 0.0033054000232368708s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:19:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[49ecfe97-3350-486f-835d-8c9faba88d01] received
[2026-03-30 07:19:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[49ecfe97-3350-486f-835d-8c9faba88d01] succeeded in 0.0031096000457182527s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:19:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[5d2b4c1e-b8f3-4bb6-bc8c-c5387223aa6c] received
[2026-03-30 07:19:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[5d2b4c1e-b8f3-4bb6-bc8c-c5387223aa6c] succeeded in 0.0032349000684916973s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:20:17,810: INFO/MainProcess] Task tasks.scrape_pending_urls[19f4b6f4-f2b3-4dbc-bf46-45916b41274a] received
[2026-03-30 07:20:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[19f4b6f4-f2b3-4dbc-bf46-45916b41274a] succeeded in 0.002978899981826544s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:20:47,810: INFO/MainProcess] Task tasks.scrape_pending_urls[eb09bd2b-a500-438a-95cf-11181d2c10a5] received
[2026-03-30 07:20:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[eb09bd2b-a500-438a-95cf-11181d2c10a5] succeeded in 0.003083999967202544s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:21:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[b734ad28-c273-43e7-85ef-8ea990f92e00] received
[2026-03-30 07:21:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[b734ad28-c273-43e7-85ef-8ea990f92e00] succeeded in 0.0030535999685525894s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:21:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[7bed5103-db61-4f60-b33b-17151776a9d9] received
[2026-03-30 07:21:47,816: INFO/MainProcess] Task tasks.scrape_pending_urls[7bed5103-db61-4f60-b33b-17151776a9d9] succeeded in 0.003184500033967197s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:22:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[1c187d10-c067-4d23-be65-499f04243fdc] received
[2026-03-30 07:22:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[1c187d10-c067-4d23-be65-499f04243fdc] succeeded in 0.0032090001041069627s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:22:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[555523f6-b046-45cd-b431-776a4de87090] received
[2026-03-30 07:22:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[555523f6-b046-45cd-b431-776a4de87090] succeeded in 0.003304600017145276s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:23:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[99c25ace-1fd1-435c-9e7f-16f45b1eaa7e] received
[2026-03-30 07:23:17,816: INFO/MainProcess] Task tasks.scrape_pending_urls[99c25ace-1fd1-435c-9e7f-16f45b1eaa7e] succeeded in 0.002881099935621023s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:23:47,515: INFO/MainProcess] Task tasks.collect_system_metrics[923fd307-b6ab-4426-b795-9ed5af14679e] received
[2026-03-30 07:23:48,032: INFO/MainProcess] Task tasks.collect_system_metrics[923fd307-b6ab-4426-b795-9ed5af14679e] succeeded in 0.5171059999847785s: {'cpu': 30.1, 'memory': 46.3}
[2026-03-30 07:23:48,034: INFO/MainProcess] Task tasks.scrape_pending_urls[117553fa-2821-46d5-bf0f-b43a74fab2f2] received
[2026-03-30 07:23:48,037: INFO/MainProcess] Task tasks.scrape_pending_urls[117553fa-2821-46d5-bf0f-b43a74fab2f2] succeeded in 0.0029099000385031104s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:24:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[f6d32506-f3c4-4cf2-b687-aae686f2db2b] received
[2026-03-30 07:24:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[f6d32506-f3c4-4cf2-b687-aae686f2db2b] succeeded in 0.0033629999961704016s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:24:47,813: INFO/MainProcess] Task tasks.scrape_pending_urls[1d960b63-5030-49f6-ac80-258fc1bc3fe4] received
[2026-03-30 07:24:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[1d960b63-5030-49f6-ac80-258fc1bc3fe4] succeeded in 0.003333200002089143s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:25:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[cf2571de-bf4a-41a2-a480-0b458dfe5037] received
[2026-03-30 07:25:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[cf2571de-bf4a-41a2-a480-0b458dfe5037] succeeded in 0.0035032000159844756s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:25:47,814: INFO/MainProcess] Task tasks.scrape_pending_urls[1b20f76c-10a4-4ffd-bb4a-5c3235c3633c] received
[2026-03-30 07:25:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[1b20f76c-10a4-4ffd-bb4a-5c3235c3633c] succeeded in 0.003216400044038892s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:26:17,814: INFO/MainProcess] Task tasks.scrape_pending_urls[cb3fa74c-e73d-4013-be8a-b67263432271] received
[2026-03-30 07:26:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[cb3fa74c-e73d-4013-be8a-b67263432271] succeeded in 0.0029075000202283263s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:26:47,814: INFO/MainProcess] Task tasks.scrape_pending_urls[bf6da548-8e98-4532-ad00-d78a26e3fc89] received
[2026-03-30 07:26:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[bf6da548-8e98-4532-ad00-d78a26e3fc89] succeeded in 0.0028679000679403543s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:27:17,813: INFO/MainProcess] Task tasks.scrape_pending_urls[a60748a9-71b6-444a-946a-ff875ce76e43] received
[2026-03-30 07:27:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[a60748a9-71b6-444a-946a-ff875ce76e43] succeeded in 0.00359890004619956s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:27:47,816: INFO/MainProcess] Task tasks.scrape_pending_urls[36de55f4-a5b0-4431-8072-1a2c068d7ae5] received
[2026-03-30 07:27:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[36de55f4-a5b0-4431-8072-1a2c068d7ae5] succeeded in 0.002861800021491945s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:28:17,816: INFO/MainProcess] Task tasks.scrape_pending_urls[8e9cd59d-41e6-4192-bbbb-05722d4a5f67] received
[2026-03-30 07:28:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[8e9cd59d-41e6-4192-bbbb-05722d4a5f67] succeeded in 0.0032079999800771475s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:28:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[2882cb94-130a-4116-b5e9-ed9edb9f4de1] received
[2026-03-30 07:28:48,031: INFO/MainProcess] Task tasks.collect_system_metrics[2882cb94-130a-4116-b5e9-ed9edb9f4de1] succeeded in 0.5162025999743491s: {'cpu': 31.1, 'memory': 46.1}
[2026-03-30 07:28:48,033: INFO/MainProcess] Task tasks.scrape_pending_urls[f9f41d92-e64a-4c9f-a7a6-d83bd1ab70ce] received
[2026-03-30 07:28:48,110: INFO/MainProcess] Task tasks.scrape_pending_urls[f9f41d92-e64a-4c9f-a7a6-d83bd1ab70ce] succeeded in 0.07665039994753897s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:29:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[0557cd47-1d14-474c-943f-b94def3e24f4] received
[2026-03-30 07:29:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[0557cd47-1d14-474c-943f-b94def3e24f4] succeeded in 0.003225899999961257s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:29:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[93a5ab24-1c90-4e9e-8f81-73b191c41485] received
[2026-03-30 07:29:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[93a5ab24-1c90-4e9e-8f81-73b191c41485] succeeded in 0.002904399996623397s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[dcdb2e88-f70c-4ed8-99a1-fc06cbf01c89] received
[2026-03-30 07:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[dcdb2e88-f70c-4ed8-99a1-fc06cbf01c89] succeeded in 0.0014355999883264303s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 07:30:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[63950562-5c6a-4850-94c4-94943325f76c] received
[2026-03-30 07:30:17,821: INFO/MainProcess] Task tasks.scrape_pending_urls[63950562-5c6a-4850-94c4-94943325f76c] succeeded in 0.003750300034880638s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:30:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[c2fae1ba-83fc-484a-96e7-62626700dfa1] received
[2026-03-30 07:30:47,821: INFO/MainProcess] Task tasks.scrape_pending_urls[c2fae1ba-83fc-484a-96e7-62626700dfa1] succeeded in 0.003279500058852136s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:31:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[e0c18a03-902f-4f7c-a923-656f66971999] received
[2026-03-30 07:31:17,821: INFO/MainProcess] Task tasks.scrape_pending_urls[e0c18a03-902f-4f7c-a923-656f66971999] succeeded in 0.0035606001038104296s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:31:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[4eaaf3d8-c68c-4aab-81fd-43399f5667b8] received
[2026-03-30 07:31:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[4eaaf3d8-c68c-4aab-81fd-43399f5667b8] succeeded in 0.003060900024138391s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:32:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[5e858ed1-8d8a-4905-9321-4c5fe6a939b7] received
[2026-03-30 07:32:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[5e858ed1-8d8a-4905-9321-4c5fe6a939b7] succeeded in 0.002851799945347011s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:32:47,817: INFO/MainProcess] Task tasks.scrape_pending_urls[f0301ef0-27cc-489b-b6e6-7a08afd40181] received
[2026-03-30 07:32:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[f0301ef0-27cc-489b-b6e6-7a08afd40181] succeeded in 0.003170000039972365s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:33:17,817: INFO/MainProcess] Task tasks.scrape_pending_urls[aea0a108-e05c-4d73-bd13-9975152df4f8] received
[2026-03-30 07:33:17,821: INFO/MainProcess] Task tasks.scrape_pending_urls[aea0a108-e05c-4d73-bd13-9975152df4f8] succeeded in 0.0032757000299170613s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:33:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[45bbbc1e-53af-43ac-b3d1-d6e4bb4ae337] received
[2026-03-30 07:33:48,032: INFO/MainProcess] Task tasks.collect_system_metrics[45bbbc1e-53af-43ac-b3d1-d6e4bb4ae337] succeeded in 0.5176662999438122s: {'cpu': 27.6, 'memory': 46.2}
[2026-03-30 07:33:48,034: INFO/MainProcess] Task tasks.scrape_pending_urls[e71dd8e6-56e8-40d4-8c4e-01cd983efb54] received
[2026-03-30 07:33:48,109: INFO/MainProcess] Task tasks.scrape_pending_urls[e71dd8e6-56e8-40d4-8c4e-01cd983efb54] succeeded in 0.07454850000794977s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:34:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[f91d982f-e74a-46c6-94c0-2c4075a49397] received
[2026-03-30 07:34:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[f91d982f-e74a-46c6-94c0-2c4075a49397] succeeded in 0.003261399921029806s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:34:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[6098df10-592c-4548-a5a5-a619d606add2] received
[2026-03-30 07:34:47,823: INFO/MainProcess] Task tasks.scrape_pending_urls[6098df10-592c-4548-a5a5-a619d606add2] succeeded in 0.002875700010918081s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:35:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[585096ea-503d-4802-aca2-0c25149b9962] received
[2026-03-30 07:35:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[585096ea-503d-4802-aca2-0c25149b9962] succeeded in 0.003488500020466745s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:35:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[5ab19ab6-e8db-4ff8-af42-e977348a116f] received
[2026-03-30 07:35:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[5ab19ab6-e8db-4ff8-af42-e977348a116f] succeeded in 0.0034702999982982874s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:36:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[27b0615d-0cd7-4505-96d7-7d2586df61c4] received
[2026-03-30 07:36:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[27b0615d-0cd7-4505-96d7-7d2586df61c4] succeeded in 0.003233300056308508s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:36:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[80dcbec3-83fc-4dde-930e-6892ededff4b] received
[2026-03-30 07:36:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[80dcbec3-83fc-4dde-930e-6892ededff4b] succeeded in 0.0032329000532627106s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:37:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[998b85b1-023c-45cc-8320-3e50f531c9da] received
[2026-03-30 07:37:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[998b85b1-023c-45cc-8320-3e50f531c9da] succeeded in 0.003392700105905533s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:37:47,820: INFO/MainProcess] Task tasks.scrape_pending_urls[b1646b5a-9c85-4dd4-8e90-5886318a9e35] received
[2026-03-30 07:37:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[b1646b5a-9c85-4dd4-8e90-5886318a9e35] succeeded in 0.003259599907323718s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:38:17,821: INFO/MainProcess] Task tasks.scrape_pending_urls[7e3e8560-475c-4b9e-95e3-dea5c46080e9] received
[2026-03-30 07:38:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[7e3e8560-475c-4b9e-95e3-dea5c46080e9] succeeded in 0.0030158000299707055s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:38:47,515: INFO/MainProcess] Task tasks.collect_system_metrics[eb756d38-a93a-4a33-9b98-5b30776cbd3f] received
[2026-03-30 07:38:48,026: INFO/MainProcess] Task tasks.collect_system_metrics[eb756d38-a93a-4a33-9b98-5b30776cbd3f] succeeded in 0.5104829000774771s: {'cpu': 29.6, 'memory': 46.1}
[2026-03-30 07:38:48,031: INFO/MainProcess] Task tasks.scrape_pending_urls[413d30a8-95f6-4578-bc86-05e3eabd9e45] received
[2026-03-30 07:38:48,034: INFO/MainProcess] Task tasks.scrape_pending_urls[413d30a8-95f6-4578-bc86-05e3eabd9e45] succeeded in 0.003157900064252317s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:39:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[c9caf661-7332-4b4d-8184-2ec17be66690] received
[2026-03-30 07:39:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[c9caf661-7332-4b4d-8184-2ec17be66690] succeeded in 0.0030608000233769417s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:39:47,821: INFO/MainProcess] Task tasks.scrape_pending_urls[66149ddc-6afd-4212-b412-9bbd45aa0463] received
[2026-03-30 07:39:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[66149ddc-6afd-4212-b412-9bbd45aa0463] succeeded in 0.0034251000033691525s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:40:17,820: INFO/MainProcess] Task tasks.scrape_pending_urls[aad8c5bb-3f6e-4fe4-ad8e-5aabb4aae780] received
[2026-03-30 07:40:17,894: INFO/MainProcess] Task tasks.scrape_pending_urls[aad8c5bb-3f6e-4fe4-ad8e-5aabb4aae780] succeeded in 0.0733407000079751s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:40:47,823: INFO/MainProcess] Task tasks.scrape_pending_urls[587d1444-56f8-4143-b100-78d320f9dfd7] received
[2026-03-30 07:40:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[587d1444-56f8-4143-b100-78d320f9dfd7] succeeded in 0.0030867999885231256s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:41:17,823: INFO/MainProcess] Task tasks.scrape_pending_urls[deb9cb1d-fae6-4cc7-8c4b-45ace74e5ea0] received
[2026-03-30 07:41:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[deb9cb1d-fae6-4cc7-8c4b-45ace74e5ea0] succeeded in 0.003019699943251908s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:41:47,823: INFO/MainProcess] Task tasks.scrape_pending_urls[2bf3def5-31aa-4c80-ba7a-3ccbe4ccb3dd] received
[2026-03-30 07:41:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[2bf3def5-31aa-4c80-ba7a-3ccbe4ccb3dd] succeeded in 0.0035241000587120652s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:42:17,823: INFO/MainProcess] Task tasks.scrape_pending_urls[e2063172-b8f0-4fbf-b5f2-6777e821f06d] received
[2026-03-30 07:42:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[e2063172-b8f0-4fbf-b5f2-6777e821f06d] succeeded in 0.003349800012074411s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:42:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[608d7efd-8fb1-4599-9aae-4d41a5bcc907] received
[2026-03-30 07:42:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[608d7efd-8fb1-4599-9aae-4d41a5bcc907] succeeded in 0.0032700999872758985s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:43:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[e21a2902-2d48-4dfb-815b-f02beba8608f] received
[2026-03-30 07:43:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[e21a2902-2d48-4dfb-815b-f02beba8608f] succeeded in 0.0031190000008791685s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:43:47,514: INFO/MainProcess] Task tasks.collect_system_metrics[7d4008d5-e476-41dc-962b-73c2c52ac45e] received
[2026-03-30 07:43:48,033: INFO/MainProcess] Task tasks.collect_system_metrics[7d4008d5-e476-41dc-962b-73c2c52ac45e] succeeded in 0.5184925999492407s: {'cpu': 27.0, 'memory': 46.2}
[2026-03-30 07:43:48,036: INFO/MainProcess] Task tasks.scrape_pending_urls[0f673d56-9e72-431f-8250-8f64acb00677] received
[2026-03-30 07:43:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[0f673d56-9e72-431f-8250-8f64acb00677] succeeded in 0.004093299969099462s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:44:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[4c36ff1f-604c-4d49-8734-bf5602c74967] received
[2026-03-30 07:44:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[4c36ff1f-604c-4d49-8734-bf5602c74967] succeeded in 0.0034333999501541257s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:44:47,823: INFO/MainProcess] Task tasks.scrape_pending_urls[45106407-85d7-4af1-ab83-d72645d265da] received
[2026-03-30 07:44:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[45106407-85d7-4af1-ab83-d72645d265da] succeeded in 0.002865399932488799s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:45:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[d0994e1a-432b-407e-b4e1-21c5d7b0646a] received
[2026-03-30 07:45:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[d0994e1a-432b-407e-b4e1-21c5d7b0646a] succeeded in 0.003061800030991435s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:45:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[2d4b36a4-92fe-4391-9add-8aaaa0f36a80] received
[2026-03-30 07:45:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[2d4b36a4-92fe-4391-9add-8aaaa0f36a80] succeeded in 0.002992300083860755s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:46:17,824: INFO/MainProcess] Task tasks.scrape_pending_urls[89bb1ed0-47a0-440b-afb7-ed2ef0a7d145] received
[2026-03-30 07:46:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[89bb1ed0-47a0-440b-afb7-ed2ef0a7d145] succeeded in 0.003080699942074716s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:46:47,824: INFO/MainProcess] Task tasks.scrape_pending_urls[83150818-7e35-4344-830c-1df4cc733ea2] received
[2026-03-30 07:46:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[83150818-7e35-4344-830c-1df4cc733ea2] succeeded in 0.002736199996434152s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:47:17,826: INFO/MainProcess] Task tasks.scrape_pending_urls[6dd89bcb-ea47-4607-ada6-54aaa2625f44] received
[2026-03-30 07:47:17,830: INFO/MainProcess] Task tasks.scrape_pending_urls[6dd89bcb-ea47-4607-ada6-54aaa2625f44] succeeded in 0.0033675999147817492s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:47:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[2afcf0dc-3fd0-4a8d-9293-c1b48ccf7bec] received
[2026-03-30 07:47:47,830: INFO/MainProcess] Task tasks.scrape_pending_urls[2afcf0dc-3fd0-4a8d-9293-c1b48ccf7bec] succeeded in 0.0031546999234706163s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:48:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[ab268d87-3bae-435b-ab2e-d381d1cfe6ee] received
[2026-03-30 07:48:17,830: INFO/MainProcess] Task tasks.scrape_pending_urls[ab268d87-3bae-435b-ab2e-d381d1cfe6ee] succeeded in 0.003161999979056418s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:48:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[ff92efe0-0aaa-4c08-a58a-6d531ee7fb8d] received
[2026-03-30 07:48:47,490: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 07:48:47,491: INFO/MainProcess] Task tasks.reset_stale_processing_urls[ff92efe0-0aaa-4c08-a58a-6d531ee7fb8d] succeeded in 0.003530499991029501s: {'reset': 0}
[2026-03-30 07:48:47,602: INFO/MainProcess] Task tasks.collect_system_metrics[6735ef17-3825-4639-bb60-4ea1c6aa998f] received
[2026-03-30 07:48:48,121: INFO/MainProcess] Task tasks.collect_system_metrics[6735ef17-3825-4639-bb60-4ea1c6aa998f] succeeded in 0.517506800009869s: {'cpu': 31.9, 'memory': 46.1}
[2026-03-30 07:48:48,122: INFO/MainProcess] Task tasks.scrape_pending_urls[643eca1e-4806-43d1-9dc5-8b4470499550] received
[2026-03-30 07:48:48,126: INFO/MainProcess] Task tasks.scrape_pending_urls[643eca1e-4806-43d1-9dc5-8b4470499550] succeeded in 0.0034734999062493443s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:49:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[4a681c1b-3701-4113-81bf-c3e359865a72] received
[2026-03-30 07:49:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[4a681c1b-3701-4113-81bf-c3e359865a72] succeeded in 0.0034733000211417675s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:49:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[a5bd40f4-2151-41d3-85c6-127c17dc2d80] received
[2026-03-30 07:49:47,830: INFO/MainProcess] Task tasks.scrape_pending_urls[a5bd40f4-2151-41d3-85c6-127c17dc2d80] succeeded in 0.0031518000178039074s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:50:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[029ac89c-7b93-408b-b9fc-851fd08d075b] received
[2026-03-30 07:50:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[029ac89c-7b93-408b-b9fc-851fd08d075b] succeeded in 0.00293960003182292s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:50:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[0f5bfb34-8eba-4cf3-b129-cb17b0f94ddb] received
[2026-03-30 07:50:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[0f5bfb34-8eba-4cf3-b129-cb17b0f94ddb] succeeded in 0.002989300061017275s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:51:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[84d71d2a-7b18-4b50-aca4-7d3d2e33a9a2] received
[2026-03-30 07:51:17,830: INFO/MainProcess] Task tasks.scrape_pending_urls[84d71d2a-7b18-4b50-aca4-7d3d2e33a9a2] succeeded in 0.003129199962131679s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:51:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[b0df183f-c623-43db-8f01-268784e192bf] received
[2026-03-30 07:51:47,830: INFO/MainProcess] Task tasks.scrape_pending_urls[b0df183f-c623-43db-8f01-268784e192bf] succeeded in 0.003170000039972365s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:52:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[b4faa3d2-92cb-44af-a840-04278c5d6270] received
[2026-03-30 07:52:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[b4faa3d2-92cb-44af-a840-04278c5d6270] succeeded in 0.0031527000246569514s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:52:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[fa3677e5-5f42-4009-96e7-4de4df8d0e5a] received
[2026-03-30 07:52:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[fa3677e5-5f42-4009-96e7-4de4df8d0e5a] succeeded in 0.002881400054320693s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:53:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[385c2e8f-3d38-4eb8-9684-21ec02635948] received
[2026-03-30 07:53:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[385c2e8f-3d38-4eb8-9684-21ec02635948] succeeded in 0.0035132000921294093s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:53:47,518: INFO/MainProcess] Task tasks.collect_system_metrics[be322bf5-5547-4321-976d-f6b56a4dbbb0] received
[2026-03-30 07:53:48,038: INFO/MainProcess] Task tasks.collect_system_metrics[be322bf5-5547-4321-976d-f6b56a4dbbb0] succeeded in 0.5198312000138685s: {'cpu': 29.8, 'memory': 46.3}
[2026-03-30 07:53:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[5dbe428a-b44a-4791-934b-56ccab2c4c44] received
[2026-03-30 07:53:48,044: INFO/MainProcess] Task tasks.scrape_pending_urls[5dbe428a-b44a-4791-934b-56ccab2c4c44] succeeded in 0.003612200031057s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:54:17,828: INFO/MainProcess] Task tasks.scrape_pending_urls[19ab6500-374d-47a2-b319-9bc4a8297e5f] received
[2026-03-30 07:54:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[19ab6500-374d-47a2-b319-9bc4a8297e5f] succeeded in 0.002905600005760789s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:54:47,828: INFO/MainProcess] Task tasks.scrape_pending_urls[9441a8ee-641c-44a6-a8ff-56da19cad545] received
[2026-03-30 07:54:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[9441a8ee-641c-44a6-a8ff-56da19cad545] succeeded in 0.0032189999474212527s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:55:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[87e1b346-921f-45e1-98ca-0d58078579c1] received
[2026-03-30 07:55:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[87e1b346-921f-45e1-98ca-0d58078579c1] succeeded in 0.003087799996137619s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:55:47,827: INFO/MainProcess] Task tasks.scrape_pending_urls[d325eea2-940e-4c68-a698-fe546651e5d6] received
[2026-03-30 07:55:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[d325eea2-940e-4c68-a698-fe546651e5d6] succeeded in 0.0032011999282985926s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:56:17,827: INFO/MainProcess] Task tasks.scrape_pending_urls[db9c775e-811b-485f-bbb6-2dcf56bd7b80] received
[2026-03-30 07:56:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[db9c775e-811b-485f-bbb6-2dcf56bd7b80] succeeded in 0.003552700043655932s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:56:47,830: INFO/MainProcess] Task tasks.scrape_pending_urls[c9102bd6-6234-4215-9e9f-367848f86172] received
[2026-03-30 07:56:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[c9102bd6-6234-4215-9e9f-367848f86172] succeeded in 0.0030658000614494085s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:57:17,830: INFO/MainProcess] Task tasks.scrape_pending_urls[a62a709d-c45a-44d4-a2b0-b7d0bda3ebf2] received
[2026-03-30 07:57:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[a62a709d-c45a-44d4-a2b0-b7d0bda3ebf2] succeeded in 0.00324480002745986s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:57:47,830: INFO/MainProcess] Task tasks.scrape_pending_urls[ad94e87c-678f-4cf1-8175-1efc88f1a26c] received
[2026-03-30 07:57:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[ad94e87c-678f-4cf1-8175-1efc88f1a26c] succeeded in 0.0035157999955117702s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:58:17,830: INFO/MainProcess] Task tasks.scrape_pending_urls[6029fb50-769e-42bd-904c-1974a897bc54] received
[2026-03-30 07:58:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[6029fb50-769e-42bd-904c-1974a897bc54] succeeded in 0.0034697999944910407s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:58:47,517: INFO/MainProcess] Task tasks.collect_system_metrics[9d494528-0660-4a35-85e7-1dc70362bbb3] received
[2026-03-30 07:58:48,034: INFO/MainProcess] Task tasks.collect_system_metrics[9d494528-0660-4a35-85e7-1dc70362bbb3] succeeded in 0.5166010000975803s: {'cpu': 27.0, 'memory': 46.0}
[2026-03-30 07:58:48,036: INFO/MainProcess] Task tasks.scrape_pending_urls[a40c6dbe-8f35-46d3-a9a4-62f076a10164] received
[2026-03-30 07:58:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[a40c6dbe-8f35-46d3-a9a4-62f076a10164] succeeded in 0.0035859999479725957s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:59:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[78e2e2a7-085b-4f22-8a07-a21f15883620] received
[2026-03-30 07:59:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[78e2e2a7-085b-4f22-8a07-a21f15883620] succeeded in 0.002801000024192035s: {'status': 'idle', 'pending': 0}
[2026-03-30 07:59:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[67f115c5-afcd-44f3-9b73-a577745b623b] received
[2026-03-30 07:59:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[67f115c5-afcd-44f3-9b73-a577745b623b] succeeded in 0.003244199906475842s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:00:17,830: INFO/MainProcess] Task tasks.scrape_pending_urls[b8b8b14d-d76e-43b1-ba80-b5190c2948db] received
[2026-03-30 08:00:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[b8b8b14d-d76e-43b1-ba80-b5190c2948db] succeeded in 0.003182400017976761s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:00:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[ceb7279a-dcf5-43ef-8a0e-fb8b0f278619] received
[2026-03-30 08:00:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[ceb7279a-dcf5-43ef-8a0e-fb8b0f278619] succeeded in 0.002933999989181757s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:01:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[4b2a5767-34dc-4696-bd0a-6b2cc6672528] received
[2026-03-30 08:01:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[4b2a5767-34dc-4696-bd0a-6b2cc6672528] succeeded in 0.003101699985563755s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:01:47,831: INFO/MainProcess] Task tasks.scrape_pending_urls[dcbbc1c3-a3ac-4355-9e87-7e9ece230d70] received
[2026-03-30 08:01:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[dcbbc1c3-a3ac-4355-9e87-7e9ece230d70] succeeded in 0.0028700000839307904s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:02:17,831: INFO/MainProcess] Task tasks.scrape_pending_urls[d5371701-d099-4ed8-bf7a-e37d4d008308] received
[2026-03-30 08:02:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[d5371701-d099-4ed8-bf7a-e37d4d008308] succeeded in 0.00303869997151196s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:02:47,830: INFO/MainProcess] Task tasks.scrape_pending_urls[d4324af9-a4bc-45ff-ba87-eca51fd67949] received
[2026-03-30 08:02:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[d4324af9-a4bc-45ff-ba87-eca51fd67949] succeeded in 0.0030345000559464097s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:03:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[7b227556-5a5d-4069-ae08-943896735463] received
[2026-03-30 08:03:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[7b227556-5a5d-4069-ae08-943896735463] succeeded in 0.002763999975286424s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:03:47,518: INFO/MainProcess] Task tasks.collect_system_metrics[3c21ec7d-0f8a-4320-b7ee-0cda38b84ed5] received
[2026-03-30 08:03:48,052: INFO/MainProcess] Task tasks.collect_system_metrics[3c21ec7d-0f8a-4320-b7ee-0cda38b84ed5] succeeded in 0.5342412999598309s: {'cpu': 31.9, 'memory': 46.1}
[2026-03-30 08:03:48,054: INFO/MainProcess] Task tasks.scrape_pending_urls[95e1bc0e-1930-40b8-878e-b655e4565acf] received
[2026-03-30 08:03:48,057: INFO/MainProcess] Task tasks.scrape_pending_urls[95e1bc0e-1930-40b8-878e-b655e4565acf] succeeded in 0.0030872999923303723s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:04:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[c9180fea-4fcf-4504-8b32-93acfe289bb5] received
[2026-03-30 08:04:17,838: INFO/MainProcess] Task tasks.scrape_pending_urls[c9180fea-4fcf-4504-8b32-93acfe289bb5] succeeded in 0.003716000006534159s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:04:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[95cd99fa-16b3-4feb-8015-60ca1325e9b6] received
[2026-03-30 08:04:47,837: INFO/MainProcess] Task tasks.scrape_pending_urls[95cd99fa-16b3-4feb-8015-60ca1325e9b6] succeeded in 0.0034078999888151884s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:05:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[d41e1304-22c6-4cf6-976d-d9cafbba21e9] received
[2026-03-30 08:05:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[d41e1304-22c6-4cf6-976d-d9cafbba21e9] succeeded in 0.002912200056016445s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:05:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[2a269072-d1a4-4b97-923a-44933c37c61b] received
[2026-03-30 08:05:47,838: INFO/MainProcess] Task tasks.scrape_pending_urls[2a269072-d1a4-4b97-923a-44933c37c61b] succeeded in 0.0033302000956609845s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:06:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[51d88264-5b36-425f-8b42-e6ffc9b98a1b] received
[2026-03-30 08:06:17,838: INFO/MainProcess] Task tasks.scrape_pending_urls[51d88264-5b36-425f-8b42-e6ffc9b98a1b] succeeded in 0.0031066000228747725s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:06:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[06c2b9cf-ddce-465d-8f8d-214f3b5b408d] received
[2026-03-30 08:06:47,838: INFO/MainProcess] Task tasks.scrape_pending_urls[06c2b9cf-ddce-465d-8f8d-214f3b5b408d] succeeded in 0.003261399921029806s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:07:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[13bc35a9-1856-4753-ab3d-c679306e28c4] received
[2026-03-30 08:07:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[13bc35a9-1856-4753-ab3d-c679306e28c4] succeeded in 0.0029369000112637877s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:07:47,834: INFO/MainProcess] Task tasks.scrape_pending_urls[37159e53-b4c6-4b3a-9d97-9177bb01ab42] received
[2026-03-30 08:07:47,837: INFO/MainProcess] Task tasks.scrape_pending_urls[37159e53-b4c6-4b3a-9d97-9177bb01ab42] succeeded in 0.0028632000321522355s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:08:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[eb6c91f5-0496-430f-bb5d-945e92040632] received
[2026-03-30 08:08:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[eb6c91f5-0496-430f-bb5d-945e92040632] succeeded in 0.002832799917086959s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:08:47,517: INFO/MainProcess] Task tasks.collect_system_metrics[dcee05e0-7fd4-4edc-8e3e-d390400b90c5] received
[2026-03-30 08:08:48,034: INFO/MainProcess] Task tasks.collect_system_metrics[dcee05e0-7fd4-4edc-8e3e-d390400b90c5] succeeded in 0.5165627999231219s: {'cpu': 24.0, 'memory': 46.2}
[2026-03-30 08:08:48,036: INFO/MainProcess] Task tasks.scrape_pending_urls[31786c40-1ff6-4d69-bb31-2e27be291ae1] received
[2026-03-30 08:08:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[31786c40-1ff6-4d69-bb31-2e27be291ae1] succeeded in 0.0037483000196516514s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:09:17,834: INFO/MainProcess] Task tasks.scrape_pending_urls[934af218-48f1-418f-9c79-d5528de2f03f] received
[2026-03-30 08:09:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[934af218-48f1-418f-9c79-d5528de2f03f] succeeded in 0.0028195000486448407s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:09:47,837: INFO/MainProcess] Task tasks.scrape_pending_urls[9af1760a-a94a-44e3-b023-ed2a5c4851c9] received
[2026-03-30 08:09:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[9af1760a-a94a-44e3-b023-ed2a5c4851c9] succeeded in 0.002841099980287254s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:10:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[8a2f599f-de93-439b-87ce-0e56dff3f4ed] received
[2026-03-30 08:10:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[8a2f599f-de93-439b-87ce-0e56dff3f4ed] succeeded in 0.003765299916267395s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:10:47,837: INFO/MainProcess] Task tasks.scrape_pending_urls[4573ea90-abcc-4ccb-9936-3a529efbd3f3] received
[2026-03-30 08:10:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[4573ea90-abcc-4ccb-9936-3a529efbd3f3] succeeded in 0.0029392000287771225s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:11:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[dee75638-8801-4140-b2e9-06f643ed5b7a] received
[2026-03-30 08:11:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[dee75638-8801-4140-b2e9-06f643ed5b7a] succeeded in 0.0030941000441089272s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:11:47,837: INFO/MainProcess] Task tasks.scrape_pending_urls[9c83bd79-abd2-4775-9e59-dd427c8eb98a] received
[2026-03-30 08:11:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[9c83bd79-abd2-4775-9e59-dd427c8eb98a] succeeded in 0.0031620999798178673s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:12:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[78566314-d5a6-410e-9d94-14e2aa292e2a] received
[2026-03-30 08:12:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[78566314-d5a6-410e-9d94-14e2aa292e2a] succeeded in 0.0028986999532207847s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:12:47,837: INFO/MainProcess] Task tasks.scrape_pending_urls[a964b826-7aa1-449e-831f-c503175a6499] received
[2026-03-30 08:12:47,840: INFO/MainProcess] Task tasks.scrape_pending_urls[a964b826-7aa1-449e-831f-c503175a6499] succeeded in 0.002745900070294738s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:13:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[15bbc4d9-5513-4895-8bed-66a8b705927e] received
[2026-03-30 08:13:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[15bbc4d9-5513-4895-8bed-66a8b705927e] succeeded in 0.0030946999322623014s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:13:47,517: INFO/MainProcess] Task tasks.collect_system_metrics[24659622-290b-47dd-a459-89c16d035969] received
[2026-03-30 08:13:48,035: INFO/MainProcess] Task tasks.collect_system_metrics[24659622-290b-47dd-a459-89c16d035969] succeeded in 0.5172691999468952s: {'cpu': 24.2, 'memory': 46.2}
[2026-03-30 08:13:48,037: INFO/MainProcess] Task tasks.scrape_pending_urls[9b5fb542-7ed1-48e8-9f6c-91f360861354] received
[2026-03-30 08:13:48,040: INFO/MainProcess] Task tasks.scrape_pending_urls[9b5fb542-7ed1-48e8-9f6c-91f360861354] succeeded in 0.0030685000820085406s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:14:17,837: INFO/MainProcess] Task tasks.scrape_pending_urls[b04e30cf-ed4e-42fc-b2cc-86a44435d40f] received
[2026-03-30 08:14:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[b04e30cf-ed4e-42fc-b2cc-86a44435d40f] succeeded in 0.0031177999917417765s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:14:47,838: INFO/MainProcess] Task tasks.scrape_pending_urls[e0196146-8426-4eb6-9899-e6efc77fec78] received
[2026-03-30 08:14:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[e0196146-8426-4eb6-9899-e6efc77fec78] succeeded in 0.0029693000251427293s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:15:17,838: INFO/MainProcess] Task tasks.scrape_pending_urls[26a92cbe-3e59-47aa-9ad1-7f8d7c2ebdb2] received
[2026-03-30 08:15:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[26a92cbe-3e59-47aa-9ad1-7f8d7c2ebdb2] succeeded in 0.0031932999845594168s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:15:47,838: INFO/MainProcess] Task tasks.scrape_pending_urls[7b001945-e2f8-473c-9ab7-b28b76480c67] received
[2026-03-30 08:15:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[7b001945-e2f8-473c-9ab7-b28b76480c67] succeeded in 0.00327590003143996s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:16:17,840: INFO/MainProcess] Task tasks.scrape_pending_urls[31224762-3354-4069-be5b-abfbd41a5f2d] received
[2026-03-30 08:16:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[31224762-3354-4069-be5b-abfbd41a5f2d] succeeded in 0.0031973000150173903s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:16:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[11468f27-513f-41d0-98e6-a4ba1a883961] received
[2026-03-30 08:16:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[11468f27-513f-41d0-98e6-a4ba1a883961] succeeded in 0.0030433000065386295s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:17:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[5d9b8c2e-b358-4699-a0fd-d12ad5fe0f18] received
[2026-03-30 08:17:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[5d9b8c2e-b358-4699-a0fd-d12ad5fe0f18] succeeded in 0.0033393000485375524s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:17:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[80d7e19f-6425-4cd5-a897-c286bb25af6a] received
[2026-03-30 08:17:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[80d7e19f-6425-4cd5-a897-c286bb25af6a] succeeded in 0.0031943999929353595s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:18:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[829c633b-59a8-49ea-944f-0bad5616eb0d] received
[2026-03-30 08:18:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[829c633b-59a8-49ea-944f-0bad5616eb0d] succeeded in 0.003294900059700012s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:18:47,487: INFO/MainProcess] Task tasks.reset_stale_processing_urls[1910f914-7d1b-4c80-898f-5f83c65d5ab3] received
[2026-03-30 08:18:47,490: INFO/MainProcess] Reset 0 stale processing URLs (language tracking cleared).
[2026-03-30 08:18:47,491: INFO/MainProcess] Task tasks.reset_stale_processing_urls[1910f914-7d1b-4c80-898f-5f83c65d5ab3] succeeded in 0.0037838000571355224s: {'reset': 0}
[2026-03-30 08:18:47,517: INFO/MainProcess] Task tasks.collect_system_metrics[910504e0-8cdf-4426-b557-87e1d3773044] received
[2026-03-30 08:18:48,036: INFO/MainProcess] Task tasks.collect_system_metrics[910504e0-8cdf-4426-b557-87e1d3773044] succeeded in 0.5183206000365317s: {'cpu': 28.5, 'memory': 46.0}
[2026-03-30 08:18:48,038: INFO/MainProcess] Task tasks.scrape_pending_urls[9820b1f1-6ab7-4a36-ac20-f8e0f5f5c243] received
[2026-03-30 08:18:48,042: INFO/MainProcess] Task tasks.scrape_pending_urls[9820b1f1-6ab7-4a36-ac20-f8e0f5f5c243] succeeded in 0.0033687999239191413s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:19:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[4567b4ca-7c3f-464b-9690-9594388f57e6] received
[2026-03-30 08:19:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[4567b4ca-7c3f-464b-9690-9594388f57e6] succeeded in 0.0032435000175610185s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:19:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[beafb705-4b6f-43e2-82cf-1b03f18328a2] received
[2026-03-30 08:19:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[beafb705-4b6f-43e2-82cf-1b03f18328a2] succeeded in 0.0031796999974176288s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:20:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[381cab2b-bec4-4be9-88ec-9aa0b9ae7439] received
[2026-03-30 08:20:17,845: INFO/MainProcess] Task tasks.scrape_pending_urls[381cab2b-bec4-4be9-88ec-9aa0b9ae7439] succeeded in 0.003333200002089143s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:20:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[d6a5d714-e12f-4c3e-a990-cb214dff6431] received
[2026-03-30 08:20:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[d6a5d714-e12f-4c3e-a990-cb214dff6431] succeeded in 0.0027074000099673867s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:21:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[6b94093f-be01-42c3-a139-a223428a5e13] received
[2026-03-30 08:21:17,845: INFO/MainProcess] Task tasks.scrape_pending_urls[6b94093f-be01-42c3-a139-a223428a5e13] succeeded in 0.0030340999364852905s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:21:47,841: INFO/MainProcess] Task tasks.scrape_pending_urls[eae4b701-581c-4e9d-93fd-94beaec7edb7] received
[2026-03-30 08:21:47,845: INFO/MainProcess] Task tasks.scrape_pending_urls[eae4b701-581c-4e9d-93fd-94beaec7edb7] succeeded in 0.003113900078460574s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:22:17,841: INFO/MainProcess] Task tasks.scrape_pending_urls[78436cfa-a7b6-4ffb-be97-98b334646bf6] received
[2026-03-30 08:22:17,845: INFO/MainProcess] Task tasks.scrape_pending_urls[78436cfa-a7b6-4ffb-be97-98b334646bf6] succeeded in 0.003387399949133396s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:22:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[ad745fea-02ce-4bc9-8e85-380067ec0599] received
[2026-03-30 08:22:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[ad745fea-02ce-4bc9-8e85-380067ec0599] succeeded in 0.0035247000632807612s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:23:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[811bd6d7-136a-40fe-ab29-7efe5d5d42f1] received
[2026-03-30 08:23:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[811bd6d7-136a-40fe-ab29-7efe5d5d42f1] succeeded in 0.003247199929319322s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:23:47,517: INFO/MainProcess] Task tasks.collect_system_metrics[7e0ab615-328b-467c-ae36-5cf7cd4f30c1] received
[2026-03-30 08:23:48,036: INFO/MainProcess] Task tasks.collect_system_metrics[7e0ab615-328b-467c-ae36-5cf7cd4f30c1] succeeded in 0.5180222999770194s: {'cpu': 28.1, 'memory': 46.2}
[2026-03-30 08:23:48,038: INFO/MainProcess] Task tasks.scrape_pending_urls[cfc682f1-4bb5-4e67-85b6-f6004c038aa6] received
[2026-03-30 08:23:48,042: INFO/MainProcess] Task tasks.scrape_pending_urls[cfc682f1-4bb5-4e67-85b6-f6004c038aa6] succeeded in 0.0037444999907165766s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:24:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[13c37331-d979-4b61-94e4-3ad4f5f2c4df] received
[2026-03-30 08:24:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[13c37331-d979-4b61-94e4-3ad4f5f2c4df] succeeded in 0.003336499910801649s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:24:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[336cf0ea-759e-4187-92c7-1ddc3ac44178] received
[2026-03-30 08:24:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[336cf0ea-759e-4187-92c7-1ddc3ac44178] succeeded in 0.0031428999500349164s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:25:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[3e81516f-cbe8-433c-885d-965809900b06] received
[2026-03-30 08:25:17,847: INFO/MainProcess] Task tasks.scrape_pending_urls[3e81516f-cbe8-433c-885d-965809900b06] succeeded in 0.0029552000341936946s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:25:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[a271bf5c-3d36-43cc-a5b3-6981e0a81ad0] received
[2026-03-30 08:25:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[a271bf5c-3d36-43cc-a5b3-6981e0a81ad0] succeeded in 0.0029571999330073595s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:26:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[70b3bcd3-628c-4e88-9a56-6e846bc879f7] received
[2026-03-30 08:26:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[70b3bcd3-628c-4e88-9a56-6e846bc879f7] succeeded in 0.0029943000990897417s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:26:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[daa14fec-a8a9-4dfe-8f32-249da9bed4b3] received
[2026-03-30 08:26:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[daa14fec-a8a9-4dfe-8f32-249da9bed4b3] succeeded in 0.0033442999701946974s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:27:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[e455c91f-8f31-45a6-b76d-bfc9f6594194] received
[2026-03-30 08:27:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[e455c91f-8f31-45a6-b76d-bfc9f6594194] succeeded in 0.0028879999881610274s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:27:47,844: INFO/MainProcess] Task tasks.scrape_pending_urls[297d2b78-a4a1-4fb2-b72b-94aff731926f] received
[2026-03-30 08:27:47,847: INFO/MainProcess] Task tasks.scrape_pending_urls[297d2b78-a4a1-4fb2-b72b-94aff731926f] succeeded in 0.0027534000109881163s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:28:17,844: INFO/MainProcess] Task tasks.scrape_pending_urls[2ff1434a-6bea-43b5-9d37-1f67c1cb62d5] received
[2026-03-30 08:28:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[2ff1434a-6bea-43b5-9d37-1f67c1cb62d5] succeeded in 0.0031960998894646764s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:28:47,518: INFO/MainProcess] Task tasks.collect_system_metrics[dcba5112-b2f6-445b-83aa-c5a512e0abb1] received
[2026-03-30 08:28:48,036: INFO/MainProcess] Task tasks.collect_system_metrics[dcba5112-b2f6-445b-83aa-c5a512e0abb1] succeeded in 0.5182963999686763s: {'cpu': 23.7, 'memory': 46.2}
[2026-03-30 08:28:48,038: INFO/MainProcess] Task tasks.scrape_pending_urls[cfb5dccb-90b1-4a5e-8249-57946499ce4e] received
[2026-03-30 08:28:48,042: INFO/MainProcess] Task tasks.scrape_pending_urls[cfb5dccb-90b1-4a5e-8249-57946499ce4e] succeeded in 0.0031145999673753977s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:29:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[fe78eff6-488b-4a0f-bfa4-aa262f96e4a5] received
[2026-03-30 08:29:17,925: INFO/MainProcess] Task tasks.scrape_pending_urls[fe78eff6-488b-4a0f-bfa4-aa262f96e4a5] succeeded in 0.07689769996795803s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:29:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[fd068a5d-77b8-44d3-92ce-580a86e8c9ac] received
[2026-03-30 08:29:47,851: INFO/MainProcess] Task tasks.scrape_pending_urls[fd068a5d-77b8-44d3-92ce-580a86e8c9ac] succeeded in 0.0029441999504342675s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:30:00,002: INFO/MainProcess] Task tasks.purge_old_debug_html[bf675325-c24f-4e56-bfb8-48f2849f4016] received
[2026-03-30 08:30:00,004: INFO/MainProcess] Task tasks.purge_old_debug_html[bf675325-c24f-4e56-bfb8-48f2849f4016] succeeded in 0.0014099000254645944s: {'skipped': True, 'reason': 'DEBUG_HTML_SAVE is disabled'}
[2026-03-30 08:30:17,847: INFO/MainProcess] Task tasks.scrape_pending_urls[8b8e4f74-e304-46ff-8da7-86f291855181] received
[2026-03-30 08:30:17,851: INFO/MainProcess] Task tasks.scrape_pending_urls[8b8e4f74-e304-46ff-8da7-86f291855181] succeeded in 0.003213500021956861s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:30:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[8c7e9dd9-2c6e-4a56-9689-81a9cbffcaee] received
[2026-03-30 08:30:47,852: INFO/MainProcess] Task tasks.scrape_pending_urls[8c7e9dd9-2c6e-4a56-9689-81a9cbffcaee] succeeded in 0.0033677000319585204s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:31:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[64bdb99e-54a4-44ac-b860-32000877586f] received
[2026-03-30 08:31:17,852: INFO/MainProcess] Task tasks.scrape_pending_urls[64bdb99e-54a4-44ac-b860-32000877586f] succeeded in 0.003467799979262054s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:31:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[a598894b-59ff-4b16-a553-ea4ca338fe5b] received
[2026-03-30 08:31:47,851: INFO/MainProcess] Task tasks.scrape_pending_urls[a598894b-59ff-4b16-a553-ea4ca338fe5b] succeeded in 0.0029821000061929226s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:32:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[dac4ab51-1f50-4a51-842f-712ee49d8ec3] received
[2026-03-30 08:32:17,852: INFO/MainProcess] Task tasks.scrape_pending_urls[dac4ab51-1f50-4a51-842f-712ee49d8ec3] succeeded in 0.003282999969087541s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:32:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[09be4861-5916-4a82-bde1-9baa144d8db9] received
[2026-03-30 08:32:47,851: INFO/MainProcess] Task tasks.scrape_pending_urls[09be4861-5916-4a82-bde1-9baa144d8db9] succeeded in 0.003206699970178306s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:33:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[f6fcba66-64f8-4387-87a5-787d75916c4f] received
[2026-03-30 08:33:17,852: INFO/MainProcess] Task tasks.scrape_pending_urls[f6fcba66-64f8-4387-87a5-787d75916c4f] succeeded in 0.0029724000487476587s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:33:47,518: INFO/MainProcess] Task tasks.collect_system_metrics[669767b5-2943-4bcc-b1c9-11837027f366] received
[2026-03-30 08:33:48,037: INFO/MainProcess] Task tasks.collect_system_metrics[669767b5-2943-4bcc-b1c9-11837027f366] succeeded in 0.5190308999735862s: {'cpu': 24.6, 'memory': 46.2}
[2026-03-30 08:33:48,041: INFO/MainProcess] Task tasks.scrape_pending_urls[ddb5a5c9-dc4b-4289-9486-bd381fb8e597] received
[2026-03-30 08:33:48,045: INFO/MainProcess] Task tasks.scrape_pending_urls[ddb5a5c9-dc4b-4289-9486-bd381fb8e597] succeeded in 0.002999700023792684s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:34:17,849: INFO/MainProcess] Task tasks.scrape_pending_urls[d35b398c-c35a-4683-b31a-f173dfc39ce8] received
[2026-03-30 08:34:17,938: INFO/MainProcess] Task tasks.scrape_pending_urls[d35b398c-c35a-4683-b31a-f173dfc39ce8] succeeded in 0.08923299994785339s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:34:47,848: INFO/MainProcess] Task tasks.scrape_pending_urls[2c1ca37e-1a4a-48c3-aef6-438bf53e6b64] received
[2026-03-30 08:34:47,852: INFO/MainProcess] Task tasks.scrape_pending_urls[2c1ca37e-1a4a-48c3-aef6-438bf53e6b64] succeeded in 0.003369600046426058s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:35:17,848: INFO/MainProcess] Task tasks.scrape_pending_urls[a3406ef3-d8ca-4faf-9ecb-61d632b7b2ed] received
[2026-03-30 08:35:17,852: INFO/MainProcess] Task tasks.scrape_pending_urls[a3406ef3-d8ca-4faf-9ecb-61d632b7b2ed] succeeded in 0.003582900040782988s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:35:47,851: INFO/MainProcess] Task tasks.scrape_pending_urls[75f795ec-f10b-4e6f-aad2-5fa520e251c0] received
[2026-03-30 08:35:47,855: INFO/MainProcess] Task tasks.scrape_pending_urls[75f795ec-f10b-4e6f-aad2-5fa520e251c0] succeeded in 0.0033770999871194363s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:36:17,851: INFO/MainProcess] Task tasks.scrape_pending_urls[800b9ef6-11ee-4610-b337-b6314836dbab] received
[2026-03-30 08:36:17,855: INFO/MainProcess] Task tasks.scrape_pending_urls[800b9ef6-11ee-4610-b337-b6314836dbab] succeeded in 0.0032837000908330083s: {'status': 'idle', 'pending': 0}
[2026-03-30 08:36:47,851: INFO/MainProcess] Task tasks.scrape_pending_urls[a98a2617-6775-4e00-86a2-0b68b721f72c] received
[2026-03-30 08:36:47,856: INFO/MainProcess] Task tasks.scrape_pending_urls[a98a2617-6775-4e00-86a2-0b68b721f72c] succeeded in 0.004748599953018129s: {'status': 'idle', 'pending': 0}
