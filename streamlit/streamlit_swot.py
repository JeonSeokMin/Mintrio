import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="리뷰 / SWOT 분석 Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

import json
from review import reivew_crawling
import platform
from matplotlib import rc
import pandas as pd

import os
import sys



# 시스템 기본 폰트 설정
if platform.system() == 'Windows':
    rc('font', family='Malgun Gothic')  # 윈도우: 맑은 고딕
elif platform.system() == 'Darwin':  # macOS
    rc('font', family='AppleGothic')
else:
    rc('font', family='NanumGothic')  # 리눅스: 나눔고딕 (또는 시스템 기본 폰트)

# 환경변수
from dotenv import load_dotenv

load_dotenv()

# ABSA_LLM
# LLM 객체 생성

from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# SWOT LLM
# chat_model
from langchain_community.chat_models import ChatOpenAI

# OutputParser
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.runnables import RunnablePassthrough
from pydantic import BaseModel, Field
from typing import List



# 스타일 설정
st.markdown(
    """
    <style>
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; padding-left: 1rem; padding-right: 1rem; }
    .css-1d391kg, .sidebar-content { background-color: #F4E5DB; }
    .css-1r6slb0 { background-color: #fff; border-radius: 10px; border: 1px solid #ddd; }
    .stButton>button { color: white; background-color: #D4A373; border: None; border-radius: 5px; width: 100%; padding: 0.5rem 1rem; }
    .stMarkdown h1, h2, h3 { font-family: 'Arial', sans-serif; color: #5A4635; }
    .swot-box { background-color: #E8D4C1; color: black; border-radius: 10px; padding: 10px; margin: 10px 0; text-align: left; height: 200px; overflow-y: auto; }
    .divider-horizontal { border-top: 1px solid #d3d3d3; margin: 20px 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

ABSA_llm = ChatOpenAI(
    temperature=0.7,  # 창의성
    model_name="gpt-3.5-turbo",  # 모델명
)

ABSA_template = """
    Define the sentiment elements as follows:
    
    − The 'aspect term' refers to a specific feature, attribute, or aspect of an item, product, or service that a user might comment on. If implicit, the aspect term can be 'null'.
    − The 'opinion term' reflects the sentiment or attitude toward a specific aspect. It can also be 'null' for implicit opinions.
    − The 'aspect category' is the general category to which the aspect belongs. Examples may include 'quality', 'pricing', 'availability', 'appearance', 'functionality', 'service', 'general', and other suitable categories as applicable across diverse domains.
    − The 'sentiment polarity' expresses whether the sentiment is 'positive', 'negative', or 'neutral'.

    Based on the provided definitions, identify and organize all sentiment elements from the following text by grouping them by sentiment polarity. 
    
    Please answer in Korean.

    Text to analyze:
    {text}
"""

# 프롬프트 생성
ABSA_prompt = ChatPromptTemplate.from_template(ABSA_template)

# 체인 생성 (프롬프트와 LLM 연결)
ABSA_chain = LLMChain(llm=ABSA_llm, prompt=ABSA_prompt)


SWOT_llm = ChatOpenAI(
    temperature=0.7,  # 창의성
    model_name="gpt-3.5-turbo",  # 모델명
)

class SWOTKeywords(BaseModel):
    strength_keyword: str = Field(description="제품의 경쟁 우위를 나타내는 긍정적인 키워드나 문구")
    weakness_keyword: str = Field(description="제품의 한계점이나 개선이 필요한 부분을 나타내는 키워드나 문구")
    opportunity_keyword: str = Field(description="리뷰를 통해 발견된 잠재적 성장 기회나 새로운 시장 기회를 나타내는 키워드나 문구")
    threat_keyword: str = Field(description="제품의 성공을 저해할 수 있는 우려사항이나 외부 위험 요소를 나타내는 키워드나 문구")

class SWOTResponse(BaseModel):
    keywords: List[SWOTKeywords] = Field(description="리뷰 텍스트에서 SWOT 카테고리별로 추출된 키워드 리스트")

# Parser 설정
swot_parser = PydanticOutputParser(pydantic_object=SWOTResponse)

swot_template = """
    다음 리뷰 텍스트를 분석하여 SWOT 분석을 수행하고, 정확히 아래 JSON 형식으로 출력해주세요.
    분석이 어려운 카테고리가 있더라도 반드시 모든 필드를 포함해야 합니다.
    키워드나 인사이트가 없는 경우 "없음" 또는 "관련 내용 없음"으로 표시해주세요.

    분석할 리뷰 텍스트:
    {review_text}

    반드시 다음 형식의 JSON으로 출력해주세요:
    {{
        "keywords": [
            {{
                "strength_keyword": "강점 키워드1",
                "weakness_keyword": "약점 키워드1",
                "opportunity_keyword": "기회 키워드1",
                "threat_keyword": "위협 키워드1"
            }},
            {{
                "strength_keyword": "강점 키워드2",
                "weakness_keyword": "약점 키워드2",
                "opportunity_keyword": "기회 키워드2",
                "threat_keyword": "위협 키워드2"
            }}
        ]
    }}

    주의사항:
    1. 반드시 위의 JSON 형식을 정확히 따라주세요
    2. 모든 필드는 필수이며, 값이 없는 경우 "없음"으로 표시
    3. 다른 설명이나 부가 텍스트 없이 JSON만 출력
    4. 실제 키워드는 한글로 작성

    {format_instructions}
    """

swot_prompt = PromptTemplate(
    template=swot_template,
    input_variables=["review_text"],
    partial_variables={"format_instructions": swot_parser.get_format_instructions()}
)

swot_chain = (
    swot_prompt
    | SWOT_llm
    | swot_parser
)

def collect_swot_keywords(swot_response):
    # 각 카테고리별 키워드를 저장할 딕셔너리
    collected = {
        'strengths': [],
        'weaknesses': [],
        'opportunities': [],
        'threats': []
    }
    
    # 각 키워드 세트에서 카테고리별로 수집
    for keyword_set in swot_response.keywords:
        # 강점 수집
        if keyword_set.strength_keyword and keyword_set.strength_keyword != "없음":
            # 쉼표로 구분된 경우 분리
            strengths = [s.strip() for s in keyword_set.strength_keyword.split(',')]
            collected['strengths'].extend(strengths)
        
        # 약점 수집
        if keyword_set.weakness_keyword and keyword_set.weakness_keyword != "없음":
            weaknesses = [w.strip() for w in keyword_set.weakness_keyword.split(',')]
            collected['weaknesses'].extend(weaknesses)
            
        # 기회 수집
        if keyword_set.opportunity_keyword and keyword_set.opportunity_keyword != "없음":
            opportunities = [o.strip() for o in keyword_set.opportunity_keyword.split(',')]
            collected['opportunities'].extend(opportunities)
            
        # 위협 수집
        if keyword_set.threat_keyword and keyword_set.threat_keyword != "없음":
            threats = [t.strip() for t in keyword_set.threat_keyword.split(',')]
            collected['threats'].extend(threats)
    
    # 중복 제거
    collected = {k: list(set(v)) for k, v in collected.items()}
    
    return collected

#######################################################################################################################################################
#######################################################################################################################################################

# 사이드바 설정
st.sidebar.header("검색기록")

# URL 입력 및 버튼
url = st.text_input("URL을 입력하세요.", placeholder="분석할 URL을 입력하세요.", key="anal_url_input")
start_button = st.button("분석시작", key="start_button")

placeholder = st.empty()

if start_button and url:  # 버튼 클릭 시 실행
    try:
        prod_name = reivew_crawling(url)
    except Exception as e:
        st.error(f"크롤링 오류가 발생했습니다: {e}")
        prod_name = None
    
    review_folder = os.path.join(os.path.dirname(__file__), 'reviewxisx')
    latest_file = max([os.path.join(review_folder, f) for f in os.listdir(review_folder)], key=os.path.getctime)
    df = pd.read_excel(latest_file)
    latest_reviews_text = df['리뷰 내용'].to_string()[:1500]  # 최대 1500자까지만 저장

    ABSA_result = ABSA_chain.run({"text": latest_reviews_text})

    swot_response = swot_chain.invoke({"review_text": latest_reviews_text})
    swot_analysis_result = collect_swot_keywords(swot_response)

    # 분석 결과가 비어있는지 확인
    if swot_analysis_result:
        try:
            swot_results = swot_analysis_result
        except json.JSONDecodeError as e:
            st.error(f"오류: {e}")
            swot_results = None
    else:
        st.error("URL을 확인하거나 다시 시도해 주세요.")
        swot_results = None

    if swot_results:
        # 입력 및 버튼 제거
        placeholder = st.empty()
        placeholder.empty()
        
        # 분석 결과 레이아웃 출력
        top_left, top_right = st.columns(2)
        
        with top_left:
            st.subheader("리뷰 분석")
            st.write(ABSA_result)

        with top_right:
            st.subheader("SWOT 분석")
            swot_cols = st.columns(2)

            with swot_cols[0]:
                st.markdown(
                    f"""
                    <div class="swot-box">
                        <strong>Strengths</strong><br>
                        {'<br>'.join(f'- {item}' for item in swot_results.get('strengths', []))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with swot_cols[1]:
                st.markdown(
                    f"""
                    <div class="swot-box">
                        <strong>Weaknesses</strong><br>
                        {'<br>'.join(f'- {item}' for item in swot_results.get('weaknesses', []))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            swot_cols2 = st.columns(2)
            with swot_cols2[0]:
                st.markdown(
                    f"""
                    <div class="swot-box">
                        <strong>Opportunities</strong><br>
                        {'<br>'.join(f'- {item}' for item in swot_results.get('opportunities', []))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with swot_cols2[1]:
                st.markdown(
                    f"""
                    <div class="swot-box">
                        <strong>Threats</strong><br>
                        {'<br>'.join(f'- {item}' for item in swot_results.get('threats', []))}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # 가로 구분선 추가
        st.markdown('<div class="divider-horizontal"></div>', unsafe_allow_html=True)

        # 아래 레이아웃이 항상 동일한 행에 위치하도록 컨테이너 유지
        bottom_left, bottom_right = st.columns((1, 1), gap="medium")
        
        with bottom_left:
            st.subheader("뉴스 기사")
            st.write(swot_analysis_result)

        with bottom_right:
            st.markdown('<div class="divider-vertical"></div>', unsafe_allow_html=True) 
            st.subheader("향후 전망")
            st.write(swot_analysis_result)
