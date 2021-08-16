import { useState, useEffect } from 'react';
import DialogContainer from './components/DialogContainer';
import Navbar from './components/Navbar';

function App() {
  const [welfares, setWelfares] = useState([]);

  return (
    <div className="App">
      <Navbar />
      <DialogContainer />
    </div>
  );
}

export default App;
