"""
带文件上传功能的测试服务器
"""

import os
import uuid
import aiofiles
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, status, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# 简化的配置
class SimpleConfig:
    PROJECT_NAME = "DoodleSketchAI"
    VERSION = "1.0.0"
    API_V1_STR = "/api/v1"
    UPLOAD_DIR = "uploads"
    DEBUG = True
    MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_FORMATS = ["mp4", "avi", "mov", "wmv", "flv", "webm"]
    ALLOWED_IMAGE_FORMATS = ["jpg", "jpeg", "png", "webp"]

settings = SimpleConfig()

# 创建应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="文件上传测试 API",
    version=settings.VERSION,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 确保上传目录存在
if settings.UPLOAD_DIR and not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    for subdir in ['videos', 'images', 'temp']:
        dir_path = os.path.join(settings.UPLOAD_DIR, subdir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return filename.split('.')[-1].lower() if '.' in filename else ''

def validate_file_type(filename: str, file_type: str = "video") -> bool:
    """验证文件类型"""
    ext = get_file_extension(filename)
    
    if file_type == "video":
        return ext in settings.ALLOWED_VIDEO_FORMATS
    elif file_type == "image":
        return ext in settings.ALLOWED_IMAGE_FORMATS
    
    return False

@app.get("/")
async def root():
    return {"message": "File Upload Test Server Running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/upload/video")
async def upload_video(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """上传视频文件"""
    try:
        # 验证文件类型
        if not validate_file_type(file.filename, "video"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件格式。支持的格式: {', '.join(settings.ALLOWED_VIDEO_FORMATS)}"
            )
        
        # 验证文件大小
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件大小超过限制。最大允许大小: {settings.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )
        
        # 生成唯一文件名
        file_ext = get_file_extension(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{int(file.file.seek(0, 2))}.{file_ext}"
        file.file.seek(0)
        
        # 保存文件
        save_path = os.path.join(settings.UPLOAD_DIR, "videos", unique_filename)
        
        async with aiofiles.open(save_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 构建返回信息
        file_url = f"/uploads/videos/{unique_filename}"
        
        return {
            "success": True,
            "message": "视频上传成功",
            "data": {
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_url": file_url,
                "file_size": file_size,
                "file_type": "video",
                "description": description
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )

@app.post("/api/v1/upload/image")
async def upload_image(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """上传图片文件"""
    try:
        # 验证文件类型
        if not validate_file_type(file.filename, "image"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件格式。支持的格式: {', '.join(settings.ALLOWED_IMAGE_FORMATS)}"
            )
        
        # 验证文件大小
        file.file.seek(0, 2)
        file_size = file.file.tell()
        file.file.seek(0)
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件大小超过限制。最大允许大小: {settings.MAX_UPLOAD_SIZE / (1024*1024):.1f}MB"
            )
        
        # 生成唯一文件名
        file_ext = get_file_extension(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{int(file.file.seek(0, 2))}.{file_ext}"
        file.file.seek(0)
        
        # 保存文件
        save_path = os.path.join(settings.UPLOAD_DIR, "images", unique_filename)
        
        async with aiofiles.open(save_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 构建返回信息
        file_url = f"/uploads/images/{unique_filename}"
        
        return {
            "success": True,
            "message": "图片上传成功",
            "data": {
                "filename": unique_filename,
                "original_filename": file.filename,
                "file_url": file_url,
                "file_size": file_size,
                "file_type": "image",
                "description": description
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )

@app.get("/api/v1/upload/list")
async def list_uploaded_files():
    """获取已上传文件列表"""
    try:
        files_info = []
        
        # 扫描videos目录
        videos_dir = os.path.join(settings.UPLOAD_DIR, "videos")
        if os.path.exists(videos_dir):
            for filename in os.listdir(videos_dir):
                file_path = os.path.join(videos_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    files_info.append({
                        "filename": filename,
                        "file_url": f"/uploads/videos/{filename}",
                        "file_size": stat.st_size,
                        "file_type": "video",
                        "created_at": stat.st_ctime
                    })
        
        # 扫描images目录
        images_dir = os.path.join(settings.UPLOAD_DIR, "images")
        if os.path.exists(images_dir):
            for filename in os.listdir(images_dir):
                file_path = os.path.join(images_dir, filename)
                if os.path.isfile(file_path):
                    stat = os.stat(file_path)
                    files_info.append({
                        "filename": filename,
                        "file_url": f"/uploads/images/{filename}",
                        "file_size": stat.st_size,
                        "file_type": "image",
                        "created_at": stat.st_ctime
                    })
        
        return {
            "success": True,
            "message": "文件列表获取成功",
            "data": {
                "files": files_info,
                "total_count": len(files_info)
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取文件列表失败: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
