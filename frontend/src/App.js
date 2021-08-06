import { useState, useEffect } from 'react';
import DialogContainer from './components/DialogContainer';
import Navbar from './components/Navbar';

function App() {
  const [welfares, setWelfares] = useState([]);

  return (
    <div className="App" style={{height:'100vh',overflowY:'hidden'}}>
      <Navbar />
      <DialogContainer />
    </div>
  );
}

export default App;
