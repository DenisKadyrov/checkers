# Checkers Game with Minimax AI

A full-stack checkers game with a minimax AI bot implementation.

## Features

- 🎮 Play against a friend (local multiplayer)
- 🤖 Play against an AI bot using minimax algorithm with alpha-beta pruning
- ♟️ Full checkers rules implementation:
  - Regular moves
  - Jump captures (mandatory)
  - Multiple jumps
  - King promotion
  - Win condition detection
- 🎨 Modern UI with TailwindCSS
- 🔌 RESTful API backend

## Tech Stack

### Frontend
- React 19
- Vite
- TailwindCSS

### Backend
- Python 3.8+
- FastAPI
- Minimax algorithm with alpha-beta pruning

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional, defaults to `http://localhost:8000`):
```bash
echo "VITE_API_URL=http://localhost:8000" > .env
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## API Endpoints

### `GET /api/init`
Initialize a new game board.

**Response:**
```json
{
  "board": [[...]]
}
```

### `POST /api/move`
Get the bot's move using minimax algorithm.

**Request:**
```json
{
  "board": [[...]],
  "current_player": "black"
}
```

**Response:**
```json
{
  "move": {
    "from": {"row": 2, "col": 1},
    "to": {"row": 3, "col": 2},
    "jumps": []
  },
  "new_board": [[...]],
  "game_over": false,
  "winner": null
}
```

### `POST /api/validate`
Validate a player's move.

**Request:**
```json
{
  "board": [[...]],
  "from_pos": {"row": 5, "col": 2},
  "to_pos": {"row": 4, "col": 3}
}
```

**Response:**
```json
{
  "from_pos": {"row": 5, "col": 2},
  "to_pos": {"row": 4, "col": 3},
  "jumps": [],
  "is_promotion": false,
  "new_board": [[...]],
  "game_over": false,
  "winner": null
}
```

### `POST /api/moves`
Get all available moves for a player.

**Request:**
```json
{
  "board": [[...]],
  "current_player": "white"
}
```

**Response:**
```json
{
  "moves": [
    {
      "from": {"row": 5, "col": 2},
      "to": {"row": 4, "col": 3},
      "jumps": []
    }
  ]
}
```

## Minimax Algorithm

The bot uses a minimax algorithm with alpha-beta pruning to determine the best move. Key features:

- **Depth**: Configurable search depth (default: 4)
- **Evaluation Function**: 
  - Piece values (regular: 10, king: 30)
  - Position bonuses
  - Mobility bonuses
- **Alpha-Beta Pruning**: Optimizes search by pruning unnecessary branches

You can adjust the depth in `backend/game_engine.py`:
```python
DEPTH = 4  # Increase for stronger AI (slower), decrease for faster (weaker)
```

## Game Rules

- Pieces move diagonally on dark squares only
- Regular pieces move forward only (white up, black down)
- Kings can move in all four diagonal directions
- Jump captures are mandatory when available
- Multiple jumps are allowed and must be completed
- Pieces are promoted to kings when reaching the opposite end
- Game ends when a player has no pieces or no valid moves

## Development

### Running Tests

To test the API endpoints, you can use curl:

```bash
# Initialize board
curl http://localhost:8000/api/init

# Get bot move
curl -X POST http://localhost:8000/api/move \
  -H "Content-Type: application/json" \
  -d '{"board": [...], "current_player": "black"}'
```

### Project Structure

```
checkers/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── game_engine.py      # Game logic and minimax AI
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── logic/          # Frontend game logic
│   │   ├── services/       # API service
│   │   └── App.jsx         # Main app component
│   └── package.json        # Node dependencies
└── README.md
```

## License

MIT

