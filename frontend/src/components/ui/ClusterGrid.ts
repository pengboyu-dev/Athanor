function renderListItems(container: HTMLUListElement, nodes: any[]) {
    nodes.forEach((node: any) => {
      const li = document.createElement('li');
      
      // 渲染标签
      const tagsHtml = node.tags && node.tags.length > 0 
        ? `<div class="bookmark-tags">${node.tags.map((t: string) => `<span class="tag">${t}</span>`).join('')}</div>`
        : '';

      li.innerHTML = `
        <a href="${node.url}" target="_blank" rel="noopener noreferrer" title="${node.title}" class="bookmark-link">
          <span class="link-text">${node.title}</span>
        </a>
        ${tagsHtml}
      `;
      container.appendChild(li);
    });
}

export function renderClustersGrid(container: HTMLElement, clusters: any[]) {
    if (!container) return;
    container.innerHTML = '';

    clusters.forEach((cluster, index) => {
      const card = document.createElement('div');
      card.className = 'cluster-card';
      card.id = `cluster-${index}`;
      
      const header = document.createElement('div');
      header.className = 'cluster-header';
      header.innerHTML = `<h3>${cluster.topic}</h3><span class="badge">${cluster.size}</span>`;
      
      const keywords = document.createElement('div');
      keywords.className = 'cluster-keywords';
      keywords.innerHTML = cluster.keywords.map((k: string) => `<span class="keyword">#${k}</span>`).join('');

      const list = document.createElement('ul');
      list.className = 'cluster-list';
      
      // 默认显示前5个
      const initialNodes = cluster.nodes.slice(0, 5);
      renderListItems(list, initialNodes);

      card.appendChild(header);
      card.appendChild(keywords);
      card.appendChild(list);

      // 如果有更多链接，添加展开按钮
      if (cluster.nodes.length > 5) {
        const expandBtn = document.createElement('button');
        expandBtn.className = 'expand-btn';
        expandBtn.textContent = `查看全部 (${cluster.nodes.length})`;
        expandBtn.onclick = () => {
          list.innerHTML = ''; // 清空列表
          if (expandBtn.classList.contains('expanded')) {
            // 收起
            renderListItems(list, initialNodes);
            expandBtn.textContent = `查看全部 (${cluster.nodes.length})`;
            expandBtn.classList.remove('expanded');
          } else {
            // 展开
            renderListItems(list, cluster.nodes);
            expandBtn.textContent = '收起';
            expandBtn.classList.add('expanded');
          }
        };
        card.appendChild(expandBtn);
      }

      container.appendChild(card);
    });
}
