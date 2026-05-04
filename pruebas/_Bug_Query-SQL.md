Query SQL: SELECT url_id , hotel_name, count(language) FROM hotels GROUP BY hotel_name ,url_id
Result:
```
"url_id"; "hotel_name"; "count"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "Hotel Wasserpalast - breakfast for free!!!"; "6"
"6339b88f-3637-4eef-a253-319da5fde794"; "Hotel Mariahilf"; "6"
"6092eab1-6017-473e-916f-46278fd28ddf"; "Haus Mobene - Hotel Garni"; "6"
"a09f778f-6437-4a15-9eda-656625ecab87"; "Hotel Sonnschupfer"; "6"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "Villa Dvor"; "6"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "Sun Lodge Schladming by Schladming-Appartements"; "6"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "Hotel zum Heiligen Geist"; "6"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "Hotel Feichtinger Graz"; "6"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "Hotel Birkenhof"; "6"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "vidimo se"; "6"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "wild & bolz eMotel"; "6"
```

---

Query SQL: SELECT url_id , count(url_id) FROM hotels GROUP BY url_id ORDER BY url_id
Result:
```
"url_id"; "count"
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

Query SQL: SELECT url_id , count(url_id) FROM hotels_legal GROUP BY url_id ORDER BY url_id
Result:
```
"url_id"; "count"
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

Query SQL: SELECT url_id , count(url_id) FROM hotels_policies GROUP BY url_id ORDER BY url_id
Result:
```
"url_id"; "count"
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

Query SQL: SELECT url_id , count(url_id) FROM hotels_description GROUP BY url_id ORDER BY url_id
Result:
```
"url_id"; "count"
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

Query SQL: SELECT url_id , language , count(url_id) FROM hotels_description GROUP BY url_id , language ORDER BY url_id, language
Result:
```
"url_id"; "language"; "count"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "de"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "en"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "es"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "fr"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "it"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "pt"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "de"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "en"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "es"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "fr"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "it"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "pt"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "de"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "en"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "es"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "fr"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "it"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "pt"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "de"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "en"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "es"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "fr"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "it"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "pt"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "de"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "en"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "es"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "fr"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "it"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "pt"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "de"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "en"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "es"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "fr"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "it"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "pt"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "de"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "en"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "es"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "fr"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "it"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "pt"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "de"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "en"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "es"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "fr"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "it"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "pt"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "de"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "en"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "es"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "fr"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "it"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "pt"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "de"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "en"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "es"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "fr"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "it"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "pt"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "de"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "en"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "es"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "fr"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "it"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "pt"; "1"
```

---

Query SQL: SELECT url_id , language , COUNT(url_id) FROM hotels GROUP BY url_id , language ORDER BY url_id, language
Result:
```
"url_id"; "language"; "count"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "de"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "en"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "es"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "fr"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "it"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "pt"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "de"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "en"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "es"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "fr"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "it"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "pt"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "de"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "en"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "es"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "fr"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "it"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "pt"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "de"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "en"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "es"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "fr"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "it"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "pt"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "de"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "en"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "es"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "fr"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "it"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "pt"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "de"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "en"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "es"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "fr"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "it"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "pt"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "de"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "en"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "es"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "fr"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "it"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "pt"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "de"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "en"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "es"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "fr"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "it"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "pt"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "de"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "en"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "es"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "fr"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "it"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "pt"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "de"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "en"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "es"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "fr"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "it"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "pt"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "de"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "en"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "es"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "fr"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "it"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "pt"; "1"
```

---

Query SQL: SELECT url_id , language , COUNT(url_id) FROM hotels_legal GROUP BY url_id , language ORDER BY url_id, language
Result:
```
"url_id"; "language"; "count"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "de"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "en"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "es"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "fr"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "it"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "pt"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "de"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "en"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "es"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "fr"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "it"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "pt"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "de"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "en"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "es"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "fr"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "it"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "pt"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "de"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "en"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "es"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "fr"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "it"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "pt"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "de"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "en"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "es"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "fr"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "it"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "pt"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "de"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "en"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "es"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "fr"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "it"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "pt"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "de"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "en"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "es"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "fr"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "it"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "pt"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "de"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "en"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "es"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "fr"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "it"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "pt"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "de"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "en"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "es"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "fr"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "it"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "pt"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "de"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "en"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "es"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "fr"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "it"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "pt"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "de"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "en"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "es"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "fr"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "it"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "pt"; "1"
```

---

