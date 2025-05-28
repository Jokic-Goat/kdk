import streamlit as st
import sympy as sp

st.set_page_config(page_title="코브-더글라스 최적 소비 도구", layout="centered")
st.title("📈 코브-더글라스 기반 최적 소비 계산기 (라그랑주 승수법)")

st.markdown("사용자가 직접 품목명, 가격, 효용 계수(a, b), 예산을 입력하면 최적 소비를 계산합니다.")

st.subheader("1️⃣ 품목 정보 입력")

item1 = st.text_input("첫 번째 품목 이름", value="아이스크림")
item2 = st.text_input("두 번째 품목 이름", value="과자")

price1 = st.number_input(f"{item1} 가격", min_value=0.01, value=2.0)
price2 = st.number_input(f"{item2} 가격", min_value=0.01, value=1.0)

alpha = st.number_input(f"{item1}의 효용 계수 α", min_value=0.01, max_value=0.99, value=0.5)
beta = round(1 - alpha, 2)

budget = st.number_input("총 예산", min_value=0.01, value=10.0)

if st.button("최적 소비량 계산"):
    try:
        x, y, lam = sp.symbols('x y lam', real=True, positive=True)

        # 효용함수 (코브-더글라스): U = x^a * y^b
        U = x**alpha * y**beta
        constraint = price1 * x + price2 * y - budget

        # 라그랑주 함수
        L = U - lam * constraint

        # 편미분
        eqs = [
            sp.Eq(sp.diff(L, x), 0),
            sp.Eq(sp.diff(L, y), 0),
            sp.Eq(sp.diff(L, lam), 0)
        ]

        sol = sp.solve(eqs, (x, y, lam), dict=True)

        if sol:
            res = sol[0]
            x_val = round(float(res[x]), 2)
            y_val = round(float(res[y]), 2)
            util_val = round(float(U.subs({x: x_val, y: y_val})), 2)

            st.success(f"✅ 최적 소비량: {item1} {x_val}개, {item2} {y_val}개")
            st.info(f"👉 총 효용: {util_val}")
        else:
            st.error("❌ 최적 해를 찾을 수 없습니다. 입력값을 다시 확인하세요.")
    except Exception as e:
        st.error(f"🚨 오류 발생: {e}")
