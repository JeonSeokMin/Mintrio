import streamlit as st

# 페이지 타이틀
st.title("Mintrio")

# 처음 한 번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화내용 저장하기 위함
    st.session_state["messages"] = []

# 이전 대화를 출력
for role, message in st.session_state["messages"]:
    st.chat_message(role).write(message)


# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 만약 사용자의 입력이 들어오면..
if user_input:

    # 웹에 대화를 출력
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)

    # 웹에 대화를 저장
    st.session_state["messages"].append(("user", user_input))
    st.session_state["messages"].append(("assistant", user_input))