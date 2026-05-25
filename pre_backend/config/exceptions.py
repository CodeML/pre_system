"""
全局异常处理模块
提供统一的异常定义和处理器
"""

from fastapi import HTTPException
from pydantic import ValidationError
from typing import Any, Dict
from datetime import datetime


# ============= 自定义异常类 =============

class AppException(Exception):
    """应用通用异常"""
    def __init__(
        self,
        code: str = "APP_ERROR",
        message: str = "应用错误",
        status_code: int = 500,
        details: Dict[str, Any] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(AppException):
    """数据验证异常"""
    def __init__(self, message: str = "数据验证失败", details: Dict[str, Any] = None):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details
        )


class AuthenticationException(AppException):
    """认证异常"""
    def __init__(self, message: str = "认证失败"):
        super().__init__(
            code="AUTHENTICATION_FAILED",
            message=message,
            status_code=401
        )


class AuthorizationException(AppException):
    """授权异常"""
    def __init__(self, message: str = "权限不足"):
        super().__init__(
            code="AUTHORIZATION_FAILED",
            message=message,
            status_code=403
        )


class ResourceNotFound(AppException):
    """资源不存在异常"""
    def __init__(self, resource: str = "资源", resource_id: Any = None):
        message = f"{resource}" + (f" (ID: {resource_id})" if resource_id else "")
        message += "不存在"
        super().__init__(
            code="RESOURCE_NOT_FOUND",
            message=message,
            status_code=404
        )


class DuplicateResourceException(AppException):
    """重复资源异常"""
    def __init__(self, resource: str = "资源", field: str = None):
        message = f"{resource}"
        if field:
            message += f"的 {field}"
        message += "已存在"
        super().__init__(
            code="DUPLICATE_RESOURCE",
            message=message,
            status_code=409
        )


class BusinessLogicException(AppException):
    """业务逻辑异常"""
    def __init__(self, message: str = "业务逻辑错误", details: Dict[str, Any] = None):
        super().__init__(
            code="BUSINESS_ERROR",
            message=message,
            status_code=400,
            details=details
        )


class InvalidOperationException(AppException):
    """非法操作异常"""
    def __init__(self, message: str = "非法操作"):
        super().__init__(
            code="INVALID_OPERATION",
            message=message,
            status_code=400
        )


# ============= 响应格式化 =============

class ErrorResponse:
    """错误响应格式化器"""
    
    @staticmethod
    def format_response(
        code: str,
        message: str,
        status_code: int = 500,
        details: Dict[str, Any] = None,
        timestamp: str = None
    ) -> Dict[str, Any]:
        """格式化错误响应"""
        return {
            "success": False,
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
                "timestamp": timestamp or datetime.utcnow().isoformat()
            },
            "data": None
        }
    
    @staticmethod
    def format_validation_errors(errors: list) -> Dict[str, list]:
        """格式化 Pydantic 验证错误"""
        formatted = {}
        for error in errors:
            field = ".".join(str(loc) for loc in error["loc"][1:])
            if field not in formatted:
                formatted[field] = []
            formatted[field].append({
                "type": error["type"],
                "message": error["msg"]
            })
        return formatted


class SuccessResponse:
    """成功响应格式化器"""
    
    @staticmethod
    def format_response(
        data: Any = None,
        message: str = "操作成功",
        timestamp: str = None
    ) -> Dict[str, Any]:
        """格式化成功响应"""
        return {
            "success": True,
            "message": message,
            "data": data,
            "timestamp": timestamp or datetime.utcnow().isoformat()
        }


# ============= 异常处理器工厂 =============

def create_exception_handlers():
    """创建异常处理器字典"""
    handlers = {}
    
    # 应用异常处理器
    def handle_app_exception(request, exc: AppException):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse.format_response(
                code=exc.code,
                message=exc.message,
                status_code=exc.status_code,
                details=exc.details
            )
        )
    
    handlers[AppException] = handle_app_exception
    
    # HTTPException 处理器
    def handle_http_exception(request, exc: HTTPException):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse.format_response(
                code="HTTP_ERROR",
                message=exc.detail or "HTTP 错误",
                status_code=exc.status_code
            )
        )
    
    handlers[HTTPException] = handle_http_exception
    
    # Pydantic ValidationError 处理器
    def handle_validation_error(request, exc: ValidationError):
        from fastapi.responses import JSONResponse
        errors = exc.errors()
        return JSONResponse(
            status_code=422,
            content=ErrorResponse.format_response(
                code="VALIDATION_ERROR",
                message="数据验证失败",
                status_code=422,
                details=ErrorResponse.format_validation_errors(errors)
            )
        )
    
    handlers[ValidationError] = handle_validation_error
    
    # 通用异常处理器
    def handle_generic_exception(request, exc: Exception):
        from fastapi.responses import JSONResponse
        import traceback
        
        # 记录完整的错误堆栈
        traceback.print_exc()
        
        return JSONResponse(
            status_code=500,
            content=ErrorResponse.format_response(
                code="INTERNAL_SERVER_ERROR",
                message="内部服务器错误",
                status_code=500,
                details={"error": str(exc)} if str(exc) else {}
            )
        )
    
    handlers[Exception] = handle_generic_exception
    
    return handlers


# ============= 辅助函数 =============

def raise_not_found(resource: str, resource_id: Any = None):
    """抛出资源不存在异常"""
    raise ResourceNotFound(resource, resource_id)


def raise_duplicate(resource: str, field: str = None):
    """抛出重复资源异常"""
    raise DuplicateResourceException(resource, field)


def raise_business_error(message: str, details: Dict[str, Any] = None):
    """抛出业务错误异常"""
    raise BusinessLogicException(message, details)


def raise_invalid_operation(message: str):
    """抛出非法操作异常"""
    raise InvalidOperationException(message)


def raise_auth_error(message: str = "认证失败"):
    """抛出认证错误"""
    raise AuthenticationException(message)


def raise_permission_error(message: str = "权限不足"):
    """抛出权限错误"""
    raise AuthorizationException(message)


def raise_validation_error(message: str, details: Dict[str, Any] = None):
    """抛出验证错误"""
    raise ValidationException(message, details)
