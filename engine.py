import logging
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

import asyncio
import websockets
import json

import chess
import chess.engine

class ChessGame:
  board: chess.Board | None
  def __init__(self, fen_position: str | None):
    if fen_position == None:
        return
    self.board = chess.Board(fen_position)

  def get_board(self):
    return self.board
  
  def to_uci(self, source, target) -> str:
    # e.g. e3f3
    return f'{source}{target}'

  # TODO    
  def game_result(self):
    return {
      'isLegal': False
    }

  def move(self, source, target) -> str:
    if self.board == None: return 'no-board'
    uci_move = self.to_uci(source, target)
    if self.isLegal(uci_move) == False:
      return 'illegal'

    print('legality:', self.isLegal(uci_move))
    next_move = chess.Move.from_uci(uci_move)
    self.board.push(next_move)

    # TODO detect who won
    if self.board.is_check():
      return 'check'
    elif self.board.is_stalemate():
      return 'stalemate'
    elif self.board.is_insufficient_material():
      return 'no-material'
    return 'moved'

  def isLegal(self, uci_move) -> bool:
    move = chess.Move.from_uci(uci_move)
    return move in self.board.legal_moves

async def handler(websocket):
  global engine
  engine = None
  async for message in websocket:
    game = json.loads(message)
    assert game['old_pos'] != None

    fen_position = game['old_pos']
    source = game['source']
    target = game['target']

    if engine == None:
      engine = ChessGame(fen_position)

    verdict = engine.move(source, target)
    print('verdict:', verdict)
    print('current_board:\n', engine.get_board())

    result = {
      "type": "result",
      "isLegal": verdict != 'illegal',
    }
    await websocket.send(json.dumps(result))


async def main():
  print('main running on ws://localhost:3001')
  async with websockets.serve(handler, "", 3001):
    await asyncio.Future()

if __name__ == "__main__":
  asyncio.run(main())

  