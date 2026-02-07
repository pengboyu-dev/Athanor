import * as echarts from 'echarts';
import 'echarts-wordcloud';

export function renderCloud(element: HTMLElement, data: Array<{name: string, value: number}>) {
  if (!element) return;
  const chart = echarts.init(element);

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {},
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '100%',
      height: '100%',
      right: null,
      bottom: null,
      sizeRange: [12, 60],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return 'rgb(' + [
            Math.round(Math.random() * 160 + 50),
            Math.round(Math.random() * 160 + 50),
            Math.round(Math.random() * 160 + 50)
          ].join(',') + ')';
        }
      },
      emphasis: {
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: data
    }]
  });
  window.addEventListener('resize', () => chart.resize());
  return chart;
}
