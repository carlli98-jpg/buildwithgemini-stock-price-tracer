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

from google.cloud import firestore

PROJECT_ID = "qwiklabs-gcp-04-f5e809382e15"
COLLECTION_NAME = "tracked_stocks"

SEED_STOCKS = [
    {
        "ticker": "AAPL",
        "company_name": "Apple Inc.",
        "price": 225.50,
        "change_percent": 1.45,
        "sector": "Technology",
        "pe_ratio": 32.1,
        "market_cap": "3.44T",
        "is_favorite": True,
    },
    {
        "ticker": "GOOGL",
        "company_name": "Alphabet Inc.",
        "price": 178.20,
        "change_percent": 0.85,
        "sector": "Technology",
        "pe_ratio": 22.4,
        "market_cap": "2.21T",
        "is_favorite": True,
    },
    {
        "ticker": "NVDA",
        "company_name": "NVIDIA Corporation",
        "price": 145.80,
        "change_percent": 3.12,
        "sector": "Technology",
        "pe_ratio": 58.6,
        "market_cap": "3.58T",
        "is_favorite": True,
    },
    {
        "ticker": "MSFT",
        "company_name": "Microsoft Corporation",
        "price": 420.10,
        "change_percent": -0.45,
        "sector": "Technology",
        "pe_ratio": 34.2,
        "market_cap": "3.12T",
        "is_favorite": False,
    },
    {
        "ticker": "AMZN",
        "company_name": "Amazon.com Inc.",
        "price": 208.50,
        "change_percent": 2.10,
        "sector": "Consumer Cyclical",
        "pe_ratio": 44.1,
        "market_cap": "2.18T",
        "is_favorite": False,
    },
    {
        "ticker": "TSLA",
        "company_name": "Tesla Inc.",
        "price": 315.40,
        "change_percent": 4.80,
        "sector": "Consumer Cyclical",
        "pe_ratio": 88.5,
        "market_cap": "1.01T",
        "is_favorite": False,
    },
]


def seed():
    print(f"Seeding Firestore collection '{COLLECTION_NAME}' in project '{PROJECT_ID}'...")
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection(COLLECTION_NAME)

    for stock in SEED_STOCKS:
        doc_id = stock["ticker"]
        stock_data = {
            **stock,
            "updated_at": firestore.SERVER_TIMESTAMP,
        }
        collection_ref.document(doc_id).set(stock_data, merge=True)
        print(f"  - Seeded stock: {doc_id} ({stock['company_name']}) @ ${stock['price']}")

    print("Firestore seeding complete!")


if __name__ == "__main__":
    seed()
