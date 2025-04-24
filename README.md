# 📦 Create Data Warehouse Projesi

Bu proje, ETL (Extract-Transform-Load) süreci ile bir satış verisini MSSQL veritabanına aktaran, veri ambarı (data warehouse) mimarisiyle modellenmiş ve Power BI ile görselleştirilmiş uçtan uca bir veri mühendisliği çalışmasıdır.

---

## 🛠️ Kullanılan Teknolojiler

- **Python (pandas, pyodbc, dotenv)** – ETL işlemleri
- **MSSQL** – Veri ambarı platformu
- **Kimball Modeli** – Veri modeli (dimensional modeling)
- **Power BI** – Veri görselleştirme
- **VS Code** – Geliştirme ortamı

---

## 🧱 Mimari Yapı

```bash
create-datawarehouse/
├── seed_data/                 # Gerçekçi CSV veri setleri
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── etl_pipeline.py           # MSSQL bağlantısı, veri yükleme ve hata loglama
├── schema.sql                # Veri ambarı şeması (Dim ve Fact tablolar)
├── procedures.py             # Stored procedure simülasyonları
├── analysis_queries.sql      # OLAP sorguları (slicer, filter, trend)
├── test_pipeline.py          # ETL testi ve veri doğrulama
├── etl_errors.log            # Veri kalitesi hataları loglanır
├── .env                      # MSSQL bağlantı bilgileri
├── requirements.txt          # Python bağımlılıkları
└── README.md

🧮 Veri Ambarı Modeli (Kimball)

Fact Table | Dim Tables
FactOrder | DimCustomer, DimProduct, DimCategory, DimDate

⚙️ ETL Süreci
.env üzerinden MSSQL bağlantısı alınır

Python etl_pipeline.py çalıştırılır

CSV verileri:

DimCustomer

DimCategory & DimProduct

FactOrder

Veri kalitesi hataları etl_errors.log dosyasına yazılır

Testler test_pipeline.py ile yapılır


📊 Power BI Dashboard – Satış Analizi
Aşağıdaki dashboard, ETL sonrası oluşan veri ambarı modelinin Power BI ile görselleştirilmiş halidir.

📸 Dashboard Görünümü:
<!-- Ekran görüntüsünü buraya koy -->

📈 İçerdiği Görseller:
Bar Chart → En çok sipariş veren müşteriler

Pie Chart → Şehirlere göre sipariş yüzdesi

Line Chart → Aylık sipariş trendi

Stacked Column Chart → Kategori bazlı ürün satışları



 Test Raporu (ETL Kalite Kontrol)

 > python test_pipeline.py

✅ [TEST 1] MSSQL bağlantısı başarılı.
✅ [TEST 2] DimCustomer tablosunda 20+ satır veri var.
✅ [TEST 3] etl_errors.log boş (veri kalitesi sorunu bulunamadı).
