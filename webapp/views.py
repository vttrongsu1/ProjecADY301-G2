import os
import json
import joblib
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# 1. Path setup & load model artifacts
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_FULL_PATH = os.path.join(BASE_DIR, 'models', 'linear_regression_full.joblib')
MODEL_REDUCED_PATH = os.path.join(BASE_DIR, 'models', 'optimal_reduced_diabetes_model.joblib')
SCALER_PATH = os.path.join(BASE_DIR, 'models', 'minmax_scaler.joblib')

model_full = joblib.load(MODEL_FULL_PATH) if os.path.exists(MODEL_FULL_PATH) else None
model_reduced = joblib.load(MODEL_REDUCED_PATH) if os.path.exists(MODEL_REDUCED_PATH) else None
scaler = joblib.load(SCALER_PATH) if os.path.exists(SCALER_PATH) else None

# Median population defaults
FEATURE_MEDIANS = {
    'age': 50.0,
    'alcohol_consumption_per_week': 2.0,
    'physical_activity_minutes_per_week': 100.0,
    'diet_score': 6.0,
    'sleep_hours_per_day': 7.0,
    'screen_time_hours_per_day': 6.0,
    'bmi': 25.6,
    'waist_to_hip_ratio': 0.86,
    'systolic_bp': 116.0,
    'diastolic_bp': 75.0,
    'heart_rate': 70.0,
    'cholesterol_total': 186.0,
    'hdl_cholesterol': 54.0,
    'triglycerides': 121.0,
    'insulin_level': 8.79,
    'hba1c': 6.52
}

scale_map = {}
if scaler is not None:
    for name, dmin, dmax in zip(scaler.feature_names_in_, scaler.data_min_, scaler.data_max_):
        scale_map[name] = (dmin, dmax)

FEATURE_LABELS = {
    'age': 'Age_scaled',
    'bmi': 'BMI_scaled',
    'hba1c': 'HbA1c_scaled',
    'insulin_level': 'Insulin_scaled',
    'hdl_cholesterol': 'HDL_Cholesterol_scaled',
    'ldl_cholesterol': 'LDL_Cholesterol_scaled',
    'cholesterol_total': 'Total_Cholesterol_scaled',
    'triglycerides': 'Triglycerides_scaled',
    'heart_rate': 'Heart_Rate_scaled',
    'systolic_bp': 'Systolic_BP_scaled',
    'diastolic_bp': 'Diastolic_BP_scaled',
    'waist_to_hip_ratio': 'Waist_Hip_Ratio_scaled',
    'physical_activity_minutes_per_week': 'Physical_Activity_scaled',
    'diet_score': 'Diet_Score_scaled',
    'screen_time_hours_per_day': 'Screen_Time_scaled',
    'sleep_hours_per_day': 'Sleep_Hours_scaled',
    'alcohol_consumption_per_week': 'Alcohol_Drinks_scaled',
    'family_history_diabetes': 'Family_History_Diabetes',
    'hypertension_history': 'Hypertension_History',
    'cardiovascular_history': 'Cardiovascular_History',
    'gender_Male': 'Gender_Male',
    'gender_Other': 'Gender_Other',
    'ethnicity_Black': 'Ethnicity_Black',
    'ethnicity_Hispanic': 'Ethnicity_Hispanic',
    'ethnicity_Other': 'Ethnicity_Other',
    'ethnicity_White': 'Ethnicity_White',
    'education_level_Highschool': 'Education_Highschool',
    'education_level_No formal': 'Education_No_Formal',
    'education_level_Postgraduate': 'Education_Postgraduate',
    'income_level_Low': 'Income_Low',
    'income_level_Lower-Middle': 'Income_Lower_Middle',
    'income_level_Middle': 'Income_Middle',
    'income_level_Upper-Middle': 'Income_Upper_Middle',
    'employment_status_Retired': 'Employment_Retired',
    'employment_status_Student': 'Employment_Student',
    'employment_status_Unemployed': 'Employment_Unemployed',
    'smoking_status_Former': 'Smoking_Former',
    'smoking_status_Never': 'Smoking_Never'
}

def is_mobile_user_agent(user_agent_str):
    ua = user_agent_str.lower()
    mobile_keywords = ['mobile', 'android', 'iphone', 'ipad', 'ipod', 'webos', 'blackberry', 'windows phone']
    return any(kw in ua for kw in mobile_keywords)

