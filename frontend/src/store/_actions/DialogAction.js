import axios from 'axios';

//사용자 메시지 대화에 기록하는 액션함수
export const recordUserMsg=(message)=>{
    return{
        type:'RECORD_USER_MSG',
        payload:message
    }
}

//사용자 메시지를 봇에게 전송하고 응답을 받아와 기록하는 액션함수
export const sendAndReceive = async (message) => {
    const result=await axios.post('http://localhost:8000/api/chat', {
        message: message
    });

    return {
        type:'SEND_AND_RECEIVE',
        payload:result.data
    }
}


