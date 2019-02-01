const getZip = () => {
    
    const zipCode = document.getElementById("entryzip").value;
    
    fetch('/zipcheck', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ zip: zipCode })
    })
    .then(res =>{ return res.json() })
    .then(myJson => { 
        document.getElementById("entrycity").value = myJson.city
        document.getElementById("entrystate").value = myJson.state;
    })
    .catch(err => alert("Make sure your zip code is corrrect"))
};

const getAddress = () => {
    
    const address = document.getElementById("entryaddress").value;
    const city = document.getElementById("entrycity").value;
    const e = document.getElementById("entrystate");
    const state = e.options[e.selectedIndex].value;

    fetch('/addresscheck', {
        method: 'post',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            city: city, state: state, address: address
        })
    })
    .then(res =>{ return res.json() })
    .then(ret => { 
        document.getElementById("entryzip").value = ret.output
    })
    .catch(err => alert("Make sure your Address, City, and State are correct"))
};

document.getElementById("fixBtn").addEventListener("click", getZip)
document.getElementById("zipBtn").addEventListener("click", getAddress)