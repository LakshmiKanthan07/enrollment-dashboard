import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.holtwinters import ExponentialSmoothing
st.set_page_config(
    page_title="Aadhaar Insight AI",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-box {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4e73df;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-value { font-size: 26px; font-weight: bold; color: #2c3e50; }
    .metric-label { font-size: 13px; color: #7f8c8d; font-weight: 600; text-transform: uppercase; }
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; }
    hr { margin-top: 2rem; margin-bottom: 2rem; border: 0; border-top: 1px solid rgba(0,0,0,.1); }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    file_path = "unified_enrolment_data.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error("❌ **CRITICAL ERROR**: File `unified_enrolment_data.csv` not found.")
        st.stop()

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    
    numeric_cols = [
        'bio_age_5_17', 'bio_age_17_', 'demo_age_5_17', 'demo_age_17_', 
        'age_0_5', 'age_5_17', 'age_18_greater'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        else:
            df[col] = 0

    df['Biometric Updates'] = df['bio_age_5_17'] + df['bio_age_17_']
    df['Demographic Updates'] = df['demo_age_5_17'] + df['demo_age_17_']
    df['Total Updates'] = df['Biometric Updates'] + df['Demographic Updates']
    df['Total Enrolments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
    
    df['MBU_Gap_Index'] = np.where(df['age_5_17'] > 0, df['bio_age_5_17'] / df['age_5_17'], 0)

    df['Migration_Intensity'] = df['demo_age_17_'] / (df['age_18_greater'] + 1)
    
    df['Weighted_Effort'] = (
        (df['Total Enrolments'] * 3.0) + 
        (df['Biometric Updates'] * 2.0) + 
        (df['Demographic Updates'] * 1.0)
    )
    df['Efficiency_Gap'] = df['Weighted_Effort'] / (df['Total Updates'] + df['Total Enrolments'] + 1)
    df['DayOfWeek'] = df['date'].dt.day_name()
    df['DayIndex'] = df['date'].dt.dayofweek 

    return df

df = load_data()

st.sidebar.title("🎛️ Control Panel")
min_d, max_d = df['date'].min(), df['date'].max()
start_date, end_date = st.sidebar.date_input("Date Range", [min_d, max_d], min_value=min_d, max_value=max_d)

all_states = sorted(df['state'].unique().astype(str))
container = st.sidebar.container()
all_selected = st.sidebar.checkbox("Select All States", value=True)

if all_selected:
    selected_states = all_states
else:
    selected_states = st.sidebar.multiselect("Select Specific States", all_states, default=all_states[:1])

mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date)) & (df['state'].isin(selected_states))
state_df = df.loc[mask]

st.sidebar.markdown("---")
st.sidebar.info(f"Analyzing **{len(state_df):,}** records.")

st.title(f"🇮🇳 Aadhaar Intelligent Monitoring")
st.caption(f"Analysis Scope: {', '.join(selected_states[:3])} {'...' if len(selected_states)>3 else ''}")

total_enrol = state_df['Total Enrolments'].sum()
total_upd = state_df['Total Updates'].sum()
mbu_risk_count = state_df[state_df['MBU_Gap_Index'] < 0.2]['pincode'].nunique()
mig_hub_count = state_df[state_df['Migration_Intensity'] > 5]['pincode'].nunique()

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="metric-box"><div class="metric-value">{total_enrol:,.0f}</div><div class="metric-label">Total Enrolments</div></div>', unsafe_allow_html=True)
k2.markdown(f'<div class="metric-box"><div class="metric-value">{total_upd:,.0f}</div><div class="metric-label">Total Updates</div></div>', unsafe_allow_html=True)
k3.markdown(f'<div class="metric-box" style="border-left: 5px solid #e74c3c"><div class="metric-value">{mbu_risk_count}</div><div class="metric-label">Compliance Risk Areas</div></div>', unsafe_allow_html=True)
k4.markdown(f'<div class="metric-box" style="border-left: 5px solid #f1c40f"><div class="metric-value">{mig_hub_count}</div><div class="metric-label">Migration Hotspots</div></div>', unsafe_allow_html=True)

st.markdown("---")

st.header("1.Pareto Analysis (80/20 Rule)")
st.caption("Identify the 'Vital Few' districts driving the majority of enrolments.")

pareto_df = state_df.groupby('district')['Total Enrolments'].sum().reset_index().sort_values('Total Enrolments', ascending=False)
pareto_df['CumPct'] = pareto_df['Total Enrolments'].cumsum() / pareto_df['Total Enrolments'].sum() * 100

fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
fig_pareto.add_trace(go.Bar(x=pareto_df['district'].head(30), y=pareto_df['Total Enrolments'].head(30), name="Volume", marker_color="#2c3e50"), secondary_y=False)
fig_pareto.add_trace(go.Scatter(x=pareto_df['district'].head(30), y=pareto_df['CumPct'].head(30), name="Cumulative %", mode='lines+markers', line=dict(color='#c0392b', width=2)), secondary_y=True)

fig_pareto.update_layout(title="Top 30 Districts (Volume vs Cumulative %)", xaxis_title="District")
fig_pareto.update_yaxes(title_text="Volume", secondary_y=False)
fig_pareto.update_yaxes(title_text="Cumulative %", secondary_y=True, range=[0, 105])

st.plotly_chart(fig_pareto, use_container_width=True)

if len(pareto_df) > 0:
    top_20_pct_idx = int(len(pareto_df) * 0.2)
    vol_20 = pareto_df.iloc[:top_20_pct_idx]['Total Enrolments'].sum()
    total_vol = pareto_df['Total Enrolments'].sum()
    pct_contrib = (vol_20 / total_vol * 100) if total_vol > 0 else 0
    st.info(f"💡 **Pareto Insight:** The top 20% of districts contribute **{pct_contrib:.1f}%** of total enrolments.")

st.markdown("---")

st.header("2. ⚔️ Head-to-Head Comparison")
h1, h2 = st.columns(2)
with h1:
    comp_state_a = st.selectbox("Select State A (Baseline)", selected_states, index=0)
with h2:
    default_b_index = 1 if len(selected_states) > 1 else 0
    comp_state_b = st.selectbox("Select State B (Comparison)", selected_states, index=default_b_index)

if comp_state_a and comp_state_b:
    df_a = state_df[state_df['state'] == comp_state_a]
    df_b = state_df[state_df['state'] == comp_state_b]
    
    metrics = {
        'Volume': 'Total Enrolments', 'Updates': 'Total Updates',
        'Child Enrolment': 'age_0_5', 'Migration Score': 'Migration_Intensity',
        'Efficiency': 'Weighted_Effort'
    }
    vals_a, vals_b = [], []
    for k, v in metrics.items():
        if k in ['Migration Score', 'Efficiency']:
            va, vb = df_a[v].mean(), df_b[v].mean()
        else:
            va, vb = df_a[v].sum(), df_b[v].sum()
        m_max = max(va, vb) if max(va, vb) > 0 else 1
        vals_a.append(va/m_max)
        vals_b.append(vb/m_max)        
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(r=vals_a, theta=list(metrics.keys()), fill='toself', name=comp_state_a, fillcolor='rgba(52, 152, 219, 0.5)', line=dict(color='#3498db', width=2)))
    fig_radar.add_trace(go.Scatterpolar(r=vals_b, theta=list(metrics.keys()), fill='toself', name=comp_state_b, fillcolor='rgba(231, 76, 60, 0.5)', line=dict(color='#e74c3c', width=2)))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), title=f"Relative Performance: {comp_state_a} vs {comp_state_b}")
    st.plotly_chart(fig_radar, use_container_width=True)
