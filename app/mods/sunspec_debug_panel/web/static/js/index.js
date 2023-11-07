// crer une liste de lien vers /onduleur avec comme parametre le port, l'ip et le slave id
function createList(){
    hideLoader()
    onduleurs = JSON.parse(this.response)
    let listeOnduleurs = document.getElementsByClassName('listeOnduleurs')[0]
    listeOnduleurs.innerHTML = ""
    for (let ip in onduleurs){
        let lien = document.createElement("a")
        let p = document.createElement("p")
        lien.setAttribute("href", "/sunspec_debug_panel/onduleur?ip=" + ip + "&port=" + onduleurs[ip]["port"] + "&slave_id=" + onduleurs[ip]["slave_id"])
        lien.innerText = ip
        p.appendChild(lien)
        listeOnduleurs.appendChild(p)
    }
}

function requestOnduleur(poubelle, refresh=false){
    if (refresh){
        displayLoader()
    }
    let req = new XMLHttpRequest();
    req.addEventListener("load", createList);
    req.addEventListener("error", errorOnRequest);
    req.open("POST", "/sunspec_debug_panel/getOnduleurs");
    let data = JSON.stringify({"refresh": refresh})
    req.send(data);
}

function errorOnRequest(){
    hideLoader()
}

function formSubmit(event) {
    event.preventDefault();
    let formData = new FormData(event.target);
    let values = Object.fromEntries(formData);
    window.location.href="/sunspec_debug_panel/onduleur?ip=" + values["ip"] + "&port=" + values["port"] + "&slave_id=" + values["slave_id"];
}

function checkForm(){
    let form = document.getElementsByClassName("formOnduleur")[0]
    formData = new FormData(form)
    valide = true
    for (let elem of formData.entries()){
        if (elem[1].length == 0){
            valide = false
        }
    }
    if (valide){
        document.getElementById("submit").disabled = false
    } else {
        document.getElementById("submit").disabled = true
    }
}

addEventListener("DOMContentLoaded", requestOnduleur)