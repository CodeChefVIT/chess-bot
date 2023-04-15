'''Program to generate and save the data from pgn to npz'''
import os 
import chess
import chess.pgn
import chess.engine
from stockfish import Stockfish
import numpy as np

STOCKFISH = Stockfish(r"/home/tarran_sid/github/chess-ai/stockfish_15.1_linux_x64_popcnt/stockfish_15.1_linux_x64_popcnt/stockfish-ubuntu-20.04-x86-64-modern")
STOCKFISH.set_depth(1)#How deep the AI looks
STOCKFISH.set_skill_level(20)#Highest rank stockfish

def serialize(x): #pylint: disable=invalid-name
    '''Function creates the dataset'''
    assert x.is_valid()
    bstate = np.zeros(64, np.uint8)
    for i in range(64):
        pp = x.piece_at(i) #pylint: disable=invalid-name
        if pp is not None:
            bstate[i] = {"P": 1, "N": 2, "B": 3, "R": 4, "Q": 5, "K": 6, \
                         "p": 9, "n":10, "b":11, "r":12, "q":13, "k": 14}[pp.symbol()]
    if x.has_queenside_castling_rights(chess.WHITE):
        assert bstate[0] == 4
        bstate[0] = 7
    if x.has_kingside_castling_rights(chess.WHITE):
        assert bstate[7] == 4
        bstate[7] = 7
    if x.has_queenside_castling_rights(chess.BLACK):
        assert bstate[56] == 8+4
        bstate[56] = 8+7
    if x.has_kingside_castling_rights(chess.BLACK):
        assert bstate[63] == 8+4
        bstate[63] = 8+7
    if x.ep_square is not None:
        assert bstate[x.ep_square] == 0
        bstate[x.ep_square] = 8
    bstate = bstate.reshape(8, 8)
    # binary state
    state = np.zeros((5, 8, 8), np.uint8)
    # 0-3 columns to binary
    state[0] = (bstate>>3)&1
    state[1] = (bstate>>2)&1
    state[2] = (bstate>>1)&1
    state[3] = (bstate>>0)&1
    # 4th column is who's turn it is
    state[4] = (x.turn*1.0)
    # 257 bits according to readme
    return state
  
def get_dataset(num_samples):
    '''Function to generate the dataset'''
    X, y = [], [] #pylint: disable=invalid-name
    gn = 0 #pylint: disable=invalid-name
    values = {'1/2-1/2':0, '0-1':-1, '1-0':1}
    for fn in os.listdir("dataset"): #pylint: disable=invalid-name
        pgn = open(os.path.join("dataset", fn))
        while 1:
            try:
                game = chess.pgn.read_game(pgn)
            except Exception:
                continue    
            if game is None:
                break
            result = game.headers['Result']
            if result not in values:
                continue
            board = game.board()
            for moves in enumerate(game.mainline_moves()):
                move = moves[1] 
                board.push(move)
                STOCKFISH.set_fen_position(board.fen()) 
                score = STOCKFISH.get_evaluation()
                ser = serialize(board)
                X.append(ser)
                y.append(score['value'])
            print("Parsing game %d got %d examples" %(gn, len(X)))
            if num_samples is not None and len(X) > num_samples:
                return X, y
            gn += 1 #pylint: disable=invalid-name
    X = np.array(X) #pylint: disable=invalid-name
    y = np.array(y) #pylint: disable=invalid-name
    return X, y

def save_output():
    '''Function saves the output as npz file'''
    data_x, data_y = get_dataset(100000)
    np.savez("dataset_processed.npz", data_x, data_y)

save_output()
