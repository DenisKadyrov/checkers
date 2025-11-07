/**
 * API service for communicating with the backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function getBotMove(board, currentPlayer) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board: board,
        current_player: currentPlayer,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get bot move');
    }

    return await response.json();
  } catch (error) {
    console.error('Error getting bot move:', error);
    throw error;
  }
}

export async function validateMove(board, fromPos, toPos) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/validate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board: board,
        from_pos: fromPos,
        to_pos: toPos,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Invalid move');
    }

    return await response.json();
  } catch (error) {
    console.error('Error validating move:', error);
    throw error;
  }
}

export async function getAvailableMoves(board, currentPlayer) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/moves`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        board: board,
        current_player: currentPlayer,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Failed to get available moves');
    }

    const data = await response.json();
    return data.moves;
  } catch (error) {
    console.error('Error getting available moves:', error);
    throw error;
  }
}

export async function initBoard() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/init`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error('Failed to initialize board');
    }

    const data = await response.json();
    return data.board;
  } catch (error) {
    console.error('Error initializing board:', error);
    throw error;
  }
}

