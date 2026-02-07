import time
import logging
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import RedirectResponse

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
    version="0.1.0"
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
async def home_redirect():
    """根路径自动跳转到交互式操作台"""
    return RedirectResponse(url="/docs")

@app.get("/health", summary="系统状态检测", tags=["系统监控"])
async def health_check():
    """查看反应堆是否在线"""
    return {
        "状态": "在线",
        "核心": "稳定",
        "运行时间": f"{time.process_time():.2f}s"
    }

@app.post("/transmute", summary="执行熔炼", tags=["核心流程"])
async def execute_transmutation(
    file: UploadFile = File(..., description="请上传从浏览器导出的 HTML 书签文件")
):
    """
    ### 炼金流程说明：
    1. **注入**: 接收原始 HTML 文件
    2. **净化**: 提取有效书签信号
    3. **结晶**: 进行聚类分析和时间线生成
    """
    if not file.filename.endswith(".html"):
        raise HTTPException(status_code=400, detail="文件格式错误。必须是 .html 结尾的书签文件。")

    start_time = time.perf_counter()
    logger.info(f"📥 接收原料: {file.filename}")

    try:
        # 1. 读取并解析
        raw_content = await file.read()
        signal_list = await run_in_threadpool(purifier.smelt, raw_content)
        
        if not signal_list:
            return {"成功": False, "信息": "未能在该物质中提取到任何有效信号。"}

        count = len(signal_list)
        if count < 2:
             return {"成功": False, "信息": "样本过少，无法进行聚类分析。"}

        # 2. 动态调整密度
        n_clusters = max(2, min(8, count // 10))
        crystallizer.n_clusters = n_clusters
        
        # 3. 结晶
        cluster_crystals = await run_in_threadpool(crystallizer.crystallize, signal_list)
        timeline_heatmap = await run_in_threadpool(crystallizer.analyze_timeline, signal_list)
        
        # 4. 深度挖掘 (新增维度)
        domain_territory = await run_in_threadpool(crystallizer.analyze_domains, signal_list)
        activity_hours = await run_in_threadpool(crystallizer.analyze_activity_hours, signal_list)
        semantic_nebula = await run_in_threadpool(crystallizer.analyze_tags_cloud, signal_list)
        persona_data = await run_in_threadpool(crystallizer.generate_persona, signal_list)
        theme_river = await run_in_threadpool(crystallizer.analyze_theme_river, signal_list)
        skill_radar = await run_in_threadpool(crystallizer.analyze_skill_radar, signal_list)

        elapsed_time = time.perf_counter() - start_time
        logger.info(f"✨ 熔炼完成 | 耗时: {elapsed_time:.2f}s | 信号数量: {count}")

        return {
            "成功": True,
            "元数据": {
                "耗时": f"{elapsed_time:.2f}s",
                "信号数量": count,
                "结晶密度": n_clusters
            },
            "结果": {
                "用户画像": persona_data,
                "技能雷达": skill_radar,
                "时间线": timeline_heatmap,
                "星群结晶": cluster_crystals,
                "域名领地": domain_territory,
                "活跃时段": activity_hours,
                "语义星云": semantic_nebula,
                "兴趣河流": theme_river
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
    print("    🔥 A T H A N O R  反应堆点火成功 (v0.1 Stateless)")
    print("    📡 交互控制台地址: http://127.0.0.1:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
