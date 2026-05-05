Query SQL: SELECT url_id , COUNT(*) as COUNT_hotels , hotel_name FROM hotels GROUP BY url_id, hotel_name ORDER BY url_id
Result:
```
"url_id"; "count_hotels"; "hotel_name"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "6"; "Sun Lodge Schladming by Schladming-Appartements"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "6"; "vidimo se"
"6092eab1-6017-473e-916f-46278fd28ddf"; "6"; "Haus Mobene - Hotel Garni"
"6339b88f-3637-4eef-a253-319da5fde794"; "6"; "Hotel Mariahilf"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "6"; "wild & bolz eMotel"
"a09f778f-6437-4a15-9eda-656625ecab87"; "6"; "Hotel Sonnschupfer"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "6"; "Villa Dvor"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "6"; "Hotel Feichtinger Graz"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "6"; "Hotel Wasserpalast - breakfast for free!!!"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "6"; "Hotel Birkenhof"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "6"; "Hotel zum Heiligen Geist"
```

---

Query SQL: SELECT url_id , COUNT(*) as COUNT_legal FROM hotels_legal GROUP BY url_id ORDER BY url_id
Result:
```
"url_id"; "count_legal"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "6"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "6"
"6092eab1-6017-473e-916f-46278fd28ddf"; "6"
"6339b88f-3637-4eef-a253-319da5fde794"; "6"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "6"
"a09f778f-6437-4a15-9eda-656625ecab87"; "6"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "6"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "6"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "6"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "6"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "6"
```

---

Query SQL: SELECT url_id , COUNT(*) as COUNT_polices FROM hotels_policies GROUP BY url_id ORDER BY url_id
Result:
```
"url_id"; "count_polices"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "66"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "42"
"6092eab1-6017-473e-916f-46278fd28ddf"; "42"
"6339b88f-3637-4eef-a253-319da5fde794"; "54"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "42"
"a09f778f-6437-4a15-9eda-656625ecab87"; "42"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "60"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "48"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "42"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "48"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "42"
```

---

Query SQL: SELECT url_id , COUNT(*) as COUNT_descriptions FROM hotels_description GROUP BY url_id  ORDER BY url_id limit 50 
Result:
```
"url_id"; "count_descriptions"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "6"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "6"
"6092eab1-6017-473e-916f-46278fd28ddf"; "6"
"6339b88f-3637-4eef-a253-319da5fde794"; "6"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "6"
"a09f778f-6437-4a15-9eda-656625ecab87"; "6"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "6"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "6"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "6"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "6"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "6"
```

---

Query SQL: SELECT url_id , language, COUNT(*) AS COUNT_service_category  FROM hotels_all_services WHERE language ='en' GROUP BY url_id , language
Result:
```
"url_id"; "language"; "count_service_category"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "en"; "6"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "en"; "12"
"6339b88f-3637-4eef-a253-319da5fde794"; "en"; "16"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "en"; "20"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "en"; "28"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "en"; "4"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "en"; "6"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "en"; "18"
"a09f778f-6437-4a15-9eda-656625ecab87"; "en"; "21"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "en"; "5"
"6092eab1-6017-473e-916f-46278fd28ddf"; "en"; "13"
```

---

