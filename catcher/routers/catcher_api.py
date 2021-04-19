from aiohttp import web

catcher_route = web.RouteTableDef()

@catcher_route.get('/catcher')
async def hello2(request):
    return web.Response(text="Hello, world")
