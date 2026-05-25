"""
高级结构化日志系统
支持 JSON 格式输出、文件轮转、多日志级别管理
"""

import logging
import logging.handlers
import json
import os
from datetime import datetime
from config.settings import UPLOAD_DIR


class JSONFormatter(logging.Formatter):
    """JSON 格式化器"""
    
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # 添加自定义字段
        if hasattr(record, 'user_id'):
            log_data["user_id"] = record.user_id
        if hasattr(record, 'request_id'):
            log_data["request_id"] = record.request_id
        if hasattr(record, 'endpoint'):
            log_data["endpoint"] = record.endpoint
        
        return json.dumps(log_data, ensure_ascii=False)


class ContextFilter(logging.Filter):
    """上下文过滤器，用于注入请求相关信息"""
    
    def __init__(self):
        super().__init__()
        self.user_id = None
        self.request_id = None
        self.endpoint = None
    
    def filter(self, record):
        record.user_id = getattr(self, 'user_id', None)
        record.request_id = getattr(self, 'request_id', None)
        record.endpoint = getattr(self, 'endpoint', None)
        return True


def setup_logging(log_dir: str = None, 
                 json_format: bool = True,
                 max_bytes: int = 10485760,  # 10MB
                 backup_count: int = 5) -> logging.Logger:
    """
    配置日志系统
    
    Args:
        log_dir: 日志文件目录，默认为 UPLOAD_DIR/logs
        json_format: 是否使用 JSON 格式
        max_bytes: 日志文件最大大小（字节）
        backup_count: 备份文件数
    
    Returns:
        Logger 实例
    """
    
    if log_dir is None:
        log_dir = os.path.join(UPLOAD_DIR, 'logs')
    
    # 创建日志目录
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建 logger
    logger = logging.getLogger('pre_system')
    logger.setLevel(logging.DEBUG)
    
    # 清除已有处理器
    logger.handlers.clear()
    
    # 选择格式化器
    if json_format:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    # 添加上下文过滤器
    context_filter = ContextFilter()
    
    # ============ 控制台处理器 (INFO 级别) ============
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(context_filter)
    logger.addHandler(console_handler)
    
    # ============ 文件处理器 (DEBUG 级别) ============
    log_file = os.path.join(log_dir, 'app.log')
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(context_filter)
    logger.addHandler(file_handler)
    
    # ============ 错误文件处理器 (ERROR 级别) ============
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = logging.handlers.RotatingFileHandler(
        error_log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    error_handler.addFilter(context_filter)
    logger.addHandler(error_handler)
    
    return logger, context_filter


# 全局 logger 和过滤器
logger, context_filter = setup_logging()


def get_logger():
    """获取全局 logger 实例"""
    return logger


def get_context_filter():
    """获取上下文过滤器实例"""
    return context_filter


def set_request_context(user_id: int = None, 
                       request_id: str = None, 
                       endpoint: str = None):
    """设置请求上下文信息"""
    context_filter.user_id = user_id
    context_filter.request_id = request_id
    context_filter.endpoint = endpoint


def clear_request_context():
    """清除请求上下文信息"""
    context_filter.user_id = None
    context_filter.request_id = None
    context_filter.endpoint = None