Query SQL: SELECT al.url_id , al.hotel_id , al.language , COUNT(al.*) AS COUNT_service_category , h.hotel_name FROM hotels_all_services al LEFT JOIN hotels h ON al.url_id = h.url_id and al.language = h.language and al.hotel_id = h.id GROUP BY al.url_id , al.hotel_id , h.hotel_name , al.language ORDER BY  al.url_id , al.language 
Result:
```
"url_id"; "hotel_id"; "language"; "count_service_category"; "hotel_name"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "a4141bee-8fa9-497a-a609-56dfe75218a5"; "de"; "28"; "Sun Lodge Schladming by Schladming-Appartements"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "18419cce-d496-4510-940c-20821ab0f280"; "en"; "28"; "Sun Lodge Schladming by Schladming-Appartements"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "3a544e25-e57e-4c7e-90fb-32c393c2752d"; "es"; "28"; "Sun Lodge Schladming by Schladming-Appartements"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "b6513ced-45d4-4add-9cde-09672e6d1c07"; "fr"; "28"; "Sun Lodge Schladming by Schladming-Appartements"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "326f266f-b475-4365-a0ed-cc9fba0c8692"; "it"; "28"; "Sun Lodge Schladming by Schladming-Appartements"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "5948f029-83c0-4aa3-a7fa-03d34b9a09b2"; "pt"; "28"; "Sun Lodge Schladming by Schladming-Appartements"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "d3649805-aa3e-44c0-b3fe-b3edb2ad729b"; "de"; "18"; "vidimo se"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "7d197c4f-7680-4a68-9c4c-62e86062659f"; "en"; "18"; "vidimo se"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "a9fdce42-94e2-46d9-b137-7b779adc5838"; "es"; "18"; "vidimo se"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "e1104235-a731-4117-a9a6-bd2e170d570f"; "fr"; "17"; "vidimo se"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "16a253cd-9d10-4639-a895-b8300a3f6e0b"; "it"; "18"; "vidimo se"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "c64a94f1-0177-4d8e-99de-2793db54ec5c"; "pt"; "17"; "vidimo se"
"6092eab1-6017-473e-916f-46278fd28ddf"; "085bb053-1547-46f5-aabe-a0a5f337256b"; "de"; "13"; "Haus Mobene - Hotel Garni"
"6092eab1-6017-473e-916f-46278fd28ddf"; "a054b362-ad21-4da8-a91e-fb41a24d5f94"; "en"; "13"; "Haus Mobene - Hotel Garni"
"6092eab1-6017-473e-916f-46278fd28ddf"; "3114e9cc-cb0b-4020-8025-c5ac62d035d7"; "es"; "13"; "Haus Mobene - Hotel Garni"
"6092eab1-6017-473e-916f-46278fd28ddf"; "7da40948-0309-4b64-ae33-718634289469"; "fr"; "13"; "Haus Mobene - Hotel Garni"
"6092eab1-6017-473e-916f-46278fd28ddf"; "c0de1b6d-b855-4ae5-86d6-567745c70032"; "it"; "13"; "Haus Mobene - Hotel Garni"
"6092eab1-6017-473e-916f-46278fd28ddf"; "f7aa8d20-4fa8-4c9f-a00f-1b510c761f66"; "pt"; "13"; "Haus Mobene - Hotel Garni"
"6339b88f-3637-4eef-a253-319da5fde794"; "49d9b763-8256-4547-b1be-c14191734e03"; "de"; "16"; "Hotel Mariahilf"
"6339b88f-3637-4eef-a253-319da5fde794"; "bf9364f4-585e-4851-b473-2b84e82a7ab2"; "en"; "16"; "Hotel Mariahilf"
"6339b88f-3637-4eef-a253-319da5fde794"; "5b0ab414-b587-4900-bf84-42a2f27446e1"; "es"; "16"; "Hotel Mariahilf"
"6339b88f-3637-4eef-a253-319da5fde794"; "9988f3b3-5cc4-4340-ad9a-6482927a2173"; "fr"; "16"; "Hotel Mariahilf"
"6339b88f-3637-4eef-a253-319da5fde794"; "79504444-9c89-445e-b697-3b12b02e8083"; "it"; "16"; "Hotel Mariahilf"
"6339b88f-3637-4eef-a253-319da5fde794"; "c445cc4b-42eb-4fe0-8083-e387af765823"; "pt"; "16"; "Hotel Mariahilf"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "54b99542-7841-4dec-941f-98a9c317eb48"; "de"; "6"; "wild & bolz eMotel"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "021d6ab0-2009-4392-a8f9-8b7a7e6ca784"; "en"; "6"; "wild & bolz eMotel"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "951455e3-0b01-4266-b992-fa6f4c4db7a9"; "es"; "6"; "wild & bolz eMotel"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "6ecab6fa-574c-4dd0-9f3e-bad343692761"; "fr"; "6"; "wild & bolz eMotel"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "adcbdc4e-082e-4315-920a-f5825e4d6927"; "it"; "6"; "wild & bolz eMotel"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "a5b8fe77-0a3e-4ebe-a7c0-a2da73670680"; "pt"; "6"; "wild & bolz eMotel"
"a09f778f-6437-4a15-9eda-656625ecab87"; "35744f5e-ff97-424d-a64f-77c60d8e3e02"; "de"; "21"; "Hotel Sonnschupfer"
"a09f778f-6437-4a15-9eda-656625ecab87"; "faa8e3b0-3438-4913-9f39-e38912cbf34f"; "en"; "21"; "Hotel Sonnschupfer"
"a09f778f-6437-4a15-9eda-656625ecab87"; "d9f0de62-9437-4131-985e-b171b74b6308"; "es"; "21"; "Hotel Sonnschupfer"
"a09f778f-6437-4a15-9eda-656625ecab87"; "a6c26fbe-b835-439a-a77e-a77cae711880"; "fr"; "21"; "Hotel Sonnschupfer"
"a09f778f-6437-4a15-9eda-656625ecab87"; "afaab18c-9f90-47d2-8f25-8c5c11d249fd"; "it"; "21"; "Hotel Sonnschupfer"
"a09f778f-6437-4a15-9eda-656625ecab87"; "3e7a6bc0-56c7-4423-b33f-3f932adf4fa8"; "pt"; "21"; "Hotel Sonnschupfer"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "77e1ee69-7e97-4d7a-b7fc-cd8a49b87551"; "de"; "6"; "Villa Dvor"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "455a8677-e248-42c0-ba93-9c2a7a5f7010"; "en"; "6"; "Villa Dvor"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "3aedff53-03c5-42c9-9ba4-d308e1e50ff9"; "es"; "6"; "Villa Dvor"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "3e65c405-6442-484d-9c53-b11f1bbdec93"; "fr"; "6"; "Villa Dvor"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "4d5930c9-c07b-46da-88e0-6dd1c2619d23"; "it"; "6"; "Villa Dvor"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "35e6de06-ca01-4e0d-95cd-84ea1598f856"; "pt"; "6"; "Villa Dvor"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "2755b1a8-35ce-4d9f-a8ac-aa6ade73ce30"; "de"; "12"; "Hotel Feichtinger Graz"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "1470dc09-a83e-4c30-8524-6d849833946c"; "en"; "12"; "Hotel Feichtinger Graz"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "c22aa8a2-57b2-47d4-b599-4e5eca219a07"; "es"; "12"; "Hotel Feichtinger Graz"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "1dc000bd-de28-4e98-8348-ae66f7998116"; "fr"; "12"; "Hotel Feichtinger Graz"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "5fa305d9-fe8d-491c-bd77-f80aefba3f5e"; "it"; "12"; "Hotel Feichtinger Graz"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "c90271b2-64d2-44c3-93ce-196ff91b816d"; "pt"; "12"; "Hotel Feichtinger Graz"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "74cf6cf4-9f15-4350-81f7-93bb7f1a5597"; "de"; "19"; "Hotel Wasserpalast - breakfast for free!!!"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "83cea878-4426-4b18-b9cb-82df2b1642f0"; "en"; "20"; "Hotel Wasserpalast - breakfast for free!!!"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "184b776a-28ee-48aa-8ce1-bbd34a86f0c3"; "es"; "17"; "Hotel Wasserpalast - breakfast for free!!!"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "0ac172bb-e4f1-4459-b24d-21305ae09f68"; "fr"; "21"; "Hotel Wasserpalast - breakfast for free!!!"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "c9d47d3d-10a5-4a81-ad4a-7427074ae32f"; "it"; "19"; "Hotel Wasserpalast - breakfast for free!!!"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "36a390b7-cb37-4035-a70a-09b65736ce5f"; "pt"; "20"; "Hotel Wasserpalast - breakfast for free!!!"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "6fdbc8ad-91f1-4b7b-8a51-1183a0c4d284"; "de"; "32"; "Hotel Birkenhof"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "3fb95368-1bae-458a-8ddc-265031636453"; "en"; "4"; "Hotel Birkenhof"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "93f89422-95d6-421e-92fe-b8468d62212d"; "es"; "32"; "Hotel Birkenhof"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "290cc083-a3f1-4492-8f21-0df8779cf708"; "fr"; "35"; "Hotel Birkenhof"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "9833f2f1-e6ef-439d-92d4-43e96c7f2fea"; "it"; "33"; "Hotel Birkenhof"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "edb33137-fdb7-41be-9385-016e2584a1ce"; "pt"; "34"; "Hotel Birkenhof"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "5ce1adfc-9ee0-43ac-8d17-003a545a6ff4"; "de"; "5"; "Hotel zum Heiligen Geist"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "b7ab62c2-02a5-4b9e-bbc0-e20a76ccd2b1"; "en"; "5"; "Hotel zum Heiligen Geist"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "1957bd2d-99f6-4eba-aa51-1766e79f4b09"; "es"; "5"; "Hotel zum Heiligen Geist"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "b3bc144b-678d-484b-96e9-8d084b6c12b1"; "fr"; "5"; "Hotel zum Heiligen Geist"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "94503c3a-0e50-4ed6-830d-631cab44ffdf"; "it"; "5"; "Hotel zum Heiligen Geist"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "5b752e11-8dcd-47b1-a49c-7d1bd9b20c49"; "pt"; "5"; "Hotel zum Heiligen Geist"
```

