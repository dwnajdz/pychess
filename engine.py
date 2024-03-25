import asyncio
import websockets
import json

async def handler(websocket):
  while True:
    message = await websocket.recv()
    game = json.loads(message)
    print('game:', game)


async def main():
  print('main running on ws://localhost:3001')
  async with websockets.serve(handler, "", 3001):
    await asyncio.Future()

if __name__ == "__main__":
  asyncio.run(main())

  