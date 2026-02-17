import pandas as pd
import numpy as np
from faker import Faker
import hashlib
import config

fake = Faker()

def anonymize_pii(value):
    """Tokenize PII using a salted hash."""
    return hashlib.sha256((str(value) + config.SALT).encode()).hexdigest()[:16]

def generate_synthetic_data(num_records=100):
    """Generates synthetic transaction data for testing."""
    data = []
    for _ in range(num_records):
        transaction = {
            'transaction_id': fake.uuid4(),
            'customer_id': fake.ssn(), # Will be anonymized
            'amount': round(np.random.uniform(10.0, 15000.0), 2),
            'timestamp': fake.date_time_this_year(),
            'merchant': fake.company(),
            'category': np.random.choice(['Retail', 'Travel', 'Food', 'Online Services', 'Utilities']),
            'zip_code': fake.zipcode(),
            'is_fraud': np.random.choice([0, 1], p=[0.95, 0.05]) # 5% fraud rate
        }
        data.append(transaction)
    
    df = pd.DataFrame(data)
    
    # Anonymize Customer ID immediately
    df['customer_id_token'] = df['customer_id'].apply(anonymize_pii)
    df.drop(columns=['customer_id'], inplace=True)
    
    return df

def load_data(uploaded_file=None, column_mapping=None):
    """
    Loads data from a file or generates synthetic data.
    - uploaded_file: Streamlit file object or path
    - column_mapping: Dict mapping {'user_col': 'internal_col'}
    """
    df = None
    
    # 1. Try uploaded file
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            return None 

    # 2. Try local default file (only if no upload)
    elif df is None:
        try:
            df = pd.read_csv("fraudTest.csv")
        except FileNotFoundError:
            return generate_synthetic_data()
            
    if df is not None:
        # Apply Logic:
        # A) If explicit mapping provided, use it
        if column_mapping:
            # Invert the mapping: User selected "MyPrice" for "amount", so we rename "MyPrice" -> "amount"
            # The UI usually gives us {'amount': 'MyPrice'}, so we need {v: k}
            rename_map = {v: k for k, v in column_mapping.items() if v}
            df.rename(columns=rename_map, inplace=True)
            
        # B) Auto-detect if it looks like the standard 'fraudTest.csv' and no mapping was done for key fields
        elif 'cc_num' in df.columns and 'amt' in df.columns:
             column_map = {
                'trans_num': 'transaction_id',
                'cc_num': 'customer_id',
                'amt': 'amount',
                'trans_date_trans_time': 'timestamp',
                'zip': 'zip_code'
            }
             df.rename(columns=column_map, inplace=True)
        
        # Ensure 'customer_id' exists for tokenization or generate a dummy one if missing (to prevent crash)
        if 'customer_id' not in df.columns:
            # If user didn't map it, create a mock one so the app runs
            df['customer_id'] = [fake.ssn() for _ in range(len(df))]
            
        # Tokenize PII
        if 'customer_id' in df.columns:
            df['customer_id_token'] = df['customer_id'].apply(anonymize_pii)
            
            # STRICT PII REMOVAL
            pii_cols = ['customer_id', 'first', 'last', 'street', 'dob', 'cc_num']
            df.drop(columns=[c for c in pii_cols if c in df.columns], inplace=True, errors='ignore')
            
        # Ensure other critical columns exist with defaults if missing
        required_cols = {'amount': 0.0, 'category': 'Unknown', 'merchant': 'Unknown', 'timestamp': pd.Timestamp.now()}
        for col, default in required_cols.items():
            if col not in df.columns:
                df[col] = default
            
        return df

    return generate_synthetic_data()
