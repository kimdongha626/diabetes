import streamlit as st

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="당뇨 예측 프로그램", page_icon="🩺", layout="centered")

st.title("🩺 당뇨 예측 프로그램")
st.write("생활 정보를 입력하면 당뇨 여부를 예측합니다.")
st.markdown("---")

# 2. 2열 레이아웃 구성
col1, col2 = st.columns(2)

with col1:
    # 임신횟수 (정수형)
    pregnancies = st.number_input("임신횟수", min_value=0, value=0, step=1)
    
    # 혈당 (실수형)
    glucose = st.number_input("혈당", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    
    # 혈압 (실수형)
    blood_pressure = st.number_input("혈압", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    
    # 피부두께 (실수형)
    skin_thickness = st.number_input("피부두께", min_value=0.0, value=0.0, step=1.0, format="%.2f")

with col2:
    # 인슐린 (실수형)
    insulin = st.number_input("인슐린", min_value=0.0, value=0.0, step=1.0, format="%.2f")
    
    # 체질량지수(BMI) (실수형)
    bmi = st.number_input("체질량지수(BMI)", min_value=0.0, value=0.0, step=0.1, format="%.2f")
    
    # 가족력 (실수형 - 보통 Diabetes Pedigree Function을 의미)
    dpf = st.number_input("가족력", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    
    # 나이 (정수형)
    age = st.number_input("나이", min_value=0, value=0, step=1)

st.markdown("---")

# 3. 예측 버튼 및 결과 출력 영역
# 버튼 내부에 이모지를 추가하여 이미지와 유사하게 구현했습니다.
if st.button("🔍 당뇨 예측하기", use_container_width=True):
    # 여기에 실제 머신러닝 모델 예측 코드를 넣으시면 됩니다.
    # 예: prediction = model.predict([[pregnancies, glucose, ...]])
    
    st.info("여기에 예측 결과 로직을 추가하세요!")
    
    # 임시 결과 예시:
    # st.success("예측 결과: 당뇨 안전군입니다.")
