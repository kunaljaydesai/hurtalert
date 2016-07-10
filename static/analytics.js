function getCrimeByHour(div) {
	$.ajax({
		'url' : '/api/data/crime_by_hour',
		success : function(data) {
			var hourDictionary = data['hour']
			var x = [];
			for(var i = 0; i < 24; i++) {
				x.push(hourDictionary[i]);
			}
			var data = [
			  {
			  	y: x,
			    x: ["12:00 AM", "1:00AM","2:00AM", "3:00AM", "4:00AM", "5:00AM", "6:00AM", "7:00AM", "8:00AM", "9:00AM", "10:00AM", "11:00AM", "12:00PM", "1:00PM", "2:00PM", "3:00PM", "4:00PM", "5:00PM", "6:00PM", "7:00PM", "8:00PM", "9:00PM", "10:00PM", "11:00PM"],
			    type: 'bar',
			  }
			];
			Plotly.newPlot(div, data);
		},
	});
}

function getCrimeByDay(div) {
	$.ajax({
		'url' : '/api/data/crime_by_dow',
		success : function(data) {
			var dowDictionary = data['dow'];
			var x = [];
			for (var i = 0; i < 7; i++) {
				x.push(dowDictionary[i]);
			}
			var data = [
				{
					y: x,
					x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
					type: 'bar',
				}
			];
			Plotly.newPlot(div, data);
		}
	})
}

function getCrimeByMonth(div) {
	$.ajax({
		'url' : 'api/data/crime_by_month',
		success : function(data) {
			var monthDictionary = data['month'];
			var x = [];
			for (var i = 0; i < 12; i++) {
				x.push(monthDictionary[i]);
			}
			var data = [
				{
					y: x,
					x: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
					type: 'bar',
				}
			];
			Plotly.newPlot(div, data);
		}
	});
}

