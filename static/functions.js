document.title = "Price Tracker App";

var procedureExecuted = false; 
var previousPrice = null; 
var intervalTimer; 

function executeProcedure() {
    var urlInput = document.getElementById('urlInput').value;
    document.getElementById('loading').style.display = 'block';
    document.getElementById('confirmation').textContent = '';
    fetch('/extract', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'url=' + encodeURIComponent(urlInput)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').style.display = 'none';
        displayDataInTable(data.data);
        checkPriceChange(data.data);
        if (!procedureExecuted) {
            intervalTimer = setInterval(executeProcedure, 180000);
            procedureExecuted = true; 
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
    });
}

function displayDataInTable(data) {
    var table = document.getElementById('dataTable');
    var parsedData = data.split('***');
    var productName = parsedData[0].trim();
    var productPrice = parsedData[1].trim();
    var currency = parsedData[2].trim();
    var dateTime = new Date().toLocaleString();

    var row = table.insertRow(1);
    var cell1 = row.insertCell(0);
    var cell2 = row.insertCell(1);
    var cell3 = row.insertCell(2);
    var cell4 = row.insertCell(3); 
    cell1.innerHTML = productName;
    cell2.innerHTML = productPrice;
    cell3.innerHTML = currency;
    cell4.innerHTML = dateTime; 

    
    table.style.display = 'block';
}


function checkPriceChange(data) {
    var parsedData = data.split('***');
    var productPrice = parseFloat(parsedData[1].trim());
    if (previousPrice !== null && productPrice !== previousPrice) {
        alert("Price has changed!"); 
    }
    previousPrice = productPrice; 
}

document.getElementById('submitBtn').addEventListener('click', function() {
    executeProcedure(); 
});
