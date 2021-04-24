from aiohttp import web

notifiers_route = web.RouteTableDef()


@notifiers_route.get('/api/notifiers')
async def get_notifiers(request):
    return web.Response(text='Hello, world')


@notifiers_route.post('/api/notifiers')
async def create_notifier(request):
    data = await request.json()
    return web.Response(text='Hello, world')


@notifiers_route.get('/api/notifiers/{id}')
async def get_notifier(request):
    return web.Response(text='Hello, world')


@notifiers_route.put('/api/notifiers/{id}')
async def update_notifier(request):
    data = await request.json()
    return web.Response(text='Hello, world')


@notifiers_route.delete('/api/notifiers/{id}')
async def delete_notifier(request):
    return web.Response(text='Hello, world')
