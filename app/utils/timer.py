import streamlit as st
from datetime import datetime
import asyncio
import time


async def timer(t, start_time):
    st.markdown(
        """
        <style>
        .time {
            font-size: 38px !important;
            font-weight: 7 !important;
            color: #ec5953 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    while True:
        time_delta = time.time() - start_time
        t.markdown(
            f"""
            <span>TIME</span>
            <br>
            <span class="time">{str(round(time_delta, 3)).rjust(3)}s</span>
            """,
            unsafe_allow_html=True,
        )
        await asyncio.sleep(0.1)
