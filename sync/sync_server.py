import asyncio
import websockets

class SyncServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def run(self):
        self.server = websockets.serve(self.handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(self.server)

    async def consumer(self, msg):
        print(f'< {msg}')

    async def producer(self):
        msg = input(': ')
        return msg

    async def consumer_handler(self, ws, path):
        async for msg in ws:
            await self.consumer(msg)

    async def producer_handler(self, ws, path):
        while True:
            msg = await self.producer()
            await ws.send(msg)

    async def handler(self, ws, path):
        consumer_task = asyncio.ensure_future(self.consumer_handler(ws, path))
        producer_task = asyncio.ensure_future(self.producer_handler(ws, path))
        
        done, pending = await asyncio.wait(
            [consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

if __name__ == '__main__':
    sync_server = SyncServer('localhost', 50001)
    sync_server.run()
    asyncio.get_event_loop().run_forever()