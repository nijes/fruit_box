import streamlit as st
import os
from os.path import dirname
from utils.db import init_db
from utils.canvas import boxing_section


def main():
    st.title("FRUIT BOX")
    st.caption("그림에 있는 과일을 찾아 딱맞는 박스를 치세요!")

    # if st.button("db init"):
    #     init_db()
    if "work_progress" in st.session_state:
        boxing_section()

    else:
        with st.expander("GUIDE", expanded=True):
            st.markdown(
                """
            * 상단에서 과일 이름을 선택한 후, 맞는 과일을 찾아 박스를 치세요.
            * 맞힌 박스 수, 틀린 박스 수, 걸린 시간에 따라 점수가 정해집니다.
            """
            )
            st.image("assets/info/boxing_exam.png")

            st.header("")
        if st.button("START", use_container_width=True, type="primary"):
            boxing_section()


if __name__ == "__main__":
    # os.chdir(dirname(__file__))  # fruit_box/app 기본 경로로
    main()
