import Cell from './Cell.jsx'
import './Board.css'

export default function Board({ board, selectedCell, availableMoves, onCellClick }) {
    return (
        <div className='grid grid-cols-8 border-4 border-gray-800'>
            {board.map((row, rIdx) =>
                row.map((col, cIdx) => {
                    const isSelected = selectedCell?.row === rIdx && selectedCell?.row === rIdx;
                    const isMove = availableMoves.some(m => m.row === cIdx && m.col === cIdx);
                    return (
                        <Cell
                            key={`${rIdx}-${cIdx}`}
                            row={rIdx}
                            col={cIdx}
                            piece={col}
                            isSelected={isSelected}
                            isMove={isMove}
                            onClick={(e) => {
                                e.stopPropagation()
                                onCellClick(rIdx, cIdx)
                            }}
                        />
                    );
                })
            )}
        </div>
    );
}
