import streamlit as st

st.set_page_config(page_title="Lab & 생산 농도 계산기", layout="centered")

st.title("🧪 Lab 단위 변환 & 맞춤형 희석 계산기")
st.caption("화장품 원료 R&D 및 대량 생산 스케일업을 위한 통합 솔루션")

st.markdown("---")

# 💡 내부 공통 표준 농도 단위(g/L) 변환 함수
def to_g_per_l(value, unit, mw):
    if unit == "mM":
        return (value * mw) / 1000
    elif unit == "μM":
        return (value * mw) / 1000000
    elif unit == "% (w/v)":
        return value * 10
    elif unit in ["μg/mL", "ppm"]:
        return value / 1000
    return value

def from_g_per_l(g_per_l, unit, mw):
    if unit == "mM":
        return (g_per_l * 1000) / mw
    elif unit == "μM":
        return (g_per_l * 1000000) / mw
    elif unit == "% (w/v)":
        return g_per_l / 10
    elif unit in ["μg/mL", "ppm"]:
        return g_per_l * 1000
    return g_per_l

# 💡 내부 공통 표준 부피 단위(mL) 변환 함수
def to_ml(value, unit):
    if unit == "μL":
        return value / 1000
    elif unit in ["mL (g)", "mL"]:
        return value
    elif unit in ["L (kg)", "L"]:
        return value * 1000
    return value

def from_ml(ml_val, unit):
    if unit == "μL":
        return ml_val * 1000
    elif unit in ["mL (g)", "mL"]:
        return ml_val
    elif unit in ["L (kg)", "L"]:
        return ml_val / 1000
    return ml_val

# [공통 정보] 화합물의 분자량 입력
st.header("🔬 화합물 기본 정보")
mw = st.number_input("화합물 분자량 (Molecular Weight, g/mol)", min_value=0.1, value=300.0, step=10.0)

st.markdown("---")

# 1. 모든 단위 간 상호 농도 변환기
st.header("1. 자율 단위 상호 농도 변환")
col1, col2 = st.columns(2)

with col1:
    input_unit = st.selectbox("기준 농도 단위 선택", ["mM", "μM", "% (w/v)", "μg/mL", "ppm"], key="input_unit")
    input_value = st.number_input(f"농도 입력 ({input_unit})", min_value=0.0, value=10.0, step=1.0, format="%.4f")

with col2:
    st.success("✨ **실시간 단위 변환 결과**")
    g_per_l = to_g_per_l(input_value, input_unit, mw)
    res_mM = from_g_per_l(g_per_l, "mM", mw)
    res_uM = from_g_per_l(g_per_l, "μM", mw)
    res_percent = from_g_per_l(g_per_l, "% (w/v)", mw)
    res_ug_ml = from_g_per_l(g_per_l, "μg/mL", mw)
    
    st.write(f"- **{res_mM:,.4f}** mM")
    st.write(f"- **{res_uM:,.2f}** μM")
    st.write(f"- **{res_percent:,.4f}** % (w/v)")
    st.write(f"- **{res_ug_ml:,.2f}** μg/mL (ppm)")

st.markdown("---")

# 2. 유연한 희석 계산기 (생산/실험 맞춤형)
st.header("2. 맞춤형 희석 계산기 (실험 및 대량 생산 스케일업)")

calc_mode = st.radio(
    "계산 방식 선택",
    ["투입할 스톡(Stock) 부피 기준 계산", "만들고자 하는 최종(Final) 부피 기준 계산"]
)

col3, col4 = st.columns(2)

with col3:
    st.subheader("농도 설정")
    stock_unit = st.selectbox("스톡 농도 단위", ["mM", "μM", "% (w/v)", "μg/mL", "ppm"], index=0, key="stock_unit_calc")
    stock_conc = st.number_input(f"스톡 농도 ({stock_unit})", min_value=0.0001, value=10.0, step=1.0, format="%.4f")
    
    final_unit = st.selectbox("원하는 최종 농도 단위", ["mM", "μM", "% (w/v)", "μg/mL", "ppm"], index=1, key="final_unit_calc")
    final_conc = st.number_input(f"목표 최종 농도 ({final_unit})", min_value=0.0001, value=50.0, step=5.0, format="%.4f")

c1 = to_g_per_l(stock_conc, stock_unit, mw)
c2 = to_g_per_l(final_conc, final_unit, mw)

with col4:
    st.subheader("부피 설정 및 결과")
    vol_units = ["μL", "mL (g)", "L (kg)"]
    
    if calc_mode == "투입할 스톡(Stock) 부피 기준 계산":
        input_vol_unit = st.selectbox("사용할 스톡 부피 단위", vol_units, index=0)
        input_stock_vol = st.number_input(f"사용할 스톡 부피 ({input_vol_unit})", min_value=0.001, value=5.0, step=0.5, format="%.3f")
        
        if c2 >= c1:
            st.error("⚠️ 목표 최종 농도가 현재 스톡 농도보다 높거나 같습니다. 희석이 불가능합니다.")
        else:
            v1_ml = to_ml(input_stock_vol, input_vol_unit)
            v2_ml = (c1 * v1_ml) / c2
            v_solvent_ml = v2_ml - v1_ml
            
            st.info("💡 **희석 조제 가이드**")
            st.write(f"- 사용할 스톡 부피: **{input_stock_vol:,.3f} {input_vol_unit}**")
            st.write(f"- 필요한 용매 부피: **{from_ml(v_solvent_ml, input_vol_unit):,.3f} {input_vol_unit}**")
            st.write(f"- 최종 용액 총 부피: **{from_ml(v2_ml, input_vol_unit):,.3f} {input_vol_unit}**")
            
    else:
        input_vol_unit = st.selectbox("만들고자 하는 최종 부피 단위", vol_units, index=1)
        input_final_vol = st.number_input(f"목표 최종 부피 ({input_vol_unit})", min_value=0.001, value=100.0, step=10.0, format="%.3f")
        
        if c2 >= c1:
            st.error("⚠️ 목표 최종 농도가 현재 스톡 농도보다 높거나 같습니다. 희석이 불가능합니다.")
        else:
            v2_ml = to_ml(input_final_vol, input_vol_unit)
            v1_ml = (c2 * v2_ml) / c1
            v_solvent_ml = v2_ml - v1_ml
            
            st.info("💡 **희석 조제 가이드**")
            st.write(f"- 필요한 스톡 부피: **{from_ml(v1_ml, input_vol_unit):,.3f} {input_vol_unit}**")
            st.write(f"- 필요한 용매 부피: **{from_ml(v_solvent_ml, input_vol_unit):,.3f} {input_vol_unit}**")
            st.write(f"- 목표 최종 총 부피: **{input_final_vol:,.3f} {input_vol_unit}**")