---

Query SQL: SELECT * FROM url_language_status WHERE status <> 'done' ORDER BY url_id , language
Result:
```
"id"; "url_id"; "language"; "status"; "attempts"; "last_error"; "created_at"; "updated_at"
"b3022f80-9d8d-4d33-84fb-ad9b48949574"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "de"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:50:19.907448+01:00"; "2026-05-04 15:50:19.907448+01:00"
"3deeab3a-d4a9-46a3-a56d-d6c43df0513d"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "en"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:43:56.756155+01:00"; "2026-05-04 15:43:56.756155+01:00"
"d0b60e36-6fed-41c0-a848-e4675742a265"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "es"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:47:27.151671+01:00"; "2026-05-04 15:47:27.151671+01:00"
"b6d7a76e-e3be-4180-b3f3-2a7769adb839"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "fr"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:56:54.063263+01:00"; "2026-05-04 15:56:54.063263+01:00"
"0ea671b7-dc03-415a-9a88-ade70ebeaec2"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "it"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:53:47.236182+01:00"; "2026-05-04 15:53:47.236182+01:00"
"2decb8fe-62ae-4f51-89bc-4b7ecf268429"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "pt"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:59:43.522448+01:00"; "2026-05-04 15:59:43.522448+01:00"
"9a92e231-9d4f-462d-9b72-df678418e968"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "de"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:12:01.536011+01:00"; "2026-05-04 16:12:01.536011+01:00"
"9a220171-57b5-4955-ac3e-7525f9478a4f"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "en"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:04:21.137877+01:00"; "2026-05-04 16:04:21.137877+01:00"
"130e38dd-7451-4e07-b219-453b521e8aa3"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "es"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:08:19.858640+01:00"; "2026-05-04 16:08:19.858640+01:00"
"07213102-5045-4767-b73a-9386bd0e7ed5"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "fr"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:20:33.844790+01:00"; "2026-05-04 16:20:33.844790+01:00"
"fd58f87f-f957-4cb4-9443-71bd85896cc5"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "it"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:16:35.281275+01:00"; "2026-05-04 16:16:35.281275+01:00"
"ba3b8d1b-d3dd-41bf-8aca-5f021fef15fd"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "pt"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:24:53.134088+01:00"; "2026-05-04 16:24:53.134088+01:00"
"d9df8af7-86dd-43e5-ba1c-8fffea96581a"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "de"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:13:06.039120+01:00"; "2026-05-04 16:13:06.039120+01:00"
"151872c9-c348-4e64-95ce-3e69917095e6"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "en"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:05:04.818921+01:00"; "2026-05-04 16:05:04.818921+01:00"
"ffd440c3-388b-4161-9e5b-3eba57509770"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "es"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:08:47.213451+01:00"; "2026-05-04 16:08:47.213451+01:00"
"353eaa37-75ed-42ab-ab8e-a2430fa9fd79"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "fr"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:22:11.623336+01:00"; "2026-05-04 16:22:11.623336+01:00"
"52be2bdc-3b29-4b76-a0c7-f048d82233bb"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "it"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:17:51.401038+01:00"; "2026-05-04 16:17:51.401038+01:00"
"1b236ce1-546c-4a46-b688-4cf3d9507302"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "pt"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:25:46.726982+01:00"; "2026-05-04 16:25:46.726982+01:00"
```

