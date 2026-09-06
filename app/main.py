import ast

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.routers import posts, auth
from app.websocket import wsManager

load_dotenv()


app = FastAPI()
app.include_router(posts.router)
app.include_router(auth.router)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

@app.get("/",  response_class=HTMLResponse)
def read_root():
    return HTMLResponse(html)

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(2, ast.literal_eval(data))
#             await websocket.send_text(f"Message text was: {data}")
#     except Exception as e:
#          print(f"WebSocket disconnected normally {e}")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await wsManager.connect(websocket)
    try:
        while True:
            # Wait for any incoming messages from this client
            text = await websocket.receive_text()
            data = ast.literal_eval(text)
            match data['action']:
                case 'new_purchases':
                    ##TODO add to DB new purchases
                    await wsManager.broadcast(f"Client says: {data}")
                case _:
                    print('Unknown actionww',data)
    except ValueError as e:
        print('xxxx',e)
    except WebSocketDisconnect:
        # Clean up the connection if the client disconnects
        wsManager.disconnect(websocket)
        await wsManager.broadcast("A client left the chat")
