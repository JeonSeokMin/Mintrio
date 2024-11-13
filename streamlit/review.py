# 프롬프트 분석
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)  # 임포트 전에 sys.path 추가


import streamlit as st
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt
from io import BytesIO
from crawling.crawl import Coupang
from collections import Counter
import matplotlib.font_manager as fm
import altair as alt


link_history_list = []
latest_reviews_text = ""

# OpenAI API 설정
client = OpenAI(api_key="you_key")  # 실제 API 키를 넣어주세요

# 사용자에게 번역되는 계단의 데이터와 대화를 검색하는 함수
def get_completion(prompt, model="gpt-3.5-turbo"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"API 호출 오류: {e}")
        return "API 호출 중 오류가 발생했습니다."

def run_analysis(url):
    global latest_reviews_text

    if "https://www.coupang.com" in url: # 쿠팡링크만 가능하게 하기
        link_history_list.append(url)

        # Coupang 클래스 인스턴스 생성 및 크롤링 시작
        try:
            coupang = Coupang()
            coupang.start(url)  # URL을 start 메서드에 전달
        except Exception as e:
            st.error(f"크롤링 오류: {e}")
            return

        # 크롤링된 엑셀 파일 경로 설정 (가장 최신 파일 가져오기)
        try:
            review_folder = os.path.join(os.path.dirname(__file__), 'reviewxisx')
            latest_file = max([os.path.join(review_folder, f) for f in os.listdir(review_folder)], key=os.path.getctime)
            df = pd.read_excel(latest_file)
        except Exception as e:
            st.error(f"엑셀 파일 오류: {e}")
            return

        # 데이터가 비어 있는지 확인
        if df.empty:
            st.error("크롤링된 데이터가 없습니다. 유효한 URL을 입력해 주세요.")
            return

        # 리뷰 텍스트의 일부를 저장 (너무 길 경우, 일부만 사용)
        latest_reviews_text = df.to_string()[:1500]  # 최대 1500자까지만 저장

        # **프롬프트 석민**
        prompt = (
            f"""
            그냥 리뷰내용 잘 보이면 잘보인다고 말해줘 
            {latest_reviews_text}
            """
        )
    else:
        st.error("유효한 URL을 입력해 주세요.")
        return

    # GPT 모델을 사용해 분석 수행
    result = get_completion(prompt)
    return result


# Streamlit 앱 구성 -> 일단 되는지 확인하려고 만든거
st.title("리뷰 / SWOT 분석 Dashboard")

url = st.text_input("아래의 URL을 입력하세요 (쿠팡 또는 구글 지도 링크)", key="url_input")
if st.button("분석 시작"):
    if url:
        analysis_result = run_analysis(url)
        if analysis_result:
            st.subheader("분석 결과")
            st.write(analysis_result)
    else:
        st.error("URL을 입력해 주세요.")