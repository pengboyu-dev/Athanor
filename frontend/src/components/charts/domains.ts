import * as echarts from 'echarts';

export function renderDomains(element: HTMLElement, data: Array<{name: string, value: number}>) {
  if (!element) return;
  const chart = echarts.init(element);

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item' },
    series: [{
      name: 'Top Domains',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '50%'],
      itemStyle: {
        borderRadius: 5,
        borderColor: '#1e293b',
        borderWidth: 2
      },
      label: { show: true, color: '#e2e8f0' },
      data: data.map(item => ({
          name: item.name, 
          value: item.value,
      }))
    }]
  });
  window.addEventListener('resize', () => chart.resize());
  return chart;
}
