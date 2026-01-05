"""
API 模块
"""
from fastapi import APIRouter

from .file_upload import router as file_router
api_router = APIRouter()

api_router.include_router(file_router, prefix="/upload")