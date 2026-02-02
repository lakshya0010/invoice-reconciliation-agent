# Multi-Agent Invoice Reconciliation System

This project implements a multi-agent invoice reconciliation system that:
- Extracts structured data from supplier invoices
- Matches invoices to purchase orders using fuzzy logic
- Detects pricing discrepancies
- Produces explainable reconciliation decisions

The system is built using **LangGraph** and **LangChain**, and uses **free cloud-hosted LLMs (Groq)**.

---

## Architecture Overview

Agents:
1. **Document Intelligence Agent**
   - Extracts structured invoice data from PDFs
   - Handles noisy text and formatting issues
   - Produces confidence scores

2. **Matching Agent**
   - Matches invoices to POs using fuzzy supplier and item similarity
   - Works even when PO references are missing

3. **Discrepancy Detection Agent**
   - Flags unit-level price mismatches
   - Surfaces potential invoice anomalies

4. **Resolution Agent**
   - Produces final decisions:
     - AUTO_APPROVE
     - REVIEW
     - ESCALATE
   - Provides clear reasoning for each decision

Agents communicate through shared state using LangGraph (not a linear pipeline).

---

## Tech Stack

- Python 3.10+
- LangChain
- LangGraph
- Groq (LLaMA 3.x models)
- pdfplumber
- pytesseract
- pdf2image
- RapidFuzz

No OpenAI APIs are used.

---

## Project Structure
invoice-reconciliation-agent/
│
├── agents/
│ ├── document_agent.py
│ ├── matching_agent.py
│ ├── discrepancy_agent.py
│ └── resolution_agent.py
│
├── tools/
│ ├── pdf_tools.py
│ ├── ocr_tools.py
│ └── matching_tools.py
│
├── utils/
│ ├── confidence.py
│ └── json_utils.py
│
├── graph/
│ └── reconciliation_graph.py
│
├── data/
│ ├── invoices/
│ └── po_db.json
│
├── main.py
├── requirements.txt
└── README.md


---

## Setup Instructions

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

2. Install dependencies
pip install -r requirements.txt

3. Set environment variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key_here


Or export manually:

export GROQ_API_KEY=your_groq_api_key

4. (Windows only) OCR setup

Install Tesseract OCR

Install Poppler

Add both to your system PATH

5. Run the system

python main.py

