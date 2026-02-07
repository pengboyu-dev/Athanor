import os
import sys
from datetime import datetime
from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional, Any

class AthanorPurifier:
    """
    [炼金组件]: 物质净化器 (V3 终极版)
    驱动引擎: lxml (High-Performance Parser)
    使命: 零重排、零噪音、全自动编码感应，实现书签信号的绝对萃取。
    """

    def __init__(self):
        # 排除无意义的根节点 (Noise Reduction)
        self.noise_roots = {
            'Bookmarks', '书签', '书签栏', '收藏夹', 'Bookmarks Bar', 
            'Bookmarks Menu', 'Personal Toolbar Folder', 'Other Bookmarks',
            'Mobile Bookmarks', '移动书签', 'Unfiled Bookmarks', '未分类书签'
        }

    def _normalize_timestamp(self, ts_str: Optional[str]) -> str:
        """
        时间戳定标 (Temporal Calibration)
        阈值定位于 10^12，完美兼容 Webkit (微秒) 与 Unix (秒)。
        """
        if not ts_str:
            return ""
        try:
            ts = int(ts_str)
            # 修正逻辑：Webkit 时间戳通常为 17 位，Unix 为 10 位
            if ts > 10**12:
                ts = ts / 1_000_000
            return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        except (ValueError, TypeError, OverflowError):
            return ""

    def _extract_context(self, link: Tag) -> List[str]:
        """逆流而上：从 A 标签攀爬 DOM 树，提取知识语境"""
        context: List[str] = []
        if not isinstance(link, Tag):
            return context

        for parent in link.parents:
            if parent.name == 'dl':
                # 寻找 DL 容器之前的文件夹标题 (H3 为标准 Netscape 格式标题)
                header = parent.find_previous_sibling(['h3', 'h1'])
                if isinstance(header, Tag):
                    name = header.get_text().strip()
                    if name and name not in self.noise_roots:
                        context.insert(0, name)
        return context

    def smelt(self, raw_content: bytes) -> List[Dict[str, Any]]:
        """
        核心熔炼逻辑：高性能字节流处理。
        """
        # ⚡ 引擎切换：使用 'html.parser' 替代 'lxml'
        # 书签文件 (Netscape 格式) 往往嵌套极深且不规范，lxml 过于严格会导致数据截断。
        # html.parser 虽然慢一点，但容错性极强，能保证数据的完整性 (High Recall)。
        soup = BeautifulSoup(raw_content, 'html.parser', from_encoding=None)
        
        actual_encoding = soup.original_encoding
        if actual_encoding:
            print(f"📡  [Spectral Analysis] 探测到物质编码: {actual_encoding}")
            
        purified_data: List[Dict[str, Any]] = []
        raw_links = soup.find_all('a')
        
        for link in raw_links:
            if not isinstance(link, Tag):
                continue

            url = link.get('href', '')
            # 过滤干扰协议与空物质
            if not isinstance(url, str) or not url or url.startswith(('javascript:', 'place:', 'data:')):
                continue

            title = link.get_text().strip() or "Untitled Signal"
            
            # 萃取核心信号切片
            signal = {
                "title": title,
                "url": url,
                "context": self._extract_context(link),
                "timestamp": self._normalize_timestamp(str(link.get('add_date', ''))),
                "tags": []
            }
            
            # 提取浏览器原生标签 (如果存在)
            # 兼容 TAGS (大写) 和 tags (小写)
            raw_tags = link.get('tags') or link.get('TAGS')
            if isinstance(raw_tags, str):
                signal["tags"] = [t.strip() for t in raw_tags.split(',')]

            purified_data.append(signal)

        return purified_data

    def process_file(self, input_path: str) -> List[Dict[str, Any]]:
        """
        [真理入口]: 验证载体并执行二进制熔炼。
        """
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"❌ [Error] 载体缺失: {input_path}")

        print(f"⚗️  [Athanor] 正在开启熔炉，加载原料: {os.path.basename(input_path)}")
        
        try:
            with open(input_path, 'rb') as f:
                raw_content = f.read()
            return self.smelt(raw_content)
        except IOError as e:
            print(f"❌ [Error] 物质读入失败: {e}")
            return []

# --- 验证逻辑 ---
def main():
    # 环境感知路径：支持环境变量注入，否则降级至默认测试路径
    target_path = os.getenv("ATHANOR_INPUT", "data/bookmarks_raw.html")
    
    purifier = AthanorPurifier()
    
    try:
        results = purifier.process_file(target_path)
        print(f"✨  [Success] 萃取完成，获得 {len(results)} 条高纯度信号。")
        
        # 检视前 5 条萃取出的信号
        for s in results[:5]:
            path_str = " > ".join(s['context']) if s['context'] else "ROOT"
            print(f"[{s['timestamp']}] {path_str} | {s['title']} -> {s['url'][:50]}...")
            
    except Exception as e:
        print(f"❌ [Critical] 熔炼事故: {e}")

if __name__ == "__main__":
    main()