def generate_scaled_equations(model, scaled_input_dict):
    b0 = model.intercept_
    cols = list(model.feature_names_in_)
    coefs = list(model.coef_)

    terms_general = [f"{b0:.3f}"]
    terms_substituted = [f"{b0:.3f}"]

    for col, coef in zip(cols, coefs):
        val = scaled_input_dict.get(col, 0.0)
        label = FEATURE_LABELS.get(col, col)
        
        sign = " + " if coef >= 0 else " - "
        abs_c = abs(coef)

        terms_general.append(f"{sign}({abs_c:.4f} * {label})")
        terms_substituted.append(f"{sign}({abs_c:.4f} * {val:.4f})")

    eq_general = "Glucose = " + "".join(terms_general)
    eq_substituted = "Glucose = " + "".join(terms_substituted)
    return eq_general, eq_substituted

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def predict(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Only POST method is allowed'}, status=405)

    try:
        if request.body:
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST.dict()

        if not data:
            return JsonResponse({'success': False, 'error': 'No input data received!'}, status=400)

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        is_mobile = is_mobile_user_agent(user_agent) or data.get('is_mobile_screen', False)

        if is_mobile and model_reduced is not None:
            active_model = model_reduced
            model_type_str = "Mobile (Reduced Model)"
            model_code = "reduced"
            r2_val = "54.81%"
            features_cnt = 20
            orig_features_cnt = 17
            device_str = "Mobile Device"
        else:
            active_model = model_full if model_full is not None else model_reduced
            model_type_str = "Desktop (Full Model)"
            model_code = "full"
            r2_val = "54.67%"
            features_cnt = 38 if model_full is not None else 20
            orig_features_cnt = 26 if model_full is not None else 17
            device_str = "Desktop Device"

        target_features = list(active_model.feature_names_in_)

        raw_input = {}
        continuous_cols = [
            'age', 'alcohol_consumption_per_week', 'physical_activity_minutes_per_week', 
            'diet_score', 'sleep_hours_per_day', 'screen_time_hours_per_day', 
            'bmi', 'waist_to_hip_ratio', 'systolic_bp', 'diastolic_bp', 
            'heart_rate', 'cholesterol_total', 'hdl_cholesterol', 'triglycerides', 
            'insulin_level', 'hba1c'
        ]
        for col in continuous_cols:
            if col in target_features:
                user_val = data.get(col, '')
                if user_val is not None and str(user_val).strip() != '':
                    raw_input[col] = float(user_val)
                else:
                    raw_input[col] = FEATURE_MEDIANS.get(col, 0.0)

        for col in ['family_history_diabetes', 'hypertension_history', 'cardiovascular_history']:
            if col in target_features:
                user_val = data.get(col, 0)
                raw_input[col] = int(user_val) if str(user_val).strip() != '' else 0

        gender = data.get('gender', '')
        if 'gender_Male' in target_features:
            raw_input['gender_Male'] = 1 if gender == 'Male' else 0
        if 'gender_Other' in target_features:
            raw_input['gender_Other'] = 1 if gender == 'Other' else 0

        ethnicity = data.get('ethnicity', '')
        for eth in ['Black', 'Hispanic', 'Other', 'White']:
            col_name = f'ethnicity_{eth}'
            if col_name in target_features:
                raw_input[col_name] = 1 if ethnicity == eth else 0

        education = data.get('education_level', '')
        for edu in ['Highschool', 'No formal', 'Postgraduate']:
            col_name = f'education_level_{edu}'
            if col_name in target_features:
                raw_input[col_name] = 1 if education == edu else 0

        income = data.get('income_level', '')
        for inc in ['Low', 'Lower-Middle', 'Middle', 'Upper-Middle']:
            col_name = f'income_level_{inc}'
            if col_name in target_features:
                raw_input[col_name] = 1 if income == inc else 0

        employment = data.get('employment_status', '')
        for emp in ['Retired', 'Student', 'Unemployed']:
            col_name = f'employment_status_{emp}'
            if col_name in target_features:
                raw_input[col_name] = 1 if employment == emp else 0

        smoking = data.get('smoking_status', '')
        for smk in ['Former', 'Never']:
            col_name = f'smoking_status_{smk}'
            if col_name in target_features:
                raw_input[col_name] = 1 if smoking == smk else 0

        scaled_input = {}
        for col in target_features:
            val = raw_input.get(col, 0.0)
            if col in scale_map:
                dmin, dmax = scale_map[col]
                val_clipped = max(dmin, min(dmax, val))
                range_val = dmax - dmin
                scaled_input[col] = (val_clipped - dmin) / range_val if range_val != 0 else val_clipped
            else:
                scaled_input[col] = val

        model_df = pd.DataFrame([scaled_input], columns=target_features).fillna(0.0)
        raw_prediction = float(active_model.predict(model_df)[0])

        prediction = float(np.clip(raw_prediction, 60.0, 180.0))

        eq_general, eq_substituted = generate_scaled_equations(active_model, scaled_input)

        return JsonResponse({
            'success': True,
            'prediction': prediction,
            'device_type': device_str,
            'model_type': model_type_str,
            'model_code': model_code,
            'features_count': features_cnt,
            'orig_features_count': orig_features_cnt,
            'r2_score': r2_val,
            'equation_general': eq_general,
            'equation_substituted': f"{eq_substituted} = {prediction:.2f} mg/dL"
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f"Prediction error: {str(e)}"
        }, status=500)
