export default function Piece({ piece, isSelected }) {
  const color = piece.player === "white" ? "bg-white" : "bg-black";
  const king = piece.isKing ? "border-4 border-yellow-300" : "";

  return (
    <div className={`w-12 h-12 rounded-full ${color} ${king} ${isSelected ? "border-4 border-red-500 ring-4 ring-yellow-400" : ""}`} />
  );
}