---

Query SQL: SELECT uq.id, uq.status, uq.retry_count, uq.languages_completed, uq.languages_failed, uq.last_error, COUNT(DISTINCT h.language)  AS hotels_langs, COUNT(DISTINCT hd.language) AS desc_langs, COUNT(DISTINCT hp.language) AS policies_langs, COUNT(DISTINCT hl.language) AS legal_langs FROM url_queue uq LEFT JOIN hotels h ON uq.id = h.url_id LEFT JOIN hotels_description hd ON uq.id = hd.url_id LEFT JOIN hotels_policies hp    ON uq.id = hp.url_id LEFT JOIN hotels_legal hl ON uq.id = hl.url_id GROUP BY uq.id, uq.status, uq.retry_count, uq.languages_completed, uq.languages_failed, uq.last_error HAVING COUNT(DISTINCT h.language) < 6 OR COUNT(DISTINCT hl.language) < COUNT(DISTINCT h.language) ORDER BY COUNT(DISTINCT h.language) ASC 
Result:
```
"id"; "status"; "retry_count"; "languages_completed"; "languages_failed"; "last_error"; "hotels_langs"; "desc_langs"; "policies_langs"; "legal_langs"
"23d5d037-6088-4e16-be9b-3ff701d2643e"; "error"; "0"; ""; "en,es,de,it,fr,pt"; "Incomplete: 0/6 languages. OK=[] FAILED=['en', 'es', 'de', 'it', 'fr', 'pt']"; "0"; "0"; "0"; "0"
"3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "error"; "0"; ""; "en,es,de,it,fr,pt"; "Incomplete: 0/6 languages. OK=[] FAILED=['en', 'es', 'de', 'it', 'fr', 'pt']"; "0"; "0"; "0"; "0"
"faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "error"; "0"; ""; "en,es,de,it,fr,pt"; "Incomplete: 0/6 languages. OK=[] FAILED=['en', 'es', 'de', 'it', 'fr', 'pt']"; "0"; "0"; "0"; "0"
```

