# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Any
from google.cloud import firestore

# Hardcode project ID to avoid project number issues on Agent Platform
PROJECT_ID = "qwiklabs-gcp-04-f5e809382e15"
COLLECTION_NAME = "tracked_stocks"

_db_client = None


def get_firestore_client() -> firestore.Client:
    """Returns a singleton Firestore client with the hardcoded project ID."""
    global _db_client
    if _db_client is None:
        _db_client = firestore.Client(project=PROJECT_ID)
    return _db_client


def get_tracked_stocks() -> list[dict[str, Any]]:
    """Retrieves all tracked stocks from the Firestore backend collection.

    Returns:
        A list of dictionaries representing tracked stocks and their current data.
    """
    db = get_firestore_client()
    docs = db.collection(COLLECTION_NAME).stream()
    stocks = []
    for doc in docs:
        data = doc.to_dict()
        data["id"] = doc.id
        stocks.append(data)
    return stocks


def get_stock_details(ticker: str) -> dict[str, Any] | str:
    """Retrieves details for a specific stock ticker from Firestore.

    Args:
        ticker: The stock ticker symbol (e.g. 'AAPL', 'GOOGL', 'NVDA').

    Returns:
        A dictionary of stock details or an error message if not found.
    """
    db = get_firestore_client()
    doc_ref = db.collection(COLLECTION_NAME).document(ticker.upper())
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        data["id"] = doc.id
        return data
    return f"Stock '{ticker.upper()}' is not currently in the tracked stocks collection."


def add_or_update_stock(
    ticker: str,
    company_name: str,
    price: float,
    change_percent: float = 0.0,
    sector: str = "Technology",
    pe_ratio: float = 0.0,
    market_cap: str = "N/A",
    is_favorite: bool = False,
) -> str:
    """Adds a new stock or updates an existing stock in the Firestore collection.

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL', 'GOOGL').
        company_name: Full name of the company.
        price: Current stock price in USD.
        change_percent: Percentage price change (+/-).
        sector: Market sector classification.
        pe_ratio: Price-to-Earnings ratio.
        market_cap: Market capitalization string (e.g. '3.4T').
        is_favorite: Whether the stock is marked as favorite by the user.

    Returns:
        Confirmation message.
    """
    db = get_firestore_client()
    doc_id = ticker.upper()
    stock_data = {
        "ticker": doc_id,
        "company_name": company_name,
        "price": float(price),
        "change_percent": float(change_percent),
        "sector": sector,
        "pe_ratio": float(pe_ratio),
        "market_cap": market_cap,
        "is_favorite": bool(is_favorite),
        "updated_at": firestore.SERVER_TIMESTAMP,
    }
    db.collection(COLLECTION_NAME).document(doc_id).set(stock_data, merge=True)
    return f"Successfully saved stock '{doc_id}' ({company_name}) with price ${price:.2f} to Firestore."


def remove_stock(ticker: str) -> str:
    """Removes a stock from the Firestore tracked stocks collection.

    Args:
        ticker: Stock ticker symbol to remove.

    Returns:
        Confirmation message.
    """
    db = get_firestore_client()
    doc_id = ticker.upper()
    doc_ref = db.collection(COLLECTION_NAME).document(doc_id)
    if doc_ref.get().exists:
        doc_ref.delete()
        return f"Removed stock '{doc_id}' from tracked stocks."
    return f"Stock '{doc_id}' was not found in tracked stocks."
