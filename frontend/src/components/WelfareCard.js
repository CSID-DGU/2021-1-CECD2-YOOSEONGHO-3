function WelfareCard({title,desc}) {
    return (
        <div className='flex-col items-center justify-center bg-blue-50 rounded-xl
        cursor-pointer md:px-4 md:py-8 md:mb-4 px-2 py-4 mb-2 shadow-md flex-grow
        hover:scale-105 duration-500 transform ease-in-out hover:bg-blue-100 
        '>
            <p className='text-blue-700 text-sm md:text-lg'>{title}</p>
            <p className='md:text-sm'>{desc}</p>
        </div>
    )
}

export default WelfareCard;
