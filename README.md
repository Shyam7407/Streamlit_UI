# Streamlit_UI
                   #LLM-Powered Company Lead Enrichment Tool (QF Innovate Assessment)
This project is a Streamlit-based web application that enriches company leads by scraping their homepage and analyzing the content using an LLM API via OpenRouter.

🚀 Features
Uploaded a CSV with company websites.

Automatically scrape homepage text using BeautifulSoup.

Send extracted content to OpenRouter (e.g., gpt-3.5-turbo) for:

A company summary

An AI automation pitch for QF Innovate

Preview enriched results in a table.

Download the enriched CSV.

📁 Input Format
Your CSV file must include a column named website.

Example:

company_name	website
Zoho	www.zoho.com

📤 Output Columns
summary_from_llm — What the company does.

automation_pitch_from_llm — A tailored AI idea QF Innovate can pitch.

🛠 Requirements
Install dependencies:
pip install streamlit pandas requests beautifulsoup4
🔐 Configuration
Got free API key from https://openrouter.ai

In app.py, replace the placeholder key:

OPENROUTER_API_KEY = "sk-or-xxxxxxxxxxxxxxxxxxxx"
▶️ How to Run the App
streamlit run app.py
It will launch a local browser window with the web interface.

💡 Notes
The tool uses only <p> tags. You can modify scrape_homepage_text() to include <h1>, <h2>, etc.

API usage is rate-limited. A time.sleep(1.5) is added after each request.

If homepage content is very short or blocked by JavaScript, the result might be N/A.

#NOTE🥇
▶️ How to Run the App
streamlit run app.py In Terminal


