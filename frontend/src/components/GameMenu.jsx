import { useState } from "react";
import Board from "./Board.jsx";

function GameMenu() {
  const [gameStarted, setGameStarted] = useState(false); 
  const [gameMode, setGameMode] = useState(null); 

  const handleStartGame = (mode) => {
    setGameMode(mode);  
    setGameStarted(true); 
  };

 return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      {!gameStarted ? (
        <div className="bg-white p-8 shadow-xl text-center">
          <h1 className="text-3xl font-bold mb-6">ВЫБЕРИТЕ РЕЖИМ</h1>
          <div className="flex justify-center gap-6">
            <button
              className="px-8 py-4 text-xl font-semibold text-white bg-blue-500 rounded-lg hover:bg-blue-600 transform hover:scale-105 transition duration-300"onClick={() => handleStartGame("friend")}>
              Игра с другом
            </button>
            <button className="px-8 py-4 text-xl font-semibold text-white bg-green-500 rounded-lg hover:bg-green-600 transform hover:scale-105 transition duration-300"onClick={() => handleStartGame("bot")}>
              Игра с ботом
            </button>
          </div>
        </div>
      ) : (
        <Board />
      )}
    </div>
  );
}

export default GameMenu;