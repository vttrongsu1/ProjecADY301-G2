# 🩸 CLINICAL AI: DỰ ĐOÁN CHỈ SỐ ĐƯỜNG HUYẾT ĐÓI & PHÂN TÍCH HỒI QUY (ADY201m)

> **Môn học:** ADY201m - AI & Data Science  
> **Trường Đại học:** FPT University  
> **Tập dữ liệu:** `diabetes_dataset.csv` (100,000 hồ sơ bệnh nhân)  
> **Framework Web:** Django Framework (`manage.py`, `Predictor/`, `webapp/`)  
> **Công nghệ:** Python, Scikit-Learn, SQLite3, Django, HTML5/CSS3, Vanilla JavaScript

---

## 🌟 1. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW)

Hệ thống ứng dụng Trí tuệ Nhân tạo (AI) và Khoa học Dữ liệu trong Y tế nhằm dự đoán chỉ số **Đường huyết lúc đói (Fasting Blood Glucose - mg/dL)** và chẩn đoán phân loại 4 mức nguy cơ y khoa chuẩn Hiệp hội Tiểu đường Hoa Kỳ (ADA):
1. 🚨 **Abnormally Low / Severe Hypoglycemia (`< 70 mg/dL`)**: Cảnh báo Hạ đường huyết cấp tính.
2. 🟢 **Normal (`70 - 99 mg/dL`)**: Mức đường huyết đói Bình thường.
3. 🟡 **Prediabetes (`100 - 125 mg/dL`)**: Mức Tiền tiểu đường.
4. 🔴 **Diabetes (`≥ 126 mg/dL`)**: Nguy cơ cao Tiểu đường.

---

## 📦 2. CÁC THƯ VIỆN CẦN THIẾT & CÀI ĐẶT (PREREQUISITES & INSTALLATION)

```bash
pip install django scikit-learn pandas numpy joblib
```

---

## 🚀 3. HƯỚNG DẪN KHỞI CHẠY SERVING WEB (QUICK START)

### Cách 1: Bằng đúp chuột trên Windows
Click đúp vào file **`start_server.bat`** ở thư mục gốc.

### Cách 2: Bằng dòng lệnh Terminal
```bash
python manage.py runserver 8000
```
Truy cập ứng dụng tại địa chỉ: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 📂 4. CẤU TRÚC THƯ MỤC DỰ ÁN (DIRECTORY STRUCTURE)

```text
ADY mới nhất/
├── 📁 Predictor/                              <-- DJANGO MAIN SETTINGS APP
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 webapp/                                 <-- DJANGO WEB APP CHÍNH
│   ├── __init__.py
│   ├── apps.py
│   ├── urls.py
│   └── views.py                               (Chứa logic xử lý AI & Router Mobile/Desktop)
│
├── ⚙️ manage.py                                (File chạy lệnh chuẩn của Django)
├── 🚀 start_server.bat                         (File click đúp chuột chạy Server Django trên Windows)
├── 📜 export_models.py                         (Script kiểm tra tệp mô hình AI)
│
├── 📂 Documents/                               <-- 4 BÁO CÁO WORD & 3 PDF NOTEBOOK NỘP BÀI
│   ├── 📄 01. Business Understanding.docx
│   ├── 📄 02. Data Analysis.docx
│   ├── 📄 03. Data Cleaning va Data Normalization.docx
│   ├── 📄 04. Giai phap ANOVA.docx
│   ├── 📕 01_normalization_preprocessing.pdf
│   ├── 📕 02_basic_model_training.pdf
│   └── 📕 03_anova_subgroup_analysis.pdf
│
├── 📂 Code/                                    <-- 3 NOTEBOOK MÃ NGUỒN MODULAR
│   ├── 📓 01_normalization_preprocessing.ipynb
│   ├── 📓 02_basic_model_training.ipynb
│   └── 📓 03_anova_subgroup_analysis.ipynb
│
├── 📂 data/                                    <-- CSDL SQLITE `diabetes_pipeline.db`
│   ├── 📊 diabetes_dataset.csv
│   └── 🗄️ diabetes_pipeline.db             (9 bảng CSDL SQLite)
│
├── 📂 models/                                  <-- MÔ HÌNH AI `.joblib`
├── 💻 index.html                               (Giao diện Web AI Responsive)
└── 📄 README.md                                (Hướng dẫn tổng quan)
```
