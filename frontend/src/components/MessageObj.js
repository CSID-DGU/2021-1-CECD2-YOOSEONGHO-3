import WelfareCard from "./WelfareCard";
import Carousel from 'nuka-carousel';
import { ChevronRightIcon, ChevronLeftIcon } from '@heroicons/react/solid'

function MessageObj({type, msg, data}) {

    let justify='';
    if (type==='bot' || type==='data'){
        justify='flex justify-start mx-3  md:mx-4 md:w-5/12 w-4/5';
    }
    else{
        justify='flex mx-2 md:mx-4 justify-end';
    }

    return (
        <div className={justify}>
            {type==='bot' && (<div className='flex items-center md:mb-8 mb-4'>
                {/* 봇 이미지 */}
                <div className='flex-shrink-0'>
                    <img src='/images/bot2.png' className='md:w-12 md:h-12 w-8 h-8' />    
                </div>

                {/* 봇 메시지 */} 
                <div className=' flex bg-gray-100 rounded-xl ml-2 p-4 hover:scale-105 
                transition duration-700 transform ease-in-out shadow-md'>
                    <p>{msg}</p>
                </div>    
            
            </div>)}
        
            {type==='user' && (<div className='flex justify-end items-center md:mb-8 mb-4 md:w-5/12'>
                {/*사용자 메시지 */}
                <div className=' flex bg-blue-400 rounded-xl ml-2 p-4 text-white shadow-md'>
                    <p>{msg}</p>
                </div>  
            </div>)}
            
            {data.length>0 && (
                <Carousel className='w-full px-4 py-4 md:px-7 md:ml-2 md:py-8 bg-blue-50 hover:scale-105 rounded-xl 
                hover:bg-blue-100 transform duration-500 shadow-lg md:mb-10' wrapAround={true}
                defaultControlsConfig={{
                    pagingDotsStyle: {
                      fill: "green",
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
                         <div className='flex-col items-center justify-center' key={d.title}>
                             <p className='text-blue-700 text-sm md:text-lg md:mb-4 mb-2'>{d.title}</p>
                             <p className='md:text-sm md:pb-0 pb-2'>{d.desc}</p>
                         </div>
                    ))}
                </Carousel>
            )}
        </div>
    )
}

export default MessageObj;
