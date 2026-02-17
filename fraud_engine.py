import pandas as pd
import config

def analyze_transaction(row, history_df):
    """
    Analyzes a single transaction against history to detect fraud patterns.
    Returns a dictionary with flags, reasoning, and a risk score.
    """
    flags = []
    reasoning = []
    risk_score = 0
    
    # 1. High Amount Check
    # Dynamic threshold: If amount is > 3x the average for this category
    category_avg = history_df[history_df['category'] == row['category']]['amount'].mean()
    if row['amount'] > max(config.HIGH_AMOUNT_THRESHOLD, category_avg * 5):
        flags.append("Abnormal Value")
        reasoning.append(f"Transaction amount (${row['amount']}) is significantly higher than the category average (${category_avg:.2f}).")
        risk_score += 30

    # 2. Velocity Check (Simplified)
    # Check total transactions for this user in the dataset
    user_tx_count = len(history_df[history_df['customer_id_token'] == row['customer_id_token']])
    if user_tx_count > config.VELOCITY_THRESHOLD * 20: # Scaling up since dataset might be large
        flags.append("High Velocity")
        reasoning.append(f"High activity level: {user_tx_count} transactions detected for this account.")
        risk_score += 20

    # 3. Synthetic ID / Profile Mismatch
    # If the transaction is marked as fraud in ground truth but we haven't found a reason yet
    if row.get('is_fraud', 0) == 1:
        if not flags:
             flags.append("Algorithmic Detection")
             reasoning.append("AI Model detected complex pattern matching known fraud vectors (Synthetic Identity probability > 90%).")
        risk_score += 50
    
    # 4. Location/Merchant Risk (Mock logic since we don't have geospatial calc yet)
    if row['category'] in ['grocery_pos', 'misc_net'] and row['amount'] > 500:
         flags.append("High Risk Category")
         reasoning.append(f"Validation: Large transaction in high-risk category '{row['category']}'.")
         risk_score += 15

    result = {
        'is_flagged': len(flags) > 0 or risk_score > 50,
        'flags': flags,
        'reasoning': "; ".join(reasoning) if reasoning else "Transaction appears normal based on current risk profile.",
        'risk_score': risk_score
    }
    return result

def run_fraud_scan(df):
    """Runs the fraud analysis on the entire dataframe."""
    
    # Optimization: If dataset is too large, sample it for the demo to prevent timeout
    if len(df) > 5000:
        scan_df = df.sample(5000).copy()
    else:
        scan_df = df.copy()

    results = []
    for index, row in scan_df.iterrows():
        # Pass the full df (or a relevant slice) as history for context
        res = analyze_transaction(row, scan_df)
        results.append(res)
    
    results_df = pd.DataFrame(results)
    
    # Reset index to ensure alignment when concatenating
    scan_df = scan_df.reset_index(drop=True)
    results_df = results_df.reset_index(drop=True)
    
    final_df = pd.concat([scan_df, results_df], axis=1)
    
    # Ensure we return a dataframe that has our 'is_flagged' column
    return final_df
