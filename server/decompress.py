import zstandard as zstd


# # Define the path to your .pgn.zst file
# file_path = "C:/Users/deerr/Downloads/lichess_db_standard_rated_2023-11.pgn.zst"

# # Function to decompress and read a part of the file
# def read_part_of_pgn_zst(file_path, max_lines=100):
#     with open(file_path, 'rb') as compressed_file:
#         dctx = zstd.ZstdDecompressor()
#         with dctx.stream_reader(compressed_file) as reader:
#             # Set up a buffer for reading lines
#             buffer = ''
#             for _ in range(max_lines):
#                 # Read until we find a newline character
#                 while '\n' not in buffer:
#                     buffer += reader.read(64).decode('utf-8')  # Read in small chunks
#                 line, buffer = buffer.split('\n', 1)
#                 print(line)

# # Call the function to read and print part of the file
# read_part_of_pgn_zst(file_path)

def decompress_zst_to_pgn(zst_file_path, output_pgn_file_path):
    with open(zst_file_path, 'rb') as compressed_file:
        dctx = zstd.ZstdDecompressor()
        with open(output_pgn_file_path, 'wb') as decompressed_file:
            dctx.copy_stream(compressed_file, decompressed_file)
            print(f"Decompressed file saved to {output_pgn_file_path}")

# Define the path to your .pgn.zst file and the output path for the decompressed .pgn file
zst_file_path = "C:/Users/deerr/Downloads/lichess_db_standard_rated_2023-11.pgn.zst"
output_pgn_file_path = "C:/Users/deerr/Desktop/HumanChessAI/decompressed_file.pgn"


# Decompress the file
decompress_zst_to_pgn(zst_file_path, output_pgn_file_path)


