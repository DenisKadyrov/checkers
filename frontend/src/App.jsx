import { useState, useEffect } from 'react'
import Board from './components/Board.jsx'
import GameMenu from './components/GameMenu.jsx'
import { getBotMove, validateMove, getAvailableMoves, initBoard as initBoardAPI } from './services/api.js'


export default function App() {
  const [board, setBoard] = useState([])
  const [selectedCell, setSelectedCell] = useState(null);
  const [availableMoves, setAvailableMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState("white");
  const [gameMode, setGameMode] = useState("friend"); // 'friend' or 'bot'
  const [isBotThinking, setIsBotThinking] = useState(false);
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [error, setError] = useState(null);

  // Initialize board from API when mode changes (use API for consistency)
  useEffect(() => {
    initBoardAPI()
      .then((apiBoard) => {
        setBoard(apiBoard);
        setCurrentPlayer('white');
        setGameOver(false);
        setWinner(null);
        setSelectedCell(null);
        setAvailableMoves([]);
      })
      .catch((err) => {
        console.error('Failed to initialize board from API:', err);
        setError('Failed to initialize board. Please check if the backend is running.');
      });
  }, [gameMode]);

  // Load available moves when a piece is selected
  useEffect(() => {
    if (selectedCell && !gameOver) {
      loadAvailableMoves(selectedCell.row, selectedCell.col);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedCell, gameOver]);

  async function loadAvailableMoves(row, col) {
    try {
      // Use backend API for both modes to ensure consistency
      const moves = await getAvailableMoves(board, currentPlayer);
      // Filter moves for the selected piece
      const pieceMoves = moves.filter(
        (move) => move.from.row === row && move.from.col === col
      );
      setAvailableMoves(pieceMoves.map(m => ({ row: m.to.row, col: m.to.col, move: m })));
      setError(null);
    } catch (err) {
      setError(err.message);
      setAvailableMoves([]);
    }
  }

  async function handleCellClick(row, col) {
    if (gameOver || isBotThinking) return;

    const piece = board[row][col];

    // Select piece
    if (piece && piece.player === currentPlayer) {
      setSelectedCell({ row, col });
      setError(null);
      return;
    }

    // Make move
    if (selectedCell) {
      const moveTarget = availableMoves.find(m => m.row === row && m.col === col);
      
      if (moveTarget) {
        try {
          // Use backend API for validation in both modes to ensure consistency
          const moveData = moveTarget.move || {
            from: selectedCell,
            to: { row, col },
          };
          
          const result = await validateMove(board, moveData.from, moveData.to);
          
          // Apply move
          setBoard(result.new_board);
          setSelectedCell(null);
          setAvailableMoves([]);
          
          // Check for game over
          if (result.game_over) {
            setGameOver(true);
            setWinner(result.winner);
          } else if (gameMode === 'bot') {
            // Bot's turn
            setCurrentPlayer('black');
            setIsBotThinking(true);
            
            // Get bot move after a short delay
            setTimeout(async () => {
              try {
                const botResult = await getBotMove(result.new_board, 'black');
                
                if (botResult.move) {
                  setBoard(botResult.new_board);
                }
                
                if (botResult.game_over) {
                  setGameOver(true);
                  setWinner(botResult.winner);
                } else {
                  setCurrentPlayer('white');
                }
              } catch (err) {
                setError(err.message);
                setCurrentPlayer('white'); // Allow player to try again
              } finally {
                setIsBotThinking(false);
              }
            }, 500);
          } else {
            // Friend mode - switch player
            setCurrentPlayer(currentPlayer === "white" ? "black" : "white");
          }
          setError(null);
        } catch (err) {
          setError(err.message);
          setSelectedCell(null);
          setAvailableMoves([]);
        }
      } else {
        // Invalid move - deselect
        setSelectedCell(null);
        setAvailableMoves([]);
      }
    }
  }


  function handleNewGame() {
    // Use API for consistency in both modes
    initBoardAPI()
      .then((apiBoard) => {
        setBoard(apiBoard);
        setCurrentPlayer('white');
        setGameOver(false);
        setWinner(null);
        setSelectedCell(null);
        setAvailableMoves([]);
        setError(null);
      })
      .catch((err) => {
        console.error('Failed to initialize board from API:', err);
        setError('Failed to initialize board. Please check if the backend is running.');
      });
  }

  return (
    <div className="flex flex-col items-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <h1 className="text-4xl font-bold text-gray-800 mb-4">Checkers</h1>
      
      <GameMenu 
        onSelectMode={setGameMode} 
        currentMode={gameMode}
      />

      {error && (
        <div className="mb-4 px-4 py-2 bg-red-100 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {isBotThinking && (
        <div className="mb-4 px-4 py-2 bg-blue-100 text-blue-700 rounded-lg">
          Bot is thinking...
        </div>
      )}

      {gameOver && (
        <div className="mb-4 px-6 py-3 bg-green-100 text-green-800 rounded-lg font-semibold">
          Game Over! Winner: {winner === 'white' ? 'White' : 'Black'}
        </div>
      )}

      <div className="mb-4 text-lg font-semibold text-gray-700">
        Current Player: <span className={currentPlayer === 'white' ? 'text-white' : 'text-black'}>
          {currentPlayer === 'white' ? 'White' : 'Black'}
        </span>
      </div>

      <Board
        board={board}
        selectedCell={selectedCell}
        availableMoves={availableMoves}
        onCellClick={handleCellClick}
      />

      <button
        onClick={handleNewGame}
        className="mt-6 px-6 py-2 bg-gray-700 text-white rounded-lg font-semibold hover:bg-gray-800 transition-colors"
      >
        New Game
      </button>
    </div>
  );
}