---

Query SQL: 
    -- ── Q8: Overall URL processing status ──────────────────────────────────────
    SELECT status, COUNT(*) AS count, MIN(updated_at) AS oldest, MAX(updated_at) AS newest FROM url_queue GROUP BY status ORDER BY count DESC;
    
Result:
```
"status"; "count"; "oldest"; "newest"
"done"; "11"; "2026-05-04 15:23:17.525046+01:00"; "2026-05-04 16:40:18.507696+01:00"
"error"; "3"; "2026-05-04 15:59:43.774935+01:00"; "2026-05-04 16:25:46.736338+01:00"
```

---

Query SQL: 
    -- Diagnóstico integral de todas las URLs afectadas
    SELECT 
        uq.id, uq.status, uq.retry_count, uq.languages_completed, uq.languages_failed, uq.last_error,
        -- Conteos por tabla
        COUNT(DISTINCT h.language)  AS hotels_langs, COUNT(DISTINCT hd.language) AS desc_langs, COUNT(DISTINCT hp.language) AS policies_langs, COUNT(DISTINCT hl.language) AS legal_langs
    FROM url_queue uq
    LEFT JOIN hotels h          ON uq.id = h.url_id
    LEFT JOIN hotels_description hd ON uq.id = hd.url_id
    LEFT JOIN hotels_policies hp    ON uq.id = hp.url_id
    LEFT JOIN hotels_legal hl       ON uq.id = hl.url_id
    GROUP BY uq.id, uq.status, uq.retry_count, uq.languages_completed, uq.languages_failed, uq.last_error
    HAVING COUNT(DISTINCT h.language) < 6 OR COUNT(DISTINCT hl.language) < COUNT(DISTINCT h.language)
    ORDER BY COUNT(DISTINCT h.language) ASC;
    
Result:
```
"id"; "status"; "retry_count"; "languages_completed"; "languages_failed"; "last_error"; "hotels_langs"; "desc_langs"; "policies_langs"; "legal_langs"
"23d5d037-6088-4e16-be9b-3ff701d2643e"; "error"; "0"; ""; "en,es,de,it,fr,pt"; "Incomplete: 0/6 languages. OK=[] FAILED=['en', 'es', 'de', 'it', 'fr', 'pt']"; "0"; "0"; "0"; "0"
"3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "error"; "0"; ""; "en,es,de,it,fr,pt"; "Incomplete: 0/6 languages. OK=[] FAILED=['en', 'es', 'de', 'it', 'fr', 'pt']"; "0"; "0"; "0"; "0"
"faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "error"; "0"; ""; "en,es,de,it,fr,pt"; "Incomplete: 0/6 languages. OK=[] FAILED=['en', 'es', 'de', 'it', 'fr', 'pt']"; "0"; "0"; "0"; "0"
```

