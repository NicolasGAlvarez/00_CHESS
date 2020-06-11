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

game_moves_7 = []
game_moves_6 = []
game_moves_5 = []
game_moves_4 = []
game_moves_3 = []
game_moves_2 = []


for g in games_df['moves']:
    move = g.split()
    for m in move:
        if len(m) == 7:
            game_moves_7.append(m)
        if len(m) == 6:
            game_moves_6.append(m)
        if len(m) == 5:
            game_moves_5.append(m)
        if len(m) == 4:
            game_moves_4.append(m)
        if len(m) == 3:
            game_moves_3.append(m)
        if len(m) == 2:
            game_moves_2.append(m)

moves_count = 50

print('7 chars', len(game_moves_7))
print('6 chars', len(game_moves_6))
print('5 chars', len(game_moves_5))
print('4 chars', len(game_moves_4))
print('3 chars', len(game_moves_3))
print('2 chars', len(game_moves_2))


print('7 chars', game_moves_7[0:moves_count])
print('7 chars', game_moves_6[0:moves_count])
print('7 chars', game_moves_5[0:moves_count])
print('7 chars', game_moves_4[0:moves_count])
print('7 chars', game_moves_3[0:moves_count])
print('7 chars', game_moves_2[0:moves_count])

file = open('moves.txt', 'w')

file.write('7 chars\n')
file.write('--------- \n')
for line in game_moves_7[0:moves_count]:
    file.write(line)
    file.write('\n')

file.write('\n6 chars\n')
file.write('--------- \n')
for line in game_moves_6[0:moves_count]:
    file.write(line)
    file.write('\n')

file.write('\n 5chars\n')
file.write('--------- \n')
for line in game_moves_5[0:moves_count]:
    file.write(line)
    file.write('\n')

file.write('\n4 chars\n')
file.write('--------- \n')
for line in game_moves_4[0:moves_count]:
    file.write(line)
    file.write('\n')

file.write('\n3 chars\n')
file.write('--------- \n')
for line in game_moves_3[0:moves_count]:
    file.write(line)
    file.write('\n')

file.write('\n2 chars\n')
file.write('--------- \n')
for line in game_moves_2[0:moves_count]:
    file.write(line)
    file.write('\n')


file.close()