import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import json
# ----------- API Configuration -----------
OPENROUTER_API_KEY = "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"  # Replace with your key
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "https://your-site.com",  # Required by OpenRouter
    "Content-Type": "application/json"
}
LLM_MODEL = "openai/gpt-3.5-turbo"  # Or any available model like "mistralai/mistral-7b-instruct"

# ----------- Functions -----------

def normalize_url(url):
    if not str(url).startswith("http"):
        return "https://" + str(url)
    return str(url)

def scrape_homepage_text(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        if not paragraphs:
            return ""
        text = ' '.join([p.get_text().strip() for p in paragraphs])
        return text[:3000]  # keep it under 3000 chars
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def analyze_with_openrouter(homepage_text):
    if len(homepage_text.strip()) < 50:
        return {"summary": "N/A (Too little content)", "automation_pitch": "N/A"}

    prompt = f"""
You are an AI analyst. From the given homepage content, provide:

1. A detailed summary of what the company does.
2. Their main target audience.
3. One personalized AI automation idea for them.

Homepage content:
\"\"\"
{homepage_text}
\"\"\"
"""

    try:
        payload = {
            "model": LLM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=HEADERS, data=json.dumps(payload))
        result_text = res.json()['choices'][0]['message']['content']

        parts = result_text.split("3.")
        summary = parts[0].strip() if len(parts) > 0 else "N/A"
        automation = "3." + parts[1].strip() if len(parts) > 1 else "N/A"

        return {"summary": summary, "automation_pitch": automation}

    except Exception as e:
        print(f"OpenRouter error: {e}")
        return {"summary": "N/A (API error)", "automation_pitch": "N/A"}

# ----------- Streamlit UI -----------

st.title("🔍 Lead Enrichment Tool")

uploaded_file = st.file_uploader("📁 Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='windows-1252')
    if "website" not in df.columns:
        st.error("CSV must contain a 'website' column.")
    else:
        if st.button("🚀 Run Enrichment"):
            summaries = []
            automations = []

            progress = st.progress(0, text="Starting enrichment...")
            total = len(df)

            for idx, row in df.iterrows():
                website = normalize_url(row['website'])
                homepage = scrape_homepage_text(website)

                progress.progress((idx + 1) / total, text=f"Processing {website} ({idx + 1}/{total})")

                result = analyze_with_openrouter(homepage)
                summaries.append(result["summary"])
                automations.append(result["automation_pitch"])

                time.sleep(1.5)  # Be polite with API usage

            df["summary_from_llm"] = summaries
            df["automation_pitch_from_llm"] = automations

            st.success("✅ Enrichment completed!")

            st.dataframe(df.head())

            # Download button
            csv_output = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Enriched CSV", csv_output, "enriched_output.csv", "text/csv")

