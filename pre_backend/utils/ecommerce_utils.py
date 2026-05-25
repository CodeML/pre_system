"""
电商参数校验工具
用于验证不同电商平台的设计参数（尺寸、分辨率等）
"""

# 电商平台标准规范
ECOMMERCE_STANDARDS = {
    "淘宝": {
        "主图": {
            "resolution": "800x800",
            "size_range": "≤500KB",
            "formats": ["JPG", "PNG"]
        },
        "详情页": {
            "resolution": "750px宽",
            "size_range": "无限制",
            "formats": ["JPG", "PNG"]
        },
        "海报": {
            "resolution": "1200x627",
            "size_range": "≤2MB",
            "formats": ["JPG", "PNG"]
        }
    },
    "抖音": {
        "主图": {
            "resolution": "1080x1080",
            "size_range": "≤2MB",
            "formats": ["JPG", "PNG"]
        },
        "视频": {
            "resolution": "1080x1920",
            "size_range": "≤1GB",
            "formats": ["MP4", "MOV"]
        },
        "横版": {
            "resolution": "1920x1080",
            "size_range": "≤1GB",
            "formats": ["MP4", "MOV"]
        }
    },
    "小红书": {
        "主图": {
            "resolution": "1080x1440",
            "size_range": "≤5MB",
            "formats": ["JPG", "PNG"]
        },
        "横版": {
            "resolution": "1920x1440",
            "size_range": "≤5MB",
            "formats": ["JPG", "PNG"]
        },
        "视频": {
            "resolution": "1080x1920",
            "size_range": "≤5GB",
            "formats": ["MP4", "MOV"]
        }
    },
    "Amazon": {
        "主图": {
            "resolution": "500x500",
            "size_range": "≤10MB",
            "formats": ["JPG", "PNG"]
        },
        "详情页": {
            "resolution": "1200x800",
            "size_range": "≤10MB",
            "formats": ["JPG", "PNG"]
        },
        "视频": {
            "resolution": "1920x1080",
            "size_range": "≤1GB",
            "formats": ["MP4"]
        }
    }
}


def validate_ecommerce_params(platform: str, params: dict) -> dict:
    """
    校验电商参数
    返回: {"valid": bool, "errors": [list of error messages]}
    """
    result = {"valid": True, "errors": []}

    if not platform:
        result["valid"] = False
        result["errors"].append("平台不能为空")
        return result

    if platform not in ECOMMERCE_STANDARDS:
        result["valid"] = False
        result["errors"].append(
            f"不支持的平台: {platform}。支持的平台: {', '.join(ECOMMERCE_STANDARDS.keys())}"
        )
        return result

    if not params or not isinstance(params, dict):
        result["valid"] = False
        result["errors"].append("参数必须是有效的字典")
        return result

    # 检查图片类型
    image_type = params.get("type")
    if not image_type:
        result["valid"] = False
        result["errors"].append(f"{platform} 必须指定图片类型 (type)")
        return result

    platform_standards = ECOMMERCE_STANDARDS[platform]

    if image_type not in platform_standards:
        result["valid"] = False
        result["errors"].append(
            f"{platform} 不支持类型 '{image_type}'。支持的类型: {', '.join(platform_standards.keys())}"
        )
        return result

    spec = platform_standards[image_type]

    # 可选：校验分辨率
    if "resolution" in params and params["resolution"]:
        if params["resolution"] != spec["resolution"]:
            result["errors"].append(
                f"分辨率不标准。标准分辨率: {spec['resolution']}, 实际: {params['resolution']}"
            )

    # 可选：校验文件大小
    if "size" in params and params["size"]:
        result["errors"].append(
            f"文件大小要求: {spec['size_range']}, 实际: {params['size']}"
        )

    # 可选：校验格式
    if "format" in params and params["format"]:
        if params["format"] not in spec["formats"]:
            result["errors"].append(
                f"格式不支持。支持的格式: {', '.join(spec['formats'])}, 实际: {params['format']}"
            )

    # 有错误但不是致命错误时，valid 保持为 True（可选字段）
    if result["errors"] and any("必须" in e for e in result["errors"]):
        result["valid"] = False

    return result


def get_platform_specs(platform: str, image_type: str = None) -> dict:
    """
    获取指定平台的规范信息
    """
    if platform not in ECOMMERCE_STANDARDS:
        return {"error": f"不支持的平台: {platform}"}

    specs = ECOMMERCE_STANDARDS[platform]

    if image_type:
        if image_type not in specs:
            return {"error": f"{platform} 不支持类型: {image_type}"}
        return {platform: {image_type: specs[image_type]}}

    return {platform: specs}


def suggest_params(platform: str, image_type: str) -> dict:
    """
    获取推荐参数
    """
    specs = get_platform_specs(platform, image_type)
    if "error" in specs:
        return specs

    return {
        "platform": platform,
        "type": image_type,
        "recommended": specs[platform][image_type]
    }


def validate_multiple_params(params_list: list) -> dict:
    """
    批量校验多个参数
    """
    results = []
    all_valid = True

    for param in params_list:
        platform = param.get("platform")
        param_data = param.get("params", {})
        result = validate_ecommerce_params(platform, param_data)
        results.append({
            "platform": platform,
            "valid": result["valid"],
            "errors": result["errors"]
        })
        if not result["valid"]:
            all_valid = False

    return {
        "all_valid": all_valid,
        "results": results
    }
