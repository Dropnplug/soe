let listeAlarmes = []
var maxAlarmesPArPage = 5

// requetes pour avoir tous les defauts de tous les ondueleurs
request("GET", "/soe/site/alarmes/").then(data => {
    // création de la page à partir des données de la bdd
    displayAlarmes(data)
    // console.log(data)
})

function displayAlarmes(data) {
    // créer une liste d'alarmes jolies
    let table = document.getElementById("listeAlarmes")
    let pagesAlarmes = document.getElementById("pagesAlarmes")
    let toutVaBien = document.getElementById("toutVaBien")
    if (data.length == 0) {
        pagesAlarmes.style.display = "none"
        toutVaBien.style.display = ""
    } else {
        pagesAlarmes.style.display = ""
        toutVaBien.style.display = "none"
    }
    let date = undefined
    let i = 0
    for (let onduleur in data) {
        for (let alarme in data[onduleur]["defaut"]) {
            let ligne = document.createElement("tr")
            if (i >= maxAlarmesPArPage) {
                ligne.style.display = "none"
            }
            let celuleNom = document.createElement("td")
            let celuleTemps = document.createElement("td")
            let celuleNomOndul = document.createElement("td")
            celuleNomOndul.innerText = data[onduleur]["nom"] + " (" + data[onduleur]["slave_id"] + ")"
            celuleNom.innerText = alarme
            date = new Date(data[onduleur]["defaut"][alarme]["temps"])
            let chaine = toIsoString(date).split("+")[0].replace("T", " ")
            chaine = chaine.substring(0,10).split("-").reverse().join("-") + chaine.substring(10, 19)
            celuleTemps.innerText = chaine
            ligne.appendChild(celuleNomOndul)
            ligne.appendChild(celuleNom)
            ligne.appendChild(celuleTemps)
            table.appendChild(ligne)
            i = i + 1
        }
    }

    setMaxPage(i)
}

function setMaxPage(nbElem) {
    let numMaxPages = document.getElementById("numPageTotale")
    let plus = 0
    if (nbElem%maxAlarmesPArPage == 0) {
        plus = 1
    }
    numMaxPages.innerText = Math.floor(nbElem/maxAlarmesPArPage)-plus
}

function updateMaxAlarmeParPage(elem) {
    maxAlarmesPArPage = Number(elem.value)
    if (maxAlarmesPArPage <= 0 || isNaN(maxAlarmesPArPage) || maxAlarmesPArPage%1 != 0) {
        maxAlarmesPArPage = 1
    }

    elem.value = maxAlarmesPArPage
    
    actualiserVisibiliteLignes()
    let table = document.getElementById("listeAlarmes")
    let rows = table.rows;
    setMaxPage(rows.length-1)
    adjustWidth(elem)
}

// itérer dans l'element tableau pour enlever le display none en fonction du numéro de page
function actualiserVisibiliteLignes(page=0) {
    let table = document.getElementById("listeAlarmes")
    let numPageActu = document.getElementById("numPageActuelle")
    let numPage = Number(numPageActu.innerText)
    let rows = table.rows;

    numPage = numPage + page
    if (page > 0) {
        if (numPage * maxAlarmesPArPage >= rows.length-1) {
            return
        }
    } else {
        if (numPage < 0) {
            return
        }
    }
    numPageActu.innerText = numPage

    let i = 0
    for (let row in rows) {
        // on ignore les élements qui ne sont pas des vrais table row
        if (typeof rows[row] == "function" || typeof rows[row] == "number") {
            continue
        }
        if (rows[row].children["0"].tagName == "TH") {
            continue
        }

        if (i < numPage * maxAlarmesPArPage) {
            rows[row].style.display = "none"
        } else if (i >= numPage * maxAlarmesPArPage + maxAlarmesPArPage) {
            rows[row].style.display = "none"
        } else {
            rows[row].style.display = ""
        }
        i = i + 1
    }
}

function adjustWidth(elem) {
    let nbAugment = elem.value.length
    if (nbAugment == 0) {
        nbAugment = 1
    }
    elem.style.width = (nbAugment + 4) + "ch";
}