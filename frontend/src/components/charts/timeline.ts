import * as echarts from 'echarts';

export function renderTimeline(element: HTMLElement, data: Record<string, number>) {
  if (!element) return;
  const chart = echarts.init(element);
  const dates = Object.keys(data);
  const counts = Object.values(data);

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { top: '10%', left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#94a3b8' } },
      axisLabel: { color: '#94a3b8', rotate: 45 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: '#334155', type: 'dashed' } },
      axisLabel: { color: '#94a3b8' }
    },
    series: [{
      name: '收藏量',
      type: 'bar',
      data: counts,
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#818cf8' },
          { offset: 1, color: '#6366f1' }
        ]),
        borderRadius: [4, 4, 0, 0]
      }
    }]
  });
  window.addEventListener('resize', () => chart.resize());
  return chart;
}
