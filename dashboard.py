import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path
import os

os.chdir(Path(__file__).parent)

st.set_page_config(
    page_title="Bank Commercial Dashboard",
    page_icon="🏦",
    layout="wide"
)

df = pd.read_csv("bank_commercial_clean.csv")
targets = pd.read_csv("branch_targets.csv")
df['subscribed'] = (df['y'] == 'yes').astype(int)

st.title("🏦 Bank Commercial Performance Dashboard")
st.markdown("**Banco de Portugal | Term Deposit Campaign Analysis**")
st.divider()

# ── Section 1: Headline KPIs ──────────────────────────────
total_contacts    = len(df)
total_conversions = df['subscribed'].sum()
overall_cvr       = df['subscribed'].mean() * 100
total_revenue     = df['deposit_value'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Contacts",    f"{total_contacts:,}")
col2.metric("Total Conversions", f"{total_conversions:,}")
col3.metric("Overall CVR",       f"{overall_cvr:.1f}%")
col4.metric("Total Revenue",     f"€{total_revenue/1e6:.1f}M")

st.divider()
# ── Section 2: Branch Performance ─────────────────────────
st.subheader("Branch Performance")

branch_perf = (df.groupby('branch')
               .agg(contacts=('subscribed','count'),
                    conversions=('subscribed','sum'),
                    revenue=('deposit_value','sum'))
               .assign(cvr=lambda x: round(x.conversions/x.contacts*100, 1))
               .reset_index())

branch_perf = branch_perf.merge(targets, on='branch')
branch_perf['target_attainment'] = round(
    branch_perf['conversions'] / branch_perf['monthly_target_conversions'] * 100, 1)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(branch_perf.sort_values('cvr'),
                 x='cvr', y='branch', orientation='h',
                 title='CVR % by Branch',
                 color='cvr',
                 color_continuous_scale='Blues',
                 labels={'cvr':'Conversion Rate (%)','branch':'Branch'})
    fig.add_vline(x=overall_cvr, line_dash='dash',
                  line_color='orange',
                  annotation_text=f'Average {overall_cvr:.1f}%')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig2 = px.bar(branch_perf.sort_values('target_attainment'),
                  x='target_attainment', y='branch', orientation='h',
                  title='Target Attainment % by Branch',
                  color='target_attainment',
                  color_continuous_scale='RdYlGn',
                  labels={'target_attainment':'Attainment (%)','branch':'Branch'})
    fig2.add_vline(x=100, line_dash='dash', line_color='black',
                   annotation_text='Target')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
# ── Section 3: Customer Segment Analysis ──────────────────
st.subheader("Customer Segment Analysis")

col1, col2 = st.columns(2)

with col1:
    seg_job = (df.groupby('job')['subscribed']
               .agg(['count','sum','mean'])
               .rename(columns={'count':'contacts',
                                'sum':'conversions',
                                'mean':'cvr'})
               .assign(cvr=lambda x: round(x.cvr*100, 1))
               .reset_index()
               .sort_values('cvr'))

    fig3 = px.bar(seg_job, x='cvr', y='job', orientation='h',
                  title='CVR % by Job Segment',
                  color='cvr',
                  color_continuous_scale='Blues',
                  labels={'cvr':'Conversion Rate (%)','job':'Job Type'})
    fig3.add_vline(x=overall_cvr, line_dash='dash',
                   line_color='orange',
                   annotation_text=f'Average {overall_cvr:.1f}%')
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    df['age_group'] = pd.cut(df['age'],
                              bins=[0,30,45,60,100],
                              labels=['Under 30','30-45','46-60','60+'])
    seg_age = (df.groupby('age_group', observed=True)['subscribed']
               .agg(['count','mean'])
               .rename(columns={'count':'contacts','mean':'cvr'})
               .assign(cvr=lambda x: round(x.cvr*100, 1))
               .reset_index())

    fig4 = px.bar(seg_age, x='age_group', y='cvr',
                  title='CVR % by Age Group',
                  color='cvr',
                  color_continuous_scale='Blues',
                  labels={'cvr':'Conversion Rate (%)',
                          'age_group':'Age Group'})
    fig4.add_hline(y=overall_cvr, line_dash='dash',
                   line_color='orange',
                   annotation_text=f'Average {overall_cvr:.1f}%')
    st.plotly_chart(fig4, use_container_width=True)

st.divider()
# ── Section 4: Monthly Trend & Euribor ────────────────────
st.subheader("Monthly Campaign Trend & Macroeconomic Context")

month_order = ['jan','feb','mar','apr','may','jun',
               'jul','aug','sep','oct','nov','dec']

monthly = (df.groupby('month', observed=True)
            .agg(contacts=('subscribed','count'),
                 conversions=('subscribed','sum'),
                 revenue=('deposit_value','sum'),
                 avg_euribor=('euribor3m','mean'))
            .assign(cvr=lambda x: round(x.conversions/x.contacts*100,1))
            .reindex(month_order)
            .dropna()
            .reset_index())

fig5 = go.Figure()

fig5.add_trace(go.Bar(
    x=monthly['month'], y=monthly['conversions'],
    name='Conversions', marker_color='#1f4e79', opacity=0.7))

fig5.add_trace(go.Scatter(
    x=monthly['month'], y=monthly['cvr'],
    name='CVR %', yaxis='y2',
    line=dict(color='#c55a11', width=2.5),
    mode='lines+markers'))

fig5.add_trace(go.Scatter(
    x=monthly['month'], y=monthly['avg_euribor'],
    name='Euribor 3M', yaxis='y2',
    line=dict(color='green', width=2, dash='dot'),
    mode='lines+markers'))

fig5.update_layout(
    title='Monthly Conversions, CVR % and Euribor Rate',
    xaxis=dict(title='Month'),
    yaxis=dict(title='Conversions'),
    yaxis2=dict(title='CVR % / Euribor', overlaying='y', side='right'),
    legend=dict(x=0, y=1.1, orientation='h'),
    height=500
)

st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ── Footer ─────────────────────────────────────────────────
st.caption("Data: Banco de Portugal Bank Marketing Dataset | "
           "Analysis: Clara Mujuni | Banking Data Analyst Portfolio")