import pandas as pd
from sqlalchemy import create_engine

# ============================================
# ETL PIPELINE
# ============================================

# 1. EXTRACT — маалымат ал
print("1. Маалымат окулуп жатат...")
df = pd.read_csv('aug_train.csv')
print(f"   Окулду: {len(df)} катар")

# 2. TRANSFORM — тазала
print("2. Тазаланып жатат...")
text_columns = ['gender', 'enrolled_university', 'education_level',
                'major_discipline', 'experience', 'company_size',
                'company_type', 'last_new_job']
for col in text_columns:
    df[col] = df[col].fillna('Unknown')
print(f"   Боштуктар: {df.isnull().sum().sum()}")

# 3. LOAD — базага жүктө
print("3. Базага жүктөлүп жатат...")
engine = create_engine('postgresql://user@host.docker.internal/hr_analytics')
df.to_sql('data_scientists', engine, if_exists='replace', index=False)
print(f"   Жүктөлдү: {len(df)} катар")

print("\nETL Pipeline ийгиликтүү аяктады!")
