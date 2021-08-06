import WelfareCard from "./WelfareCard";

function MessageObj({type, msg, data}) {
    let justify='';
    if (type==='bot' || type==='data'){
        justify='flex justify-start mx-3 md:mx-4 md:w-5/12 w-4/5';
    }
    else{
        justify='flex mx-2 md:mx-4 justify-end';
    }

    return (
        <div className={justify}>
            {type==='bot' && (<div className='flex items-center md:mb-8 mb-4'>
                {/* 봇 이미지 */}
                <div className='flex-shrink-0'>
                    <img src='/images/bot.png' className='md:w-12 md:h-12 w-8 h-8' />    
                </div>

                {/* 봇 메시지 */} 
                <div className=' flex bg-gray-100 rounded-xl ml-2 p-4 hover:scale-105 transition duration-700 transform ease-in-out '>
                    <p>{msg}</p>
                </div>    
            
            </div>)}
        
            {type==='user' && (<div className='flex justify-end items-center md:mb-8 mb-4 md:w-5/12'>
                {/*사용자 메시지 */}
                <div className=' flex bg-blue-400 rounded-xl ml-2 p-4 text-white'>
                    <p>{msg}</p>
                </div>  
            </div>)}
            
            {data.length>0 && (
                <div className='flex-col w-full'>
                    {data.map(d=>(
                        <WelfareCard key={d.title} title={d.title} desc={d.desc} />
                    ))}
                </div>
            )}
        </div>
    )
}

export default MessageObj;
