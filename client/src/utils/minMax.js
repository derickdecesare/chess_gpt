import { evaluateBoard } from "./evaluateBoard";
import { Chess } from "chess.js";

export const minMax = (
  node,
  depth,
  alpha,
  beta,
  isMaximizingPlayer,
  depthLimit
) => {
  if (depth === depthLimit || node.isCheckmate() || node.isDraw()) {
    return { score: evaluateBoard(node), move: null };
  }

  const potentialMoves = node.moves({ verbose: true });

  // Order moves - captures first
  potentialMoves.sort((a, b) => {
    // Prioritize captures
    const isACapture = a.flags.includes("c");
    const isBCapture = b.flags.includes("c");
    if (isACapture !== isBCapture) {
      return isBCapture - isACapture;
    }

    // Prioritize checks
    const isACheck = a.san.includes("+"); // 'san' is the Standard Algebraic Notation property
    const isBCheck = b.san.includes("+");
    if (isACheck !== isBCheck) {
      return isBCheck - isACheck;
    }
  });

  let bestScore = isMaximizingPlayer ? -Infinity : Infinity;
  let bestMove = potentialMoves[0];

  for (let i = 0; i < potentialMoves.length; i++) {
    const newBoard = new Chess(node.fen());
    newBoard.move(potentialMoves[i]);

    // Selective deepening: increase depth for promising moves
    let currentDepthLimit = depthLimit;
    if (
      potentialMoves[i].flags.includes("c") ||
      potentialMoves[i].san.includes("+") ||
      potentialMoves[i].flags.includes("p")
    ) {
      currentDepthLimit += 1; // Search two levels deeper for captures, checks, and promotions
    }

    const result = minMax(
      newBoard,
      depth + 1,
      alpha,
      beta,
      !isMaximizingPlayer,
      depthLimit
    );

    if (isMaximizingPlayer) {
      if (result.score > bestScore) {
        bestScore = result.score;
        bestMove = potentialMoves[i];
      }
      alpha = Math.max(alpha, bestScore);
      if (beta <= alpha) {
        break; // beta cutoff
      }
    } else {
      if (result.score < bestScore) {
        bestScore = result.score;
        bestMove = potentialMoves[i];
      }
      beta = Math.min(beta, bestScore);
      if (beta <= alpha) {
        break; // alpha cutoff
      }
    }
  }

  return {
    score: bestScore,
    move: bestMove,
  };
};
