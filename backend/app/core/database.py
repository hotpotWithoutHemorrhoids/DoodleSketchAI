# """
# 数据库配置和连接管理
# """

# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.pool import NullPool
# import logging

# from app.core.config import settings

# logger = logging.getLogger(__name__)

# # 创建异步数据库引擎
# engine = create_async_engine(
#     settings.DATABASE_URL,
#     echo=settings.DEBUG,
#     pool_pre_ping=True,
#     poolclass=NullPool,  # 禁用连接池，适合开发环境
#     future=True,
# )

# # 创建会话工厂
# AsyncSessionLocal = async_sessionmaker(
#     engine,
#     class_=AsyncSession,
#     expire_on_commit=False,
#     autocommit=False,
#     autoflush=False,
# )

# # 创建基础模型类
# Base = declarative_base()


# async def get_db() -> AsyncSession:
#     """
#     获取数据库会话
#     用于依赖注入
#     """
#     async with AsyncSessionLocal() as session:
#         try:
#             yield session
#         except Exception as e:
#             logger.error(f"Database session error: {e}")
#             await session.rollback()
#             raise
#         finally:
#             await session.close()


# async def init_db():
#     """
#     初始化数据库
#     创建所有表
#     """
#     try:
#         async with engine.begin() as conn:
#             # 导入所有模型以确保它们被注册到 Base.metadata
#             from app.models import video, breakpoint, task, generation_result, user_session, system_config
            
#             # 创建所有表
#             await conn.run_sync(Base.metadata.create_all)
#             logger.info("✅ Database tables created successfully")
            
#     except Exception as e:
#         logger.error(f"❌ Failed to initialize database: {e}")
#         raise


# async def close_db():
#     """
#     关闭数据库连接
#     """
#     try:
#         await engine.dispose()
#         logger.info("✅ Database connections closed")
#     except Exception as e:
#         logger.error(f"❌ Error closing database connections: {e}")


# class DatabaseManager:
#     """数据库管理器"""
    
#     def __init__(self):
#         self.engine = engine
#         self.session_factory = AsyncSessionLocal
    
#     async def create_session(self) -> AsyncSession:
#         """创建新的数据库会话"""
#         return self.session_factory()
    
#     async def execute_raw_sql(self, sql: str, params: dict = None):
#         """执行原生 SQL"""
#         async with self.create_session() as session:
#             try:
#                 result = await session.execute(sql, params or {})
#                 await session.commit()
#                 return result
#             except Exception as e:
#                 await session.rollback()
#                 logger.error(f"Raw SQL execution error: {e}")
#                 raise
    
#     async def check_connection(self) -> bool:
#         """检查数据库连接"""
#         try:
#             async with self.create_session() as session:
#                 await session.execute("SELECT 1")
#                 return True
#         except Exception as e:
#             logger.error(f"Database connection check failed: {e}")
#             return False
    
#     async def get_table_info(self, table_name: str):
#         """获取表信息"""
#         sql = """
#         SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY
#         FROM INFORMATION_SCHEMA.COLUMNS
#         WHERE TABLE_SCHEMA = :schema AND TABLE_NAME = :table_name
#         ORDER BY ORDINAL_POSITION
#         """
        
#         async with self.create_session() as session:
#             result = await session.execute(
#                 sql, 
#                 {"schema": settings.DB_NAME, "table_name": table_name}
#             )
#             return result.fetchall()


# # 创建全局数据库管理器实例
# db_manager = DatabaseManager()


# # 数据库健康检查
# async def health_check() -> dict:
#     """数据库健康检查"""
#     try:
#         is_connected = await db_manager.check_connection()
#         return {
#             "status": "healthy" if is_connected else "unhealthy",
#             "database": settings.DB_NAME,
#             "host": settings.DB_HOST,
#             "port": settings.DB_PORT,
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "error": str(e),
#             "database": settings.DB_NAME,
#         }
