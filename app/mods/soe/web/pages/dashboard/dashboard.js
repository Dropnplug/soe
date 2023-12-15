const listeCouleur = ["chartreuse", "DarkGreen", "blue", "green", "lime", "DarkCyan"]
const anneMinHisto = 2022
const listeMois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

request("GET", "/soe/dashboard/data/").then(data => {
    // création de la page à partir des données de la bdd
    creerAffichageACDC(data)
})

function getMonthFromString(nom){
    return new Date(Date.parse(nom +" 1, 2012")).getMonth()+1
}

function toIsoString(date) {
    var tzo = -date.getTimezoneOffset(),
        dif = tzo >= 0 ? '+' : '-',
        pad = function(num) {
            return (num < 10 ? '0' : '') + num;
        };
    return date.getFullYear() +
        '-' + pad(date.getMonth() + 1) +
        '-' + pad(date.getDate()) +
        'T' + pad(date.getHours()) +
        ':' + pad(date.getMinutes()) +
        ':' + pad(date.getSeconds()) +
        dif + pad(Math.floor(Math.abs(tzo) / 60)) +
        ':' + pad(Math.abs(tzo) % 60);
}

// construction du graph de l'historique
function requestHistoAC() {
    // recup value des inputs
    let inputHistoMois = document.getElementById("inputHistoMois")
    let inputHistoAnnee = document.getElementById("inputHistoAnnee")
    
    let end
    let start
    let now = new Date()
    // le 30 dernier jour
    if (listeMois[now.getMonth()] == inputHistoMois.value && inputHistoAnnee.value == now.getFullYear() ) {
        end = new Date()
        start = new Date(now.setMonth(now.getMonth()-1))
    // le mois selectioné
    } else {
        let mois = listeMois.indexOf(inputHistoMois.value)+1
        let annee = Number(inputHistoAnnee.value)
        start = new Date(annee, mois-1)
        end = new Date(annee, mois-1, new Date(annee, mois, 0).getDate())
    }

    start.setDate(start.getDate() - 1)

    start = toIsoString(start).substring(0, 10)
    end = toIsoString(end).substring(0, 10)

    request("POST", "/soe/dashboard/dataHisto/", {"start":start, "end":end}).then(data => {
        creerAffichageHistoriqueAC(data, start, end)
    })
}

