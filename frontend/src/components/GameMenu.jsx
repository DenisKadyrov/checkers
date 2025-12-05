export default function GameMenu({ onSelectMode, currentMode }) {
  return (
    <div className="mb-6 flex gap-4">
      <button
        onClick={() => onSelectMode('friend')}
        className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
          currentMode === 'friend'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        Play vs Friend
      </button>
      <button
        onClick={() => onSelectMode('bot')}
        className={`px-6 py-2 rounded-lg font-semibold transition-colors ${
          currentMode === 'bot'
            ? 'bg-blue-600 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        Play vs Bot (Minimax AI)
      </button>
    </div>
  );
}

