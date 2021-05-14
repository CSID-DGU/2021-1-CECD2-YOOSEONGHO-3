import {useState, useEffect} from 'react';
import { Form,  Button} from 'react-bootstrap';
import { useDispatch, useSelector } from 'react-redux';
import './SignupPage.css';
import {loginTry} from '../store/_actions/userActions';
import {useHistory} from 'react-router-dom';

export default function SignupPage() {
    const isLogin=useSelector(state=>state.user.isLogin);
    const dispatch=useDispatch();
    const history=useHistory();

    const [email,setEmail]=useState('');
    const [password,setPassword]=useState('');

    const data = {email : email, password : password}

    useEffect(()=>{
        console.log('Login page rendered!');
       if(isLogin===true){
           history.push('/');
       }
    },[isLogin])

    function handleChange(e){
        if(e.target.type==='email'){
            setEmail(e.target.value);
        }else if(e.target.type==='password'){
            setPassword(e.target.value);
        }
    }

    return (
        <div id='SigninPage'> 
            <div id='formContent'>
            <Form>
                 <Form.Group controlId="formBasicEmail">
                     <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" onChange={handleChange} />
                </Form.Group>

        
       
                <Form.Group controlId="formBasicPassword">
                     <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Password" onChange={handleChange} />
                </Form.Group>

                    <Button variant="primary" onClick={()=>{
                          dispatch(loginTry(data));
                    }}>
                         로그인
                </Button>
            </Form>
            </div>
        </div>
    );
}
