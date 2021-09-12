import Carousel from 'nuka-carousel';
import CircularProgress from '@material-ui/core/CircularProgress';
import { ChevronRightIcon, ChevronLeftIcon } from '@heroicons/react/solid'
import { resetDialog } from "../store/_actions/DialogAction";
import {useDispatch} from 'react-redux';
import botImg from '../images/bot2.png';

function MessageObj({type, msg='', data=[]}) {
    const dispatch=useDispatch();

    let justify='';
    if (type==='bot' || type==='data'){
        justify='flex justify-start mx-3  md:mx-4 md:w-5/12 w-3/5';
    }
    else{
        justify='flex mx-2 md:mx-4 justify-end';
    }

    return (
        <div className={justify}>
            {type==='bot' && (<div className='flex items-center mb-8'>
                {/* 봇 이미지 */}
                <div className='flex-shrink-0'>
                    <img src={botImg} className='md:w-12 md:h-12 w-8 h-8' />    
                </div>

                {/* 봇 메시지 */} 
                <div className='flex bg-gray-100 rounded-xl ml-2 p-4 hover:scale-105 
                    transition duration-700 transform ease-in-out shadow-md'>
                    {msg ? (<p>{msg}</p>) : (
                        <CircularProgress />
                    )}
                </div>
            </div>)}
        
            {type==='user' && (<div className='flex justify-end items-center mb-8 md:w-5/12'>
                {/*사용자 메시지 */}
                <div className=' flex bg-blue-400 rounded-xl ml-2 p-4 text-white shadow-md'>
                    <p>{msg}</p>
                </div>  
            </div>)}
            
            {data.length>0 && (
              <div className='flex flex-col w-full items-center'>
                <Carousel className='flex px-4 py-4 md:px-7 ml-2 md:py-8 bg-blue-50 hover:scale-105 rounded-xl 
                hover:bg-blue-100 transform duration-500 shadow-lg mb-4 outline-none' wrapAround={true}
                defaultControlsConfig={{
                    pagingDotsStyle: {
                      fill: "purple",
                      margin:'3px'
                    }
                  }}
                renderCenterLeftControls={({previousSlide})=>(
                    <ChevronLeftIcon className='w-8 h-8 opacity-50 hover:text-gray-500 animate-bounce text-gray-400' onClick={previousSlide} />
                )}
                renderCenterRightControls={({nextSlide})=>(
                    <ChevronRightIcon className='w-8 h-8 opacity-50 hover:text-gray-500 animate-bounce text-gray-400' onClick={nextSlide} />
                )}>
                    {data.map(d=>(
                         <div className='flex flex-col items-center justify-center' key={d.title}>
                             <p className='text-blue-700 text-sm md:text-lg md:mb-4 mb-2'>{d.title}</p>
                             <p className='md:text-sm md:pb-0 pb-2'>{d.description}</p>
                         </div>
                    ))}
                </Carousel>
                <button 
                    className=' bg-blue-400 text-white text-sm p-2 rounded-full
                    animate-pulse float-right md:ml-2 mb-8'
                    onClick={()=>{
                        dispatch(resetDialog());
                    }}
                >다시 대화하기</button>
                </div> 
            )}
        </div>
    )
}

export default MessageObj;
