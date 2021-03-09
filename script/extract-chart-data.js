function extractData() {
	let result = 'date,total_cases,total_deaths,new_cases,new_deaths\n';
	let chart_list = ['coronavirus-cases-linear', 'coronavirus-deaths-linear', 'graph-active-cases-total'];
	let chart = $('#' + chart_list[0]).highcharts();
	let chart_data1 = chart ? { 'x_data': chart.xAxis[0].categories, 'y_data': chart.series[0].yData } : {};
	chart = $('#' + chart_list[1]).highcharts();
	let chart_data2 = chart ? { 'x_data': chart.xAxis[0].categories, 'y_data': chart.series[0].yData } : {};

	if (chart_data1.x_data.length == chart_data2.x_data.length) {
		let n = chart_data1.x_data.length;

		for (i = 0; i < n; i++) {
			tokens = chart_data1.x_data[i].split(' ');
			curr_month = ("JanFebMarAprMayJunJulAugSepOctNovDec".indexOf(tokens[0]) / 3 + 1);
			curr_day = tokens[1].replace(',', '');
			curr_date = curr_month + '/' + curr_day + '/2020';
			new_cases = (i > 0 ? chart_data1.y_data[i] - curr_cases : 0);
			new_deaths = (i > 0 ? chart_data2.y_data[i] - curr_deaths : 0);
			curr_cases = chart_data1.y_data[i];
			curr_deaths = chart_data2.y_data[i];

			result += curr_date + ',' + curr_cases + ',' + curr_deaths + ',' + new_cases + ',' + new_deaths + '\n';
		}
	}
	return result;
}

extractData();
