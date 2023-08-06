def generate_payload(symbol, resolution, date_format, range_from, range_to):
    return {
        "symbol": symbol,
        "resolution": resolution,
        "date_format": date_format,
        "range_from": range_from,
        "range_to": range_to,
        "cont_flag": "1",
    }
