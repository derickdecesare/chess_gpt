# routes.py
from fastapi import APIRouter
from models import ChessPosition, EvaluationResponse  # Import your Pydantic models
from utils import fen_to_grid, denormalize_score, evaluate_board_with_nn, evaluate_board_with_stockfish, min_max, StockfishCounter, get_best_move_stockfish, generate_next_move_with_gpt, polish_pgn
import chess
import io
import random


router = APIRouter()



@router.post("/gpt-next-move")
async def gpt_next_move(position: ChessPosition):
    print("gpt_next_move endpoint hit")
    print("fen", position.fen)
    print("pgn", position.pgn)

    ## Random move for testing
    # board = chess.Board(position.fen)
    # legal_moves = list(board.legal_moves)
    # random_move = random.choice(legal_moves) 
    # return {"best_move": random_move.uci()}

    # add the ;. to the start of the pgn to match format that our nn expects
    formatted_pgn = ";" + polish_pgn(position.pgn) + " " # add a space at the end so it knows to generate next move (only works for black?)
 
    print(f"formatted_pgn-->'{formatted_pgn}'")

    move = generate_next_move_with_gpt(formatted_pgn, position.fen, position.pgn)

    if move is not None:
        return {"best_move": move.uci(), "gpt_move": True}
    else:
        # fallback to random move
        print("!!!!!!Falling back to random move")
        board = chess.Board(position.fen)
        legal_moves = list(board.legal_moves)
        random_move = random.choice(legal_moves) 
        return {"best_move": random_move.uci()}
        # # Fallback to the minimax algorithm if GPT fails
        # depth = 2
        # alpha = -float("inf")
        # beta = float("inf")
        # counter = StockfishCounter()
        # eval_score, best_move = min_max(board, depth, alpha, beta, counter)
        # print(f"Stockfish calls: {counter.calls}")
        # return {"best_move": best_move.uci()}


@router.post("/evaluate")
async def evaluate_position(position: ChessPosition):
    nn_predicted_score = evaluate_board_with_nn(position.fen)
    stockfish_score = evaluate_board_with_stockfish(position.fen)
    

    # Return both predictions
    return EvaluationResponse(neural_net_score=nn_predicted_score, stockfish_score=stockfish_score)


@router.post("/stockfish-next-move")
async def stockfish_next_move(position: ChessPosition):
    # generate a board from the fen
    board = chess.Board(position.fen)
    best_move = get_best_move_stockfish(board.fen())
    return {"best_move": best_move.uci()}



@router.post("/next-move")
async def next_move(position: ChessPosition):
    print("next_move endpoint hit")
    # return e5
    # print("position", position) 
    # position fen='rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'

    # print("position.fen", position.fen)
    # position.fen rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1


    # convert fen to pgn
    # Convert FEN to PGN
    board = chess.Board(position.fen)
    # print("board", board)
    #board r n b q k b n r
    # p p p p p p p p
    # . . . . . . . .
    # . . . . . . . .
    # . . . . P . . .
    # . . . . . . . .
    # P P P P . P P P
    # R N B Q K B N R

    # get all legal moves
    legal_moves = list(board.legal_moves)
    # print("legal_moves", legal_moves)
    # legal_moves [Move.from_uci('g8h6'), Move.from_uci('g8f6'), Move.from_uci('b8c6'), Move.from_uci('b8a6'), Move.from_uci('h7h6'), Move.from_uci('g7g6'), Move.from_uci('f7f6'), Move.from_uci('e7e6'), Move.from_uci('d7d6'), Move.from_uci('c7c6'), Move.from_uci('b7b6'), Move.from_uci('a7a6'), Move.from_uci('h7h5'), Move.from_uci('g7g5'), Move.from_uci('f7f5'), Move.from_uci('e7e5'), Move.from_uci('d7d5

    # select a random legal move
    random_move = random.choice(legal_moves) 
    # print("random_move", random_move)
    # random_move h7h6

    print("random_move.uci()", random_move.uci())


    return {"best_move": random_move.uci()}

   
  

    # need to return a random legal move
    return {"best_move": "e7e5"}
    board = chess.Board(position.fen)
    
    # Check if game is already over
    if board.is_game_over():
        return {"best_move": None}
    
    # Get legal moves using chess library
    legal_moves = list(board.legal_moves)  # Use legal_moves instead of just listing moves
    if not legal_moves:
        return {"best_move": None}
        
    # Select random move and convert to UCI format
    random_move = random.choice(legal_moves)
    return {"best_move": random_move.uci()}
    # generate a board from the fen
    board = chess.Board(position.fen)
    # call min_max on the board
    depth = 2
    alpha = -float("inf")
    beta = float("inf")
    counter = StockfishCounter()
    eval, best_move = min_max(board, depth, alpha, beta, counter)

    print(f"Stockfish calls: {counter.calls}")

    return {"best_move": best_move.uci()}
