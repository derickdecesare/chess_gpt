#for utility functions or processing data
#utils.py
import os
import torch 
from chess_cnn import ChessCNN
import numpy as np
import chess
import chess.engine

# print("Current working directory:", os.getcwd())

# Load the model
model = ChessCNN()
model.load_state_dict(torch.load("./neural_net/chess_model_state2.pth", map_location=torch.device('cpu')))
model.eval()

def fen_to_grid(fen):
    board = chess.Board(fen)

    # Initialize an empty grid with 12 channels (6 pieces x 2 colors)
    grid = np.zeros((12, 8, 8))

    # Mapping chess pieces to indices in the grid
    piece_indices = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }

    # Iterating over all squares and filling the grid
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece.piece_type
            color_index = 0 if piece.color == chess.WHITE else 1
            combined_index = piece_indices[piece_type] * 2 + color_index
            row, col = divmod(square, 8)
            grid[combined_index, row, col] = 1 if piece.color == chess.WHITE else -1
    
    return grid

def generate_attacked_area_grids(fen):
    board = chess.Board(fen)
    white_attacks = np.zeros((8, 8))
    black_attacks = np.zeros((8, 8))

    for square in range(64):
        row, col = divmod(square, 8)
        if board.is_attacked_by(chess.WHITE, square):
            white_attacks[row, col] = 1
        if board.is_attacked_by(chess.BLACK, square):
            black_attacks[row, col] = -1

    return white_attacks, black_attacks

def generate_turn_grid(turn):
    return np.full((8, 8), 1 if turn == 'w' else -1)

def create_combined_grid(piece_grid, white_attacks, black_attacks, turn_grid):
    return np.vstack((piece_grid, white_attacks[np.newaxis, :, :], black_attacks[np.newaxis, :, :], turn_grid[np.newaxis, :, :]))


def denormalize_score(score):
    return score * (1500 - (-1500)) + (-1500)


def evaluate_board_with_nn(fen):
    piece_grid = fen_to_grid(fen)
    white_attacks, black_attacks = generate_attacked_area_grids(fen)
    turn = 'w' if 'w' in fen.split(' ')[1] else 'b'
    turn_grid = generate_turn_grid(turn)
    grid = create_combined_grid(piece_grid, white_attacks, black_attacks, turn_grid)
    grid_tensor = torch.tensor(grid, dtype=torch.float32).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        prediction = model(grid_tensor)
        score = denormalize_score(prediction.item())
    return score


def evaluate_board_with_stockfish(fen):
    print('stockfish')
    STOCKFISH_PATH="../stockfish-windows-x86-64-avx2.exe"
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        board = chess.Board(fen)
        info = engine.analyse(board, chess.engine.Limit(depth=0))
        score = info["score"].white().score(mate_score=10000)  # Adjust as needed
    return score

def get_best_move_stockfish(fen):
    STOCKFISH_PATH="../stockfish-windows-x86-64-avx2.exe"
    with chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH) as engine:
        board = chess.Board(fen)
        result = engine.play(board, chess.engine.Limit(depth=4))
        best_move = result.move
    return best_move

class StockfishCounter:
    def __init__(self):
        self.calls = 0

def min_max(game: chess.Board, depth: int, alpha: float, beta: float, counter: StockfishCounter):
    if depth == 0 or game.is_game_over():
        counter.calls += 1
        return evaluate_board_with_nn(game.fen()), None
    
    if game.turn == chess.WHITE: # white is maximizing player
        max_eval = -float("inf")
        for move in game.legal_moves:
            game.push(move) # make the simulated move
            eval, _ = min_max(game, depth - 1, alpha, beta, counter) # pass the new board state into min_max recursively
            game.pop() # undo the simulated move
            if eval > max_eval:
                best_move = move
                max_eval = eval
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else: # black is minimizing player
        min_eval = float("inf")
        for move in game.legal_moves:
            game.push(move)
            eval, _= min_max(game, depth - 1, alpha, beta, counter)
            game.pop()
            if eval < min_eval:
                best_move = move
                min_eval = eval
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
    