---

Query SQL: 
       -- ── Q1: URLs with missing languages ────────────────────────────────────────
    -- Expected after Build 62: 0 rows.
    -- Run after each batch to confirm all 6 languages are captured.
    SELECT
        uq.id  AS url_id,
        uq.url,
        uq.status,
        COUNT(DISTINCT h.language) AS lang_count,
        STRING_AGG(DISTINCT h.language, ', '
                   ORDER BY h.language) AS languages_present,
        6 - COUNT(DISTINCT h.language)  AS missing_count,
        uq.languages_failed
    FROM url_queue uq
    LEFT JOIN hotels h ON h.url_id = uq.id
    WHERE uq.status IN ('done', 'error')
    GROUP BY uq.id, uq.url, uq.status, uq.languages_failed
    HAVING COUNT(DISTINCT h.language) < 6
    ORDER BY missing_count DESC, uq.updated_at DESC;
    
Result:
```
"url_id"; "url"; "status"; "lang_count"; "languages_present"; "missing_count"; "languages_failed"
"faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "https://www.booking.com/hotel/at/vital-styria.html"; "error"; "0"; "NULL"; "6"; "en,es,de,it,fr,pt"
"3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "https://www.booking.com/hotel/at/steinthron.html"; "error"; "0"; "NULL"; "6"; "en,es,de,it,fr,pt"
"23d5d037-6088-4e16-be9b-3ff701d2643e"; "https://www.booking.com/hotel/at/minihotel-graz.html"; "error"; "0"; "NULL"; "6"; "en,es,de,it,fr,pt"
```

---

Query SQL: 
    SELECT 'hotels_amenities' AS t, COUNT(*) FROM hotels_amenities
    UNION ALL SELECT 'hotels_popular_services', COUNT(*) FROM hotels_popular_services
    UNION ALL SELECT 'hotels_fine_print', COUNT(*) FROM hotels_fine_print
    UNION ALL SELECT 'hotels_all_services', COUNT(*) FROM hotels_all_services
    UNION ALL SELECT 'hotels_faqs', COUNT(*) FROM hotels_faqs
    UNION ALL SELECT 'hotels_guest_reviews', COUNT(*) FROM hotels_guest_reviews
    UNION ALL SELECT 'hotels_property_highlights', COUNT(*) FROM hotels_property_highlights
    UNION ALL SELECT 'image_data', COUNT(*) FROM image_data
    UNION ALL SELECT 'image_downloads', COUNT(*) FROM image_downloads;
    
Result:
```
ERROR SQL: no existe la relación «hotels_amenities»
LINE 2:     SELECT 'hotels_amenities' AS t, COUNT(*) FROM hotels_ame...
                                                          ^

```

---

