# Bank Commercial Performance Dashboard
**Banking Data Analyst Portfolio Project | Clara Mujuni**

---

## Business Problem
A bank's commercial team runs term deposit campaigns across 8 branches. 
Management needs to understand which branches, customer segments and 
time periods drive the highest conversion rates — and why performance 
varies across the portfolio.

## What This Project Does
End-to-end commercial data analysis pipeline built on a real banking 
dataset (Banco de Portugal, 41,188 records), covering:

- Data quality audit and cleaning with documented business decisions
- Commercial KPI engineering (CVR, revenue, target attainment)
- Advanced SQL analysis — CTEs, window functions, RANK(), LAG()
- Macroeconomic correlation analysis (Euribor vs conversion rate)
- Interactive dashboard for sales and management reporting

## Key Findings
- Overall conversion rate: **11.3%** across 41,188 customer contacts
- **Student and retired segments** convert at 31% and 25% — nearly 
  3x the overall average. Underserved by current campaign strategy.
- **Cellular contact outperforms telephone** at 14.7% vs 5.2% CVR
- **CVR drops sharply after 3 contacts** — over-contacting wastes 
  sales team capacity and risks customer attrition
- **Low Euribor months correlate with higher CVR** — macroeconomic 
  context should inform campaign timing, not just sales targets
- Branch target attainment varies significantly — high-CVR branches 
  are constrained by contact volume, not conversion capability

## Tech Stack
| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data cleaning and KPI engineering |
| SQL (SQLite) | Advanced querying — CTEs, window functions |
| Matplotlib / Plotly | Static and interactive visualisations |
| Streamlit | Interactive dashboard |

## Project Structure
bank-commercial-dashboard/

| bank_marketing_project.ipynb   # EDA and data cleaning

| 02_sql_analysis.ipynb          # SQL analysis notebook

| dashboard.py                   # Interactive Streamlit dashboard

| bank_commercial_full.csv       # Raw enriched dataset

| bank_commercial_clean.csv      # Cleaned dataset

| branch_targets.csv             # Branch targets table

| fig1-fig6_*.png                # Exported visualisations

## How to Run
```bash
# Install dependencies
pip install pandas numpy matplotlib plotly streamlit

# Launch dashboard
streamlit run dashboard.py
```

## Data Source
Moro, S., Cortez, P., & Rita, P. (2014). A data-driven approach to 
predict the success of bank telemarketing. *Decision Support Systems.*  
UCI Machine Learning Repository — Bank Marketing Dataset.

---
*This project is part of a banking data analyst portfolio targeting 
commercial management BI roles in the banking sector.*
