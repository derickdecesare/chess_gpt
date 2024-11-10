#for utility functions or processing data
#utils.py
import os
import torch 
from chess_cnn import ChessCNN
import numpy as np
import chess
import chess.engine
import re

import pickle
from contextlib import nullcontext
# Import your GPT model architecture
from model import GPTConfig, GPT

# Constants
MODEL_DIR = './models'
DEVICE = 'cpu'  # Change to 'cuda' if using a GPU

# Seed and device settings
torch.manual_seed(1337)
if DEVICE == 'cuda':
    torch.cuda.manual_seed(1337)
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# Load the checkpoint
ckpt_path = os.path.join(MODEL_DIR, 'ckpt.pt')
checkpoint = torch.load(ckpt_path, map_location=DEVICE)

# Initialize the model
gptconf = GPTConfig(**checkpoint['model_args'])
model = GPT(gptconf)
model.load_state_dict(checkpoint['model'])
model.eval()
model.to(DEVICE)

# Load the tokenizer from meta.pkl
meta_path = os.path.join(MODEL_DIR, 'meta.pkl')
with open(meta_path, 'rb') as f:
    meta = pickle.load(f)
stoi, itos = meta['stoi'], meta['itos']
encode = lambda s: [stoi[c] for c in s if c in stoi]
decode = lambda l: ''.join([itos[i] for i in l])

# Function to generate the next move
def generate_next_move_with_gpt(game_history, rawFen, rawPgn, max_attempts=5,):
    """
    Generates the next move using the GPT model.
    Tries up to `max_attempts` times to get a legal move.
    If unsuccessful, returns None.
    """

     # Starting temperature and increment
    base_temperature = 0.6
    temperature_increment = 0.1

    for attempt in range(max_attempts):
        # Adjust temperature for this attempt
        temperature = base_temperature + (temperature_increment * attempt)
        # Prepare the input prompt
        prompt = game_history.strip()

        # Encode the prompt
        start_ids = encode(prompt)
        x = torch.tensor(start_ids, dtype=torch.long, device=DEVICE)[None, ...]

        # Generate output
        with torch.no_grad():
            y = model.generate(
                x,
                max_new_tokens=12,  # Adjust as needed
                temperature=temperature, # increased dynamically
                top_k=200
            )
        # Decode the output
        generated_text = decode(y[0].tolist())
        print("generated_text", generated_text)

        # Extract the new move(s)
        new_text = generated_text[len(prompt):].strip()
        print("new_text", new_text)

        # Remove move numbers from new_text
        new_text_no_numbers = re.sub(r'\d+\.\s*', '', new_text)
        print("new_text_no_numbers", new_text_no_numbers)

        # Split the new_text into tokens (potential moves)
        tokens = new_text_no_numbers.split()
        print("Tokens:", tokens)

        # Initialize the board with the given FEN
        board = chess.Board(rawFen)

        # Attempt to parse each token as a move
        for token in tokens:
            move_text = token.strip()
            if not move_text:
                continue

            # Clean up move text by removing annotations like '+' or '#'
            clean_move_text = move_text.rstrip('+#')
            print("Trying move:", clean_move_text)

            # Skip the move if it's too short to be valid # probably implement some regex here to check if it's a valid looking move to further eliminate fragments like -O since that is two characters but is a fragment..
            if len(clean_move_text) < 2:
                print(f"Move '{clean_move_text}' is too short to be valid. Skipping.")
                continue

            # Validate the move
            try:
                move = board.parse_san(clean_move_text)
                if move in board.legal_moves:
                    print("Found legal move -- returning:", move)
                    return move  # Return the valid move
                else:
                    print(f"Move '{clean_move_text}' is not legal in the current position.")
            except Exception as e:
                print(f"Error parsing move '{clean_move_text}': {e}")
                break  # We don't want to try the next token.. 

        # If no valid move found in this attempt, proceed to the next attempt
        print("No valid move found in this attempt. Retrying...")
        # increase temperature for next attempt
        temperature += temperature_increment
        print("new_temperature", temperature)

    # Return None if no valid move is found after max_attempts
    print("Exceeded maximum attempts. No valid move found.")
    return None


    #     # Use regex to extract the first move after the prompt
    #     # This accounts for possible move numbers and annotations
    #     move_match = re.match(r'^(\d+\.\s*)?([^\s]+)', new_text)
    #     if move_match:
    #         move_text = move_match.group(2).strip()
    #         print("Extracted move:", move_text)
    #     else:
    #         print("No move found in generated text.")
    #         continue  # Try the next attempt

    #     # Initialize the board with the given FEN
    #     board = chess.Board(rawFen)

    #     # Remove any move numbers from move_text (e.g., '2.Nf3' -> 'Nf3')
    #     clean_move_text = re.sub(r'^\d+\.(\s*)', '', move_text)

    #     # Validate and return the move
    #     try:
    #         # Try applying the generated move
    #         print("Trying move:", clean_move_text)
    #         move = board.parse_san(clean_move_text)
    #         if move in board.legal_moves:
    #             print("Found legal move -- returning:", move)
    #             return move  # Return the valid move
    #         else:
    #             print(f"Move '{clean_move_text}' is not legal in the current position.")
    #     except Exception as e:
    #         print(f"Error parsing move '{clean_move_text}': {e}")
    #         continue  # Try the next attempt

    # # Return None if no valid move is found
    # return None

# print("Current working directory:", os.getcwd())

# # Load the model (CNN)
# model = ChessCNN()
# model.load_state_dict(torch.load("./neural_net/chess_model_state2.pth", map_location=torch.device('cpu')))
# model.eval()

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
        return evaluate_board_with_stockfish(game.fen()), None
    
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
    



def polish_pgn(pgn):
    """
    Remove spaces after move numbers in the PGN to match the expected format.
    """
    import re
    # Replace patterns like '1. e4' with '1.e4'
    polished_pgn = re.sub(r'(\d+)\.\s+', r'\1.', pgn)
    return polished_pgn