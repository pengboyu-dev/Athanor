from collections import defaultdict
from typing import List, Dict, Any, Optional

# 催化剂检查：确保炼金试剂存在
try:
    import jieba
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    DEPENDENCIES_INSTALLED = True
except ImportError:
    DEPENDENCIES_INSTALLED = False

class KnowledgeCrystallizer:
    """
    [炼金组件]: 知识结晶器 (V1 结晶版)
    驱动引擎: Scikit-learn + Jieba
    逻辑: TF-IDF 萃取 -> K-Means 聚合 -> 重心逆向标记
    """

    def __init__(self, n_clusters: int = 8):
        self.n_clusters = n_clusters
        # 🛡️ 噪音屏蔽场 (Stop Words)
        self.stop_words = {
            '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这', '如何', '什么', '怎么', '教程', '指南', '2023', '2024', '2025', 'com', 'cn', 'net', 'org', 'github', '官网', '下载', '使用', '方法', '解决', '推荐', '工具', '平台'
        }

    def _tokenize(self, text: str) -> str:
        """原子级分词：将文本打散为语义粉末"""
        if not text: return ""
        # 使用 lcut 直接获取列表，减少生成器上下文开销
        words = jieba.lcut(text)
        # 过滤长度为1的单字（通常是噪音）和停用词
        return " ".join([w for w in words if len(w) > 1 and w not in self.stop_words])

    def crystallize(self, bookmarks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [熔炼流程]: 执行光谱聚类并析出星群结晶
        """
        if not DEPENDENCIES_INSTALLED:
            print("❌ [Crystallizer] 缺少关键试剂: sklearn 或 jieba。")
            return []

        # 1. 原料筛选
        corpus = []
        valid_items = []
        for b in bookmarks:
            tokenized = self._tokenize(b.get('title', ''))
            if len(tokenized.split()) >= 2: # 至少保留2个语义特征的信号
                corpus.append(tokenized)
                valid_items.append(b)

        # 🛡️ 样本保护：如果样本量太少，聚类会退化为噪音
        min_samples = self.n_clusters * 2
        if len(corpus) < min_samples:
            print(f"⚠️ [Crystallizer] 样本量 ({len(corpus)}) 不足，星群无法析出。")
            return []

        print(f"⚗️ [Crystallizer] 正在高维空间解析 {len(corpus)} 条知识路径...")

        # 2. 向量化 (TF-IDF)
        # token_pattern=r"(?u)\b\w+\b" 确保兼容中英混合
        vectorizer = TfidfVectorizer(max_features=1000, token_pattern=r"(?u)\b\w+\b")
        try:
            X = vectorizer.fit_transform(corpus)
        except Exception as e:
            print(f"❌ [Crystallizer] 向量化失败: {e}")
            return []

        # 3. 空间聚类 (K-Means)
        # 使用 random_state=42 确保每次炼金的稳定性
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init='auto')
        kmeans.fit(X)

        # 4. 逆向析出星群标签
        feature_names = vectorizer.get_feature_names_out()
        cluster_map = defaultdict(list)
        for idx, label in enumerate(kmeans.labels_):
            cluster_map[label].append(valid_items[idx])

        crystals = []
        for i in range(self.n_clusters):
            items = cluster_map[i]
            if not items: continue

            # 通过聚类重心 (Centroid) 逆向获取最重要的 3 个特征词
            centroid = kmeans.cluster_centers_[i]
            top_indices = centroid.argsort()[-3:][::-1]
            keywords = [feature_names[idx] for idx in top_indices]
            
            cluster_name = " + ".join(keywords).upper()

            crystals.append({
                "cluster_id": i,
                "topic": cluster_name,
                "size": len(items),
                "nodes": items[:10], # 只保留前10个样本作为预览信号
                "keywords": keywords
            })

        # 按星群引力（大小）降序排列
        return sorted(crystals, key=lambda x: x['size'], reverse=True)

    def analyze_timeline(self, bookmarks: List[Dict[str, Any]]) -> Dict[str, int]:
        """[Chronos]: 时间热力图析出"""
        counts = defaultdict(int)
        for b in bookmarks:
            ts = b.get('timestamp', '')
            if ts and len(ts) >= 7:
                counts[ts[:7]] += 1 # 统计 YYYY-MM
        return dict(sorted(counts.items()))

    def analyze_domains(self, bookmarks: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """[Territory]: 域名领地分析"""
        from urllib.parse import urlparse
        domain_counts = defaultdict(int)
        
        for b in bookmarks:
            url = b.get('url', '')
            try:
                domain = urlparse(url).netloc
                if domain.startswith('www.'):
                    domain = domain[4:]
                if domain:
                    domain_counts[domain] += 1
            except:
                continue
                
        sorted_domains = sorted(domain_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [{"name": d, "value": c} for d, c in sorted_domains]

    def analyze_activity_hours(self, bookmarks: List[Dict[str, Any]]) -> Dict[str, int]:
        """[Circadian]: 昼夜活跃节律"""
        hours = defaultdict(int)
        for b in bookmarks:
            ts = b.get('timestamp', '') # YYYY-MM-DD HH:MM:SS
            if ts and len(ts) >= 13:
                hour = ts[11:13] # Extract HH
                hours[hour] += 1
        return dict(sorted(hours.items()))

    def analyze_skill_radar(self, bookmarks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """[Skill Tree]: 技能六边形雷达数据"""
        # 定义技能维度与关键词映射
        dimensions = {
            "Coding": ["github", "stackoverflow", "csdn", "juejin", "python", "java", "code", "git", "api", "dev"],
            "AI/ML": ["arxiv", "huggingface", "openai", "gpt", "model", "deep", "learning", "ai", "bot"],
            "Product": ["figma", "dribbble", "producthunt", "notion", "linear", "design", "ui", "ux"],
            "Media": ["bilibili", "youtube", "netflix", "spotify", "music", "video", "douban", "movie"],
            "Academic": ["scholar", "edu", "university", "paper", "research", "science", "wiki", "book"],
            "Life": ["taobao", "jd", "amazon", "map", "food", "travel", "news", "blog"]
        }
        
        scores = defaultdict(int)
        
        for b in bookmarks:
            content = (b.get('title', '') + " " + b.get('url', '')).lower()
            for dim, keywords in dimensions.items():
                for kw in keywords:
                    if kw in content:
                        scores[dim] += 1
                        break # 一个书签在一个维度只算一次
        
        # 归一化处理：找出最大值，将所有值映射到 0-100
        max_score = max(scores.values()) if scores else 1
        
        radar_data = []
        for dim in dimensions.keys():
            raw_score = scores[dim]
            # 简单的线性映射，但也保留原始值
            normalized = int((raw_score / max_score) * 100) if max_score > 0 else 0
            radar_data.append({
                "name": dim,
                "value": raw_score, 
                "max": max_score + 5 # 雷达图的最大刻度略大于实际最大值
            })
            
        return radar_data

    def generate_persona(self, bookmarks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """[Persona]: 用户画像生成器 (V3 核心)"""
        if not bookmarks:
            return {"level": "Lv.0 萌新", "tags": [], "top_domain": "N/A", "top_cluster": "N/A"}

        # 1. 计算等级 (基于收藏量)
        count = len(bookmarks)
        if count < 100: level = "Lv.1 探索者"
        elif count < 500: level = "Lv.2 收藏家"
        elif count < 1000: level = "Lv.3 知识囤积者"
        elif count < 5000: level = "Lv.4 图书馆长"
        else: level = "Lv.5 赛博贤者"

        # 2. 提取标签 (基于域名规则)
        tags = set()
        from urllib.parse import urlparse
        domains = []
        for b in bookmarks:
            try:
                d = urlparse(b.get('url', '')).netloc
                domains.append(d)
            except: pass
        
        domain_str = " ".join(domains).lower()
        
        # 规则引擎
        if "github.com" in domain_str or "stackoverflow.com" in domain_str: tags.add("开源极客")
        if "bilibili.com" in domain_str or "youtube.com" in domain_str: tags.add("视听学习者")
        if "arxiv.org" in domain_str or "scholar.google" in domain_str: tags.add("学术研究")
        if "zhihu.com" in domain_str or "medium.com" in domain_str: tags.add("深度阅读")
        if "taobao.com" in domain_str or "jd.com" in domain_str: tags.add("数字生活")
        if "figma.com" in domain_str or "dribbble.com" in domain_str: tags.add("设计美学")

        # 3. 获取 Top 1 域名 (最爱来源)
        domain_stats = self.analyze_domains(bookmarks, top_n=1)
        top_domain = domain_stats[0]['name'] if domain_stats else "N/A"

        # 4. 获取 Top 1 聚类 (专注领域)
        # 这里需要复用已经生成的结晶数据，为了解耦，我们简单用词频最高的词代替，或者由上层传入
        # 暂时用词频最高的非停用词作为"专注领域"
        cloud = self.analyze_tags_cloud(bookmarks, top_n=1)
        top_cluster = cloud[0]['name'] if cloud else "杂学家"

        return {
            "level": level,
            "tags": list(tags)[:3], # 最多展示3个标签
            "top_domain": top_domain,
            "top_cluster": top_cluster
        }


    def analyze_theme_river(self, bookmarks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """[River]: 兴趣河流图 (ThemeRiver) 数据"""
        # 按月聚合，统计每个月的 Top 3 聚类词频
        # 1. 先按月分组
        monthly_data = defaultdict(list)
        for b in bookmarks:
            ts = b.get('timestamp', '')
            if ts and len(ts) >= 7:
                month = ts[:7] # YYYY-MM
                monthly_data[month].append(b)
        
        # 2. 对每个月的数据提取关键词
        river_data = []
        months = sorted(monthly_data.keys())
        
        # 为了保持河流的连贯性，我们选取全局最高频的 5 个词作为"河道"
        global_cloud = self.analyze_tags_cloud(bookmarks, top_n=5)
        top_themes = [item['name'] for item in global_cloud]
        
        for month in months:
            items = monthly_data[month]
            # 统计该月内这5个主题词的频率
            month_counts = defaultdict(int)
            for b in items:
                text = b.get('title', '')
                for theme in top_themes:
                    if theme in text:
                        month_counts[theme] += 1
            
            for theme in top_themes:
                river_data.append({
                    "date": month,
                    "name": theme,
                    "value": month_counts[theme]
                })
                
        return river_data

    def analyze_tags_cloud(self, bookmarks: List[Dict[str, Any]], top_n: int = 50) -> List[Dict[str, Any]]:
        """[Nebula]: 语义星云（词云数据）"""
        if not DEPENDENCIES_INSTALLED: return []
        
        word_counts = defaultdict(int)
        for b in bookmarks:
            # 结合标题和现有标签
            text = b.get('title', '') + " " + " ".join(b.get('tags', []))
            words = self._tokenize(text).split()
            for w in words:
                word_counts[w] += 1
                
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
        return [{"name": w, "value": c} for w, c in sorted_words]

# --- 验证逻辑 ---
if __name__ == "__main__":
    crystallizer = KnowledgeCrystallizer(n_clusters=3)
    # 注入测试原料...