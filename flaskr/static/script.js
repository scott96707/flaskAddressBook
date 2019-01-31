const apiKey = "829SGCOM5266";

document.getElementById("zipBtn").addEventListener("click", function() {
        
    let address = document.getElementById("entryaddress").value;
    let city = document.getElementById("entrycity").value;
    let e = document.getElementById("entrystate");
    let state = e.options[e.selectedIndex].value;

    let theUrl = `http://production.shippingapis.com/ShippingAPI.dll?API=ZipCodeLookup&XML=` +
    `<ZipCodeLookupRequest%20USERID=${apiKey}><Address><Address1></Address1>` +
    `<Address2>${address}</Address2>` +
    `<City>${city}</City><State>${state}</State>` +
    `</Address></ZipCodeLookupRequest>`;

        let xhr = new XMLHttpRequest();
        xhr.open("GET", theUrl, true);
        xhr.send();

        xhr.addEventListener("readystatechange", processRequest, false);
        
        function processRequest(e) {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let response = xhr.responseText;
                parser = new DOMParser();
                xmlDoc = parser.parseFromString(response, "text/xml");
                
                try {
                    let zip5 = xmlDoc.getElementsByTagName("Zip5")[0].childNodes[0].nodeValue;
                    let zip4 = xmlDoc.getElementsByTagName("Zip4")[0].childNodes[0].nodeValue;
                    document.getElementById("entryzip").value = `${zip5} - ${zip4}`;
                } catch (err) {
                    alert('Check your address/city/state');
                }
            }
        }
});

document.getElementById("fixBtn").addEventListener("click", function() {
    
    let zipCode = document.getElementById("entryzip").value;

    let theUrl = `http://production.shippingapis.com/ShippingAPITest.dll?API=` +
    `CityStateLookup&XML=<CityStateLookupRequest USERID=${apiKey}>` +
    `<ZipCode ID="0"><Zip5>${zipCode}</Zip5></ZipCode></CityStateLookupRequest>`;

        let xhr = new XMLHttpRequest();
        xhr.open("GET", theUrl, true);
        xhr.send();

        xhr.addEventListener("readystatechange", processRequest, false);
        
        function processRequest(e) {
            if (xhr.readyState == 4 && xhr.status == 200) {
                let response = xhr.responseText;
                parser = new DOMParser();
                xmlDoc = parser.parseFromString(response, "text/xml");
                
                try {
                    let city = xmlDoc.getElementsByTagName("City")[0].childNodes[0].nodeValue;
                    let state = xmlDoc.getElementsByTagName("State")[0].childNodes[0].nodeValue;
                    document.getElementById("entrycity").value = city;
                    document.getElementById("entrystate").value = state;
                } catch (err) {
                    alert('Invalid zip code');
                }
            }
        }
});