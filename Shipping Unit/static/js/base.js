$.ajax({
	url:'127.0.0.1:8000/units/count/',
	type: 'get',
	success: function(data) {
		$('#unit_count').val(data);
	},
	failure: function(data) {
		alert('Failure');
	}
});