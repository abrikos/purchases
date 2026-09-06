from typing import List
from fastapi import  WebSocket


class ConnectionManager:
    def __init__(self):
        # Keep track of active connections
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        print('connecting')
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        print('disconnecting')
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        # Loop through all clients and send the message
        print(f'broadcasting for {len(self.active_connections)}')
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print('Error for broadcasting', e)


# Initialize the manager
wsManager = ConnectionManager()
