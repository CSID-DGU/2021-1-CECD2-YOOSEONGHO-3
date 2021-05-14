import * as types from '../_actions/types';

const initialState={
    isLogin:false,
    username:'',
    token:'',
};

export const userReducer=(state=initialState,action)=>{
    switch(action.type){
        case types.LOGIN_USER:
            return{
                isLogin:true,
                username:action.payload.username,
                token:action.payload.token
            }
        case types.LOGOUT_USER:
            return{
                isLogin:false,
                username:'',
                token:'',
            }   
        case types.REGISTER_USER:
            return{
                ...state
            }
        case types.RE_AUTH:
            return{
                isLogin:true,
                username:localStorage.getItem('username'),
                token:localStorage.getItem('token')
            }
        default:
            return state;
    }
}