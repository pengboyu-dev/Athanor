export function renderPersonaCard(container: HTMLElement, data: any) {
  if (!container) return;
  container.innerHTML = `
    <div class="persona-card">
      <div class="avatar-section">
        <div class="avatar-circle">${data.level.substring(0, 1)}</div>
        <div class="level-info">
          <div class="level-title">${data.level}</div>
          <div class="level-subtitle">Athanor ID: ${Math.random().toString(36).substr(2, 9).toUpperCase()}</div>
        </div>
      </div>
      <div class="stats-section">
        <div class="stat-item">
          <span class="label">最爱来源</span>
          <span class="value">${data.top_domain}</span>
        </div>
        <div class="stat-item">
          <span class="label">专注领域</span>
          <span class="value">${data.top_cluster}</span>
        </div>
      </div>
      <div class="tags-section">
        ${data.tags.map((tag: string) => `<span class="persona-tag">${tag}</span>`).join('')}
      </div>
    </div>
  `;
}
