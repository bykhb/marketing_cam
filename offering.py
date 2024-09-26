import streamlit as st
import os
import openai
from openai import OpenAI

# Streamlit Cloud에서는 이 부분이 필요 없으므로 조건부로 실행
if not os.getenv("STREAMLIT_CLOUD"):
    from dotenv import load_dotenv
    load_dotenv()

# 환경 변수에서 OpenAI API 키 가져오기
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OpenAI API 키가 설정되지 않았습니다. 환경 변수를 확인해주세요.")
    st.stop()

client = OpenAI(api_key=api_key)

def get_gpt_response(prompt):
    try:
        # Define the desired format
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
"아이폰 16 TDS 사전예약"

[대상군 수]
"450,000명"

[캠페인 기간]
'''
2024년 9월 13일(금) ~ 20일(금)
(아이폰 사존예약기간 동안)
'''

[캠페인 텍스트]
'''
<title>
    (광고)[SKT] iPhone 16 사전에약 혜택 안내

    <intro>
    '홍길동' 고객님, 안녕하세요.
    iPhone 16 사전예약이 2024년 9월 13일(금) 오후 9시에 시작됩니다.
    
    사전예약 후 개통 시 넷플릭스 요금제는 또는 T우주팻 Netflix에 가입하시면,
    추첨을 통해 Netflix Watch Kit를 드립니다.
    
    SK텔레콤에서 준비한 다양한 혜택을 지금 확인해 보세요.
    
		<body>  
    ▶ Netflix Watch Kit 자세히 보기: http://t-mms.kr/jzZ/#74
    * 위 URL은 사전예약 시작과 함께 2024년 9월 13일(금) 오후 9시에 오픈됩니다.
    
    ▶ 사전예약 혜택 모아 보기: http://t-mms.kr/jzG/#74
    ▶ T 다이렉트샵 사전예약: http://t-mms.kr/jzd/#74
    * 위 URL은 사전예약 시작과 함께 2024년 9월 13일(금) 오후 9시에 오픈됩니다.
    
    ■ 문의: T 다이렉트샵 고객센터(1525, 무료)

    <close>
    SKT와 함께해 주셔서 감사합니다.
    
    무료 수신거부 1504
'''

[캠페인 이미지]
이미지 생성 필요

[예상 캠페인 반응율]
"5.6%"

---

[2번]

(위와 동일한 형식으로 최대 5개까지 제안)

포맷에서 "" 안에 들어간 내용은 예시입니다. 답변을 예시와 비슷한 형식으로 만들어 주세요.

제안하는 캠페인 Context의 개수는 최대 5개로 제한합니다.
"""

        # Combine the format instructions with the system prompt
        messages = [
            {
                "role": "system",
                "content": format_instructions
            },
            {
                "role": "user",
                "content": prompt
            }
        ]

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens = 5000,
            temperature = 0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Offering Framework(가제)")
    st.write("김한범 매니저님, 원하시는 캠페인 아이디어를 프롬프트 형식으로 입력해주세요.")

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
    placeholder = "(예시) 아이폰 16 사전 예약할 고객에게 TDS에서 예약하게 하는 MMS 캠페인을 만들어줘"

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
