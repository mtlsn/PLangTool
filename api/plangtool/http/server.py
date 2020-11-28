import asyncio
from aiohttp import web


routes = web.RouteTableDef()
web_runner = None

# use to check text
@routes.post("/check")
async def check_text(request):
    # @to-do validate input
    print(request)
    body = await request.json()

    out = {
        "text":body["text"],
        "warnings": []
    }
    
    return web.json_response(out)

# use to parse and check a website
@routes.get("/check")
async def check_url(request):
    # not implemented
    return web.json_response({"error": "not implemented"})


def init_app(args):   
    app = web.Application()
    app.add_routes(routes)
    app.args = args
    app.web_runner = web.AppRunner(app) 
    return app

async def run(app):
    await app.web_runner.setup()
    await web.TCPSite(app.web_runner, app.args["host"], app.args["port"]).start()

if __name__ == "__main__":
    
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


