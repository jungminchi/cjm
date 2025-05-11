import streamlit as st
import random

# 상태 초기화
if "fuel" not in st.session_state:
    st.session_state.fuel = 100
    st.session_state.health = 100
    st.session_state.money = 100
    st.session_state.distance = 0
    st.session_state.day = 1

st.title("🚘 자동차 생존 시뮬레이션")

st.markdown(f"**🗓️ 날짜**: Day {st.session_state.day}")
st.markdown(f"**🛢️ 연료**: {st.session_state.fuel}")
st.markdown(f"**🛠️ 차량 내구도**: {st.session_state.health}")
st.markdown(f"**💰 소지금**: {st.session_state.money}만원")
st.markdown(f"**📍 이동 거리**: {st.session_state.distance} km")

st.divider()
st.subheader("오늘의 행동을 선택하세요:")

action = st.radio("행동", ["운전하기", "정비하기", "주유하기", "휴식"])

if st.button("진행하기"):
    st.session_state.day += 1

    if action == "운전하기":
        dist = random.randint(10, 30)
        fuel_used = random.randint(10, 20)
        damage = random.randint(5, 15)

        st.session_state.fuel -= fuel_used
        st.session_state.health -= damage
        st.session_state.distance += dist

        st.success(f"{dist}km 운전! 연료 {fuel_used} 감소, 내구도 {damage} 감소")

    elif action == "정비하기":
        if st.session_state.money >= 10:
            st.session_state.health = min(100, st.session_state.health + 30)
            st.session_state.money -= 10
            st.success("정비 완료! 내구도 +30")
        else:
            st.warning("돈이 부족합니다!")

    elif action == "주유하기":
        if st.session_state.money >= 10:
            st.session_state.fuel = min(100, st.session_state.fuel + 40)
            st.session_state.money -= 10
            st.success("주유 완료! 연료 +40")
        else:
            st.warning("돈이 부족합니다!")

    elif action == "휴식":
        st.success("아무 일도 일어나지 않았습니다. 컨디션 회복!")

    # 랜덤 이벤트
    event_chance = random.random()
    if event_chance < 0.2:
        st.error("❗ 타이어 펑크! 내구도 -10")
        st.session_state.health -= 10
    elif event_chance < 0.3:
        st.info("💵 도로변 보너스 발견! 소지금 +10")
        st.session_state.money += 10
    elif event_chance < 0.35:
        st.warning("👮 경찰 단속 벌금! 소지금 -10")
        st.session_state.money -= 10

    # 게임 오버 조건
    if st.session_state.fuel <= 0 or st.session_state.health <= 0:
        st.error("게임 오버! 차가 더 이상 움직일 수 없습니다.")
        st.session_state.fuel = 0
        st.session_state.health = 0
        st.stop()

# 리셋 버튼
if st.button("게임 초기화"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
