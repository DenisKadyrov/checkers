import Piece from "./Piece";

export default function Cell({ row, col, piece, isSelected, isMove, onClick }) {
  const isDark = (row + col) % 2 === 1;
  const bg = isDark ? "bg-yellow-700" : "bg-yellow-300";
  const highlight = isSelected ? "border-4 border-blue-400" : "";

  return (
    <div
      onClick={onClick}
      className={`w-20 h-20 flex items-center justify-center ${bg} ${highlight}`}
    >
      {piece && <Piece piece={piece} />}
    </div>
  );
}