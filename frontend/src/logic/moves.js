export function getAvailableMoves(board, row, col) {
  const piece = board[row][col];
  if (!piece) return [];

  const directions = piece.isKing
    ? [[1, 1], [1, -1], [-1, 1], [-1, -1]]
    : piece.player === 'white'
      ? [[-1, -1], [-1, 1]]
      : [[1, -1], [1, 1]];

  const moves = [];

  for (const [dr, dc] of directions) {
    const r = row + dr;
    const c = col + dc;

    if (r < 0 || r >= 8 || c < 0 || c >= 8) continue;
    if (!board[r][c]) moves.push({ row: r, col: c });
  }

  return moves;
}

export function movePiece(board, from, to) {
  const newBoard = board.map(row => [...row]);
  newBoard[to.row][to.col] = newBoard[from.row][from.col];
  newBoard[from.row][from.col] = null;
  return newBoard;
}
