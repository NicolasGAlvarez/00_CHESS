def listMoves(game):
   id = game.get('game_id')
   moves = game.get('game_moves')
   current_player = 'white'
   print(f'[{id}] moves:')
   print('-------------------')
   for moveIndex, move in enumerate(moves):
      print(f'[{moveIndex}] {current_player}: {move}')
      current_player = 'black' if current_player == 'white' else 'white'
   print('')


import pandas as pd

csv_path = "./DATA/games.csv"

# Read the dataset.
games_df = pd.read_csv(csv_path, usecols=['id', 'turns', 'moves'])

# Shape of the dataset
games_shape = games_df.shape

# Get the moves in a list for a specific line in the df
#game1 = games_df.iloc[[5]]['moves'].str.split().tolist()
#game1 = game1[0]

game_index = 0
game_id = games_df['id'][game_index]
game_moves = games_df['moves'][game_index].split()
game_data = {'game_id':game_id, 'game_moves':game_moves}

listMoves(game_data)


# Creo un tablero y lo inicializo
from chess import ChessBoard as cb
from chess import Game as gm

try:
   board = cb.ChessBoard()
   board.setupBoard()

   pieces = board.getPieces()

   # Leo jugada por jugada y las ejecuto
   # move = game_moves[0]

   game = gm.Game(board, game_data)
   # While?
   game.play()

   
except Exception as e:
   print(e)