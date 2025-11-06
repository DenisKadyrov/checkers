import { useState } from 'react'
import Board from './components/Board.jsx'
import initBoard from './logic/board.js'
import { getAvailableMoves, movePiece } from "./logic/moves.js";


export default function App() {
  const [board, setBoard] = useState(initBoard())
  const [selectedCell, setSelectedCell] = useState(null);
  const [availableMoves, setAvailableMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState("white");

  function handleCellClick(row, col) {
    const piece = board[row][col];

    // Выбор фигуры
    if (piece && piece.player === currentPlayer) {
      setSelectedCell({ row, col });
      setAvailableMoves(getAvailableMoves(board, row, col));
      return;
    }

    // Перемещение
    if (selectedCell) {
      const move = availableMoves.find(m => m.row === row && m.col === col);
      if (move) {
        const newBoard = movePiece(board, selectedCell, move);
        setBoard(newBoard);
        setSelectedCell(null);
        setAvailableMoves([]);
        setCurrentPlayer(currentPlayer === "white" ? "black" : "white");
      }
    }
  }

  return (
    <div className="flex flex-col items-center">
      <Board
        board={board}
        selectedCell={selectedCell}
        availableMoves={availableMoves}
        onCellClick={handleCellClick}
      />

    </div >
  );
}