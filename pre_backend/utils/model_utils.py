from typing import Dict, Any


def sqlalchemy_to_dict(obj, exclude: list = None) -> Dict[str, Any]:
    """Convert a SQLAlchemy model instance to dict, excluding fields if needed."""
    if exclude is None:
        exclude = []
    data = {}
    for col in obj.__table__.columns:
        if col.name in exclude:
            continue
        data[col.name] = getattr(obj, col.name)
    return data