st.markdown("---")
st.header("3.  Temporal & Statistical Analysis")
t1, t2 = st.columns(2)

with t1:
    st.subheader("Day of Week Analysis")
    dow_df = state_df.groupby(['DayOfWeek', 'DayIndex'])['Total Enrolments'].sum().reset_index().sort_values('DayIndex')
    fig_dow = px.bar(dow_df, x='DayOfWeek', y='Total Enrolments', color='Total Enrolments', color_continuous_scale='Blues')
    st.plotly_chart(fig_dow, use_container_width=True)

with t2:
    st.subheader("Correlation Matrix (Proof)")
    corr_cols = ['Total Enrolments', 'Total Updates', 'age_0_5', 'Migration_Intensity', 'MBU_Gap_Index']
    fig_corr = px.imshow(state_df[corr_cols].corr(), text_auto=True, color_continuous_scale="RdBu_r")
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")

st.header("4. AI Diagnostics & Forecasting")
c1, c2 = st.columns(2)

with c1:
    st.subheader("Anomaly Detection")
    if st.button("Run Anomaly Scan"):
        feat = ['Total Enrolments', 'Total Updates', 'bio_age_5_17']
        pin_agg = state_df.groupby('pincode')[feat].sum().reset_index()
        scaler = StandardScaler()
        X = scaler.fit_transform(pin_agg[feat])
        iso = IsolationForest(contamination=0.05, random_state=42)
        pin_agg['anomaly'] = iso.fit_predict(X)
        pin_agg['anomaly_label'] = pin_agg['anomaly'].map({-1: 'Anomaly', 1: 'Normal'})
        anoms = pin_agg[pin_agg['anomaly'] == -1]
        fig_anom = px.scatter(pin_agg, x="Total Enrolments", y="Total Updates", color='anomaly_label', color_discrete_map={'Anomaly':'#e74c3c', 'Normal':'#27ae60'}, hover_data=['pincode'])
        st.plotly_chart(fig_anom, use_container_width=True)
        st.error(f" **{len(anoms)} Pincodes** flagged as anomalous.")

