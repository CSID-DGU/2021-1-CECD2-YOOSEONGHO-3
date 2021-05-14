import {useState,useEffect} from 'react';
import {HashRouter as Router, Route} from 'react-router-dom'
import Navbar from './components/Navbar';
import SignupPage from './pages/SignupPage';
import LoginPage from './pages/LoginPage';
import 'bootstrap/dist/css/bootstrap.min.css';
import { reAuth } from './store/_actions/userActions';
import {useDispatch, useSelector} from 'react-redux';
import axios from 'axios';

function App() {
  const [welfares,setWelfares]=useState([]);
  const token=useSelector(state=>state.user.token);

  const dispatch=useDispatch();

  useEffect(()=>{
      if(localStorage.getItem('token')){
         dispatch(reAuth());

         axios.get('/api/welfares',{
          headers: { Authorization: `Bearer ${token}` }
         }).then(res=>{
           setWelfares(res.data);
          });
      }
  },[])
  return (
    <div className="App">
      <Navbar/>
      <Router>
         <Route exact path="/Signup" component={SignupPage}></Route>
         <Route exact path="/Signin" component={LoginPage}></Route>
      </Router>
    </div>
  );
}

export default App;
