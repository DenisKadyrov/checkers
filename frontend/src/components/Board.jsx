import Cell from './Cell.jsx'
import './Board.css'

export default function Board() {
    return (
        <div className='grid grid-cols-8  overflow-hidden'>
            {[7, 6, 5, 4, 3, 2, 1, 0].map(y =>
                <div className='w-[80px] m-0 p-0' key={y}>
                    {[0, 1, 2, 3, 4, 5, 6, 7].map(x =>
                        <Cell key={x} label={(x + y) % 2 == 0 ? 'dark' : 'light'} />
                    )}
                </div>
            )}
        </div>
    );
}
