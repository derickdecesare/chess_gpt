// const pieceValue = {
//   p: 100,
//   n: 280,
//   b: 320,
//   r: 479,
//   q: 929,
//   k: 0, // King's value is not counted as losing the king means losing the game
// };

const pieceValue = {
  p: 100,
  n: 280,
  b: 320,
  r: 479,
  q: 928,
  k: 0, // King's value is not counted as losing the king means losing the game
};
const pstWhite = {
  p: [
    [100, 100, 100, 100, 105, 100, 100, 100],
    [78, 83, 86, 73, 102, 82, 85, 90],
    [7, 29, 21, 44, 40, 31, 44, 7],
    [-17, 16, -2, 15, 14, 0, 15, -13],
    [-26, 3, 10, 9, 6, 1, 0, -23],
    [-22, 9, 5, -11, -10, -2, 3, -19],
    [-31, 8, -7, -37, -36, -14, 3, -31],
    [0, 0, 0, 0, 0, 0, 0, 0],
  ],
  n: [
    [-66, -53, -75, -75, -10, -55, -58, -70],
    [-3, -6, 100, -36, 4, 62, -4, -14],
    [10, 67, 1, 74, 73, 27, 62, -2],
    [24, 24, 45, 37, 33, 41, 25, 17],
    [-1, 5, 31, 21, 22, 35, 2, 0],
    [-18, 10, 13, 22, 18, 15, 11, -14],
    [-23, -15, 2, 0, 2, 0, -23, -20],
    [-74, -23, -26, -24, -19, -35, -22, -69],
  ],
  b: [
    [-59, -78, -82, -76, -23, -107, -37, -50],
    [-11, 20, 35, -42, -39, 31, 2, -22],
    [-9, 39, -32, 41, 52, -10, 28, -14],
    [25, 17, 20, 34, 26, 25, 15, 10],
    [13, 10, 17, 23, 17, 16, 0, 7],
    [14, 25, 24, 15, 8, 25, 20, 15],
    [19, 20, 11, 6, 7, 6, 20, 16],
    [-7, 2, -15, -12, -14, -15, -10, -10],
  ],
  r: [
    [35, 29, 33, 4, 37, 33, 56, 50],
    [55, 29, 56, 67, 55, 62, 34, 60],
    [19, 35, 28, 33, 45, 27, 25, 15],
    [0, 5, 16, 13, 18, -4, -9, -6],
    [-28, -35, -16, -21, -13, -29, -46, -30],
    [-42, -28, -42, -25, -25, -35, -26, -46],
    [-53, -38, -31, -26, -29, -43, -44, -53],
    [-30, -24, -18, 5, -2, -18, -31, -32],
  ],
  q: [
    [6, 1, -8, -104, 69, 24, 88, 26],
    [14, 32, 60, -10, 20, 76, 57, 24],
    [-2, 43, 32, 60, 72, 63, 43, 2],
    [1, -16, 22, 17, 25, 20, -13, -6],
    [-14, -15, -2, -5, -1, -10, -20, -22],
    [-30, -6, -13, -11, -16, -11, -16, -27],
    [-36, -18, 0, -19, -15, -15, -21, -38],
    [-39, -30, -31, -13, -31, -36, -34, -42],
  ],
  k: [
    [4, 54, 47, -99, -99, 60, 83, -62],
    [-32, 10, 55, 56, 56, 55, 10, 3],
    [-62, 12, -57, 44, -67, 28, 37, -31],
    [-55, 50, 11, -4, -19, 13, 0, -49],
    [-55, -43, -52, -28, -51, -47, -8, -50],
    [-47, -42, -43, -79, -64, -32, -29, -32],
    [-4, 3, -14, -50, -57, -18, 13, 4],
    [17, 30, -3, -14, 6, -1, 40, 18],
  ],
};

