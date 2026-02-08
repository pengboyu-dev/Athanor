# ⚗️ Athanor (炼金炉)

> **Where raw data meets insight.**
> 你的浏览器书签不是死的数据，它们是冻结的思维切片。

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Stack](https://img.shields.io/badge/Astro-Tailwind-orange)
![Privacy](https://img.shields.io/badge/Privacy-Local--Only-red)

**Athanor** 是一个坚持 **Local-first (本地优先)** 的个人数字资产分析器。它像一座炼金炉，接收你凌乱的浏览器书签（Raw Materials），通过清洗、聚类和可视化，将其转化为可被认知的兴趣图谱（Wisdom）。

它拒绝云端上传，拒绝 API 依赖，拒绝将你的记忆交给第三方。

---

## 🛡️ 核心哲学 (Philosophy)

* **Sovereignty (主权)**: 你的数据只属于你。没有服务器，没有账号，没有 "Sync"。
* **Privacy (隐私)**: 这是一个完全离线的黑盒。所有计算都在你的 CPU 上完成。
* **Minimalism (极简)**: 甚至不需要 AI Key。v0.1 版本回归算法本源，用 TF-IDF 和聚类算法挖掘价值。

---

## 📦 原料支持 (Raw Materials)

Athanor 目前支持“冶炼”以下来源的 `Netscape Bookmark File (.html)`：

* Google Chrome
* Microsoft Edge
* Mozilla Firefox

<details>
<summary><strong>如何获取原料？(点击展开)</strong></summary>

* **Chrome / Edge**：设置 → 书签 → 书签管理器 → 导出书签（HTML）
* **Firefox**：书签 → 管理书签 → 导入和备份 → 导出书签（HTML）

</details>

---

## ⚡ 快速开始 (Transmutation)

### 1. 获取炼金炉
前往 [Releases](../../releases) 下载最新版本的压缩包。

### 2. 部署
解压到任意本地目录。

### 3. 点火 (Ignite)
运行启动脚本：
* **Windows**: 双击 `start.bat`
* **macOS / Linux**: 终端运行 `./start.sh`

### 4. 观测
浏览器将自动打开观测台（默认为 `http://localhost:8000`）。上传你的 HTML 文件，等待转化完成。

---

## 🔮 功能特性 (v0.1)

### 📥 摄入 (Ingest)
* **递归结构解析**: 完整保留原本的文件夹层级结构，不丢失上下文。
* **元数据提取**: 精确提取标题、URL、添加时间。

### ⚙️ 转化 (Process)
* **结构归一化**: 抹平不同浏览器的格式差异，建立统一的内部数据模型。
* **物理隔绝**: 数据仅在内存中流转，无数据库，无网络请求，真正的“飞行模式”应用。

### 📊 显现 (Reveal)
* **Persona (用户画像)**:
    *   **赛博身份**: 根据收藏量授予从 `Lv.1 探索者` 到 `Lv.5 赛博贤者` 的动态称号。
    *   **智能标签**: 自动生成核心属性标签（如 `开源极客`、`视听学习者`），构建你的数字人格。
* **Skill Radar (技能雷达)**:
    *   **六维能力图**: 自动分析收藏内容，量化你的技能分布（Coding, AI/ML, Product, Media, Academic, Life）。
* **Theme River (兴趣河流)**:
    *   动态展示兴趣主题随时间的流动与消涨，一眼看穿你的知识迁移路径。
* **Chronos (时间流)**:
    *   **Timeline**: 按月维度的收藏热力图。
    *   **Circadian**: 昼夜活跃节律雷达，揭示你的“数字生物钟”。
* **Territory (领地分析)**:
    *   **域名统计**: 识别你的核心知识来源（GitHub? Bilibili? Arxiv?）。
    *   **语义星云**: 基于本地词频分析生成的动态词云。


---

## ⚠️ 当前限制 (Limitations)
* 🚧 仅支持单文件导入（暂不支持多源合并）。
* 🚧 仅限书签（不含视频/社交媒体收藏）。
* 🚧 只读分析（不修改原始文件）。

## 🗺️ 路线图 (Roadmap)
- [ ] **Necromancy (死灵术)**: 集成 Wayback Machine，复活失效链接 (404)。
- [ ] **Fusion**: 支持多次导入与多源数据合并。
- [ ] **AI Augmentation**: (可选) 接入 LLM 进行更深度的语义总结。
- [ ] **Export**: 分析报告导出。

---

*Built with Python & Astro. Designed for the Observers.*