Query SQL: 
    SELECT event_type, status, count(*) FROM scraping_logs GROUP BY event_type, status ORDER BY count DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
    -- Logs de la última sesión:
    SELECT url_id, language, event_type, status, duration_ms, scraped_at
    FROM scraping_logs
    WHERE scraped_at >= '2026-03-31 22:00:00+00'
    ORDER BY scraped_at DESC
    LIMIT 40;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 2a. Row count per url_id + language, both tables side by side
        SELECT
            a.url_id,
            a.language,
            a.amenities_rows,
            p.popular_rows,
            CASE
                WHEN a.amenities_rows = p.popular_rows THEN 'EQUAL — investigate'
                ELSE                                        'DIFFERENT — OK'
            END AS assessment
        FROM (
            SELECT url_id, language, COUNT(*) AS amenities_rows
            FROM hotels_amenities
            GROUP BY url_id, language
        ) a
        JOIN (
            SELECT url_id, language, COUNT(*) AS popular_rows
            FROM hotels_popular_services
            GROUP BY url_id, language
        ) p USING (url_id, language)
        ORDER BY url_id, language;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 2b. Summary: how many url/language pairs share the exact same count?
        SELECT
            COUNT(*) FILTER (WHERE a_cnt = p_cnt)   AS pairs_equal_count,
            COUNT(*) FILTER (WHERE a_cnt <> p_cnt)  AS pairs_diff_count,
            COUNT(*)                                AS total_pairs
        FROM (
            SELECT
                a.url_id, a.language,
                a.cnt AS a_cnt,
                p.cnt AS p_cnt
            FROM (
                SELECT url_id, language, COUNT(*) AS cnt
                FROM hotels_amenities
                GROUP BY url_id, language
            ) a
            JOIN (
                SELECT url_id, language, COUNT(*) AS cnt
                FROM hotels_popular_services
                GROUP BY url_id, language
            ) p USING (url_id, language)
        ) x;
        -- pairs_equal_count = 78 → strong evidence of cross-contamination
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 3a. Distribution using only confirmed columns
        SELECT
            event_type,
            status,
            COUNT(*)                                AS total,
            ROUND(AVG(duration_ms) / 1000.0, 1)    AS avg_s,
            ROUND(MIN(duration_ms) / 1000.0, 1)    AS min_s,
            ROUND(MAX(duration_ms) / 1000.0, 1)    AS max_s
        FROM scraping_logs
        GROUP BY event_type, status
        ORDER BY total DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 4a. Scrapes over 100 seconds
        SELECT
            url_id,
            language,
            event_type,
            status,
            duration_ms,
            ROUND(duration_ms / 1000.0, 1) AS duration_s,
            scraped_at
        FROM scraping_logs
        WHERE duration_ms > 100000
        ORDER BY duration_ms DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 4b. Per-language duration statistics
        SELECT
            language,
            COUNT(*)                                 AS scrapes,
            ROUND(AVG(duration_ms) / 1000.0, 1)     AS avg_s,
            ROUND(MIN(duration_ms) / 1000.0, 1)     AS min_s,
            ROUND(MAX(duration_ms) / 1000.0, 1)     AS max_s,
            ROUND(STDDEV(duration_ms) / 1000.0, 1)  AS stddev_s
        FROM scraping_logs
        WHERE status = 'done'
        GROUP BY language
        ORDER BY avg_s DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 4c. Timestamp collision risk (WARN-ORM-001, scraped_at as ORM PK)
        SELECT
            scraped_at,
            COUNT(*) AS collision_count
        FROM scraping_logs
        GROUP BY scraped_at
        HAVING COUNT(*) > 1
        ORDER BY collision_count DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 5a. Basic ratio (no column assumptions)
        SELECT
            (SELECT COUNT(*) FROM image_data)       AS total_image_data,
            (SELECT COUNT(*) FROM image_downloads)  AS total_image_downloads,
            ROUND(
                (SELECT COUNT(*) FROM image_downloads)::numeric /
                NULLIF((SELECT COUNT(*) FROM image_data), 0),
            2)                                      AS downloads_per_photo;
        -- Expected: 3.00 (thumb + large + highres)
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
    -- 5b. Download status breakdown — fill in after \d confirms 'status' column
       SELECT status, COUNT(*) FROM image_downloads GROUP BY status ORDER BY count DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        SELECT 'hotels' AS table_name, COUNT(*) AS rows FROM hotels
        UNION ALL SELECT 'hotels_description',          COUNT(*) FROM hotels_description
        UNION ALL SELECT 'hotels_policies',             COUNT(*) FROM hotels_policies
        UNION ALL SELECT 'hotels_legal',                COUNT(*) FROM hotels_legal
        UNION ALL SELECT 'hotels_amenities',            COUNT(*) FROM hotels_amenities
        UNION ALL SELECT 'hotels_popular_services',     COUNT(*) FROM hotels_popular_services
        UNION ALL SELECT 'hotels_fine_print',           COUNT(*) FROM hotels_fine_print
        UNION ALL SELECT 'hotels_all_services',         COUNT(*) FROM hotels_all_services
        UNION ALL SELECT 'hotels_faqs',                 COUNT(*) FROM hotels_faqs
        UNION ALL SELECT 'hotels_guest_reviews',        COUNT(*) FROM hotels_guest_reviews
        UNION ALL SELECT 'hotels_property_highlights',  COUNT(*) FROM hotels_property_highlights
        UNION ALL SELECT 'image_data',                  COUNT(*) FROM image_data
        UNION ALL SELECT 'image_downloads',             COUNT(*) FROM image_downloads
        UNION ALL SELECT 'url_language_status',         COUNT(*) FROM url_language_status
        UNION ALL SELECT 'scraping_logs',               COUNT(*) FROM scraping_logs
        UNION ALL SELECT 'url_queue',                   COUNT(*) FROM url_queue
        ORDER BY table_name;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        SELECT
            tablename,
            pg_size_pretty(
                pg_total_relation_size(schemaname || '.' || tablename)
            ) AS size
        FROM pg_tables
        WHERE tablename LIKE 'scraping_logs%'
        ORDER BY tablename;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- 5a. Resumen global
        SELECT
            event_type,
            status,
            COUNT(*)                            AS total,
            ROUND(AVG(duration_ms)/1000.0, 1)  AS avg_s,
            ROUND(MIN(duration_ms)/1000.0, 1)  AS min_s,
            ROUND(MAX(duration_ms)/1000.0, 1)  AS max_s
        FROM scraping_logs
        GROUP BY event_type, status
        ORDER BY total DESC;
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL:     
        SELECT 'hotels'                     AS table_name, COUNT(*) AS rows FROM hotels
        UNION ALL SELECT 'hotels_description',              COUNT(*) FROM hotels_description
        UNION ALL SELECT 'hotels_policies',                 COUNT(*) FROM hotels_policies
        UNION ALL SELECT 'hotels_legal',                    COUNT(*) FROM hotels_legal
        UNION ALL SELECT 'hotels_fine_print',               COUNT(*) FROM hotels_fine_print
        UNION ALL SELECT 'hotels_all_services',             COUNT(*) FROM hotels_all_services
        UNION ALL SELECT 'hotels_popular_services',         COUNT(*) FROM hotels_popular_services
        UNION ALL SELECT 'hotels_faqs',                     COUNT(*) FROM hotels_faqs
        UNION ALL SELECT 'hotels_guest_reviews',            COUNT(*) FROM hotels_guest_reviews
        UNION ALL SELECT 'hotels_property_highlights',      COUNT(*) FROM hotels_property_highlights
        UNION ALL SELECT 'image_data',                      COUNT(*) FROM image_data
        UNION ALL SELECT 'image_downloads',                 COUNT(*) FROM image_downloads
        UNION ALL SELECT 'url_language_status',             COUNT(*) FROM url_language_status
        UNION ALL SELECT 'scraping_logs',                   COUNT(*) FROM scraping_logs
        UNION ALL SELECT 'url_queue',                       COUNT(*) FROM url_queue
        ORDER BY table_name;
        -- Esperado para 13 URLs x 6 idiomas:
        --   hotels / description / policies / legal / fine_print → 78 filas c/u
        --   url_language_status / scraping_logs                  → 78 filas c/u
        --   url_queue                                            → 13 filas
        --   Tablas variables (all_services, popular_services, faqs,
        --     guest_reviews, property_highlights, image_data, image_downloads) → > 0
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```

---

Query SQL: 
        -- -----------------------------------------------------------------------------
        -- 4. CALIDAD DE DATOS — hotels_popular_services vs hotels_all_services
        --    Valida que popular es subconjunto razonable de all_services
        -- -----------------------------------------------------------------------------
        SELECT
            ps.url_id,
            ps.language,
            COUNT(DISTINCT ps.popular_service)  AS n_popular,
            COUNT(DISTINCT al.service)          AS n_all,
            ROUND(
                COUNT(DISTINCT ps.popular_service)::numeric /
                NULLIF(COUNT(DISTINCT al.service), 0) * 100,
            1) AS pct_popular_de_all
        FROM hotels_popular_services ps
        LEFT JOIN hotels_all_services al
               ON al.url_id = ps.url_id AND al.language = ps.language
        GROUP BY ps.url_id, ps.language
        ORDER BY pct_popular_de_all DESC
        LIMIT 20;
        -- Esperado: n_popular < n_all en la mayoría de casos
        -- pct alto (>100%) indicaría que popular tiene ítems no presentes en all
    
Result:
```
ERROR SQL: transacción abortada, las órdenes serán ignoradas hasta el fin de bloque de transacción

```
