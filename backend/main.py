import time
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import RedirectResponse
from typing import Dict, Any

# 导入 Athanor 核心组件
from cleaner import AthanorPurifier
from analyzer import KnowledgeCrystallizer

# --- 日志系统：监控熔炉状态 ---
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [炼金反应堆] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# --- API 实例：汉化元数据 ---
app = FastAPI(
    title="Athanor 炼金反应堆",
    description="信号高于噪音：原子级知识转化引擎。将混乱的书签 HTML 转化为有序的知识星群。",
    version="1.0.0"
)

# --- 跨域配置：允许前端访问 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 组件初始化 ---
purifier = AthanorPurifier()
crystallizer = KnowledgeCrystallizer(n_clusters=8)

@app.get("/", include_in_schema=False)
async def 首页跳转():
    """根路径自动跳转到交互式操作台"""
    return RedirectResponse(url="/docs")

@app.get("/health", summary="系统状态检测", tags=["系统监控"])
async def 健康检查():
    """查看反应堆是否在线"""
    return {
        "状态": "在线",
        "核心": "稳定",
        "运行时间": f"{time.process_time():.2f}s"
    }

@app.post("/transmute", summary="执行熔炼（书签转化）", tags=["核心流程"])
async def 执行熔炼(file: UploadFile = File(..., description="请上传从浏览器导出的 HTML 书签文件")):
    """
    ### 炼金流程说明：
    1. **注入**: 接收原始 HTML 文件
    2. **净化 (Purification)**: 剔除冗余代码，萃取 URL 与标题
    3. **结晶 (Crystallization)**: 利用机器学习算法按语义自动分类
    4. **析出**: 输出星群 JSON 数据
    """
    if not file.filename.endswith(".html"):
        raise HTTPException(status_code=400, detail="文件格式错误。必须是 .html 结尾的书签文件。")

    计时开始 = time.perf_counter()
    logger.info(f"📥 接收原料: {file.filename}")

    try:
        # 读取字节流
        原始内容 = await file.read()
        
        # 第一阶段：净化
        信号列表 = await run_in_threadpool(purifier.smelt, 原始内容)
        
        if not 信号列表:
            return {"成功": False, "信息": "未能在该物质中提取到任何有效信号。"}

        # 动态调整星群密度
        星群数量 = max(2, min(8, len(信号列表) // 10))
        crystallizer.n_clusters = 星群数量
        
        # 第二阶段：结晶与时间线分析
        星群结晶 = await run_in_threadpool(crystallizer.crystallize, 信号列表)
        时间热力图 = await run_in_threadpool(crystallizer.analyze_timeline, 信号列表)

        耗时 = time.perf_counter() - 计时开始
        logger.info(f"✨ 熔炼完成 | 耗时: {耗时:.2f}s | 信号总数: {len(信号列表)}")

        return {
            "成功": True,
            "元数据": {
                "耗时": f"{耗时:.2f}s",
                "信号数量": len(信号列表),
                "结晶密度": 星群数量
            },
            "结果": {
                "时间线": 时间热力图,
                "星群结晶": 星群结晶
            }
        }

    except Exception as e:
        logger.error(f"❌ 熔炼事故: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"反应堆熔毁: {str(e)}")
    finally:
        await file.close()

if __name__ == "__main__":
    import uvicorn
    # 🏮 A-T-H-A-N-O-R 赛博铭牌
    print("\033[36m" + r"""
      ▄▀▄ ▀█▀ █ █ ▄▀▄ █▄ █ ▄▀▄ █▀▄
      █▀█  █  █▀█ █▀█ █ ▀█ █▄█ █▀▄
    """ + "\033[0m")
    print("    🔥 A T H A N O R  反应堆点火成功")
    print("    📡 交互控制台地址: http://127.0.0.1:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")