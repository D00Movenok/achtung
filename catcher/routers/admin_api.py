from aiohttp import web

admin_route = web.RouteTableDef()

@admin_route.get('/admin')
async def hello1(request):
    return web.Response(text="Hello, world")
