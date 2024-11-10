from pydantic import BaseModel

class ChessPosition(BaseModel):
    fen: str # Use FEN representation which is a string
    pgn: str # Use PGN representation which is a string
    

class EvaluationResponse(BaseModel):
    neural_net_score: float
    stockfish_score: float