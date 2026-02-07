import * as echarts from 'echarts';

export function renderActivity(element: HTMLElement, data: Record<string, number>) {
  if (!element) return;
  const chart = echarts.init(element);
  
  // 补全24小时数据
  const hours = Array.from({length: 24}, (_, i) => i.toString().padStart(2, '0'));
  const counts = hours.map(h => data[h] || 0);

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    radar: {
      indicator: hours.map(h => ({ name: h + 'h', max: Math.max(...counts) * 1.2 })),
      splitArea: { areaStyle: { color: ['rgba(30, 41, 59, 0.5)', 'rgba(15, 23, 42, 0.5)'] } },
      axisLine: { lineStyle: { color: '#334155' } },
      splitLine: { lineStyle: { color: '#334155' } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: counts,
        name: '活跃时段',
        itemStyle: { color: '#f472b6' },
        areaStyle: { color: 'rgba(244, 114, 182, 0.2)' }
      }]
    }]
  });
  window.addEventListener('resize', () => chart.resize());
  return chart;
}
