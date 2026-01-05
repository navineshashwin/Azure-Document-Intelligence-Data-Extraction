import os
import pyodbc
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential

# ===================== Azure setup =====================
AZURE_ENDPOINT = "https://<your-document-intelligence-resource>.cognitiveservices.azure.com/"
AZURE_API_KEY = "<YOUR_AZURE_DOCUMENT_INTELLIGENCE_KEY>"

client = DocumentIntelligenceClient(
    endpoint=AZURE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_API_KEY)
)

# ===================== SQL Server connection =====================
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=<YOUR_SQL_SERVER_NAME>;"
    "Database=<YOUR_DATABASE_NAME>;"
    "UID=<YOUR_DB_USERNAME>;"
    "PWD=<YOUR_DB_PASSWORD>;"
    "Encrypt=no;"
)
cursor = conn.cursor()

# ===================== Helpers =====================
def clean(val):
    return val.replace("\n", " ").strip() if val else None

# ===================== Invoice Extraction =====================
def extract_invoice(file_path):
    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-invoice",
            body=f,
            features=["queryFields"],
            query_fields=[
                "VendorName",
                "VendorAddress",
                "PurchaseOrder",
                "Description",
                "HSNCode",
                "Quantity",
                "UnitPrice"
            ]
        )
        result = poller.result()

    for doc in result.documents:
        # ----- Invoice Header -----
        name = clean(doc.fields.get("VendorName").content if doc.fields.get("VendorName") else None)
        addr = clean(doc.fields.get("VendorAddress").content if doc.fields.get("VendorAddress") else None)
        po = clean(doc.fields.get("PurchaseOrder").content if doc.fields.get("PurchaseOrder") else None)

        cursor.execute(
            """
            INSERT INTO InvoiceHeader (Name, Address, PO)
            OUTPUT INSERTED.InvoiceId
            VALUES (?, ?, ?)
            """,
            (name, addr, po)
        )
        invoice_id = cursor.fetchone()[0]
        conn.commit()

        print(f"Inserted Header: {name} | PO: {po} (InvoiceId={invoice_id})")

        # ----- Invoice Line -----
        desc = clean(doc.fields.get("Description").content if doc.fields.get("Description") else None)
        hsn = clean(doc.fields.get("HSNCode").content if doc.fields.get("HSNCode") else None)
        qty = clean(doc.fields.get("Quantity").content if doc.fields.get("Quantity") else None)
        rate = clean(doc.fields.get("UnitPrice").content if doc.fields.get("UnitPrice") else None)

        cursor.execute(
            """
            INSERT INTO InvoiceLine (InvoiceId, DescriptionOfGoods, HSNCode, Qty, Rate)
            VALUES (?, ?, ?, ?, ?)
            """,
            (invoice_id, desc, hsn, qty, rate)
        )
        conn.commit()

        print(f"Inserted Line: {desc} | {hsn} | {qty} | {rate}")

# ===================== Folder Processing =====================
def process_folder(folder_path):
    for file in os.listdir(folder_path):
        if file.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
            extract_invoice(os.path.join(folder_path, file))

if __name__ == "__main__":
    process_folder(r"<PATH_TO_INVOICE_FOLDER>")

