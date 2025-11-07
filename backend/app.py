from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from game_engine import CheckersEngine

app = FastAPI(title="Checkers API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class BoardRequest(BaseModel):
    board: List[List[Optional[Dict]]]
    current_player: str


class MoveRequest(BaseModel):
    board: List[List[Optional[Dict]]]
    from_pos: Dict
    to_pos: Dict


class MoveResponse(BaseModel):
    from_pos: Dict
    to_pos: Dict
    jumps: List[List[int]]
    is_promotion: bool
    new_board: List[List[Optional[Dict]]]
    game_over: bool
    winner: Optional[str] = None


class BotMoveResponse(BaseModel):
    move: Optional[Dict] = None
    new_board: List[List[Optional[Dict]]]
    game_over: bool
    winner: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Checkers API", "status": "running"}


@app.get("/api/init")
async def init_board():
    """Initialize a new game board"""
    engine = CheckersEngine()
    board = engine.init_default_board()
    return {"board": board}


@app.post("/api/move")
async def get_bot_move(request: BoardRequest):
    """
    Get bot's move using minimax algorithm.
    Expects current board state and current player.
    """
    try:
        engine = CheckersEngine(request.board)
        
        # Validate board
        if len(request.board) != 8 or any(len(row) != 8 for row in request.board):
            raise HTTPException(status_code=400, detail="Invalid board size")
        
        # Get bot's move (bot always plays as 'black')
        bot_player = request.current_player
        best_move = engine.get_best_move(request.board, bot_player)
        
        if best_move is None:
            # No moves available
            is_over, winner = engine.is_game_over(request.board, bot_player)
            return BotMoveResponse(
                move=None,
                new_board=request.board,
                game_over=is_over,
                winner=winner
            )
        
        # Make the move
        new_board, is_promotion = engine.make_move(request.board, best_move)
        
        # Check if game is over
        opponent = 'white' if bot_player == 'black' else 'black'
        is_over, winner = engine.is_game_over(new_board, opponent)
        
        # Convert jumps to list of lists for JSON serialization
        jumps_list = [[pos[0], pos[1]] for pos in best_move.get('jumps', [])]
        
        return BotMoveResponse(
            move={
                'from': best_move['from'],
                'to': best_move['to'],
                'jumps': jumps_list
            },
            new_board=new_board,
            game_over=is_over,
            winner=winner
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating move: {str(e)}")


@app.post("/api/validate")
async def validate_move(request: MoveRequest):
    """Validate a move and return the new board state"""
    try:
        engine = CheckersEngine(request.board)
        
        # Get all available moves for the piece
        piece = request.board[request.from_pos['row']][request.from_pos['col']]
        if not piece or piece is None:
            raise HTTPException(status_code=400, detail="No piece at from position")
        
        player = piece.get('player')
        if not player:
            raise HTTPException(status_code=400, detail="Invalid piece data")
        all_moves = engine.get_all_moves(player, request.board)
        
        # Check if the requested move is valid
        move_dict = {
            'from': request.from_pos,
            'to': request.to_pos,
            'jumps': []
        }
        
        valid_move = None
        for move in all_moves:
            if (move['from']['row'] == request.from_pos['row'] and
                move['from']['col'] == request.from_pos['col'] and
                move['to']['row'] == request.to_pos['row'] and
                move['to']['col'] == request.to_pos['col']):
                valid_move = move
                break
        
        if not valid_move:
            raise HTTPException(status_code=400, detail="Invalid move")
        
        # Make the move
        new_board, is_promotion = engine.make_move(request.board, valid_move)
        
        # Check if game is over
        opponent = 'black' if player == 'white' else 'white'
        is_over, winner = engine.is_game_over(new_board, opponent)
        
        jumps_list = [[pos[0], pos[1]] for pos in valid_move.get('jumps', [])]
        
        return MoveResponse(
            from_pos=valid_move['from'],
            to_pos=valid_move['to'],
            jumps=jumps_list,
            is_promotion=is_promotion,
            new_board=new_board,
            game_over=is_over,
            winner=winner
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error validating move: {str(e)}")


@app.post("/api/moves")
async def get_available_moves(request: BoardRequest):
    """Get all available moves for the current player"""
    try:
        engine = CheckersEngine(request.board)
        moves = engine.get_all_moves(request.current_player, request.board)
        
        # Convert moves to serializable format
        serialized_moves = []
        for move in moves:
            jumps_list = [[pos[0], pos[1]] for pos in move.get('jumps', [])]
            serialized_moves.append({
                'from': move['from'],
                'to': move['to'],
                'jumps': jumps_list
            })
        
        return {"moves": serialized_moves}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting moves: {str(e)}")
