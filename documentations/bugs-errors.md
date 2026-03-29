# Bug-1
Note: faltan idiomas, son 6 idiomas a procesar (env.example) 

 
Query SQL: SELECT url_id , count(url_id) FROM hotels GROUP BY url_id
Result: 
```
"url_id"; "count"
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; 6
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; 6
"4a47abd4-e587-4091-b770-2a0ad9280e15"; 6
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; 6
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; 6
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; 6
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; 6
"9196f2c9-d95b-459e-922b-299a2970a88f"; 6
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; 6
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; 6
"d7704d4b-a617-4f66-8424-21c14805159d"; 6
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; 6
```


Query SQL: SELECT url_id , count(url_id) FROM hotels_legal GROUP BY url_id
Result: 
```
"url_id"; "count"
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; 5
"9196f2c9-d95b-459e-922b-299a2970a88f"; 6
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; 6
"d7704d4b-a617-4f66-8424-21c14805159d"; 6
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; 6
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; 6
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; 6
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; 6
```


Query SQL: SELECT url_id , count(url_id) FROM hotels_policies GROUP BY url_id 
Result: 
```
"url_id"; "count"
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; 6
"4a47abd4-e587-4091-b770-2a0ad9280e15"; 6
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; 6
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; 6
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; 6
"9196f2c9-d95b-459e-922b-299a2970a88f"; 6
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; 6
"d7704d4b-a617-4f66-8424-21c14805159d"; 6
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; 6
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; 6
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; 6
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; 6
```


Query SQL: SELECT url_id , count(url_id) FROM hotels_description GROUP BY url_id
Result: 
```
"url_id"; "count"
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; 6
"4a47abd4-e587-4091-b770-2a0ad9280e15"; 6
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; 6
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; 6
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; 6
"9196f2c9-d95b-459e-922b-299a2970a88f"; 6
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; 6
"d7704d4b-a617-4f66-8424-21c14805159d"; 6
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; 6
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; 6
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; 6
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; 6
```

Query SQL: SELECT url_id , language , count(url_id) FROM hotels_description GROUP BY url_id , language
Result: 
```
"url_id"; "language"; "count"
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "de"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "en"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "es"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "fr"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "it"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "pt"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "de"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "en"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "es"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "fr"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "it"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "pt"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "de"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "en"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "es"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "fr"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "it"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "pt"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "de"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "en"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "es"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "fr"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "it"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "pt"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "de"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "en"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "es"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "fr"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "it"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "pt"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "de"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "en"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "es"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "fr"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "it"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "pt"; 1
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; "es"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "de"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "en"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "es"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "fr"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "it"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "pt"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "de"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "en"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "es"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "fr"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "it"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "pt"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "de"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "en"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "es"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "fr"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "it"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "pt"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "de"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "en"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "es"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "fr"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "it"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "pt"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "de"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "en"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "es"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "fr"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "it"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "pt"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "de"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "en"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "es"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "fr"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "it"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "pt"; 1
```


Query SQL: SELECT url_id , language , COUNT(url_id) FROM hotels GROUP BY url_id , language
Result: 
```
"url_id"; "language"; "count"
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "de"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "en"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "es"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "fr"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "it"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "pt"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "de"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "en"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "es"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "fr"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "it"; 1
"4a47abd4-e587-4091-b770-2a0ad9280e15"; "pt"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "de"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "en"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "es"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "fr"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "it"; 1
"5957d3f5-59ef-4ed8-aa3c-e1cd2eae2583"; "pt"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "de"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "en"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "es"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "fr"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "it"; 1
"73e168e3-06d5-4615-9a3b-45fb836b4d15"; "pt"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "de"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "en"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "es"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "fr"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "it"; 1
"85572d7b-3d83-4e48-ae2d-fd478ff660f2"; "pt"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "de"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "en"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "es"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "fr"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "it"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "pt"; 1
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; "es"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "de"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "en"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "es"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "fr"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "it"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "pt"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "de"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "en"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "es"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "fr"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "it"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "pt"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "de"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "en"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "es"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "fr"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "it"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "pt"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "de"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "en"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "es"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "fr"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "it"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "pt"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "de"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "en"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "es"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "fr"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "it"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "pt"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "de"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "en"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "es"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "fr"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "it"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "pt"; 1
```

Query SQL: SELECT url_id , language , COUNT(url_id) FROM hotels_legal GROUP BY url_id , language 
Result: 
```
"url_id"; "language"; "count"
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "de"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "en"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "es"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "fr"; 1
"0d3a7d06-2d69-4d0b-8e03-2b794358977e"; "it"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "de"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "en"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "es"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "fr"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "it"; 1
"9196f2c9-d95b-459e-922b-299a2970a88f"; "pt"; 1
"a12bc041-5341-4f6c-bce9-338f023b7fb8"; "es"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "de"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "en"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "es"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "fr"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "it"; 1
"aeb8a08c-a894-4b14-873b-4eb3c85b49c1"; "pt"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "de"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "en"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "es"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "fr"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "it"; 1
"d7704d4b-a617-4f66-8424-21c14805159d"; "pt"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "de"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "en"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "es"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "fr"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "it"; 1
"e0b37fd7-b906-4e5c-a3fd-1ba839138900"; "pt"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "de"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "en"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "es"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "fr"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "it"; 1
"e448865f-1a25-45bc-9d74-d01a35b9a9f9"; "pt"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "de"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "en"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "es"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "fr"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "it"; 1
"e5698a41-3ffa-4d1d-90fa-854ec5619d99"; "pt"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "de"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "en"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "es"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "fr"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "it"; 1
"e6b53dfb-1304-47cc-bb9e-ac2a4c9c9ecd"; "pt"; 1
```