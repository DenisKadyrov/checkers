export default function Cell({ label }) {
  return (
    <div className={`w-[80px] h-[80px] bg-yellow-400 flex items-center m-0 p-0 justify-center ${label}`}>
    </div>
  );
}