from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import os
import uuid
from app.core.config import settings

router = APIRouter()

@router.post("/video")
async def file_upload(file: UploadFile = File(...)):
    """上传视频文件"""
    try:
        # 验证文件类型
        if not file.filename:
            raise HTTPException(status_code=400, detail="未提供文件")
        
        # 获取文件扩展名
        file_ext = file.filename.split('.')[-1].lower() if '.' in file.filename else ''
        
        # 检查是否为允许的视频格式
        if file_ext not in settings.ALLOWED_VIDEO_FORMATS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"不支持的文件格式。支持的格式: {', '.join(settings.ALLOWED_VIDEO_FORMATS)}"
            )
        print(f"filename: {file.filename}")
        
        # 检查文件大小
        file.file.seek(0, 2)  # 移动到文件末尾
        file_size = file.file.tell()  # 获取文件大小
        file.file.seek(0)  # 移动回文件开头
        
        if file_size > settings.MAX_UPLOAD_SIZE:
            max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"文件大小超过限制。最大允许大小: {max_size_mb:.1f}MB"
            )
        
        # 生成唯一文件名
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        
        # 确保上传目录存在
        upload_dir = os.path.join(settings.UPLOAD_DIR, "videos")
        os.makedirs(upload_dir, exist_ok=True)
        
        # 保存文件
        file_location = os.path.join(upload_dir, unique_filename)
        with open(file_location, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 构建返回信息
        file_url = f"/uploads/videos/{unique_filename}"
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "视频上传成功",
                "data": {
                    "filename": unique_filename,
                    "original_filename": file.filename,
                    "file_url": file_url,
                    "file_size": file_size,
                    "file_type": "video"
                }
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件上传失败: {str(e)}"
        )
