var request = require("request");
var json2csv = require("json2csv");
var fs = require("fs");
var geolib = require("geolib");

var fields = ['id', 'latitude', 'longitude', 'time', 'type_crime'];

request.get({
    uri: "http://crimeapp-dev.us-west-1.elasticbeanstalk.com/get_reports",
    headers: {
        "Content-Type": "application/json"
    }
}, function(error, response, body) {
    //createCSV(body);
    var mapJSON = JSON.parse(body).reports;
    var center = geolib.getCenter(mapJSON);
    fs.writeFile('center.json', JSON.stringify(center));
    json2csv({data: mapJSON, fields: fields}, function(err, csv) {
        if (err) console.error(err);
        fs.writeFile('crime.csv', csv, function(err) {
            if (err) throw err;
            console.log('file saved');
        });
    });
    //console.log(body);
});



