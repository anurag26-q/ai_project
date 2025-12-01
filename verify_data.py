#!/usr/bin/env python3
"""Simple verification test for transaction data - no dependencies on vector store."""

import json
from pathlib import Path

def verify_transaction_data():
    """Verify all 7 customers and 14 transactions are in the data file."""
    print("=" * 80)
    print("TRANSACTION DATA VERIFICATION")
    print("=" * 80)
    
    # Load transactions
    with open("transactions.json", 'r', encoding='utf-8') as f:
        transactions = json.load(f)
    
    print(f"\n[OK] Loaded {len(transactions)} transactions from transactions.json")
    
    # Verify count
    assert len(transactions) == 14, f"Expected 14 transactions, got {len(transactions)}"
    
    # Get unique customers
    customers = set(txn['customer'] for txn in transactions)
    print(f"[OK] Found {len(customers)} unique customers")
    
    # Verify customer count
    assert len(customers) == 7, f"Expected 7 customers, got {len(customers)}"
    
    # Calculate totals
    total_spending = sum(txn['amount'] for txn in transactions)
    print(f"[OK] Total spending across all customers: Rs.{total_spending:,}")
    
    # Verify expected total
    expected_total = 203900
    assert total_spending == expected_total, f"Expected total Rs.{expected_total:,}, got Rs.{total_spending:,}"
    
    # Show detailed breakdown
    print("\n" + "=" * 80)
    print("DETAILED BREAKDOWN BY CUSTOMER")
    print("=" * 80)
    
    customer_data = {}
    for txn in transactions:
        customer = txn['customer']
        if customer not in customer_data:
            customer_data[customer] = []
        customer_data[customer].append(txn)
    
    # Sort customers alphabetically
    for customer in sorted(customer_data.keys()):
        txns = customer_data[customer]
        total = sum(t['amount'] for t in txns)
        
        print(f"\n{customer}:")
        for txn in sorted(txns, key=lambda x: x['date']):
            print(f"  Transaction ID {txn['id']}: {txn['date']} - {txn['product']} - Rs.{txn['amount']:,}")
        print(f"  Total for {customer}: Rs.{total:,}")
    
    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Customer':<15} {'Transactions':<15} {'Total Spending':<20}")
    print("-" * 80)
    
    for customer in sorted(customer_data.keys()):
        txns = customer_data[customer]
        total = sum(t['amount'] for t in txns)
        print(f"{customer:<15} {len(txns):<15} Rs.{total:,}")
    
    print("-" * 80)
    print(f"{'TOTAL':<15} {len(transactions):<15} Rs.{total_spending:,}")
    print("=" * 80)
    
    # Verify each customer has exactly 2 transactions
    print("\n[VERIFICATION CHECKS]")
    for customer in sorted(customer_data.keys()):
        txn_count = len(customer_data[customer])
        status = "[OK]" if txn_count == 2 else "[ERROR]"
        print(f"{status} {customer}: {txn_count} transactions")
        assert txn_count == 2, f"{customer} should have 2 transactions, got {txn_count}"
    
    print("\n" + "=" * 80)
    print("*** ALL VERIFICATIONS PASSED! ***")
    print("=" * 80)
    print("\n[OK] All 7 customers are present in the data")
    print("[OK] All 14 transactions are present in the data")
    print("[OK] Each customer has exactly 2 transactions")
    print("[OK] Total spending is Rs.203,900")
    print("\n" + "=" * 80)
    
    return True

if __name__ == "__main__":
    try:
        verify_transaction_data()
    except Exception as e:
        print(f"\n[ERROR] Verification failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
