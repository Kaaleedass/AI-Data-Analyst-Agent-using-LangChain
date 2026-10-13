# Multi-CSV AI Data Analyst Agent

An AI-powered data analysis assistant that allows users to ask questions in natural language across multiple CSV datasets. Built using **Python, LangChain, Pandas, and OpenAI GPT-4o-mini**, the agent selects relevant datasets and uses Python-based data analysis to generate answers.

## 🚀 Project Overview

This project demonstrates how an LLM-powered agent can interact with structured data across multiple domains without requiring users to write Pandas queries manually.

The agent works with four datasets:

- **SaaS Documentation** — Technical documentation and API usage
- **Credit Card Terms** — Interest rates, fees, and financial terms
- **Hospital Policy** — Visiting hours and administrative policies
- **E-commerce FAQs** — Shipping, returns, and product information

## ✨ Key Features

- **Multi-dataset analysis:** Load and query four CSV files in one agent.
- **Natural-language queries:** Ask questions in plain English.
- **AI-powered tool calling:** Uses LangChain's Pandas DataFrame agent with OpenAI tools.
- **Python-based analysis:** Uses Pandas operations to retrieve and analyze relevant records.
- **Automatic file downloads:** Downloads datasets from Google Drive when they are not available locally.
- **Interactive CLI:** Supports continuous question-and-answer conversations.
- **Secure API configuration:** Reads the OpenAI API key from an environment variable.

## 🛠️ Technology Stack

- Python
- Pandas
- LangChain
- LangChain OpenAI
- LangChain Experimental
- OpenAI GPT-4o-mini
- gdown

## ⚙️ Setup and Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/multi-csv-ai-data-analyst.git
cd multi-csv-ai-data-analyst
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install pandas gdown langchain langchain-openai langchain-experimental
```

### 4. Configure your OpenAI API key

In Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_openai_api_key"
```

Replace the placeholder with your own API key. Never commit API keys or secrets to GitHub.

### 5. Run the application

Save the Python script as `main.py`, then run:

```bash
python main.py
```

## 💬 Example Questions

- What are the visiting hours mentioned in the hospital policy?
- What is the API usage limit in the SaaS documentation?
- What interest rates or fees are listed in the credit card terms?
- What is the return policy for e-commerce orders?

Type `exit` to stop the application.

## 🧠 How It Works

1. Download the required CSV files if they are missing.
2. Load the datasets into Pandas DataFrames.
3. Initialize the OpenAI language model.
4. Create a LangChain DataFrame agent with access to the datasets.
5. Submit a natural-language question.
6. Let the agent select and execute Python/Pandas operations.
7. Return the generated answer to the user.

## 🔐 Security Considerations

This project enables Python code execution through the DataFrame agent. Use it only in a controlled environment, and do not run untrusted code or expose the agent to untrusted users without appropriate sandboxing and access controls.

## 📌 Future Enhancements

- Add a Streamlit chat interface.
- Display source rows supporting each answer.
- Add dataset selection and metadata-based routing.
- Implement validation and stronger execution controls.
- Add retrieval-based search for larger datasets.
- Improve answer grounding and error handling.

## 👨‍💻 Author

Developed as a hands-on project exploring LLM-powered data analysis, LangChain agents, and natural-language interaction with structured datasets.

**Note:** Configure your own OpenAI API key and ensure you have permission to access the linked datasets before running the project.
