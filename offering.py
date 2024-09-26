import streamlit as st
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Streamlit Cloud에서는 이 부분이 필요 없으므로 조건부로 실행
if not os.getenv("STREAMLIT_CLOUD"):
    from dotenv import load_dotenv
    load_dotenv()

# 환경 변수에서 OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경 변수를 확인해주세요.")
    st.stop()

# LangChain LLM 설정
llm = ChatOpenAI(
    model='anthropic/claude-3-5-sonnet-20240620',
    temperature=0.9,
    frequency_penalty=1.5,
    max_tokens=4096,
    timeout=None,
    base_url="https://api.platform.a15t.com/v1"
)


def get_gpt_response(prompt):
    try:
        # 원하는 형식 정의
        format_instructions = """
당신은 마케팅 캠페인 아이디어를 생성하는 도우미입니다. 답변을 아래의 형식으로 제공해 주세요:

---------------------------------------

제안 드리는 "{캠페인명}" MMS 캠페인은 아래와 같이 최대 5가지입니다.

[1번]

[캠페인 Context] 
'''
아이폰 16 TDS 사전 예약 MMS 캠페인은 아이폰 기변 확률이 높은 고객 중
사전 예약 혜택에 관심이 있는 고객에게 사전 예약 기간동안 캠페인 진행을 제안드립니다.
'''

[캠페인명]
아이폰 16 TDS 사전예약

[대상군 수]
450,000명

[캠페인 기간]
2024년 9월 13일(금) ~ 20일(금)
(아이폰 사존예약기간 동안)

[캠페인 텍스트]
    (광고)[SKT] iPhone 16 사전에약 혜택 안내

    '홍길동' 고객님, 안녕하세요.
    iPhone 16 사전예약이 2024년 9월 13일(금) 오후 9시에 시작됩니다.
    
    사전예약 후 개통 시 넷플릭스 요금제는 또는 T우주팻 Netflix에 가입하시면,
    추첨을 통해 Netflix Watch Kit를 드립니다.
    
    SK텔레콤에서 준비한 다양한 혜택을 지금 확인해 보세요.
    
    ▶ Netflix Watch Kit 자세히 보기: http://t-mms.kr/jzZ/#74
    * 위 URL은 사전예약 시작과 함께 2024년 9월 13일(금) 오후 9시에 오픈됩니다.
    
    ▶ 사전예약 혜택 모아 보기: http://t-mms.kr/jzG/#74
    ▶ T 다이렉트샵 사전예약: http://t-mms.kr/jzd/#74
    * 위 URL은 사전예약 시작과 함께 2024년 9월 13일(금) 오후 9시에 오픈됩니다.
    
    ■ 문의: T 다이렉트샵 고객센터(1525, 무료)

    SKT와 함께해 주셔서 감사합니다.
    
    무료 수신거부 1504

[캠페인 이미지]
MMS에 들어가는 크기로 캠페인 context에 맞게 이미지 생성해줘

[예상 캠페인 반응율]
"5.6%"

---
마케팅 캠페인 아이디어 생성 지침
1. 포맷에서 [..] 안에 들어간 내용은 예시입니다.답변을 예시와 비슷한 형식으로 만들어 주세요.
2. 제안하는 캠페인 Context의 개수는 최대 5개로 제한.
3. 캠페인을 여러 개 제안할 때는 각 캠페인의 context가 달라야 됩니다.
4. 캠페인 이미지 부분에도 gpt가 이미지를 생성해서 넣어줘
5. context 여러개를 제안할 떄는 '-----'와 같은 line으로 구분지어줘

"""

        # Combine the format instructions with the system prompt
        messages = [
            SystemMessage(content=format_instructions),
            HumanMessage(content=prompt)
        ]

        response = llm(messages)
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Offering Framework(가제)")
    st.write("유수빈 매니저님, 원하시는 캠페인 아이디어를 프롬프트 형식으로 입력해주세요.")

    # 세로 간격 추가
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # CSS 스타일 수정
    st.markdown("""
    <style>
    /* 스타일 코드 생략 */
    </style>
    """, unsafe_allow_html=True)

    # 세션 상태에서 메시지 리스트 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 프롬프트 입력칸
    placeholder = "(예시) SK텔레콤에서 아이폰 16 사전 예약할 고객에게 TDS에서 예약하게 하는 MMS 캠페인을 만들어줘"

    campaign_prompt = st.text_area(
        "마케팅 캠패인 프롬프트",
        value="",
        placeholder=placeholder,
        height=100,
        key="prompt_input"
    )

    # 버튼 컨테이너
    st.markdown('<div class="button-container full-width">', unsafe_allow_html=True)

    # 균형 잡힌 컬럼 사용
    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        st.markdown('<div class="left-button">', unsafe_allow_html=True)
        if st.button("Type", key="type_button"):
            st.session_state.show_options = not st.session_state.get('show_options', False)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="right-button">', unsafe_allow_html=True)
        # 아이디어 생성 버튼 클릭 시 동작
        if st.button("아이디어 생성", key="generate_idea"):
            if campaign_prompt:
                st.session_state.messages.append({"role": "user", "content": campaign_prompt})
                with st.spinner("아이디어를 생성 중입니다..."):
                    response = get_gpt_response(campaign_prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})
            else:
                st.warning("프롬프트를 입력해주세요.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Type 선택 옵션
    if st.session_state.get('show_options', False):
        st.markdown("<div style='margin-top: -10px;'>", unsafe_allow_html=True)
        option = st.radio(
            "강조 하고 싶은 캠페인 Type을 선택하세요:",
            ('개인화 강조', '감성적', 'MASS'),
            key="campaign_type",
            horizontal=True
        )
        if option == '개인화 강조':
            st.info('메시지의 개인화를 강조합니다. 생성에 시간이 더 걸립니다.')
        elif option == '감성적':
            st.info('메시지를 감성적으로 작성합니다. T는 이해하기 어려울 수 있습니다.')
        else:
            st.info('최대한 다수의 대상군을 Focusing 합니다. 반응율이 떨어질 수 있습니다.')
        st.markdown("</div>", unsafe_allow_html=True)

    # 대화 내용 표시
    if st.session_state.messages:
        st.markdown("---")  # 구분선 추가
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.write(f"**사용자:** {message['content']}")
            else:
                with st.chat_message("assistant"):
                    st.write(f"**AI:** {message['content']}")

if __name__ == "__main__":
    main()