with c2:
    st.subheader("Demand Forecasting (30 Days)")
    ts_data = state_df.groupby('date')['Total Enrolments'].sum().asfreq('D').fillna(0)
    try:
        model = ExponentialSmoothing(ts_data, trend='add', seasonal=None).fit()
        forecast = model.forecast(30)
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=ts_data.index, y=ts_data, name='History'))
        fig_pred.add_trace(go.Scatter(x=pd.date_range(ts_data.index[-1]+pd.Timedelta(days=1), periods=30), y=forecast, name='Forecast', line=dict(color='red', dash='dash')))
        st.plotly_chart(fig_pred, use_container_width=True)
        st.success(f" Expected Load: **{int(forecast.sum())}** enrolments next month.")
    except:
        st.warning("Insufficient data.")

st.markdown("---")

st.header("5.  Deep Insights & Optimization")

st.subheader("A. Operator Efficiency Analysis")
fig_eff = px.scatter(state_df, x="Total Updates", y="Weighted_Effort", color="Efficiency_Gap", size="Total Enrolments", color_continuous_scale="Viridis", title="Volume vs True Effort")
st.plotly_chart(fig_eff, use_container_width=True)

st.subheader("B. Migration Dynamics: The 'Churn' Map")
st.write("Identifies districts with high population turnover (High Address Updates vs Low New Enrolments).")

churn_data = state_df.groupby('district')['Migration_Intensity'].mean().sort_values(ascending=False).head(10)

col_mig1, col_mig2 = st.columns([1, 1])
with col_mig1:
    st.dataframe(churn_data, column_config={"Migration_Intensity": st.column_config.ProgressColumn("Migration Score", format="%.2f", min_value=0, max_value=churn_data.max())})
with col_mig2:
    st.caption("Strategic Interpretation")
    st.info("""
    - **High Score (>10):** "Transit Hubs" (Industrial zones). People move here and update addresses. **Action:** Deploy 'Update-Only' Kiosks.
    - **Low Score (<2):** "Settled Zones". **Action:** Focus on Child Enrolment camps.
    """)

st.subheader("C. Resource Allocation (Urgency Score)")
alloc_df = state_df.groupby('district').agg({'MBU_Gap_Index': 'mean', 'Total Enrolments': 'sum', 'age_0_5': 'sum'}).reset_index()
def normalize(s): return (s - s.min()) / (s.max() - s.min())
alloc_df['Urgency_Score'] = (normalize(alloc_df['MBU_Gap_Index'])*0.5 + normalize(alloc_df['Total Enrolments'])*0.3 + normalize(alloc_df['age_0_5'])*0.2)
alloc_df = alloc_df.sort_values('Urgency_Score', ascending=False).head(15)
fig_alloc = px.bar(alloc_df, x='Urgency_Score', y='district', orientation='h', color='Urgency_Score', color_continuous_scale='Reds')
st.plotly_chart(fig_alloc, use_container_width=True)
st.success(f" **Action:** Deploy kits to **{alloc_df.iloc[0]['district']}** immediately.")