import { evaluateBoard } from "./evaluateBoard";
import { Chess } from "chess.js";

export const playBestImmediateMoveForBlack = (
  game,
  depth,
  isMaximizingPlayer,
  depthLimit
) => {
  console.log("playBestImmediateMove");
  // we need our base case.. which is if we reach our depth limit... probably the best move so that is goes back up
  if (depth === depthLimit) {
    // we need to go back up the recursive tree at this point
    return;
  }

  const potentialMoves = game.moves();
  console.log("potentialMoves", potentialMoves);
  if (potentialMoves.length === 0) {
    return;
  }

  const moveEvaluations = [];
  let bestMoveEval = 1000;
  let bestMoveIndex = 0;

  for (let i = 0; i < potentialMoves.length; i++) {
    // get board position after the potential move
    const newBoard = new Chess(game.fen());

    // move
    const result = newBoard.move(potentialMoves[i]);

    const evaluation = evaluateBoard(newBoard);
    moveEvaluations.push(evaluation);
    if (evaluation < bestMoveEval) {
      bestMoveEval = evaluation;
      bestMoveIndex = i;
    }
    console.log(`evaluation for move ${i} is ${evaluation} `);
  }

  console.log(moveEvaluations);
  console.log("bestMoveIndex", bestMoveIndex);

  makeAMove(potentialMoves[bestMoveIndex]);
};
