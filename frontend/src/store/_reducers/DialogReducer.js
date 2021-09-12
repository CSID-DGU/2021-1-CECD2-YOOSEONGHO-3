import * as type from '../_actions/ActionTypes';

const initialState={
    dialog:[{type:'bot',message:'안녕하세요? 맞춤형 복지정보 탐색 봇 서비스에 오신걸 환영합니다^^'}]
}

export default function dialogReducer(state=initialState.dialog,action){
    switch (action.type){
        case type.RECORD_USER_MSG:
            console.log(state, action.payload);
            return [...state, {type:'user',message:action.payload}];

        case type.LOADING:
            return [...state, {type:'bot',message:''}]
        
        case type.SEND_AND_RECEIVE:
            let tmpState=[...state];
            tmpState[state.length-1].message=action.payload.message;
    
            if(action.payload.isLast===true){
                return [...tmpState, {type:'data', message:'', data:action.payload.data}];
            }
            else{
                return [...tmpState];
            }
            
        case type.RESET_DIALOG:
            return [{type:'bot',message:'안녕하세요? 맞춤형 복지정보 탐색 봇 서비스에 오신걸 환영합니다^^'}]
        
            default:
            return [...state];
    }
}