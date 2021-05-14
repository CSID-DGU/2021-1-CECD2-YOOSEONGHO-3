import {useState} from 'react';
import { Form,  Button} from 'react-bootstrap';
import axios from 'axios';
import './SignupPage.css';


export default function SignupPage() {
    const [email,setEmail]=useState('');
    const [password,setPassword]=useState('');
    const [nickname,setNickname]=useState('');
    const [age, setAge]=useState(0);

    function handleChange(e){
        if(e.target.type==='email'){
            setEmail(e.target.value);
        }else if(e.target.type==='password'){
            setPassword(e.target.value);
        }else if(e.target.type==='text'){
            setNickname(e.target.value)
        }else if(e.target.type==='number'){
            setAge(e.target.value);
        }
    }

    return (
        <div id='SignupPage'> 
            <div id='formContent'>
            <Form>
                 <Form.Group controlId="formBasicEmail">
                     <Form.Label>Email address</Form.Label>
                    <Form.Control type="email" placeholder="Enter email" onChange={handleChange} />
                </Form.Group>

                
                 <Form.Label>Nickname</Form.Label>
                <Form.Control type="text" placeholder="Enter nickname" onChange={handleChange} />
                
       
                <Form.Group controlId="formBasicPassword">
                     <Form.Label>Password</Form.Label>
                    <Form.Control type="password" placeholder="Enter password" onChange={handleChange} />
                </Form.Group>
                 
                
                     <Form.Label>Age</Form.Label>
                    <Form.Control type="number" placeholder="Enter age" onChange={handleChange} />


                    <Button variant="primary" onClick={()=>{
                        axios.post('/users/create/',{
                            email:email,
                            username:nickname,
                            password:password,
                            age:age
                        }).then(res=>{
                             if(res.data.message==='ok'){
                                 alert('회원가입 완료 !');
                                 window.location.href='/';
                             }
                        })
                    }}>
                         Submit
                </Button>
            </Form>
            </div>
        </div>
    );
}
