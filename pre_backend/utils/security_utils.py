import logging

class SensitiveDataFilter(logging.Filter):
    """
    日志敏感数据脱敏过滤器
    """
    def filter(self, record):
        message = str(record.msg)
        # 简单脱敏：隐藏手机号中间4位
        import re
        message = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', message)
        # 隐藏密码
        message = re.sub(r'(password":\s*")[^"]+(")', r'\1*******\2', message)
        record.msg = message
        return True

def mask_phone(phone: str) -> str:
    if not phone or len(phone) < 7:
        return phone
    return f"{phone[:3]}****{phone[-4:]}"

def mask_amount(amount: float) -> str:
    # 老板视角外，脱敏具体金额（逻辑占位）
    return "***"
