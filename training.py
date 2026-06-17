import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def analyze_churn(filepath):

    df = pd.read_csv(filepath) if filepath.endswith('.csv') else pd.read_excel(filepath)

    if 'Churn' not in df.columns:
        return "Dataset must contain 'Churn' column"

    # ---------- CLEAN ----------
    df = df.dropna()
    df['Churn'] = df['Churn'].replace({'Yes': 1, 'No': 0})

    total = len(df)
    churn_count = int(df['Churn'].sum())
    non_churn = total - churn_count
    churn_rate = round((churn_count / total) * 100, 2)

    # ---------- OPTIONAL METRICS ----------
    avg_mrr = df['MonthlyCharges'].mean() if 'MonthlyCharges' in df.columns else None
    revenue_churn = round((churn_count / total) * 100, 2) if avg_mrr else "N/A"

    clv = round(df['tenure'].mean() * avg_mrr, 2) if 'tenure' in df.columns and avg_mrr else "N/A"

    # ---------- CLEAN OLD IMAGES ----------
    if os.path.exists("static"):
        for f in os.listdir("static"):
            if f.endswith(".png"):
                os.remove(os.path.join("static", f))

    timestamp = str(int(time.time()))
    bar_file = f"bar_{timestamp}.png"
    pie_file = f"pie_{timestamp}.png"

    bar_path = os.path.join("static", bar_file)
    pie_path = os.path.join("static", pie_file)

    # ---------- BAR ----------
    plt.figure()
    plt.bar(['Churn', 'Not Churn'], [churn_count, non_churn])
    plt.title("Churn vs Non-Churn")
    plt.savefig(bar_path)
    plt.close()

    # ---------- PIE ----------
    plt.figure()
    plt.pie([churn_count, non_churn], labels=['Churn', 'Not Churn'], autopct='%1.1f%%')
    plt.title("Churn Distribution")
    plt.savefig(pie_path)
    plt.close()

    # ---------- TABLE ----------
    summary_df = pd.DataFrame({
        "Metric": ["Total Customers", "Churn Customers", "Retained Customers", "Churn Rate"],
        "Value": [total, churn_count, non_churn, f"{churn_rate}%"]
    })

    table_html = summary_df.to_html(index=False, classes="table")

    # ---------- SEGMENTATION ----------
    segmentation_html = ""
    if 'Contract' in df.columns:
        seg = df.groupby('Contract')['Churn'].mean().round(2) * 100
        seg_df = seg.reset_index()
        seg_df.columns = ["Contract Type", "Churn %"]
        segmentation_html = seg_df.to_html(index=False, classes="table")

    # ---------- FINAL OUTPUT ----------
    return f"""
    <h3>📊 Key Metrics</h3>
    {table_html}

    <br>
    <b>Revenue Churn:</b> {revenue_churn}%<br>
    <b>Customer Lifetime Value (CLV):</b> {clv}<br>

    <br><h3>📊 Segmentation (Contract Type)</h3>
    {segmentation_html if segmentation_html else "Not Available"}

    <br><h3>📊 Charts</h3>
    <img src="/static/{bar_file}?v={timestamp}" width="350"><br><br>
    <img src="/static/{pie_file}?v={timestamp}" width="350">
    """