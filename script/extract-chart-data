let chart_list = ['coronavirus-cases-linear', 'coronavirus-deaths-linear', 'graph-active-cases-total'];
let chart = $('#' + chart_list[0]).highcharts();
let chart_data1 = chart ? {'x_data': chart.xAxis[0].categories, 'y_data': chart.series[0].yData} : {};
chart = $('#' + chart_list[1]).highcharts();
let chart_data2 = chart ? {'x_data': chart.xAxis[0].categories, 'y_data': chart.series[0].yData} : {};

if (chart_data1.x_data.length == chart_data2.x_data.length) {
	let n = chart_data1.x_data.length;
	console.log('date,total_cases,total_deaths')
	for (i=0; i<n; i++) {
		console.log(chart_data1.x_data[i] + '/2020,' + chart_data1.y_data[i] + ',' + chart_data2.y_data[i]);
	}
}
