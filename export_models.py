import os
import sys
import joblib

# Force UTF-8 output encoding for Windows Console
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

cwd = r'c:\Users\PC\Desktop\Du_An\project ADY201m\ADY mới nhất'
models_dir = os.path.join(cwd, 'models')

print(f"Kiểm tra các tệp mô hình tại: {models_dir}")
m_full_p = os.path.join(models_dir, 'linear_regression_full.joblib')
m_red_p = os.path.join(models_dir, 'optimal_reduced_diabetes_model.joblib')

if os.path.exists(m_full_p) and os.path.exists(m_red_p):
    m_full = joblib.load(m_full_p)
    m_red = joblib.load(m_red_p)
    print(f"✅ Desktop Model (OLS): {len(m_full.feature_names_in_)} đặc trưng")
    print(f"✅ Mobile Model (Lasso): {len(m_red.feature_names_in_)} đặc trưng")
    print("Export verification completed successfully!")
else:
    print("⚠️ Tệp mô hình không tồn tại.")
