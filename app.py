import streamlit as st
import pickle
import numpy as np
import pandas as pd  # 데이터 테이블 표시를 위해 추가

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="당뇨 예측 프로그램", page_icon="🩺", layout="centered")

st.title("🩺 당뇨 예측 프로그램")
st.write("생활 정보를 입력하면 당뇨 여부를 예측합니다.")
st.markdown("---")

# [모델 로드 로직]
@st.cache_resource
def load_model():
    try:
        with open("diabetes.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        # 에러 발생 시 왼쪽 사이드바에 원인 출력
        st.sidebar.error(f"모델 로드 실패: {e}")
        return None

model = load_model()

# 2. 2열 입력 레이아웃 구성
col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("임신횟수", min_value=0, value=1, step=1)
    glucose = st.number_input("혈당", min_value=0.0, value=100.0, step=1.0, format="%.2f")
    blood_pressure = st.number_input("혈압", min_value=0.0, value=70.0, step=1.0, format="%.2f")
    skin_thickness = st.number_input("피부두께", min_value=0.0, value=20.0, step=1.0, format="%.2f")

with col2:
    insulin = st.number_input("인슐린", min_value=0.0, value=80.0, step=1.0, format="%.2f")
    bmi = st.number_input("체질량지수(BMI)", min_value=0.0, value=23.0, step=0.1, format="%.2f")
    dpf = st.number_input("가족력", min_value=0.0, value=0.5, step=0.01, format="%.2f")
    age = st.number_input("나이", min_value=0, value=25, step=1)

st.markdown("---")

# 3. 예측 버튼 클릭 시 실행되는 로직
if st.button("🔍 당뇨 예측하기", use_container_width=True):
    
    # 입력받은 데이터를 2차원 배열 형태로 변환
    input_array = np.array([[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]])
    
    # 오른쪽 화면처럼 상단에 당뇨 확률을 먼저 보여주기 위한 세팅
    st.subheader("📊 예측 결과")
    
    # 상황 A: 실제 모델 파일이 정상 작동하는 경우
    if model is not None:
        try:
            prediction = model.predict(input_array)
            # 당뇨(1)일 확률 추출
            prediction_proba = model.predict_proba(input_array)[0][1] * 100
            
            # 당뇨 확률 큰 글씨로 표시 (오른쪽 예시 스타일)
            st.write("당뇨 확률")
            st.title(f"{prediction_proba:.1f}%")
            st.markdown("---")
            
            # 결과 텍스트 안내
            if prediction[0] == 1:
                st.error("당뇨 가능성이 높습니다.")
            else:
                st.success("정상 가능성이 높습니다.")
                
        except Exception as e:
            st.error(f"모델 연산 오류: {e}. 가상 로직 결과로 대체합니다.")
            model = None

    # 상황 B: 모델이 없거나 버전 오류(STACK_GLOBAL)로 작동하지 않을 때 (임시 시각화용)
    if model is None:
        # 가상 확률 계산 로직 (혈당과 BMI 수치에 따라 임시 반응하도록 구성)
        mock_proba = min(99.9, max(0.0, (glucose * 0.4) + (bmi * 1.2) - 30))
        
        st.write("당뇨 확률 (가상 데이터)")
        st.title(f"{mock_proba:.1f}%")
        st.markdown("---")
        
        if mock_proba >= 50.0:
            st.error("당뇨 가능성이 높습니다. (가상 결과)")
        else:
            st.success("정상 가능성이 높습니다. (가상 결과)")

    # 4. 입력 데이터 테이블 표시 (오른쪽 예시의 '입력 데이터 보기' 접기 기능)
    st.write("")
    with st.expander("👀 입력 데이터 보기", expanded=False):
        # 판다스 데이터프레임으로 변환하여 테이블 생성
        df = pd.DataFrame(
            input_array, 
            columns=["임신횟수", "혈당", "혈압", "피부두께", "인슐린", "체질량지수", "가족력", "나이"]
        )
        
        # 오른쪽 예시에 있는 파생 변수(비만위험, 고혈당 등) 공간 예시 추가
        df["비만위험"] = [1 if bmi >= 25 else 0]
        df["고혈당"] = [1 if glucose >= 140 else 0]
        
        st.dataframe(df, use_container_width=True)
