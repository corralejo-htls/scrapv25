
===  BookingScraper API  ===

←[32mINFO←[0m:     Started server process [←[36m11852←[0m]
←[32mINFO←[0m:     Waiting for application startup.
{"time":"2026-03-13T00:58:08","level":"INFO","logger":"app.main","msg":Starting BookingScraper Pro v6.0.0 build 49 | platform=win32}
{"time":"2026-03-13T00:58:08","level":"INFO","logger":"app.database","msg":Database engine created: host=localhost db=bookingscraper pool_size=10 max_overflow=5}
←[32mINFO←[0m:     Application startup complete.
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     127.0.0.1:54782 - "←[1mGET /docs HTTP/1.1←[0m" ←[32m200 OK←[0m
←[32mINFO←[0m:     127.0.0.1:54782 - "←[1mGET /openapi.json HTTP/1.1←[0m" ←[32m200 OK←[0m
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 1151, in emit
    msg = self.format(record)
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 999, in format
    return fmt.format(record)
           ~~~~~~~~~~^^^^^^^^
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 712, in format
    record.message = record.getMessage()
                     ~~~~~~~~~~~~~~~~~^^
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 400, in getMessage
    msg = msg % self.args
          ~~~~^~~~~~~~~~~
TypeError: not all arguments converted during string formatting
Call stack:
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\__main__.py", line 4, in <module>
    uvicorn.main()
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 1485, in __call__
    return self.main(*args, **kwargs)
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 1406, in main
    rv = self.invoke(ctx)
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 1269, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 824, in invoke
    return callback(*args, **kwargs)
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\main.py", line 410, in main
    run(
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\main.py", line 577, in run
    server.run()
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\server.py", line 65, in run
    return asyncio.run(self.serve(sockets=sockets))
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\runners.py", line 204, in run
    return runner.run(main)
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\runners.py", line 127, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\base_events.py", line 706, in run_until_complete
    self.run_forever()
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\base_events.py", line 677, in run_forever
    self._run_once()
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\base_events.py", line 2046, in _run_once
    handle._run()
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\events.py", line 94, in _run
    self._context.run(self._callback, *self._args)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\middleware\base.py", line 141, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 714, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 734, in app
    await route.handle(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 288, in handle
    await self.app(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 76, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 73, in app
    response = await f(request)
  File "C:\BookingScraper\.venv\Lib\site-packages\fastapi\routing.py", line 301, in app
    raw_response = await run_endpoint_function(
  File "C:\BookingScraper\.venv\Lib\site-packages\fastapi\routing.py", line 212, in run_endpoint_function
    return await dependant.call(**values)
  File "C:\BookingScraper\app\main.py", line 690, in load_urls_csv
    logger.info(
Message: 'load-csv completado — insertadas: {}  external_ref actualizado: {}  sin cambios: {}  invalidas: {}'
Arguments: (35, 0, 0, 0)
--- Logging error ---
Traceback (most recent call last):
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\handlers.py", line 79, in emit
    if self.shouldRollover(record):
       ~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\handlers.py", line 207, in shouldRollover
    msg = "%s\n" % self.format(record)
                   ~~~~~~~~~~~^^^^^^^^
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 999, in format
    return fmt.format(record)
           ~~~~~~~~~~^^^^^^^^
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 712, in format
    record.message = record.getMessage()
                     ~~~~~~~~~~~~~~~~~^^
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\logging\__init__.py", line 400, in getMessage
    msg = msg % self.args
          ~~~~^~~~~~~~~~~
TypeError: not all arguments converted during string formatting
Call stack:
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\__main__.py", line 4, in <module>
    uvicorn.main()
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 1485, in __call__
    return self.main(*args, **kwargs)
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 1406, in main
    rv = self.invoke(ctx)
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 1269, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\BookingScraper\.venv\Lib\site-packages\click\core.py", line 824, in invoke
    return callback(*args, **kwargs)
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\main.py", line 410, in main
    run(
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\main.py", line 577, in run
    server.run()
  File "C:\BookingScraper\.venv\Lib\site-packages\uvicorn\server.py", line 65, in run
    return asyncio.run(self.serve(sockets=sockets))
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\runners.py", line 204, in run
    return runner.run(main)
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\runners.py", line 127, in run
    return self._loop.run_until_complete(task)
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\base_events.py", line 706, in run_until_complete
    self.run_forever()
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\base_events.py", line 677, in run_forever
    self._run_once()
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\base_events.py", line 2046, in _run_once
    handle._run()
  File "C:\Users\SA\AppData\Local\Programs\Python\Python314\Lib\asyncio\events.py", line 94, in _run
    self._context.run(self._callback, *self._args)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\middleware\base.py", line 141, in coro
    await self.app(scope, receive_or_disconnect, send_no_error)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\middleware\exceptions.py", line 62, in __call__
    await wrap_app_handling_exceptions(self.app, conn)(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 714, in __call__
    await self.middleware_stack(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 734, in app
    await route.handle(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 288, in handle
    await self.app(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 76, in app
    await wrap_app_handling_exceptions(app, request)(scope, receive, send)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\_exception_handler.py", line 42, in wrapped_app
    await app(scope, receive, sender)
  File "C:\BookingScraper\.venv\Lib\site-packages\starlette\routing.py", line 73, in app
    response = await f(request)
  File "C:\BookingScraper\.venv\Lib\site-packages\fastapi\routing.py", line 301, in app
    raw_response = await run_endpoint_function(
  File "C:\BookingScraper\.venv\Lib\site-packages\fastapi\routing.py", line 212, in run_endpoint_function
    return await dependant.call(**values)
  File "C:\BookingScraper\app\main.py", line 690, in load_urls_csv
    logger.info(
Message: 'load-csv completado — insertadas: {}  external_ref actualizado: {}  sin cambios: {}  invalidas: {}'
Arguments: (35, 0, 0, 0)
←[32mINFO←[0m:     127.0.0.1:56340 - "←[1mPOST /urls/load-csv HTTP/1.1←[0m" ←[32m200 OK←[0m
