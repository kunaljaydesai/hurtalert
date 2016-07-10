function getContacts(cb) {
	$.ajax({
		'url' : '/api/user/get_contacts',
		success : function(data) {
			cb(data);
		}
	});
}