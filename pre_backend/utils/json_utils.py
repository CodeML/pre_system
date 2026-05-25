"""
JSON 字段处理工具
- 序列化/反序列化
- JSON 聚合统计
- 类型转换
"""
import json
from typing import Any, Dict, List, Union


def serialize_json(data: Any) -> str:
    """将 Python 对象序列化为 JSON 字符串"""
    if data is None:
        return "[]" if isinstance(data, list) else "{}"
    try:
        return json.dumps(data, ensure_ascii=False, default=str)
    except (TypeError, ValueError) as e:
        print(f"序列化失败: {e}")
        return "[]" if isinstance(data, list) else "{}"


def deserialize_json(data: Union[str, dict, list]) -> Union[Dict, List]:
    """将 JSON 字符串反序列化为 Python 对象"""
    if isinstance(data, (dict, list)):
        return data
    if not data:
        return [] if data == "[]" else {}
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"反序列化失败: {e}")
        return [] if isinstance(data, str) and data.startswith("[") else {}


def merge_json_arrays(arrays: List[Union[str, List]]) -> List:
    """合并多个 JSON 数组"""
    result = []
    for arr in arrays:
        if isinstance(arr, str):
            arr = deserialize_json(arr)
        if isinstance(arr, list):
            result.extend(arr)
    return result


def aggregate_json_stats(items: List[Dict], group_key: str) -> Dict[str, int]:
    """
    按照 group_key 对项目进行分组统计
    例: aggregate_json_stats(users, 'role') -> {'admin': 2, 'user': 5}
    """
    stats = {}
    for item in items:
        if isinstance(item, str):
            item = deserialize_json(item)
        key = item.get(group_key)
        if key:
            stats[key] = stats.get(key, 0) + 1
    return stats


def count_by_json_field(items: List[Dict], field_name: str, match_value: Any) -> int:
    """
    统计 JSON 字段中匹配值的个数
    例: count_by_json_field(tasks, 'status', 'completed') -> 5
    """
    count = 0
    for item in items:
        if isinstance(item, str):
            item = deserialize_json(item)
        if item.get(field_name) == match_value:
            count += 1
    return count


def filter_json_items(items: List[Dict], field_name: str, values: List[Any]) -> List[Dict]:
    """
    按照字段值过滤 JSON 项目
    例: filter_json_items(tasks, 'status', ['completed', 'pending'])
    """
    result = []
    for item in items:
        if isinstance(item, str):
            item = deserialize_json(item)
        if item.get(field_name) in values:
            result.append(item)
    return result


def extract_json_field(items: List[Dict], field_name: str) -> List:
    """
    提取所有项目的某个 JSON 字段
    例: extract_json_field(materials, 'tags') -> [['a', 'b'], ['c']]
    """
    result = []
    for item in items:
        if isinstance(item, str):
            item = deserialize_json(item)
        value = item.get(field_name)
        if value:
            result.append(value)
    return result


def json_to_csv_row(data: Union[str, Dict], fields: List[str]) -> str:
    """
    将 JSON 数据转换为 CSV 行
    例: json_to_csv_row({'name': 'Project1', 'status': 'active'}, ['name', 'status'])
        -> 'Project1,active'
    """
    if isinstance(data, str):
        data = deserialize_json(data)
    row = []
    for field in fields:
        value = data.get(field, "")
        # CSV 转义处理
        if isinstance(value, str) and ("," in value or '"' in value):
            value = f'"{value}"'
        row.append(str(value))
    return ",".join(row)


def sum_json_numbers(items: List[Dict], field_name: str) -> Union[int, float]:
    """
    对 JSON 字段中的数字求和
    例: sum_json_numbers(tasks, 'progress') -> 250
    """
    total = 0
    for item in items:
        if isinstance(item, str):
            item = deserialize_json(item)
        value = item.get(field_name, 0)
        try:
            total += float(value)
        except (TypeError, ValueError):
            continue
    return total


def average_json_numbers(items: List[Dict], field_name: str) -> float:
    """
    计算 JSON 字段中数字的平均值
    """
    if not items:
        return 0.0
    total = sum_json_numbers(items, field_name)
    return round(total / len(items), 2)
