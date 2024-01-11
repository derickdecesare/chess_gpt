import React, { useEffect, useState } from "react";
import { Chessboard } from "react-chessboard";
import { Chess } from "chess.js";
import { minMax } from "../../utils/minMax";

// Paths to your sound files
const moveSound = new Audio("/move-self.mp3");
const captureSound = new Audio("/capture.mp3");
const checkSound = new Audio("/move-check.mp3");

export default function Home() {
  const [game, setGame] = useState(new Chess());
  const [isPlayerTurn, setIsPlayerTurn] = useState(true);
  const [whoIsAI, setWhoIsAI] = useState("white");
  const [human, setHuman] = useState("w");

  const gameRef = React.useRef(game);

  // isMaximizingPlayer flips on each layer

  const undoMove = () => {
    console.log("undoing move");
    // Directly call undo on the game instance without creating a new one
    gameRef.current.undo();
    // Update the state to trigger re-rendering; this doesn't change the game object itself
    // But it will make React aware that an update has occurred
    // setGame(new Chess(game.fen()));
    setGame({ ...gameRef.current });
  };

  const handleAIMove = () => {
    // const isMaximizer = whoIsAI === "white" ? true : false;
    console.log("game turn", gameRef.current.turn());
    const isMaximizer = gameRef.current.turn() === "w" ? true : false;
    console.log("isMaximizer", isMaximizer);
    const bestMove = minMax(
      gameRef.current,
      0,
      -Infinity,
      Infinity,
      isMaximizer,
      4
    );
    if (!bestMove.move) {
      if (gameRef.current.isCheckmate()) {
        alert("checkmate");
        return;
      }
      if (gameRef.current.isGameOver()) {
        alert("gameover");
        return;
      }
    }
    makeAMove(bestMove.move);
  };

  const handlePythonAIMove = async () => {
    console.log("handlePythonAIMove");
    const response = await fetch("http://127.0.0.1:8000/next-move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ fen: gameRef.current.fen() }),
    });
    const data = await response.json();
    console.log("data", data);
    const move = data.best_move;
    makeAMove(move);
  };

  const handleStockFishMove = async () => {
    console.log("handleStockFishMove");
    const response = await fetch("http://127.0.0.1:8000/stockfish-next-move", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ fen: gameRef.current.fen() }),
    });
    const data = await response.json();
    console.log("data", data);
    const move = data.best_move;
    makeAMove(move);
  };

  // useEffect(() => {
  //   console.log("potential moves", gameRef.current.moves({ verbose: true }));
  //   if (gameRef.current.turn() !== human) {
  //     setTimeout(() => {
  //       handleAIMove();
  //     }, [200]);
  //   }
  // }, [game]);

  // const makeAMove = (move) => {
  //   console.log("making a move");
  //   const newGame = new Chess(game.fen());
  //   const result = newGame.move(move);

  //   // Check if the move is a capture
  //   if (result && newGame.inCheck()) {
  //     checkSound.play();
  //   } else if (result && result.flags.includes("c")) {
  //     captureSound.play();
  //   } else {
  //     moveSound.play();
  //   }
  //   // const result = game.move(move);
  //   if (result) {
  //     // setGame((prev) => new Chess(prev.fen()));
  //     setGame(newGame);

  //     // check if the game is over or checkmate
  //     if (newGame.isCheckmate()) {
  //       setTimeout(() => alert("Checkmate"), 400);
  //       return;
  //     }
  //     setIsPlayerTurn(!isPlayerTurn); // Toggle the turn
  //   }
  //   return result;
  // };

  const makeAMove = async (move) => {
    console.log("making a move");
    const result = gameRef.current.move(move);

    // Check if the move is a capture
    if (result && gameRef.current.inCheck()) {
      checkSound.play();
    } else if (result && result.flags.includes("c")) {
      captureSound.play();
    } else {
      moveSound.play();
    }

    if (result) {
      // Directly update the state with the same game reference to trigger a re-render
      setGame({ ...gameRef.current });

      // check if the game is over or checkmate
      if (gameRef.current.isCheckmate()) {
        setTimeout(() => alert("Checkmate"), 400);
        return;
      }

      // this is where we are going to make api call the backend to get the eval for the current fen
      console.log("fen", gameRef.current.fen());
      try {
        const evalFromAI = await getEval(gameRef.current.fen());
        console.log("eval", evalFromAI);
      } catch (err) {
        console.log(err);
      }
      setIsPlayerTurn(!isPlayerTurn); // Toggle the turn
    }
    return result;
  };

  const getTest = async () => {
    const response = await fetch(`http://127.0.0.1:8000`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    console.log("data", data);
    return data;
  };

  const getEval = async (fen) => {
    console.log("fetching backend for eval");
    try {
      const response = await fetch(`http://127.0.0.1:8000/evaluate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ fen: fen }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("There was an error fetching the evaluation:", error);
      return null;
    }
  };

  // Function to handle moves. It updates the game state with the new move.
  const onDropPiece = (sourceSquare, targetSquare) => {
    console.log("game turn", gameRef.current.turn());
    setHuman(gameRef.current.turn());
    try {
      console.log("sourceSquare", sourceSquare);
      console.log("targetSquare", targetSquare);
      // Attempt to make a move
      const move = {
        from: sourceSquare,
        to: targetSquare,
        promotion: "q", // Automatically promote to a queen
      };

      const result = makeAMove(move);
      if (result === null) {
        return;
      }

      return true;
    } catch (error) {
      // Handle the error appropriately
      console.error(error);
      return false;
    }
  };

  return (
    <div className="flex flex-col justify-center items-center h-screen">
      <h1 className="text-2xl font-bold mb-4">The Perplexer</h1>
      <div className="flex-row items-center">
        <button
          onClick={handlePythonAIMove}
          className="mb-4 bg-gray-900 hover:text-yellow-100 text-white py-2 px-4 rounded "
        >
          Run min max algo
        </button>
        <button
          onClick={handleStockFishMove}
          className="mb-4 bg-gray-900 hover:text-yellow-100 text-white py-2 px-4 rounded ml-4"
        >
          Stockfish
        </button>
        <button
          onClick={undoMove}
          className="mb-4 bg-gray-900 hover:text-yellow-100 text-white py-2 px-4 rounded ml-4"
        >
          Undo
        </button>
      </div>
      <div className="w-full md:w-1/2 lg:w-1/3 xl:w-1/4">
        <Chessboard
          position={gameRef.current.fen()}
          onPieceDrop={onDropPiece}
          boardOrientation={whoIsAI}
        />
      </div>
    </div>
  );
}
