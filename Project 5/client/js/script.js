"use strict";

(function() {
    // the API end point
    var url = "getListOfFavPlaces";
    var data;
    // TO DO: YOU NEED TO USE AJAX TO CALL getListOfFavPlaces end-point from server
    // STEPS:
    // 1. Hit the getListOfFavPlaces end-point of server using AJAX get method
    // 2. Upon successful completion of API call, server will return the list of places
    // 2. Use the response returned to dynamically add rows to 'myFavTable' present in favourites.html page
    // 3. You can make use of jQuery or JavaScript to achieve this
    // Note: No changes will be needed in favourites.html page
    $.ajax({
        url: url,
        data: data,
        success: function(data) {
                populate(data);
            }
            // dataType: dataType
    });
    /*var data;
    var tbl = $('#myFavTable');
    $.getJSON(url, data, function(data) {
        console.log(data);
    })*/
    function populate(data) {
        var places = data.res.placeList;
        var tbl = document.getElementById('myFavTable');
        for (var i = 0; i < places.length; i++) {
            var row = document.createElement("tr");
            row.setAttribute("style", "border-top: solid 1px grey;");
            for (var key in places[i]) {
                if (key === 'addressline2') {
                    var cellText = document.createTextNode(' ' + places[i][key]);
                    cell.appendChild(cellText);
                    console.log(key.val)
                } else if (key === 'closetime') {
                    var br = document.createElement('br');
                    cell.appendChild(br);
                    var cellText = document.createTextNode(places[i][key]);
                    cell.appendChild(cellText);
                } else {
                    var cell = document.createElement("td");
                    var cellText = document.createTextNode(places[i][key]);
                    cell.appendChild(cellText);
                    row.appendChild(cell);
                }

            }
            tbl.appendChild(row);
        }
    }
})();