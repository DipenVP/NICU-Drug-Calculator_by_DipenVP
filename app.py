import streamlit as st
import pandas as pd

# Load Excel database
df = pd.read_excel("NICU_Streamlit_Drug_Database.xlsx")

# Page settings
st.set_page_config(
    page_title="NICU Drug Calculator",
    layout="wide"
)

st.title("NICU Drug Calculator")
st.markdown("### Neonatal Drug Dose Automation")

# Sidebar patient details
st.sidebar.header("Patient Details")

weight = st.sidebar.number_input(
    "Weight (kg)",
    min_value=0.3,
    max_value=10.0,
    value=1.0,
    step=0.1
)

ga = st.sidebar.number_input(
    "Gestational Age (weeks)",
    min_value=22,
    max_value=44,
    value=34
)

pna = st.sidebar.number_input(
    "Postnatal Age (days)",
    min_value=0,
    max_value=120,
    value=1
)

length = st.sidebar.number_input(
    "Length (cm)",
    min_value=20.0,
    max_value=70.0,
    value=40.0
)

serum_creat = st.sidebar.number_input(
    "Serum Creatinine (mg/dL)",
    min_value=0.1,
    max_value=10.0,
    value=0.8
)

# Creatinine clearance
if ga >= 37:
    crcl = (0.45 * length) / serum_creat
    maturity = "Term"
else:
    crcl = (0.35 * length) / serum_creat
    maturity = "Preterm"

st.sidebar.markdown("---")
st.sidebar.write(f"Maturity: {maturity}")
st.sidebar.write(f"Estimated CrCl: {crcl:.2f}")

# Drug selection
drug_list = sorted(df["Drug_Name"].dropna().unique())

selected_drug = st.selectbox(
    "Select Drug",
    drug_list
)

drug_df = df[df["Drug_Name"] == selected_drug]

# Display drug table
st.subheader(selected_drug)
st.dataframe(drug_df)

# Dose calculation
st.markdown("---")
st.subheader("Dose Calculator")

selected_row = drug_df.iloc[0]

dose_text = str(selected_row["Dose"])

st.info(f"Dose Rule: {dose_text}")

dose_value = None

try:
    dose_value = float(dose_text.split(" ")[0])
except:
    pass

if dose_value:
    exact_dose = dose_value * weight

    st.success(
        f"Calculated Dose = {exact_dose:.2f} mg"
    )

# Drug details
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Preparation")
    st.write("Brand:", selected_row["Brand_Name"])
    st.write("Strength:", selected_row["Strength"])
    st.write("Compatible With:", selected_row["Compatible_With"])
    st.write("Dilution:", selected_row["Dilution"])

with col2:
    st.markdown("### Administration")
    st.write("Administration:", selected_row["Administration"])
    st.write("Renal Modification:", selected_row["Renal_Modification"])
    st.write("Storage:", selected_row["Storage"])
    st.write("Notes:", selected_row["Notes"])

# Safety
st.markdown("---")

st.warning(
    "Final prescription must always be clinically verified by the treating neonatologist."
)
