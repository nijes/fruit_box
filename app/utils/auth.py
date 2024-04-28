import streamlit as st
from utils.db import insert_db, inquire_db


def register_section():
    with st.container():
        user_id = st.text_input(
            "name", max_chars=10, help="새로운 이름의 경우 자동 등록"
        )
        user_pw = st.text_input("password", max_chars=10)

        if st.button(
            "점수 등록",
            disabled=(not user_id or not user_pw),
            type="primary",
            use_container_width=True,
        ):
            user_existence = inquire_db("user", f"user_id='{user_id}'")
            # 기존 user이지만 pw 불일치
            if user_existence and user_existence[0][1] != user_pw:
                st.warning(":exclamation:비밀번호를 확인하거나, 다른 이름을 입력하세요")
                return False
            # 새로운 id일 경우 db에 id, pw 저장
            if not user_existence:
                insert_db("user", user_id=user_id, user_pw=user_pw)

            st.session_state["user_id"] = user_id
            return True