Query SQL: SELECT url_id , language , COUNT(url_id) FROM hotels_description GROUP BY url_id, language ORDER BY url_id, language
Result:
```
"url_id"; "language"; "count"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "de"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "en"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "es"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "fr"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "it"; "1"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "pt"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "de"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "en"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "es"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "fr"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "it"; "1"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "pt"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "de"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "en"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "es"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "fr"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "it"; "1"
"6092eab1-6017-473e-916f-46278fd28ddf"; "pt"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "de"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "en"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "es"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "fr"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "it"; "1"
"6339b88f-3637-4eef-a253-319da5fde794"; "pt"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "de"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "en"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "es"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "fr"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "it"; "1"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "pt"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "de"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "en"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "es"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "fr"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "it"; "1"
"a09f778f-6437-4a15-9eda-656625ecab87"; "pt"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "de"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "en"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "es"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "fr"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "it"; "1"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "pt"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "de"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "en"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "es"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "fr"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "it"; "1"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "pt"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "de"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "en"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "es"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "fr"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "it"; "1"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "pt"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "de"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "en"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "es"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "fr"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "it"; "1"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "pt"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "de"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "en"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "es"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "fr"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "it"; "1"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "pt"; "1"
```

---

Query SQL: SELECT url_id , COUNT(language) FROM hotels_all_services WHERE language ='en' GROUP BY url_id , language
Result:
```
"url_id"; "count"
"81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "6"
"ab8580e9-7036-4824-be01-ab7120c08d01"; "12"
"6339b88f-3637-4eef-a253-319da5fde794"; "16"
"bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "20"
"03a81e7d-a654-4d48-a02e-0dee6f13301d"; "28"
"d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "4"
"ab4a5058-fd28-4eac-960b-b00c37f94b65"; "6"
"286cbdba-a206-41e7-b0a3-41d3a272f78c"; "18"
"a09f778f-6437-4a15-9eda-656625ecab87"; "21"
"fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "5"
"6092eab1-6017-473e-916f-46278fd28ddf"; "13"
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

Query SQL: SELECT * FROM url_language_status ORDER BY url_id , language
Result:
```
"id"; "url_id"; "language"; "status"; "attempts"; "last_error"; "created_at"; "updated_at"
"e857fb1b-fcd9-4bfc-85b1-cb3e2536d357"; "03a81e7d-a654-4d48-a02e-0dee6f13301d"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:28:27.312849+01:00"; "2026-05-04 15:28:27.312849+01:00"
"3ad4ef30-370e-44c2-a2b2-d02842fd9810"; "03a81e7d-a654-4d48-a02e-0dee6f13301d"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:26:18.088681+01:00"; "2026-05-04 15:26:18.088681+01:00"
"8d4dafe8-a940-46ed-b318-083364b9f743"; "03a81e7d-a654-4d48-a02e-0dee6f13301d"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:27:08.742117+01:00"; "2026-05-04 15:27:08.742117+01:00"
"f4ad4aa0-f70e-4c68-9331-e03c018d143a"; "03a81e7d-a654-4d48-a02e-0dee6f13301d"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:31:03.556896+01:00"; "2026-05-04 15:31:03.556896+01:00"
"1e6b2835-18d5-490b-a61d-6befd20ff370"; "03a81e7d-a654-4d48-a02e-0dee6f13301d"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:29:54.930296+01:00"; "2026-05-04 15:29:54.930296+01:00"
"674688a1-06bf-4462-87ac-8f8384a0ff21"; "03a81e7d-a654-4d48-a02e-0dee6f13301d"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:31:57.491176+01:00"; "2026-05-04 15:31:57.491176+01:00"
"b3022f80-9d8d-4d33-84fb-ad9b48949574"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "de"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:50:19.907448+01:00"; "2026-05-04 15:50:19.907448+01:00"
"3deeab3a-d4a9-46a3-a56d-d6c43df0513d"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "en"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:43:56.756155+01:00"; "2026-05-04 15:43:56.756155+01:00"
"d0b60e36-6fed-41c0-a848-e4675742a265"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "es"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:47:27.151671+01:00"; "2026-05-04 15:47:27.151671+01:00"
"b6d7a76e-e3be-4180-b3f3-2a7769adb839"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "fr"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:56:54.063263+01:00"; "2026-05-04 15:56:54.063263+01:00"
"0ea671b7-dc03-415a-9a88-ade70ebeaec2"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "it"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:53:47.236182+01:00"; "2026-05-04 15:53:47.236182+01:00"
"2decb8fe-62ae-4f51-89bc-4b7ecf268429"; "23d5d037-6088-4e16-be9b-3ff701d2643e"; "pt"; "error"; "1"; "All scraping engines failed"; "2026-05-04 15:59:43.522448+01:00"; "2026-05-04 15:59:43.522448+01:00"
"f02f8197-1a71-4d24-bfa5-5c4e87a5e65d"; "286cbdba-a206-41e7-b0a3-41d3a272f78c"; "de"; "done"; "1"; "NULL"; "2026-05-04 16:31:07.795111+01:00"; "2026-05-04 16:31:07.795111+01:00"
"b439be20-34c4-44a5-89ac-260387d36709"; "286cbdba-a206-41e7-b0a3-41d3a272f78c"; "en"; "done"; "1"; "NULL"; "2026-05-04 16:29:27.740497+01:00"; "2026-05-04 16:29:27.740497+01:00"
"9474a315-fed6-4b2c-b57c-51a4fcad2ea3"; "286cbdba-a206-41e7-b0a3-41d3a272f78c"; "es"; "done"; "1"; "NULL"; "2026-05-04 16:30:33.370771+01:00"; "2026-05-04 16:30:33.370771+01:00"
"adef5f8f-b4af-4538-9aa6-67f9ca00b5dd"; "286cbdba-a206-41e7-b0a3-41d3a272f78c"; "fr"; "done"; "1"; "NULL"; "2026-05-04 16:33:23.444941+01:00"; "2026-05-04 16:33:23.444941+01:00"
"37de1ab9-94a6-4a21-9982-b84ec2bf1599"; "286cbdba-a206-41e7-b0a3-41d3a272f78c"; "it"; "done"; "1"; "NULL"; "2026-05-04 16:32:07.484612+01:00"; "2026-05-04 16:32:07.484612+01:00"
"7cba9e95-23e3-413e-9553-f6145857e3f8"; "286cbdba-a206-41e7-b0a3-41d3a272f78c"; "pt"; "done"; "1"; "NULL"; "2026-05-04 16:33:48.124510+01:00"; "2026-05-04 16:33:48.124510+01:00"
"9a92e231-9d4f-462d-9b72-df678418e968"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "de"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:12:01.536011+01:00"; "2026-05-04 16:12:01.536011+01:00"
"9a220171-57b5-4955-ac3e-7525f9478a4f"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "en"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:04:21.137877+01:00"; "2026-05-04 16:04:21.137877+01:00"
"130e38dd-7451-4e07-b219-453b521e8aa3"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "es"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:08:19.858640+01:00"; "2026-05-04 16:08:19.858640+01:00"
"07213102-5045-4767-b73a-9386bd0e7ed5"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "fr"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:20:33.844790+01:00"; "2026-05-04 16:20:33.844790+01:00"
"fd58f87f-f957-4cb4-9443-71bd85896cc5"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "it"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:16:35.281275+01:00"; "2026-05-04 16:16:35.281275+01:00"
"ba3b8d1b-d3dd-41bf-8aca-5f021fef15fd"; "3d8c110f-c133-4e5e-a2e4-e0ff4deb062a"; "pt"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:24:53.134088+01:00"; "2026-05-04 16:24:53.134088+01:00"
"027b4435-f179-4d0f-aea7-8da9076fcc27"; "6092eab1-6017-473e-916f-46278fd28ddf"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:34:44.426604+01:00"; "2026-05-04 15:34:44.426604+01:00"
"d745c813-efbb-42b9-bf37-e50f69f437ff"; "6092eab1-6017-473e-916f-46278fd28ddf"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:33:01.739883+01:00"; "2026-05-04 15:33:01.739883+01:00"
"0d520d68-8bbd-472f-ad1d-8aef18aa899f"; "6092eab1-6017-473e-916f-46278fd28ddf"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:33:40.334967+01:00"; "2026-05-04 15:33:40.334967+01:00"
"6cdfbf72-2027-4468-8aa3-3eae6d2d6941"; "6092eab1-6017-473e-916f-46278fd28ddf"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:36:44.299477+01:00"; "2026-05-04 15:36:44.299477+01:00"
"29f42326-2f10-4302-b578-bc07771a9f00"; "6092eab1-6017-473e-916f-46278fd28ddf"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:35:17.446912+01:00"; "2026-05-04 15:35:17.446912+01:00"
"3ed3a0c8-ef48-4620-a814-c62f7212223b"; "6092eab1-6017-473e-916f-46278fd28ddf"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:37:54.847115+01:00"; "2026-05-04 15:37:54.847115+01:00"
"b40c473e-f914-4f0e-b2fe-edc918e0f1e8"; "6339b88f-3637-4eef-a253-319da5fde794"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:36:18.137109+01:00"; "2026-05-04 15:36:18.137109+01:00"
"31f99c6d-7d27-428b-9c79-7ca4239a5b04"; "6339b88f-3637-4eef-a253-319da5fde794"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:33:38.983588+01:00"; "2026-05-04 15:33:38.983588+01:00"
"189ceadf-331f-4250-8ecd-78ff18667d23"; "6339b88f-3637-4eef-a253-319da5fde794"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:35:06.453937+01:00"; "2026-05-04 15:35:06.453937+01:00"
"4f658a77-a7d5-48eb-b7d4-a4f191e6d96f"; "6339b88f-3637-4eef-a253-319da5fde794"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:38:16.440797+01:00"; "2026-05-04 15:38:16.440797+01:00"
"be1ac2d7-c6b6-4ae9-a40c-903af8cf22b4"; "6339b88f-3637-4eef-a253-319da5fde794"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:37:02.974487+01:00"; "2026-05-04 15:37:02.974487+01:00"
"36195337-ffbd-47ea-b361-f8ed206b1b8f"; "6339b88f-3637-4eef-a253-319da5fde794"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:39:27.046696+01:00"; "2026-05-04 15:39:27.046696+01:00"
"00ed6799-2962-4b77-9c37-74612f0e3aa0"; "81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:20:03.075791+01:00"; "2026-05-04 15:20:03.075791+01:00"
"65a8a308-2df9-4219-ad99-695065ec156b"; "81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:18:26.423745+01:00"; "2026-05-04 15:18:26.423745+01:00"
"442117a1-c1ad-4598-bfc8-02da907bd74c"; "81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:19:33.611137+01:00"; "2026-05-04 15:19:33.611137+01:00"
"aafd3344-9e7c-4d43-86e9-75c58c2e8df7"; "81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:22:46.004842+01:00"; "2026-05-04 15:22:46.004842+01:00"
"6e1ab70c-c470-41f2-9a16-12093a5d4361"; "81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:21:24.116374+01:00"; "2026-05-04 15:21:24.116374+01:00"
"6498f320-45c8-48e8-95a9-799f1661482e"; "81c6dfb4-6b44-4d67-b6fa-80e0049342da"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:23:17.510003+01:00"; "2026-05-04 15:23:17.510003+01:00"
"70e00dd7-d06f-4f4e-bc53-f3fbc2aee89c"; "a09f778f-6437-4a15-9eda-656625ecab87"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:28:05.478341+01:00"; "2026-05-04 15:28:05.478341+01:00"
"b5e7286a-86ef-453b-b0b4-e2abb7648a2e"; "a09f778f-6437-4a15-9eda-656625ecab87"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:25:30.763219+01:00"; "2026-05-04 15:25:30.763219+01:00"
"c5b7a502-d938-40cd-9348-fff245d93dd2"; "a09f778f-6437-4a15-9eda-656625ecab87"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:26:57.162336+01:00"; "2026-05-04 15:26:57.162336+01:00"
"fde573ad-73b6-4c7a-bbd8-f83276393ee4"; "a09f778f-6437-4a15-9eda-656625ecab87"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:29:37.637195+01:00"; "2026-05-04 15:29:37.637195+01:00"
"cb04a190-807c-49b8-b282-02ea1b753970"; "a09f778f-6437-4a15-9eda-656625ecab87"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:28:52.922689+01:00"; "2026-05-04 15:28:52.922689+01:00"
"33feb787-5d34-4c01-a6aa-6efc4005eb88"; "a09f778f-6437-4a15-9eda-656625ecab87"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:30:54.680129+01:00"; "2026-05-04 15:30:54.680129+01:00"
"ad1129ff-f3b5-4a39-9118-ea594d27b7ad"; "ab4a5058-fd28-4eac-960b-b00c37f94b65"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:42:56.445789+01:00"; "2026-05-04 15:42:56.445789+01:00"
"8499a4b1-91a8-4f69-8c41-1e6772789aa5"; "ab4a5058-fd28-4eac-960b-b00c37f94b65"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:40:52.535567+01:00"; "2026-05-04 15:40:52.535567+01:00"
"156afc3a-bd66-4a02-b9da-27ff2d0a1a81"; "ab4a5058-fd28-4eac-960b-b00c37f94b65"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:42:02.554473+01:00"; "2026-05-04 15:42:02.554473+01:00"
"7a2c519f-3f58-45a0-99e0-743847c9f35e"; "ab4a5058-fd28-4eac-960b-b00c37f94b65"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:45:36.864611+01:00"; "2026-05-04 15:45:36.864611+01:00"
"79e1778a-e924-4a49-b0b4-fbf1c86e663d"; "ab4a5058-fd28-4eac-960b-b00c37f94b65"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:44:40.706176+01:00"; "2026-05-04 15:44:40.706176+01:00"
"346d3ec0-8d0f-4f51-afe6-855be732a8b8"; "ab4a5058-fd28-4eac-960b-b00c37f94b65"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:46:55.640162+01:00"; "2026-05-04 15:46:55.640162+01:00"
"f8b73f98-11e6-459d-a29b-189d60d804c8"; "ab8580e9-7036-4824-be01-ab7120c08d01"; "de"; "done"; "1"; "NULL"; "2026-05-04 16:29:18.195347+01:00"; "2026-05-04 16:29:18.195347+01:00"
"a80bbe34-56fa-4304-b180-29eac7f60b37"; "ab8580e9-7036-4824-be01-ab7120c08d01"; "en"; "done"; "1"; "NULL"; "2026-05-04 16:26:54.120107+01:00"; "2026-05-04 16:26:54.120107+01:00"
"319c92d4-8f51-45f6-8f7a-5be531d469a8"; "ab8580e9-7036-4824-be01-ab7120c08d01"; "es"; "done"; "1"; "NULL"; "2026-05-04 16:28:02.914259+01:00"; "2026-05-04 16:28:02.914259+01:00"
"847b2ae9-5c09-4473-b5f9-98ec3400960f"; "ab8580e9-7036-4824-be01-ab7120c08d01"; "fr"; "done"; "1"; "NULL"; "2026-05-04 16:30:53.093272+01:00"; "2026-05-04 16:30:53.093272+01:00"
"ac53b351-a06d-4662-8a41-7e46adf36bac"; "ab8580e9-7036-4824-be01-ab7120c08d01"; "it"; "done"; "1"; "NULL"; "2026-05-04 16:30:00.793262+01:00"; "2026-05-04 16:30:00.793262+01:00"
"d2d03366-d1f6-4edf-8183-79235e6b5ed3"; "ab8580e9-7036-4824-be01-ab7120c08d01"; "pt"; "done"; "1"; "NULL"; "2026-05-04 16:32:00.836402+01:00"; "2026-05-04 16:32:00.836402+01:00"
"dd7ce0a7-3852-464b-91fd-61b82da53e5f"; "bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "de"; "done"; "1"; "NULL"; "2026-05-04 16:37:31.460588+01:00"; "2026-05-04 16:37:31.460588+01:00"
"e2547021-7aec-4aca-a34a-f33841ff4822"; "bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "en"; "done"; "1"; "NULL"; "2026-05-04 16:35:21.277170+01:00"; "2026-05-04 16:35:21.277170+01:00"
"50e1a8f9-29fa-4ca6-84ff-27d83a624059"; "bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "es"; "done"; "1"; "NULL"; "2026-05-04 16:36:30.380079+01:00"; "2026-05-04 16:36:30.380079+01:00"
"8f1b9441-599b-40a2-99aa-3651144a2a72"; "bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "fr"; "done"; "1"; "NULL"; "2026-05-04 16:39:09.844418+01:00"; "2026-05-04 16:39:09.844418+01:00"
"8eec30b9-9edf-487f-89bd-42250c2b3ae6"; "bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "it"; "done"; "1"; "NULL"; "2026-05-04 16:38:08.164455+01:00"; "2026-05-04 16:38:08.164455+01:00"
"44fba6a9-cc21-491e-a6a4-1955e14ea052"; "bb1b79d9-5f8b-408b-9ed8-e14695b0b820"; "pt"; "done"; "1"; "NULL"; "2026-05-04 16:40:18.490921+01:00"; "2026-05-04 16:40:18.490921+01:00"
"b421a0aa-f489-444b-ad31-705bcc36b21a"; "d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "de"; "done"; "1"; "NULL"; "2026-05-04 16:36:59.896495+01:00"; "2026-05-04 16:36:59.896495+01:00"
"3bd2e268-050d-4f68-a1a5-083009850b2b"; "d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "en"; "done"; "1"; "NULL"; "2026-05-04 16:35:09.037786+01:00"; "2026-05-04 16:35:09.037786+01:00"
"067c26bd-4817-41f4-afff-73abae93154c"; "d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "es"; "done"; "1"; "NULL"; "2026-05-04 16:36:10.837200+01:00"; "2026-05-04 16:36:10.837200+01:00"
"bd82b332-eeaa-49e0-abf7-b7c199874534"; "d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "fr"; "done"; "1"; "NULL"; "2026-05-04 16:38:51.135311+01:00"; "2026-05-04 16:38:51.135311+01:00"
"f8f4a098-342d-4542-98ef-c07a13bcf846"; "d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "it"; "done"; "1"; "NULL"; "2026-05-04 16:37:53.560184+01:00"; "2026-05-04 16:37:53.560184+01:00"
"e05fc84f-1084-45bb-9bde-e1ecadd387be"; "d701e6eb-e54e-4e03-bd8e-1474bf4f4c2e"; "pt"; "done"; "1"; "NULL"; "2026-05-04 16:39:35.073811+01:00"; "2026-05-04 16:39:35.073811+01:00"
"d9df8af7-86dd-43e5-ba1c-8fffea96581a"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "de"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:13:06.039120+01:00"; "2026-05-04 16:13:06.039120+01:00"
"151872c9-c348-4e64-95ce-3e69917095e6"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "en"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:05:04.818921+01:00"; "2026-05-04 16:05:04.818921+01:00"
"ffd440c3-388b-4161-9e5b-3eba57509770"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "es"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:08:47.213451+01:00"; "2026-05-04 16:08:47.213451+01:00"
"353eaa37-75ed-42ab-ab8e-a2430fa9fd79"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "fr"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:22:11.623336+01:00"; "2026-05-04 16:22:11.623336+01:00"
"52be2bdc-3b29-4b76-a0c7-f048d82233bb"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "it"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:17:51.401038+01:00"; "2026-05-04 16:17:51.401038+01:00"
"1b236ce1-546c-4a46-b688-4cf3d9507302"; "faa8f35a-0726-4fbe-9c89-8a7be30c7453"; "pt"; "error"; "1"; "All scraping engines failed"; "2026-05-04 16:25:46.726982+01:00"; "2026-05-04 16:25:46.726982+01:00"
"fdb8b6e6-884b-4c2d-90bc-6d955d633ce4"; "fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "de"; "done"; "1"; "NULL"; "2026-05-04 15:20:55.994957+01:00"; "2026-05-04 15:20:55.994957+01:00"
"be5d4e30-eb26-4ce1-9679-e95f8c8a5a5f"; "fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "en"; "done"; "1"; "NULL"; "2026-05-04 15:19:20.449693+01:00"; "2026-05-04 15:19:20.449693+01:00"
"bf3fe43e-881b-411b-8324-6fd958363339"; "fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "es"; "done"; "1"; "NULL"; "2026-05-04 15:19:47.308551+01:00"; "2026-05-04 15:19:47.308551+01:00"
"5ffcccc0-a252-4bb1-b47a-ea8278a4665c"; "fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "fr"; "done"; "1"; "NULL"; "2026-05-04 15:22:58.795567+01:00"; "2026-05-04 15:22:58.795567+01:00"
"7e687b17-6d20-4070-bc2d-ca6deda6b588"; "fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "it"; "done"; "1"; "NULL"; "2026-05-04 15:21:30.267870+01:00"; "2026-05-04 15:21:30.267870+01:00"
"8128a48e-a56a-42fe-aebb-1238cbad5c02"; "fdd7bf92-2095-42e0-a9b7-61b2b2ab6a93"; "pt"; "done"; "1"; "NULL"; "2026-05-04 15:24:13.429141+01:00"; "2026-05-04 15:24:13.429141+01:00"
```

---

Query SQL: 
    -- ── Q8: Overall URL processing status ──────────────────────────────────────
    SELECT
        status,
        COUNT(*) AS count,
        MIN(updated_at) AS oldest,
        MAX(updated_at) AS newest
    FROM url_queue
    GROUP BY status
    ORDER BY count DESC;
    
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
    SELECT event_type, status, count(*)
    FROM scraping_logs
    GROUP BY event_type, status ORDER BY count DESC;
    
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
