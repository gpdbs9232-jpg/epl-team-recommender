import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="EPL 팀 추천기", page_icon="⚽", layout="wide")

st.sidebar.title("⚽ 취향 선택")
st.sidebar.write("본인의 축구 취향을 선택해 주세요.")

style = st.sidebar.selectbox(
    "좋아하는 플레이 스타일",
    ["공격적", "역습", "점유율", "균형"]
)

club_type = st.sidebar.selectbox(
    "선호하는 팀 유형",
    ["명문 구단", "신흥 강호", "언더독"]
)

player_type = st.sidebar.selectbox(
    "좋아하는 선수 유형",
    ["스트라이커", "윙어", "플레이메이커"]
)

recommend_button = st.sidebar.button("추천받기")

st.title("🏆 EPL 팀 추천 웹 애플리케이션")
st.write("왼쪽 사이드바에서 취향을 선택하면, FastAPI가 추천 결과를 계산해 보여줍니다.")

if recommend_button:
    data = {
        "style": style,
        "club_type": club_type,
        "player_type": player_type
    }

    response = requests.post(
        "http://backend:8000/recommend" ,
        json=data
    )

    result = response.json()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.image(result["logo_url"], width=220)

    with col2:
        st.markdown(f"## 추천 팀: {result['team']}")
        st.success("당신의 취향과 가장 잘 맞는 팀입니다.")

        st.markdown(
            f"""
            <div style="
                padding: 18px;
                border-radius: 12px;
                background-color: #f5f5f5;
                border: 1px solid #dddddd;
                color: #111111;
            ">
                <h4>팀 정보 카드</h4>
                <p><b>{result['rank']}</b></p>
                <p><b>감독:</b> {result['coach']}</p>
                <p><b>주요 선수:</b> {result['players']}</p>
                <p><b>팀 컬러:</b> {result['color']}</p>
                <p><b>입문 난이도:</b> {result['difficulty']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    col3, col4 = st.columns([1, 1])

    with col3:
        st.subheader("✅ 추천 이유")
        for reason in result["selected_reasons"]:
            st.write(f"✔ {reason}")

        st.subheader("📌 팀 특징")
        st.write(result["description"])

        st.metric(label="추천 점수", value=f"{result['score']}점")

    with col4:
        st.subheader("📊 팀별 추천 점수")

        score_data = pd.DataFrame(
            list(result["all_scores"].items()),
            columns=["팀", "점수"]
        )

        score_data = score_data.sort_values(by="점수", ascending=False)

        st.bar_chart(
            score_data,
            x="팀",
            y="점수"
        )

else:
    st.info("왼쪽 사이드바에서 취향을 선택한 뒤 추천받기 버튼을 눌러주세요.")