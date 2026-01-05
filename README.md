# Azure Document Intelligence – Invoice Data Extraction

## 📌 Project Overview
This project demonstrates automated invoice data extraction using
**Azure Document Intelligence (Prebuilt Invoice Model)** and stores
the extracted data into **SQL Server**.

The solution processes PDF and image invoices, extracts header and line
item details, and persists them into relational tables.

---

## 🎯 Use Case
- Invoice automation
- OCR-based data extraction
- Structured storage for reporting & analytics
- ERP / Accounting system integration

---

## 🏗 Architecture Flow
1. Invoice files (PDF/Image) are read from a local folder
2. Azure Document Intelligence analyzes documents
3. Key fields are extracted using **queryFields**
4. Header and line data are inserted into SQL Server tables

---

## 🛠 Technologies Used
- Azure Document Intelligence
- Python
- Azure AI SDK
- SQL Server
- pyodbc
- REST-based OCR processing

---

## 📂 Project Structure

- **SourceCode/**
  - `invoice_extraction.py`

- **SampleDocuments/**
  - `sample_invoice_dummy.pdf`

- **ExtractedOutput/**
  - `output_sample.json`

- **Database/**
  - `table_scripts.sql`

- **README.md**


