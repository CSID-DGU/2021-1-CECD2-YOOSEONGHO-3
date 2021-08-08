import * as type from '../_actions/ActionTypes';

const initialState={
    dialog:[{type:'bot',message:'안녕하세요? 맞춤형 복지정보 탐색 봇 서비스에 오신걸 환영합니다^^',data:[]}]
}

export default function dialogReducer(state=initialState.dialog,action){
    switch (action.type){
        case type.RECORD_USER_MSG:
            console.log(state, action.payload);
            return [...state, {type:'user',message:action.payload, data:[]}];
        
        case type.SEND_AND_RECEIVE:
            if(action.payload.isLast===true){
                return [...state, {type:'bot',message:action.payload.message, data:[]}, {type:'data', message:'', data:action.payload.data}];
            }
            else{
                return [...state, {type:'bot',message:action.payload.message, data:action.payload.data}];
            }
            
        
        default:
            return [...state];
    }
}