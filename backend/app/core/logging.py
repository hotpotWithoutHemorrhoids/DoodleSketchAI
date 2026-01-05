# """
# 日志配置和设置
# """

# import logging
# import sys
# import json
# from typing import Any, Dict
# from datetime import datetime
# from pathlib import Path

# import structlog
# from pythonjsonlogger import jsonlogger

# from app.core.config import settings


# class JSONFormatter(jsonlogger.JsonFormatter):
#     """自定义 JSON 格式化器"""
    
#     def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
#         """添加自定义字段"""
#         super().add_fields(log_record, record, message_dict)
        
#         # 添加时间戳
#         if not log_record.get('timestamp'):
#             log_record['timestamp'] = datetime.utcnow().isoformat()
        
#         # 添加日志级别
#         if log_record.get('level'):
#             log_record['level'] = log_record['level'].upper()
#         else:
#             log_record['level'] = record.levelname
        
#         # 添加服务信息
#         log_record['service'] = settings.PROJECT_NAME
#         log_record['version'] = settings.VERSION
        
#         # 添加环境和模块信息
#         if not log_record.get('logger'):
#             log_record['logger'] = record.name
        
#         # 添加异常信息
#         if record.exc_info:
#             log_record['exception'] = self.formatException(record.exc_info)
        
#         # 移除不需要的字段
#         for field in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 'filename', 
#                      'module', 'lineno', 'funcName', 'created', 'msecs', 'relativeCreated', 
#                      'thread', 'threadName', 'processName', 'process']:
#             log_record.pop(field, None)


# class ColoredFormatter(logging.Formatter):
#     """彩色控制台格式化器"""
    
#     # 颜色代码
#     COLORS = {
#         'DEBUG': '\033[36m',     # 青色
#         'INFO': '\033[32m',      # 绿色
#         'WARNING': '\033[33m',   # 黄色
#         'ERROR': '\033[31m',      # 红色
#         'CRITICAL': '\033[35m',   # 紫色
#     }
#     RESET = '\033[0m'
    
#     def format(self, record):
#         """格式化日志记录"""
#         # 添加颜色
#         level_color = self.COLORS.get(record.levelname, '')
#         record.levelname = f"{level_color}{record.levelname}{self.RESET}"
        
#         # 格式化时间
#         timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
#         # 构建日志消息
#         log_message = (
#             f"{timestamp} | {record.levelname} | {record.name} | "
#             f"{record.filename}:{record.lineno} | {record.getMessage()}"
#         )
        
#         # 添加异常信息
#         if record.exc_info:
#             log_message += f"\n{self.formatException(record.exc_info)}"
        
#         return log_message


# def setup_logging():
#     """设置日志配置"""
    
#     # 创建根日志记录器
#     root_logger = logging.getLogger()
#     root_logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
#     # 清除现有处理器
#     root_logger.handlers.clear()
    
#     # 控制台处理器
#     console_handler = logging.StreamHandler(sys.stdout)
#     console_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
    
#     if settings.LOG_FORMAT.lower() == 'json':
#         # JSON 格式
#         console_handler.setFormatter(JSONFormatter(
#             fmt='%(timestamp)s %(level)s %(logger)s %(message)s',
#             datefmt='%Y-%m-%d %H:%M:%S'
#         ))
#     else:
#         # 彩色格式
#         console_handler.setFormatter(ColoredFormatter())
    
#     root_logger.addHandler(console_handler)
    
#     # 文件处理器（如果配置了日志文件）
#     if settings.LOG_FILE:
#         # 确保日志目录存在
#         log_path = Path(settings.LOG_FILE)
#         log_path.parent.mkdir(parents=True, exist_ok=True)
        
#         file_handler = logging.FileHandler(settings.LOG_FILE, encoding='utf-8')
#         file_handler.setLevel(getattr(logging, settings.LOG_LEVEL.upper()))
        
