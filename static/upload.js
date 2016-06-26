var addContact = function(phone, cb) {
	$.ajax({
		'url' : '/addcontact',
		'data' : {
			'user_ref' : 3,
			'phone' : phone,
		},
		success : function(data) {
			cb(data)
		}
	})
};
