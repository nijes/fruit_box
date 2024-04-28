import streamlit as st
import time
import json
import math
from utils.db import insert_db, inquire_db
from datetime import datetime
import pandas as pd
from utils.auth import register_section


IMG_CONFIG = json.load(open("img_config.json", "r"))
LABEL_CONFIG = json.load(open("label_config.json", "r"))


def color_label_map():
    color_label_dict = {}
    for k, v in LABEL_CONFIG:
        color_label_dict[v["color"]] = k
    return color_label_dict


def get_bbox_center(bbox: list):
    """
    bbox : (left, top, width, height)
    """
    x_center = bbox[0] + bbox[2] // 2
    y_center = bbox[1] - bbox[3] // 2
    return [x_center, y_center]


def get_overlap_ratio(bbox_1: list, bbox_2: list):
    """
    bbox_1 : (left, top, width, height)
    bbox_2 : (left, top, width, height)
    overlap_ratio = 공통 영역 / 전체 영역
    """
    overlap_left = max(bbox_1[0], bbox_2[0])
    overlap_right = min(bbox_1[0] + bbox_1[2], bbox_2[0] + bbox_2[2])
    overlap_top = min(bbox_1[1], bbox_2[1])
    overlap_bottom = max(bbox_1[1] - bbox_1[3], bbox_2[1] - bbox_2[3])

    overlap_area = max(overlap_right - overlap_left, 0) * max(
        overlap_top - overlap_bottom, 0
    )
    total_area = bbox_1[2] * bbox_1[3] + bbox_2[2] * bbox_2[2]

    return overlap_area / (total_area - overlap_area)


def get_nearest_box(src_bbox: list, trg_bboxes: list):
    src_bbox_center = get_bbox_center(src_bbox)
    trg_bboxes_center = map(get_bbox_center, trg_bboxes)

    nearest_bbox = 0
    min_distance = math.inf
    for i, trg_bbox_center in enumerate(trg_bboxes_center):
        distance = abs(src_bbox_center[0] - trg_bbox_center[0]) + abs(
            src_bbox_center[1] - trg_bbox_center[1]
        )
        if distance < min_distance:
            min_distance = distance
            nearest_bbox = i
    return trg_bboxes[nearest_bbox]


def scoreboard_section():
    if "finish_time" not in st.session_state["work_progress"]:
        st.session_state["work_progress"]["finish_time"] = time.time()
    if "score" not in st.session_state["work_progress"]:
        st.session_state["work_progress"]["score"] = get_score(
            st.session_state["work_progress"]["complete"],
            st.session_state["work_progress"]["finish_time"]
            - st.session_state["work_progress"]["start_time"],
        )

    user_score = st.session_state["work_progress"]["score"]

    cols = st.columns([1, 1, 1, 2])
    cols[0].metric("맞힌 박스", user_score["correct_box"])
    cols[1].metric("걸린 시간", user_score["duration"])
    cols[2].metric("SCORE", user_score["score"])

    with cols[-1].container():
        register_avaliable = register_section()
        if register_avaliable:
            date = datetime.now().strftime("%y%m%d")
            insert_db(
                "user_score",
                user_id=st.session_state["user_id"],
                correct_box=user_score["correct_box"],
                incorrect_box=user_score["incorrect_box"],
                duration=user_score["duration"],
                score=user_score["score"],
                date=date,
            )

    # if st.session_state["user_id"] == "":
    #     st.info(":exclamation:이름을 입력해야지만, 기록을 저장할 수 있습니다")

    score_top_10 = inquire_db(
        "user_score", condition="user_id != ''", sort="score DESC", limit=10
    )
    score_top_10 = list(
        map(
            lambda x: {
                "NAME": x[1],
                "DATE": x[6],
                "CORRECT BOX": x[2],
                "INCORRECT BOX": x[3],
                "TIME": x[4],
                "SCORE": x[5],
            },
            score_top_10,
        )
    )
    st.title("LEADER BOARD")
    st.dataframe(pd.DataFrame(score_top_10), use_container_width=True, hide_index=True)


def get_score(user_completion: dict, time_duration: float, threshold=0.6):
    answer_count = 0
    color_label_dict = {}
    for k, v in LABEL_CONFIG.items():
        color_label_dict[v["color"]] = k

    for img_name in IMG_CONFIG.keys():
        answer_bboxes = IMG_CONFIG[img_name]["bboxes"]

        # answer_bboxes와 동일한 형식으로 user_bboxes 만들기
        user_submit = user_completion[img_name]
        user_bboxes = {}
        for submit_box in user_submit:
            label = color_label_dict[submit_box["stroke"]]
            if label in user_bboxes.keys():
                user_bboxes[label].append(
                    [
                        submit_box["left"],
                        submit_box["top"],
                        submit_box["width"],
                        submit_box["height"],
                    ]
                )
            else:
                user_bboxes[label] = [
                    [
                        submit_box["left"],
                        submit_box["top"],
                        submit_box["width"],
                        submit_box["height"],
                    ]
                ]

        for label, ref_bboxes in answer_bboxes.items():
            for ref_bbox in ref_bboxes:
                if label not in user_bboxes.keys():
                    break
                if user_bboxes[label] == []:
                    break
                # 정답 박스와 라벨 같으면서 가장 가까운 박스 찾기
                user_bbox = get_nearest_box(ref_bbox, user_bboxes[label])
                # 정답 박스와 가장 가까운 박스 겹치는 비율 threshold보다 높으면 정답처리
                overap_ratio = get_overlap_ratio(ref_bbox, user_bbox)
                if overap_ratio > threshold:
                    answer_count += 1
                    # 정답 카운트 된 박스 제거
                    user_bboxes[label].remove(user_bbox)
        # 남은 박스 수만큼 감점
        left_bboxes = sum((len(v) for v in user_bboxes.values()))

    final_score = answer_count * 10 - left_bboxes * 5 - int(time_duration)
    return {
        "correct_box": answer_count,
        "incorrect_box": left_bboxes,
        "duration": int(time_duration),
        "score": final_score,
    }
