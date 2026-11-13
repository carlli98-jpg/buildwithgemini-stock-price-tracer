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

import os
from typing import Any
import httpx


def fetch_live_stock_quote(ticker: str) -> dict[str, Any] | str:
    """Fetches real-time stock price and market statistics for a ticker symbol.

    Args:
        ticker: Stock ticker symbol (e.g. 'AAPL', 'GOOGL', 'NVDA', 'TSLA').

    Returns:
        A dictionary containing the symbol, current price, previous close,
        price change, percentage change, day high/low, and currency.
    """
    symbol = ticker.strip().upper()
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url, headers=headers)
            if resp.status_code != 200:
                return f"Could not fetch quote for ticker '{symbol}'. Status code: {resp.status_code}"

            data = resp.json()
            results = data.get("chart", {}).get("result")
            if not results:
                return f"Ticker '{symbol}' not found or no market data available."

            meta = results[0].get("meta", {})
            current_price = meta.get("regularMarketPrice")
            prev_close = meta.get("chartPreviousClose")
            day_high = meta.get("regularMarketDayHigh")
            day_low = meta.get("regularMarketDayLow")

            change = round(current_price - prev_close, 2) if current_price and prev_close else 0.0
            change_pct = round((change / prev_close) * 100, 2) if prev_close and prev_close > 0 else 0.0

            return {
                "ticker": symbol,
                "price": current_price,
                "previous_close": prev_close,
                "change": change,
                "change_percent": change_pct,
                "day_high": day_high,
                "day_low": day_low,
                "currency": meta.get("currency", "USD"),
                "exchange": meta.get("exchangeName", "Unknown"),
            }
    except Exception as e:
        return f"Error fetching quote for '{symbol}': {str(e)}"


def get_currency_exchange_rates(
    base_currency: str = "USD",
    target_currencies: str = "EUR,GBP,JPY,CAD,AUD,CHF,INR",
) -> dict[str, Any] | str:
    """Fetches real-time foreign currency exchange rates from the open ExchangeRate API.
    Use this to convert stock prices and portfolio valuations into international currencies.

    Args:
        base_currency: The base currency code to convert from (default: 'USD').
        target_currencies: Comma-separated list of target currency codes (e.g. 'EUR,GBP,JPY,CAD').

    Returns:
        A dictionary containing the base currency, timestamp, and target conversion rates.
    """
    base = base_currency.strip().upper()
    api_key = os.environ.get("EXCHANGE_RATE_API_KEY", "")
    # Support open free tier without key or with custom key if provided
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}" if api_key else f"https://open.er-api.com/v6/latest/{base}"

    try:
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(url)
            if resp.status_code != 200:
                return f"Could not fetch exchange rates for {base}. HTTP status: {resp.status_code}"

            data = resp.json()
            if data.get("result") != "success":
                return f"Error retrieving exchange rates: {data.get('error-type', 'Unknown error')}"

            rates = data.get("rates", {})
            targets = [c.strip().upper() for c in target_currencies.split(",") if c.strip()]
            filtered_rates = {cur: rates[cur] for cur in targets if cur in rates} if targets else rates

            return {
                "base_currency": base,
                "last_updated": data.get("time_last_update_utc", "N/A"),
                "rates": filtered_rates,
            }
    except Exception as e:
        return f"Error fetching exchange rates for '{base}': {str(e)}"