function creerAffichageHistoriqueAC(data, start, end){
    let sommePuissanceParJour = {}
    start = new Date(start)
    end = new Date(end)
    start.setHours(0)
    end.setHours(0)

    // on set tous les jours à afficher à 0
    for (let d = start; d <= end; d.setDate(d.getDate() + 1)) {
        let date = new Date(d)
        let jour = "0" + date.getDate()
        jour = jour.substring(jour.length - 2)
        let mois = "0" + Number(date.getMonth() + 1)
        mois = mois.substring(mois.length - 2)
        sommePuissanceParJour[jour + "/" + mois] = 0
    }
    
    // on range les données par onduleur
    let onduleursData = {}
    for (donnee in data) {
        if (onduleursData[data[donnee]["mac_onduleur"]+"_"+data[donnee]["slave_id"]] === undefined) {
            onduleursData[data[donnee]["mac_onduleur"]+"_"+data[donnee]["slave_id"]] = []
        }
        onduleursData[data[donnee]["mac_onduleur"]+"_"+data[donnee]["slave_id"]].push(data[donnee])
    }
    
    // on trouve l'énergie par jour et par onduleur : energieDuJour = energieJour - energieJour-1
    puissanceParJourPArOnduleur = {}
    for (let macOnduleur in onduleursData) {
        puissanceParJourPArOnduleur[macOnduleur] = {}
        Object.assign(puissanceParJourPArOnduleur[macOnduleur], sommePuissanceParJour)

        for (let donnee in onduleursData[macOnduleur]) {
            let date = new Date(onduleursData[macOnduleur][donnee]["time"])
            let jour = "0" + date.getDate()
            jour = jour.substring(jour.length - 2)
            let mois = "0" + Number(date.getMonth() + 1)
            mois = mois.substring(mois.length - 2)

            if (puissanceParJourPArOnduleur[macOnduleur][jour + "/" + mois] < onduleursData[macOnduleur][donnee]["energie_totale"]) {
                puissanceParJourPArOnduleur[macOnduleur][jour + "/" + mois] = onduleursData[macOnduleur][donnee]["energie_totale"]
            }
        }
    }

    for (let macOnduleur in puissanceParJourPArOnduleur) {
        for (let jour in puissanceParJourPArOnduleur[macOnduleur]) {
            sommePuissanceParJour[jour] += puissanceParJourPArOnduleur[macOnduleur][jour]
        }
    }

    let jourAvant = undefined
    for (jour in sommePuissanceParJour) {
        if (jourAvant === undefined) {
            jourAvant = jour
            continue
        }
        if (sommePuissanceParJour[jour] != 0) {
            sommePuissanceParJour[jour] = sommePuissanceParJour[jour] - sommePuissanceParJour[jourAvant]
        }
        jourAvant = jour
    }

    // remplissage des liste qui vont dans le graph
    dataPuissanceMois = []
    labelPuissanceMois = []
    for(jour in sommePuissanceParJour) {
        dataPuissanceMois.push(Number(sommePuissanceParJour[jour].toFixed(2)))
        labelPuissanceMois.push(jour)
    }
    // on retire le premier jour pck il vient du mois d'avant
    dataPuissanceMois.shift()
    labelPuissanceMois.shift()


    // on vérifie que yai pas déjà un chart et si y en a un on update et on se casse
    let chart = Chart.getChart("canvasHistoriqueEnergie")
    if (chart) {
        chart.data.labels = labelPuissanceMois
        chart.data.datasets[0].data = dataPuissanceMois
        chart.data.datasets[0].labels = dataPuissanceMois
        chart.update()
        return
    }

    let canvasHisto = document.getElementById("canvasHistoriqueEnergie");
    new Chart(canvasHisto, {
        type: 'bar',
        data: {
            labels: labelPuissanceMois,
            datasets: [{
                label: 'Energie produite ce jour',
                data: dataPuissanceMois,
                backgroundColor: "#17b69d",
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    ticks: {
                        callback: function(value, index, ticks) {
                            return value + ' kWh';
                        }
                    },
                    title: {
                        color: 'black',
                        display: true,
                        text: 'Puissance'
                    }
                },
                x: {
                    title: {
                        color: 'black',
                        display: true,
                        text: 'Jour'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    callbacks: {
                        label: function(ctx) {
                            let dataset = ctx.dataset;
                            return [dataset.label + " : " + dataset.data[ctx.dataIndex] + " kWh"];
                        }
                    }
                }
            }
        }
    })
}

function creerTableauEtat(dataOnduleurs, lastDataFromBdd) {
    let liste = document.getElementById("listeEtatOnduleurs")
    for (let donnee in dataOnduleurs) {
        let listeEtat = ["Déconnecté"]
        if (dataOnduleurs[donnee]["mac"] + "_" + dataOnduleurs[donnee]["slave_id"] in lastDataFromBdd) {
            listeEtat = lastDataFromBdd[dataOnduleurs[donnee]["mac"] + "_" + dataOnduleurs[donnee]["slave_id"]]["etat"]
        }

        let li = document.createElement("li")
        let div = document.createElement("div")
        let divBandeau = document.createElement("div")
        let span = document.createElement("span")
        let h4 = document.createElement("h4")
        let p = document.createElement("p")

        let chaineEtat = ""
        for (let etat in listeEtat) {
            chaineEtat += listeEtat[etat] + " "
        }

        span.innerText = dataOnduleurs[donnee]["slave_id"]
        h4.innerText = dataOnduleurs[donnee]["nom"]
        p.innerText = chaineEtat
        div.classList.add("titreEtatOnduleurs")
        divBandeau.classList.add("bandeauListe")

        if (listeEtat.includes("Locked") || listeEtat.includes("Déconnecté")) {
            divBandeau.style.background = "#dd4949"
            span.style.background = "#dd4949"
        } else {
            divBandeau.style.background = "var(--main-color)"
        }

        li.classList.add("hide")
        div.appendChild(span)
        div.appendChild(h4)
        li.appendChild(divBandeau)
        li.appendChild(div)
        li.appendChild(p)
        liste.appendChild(li)

        setTimeout(() => {
            li.classList.remove("hide")
        }, 1)
    }
}

function creerAffichageACDC(data) {
    let dcPuissance = 0
    let dcTension = 0
    let indCouleur = 0
    // on parcours tous les string de panneaux et on fait la sommme des puissance
    let dataPuissance = []
    let colorPuissance = []
    let labelPuissance = []
    // calcul puissance dc de tous les panneaux
    for (let onduleur in data) {
        let pvPuissance = 0
        for (let pv in data[onduleur]["puissance_dc"]) {
            pvPuissance = pvPuissance + data[onduleur]["puissance_dc"][pv]
            dcPuissance = dcPuissance + data[onduleur]["puissance_dc"][pv]
        }
        dataPuissance.push(pvPuissance)
        colorPuissance.push(listeCouleur[indCouleur % listeCouleur.length])
        indCouleur = indCouleur + 1
    }
    document.getElementById("puissanceDC").innerText = dcPuissance + " kW"

    let acPuissance = 0
    let reacPuissance = 0
    for (let onduleur in data) {
        acPuissance = acPuissance + data[onduleur]["puissance_ac"]
        reacPuissance = reacPuissance + data[onduleur]["puissance_reactive"]
    }
    document.getElementById("puissanceAC").innerText = acPuissance + " kW"
    document.getElementById("puissanceReac").innerText = reacPuissance + " kW"

    let lastDataFromBdd = data

    request("GET", "/soe/dashboard/onduleursInfo/").then(data => {
        // création du tableau des état ici pour pas devoir faire deux requettek
        creerTableauEtat(data, lastDataFromBdd)

        // on récupère la pmax de tous les onduleurs et on les parcours pour en faire la sommme
        let allPmax = 0
        for (let onduleur in data) {
            allPmax = allPmax + data[onduleur]["pmax"]
            labelPuissance.push(data[onduleur]["nom"] + ", Slave ID : " + data[onduleur]["slave_id"])
        }

        // création du chart en demi cercle pour la puissance dc
        let canvas = document.getElementById("canvasPuissanceDC");

        dataPuissance.push(allPmax-dcPuissance)
        colorPuissance.push("gray")
        labelPuissance.push("")

        new Chart(canvas, {
            type: 'doughnut',
            data: {
                datasets: [
                    {
                        label: ' Puissance Totale DC ',
                        labelsCustom: ["", ""],
                        data: [dcPuissance, allPmax-dcPuissance],
                        backgroundColor: ["blue", "gray"],
                        borderColor: [
                            'white',
                            'white'
                        ],
                        hoverOffset: 10,
                        borderWidth: 2
                    },
                    {
                        label: ' Puissance DC ',
                        labelsCustom: labelPuissance,
                        data: dataPuissance,
                        backgroundColor: colorPuissance,
                        borderColor: [
                            'white',
                            'white'
                        ],
                        hoverOffset: 10,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                rotation: -90,
                circumference: 180,
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        filter: function (ctx) {
                            let dataset = ctx.dataset;
                            if (ctx.dataIndex == dataset.data.length-1) {
                                return false
                            }
                            return true
                        },
                        callbacks: {
                            label: function(ctx) {
                                let dataset = ctx.dataset;
                                if (dataset.datasetIndex == 0){
                                    return dataset.label + " : " + dataset.data[ctx.dataIndex];
                                } else {
                                    return [[dataset.label + " : " + dataset.data[ctx.dataIndex] + " kW"], dataset.labelsCustom[ctx.dataIndex]];
                                }
                            }
                        }
                    }
                }
            }
        })


        // création du chart en demi cercle pour la puissance ac
        let canvasAc = document.getElementById("canvasPuissanceAC");

        new Chart(canvasAc, {
            type: 'doughnut',
            data: {
                datasets: [
                    {
                        label: ' Puissance Totale AC ',
                        labelsCustom: [acPuissance, ""],
                        data: [acPuissance, acPuissance-allPmax],
                        backgroundColor: ["black", "gray"],
                        borderColor: [
                            'white',
                            'white'
                        ],
                        hoverOffset: 10,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                rotation: -90,
                circumference: 180,
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        filter: function (ctx) {
                            let dataset = ctx.dataset;
                            if (ctx.dataIndex == dataset.data.length-1) {
                                return false
                            }
                            return true
                        },
                        callbacks: {
                            label: function(ctx) {
                                let dataset = ctx.dataset;
                                return dataset.label + " : " + dataset.data[ctx.dataIndex] + " kW";
                            }
                        }
                    }
                }
            }
        })

        // création du chart en demi cercle pour la puissance reactive
        let canvasReac = document.getElementById("canvasPuissanceReac");

        new Chart(canvasReac, {
            type: 'doughnut',
            data: {
                datasets: [
                    {
                        label: ' Puissance Réacrtive ',
                        labelsCustom: [reacPuissance, ""],
                        data: [reacPuissance, reacPuissance-allPmax],
                        backgroundColor: ["black", "gray"],
                        borderColor: [
                            'white',
                            'white'
                        ],
                        hoverOffset: 10,
                        borderWidth: 2
                    }
                ]
            },
            options: {
                rotation: -90,
                circumference: 180,
                plugins: {
                    legend: {
                        display: false,
                    },
                    tooltip: {
                        filter: function (ctx) {
                            let dataset = ctx.dataset;
                            if (ctx.dataIndex == dataset.data.length-1) {
                                return false
                            }
                            return true
                        },
                        callbacks: {
                            label: function(ctx) {
                                let dataset = ctx.dataset;
                                return dataset.label + " : " + dataset.data[ctx.dataIndex] + " kW";
                            }
                        }
                    }
                }
            }
        })
    })
}
