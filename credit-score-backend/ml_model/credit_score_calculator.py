import numpy as np
from typing import Dict, List, Union, Tuple

def calculate_credit_score(data: Dict[str, Union[float, int]]) -> Tuple[int, List[Dict[str, Union[str, List[str]]]]]:
    """
    Calculate credit score and provide improvement recommendations based on financial data.
    
    Args:
        data: Dictionary containing financial information
        
    Returns:
        Tuple containing:
        - Credit score (300-850)
        - List of improvement recommendations
    """
    score = 300  # Base score
    improvements = []
    
    # Payment History (35% impact)
    if all(k in data for k in ['on_time_payments', 'late_payments', 'missed_payments']):
        total_payments = data['on_time_payments'] + data['late_payments'] + data['missed_payments']
        if total_payments > 0:
            payment_score = (data['on_time_payments'] / total_payments) * 200
            score += payment_score
            
            if data['late_payments'] > 0 or data['missed_payments'] > 0:
                improvements.append({
                    "timeframe": "6-12 months",
                    "action": "Improve Payment History",
                    "impact": "+50 points",
                    "steps": [
                        "Set up automatic payments",
                        "Create payment reminders",
                        "Build an emergency fund",
                        "Contact creditors if you might miss a payment"
                    ]
                })

    # Credit Utilization (30% impact)
    if all(k in data for k in ['credit_limit', 'current_balance']):
        if data['credit_limit'] > 0:
            utilization = (data['current_balance'] / data['credit_limit']) * 100
            utilization_score = max(0, 150 - (utilization * 1.5))
            score += utilization_score
            
            if utilization > 30:
                improvements.append({
                    "timeframe": "1-3 months",
                    "action": "Reduce Credit Utilization",
                    "impact": "+30 points",
                    "steps": [
                        f"Aim to reduce utilization from {utilization:.1f}% to below 30%",
                        "Make multiple payments per month",
                        "Request a credit limit increase",
                        "Consider debt consolidation"
                    ]
                })

    # Debt-to-Income Ratio (15% impact)
    if all(k in data for k in ['monthly_income', 'monthly_expenses']):
        if data['monthly_income'] > 0:
            dti_ratio = (data['monthly_expenses'] / data['monthly_income']) * 100
            dti_score = max(0, 100 - (dti_ratio))
            score += dti_score
            
            if dti_ratio > 43:
                improvements.append({
                    "timeframe": "3-6 months",
                    "action": "Improve Debt-to-Income Ratio",
                    "impact": "+40 points",
                    "steps": [
                        "Create a budget to reduce expenses",
                        "Look for additional income sources",
                        "Negotiate better interest rates",
                        "Consider debt consolidation"
                    ]
                })

    # Credit Mix (10% impact)
    credit_types = {
        'revolving': any(data.get(t, 0) > 0 for t in ['credit_card_debt']),
        'installment': any(data.get(t, 0) > 0 for t in ['personal_loan', 'student_loan', 'mortgage'])
    }
    
    # Calculate credit mix score
    if credit_types['revolving'] and credit_types['installment']:
        mix_score = 100  # Perfect mix: both revolving and installment credit
    elif credit_types['revolving'] or credit_types['installment']:
        mix_score = 50   # Partial mix: only one type of credit
    else:
        mix_score = 0    # No credit mix
    
    score += mix_score
    
    if mix_score < 100:
        improvements.append({
            "timeframe": "6-12 months",
            "action": "Diversify Credit Mix",
            "impact": "+25 points",
            "steps": [
                "Consider adding a mix of revolving and installment credit",
                "Maintain both credit cards and installment loans responsibly",
                "Focus on managing existing credit well before adding new accounts",
                "Keep older accounts open to build credit history"
            ]
        })

    # Savings Impact (10% impact)
    if 'savings' in data and 'monthly_income' in data and data['monthly_income'] > 0:
        savings_ratio = (data['savings'] / data['monthly_income'])
        savings_score = min(100, savings_ratio * 50)
        score += savings_score
        
        if savings_ratio < 3:  # Less than 3 months of expenses saved
            improvements.append({
                "timeframe": "6-12 months",
                "action": "Build Emergency Savings",
                "impact": "+20 points",
                "steps": [
                    "Set up automatic savings transfers",
                    "Save at least 20% of monthly income",
                    "Build 3-6 months emergency fund",
                    "Consider high-yield savings accounts"
                ]
            })

    # Ensure score is within valid range
    score = max(300, min(850, round(score)))
    
    # Sort improvements by impact (convert "+XX points" to numbers)
    improvements.sort(key=lambda x: int(x['impact'].split()[0][1:]), reverse=True)
    
    return score, improvements 