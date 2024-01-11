import chess
import chess.pgn
import chess.engine
import sqlite3



# Initialize the chess engine (e.g., Stockfish)
engine = chess.engine.SimpleEngine.popen_uci("C:/Users/deerr/Desktop/HumanChessAI/stockfish-windows-x86-64-avx2.exe")



def process_pgn_file(file_path):
    pgn = open(file_path)
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        board = game.board()
        for move in game.mainline_moves():
            board.push(move)
            fen = board.fen()
            info = engine.analyse(board, chess.engine.Limit(time=0.1))
            score = info['score'].white().score(mate_score=10000)  # Adjust as needed
            bitboard = board_to_bitboard(board)  # Function to convert board to bitboard
            # Process and store fen, bitboard, score in the database

def board_to_bitboard(board):
    bitboards = {}
    for piece_type in chess.PIECE_TYPES:
        for color in [True, False]:  # True for white, False for black
            bitboard = 0
            for square in chess.SQUARES:
                piece = board.piece_at(square) # check if piece in on the square
                if piece and piece.piece_type == piece_type and piece.color == color:
                    bitboard |= 1 << square
            bitboards[(piece_type, color)] = bitboard
    return bitboards


# Call the function with the path to your PGN file
# process_pgn_file("path_to_your_pgn_file")



# def process_first_10_games(file_path, engine, analysis_depth = 10):
#     with open(file_path, 'r') as pgn:
#         position_counter = 0
#         while position_counter < 5:
#             game = chess.pgn.read_game(pgn)
#             if game is None:
#                 break
#             board = game.board()
#             for move in game.mainline_moves():
#                 if position_counter >= 5:
#                     break
#                 board.push(move)
#                 fen = board.fen()
#                 info = engine.analyse(board, chess.engine.Limit(depth=analysis_depth))
#                 score = info['score'].white().score(mate_score=10000)  # Adjust as needed
#                 bitboard = board_to_bitboard(board)
#                 print(f"Index: {position_counter} FEN: {fen}, Score: {score}, Bitboard: {bitboard}")
#                 position_counter += 1
            


# process_first_10_games("C:/Users/deerr/Desktop/HumanChessAI/decompressed_file.pgn", engine, 12)


def process_first_5000_games(file_path, engine, analysis_depth=10):
    # Connect to SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect('chess_games.db')
    cursor = conn.cursor()

    # Create table
    cursor.execute('''CREATE TABLE IF NOT EXISTS evaluations (
                        id INTEGER PRIMARY KEY,
                        fen TEXT,
                        eval REAL,
                        bitboard TEXT)''')

    game_counter = 0
    with open(file_path, 'r') as pgn:
        position_counter = 0
        while game_counter < 5000:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break

            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
                fen = board.fen()
                info = engine.analyse(board, chess.engine.Limit(depth=analysis_depth))
                score = info['score'].white().score(mate_score=10000)
                bitboard = board_to_bitboard(board)

                # Insert data into the database
                cursor.execute("INSERT INTO evaluations (fen, eval, bitboard) VALUES (?, ?, ?)",
                               (fen, score, str(bitboard)))
                if position_counter % 50 == 0:
                    print(f"Game: {game_counter}, Score: {score}")
                position_counter += 1

            game_counter += 1

    # Commit changes and close connection
    conn.commit()
    conn.close()

    engine.quit()

# Call the function with the path to your PGN file
process_first_5000_games("C:/Users/deerr/Desktop/HumanChessAI/decompressed_file.pgn", engine, 12)