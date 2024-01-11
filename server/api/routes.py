# routes.py
from fastapi import APIRouter
from models import ChessPosition, EvaluationResponse  # Import your Pydantic models
from utils import fen_to_grid, denormalize_score, evaluate_board_with_nn, evaluate_board_with_stockfish, min_max, StockfishCounter, get_best_move_stockfish
import chess


router = APIRouter()




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
