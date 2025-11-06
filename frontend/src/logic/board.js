export default function initBoard() {
  const board = Array(8).fill(null).map(() => Array(8).fill(null));
  for (let row = 0; row < 3; row++) {
    for (let col = 0; col < 8; col++) {
      if ((row + col) % 2 === 1) board[row][col] = { player: 'black', isKing: false };
    }
  }
  for (let row = 5; row < 8; row++) {
    for (let col = 0; col < 8; col++) {
      if ((row + col) % 2 === 1) board[row][col] = { player: 'white', isKing: false };
    }
  }
  return board
}