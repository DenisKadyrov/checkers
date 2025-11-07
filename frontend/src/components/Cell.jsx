import Piece from "./Piece";

export default function Cell({ row, col, piece, selectedCell, isMove, onClick }) {
  const isDark = (row + col) % 2 === 1;
  const bg = isDark ? "bg-yellow-700" : "bg-yellow-300";
  const isSelected = selectedCell?.row === row && selectedCell?.col == col

  return (
    <div
      onClick={onClick}
      className={`w-20 h-20 flex items-center justify-center ${bg}`}
    >
      {piece && <Piece piece={piece} isSelected={isSelected} />}
    </div>
  );
}