import pandas as pd
import os
import sys
import gdown
from getpass import getpass
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

# ==========================================
#  PART 1: AUTOMATIC FILE DOWNLOADER
# ==========================================

files_to_download = {
    "saas_docs.csv":         "https://drive.google.com/file/d/1RElOhN7bYsDAJUNQhYyqM7IzX-Xo6myq/view?usp=sharing",
    "credit_card_terms.csv": "https://drive.google.com/file/d/1_giivc_B0urOKpct0XY2yVZuxW3Eenuf/view?usp=sharing",
    "hospital_policy.csv":   "https://drive.google.com/file/d/1pL7OnDhnmz9pteIpBJ12gu2_ixrc2hPm/view?usp=sharing",
    "ecommerce_faqs.csv":    "https://drive.google.com/file/d/1O4fTjsLFbz55oOiwJUwLwZryO5OSSF6p/view?usp=sharing"
}

print("--- Downloading Files from Google Drive ---")
for filename, url in files_to_download.items():
    if not os.path.exists(filename):
        gdown.download(url, filename, quiet=False)
        print(f"Downloaded: {filename}")
    else:
        print(f"Skipped: {filename} (Already exists)")
print("--- Download Complete ---\n")


# ==========================================
#  PART 2: AI AGENT SETUP (MULTI-FILE)
# ==========================================

# 1. SETUP: Get API Key Securely
#print("ENTER YOUR OPENAI API KEY BELOW:")
#api_key = getpass()

print("Initializing OpenAI client...")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("ERROR: OPENAI_API_KEY is not set.")
    sys.exit(1)

print("OpenAI API key found.")

# 2. LOAD ALL CSVs INTO A LIST
dataframes = [] # We will store all the loaded tables here
loaded_names = []

try:
    for filename in files_to_download.keys():
        df = pd.read_csv(filename)
        dataframes.append(df)
        loaded_names.append(filename)
        print(f"SUCCESS: Loaded '{filename}' ({len(df)} rows)")

except Exception as e:
    print(f"\nERROR loading files: {e}")
    sys.exit()

custom_prefix = """
You are a master data analyst working with 4 specific DataFrames.
Your goal is to query the correct dataframe to answer user questions.

Here is your data map:
- df1: SaaS Documentation (Technical docs, API usage)
- df2: Credit Card Terms (Financial terms, interest rates, fees)
- df3: Hospital Policy (Visiting rules, admin info)
- df4: Ecommerce FAQs (Shipping, returns, product info)

RULES:
1. First, reason about which DataFrame is most relevant to the question.
2. Use Python string methods like `.str.contains('keyword', case=False)` to find relevant rows.
3. DO NOT look for exact matches; always use flexible string matching.
4. If you find the answer, print it clearly.
"""

# 3. DEFINE THE RULES
system_prompt = """
You are a smart data assistant capable of reading multiple CSV files.
- You have access to 4 different datasets: SaaS Docs, Credit Card Terms, Hospital Policy, and Ecommerce FAQs.
- When asked a question, determine which DataFrame is most relevant.
- Do NOT answer from general knowledge.
- Answer in plain English.
"""

# 4. INITIALIZE THE AGENT WITH MULTIPLE DFS
try:
    llm = ChatOpenAI(
        temperature=0.0,
        model="gpt-4o-mini",
        openai_api_key=api_key
    )

    # --- KEY CHANGE: We pass the LIST 'dataframes' instead of a single 'df' ---
    agent = create_pandas_dataframe_agent(
       llm,
        dataframes,
        verbose=True,
        agent_type="openai-tools", # 'openai-tools' is often more stable than 'functions'
        prefix=custom_prefix,      # <--- Injecting the map here
        include_df_in_prompt=True, # Ensures the agent sees column names
        #handle_parsing_errors=True, # <--- Allows agent to self-correct coding errors
        allow_dangerous_code=True
    )

    print("\nAI Agent is ready! You can ask questions across ALL files.")
    print("Example: 'What is the visiting hour in the hospital?' or 'What is the API limit?'")

except Exception as e:
    print(f"Error initializing agent: {e}")
    sys.exit()


# ==========================================
#  PART 3: CHAT LOOP
# ==========================================
print("\nType 'exit' or 'quit' to stop conversation.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    final_query = system_prompt + "\n\nQuestion: " + user_input
    print("AI is thinking...")

    try:
        response = agent.invoke(final_query)['output']
        print(f"AI: {response}\n" + "-"*30)
    except Exception as e:
        print(f"An error occurred: {e}")