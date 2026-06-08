import streamlit as st
import pickle
import numpy as np

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="당뇨 예측 프로그램", page_icon="🩺", layout="centered")

st.title("🩺 당뇨 예측 프로그램")
st.write("생활 정보를 입력하면 당뇨 여부를 예측합니다.")
st.markdown("---")

# [모델 로드 로직]
# 실제 사용 시에는 학습된 모델 파일(diabetes.pkl)의 경로를 지정하세요.
@st.cache_resource  # 모델을 매번 새로 로드하지 않고 캐싱하여 속도를 높입니다.
def load_model():
    try:
        with open("diabetes.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        return None

model = load_model()

# 2. 2열 입력 레이아웃 구성
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("임신횟수", min_value=0, value=0, step=1)
    glucose = st.number_input("혈당", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    blood_pressure = st.number_input("혈압", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    skin_thickness = st.number_input("피부두께", min_value=0.0, value=0.0, step=1.0, format="%.2f")

with col2:
    insulin = st.number_input("인슐린", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    bmi = st.number_input("체질량지수(BMI)", min_value=0.0, value=0.0, step=0.1, format="%.2f")
    dpf = st.number_input("가족력", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    age = st.number_input("나이", min_value=0, value=0, step=1)

st.markdown("---")

# 3. 예측 버튼 클릭 시 실행되는 로직
if st.button("🔍 당뇨 예측하기", use_container_width=True):
    
    # 입력받은 8개의 데이터를 모델이 인식할 수 있는 2차원 배열 형태로 변환
    input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    
    # 상황 A: 실제 모델 파일이 존재하는 경우
    if model is not None:
        # 0 또는 1 예측 (0: 정상, 1: 당뇨)
        prediction = model.predict(input_data)
        # 확률 예측 (옵션: 당뇨일 확률 % 표현용)
        prediction_proba = model.predict_proba(input_data)[0][1] * 100
        
        # 결과 시각화
        st.subheader("📊 예측 결과")
        if prediction[0] == 1:
            st.error(f"⚠️ 당뇨병 환자일 가능성이 높습니다. (확률: {prediction_proba:.1f}%)")
            st.warning("전문 의료기관을 방문하여 정확한 진단을 받아보시는 것을 권장합니다.")
        else:
            st.success(f"✅ 당뇨병 정상군일 가능성이 높습니다. (안전 확률: {100 - prediction_proba:.1f}%)")
            st.info("꾸준한 건강 관리를 통해 건강을 유지하세요!")
            
    # 상황 B: 아직 모델 파일이 없는 경우 (테스트용 가상 로직)
    else:
        st.warning("기존에 학습된 `diabetes.pkl` 파일이 없어 가상 로직으로 대체합니다.")
        
        # 간단한 규칙 기반(Rule-based) 가상 예측 알고리즘 예시
        if glucose >= 140.0 or bmi >= 30.0:
            st.error("⚠️ 당뇨 위험군으로 예측됩니다. (가상 결과)")
        else:
            st.success("✅ 정상군으로 예측됩니다. (가상 결과)")
