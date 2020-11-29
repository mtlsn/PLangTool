import asyncio
from aiohttp import web
import aiohttp_cors
from plangtool.core.nlp import *

routes = web.RouteTableDef()
web_runner = None

## routes 
# use to check text
@routes.post("/check")
async def check_text(request):
    # @to-do validate input
    body = await request.json()
    blocks = body["blocks"]

    out = []
    for block in blocks:
        result = {"warnings":[]}
        text = block["data"]["text"]
        word_count = sentence_length(text)
        result["word_count"] = word_count
        if len(word_count) > 1:
            result["warnings"].append({"msg":"Mehrere Sätze in einer Zeile", "code":"more_than_one_sentence"})
        if word_count[0] > 7:
            result["warnings"].append({"msg":"Satz zu lang", "code":"long_sentence"})
        result["words"] = check_words(text)
        out.append(result)

    response = {
        "in":body,
        "out":out
    }
    
    return web.json_response(response)

# use to parse and check a website
@routes.get("/check")
async def check_url(request):
    # not implemented
    return web.json_response({"error": "not implemented"})


def init_app(args):   
    app = web.Application()
    app.add_routes(routes)
    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    # Configure CORS on all routes.
    for route in list(app.router.routes()):
        cors.add(route)

    app.args = args
    app.web_runner = web.AppRunner(app) 
    return app

async def run(app):
    await app.web_runner.setup()
    await web.TCPSite(app.web_runner, app.args["host"], app.args["port"]).start()

def main():
    # @to-do parse cli
    args = {
        "host":"127.0.0.1",
        "port": 7001
    }

    app = init_app(args)

    # start loop
    loop = asyncio.get_event_loop()
    loop.create_task(run(app))

    print('started server on %s:%s' % (args["host"], args["port"]))

    try:
        loop.run_forever()
    except:
        pass
    finally:
        loop.run_until_complete(app.web_runner.cleanup())


if __name__ == "__main__":
    main()
    
  
