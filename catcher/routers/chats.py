from aiohttp import web

chats_route = web.RouteTableDef()


@chats_route.get('/api/chats')
async def get_chats(request):
    return web.Response(text='Hello, world')


@chats_route.post('/api/chats')
async def create_chat(request):
    data = await request.json()
    return web.Response(text='Hello, world')


@chats_route.get('/api/chats/{id}')
async def get_chat(request):
    return web.Response(text='Hello, world')


@chats_route.put('/api/chats/{id}')
async def update_chat(request):
    data = await request.json()
    return web.Response(text='Hello, world')


@chats_route.delete('/api/chats/{id}')
async def delete_chat(request):
    return web.Response(text='Hello, world')
