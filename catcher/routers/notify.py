from aiohttp import web

notify_route = web.RouteTableDef()


@notify_route.post('/api/notify')
async def notify(request):
    data = await request.json()
    return web.Response(text='Hello, world')
