from flask import request


def request_query(schema):
    return {k: request.args.get(k, type=t) for k, t in schema.items()}


def clean_filters(filters: dict) -> dict:
    return {k: v for k, v in filters.items() if v not in ("", None)}
