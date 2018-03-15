
/* global home, keller, chipotle, northrop, placename, addressline1, addressline2, opentime, closetime, additionalinformation */

function name(elmt) {
    if (elmt === home) {
        document.getElementById('myImg').src = 'century.png';
    }
    else if (elmt === keller) {
        document.getElementById('myImg').src = 'keller.png';
    }
     else if (elmt === chipotle) {
        document.getElementById('myImg').src = 'chipotle.png';
    }
     else if (elmt === northrop) {
        document.getElementById('myImg').src = 'northrop.png';
    }
    else {
        document.getElementById('myImg').src = 'gophers-mascot.png';
    }
}



function validate() {
    var p = document.getElementById('pname').value;
    var adl1 = document.getElementById('ad1').value;
    var adl2 = document.getElementById('ad2').value;
    var ap = /^[0-9a-zA-Z]+$/;
    
    if ((p.search(ap) !== 0) || (adl1.search(ap) !== 0) || (adl2.search(ap) !== 0)) {
        alert("Place Name and address must be alphanumeric");
        return false;
    }
    else {
        return true;
    }


}
