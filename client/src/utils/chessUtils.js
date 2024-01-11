// chessUtils.js
import { Chess } from "chess.js";

class ChessGame {
  constructor(fen) {
    this.game = new Chess(fen);
  }

  makeMove(move) {
    const result = this.game.move(move);
    if (result) {
      this.togglePlayerTurn();
    }
    return result;
  }

  getRandomMove() {
    const possibleMoves = this.game.moves();
    if (this.game.isGameOver() || possibleMoves.length === 0) {
      return null;
    }
    const randomIndex = Math.floor(Math.random() * possibleMoves.length);
    return possibleMoves[randomIndex];
  }

  makeRandomMove() {
    const move = this.getRandomMove();
    if (move) {
      this.togglePlayerTurn();
      return this.makeMove(move);
    }
    return null;
  }

  isGameOver() {
    return this.game.isGameOver();
  }

  getFen() {
    return this.game.fen();
  }

  ascii() {
    return this.game.ascii();
  }

  // Additional methods to expose necessary chess.js functionality
  // ...

  // State control methods
  setIsPlayerTurn = (isPlayerTurn) => {
    this.isPlayerTurn = isPlayerTurn;
  };

  togglePlayerTurn = () => {
    this.isPlayerTurn = !this.isPlayerTurn;
  };
}

export default ChessGame;
