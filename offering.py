import streamlit as st
import os
from openai import OpenAI

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
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for marketing campaigns."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("Offering Framework(가제)")
    
    st.write("김한범 매니저님, 원하시는 캠페인 아이디어를 프롬프트 형식으로 입력해주세요.")
    
    campaign_prompt = st.text_area("캠페인 아이디어 프롬프트", 
                                   "다음과 같은 마케팅 캠페인 아이디어를 생성해주세요: ")
    
    if st.button("아이디어 생성"):
        if campaign_prompt:
            with st.spinner("아이디어를 생성 중입니다..."):
                response = get_gpt_response(campaign_prompt)
            st.write("생성된 아이디어:")
            st.write(response)
        else:
            st.warning("프롬프트를 입력해주세요.")

if __name__ == "__main__":
    main()