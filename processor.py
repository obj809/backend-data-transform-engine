"""Data transformation processor for stock market data."""

from typing import Any


def process_stock_data(data: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Aggregate an array of stock price data points into a single summary record.

    Args:
        data: List of stock data records with price, change, day_high, day_low, etc.

    Returns:
        Aggregated record with averaged values and current UTC timestamp.

    Raises:
        ValueError: If input data is empty or missing required fields.
    """
    if not data:
        raise ValueError("Input data cannot be empty")

    required_fields = {
        "symbol",
        "name",
        "price",
        "change",
        "change_percent",
        "day_high",
        "day_low",
        "previous_close",
    }

    first_record = data[0]
    missing = required_fields - set(first_record.keys())
    if missing:
        raise ValueError(f"Missing required fields: {missing}")

    count = len(data)

    avg_price = sum(record["price"] for record in data) / count
    avg_change = sum(record["change"] for record in data) / count
    avg_change_percent = sum(record["change_percent"] for record in data) / count
    avg_day_high = sum(record["day_high"] for record in data) / count
    avg_day_low = sum(record["day_low"] for record in data) / count
    avg_previous_close = sum(record["previous_close"] for record in data) / count

    return {
        "symbol": first_record["symbol"],
        "name": first_record["name"],
        "price": round(avg_price, 2),
        "change": round(avg_change, 4),
        "change_percent": round(avg_change_percent, 6),
        "day_high": round(avg_day_high, 2),
        "day_low": round(avg_day_low, 2),
        "previous_close": round(avg_previous_close, 2),
        "timestamp": "(current UTC time)",
    }
