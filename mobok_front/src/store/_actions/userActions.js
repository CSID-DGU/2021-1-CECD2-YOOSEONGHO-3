import axios from 'axios';
import {
    LOGIN_USER,
    REGISTER_USER,
    LOGOUT_USER,
    RE_AUTH,
    ERROR
} from './types';

export function loginUser(data){
    localStorage.setItem('token',data.token);
    localStorage.setItem('username',data.username);
    return {
        type:LOGIN_USER,
        payload:data
    } 
};

export const loginTry=(dataToSubmit)=>async(dispatch,getState)=>{
    try{
        const res=await axios.post('/users/login/',dataToSubmit);
        dispatch(loginUser(res.data));
    }catch(error){
        dispatch(error());
    }
}

export function logoutUser(){
    localStorage.removeItem('token');
    localStorage.removeItem('username');

    return{
        type:LOGOUT_USER,
    }
}

export function registerUser(dataToSubmit){
    const request=axios.post('/users/create',dataToSubmit)
    .then(res=>res.data);

    return {
        type:REGISTER_USER,
        payload:request
    }
};

export function reAuth(){
    return {
        type:RE_AUTH
    }
}

export function error(){
    return{
        tyoe:ERROR
    }
}