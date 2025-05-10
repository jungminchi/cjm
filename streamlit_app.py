import streamlit as st
import requests
import json
import openai

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="GPT 중고차 정보 도우미", layout="wide")
st.title("🚗 Encar 실제 매물 검색 + GPT 설명")

# 검색 필터 UI
manufacturer = st.selectbox("제조사", ["현대", "기아", "쉐보레", "르노삼성", "테슬라"])
model = st.text_input("모델명", "아반떼")
min_price = st.number_input("최소 가격 (만원)", 0)
max_price = st.number_input("최대 가격 (만원)", 5000, step=100)

if st.button("차량 검색"):
    payload = {
        "count": 10,
        "page": 1,
        "sort": "Year|Desc",
        "searchFilter": {
            "Price": {"min": min_price * 10000, "max": max_price * 10000},
            "Manufacture": manufacturer,
            "Model": model
        }
    }
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }
    try:
        res = requests.post(
            "https://api.encar.com/search/car/list/premium",
            headers=headers,
            data=json.dumps(payload)
        )
        res.raise_for_status()
        data = res.json()
        vehicles = data.get("SearchResult", {}).get("Vehicles", [])

        if not vehicles:
            st.warning("조건에 맞는 매물이 없습니다.")
        else:
            st.success(f"{len(vehicles)}개의 실제 매물이 검색되었습니다.")
            for idx, car in enumerate(vehicles):
                with st.expander(f"{car.get('Model', '차량')} - {car.get('Year')}년식 / {car.get('Price') // 10000}만원"):
                    cols = st.columns([1, 2])
                    # 이미지 표시
                    img_url = car.get('ImageUrl') or car.get('ImageUrl1') or car.get('MainPhotoUrl')
                    with cols[0]:
                        if img_url:
                            st.image(img_url, use_column_width=True)
                        else:
                            st.write("이미지 없음")
                    # 상세 정보
                    with cols[1]:
                        st.markdown(f"**ID**: {car.get('Id')}")
                        st.markdown(f"**제조사**: {manufacturer}")
                        st.markdown(f"**모델명**: {car.get('Model')}")
                        st.markdown(f"**연식**: {car.get('Year')}년")
                        st.markdown(f"**가격**: {car.get('Price') // 10000}만원")
                        st.markdown(f"**주행거리**: {car.get('Mileage'):,} km")
                        detail_url = f"https://www.encar.com/dc/dc_carsearchlist.do?carid={car.get('Id')}"
                        st.markdown(f"[자세히 보기]({detail_url})")

                    # GPT 설명
                    if st.button(f"이 차량 설명 요청 (GPT)", key=f"gpt_{idx}"):
                        prompt = (
                            f"다음은 중고차 매물 정보입니다. 이 차량의 장단점, 적합한 사용자, 주의할 점 등을 친절하게 설명해주세요."
                            f"\n- 제조사: {manufacturer}"
                            f"\n- 모델명: {car.get('Model')}"
                            f"\n- 연식: {car.get('Year')}년"
                            f"\n- 가격: {car.get('Price') // 10000}만원"
                            f"\n- 주행거리: {car.get('Mileage'):,} km"
                        )
                        gpt_resp = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt}],
                            temperature=0.7
                        )
                        explanation = gpt_resp.choices[0].message.content
                        st.markdown("### 🤖 GPT 차량 설명")
                        st.write(explanation)
    except Exception as e:
        st.error(f"검색 중 오류 발생: {e}")
