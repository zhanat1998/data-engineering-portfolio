from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

# ============================================
# ТАПШЫРМАЛАР (Functions)
# ============================================

def маалымат_ал():
    """1-кадам: CSV окуу"""
    df = pd.read_csv('/Users/user/Documents/data-engineering/aug_train.csv')
    print(f"Маалымат окулду: {len(df)} катар, {len(df.columns)} баган")

def тазала():
    """2-кадам: Маалыматты тазалоо"""
    df = pd.read_csv('/Users/user/Documents/data-engineering/aug_train.csv')
    text_columns = ['gender', 'enrolled_university', 'education_level',
                    'major_discipline', 'experience', 'company_size',
                    'company_type', 'last_new_job']
    for col in text_columns:
        df[col] = df[col].fillna('Unknown')
    df.to_csv('/Users/user/Documents/data-engineering/cleaned_data.csv', index=False)
    print(f"Тазаланды! Боштуктар: {df.isnull().sum().sum()}")

def базага_жүктө():
    """3-кадам: PostgreSQL'ге жүктөө"""
    from sqlalchemy import create_engine
    df = pd.read_csv('/Users/user/Documents/data-engineering/cleaned_data.csv')
    engine = create_engine('postgresql://user@localhost/hr_analytics')
    df.to_sql('data_scientists', engine, if_exists='replace', index=False)
    print(f"Базага жүктөлдү: {len(df)} катар")

# ============================================
# DAG — PIPELINE ТҮЗҮҮ
# ============================================
with DAG(
    dag_id='hr_etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',       # Күн сайын иштейт
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id='маалымат_ал',
        python_callable=маалымат_ал,
    )

    t2 = PythonOperator(
        task_id='тазала',
        python_callable=тазала,
    )

    t3 = PythonOperator(
        task_id='базага_жүктө',
        python_callable=базага_жүктө,
    )

    # ТАРТИП: 1 → 2 → 3
    t1 >> t2 >> t3
