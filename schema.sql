-- DimCategory
CREATE TABLE DimCategory (
    CategoryKey INT PRIMARY KEY IDENTITY(1,1),
    CategoryName NVARCHAR(100)
);

-- DimProduct
CREATE TABLE DimProduct (
    ProductKey INT PRIMARY KEY,
    ProductName NVARCHAR(100),
    Price DECIMAL(10, 2),
    Stock INT,
    CategoryKey INT,
    FOREIGN KEY (CategoryKey) REFERENCES DimCategory(CategoryKey)
);

-- DimCustomer
CREATE TABLE DimCustomer (
    CustomerKey INT PRIMARY KEY,
    FullName NVARCHAR(100),
    Email NVARCHAR(100),
    City NVARCHAR(100),
    SignupDate DATE
);

-- DimDate
CREATE TABLE DimDate (
    DateKey INT PRIMARY KEY,
    FullDate DATE,
    Year INT,
    Month INT,
    Day INT,
    Quarter INT
);

-- FactOrder
CREATE TABLE FactOrder (
    OrderKey INT PRIMARY KEY,
    CustomerKey INT,
    ProductKey INT,
    Quantity INT,
    OrderDate DATE,
    PaymentType NVARCHAR(50),
    Status NVARCHAR(50),
    UpdatedAt DATE,
    FOREIGN KEY (CustomerKey) REFERENCES DimCustomer(CustomerKey),
    FOREIGN KEY (ProductKey) REFERENCES DimProduct(ProductKey)
);
