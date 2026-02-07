import * as echarts from 'echarts';

export function renderRiver(element: HTMLElement, data: Array<{date: string, name: string, value: number}>) {
  if (!element) return;
  const chart = echarts.init(element);
  
  // 数据预处理：转换成 ThemeRiver 需要的 [date, value, name] 格式
  const riverData = data.map(item => [item.date, item.value, item.name]);

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: 'rgba(0,0,0,0.2)', width: 1, type: 'solid' } } },
    singleAxis: {
      top: 50, bottom: 50,
      type: 'time',
      axisLine: { lineStyle: { color: '#94a3b8' } },
      axisLabel: { color: '#94a3b8' },
      splitLine: { show: true, lineStyle: { type: 'dashed', opacity: 0.2 } }
    },
    series: [{
      type: 'themeRiver',
      emphasis: { itemStyle: { shadowBlur: 20, shadowColor: 'rgba(0, 0, 0, 0.8)' } },
      data: riverData,
      label: { show: false }
    }]
  });
  window.addEventListener('resize', () => chart.resize());
  return chart;
}
