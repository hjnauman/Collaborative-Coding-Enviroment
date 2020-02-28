import websockets
import asyncio

class SyncClient:
    def __init__(self, host, port):
        self.uri = f'ws://{host}:{port}'

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.connect())

        tasks = [
            asyncio.ensure_future(client.heartbeat()),
            asyncio.ensure_future(client.receive_message()),
        ]

        asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))

    async def connect(self):
        '''
        Connecting to webSocket server. Sets self.connection to the WebSocketClientProtocol, which is used to
        send and receive messages.
        '''

        self.connection = await websockets.client.connect(self.uri)

        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            await self.send_message('Hey server, this is webSocket client')


    async def send_message(self, msg):
        '''
        Sends the given message to the websocket server.
        '''

        await self.connection.send(msg)

    async def receive_message(self):
        '''
        Receives and handles all messages from the websocket server.
        '''

        while True:
            try:
                message = await self.connection.recv()
                print('Received message from server: ' + str(message))
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def heartbeat(self):
        '''
        Sends a heartbeat ping to the server every 5 seconds to verify if
        the connection is still alive.
        '''
        while True:
            try:
                await self.connection.send('ping')
                await asyncio.sleep(5)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

if __name__ == '__main__':
    client = SyncClient('localhost', 50001)
    client.run()