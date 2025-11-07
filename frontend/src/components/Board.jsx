import Cell from './Cell.jsx'
import './Board.css'

export default function Board({ board, selectedCell, availableMoves, onCellClick }) {
    return (
        <div className='grid grid-cols-8 border-4 border-gray-800'>
            {board.map((row, rIdx) =>
                row.map((col, cIdx) => {
                    const isMove = availableMoves.some(m => m.row === rIdx && m.col === cIdx);
                    return (
                        <Cell
                            key={`${rIdx}-${cIdx}`}
                            row={rIdx}
                            col={cIdx}
                            piece={col}
                            selectedCell={selectedCell}
                            isMove={isMove}
                            onClick={() => {
                                onCellClick(rIdx, cIdx)
                            }}
                        />
                    );
                })
            )}
        </div>
    );
}
