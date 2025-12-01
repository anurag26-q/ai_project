"""Data loading and preprocessing for transaction data."""
import json
from pathlib import Path
from typing import List, Dict


def load_transactions(file_path: str = "transactions.json") -> List[Dict]:
    """
    Load transaction data from JSON file.
    
    Args:
        file_path: Path to the transactions JSON file
        
    Returns:
        List of transaction dictionaries
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Transaction file not found: {file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        transactions = json.load(f)
    
    return transactions


def preprocess_transaction(transaction: Dict) -> str:
    """
    Convert a transaction dictionary into a descriptive text string.
    
    Args:
        transaction: Dictionary containing transaction details
        
    Returns:
        Formatted string describing the transaction
        
    Example:
        >>> txn = {"id": 1, "customer": "Amit", "product": "Laptop", "amount": 55000, "date": "2024-01-12"}
        >>> preprocess_transaction(txn)
        "On 2024-01-12, Amit purchased a Laptop for 55000."
    """
    customer = transaction.get("customer", "Unknown")
    product = transaction.get("product", "Unknown Product")
    amount = transaction.get("amount", 0)
    date = transaction.get("date", "Unknown Date")
    txn_id = transaction.get("id", 0)
    
    # Create a detailed description
    text = (
        f"Transaction ID {txn_id}: On {date}, {customer} purchased a {product} "
        f"for ₹{amount}. Customer: {customer}, Product: {product}, "
        f"Amount: {amount}, Date: {date}."
    )
    
    return text


def get_all_transaction_texts() -> List[str]:
    """
    Load all transactions and convert them to text descriptions.
    
    Returns:
        List of formatted transaction strings
    """
    transactions = load_transactions()
    return [preprocess_transaction(txn) for txn in transactions]


def get_transaction_metadata() -> List[Dict]:
    """
    Get metadata for all transactions (useful for filtering and source tracking).
    
    Returns:
        List of metadata dictionaries
    """
    transactions = load_transactions()
    return [
        {
            "id": txn.get("id"),
            "customer": txn.get("customer"),
            "product": txn.get("product"),
            "amount": txn.get("amount"),
            "date": txn.get("date")
        }
        for txn in transactions
    ]


if __name__ == "__main__":
    # Test the data loader
    print("Loading transactions...")
    txns = load_transactions()
    print(f"Loaded {len(txns)} transactions\n")
    
    print("Preprocessed transactions:")
    for txn in txns:
        print(f"- {preprocess_transaction(txn)}")
