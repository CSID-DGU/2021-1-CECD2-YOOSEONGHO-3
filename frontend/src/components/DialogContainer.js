import { useState, useEffect, useRef } from 'react';
import { MailIcon } from '@heroicons/react/solid'
import MessageObj from './MessageObj';
import axios from 'axios';

const testData = [{
    title: '여성장애인 출산 및 양육 지원',
    desc: '- 출산지원금 : 여성장애인의 출산비용 지원을 통해 경제적 부담 경감 및 출산친화 문화 조성 - 양육지원금 : 여성장애인에게 양육비 지원을 통해 여성장애인의 안정적인 가족생활 영위 및 출산장려'
},
{
    title: '저소득층 국민건강보험료 지원',
    desc: '생활에 어려움을 겪고 있는 저소득 주민에게 국민건강보험료 및 노인장기요양보험료를 지원함으로써 시민의 건강증진과 사회복지 향상을 도모하고 의료사각지대 해소'
},
{
    title: '불우소외계층지원',
    desc: '어려운 이웃과 따뜻한 정을 나누는 사회분위기 조성'
},
{
    title: '장애인 의료재활지원',
    desc: '저소득 장루 요루 장애인에 대한 의료케어제품 구입비 지원'
},
{
    title: '노인대학운영',
    desc: '노인 여가활동 지원'
}]

function DialogContainer() {
    const [dialog, setDialog] = useState([{ type: 'bot', message: '안녕하세요? 맞춤형 복지정보 탐색 챗봇입니다 ^^\n어떤 복지정보를 찾으시는지 알려주세요', data: [] }]);
    const [botMessage, setBotMessage] = useState([]);
    const [userMessage, setUserMessage] = useState([]);
    const inputRef = useRef(null);
    const messagesEndRef = useRef(null)

    window.onbeforeunload = function () {
        window.scrollTo(0, 0);
    }

    const scrollToBottom = () => {
        //scollIntoView 사용 시 상단 overflow문제가 발생해서 
        messagesEndRef.current.parentNode.scrollTop=messagesEndRef.current.offsetTop;
        
    }
    useEffect(() => {
        //대화 내용이 3개를 넘어가면 자동으로 맨 밑 스크롤
        if (dialog.length > 4) {
            scrollToBottom();
        }

    }, [dialog]);


    const sendMessage = (e) => {
        e.preventDefault();

        if (!inputRef.current.value) return;

        setDialog([...dialog, { type: 'user', message: inputRef.current.value, data: [] }]);

        axios.post('http://localhost:8000/api/chat', {
            message: inputRef.current.value
        }).then(res => {
            console.log(res);
            let check = res.data.isLast;
            let welfare = [];
            if (check === true) {
                
                welfare = testData;
            }
            setDialog(elements => [...elements, { type: 'bot', message: res.data.message, data: [] }, { type: 'data', message: '', data: welfare }]);

        })

        inputRef.current.value = '';
    }

    return (
        <div className='flex-col border-l-2 border-r-2 border-gray-300 md:mx-14'>
            {/* 봇과 사용자의 대화 부분 */}
            <div className='flex-col h-screen overflow-y-auto md:pt-8 pt-4  pb-32 text-xs md:text-base'
            style={{scrollBehavior:'smooth'}}>
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
