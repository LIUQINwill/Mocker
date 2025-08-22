"""
FastAPI主应用
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .api.api import api_router, proxy_router
from .core.config import settings

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="一个强大的Mock API平台，用于开发和测试",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 包含Mock代理路由
app.include_router(proxy_router, prefix=settings.MOCK_PREFIX)


@app.get("/", response_class=HTMLResponse)
async def root():
    """根路径 - 返回欢迎页面"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Mocker API Platform</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .links { display: flex; justify-content: center; gap: 20px; margin-top: 30px; }
            .link { padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .link:hover { background: #0056b3; }
            .status { text-align: center; margin: 20px 0; color: #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Mocker API Platform</h1>
            <div class="status">✅ 服务运行正常</div>
            <p style="text-align: center; color: #666;">
                欢迎使用Mocker API平台！这是一个强大的Mock服务工具，帮助您快速创建和管理API模拟接口。
            </p>
            <div class="links">
                <a href="/api/v1/docs" class="link">📚 API文档</a>
                <a href="/api/v1/redoc" class="link">📖 ReDoc文档</a>
            </div>
            <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 5px;">
                <h3>🚀 快速开始</h3>
                <ul>
                    <li><strong>管理接口：</strong> 访问 <code>/api/v1/docs</code> 查看完整API文档</li>
                    <li><strong>Mock服务：</strong> 所有Mock接口都在 <code>/mock/*</code> 路径下</li>
                    <li><strong>前端界面：</strong> 即将推出Web管理界面</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
