let listeAlarmes = []

// requetes pour avoir tous les defauts de tous les ondueleurs
request("GET", "/soe/site/alarmes/").then(data => {
    // création de la page à partir des données de la bdd
    displayAlarmes(data)
})

function displayAlarmes(data) {
    // créer une liste d'alarmes jolies
    let table = document.getElementById("listeAlarmes")
    let toutVaBien = document.getElementById("toutVaBien")
    if (data.length == 0) {
        table.style.display = "none"
        toutVaBien.style.display = "table"
    } else {
        table.style.display = "table"
        toutVaBien.style.display = "none"
    }
    for (let onduleur in data) {
        for (let alarme in data[onduleur]["defaut"]) {
            let ligne = document.createElement("tr")
            let celuleNom = document.createElement("td")
            let celuleTemps = document.createElement("td")
            let celuleNomOndul = document.createElement("td")
            celuleNomOndul.innerText = data[onduleur]["nom"]
            celuleNom.innerText = alarme
            celuleTemps.innerText = data[onduleur]["defaut"][alarme]["temps"]
            ligne.appendChild(celuleNomOndul)
            ligne.appendChild(celuleNom)
            ligne.appendChild(celuleTemps)
            table.appendChild(ligne)
        }
    }
}