#         if settings.LOG_FORMAT.lower() == 'json':
#             file_handler.setFormatter(JSONFormatter(
#                 fmt='%(timestamp)s %(level)s %(logger)s %(message)s',
#                 datefmt='%Y-%m-%d %H:%M:%S'
#             ))
#         else:
#             file_handler.setFormatter(logging.Formatter(
#                 '%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s'
#             ))
        
#         root_logger.addHandler(file_handler)
    
#     # 配置第三方库日志级别
#     logging.getLogger("uvicorn").setLevel(logging.INFO)
#     logging.getLogger("uvicorn.access").setLevel(logging.INFO)
#     logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
#     logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
#     logging.getLogger("httpx").setLevel(logging.WARNING)
    
#     # 配置 structlog
#     structlog.configure(
#         processors=[
#             structlog.stdlib.filter_by_level,
#             structlog.stdlib.add_logger_name,
#             structlog.stdlib.add_log_level,
#             structlog.stdlib.PositionalArgumentsFormatter(),
#             structlog.processors.TimeStamper(fmt="iso"),
#             structlog.processors.StackInfoRenderer(),
#             structlog.processors.format_exc_info,
#             structlog.processors.UnicodeDecoder(),
#             structlog.processors.JSONRenderer()
#         ],
#         context_class=dict,
#         logger_factory=structlog.stdlib.LoggerFactory(),
#         wrapper_class=structlog.stdlib.BoundLogger,
#         cache_logger_on_first_use=True,
#     )


# def get_logger(name: str) -> logging.Logger:
#     """获取日志记录器"""
#     return logging.getLogger(name)


# class LoggerMixin:
#     """日志记录器混入类"""
    
#     @property
#     def logger(self) -> logging.Logger:
#         """获取当前类的日志记录器"""
#         return logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)


# # 预定义的日志记录器
# app_logger = logging.getLogger("app")
# api_logger = logging.getLogger("app.api")
# db_logger = logging.getLogger("app.database")
# task_logger = logging.getLogger("app.task")
# cpp_logger = logging.getLogger("app.cpp")


# def log_function_call(func):
#     """函数调用日志装饰器"""
#     def wrapper(*args, **kwargs):
#         logger = logging.getLogger(func.__module__)
#         logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
        
#         try:
#             result = func(*args, **kwargs)
#             logger.debug(f"{func.__name__} returned {result}")
#             return result
#         except Exception as e:
#             logger.error(f"{func.__name__} raised {e}")
#             raise
    
#     return wrapper


# async def log_async_function_call(func):
#     """异步函数调用日志装饰器"""
#     async def wrapper(*args, **kwargs):
#         logger = logging.getLogger(func.__module__)
#         logger.debug(f"Calling async {func.__name__} with args={args}, kwargs={kwargs}")
        
#         try:
#             result = await func(*args, **kwargs)
#             logger.debug(f"async {func.__name__} returned {result}")
#             return result
#         except Exception as e:
#             logger.error(f"async {func.__name__} raised {e}")
#             raise
    
#     return wrapper


# def log_performance(func):
#     """性能监控装饰器"""
#     import time
    
#     def wrapper(*args, **kwargs):
#         logger = logging.getLogger(func.__module__)
#         start_time = time.time()
        
#         try:
#             result = func(*args, **kwargs)
#             end_time = time.time()
#             execution_time = end_time - start_time
            
#             logger.info(
#                 f"Performance: {func.__name__} executed in {execution_time:.4f}s",
#                 extra={
#                     "function": func.__name__,
#                     "execution_time": execution_time,
#                     "args_count": len(args),
#                     "kwargs_count": len(kwargs),
#                 }
#             )
            
#             return result
#         except Exception as e:
#             end_time = time.time()
#             execution_time = end_time - start_time
            
#             logger.error(
#                 f"Performance: {func.__name__} failed after {execution_time:.4f}s",
#                 extra={
#                     "function": func.__name__,
#                     "execution_time": execution_time,
#                     "error": str(e),
#                 },
#                 exc_info=True
#             )
#             raise
    
#     return wrapper
