CREATE TABLE InvoiceHeader (
    InvoiceId INT IDENTITY PRIMARY KEY,
    VendorName NVARCHAR(200),
    VendorAddress NVARCHAR(500),
    PurchaseOrder NVARCHAR(100)
);

CREATE TABLE InvoiceLine (
    LineId INT IDENTITY PRIMARY KEY,
    InvoiceId INT,
    DescriptionOfGoods NVARCHAR(500),
    HSNCode NVARCHAR(50),
    Quantity DECIMAL(10,2),
    UnitPrice DECIMAL(10,2),
    FOREIGN KEY (InvoiceId) REFERENCES InvoiceHeader(InvoiceId)
);

