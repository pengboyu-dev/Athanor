import numpy as np
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

# --- 验证逻辑 ---
if __name__ == "__main__":
    crystallizer = KnowledgeCrystallizer(n_clusters=3)
    # 注入测试原料...