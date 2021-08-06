import AccessibilityNewIcon from '@material-ui/icons/AccessibilityNew';

function Navbar() {
  return (
    <div className='sticky top-0 z-50 md:h-16 bg-yellow-100 flex items-center p-2 lg:px-5 font-bold text-xl shadow-md'>
      <div className='flex items-center'>
        <AccessibilityNewIcon
          className='md:w-14 md:h-14 text-green-500'
        />
        <p className='text-gray-800 ml-2 '>모두의 복지</p>
      </div>      
    </div>
  )
}

export default Navbar;