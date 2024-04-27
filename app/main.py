import streamlit as st
import os
from os.path import dirname
from utils.db import init_db, insert_db, inquire_db
from utils.canvas import boxing_section


def login_section():
    with st.container():
        user_id = st.text_input(
            "name", max_chars=12, help="새로운 이름의 경우 자동 등록"
        )
        user_pw = st.text_input("password", max_chars=12)
        st.header("")

        cols = st.columns([2, 1])
        if cols[0].button(
            "START",
            disabled=(not user_id or not user_pw),
            type="primary",
            use_container_width=True,
        ):
            user_existence = inquire_db("user", f"user_id='{user_id}'")
            # 기존 user이지만 pw 불일치
            if user_existence and user_existence[0][1] != user_pw:
                st.warning(":exclamation:비밀번호를 확인하거나, 다른 이름을 입력하세요")
                return
            # 새로운 id일 경우 db에 id, pw 저장
            if not user_existence:
                insert_db("user", user_id=user_id, user_pw=user_pw)

            st.session_state["user_id"] = user_id
            st.rerun()
        if cols[1].button("SKIP", use_container_width=True):
            st.session_state["user_id"] = ""
            st.rerun()


def main():
    st.title("FRUIT BOX")
    st.caption("그림에 있는 과일을 찾아 딱맞는 박스를 치세요!")

    # if st.button("db init"):
    #     init_db()

    if "user_id" not in st.session_state:
        login_section()
    else:
        boxing_section()


if __name__ == "__main__":
    os.chdir(dirname(__file__))  # fruit_box/app 기본 경로로
    main()