// incentivizing long castle for black
// const pstWhite = {
//   p: [
//     [200, 200, 200, 200, 205, 200, 200, 200],
//     [78, 83, 86, 73, 102, 82, 85, 90],
//     [7, 29, 21, 44, 40, 31, 44, 7],
//     [-17, 16, -2, 15, 14, 0, 15, -13],
//     [-26, 3, 10, 9, 6, 1, 0, -23],
//     [80, 80, 80, 150, 150, 80, 80, 80],
//     [-31, 8, -7, -37, -36, -14, 3, -31],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
//   n: [
//     [-66, -53, -75, -75, -10, -55, -58, -70],
//     [-3, -6, 100, -36, 4, 62, -4, -14],
//     [10, 67, 1, 74, 73, 27, 62, -2],
//     [24, 24, 45, 37, 33, 41, 25, 17],
//     [-1, 5, 31, 21, 22, 35, 2, 0],
//     [-18, 10, 10, 22, 18, 90, 11, -14],
//     [-23, -15, 2, 0, 2, 0, -23, -20],
//     [-74, -23, -26, -24, -19, -35, -99, -69],
//   ],
//   b: [
//     [-59, -78, -82, -76, -23, -107, -37, -50],
//     [-11, 20, 35, -42, -39, 31, 2, -22],
//     [-9, 39, -32, 41, 52, -10, 28, -14],
//     [25, 17, 20, 34, 26, 25, 15, 10],
//     [13, 10, 17, 23, 17, 16, 0, 7],
//     [14, 25, 24, 15, 8, 25, 20, 15],
//     [19, 20, 11, 6, 7, 6, 20, 16],
//     [-7, 2, -60, -12, -14, -99, -60, -10],
//   ],
//   r: [
//     [35, 29, 33, 4, 37, 33, 56, 50],
//     [80, 80, 80, 80, 80, 80, 80, 80],
//     [19, 35, 28, 33, 45, 27, 25, 15],
//     [0, 5, 16, 13, 18, -4, -9, -6],
//     [-28, -35, -16, -21, -13, -29, -46, -30],
//     [-42, -28, -42, -25, -25, -35, -26, -46],
//     [-53, -38, -31, -26, -29, -43, -44, -53],
//     [-30, -24, -18, -18, 200, -18, -31, -32],
//   ],
//   q: [
//     [6, 1, -8, -104, 69, 24, 88, 26],
//     [14, 32, 60, -10, 20, 76, 57, 24],
//     [-2, 43, 32, 60, 72, 63, 43, 2],
//     [1, -16, 22, 17, 25, 20, -13, -6],
//     [-14, -15, -2, -5, -1, -10, -20, -22],
//     [-30, -6, -13, -11, -16, -11, -16, -27],
//     [-36, -18, 0, -19, -15, -15, -21, -38],
//     [-39, -30, -31, -100, -31, -36, -34, -42],
//   ],
//   k: [
//     [4, 54, 47, -99, -99, 60, 83, -62],
//     [-32, 10, 55, 56, 56, 55, 10, 3],
//     [-62, 12, -57, 44, -67, 28, 37, -31],
//     [-55, 50, 11, -4, -19, 13, 0, -49],
//     [-55, -43, -52, -28, -51, -47, -8, -50],
//     [-47, -42, -43, -79, -64, -32, -29, -32],
//     [-4, 3, -14, -50, -57, -18, 13, 4],
//     [17, 30, 100, -14, 6, -1, 40, 18],
//   ],
// };

// pure perplexity
// const pstWhite = {
//   p: [
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 300],
//     [0, 0, 0, 0, 0, 0, 0, 200],
//     [100, 100, 100, 100, 100, 100, 100, 200],
//     [-31, 8, -7, -37, -36, -14, 3, -31],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
//   n: [
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
//   b: [
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
//   r: [
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
//   q: [
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
//   k: [
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//     [0, 0, 0, 0, 0, 0, 0, 0],
//   ],
// };

// mirror for the pst for black -- both rows and columsn are reversed
const pstBlack = {
  p: [...pstWhite.p].reverse().map((row) => [...row].reverse()),
  n: [...pstWhite.n].reverse().map((row) => [...row].reverse()),
  b: [...pstWhite.b].reverse().map((row) => [...row].reverse()),
  r: [...pstWhite.r].reverse().map((row) => [...row].reverse()),
  q: [...pstWhite.q].reverse().map((row) => [...row].reverse()),
  k: [...pstWhite.k].reverse().map((row) => [...row].reverse()),
  //   k: [
  //     [4, 54, 100, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //     [-99, -99, -99, -99, -99, -99, -99],
  //   ],
};

const pst = {
  w: pstWhite,
  b: pstBlack,
};

export function evaluateBoard(node) {
  // If it's a checkmate, return a very high or low score depending on the player
  if (node.isCheckmate()) {
    // Assign a very high positive value for checkmate in favor of 'w' and negative for 'b'
    return node.turn() === "w" ? -Infinity : Infinity;
  }

  // If it's a draw, return 0 or some other value that reflects the desirability of a draw
  if (
    node.isDraw() ||
    node.isStalemate() ||
    node.isThreefoldRepetition() ||
    node.isInsufficientMaterial()
  ) {
    return 0;
  }

  let value = 0;
  const board = node.board(); // This returns an 8x8 array of the board with values (2 d representation). eg: [[{square: 'a8', type: 'r', color: 'b'},...],...]

  // if there is a piece then we have the object, if not then it is null

  board.forEach((row, i) => {
    row.forEach((piece, j) => {
      // console.log(piece);
      if (piece) {
        // adjust value for pieces on the board
        value += pieceValue[piece.type] * (piece.color === "w" ? 1 : -1);
        // Adjust value based on the piece's square using the PST
        value +=
          pst[piece.color][piece.type][i][j] * (piece.color === "w" ? 1 : -1);
      }
    });
  });

  return value;
}

const logPsts = () => {
  //   console.log(pstWhite);
  console.log(pstBlack.k);
};

logPsts();