import * as echarts from 'echarts';

export function renderSkillRadar(element: HTMLElement, data: Array<{name: string, value: number, max: number}>) {
  if (!element) return;
  const chart = echarts.init(element);
  
  chart.setOption({
      backgroundColor: 'transparent',
      tooltip: {},
      radar: {
          indicator: data.map(item => ({ name: item.name, max: item.max })),
          splitArea: {
              areaStyle: {
                  color: ['rgba(30, 41, 59, 0.5)', 'rgba(15, 23, 42, 0.5)']
              }
          },
          axisLine: { lineStyle: { color: '#334155' } },
          splitLine: { lineStyle: { color: '#334155' } }
      },
      series: [{
          name: '技能能力',
          type: 'radar',
          data: [
              {
                  value: data.map(item => item.value),
                  name: '技能能力',
                  itemStyle: { color: '#c084fc' },
                  areaStyle: { color: 'rgba(192, 132, 252, 0.2)' }
              }
          ]
      }]
  });
  window.addEventListener('resize', () => chart.resize());
  return chart;
}
