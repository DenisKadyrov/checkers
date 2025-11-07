"""
Checkers game engine with minimax AI
"""
from typing import List, Tuple, Optional, Dict
from copy import deepcopy


class CheckersEngine:
    """Complete checkers game engine with minimax algorithm"""
    
    BOARD_SIZE = 8
    DEPTH = 4  # Minimax depth
    
    def __init__(self, board: Optional[List[List]] = None):
        """Initialize game engine with a board state"""
        if board is None:
            self.board = self._init_board()
        else:
            self.board = board
    
    def _init_board(self) -> List[List]:
        """Initialize empty 8x8 board"""
        return [[None for _ in range(8)] for _ in range(8)]
    
    def init_default_board(self) -> List[List]:
        """Initialize board with default piece positions"""
        board = self._init_board()
        # Black pieces (top 3 rows)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = {'player': 'black', 'isKing': False}
        # White pieces (bottom 3 rows)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = {'player': 'white', 'isKing': False}
        return board
    
    def _is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def _is_dark_square(self, row: int, col: int) -> bool:
        """Check if square is dark (playable)"""
        return (row + col) % 2 == 1
    
    def get_all_moves(self, player: str, board: Optional[List[List]] = None) -> List[Dict]:
        """
        Get all possible moves for a player, including jumps.
        Returns list of moves: [{'from': (r, c), 'to': (r, c), 'jumps': [(r, c), ...]}]
        """
        if board is None:
            board = self.board
        
        moves = []
        jumps = []
        
        # First, check for forced jumps
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = board[row][col]
                if piece and piece is not None and piece.get('player') == player:
                    piece_jumps = self._get_jumps(board, row, col, player)
                    jumps.extend(piece_jumps)
        
        # If there are jumps, they are mandatory
        if jumps:
            return jumps
        
        # Otherwise, return regular moves
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = board[row][col]
                if piece and piece is not None and piece.get('player') == player:
                    piece_moves = self._get_regular_moves(board, row, col, player)
                    moves.extend(piece_moves)
        
        return moves
    
    def _get_regular_moves(self, board: List[List], row: int, col: int, player: str) -> List[Dict]:
        """Get regular (non-jump) moves for a piece"""
        piece = board[row][col]
        if not piece or piece is None or piece.get('player') != player:
            return []
        
        moves = []
        directions = []
        
        if piece.get('isKing'):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif player == 'white':
            directions = [(-1, -1), (-1, 1)]  # White moves up
        else:
            directions = [(1, -1), (1, 1)]  # Black moves down
        
        for dr, dc in directions:
            new_row = row + dr
            new_col = col + dc
            
            if (self._is_valid_position(new_row, new_col) and 
                self._is_dark_square(new_row, new_col) and 
                board[new_row][new_col] is None):
                moves.append({
                    'from': {'row': row, 'col': col},
                    'to': {'row': new_row, 'col': new_col},
                    'jumps': []
                })
        
        return moves
    
    def _get_jumps(self, board: List[List], row: int, col: int, player: str, 
                   jumped: Optional[List[Tuple]] = None) -> List[Dict]:
        """Get jump moves for a piece (including multiple jumps)"""
        piece = board[row][col]
        if not piece or piece is None or piece.get('player') != player:
            return []
        
        if jumped is None:
            jumped = []
        
        jumps = []
        directions = []
        
        if piece.get('isKing'):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif player == 'white':
            directions = [(-1, -1), (-1, 1)]
        else:
            directions = [(1, -1), (1, 1)]
        
        for dr, dc in directions:
            jump_row = row + dr
            jump_col = col + dc
            land_row = row + 2 * dr
            land_col = col + 2 * dc
            
            # Check if we can jump
            if (self._is_valid_position(jump_row, jump_col) and
                self._is_valid_position(land_row, land_col) and
                self._is_dark_square(land_row, land_col)):
                
                jumped_piece = board[jump_row][jump_col]
                land_piece = board[land_row][land_col]
                
                # Check if there's an enemy piece to jump and landing spot is empty
                if (jumped_piece and jumped_piece is not None and
                    jumped_piece.get('player') != player and
                    (jump_row, jump_col) not in jumped and
                    land_piece is None):
                    
                    # Check for multiple jumps
                    temp_board = deepcopy(board)
                    temp_board[land_row][land_col] = temp_board[row][col]
                    temp_board[row][col] = None
                    temp_board[jump_row][jump_col] = None
                    
                    # Promote to king if reached end
                    if temp_board[land_row][land_col] and ((player == 'white' and land_row == 0) or 
                        (player == 'black' and land_row == 7)):
                        temp_board[land_row][land_col]['isKing'] = True
                    
                    # Check for additional jumps from new position
                    new_jumped = jumped + [(jump_row, jump_col)]
                    additional_jumps = self._get_jumps(temp_board, land_row, land_col, player, new_jumped)
                    
                    if additional_jumps:
                        # Chain multiple jumps
                        for add_jump in additional_jumps:
                            jumps.append({
                                'from': {'row': row, 'col': col},
                                'to': add_jump['to'],
                                'jumps': [(jump_row, jump_col)] + add_jump['jumps']
                            })
                    else:
                        # Single or final jump
                        jumps.append({
                            'from': {'row': row, 'col': col},
                            'to': {'row': land_row, 'col': land_col},
                            'jumps': [(jump_row, jump_col)]
                        })
        
        return jumps
    
    def make_move(self, board: List[List], move: Dict) -> Tuple[List[List], bool]:
        """
        Make a move on the board.
        Returns: (new_board, is_promotion)
        """
        new_board = deepcopy(board)
        from_pos = move['from']
        to_pos = move['to']
        jumps = move.get('jumps', [])
        
        piece = new_board[from_pos['row']][from_pos['col']]
        if not piece or piece is None:
            return new_board, False
        
        new_board[to_pos['row']][to_pos['col']] = piece
        new_board[from_pos['row']][from_pos['col']] = None
        
        # Remove jumped pieces
        for jump_pos in jumps:
            if len(jump_pos) >= 2:
                new_board[jump_pos[0]][jump_pos[1]] = None
        
        # Check for king promotion
        is_promotion = False
        if not piece.get('isKing'):
            if ((piece.get('player') == 'white' and to_pos['row'] == 0) or
                (piece.get('player') == 'black' and to_pos['row'] == 7)):
                if new_board[to_pos['row']][to_pos['col']]:
                    new_board[to_pos['row']][to_pos['col']]['isKing'] = True
                    is_promotion = True
        
        return new_board, is_promotion
    
    def evaluate_board(self, board: List[List], player: str) -> float:
        """
        Evaluate board position for minimax.
        Positive values favor the player.
        """
        opponent = 'black' if player == 'white' else 'white'
        score = 0
        
        piece_values = {
            'regular': 10,
            'king': 30
        }
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = board[row][col]
                if piece and piece is not None:
                    value = piece_values['king'] if piece.get('isKing') else piece_values['regular']
                    
                    # Position bonus for kings in center
                    if piece.get('isKing'):
                        center_dist = abs(row - 3.5) + abs(col - 3.5)
                        value += (7 - center_dist) * 0.5
                    
                    # Position bonus for regular pieces (promoting is good)
                    if not piece.get('isKing'):
                        if piece.get('player') == 'white':
                            value += (7 - row) * 0.5  # Closer to promotion
                        else:
                            value += row * 0.5
                    
                    if piece.get('player') == player:
                        score += value
                    else:
                        score -= value
        
        # Mobility bonus
        player_moves = len(self.get_all_moves(player, board))
        opponent_moves = len(self.get_all_moves(opponent, board))
        score += (player_moves - opponent_moves) * 0.1
        
        return score
    
    def is_game_over(self, board: List[List], player: str) -> Tuple[bool, Optional[str]]:
        """
        Check if game is over.
        Returns: (is_over, winner)
        """
        opponent = 'black' if player == 'white' else 'white'
        
        player_moves = self.get_all_moves(player, board)
        opponent_moves = self.get_all_moves(opponent, board)
        
        player_pieces = sum(1 for row in board for piece in row if piece and piece is not None and piece.get('player') == player)
        opponent_pieces = sum(1 for row in board for piece in row if piece and piece is not None and piece.get('player') == opponent)
        
        if player_pieces == 0:
            return True, opponent
        if opponent_pieces == 0:
            return True, player
        if len(player_moves) == 0:
            return True, opponent
        if len(opponent_moves) == 0:
            return True, player
        
        return False, None
    
    def minimax(self, board: List[List], depth: int, alpha: float, beta: float, 
                maximizing: bool, player: str) -> Tuple[float, Optional[Dict]]:
        """
        Minimax algorithm with alpha-beta pruning.
        Returns: (best_score, best_move)
        """
        opponent = 'black' if player == 'white' else 'white'
        current_player = player if maximizing else opponent
        
        # Check terminal conditions
        is_over, winner = self.is_game_over(board, current_player)
        if is_over:
            if winner == player:
                return float('inf'), None
            elif winner == opponent:
                return float('-inf'), None
            else:
                return 0, None
        
        if depth == 0:
            return self.evaluate_board(board, player), None
        
        moves = self.get_all_moves(current_player, board)
        if not moves:
            return self.evaluate_board(board, player), None
        
        best_move = None
        
        if maximizing:
            max_eval = float('-inf')
            for move in moves:
                new_board, _ = self.make_move(board, move)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, False, player)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in moves:
                new_board, _ = self.make_move(board, move)
                eval_score, _ = self.minimax(new_board, depth - 1, alpha, beta, True, player)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            return min_eval, best_move
    
    def get_best_move(self, board: List[List], player: str, depth: Optional[int] = None) -> Optional[Dict]:
        """Get the best move using minimax algorithm"""
        if depth is None:
            depth = self.DEPTH
        
        _, best_move = self.minimax(board, depth, float('-inf'), float('inf'), True, player)
        return best_move

