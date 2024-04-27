import streamlit as st
import os
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
import json
# from utils.timer import timer
from utils.scoreboard import scoreboard_section
# import asyncio
import time


LABEL_CONFIG = json.load(open("label_config.json", "r"))
IMG_CONFIG = json.load(open("img_config.json", "r"))
IMG_DIR = "assets/"


def get_imgs(img_path=None):
    img_list = list(
        filter(lambda x: x.endswith(("jpg", "jpeg", "png")), os.listdir(IMG_DIR))
    )
    return img_list


def display_canvas(img_name):
    label_names = IMG_CONFIG[img_name]["label_names"]
    selected_label_name = st.radio("SELECT LABEL", label_names, horizontal=True)
    selected_label_color = LABEL_CONFIG[selected_label_name]["color"]

    pil_img = Image.open(os.path.join(IMG_DIR, img_name)).convert("RGB")
    np_img = np.array(pil_img)
    # 캔버스 생성
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.3)",
        stroke_width=1,
        stroke_color=selected_label_color,
        background_image=pil_img,
        height=np_img.shape[0],
        width=np_img.shape[1],
        drawing_mode="rect",
        key=f"canvas_{img_name}",
    )
    return canvas_result.json_data["objects"] if canvas_result.json_data else []


def do_boxing(img_name):
    boxing_result = display_canvas(img_name)

    with st.container():
        if st.button(
            "SUBMIT", use_container_width=True, type="primary", key="submit_btn"
        ):
            st.session_state["work_progress"]["incomplete"].pop(0)
            st.session_state["work_progress"]["complete"][img_name] = boxing_result
            st.rerun()


def boxing_section():
    if "work_progress" not in st.session_state:
        img_list = list(IMG_CONFIG.keys())
        st.session_state["work_progress"] = {
            "start_time": time.time(),
            "incomplete": img_list,
            "complete": {},
        }
    # print(st.session_state["work_progress"])
    if st.session_state["work_progress"]["incomplete"]:
        do_boxing(st.session_state["work_progress"]["incomplete"][0])
    else:
        scoreboard_section()

    # asyncio.run(timer(timer_section, start_time))
