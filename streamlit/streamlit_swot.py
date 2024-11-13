import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="리뷰 / SWOT 분석 Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# CSS 스타일링 적용
st.markdown(
    """
    <style>
    /* 전체 레이아웃 스타일링 */
    .css-18e3th9 {
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* 사이드바 */
    .css-1d391kg {
        background-color: #F4E5DB; /* 사이드바 배경색 */
    }
    .sidebar-content {
        background-color: #F4E5DB;
    }

    /* 입력창 스타일 */
    .css-1r6slb0 {
        background-color: #fff;
        border-radius: 10px;
        border: 1px solid #ddd;
    }

    /* 버튼 스타일 */
    .stButton>button {
        color: white;
        background-color: #D4A373;
        border: None;
        border-radius: 5px;
        width: 100%;
        padding: 0.5rem 1rem;
    }

    /* 메인 텍스트와 서브 텍스트 스타일 */
    .stMarkdown h1, h2, h3 {
        font-family: 'Arial', sans-serif;
        color: #5A4635; /* 메인 텍스트 색상 */
    }

    /* SWOT 영역 스타일링 */
    .swot-box {
        background-color: #E8D4C1;  /* SWOT 박스 배경색 */
        color: black;  /* 글자 색상 */
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
        text-align: left;
        height: 200px;  /* 고정된 높이 설정 */
        overflow-y: auto;  /* 내용이 길어질 경우 스크롤 활성화 */
    }

    /* 구분선 스타일 */
    .divider-horizontal {
        border-top: 1px solid #d3d3d3; /* 연한 회색 가로 구분선 */
        margin: 20px 0;
    }

    .divider-vertical {
        border-left: 2px solid #d3d3d3; /* 더 두꺼운 세로 구분선 */
        height: 100%;  /* 세로 구분선 높이 */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 사이드바 설정
st.sidebar.header("검색기록")
st.sidebar.write("로그")
st.sidebar.write("- 검색기록 1")
st.sidebar.write("- 검색기록 2")
st.sidebar.write("- 검색기록 3")

# 메인 페이지
st.title("리뷰 / SWOT 분석 Dashboard")

# URL 입력 및 버튼
url = st.text_input("URL을 입력하세요.", placeholder="분석할 URL을 입력하세요.", key="url_input")
start_button = st.button("분석시작", key="start_button")
# 동적 레이아웃 컨테이너
placeholder = st.empty()

# 가상 SWOT 분석 결과
swot_results = {
    'strengths': ['하루 한 알 복용으로 편리함', '알 크기가 작음', '가격이 훨씬 착함', '개별 포장으로 위생적임', '가격이 합리적임'],
    'weaknesses': [],
    'opportunities': ['온라인 구매 시 추가 할인 제공 등 프로모션 전략 개발 가능성', '개별 포장된 제품의 위생적 장점을 마케팅 포인트로 활용 가능', '건강보조식품 시장에서 젊은 층을 타겟팅한 광고 전략 개발 가능성'],
    'threats': ['기존 브랜드에 대한 충성도 있는 고객층 존재 가능성', '경쟁사의 유사한 저렴한 제품 존재 가능성', '무료 샘플이나 경쟁사의 프로모션 활동']
}

if start_button:
    # 입력 및 버튼을 화면 위로 이동
    placeholder.empty()  # 기존 입력 요소 제거

    # 분석 결과 레이아웃 출력
    top_left, top_right = st.columns(2)
    
    with top_left:
        st.subheader("리뷰 분석")
        st.write("- 리뷰 분석 결과 1")
        st.write("- 리뷰 분석 결과 2")

    with top_right:
        st.subheader("SWOT 분석")
        swot_cols = st.columns(2)

        with swot_cols[0]:
            st.markdown(
                f"""
                <div class="swot-box">
                    <strong>Strong</strong><br>
                    {'<br>'.join(f'- {item}' for item in swot_results['strengths'])}
                </div>
                """,
                unsafe_allow_html=True
            )

        with swot_cols[1]:
            st.markdown(
                f"""
                <div class="swot-box">
                    <strong>Weak</strong><br>
                    {'<br>'.join(f'- {item}' for item in swot_results['weaknesses']) if swot_results['weaknesses'] else '- 없음'}
                </div>
                """,
                unsafe_allow_html=True
            )

        swot_cols2 = st.columns(2)
        with swot_cols2[0]:
            st.markdown(
                f"""
                <div class="swot-box">
                    <strong>Opportunity</strong><br>
                    {'<br>'.join(f'- {item}' for item in swot_results['opportunities'])}
                </div>
                """,
                unsafe_allow_html=True
            )

        with swot_cols2[1]:
            st.markdown(
                f"""
                <div class="swot-box">
                    <strong>Threat</strong><br>
                    {'<br>'.join(f'- {item}' for item in swot_results['threats'])}
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
        st.write("시각화 내용")

    with bottom_right:
        st.markdown('<div class="divider-vertical"></div>', unsafe_allow_html=True) #안나오는데 원인을 모르겠음..
        st.subheader("향후 전망")
        st.write("시각화 내용")


