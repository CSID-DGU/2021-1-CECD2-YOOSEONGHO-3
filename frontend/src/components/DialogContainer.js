import { useState, useEffect, useRef } from 'react';
import { MailIcon } from '@heroicons/react/solid'
import MessageObj from './MessageObj';
import { useSelector, useDispatch } from 'react-redux';
import { sendAndReceive, recordUserMsg } from '../store/_actions/DialogAction';

function DialogContainer() {
    const inputRef = useRef(null);
    const messagesEndRef = useRef(null);
    const scrollBtnRef=useRef(null);
    const dispatch = useDispatch();
    const dialog = useSelector(state => state.dialog);

    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }

    const scrollToBottom = () => {
        //scollIntoView 사용 시 상단 overflow문제가 발생해서 scrollTop 사용
        messagesEndRef.current.parentNode.scrollTop = messagesEndRef.current.offsetTop;

    }
    useEffect(() => {
        if (dialog.length>4){
            scrollToBottom();
        }

    }, [dialog]);

    const sendMessage = (e) => {
        e.preventDefault();

        if (!inputRef.current.value) return;

        //유저 메시지 등록 액션 호출
        dispatch(recordUserMsg(inputRef.current.value));

        //메시지 전송 및 봇 응답 수신 액션 호출
        sendAndReceive(inputRef.current.value).then(res => {
            dispatch(res);
            scrollToBottom();
        });

        inputRef.current.value = ''
    }

    return (
        <div className='flex-col border-l-2 border-r-2 border-gray-300 md:mx-14'>
            {/* 봇과 사용자의 대화 부분 */}
            <div className='flex-col h-screen overflow-y-auto md:pt-8 pt-4  pb-32 text-xs md:text-base'
                style={{ scrollBehavior: 'smooth' }}>
                {dialog.map(message => (
                    <div key={Math.random()}>
                        <MessageObj type={message.type} msg={message.message} data={message.data} />
                    </div>
                ))}
                <div ref={messagesEndRef}></div>
            </div>

            {/* 사용자 메시지 입력 input */}
            <form
                className='flex sticky bottom-0 items-center  md:h-14 h-12 z-50 bg-white py-1 border-t-2 border-gray-300'
                onSubmit={sendMessage}
            >
                <input
                    className='md:w-11/12 flex-shrink-0 w-4/5 items-center outline-none h-full rounded-xl pl-2
                    focus:placeholder-gray-600 bg-gray-100 mx-1'
                    type='text'
                    placeholder='메시지를 입력하세요..'
                    ref={inputRef}
                />

                <MailIcon
                    className='flex-grow hover:scale-105 w-9 h-9  text-blue-400 cursor-pointer
                    hover:text-blue-500 transition duration-300 transform ease-in-out '
                    type='submit'
                    fontSize='large'
                    onClick={sendMessage}
                />

            </form>
        </div>
    )
}

export default DialogContainer
