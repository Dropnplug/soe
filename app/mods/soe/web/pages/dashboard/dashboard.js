const listeCouleur = ["chartreuse", "DarkGreen", "blue", "green", "lime", "DarkCyan"]
const anneMinHisto = 2022
const listeMois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

request("GET", "/soe/site/lastData/").then(data => {
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

    request("POST", "/soe/site/dataHisto/", {"start":start, "end":end}).then(data => {
        creerAffichageHistoriqueAC(data, start, end)
    })
}

function creerAffichageHistoriqueAC(data, start, end){
    let sommePuissanceParJour = {}
    start = new Date(start)
    end = new Date(end)
    start.setHours(0)
    end.setHours(0)
    let realStart = new Date(start)
    realStart.setHours(0)

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
    
    let dataPuissanceMois = []
    let labelPuissanceMois = []

    let chart = Chart.getChart("canvasHistoriqueEnergie")
    if (!chart) {
        let canvasHisto = document.getElementById("canvasHistoriqueEnergie");
        new Chart(canvasHisto, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Energie produite ce jour',
                    data: [],
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
                            text: 'Énergie'
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
    } else {
        for(jour in sommePuissanceParJour) {
            dataPuissanceMois.push(Number(sommePuissanceParJour[jour].toFixed(2)))
            labelPuissanceMois.push(jour)
        }
        chart.data.labels = labelPuissanceMois
        chart.data.datasets[0].data = dataPuissanceMois
        chart.data.datasets[0].labels = dataPuissanceMois
        chart.update()
    }

    let horloge = 0
    for (let macOnduleur in puissanceParJourPArOnduleur) {
        let max = 0
        let lastEnergy = 0
        request("POST", "/soe/onduleur/LastEnergyData/", {"mac":macOnduleur.split("_")[0], "slave_id":macOnduleur.split("_")[1], "dateLimite":realStart}).then(data => {
            if (data.length > 0) {
                lastEnergy = data[0]["energie_totale"]
            }

            horloge += 1

            max = lastEnergy
            for (let jour in puissanceParJourPArOnduleur[macOnduleur]) {
                // recherche de l'énergie max (fonctionne car valeur rangées par ordre chrono)
                if (puissanceParJourPArOnduleur[macOnduleur][jour] > max) {
                    max = puissanceParJourPArOnduleur[macOnduleur][jour]
                }
                
                // si on a pas de donné le jour est à 0 par défaut
                if (puissanceParJourPArOnduleur[macOnduleur][jour] == 0) {
                    puissanceParJourPArOnduleur[macOnduleur][jour] = max
                }
                sommePuissanceParJour[jour] += puissanceParJourPArOnduleur[macOnduleur][jour]
            }
            
            // si c'est le dernier tour de boucle on peut maj le graphe
            if (horloge != Object.keys(puissanceParJourPArOnduleur).length) {
                return
            }

            let dernirereVariation = lastEnergy

            let sommePuissanceParJourVrai = {}
            Object.assign(sommePuissanceParJourVrai, sommePuissanceParJour)
            for (let jour in sommePuissanceParJourVrai) {
                sommePuissanceParJour[jour] = sommePuissanceParJourVrai[jour] - dernirereVariation
                dernirereVariation = sommePuissanceParJourVrai[jour]
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
            chart.data.labels = labelPuissanceMois
            chart.data.datasets[0].data = dataPuissanceMois
            chart.data.datasets[0].labels = dataPuissanceMois
            chart.update()
            
        })
    }
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
            chaineEtat += listeEtat[etat] + ", "
        }
        chaineEtat = chaineEtat.substring(0, chaineEtat.length - 2)

        span.innerText = dataOnduleurs[donnee]["slave_id"]
        h4.innerText = dataOnduleurs[donnee]["nom"]
        p.innerText = chaineEtat
        div.classList.add("titreEtatOnduleurs")
        divBandeau.classList.add("bandeauListe")

        let couleur = "var(--main-color)"
        if (listeEtat.includes("Locked")) {
            couleur = "#fc881b"
        } else if (listeEtat.includes("Déconnecté")) {
            couleur = "#dd4949"
        }
        divBandeau.style.background = couleur
        span.style.background = couleur

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
    let indCouleur = 0
    let acPuissance = 0
    let reacPuissance = 0
    // on parcours tous les string de panneaux et on fait la sommme des puissance
    let dataPuissance = []
    let colorPuissance = []
    let labelPuissance = []
    // calcul puissance dc de tous les panneaux
    for (let onduleur in data) {
        let pvPuissance = 0
        acPuissance = acPuissance + Number((data[onduleur]["puissance_ac"] * 0.001).toFixed(1))
        reacPuissance = reacPuissance + data[onduleur]["puissance_reactive"]
        for (let pv in data[onduleur]["puissance_dc"]) {
            pvPuissance = pvPuissance + Number((data[onduleur]["puissance_dc"][pv] * 0.001).toFixed(1))
            dcPuissance = dcPuissance + Number((data[onduleur]["puissance_dc"][pv] * 0.001).toFixed(1))
        }
        dataPuissance.push(pvPuissance)
        colorPuissance.push(listeCouleur[indCouleur % listeCouleur.length])
        indCouleur = indCouleur + 1
    }
    document.getElementById("puissanceDC").innerText = dcPuissance + " kW"
    document.getElementById("puissanceAC").innerText = acPuissance + " kW"
    document.getElementById("puissanceReac").innerText = reacPuissance + " kW"

    let lastDataFromBdd = data

    request("GET", "/soe/site/onduleursInfo/").then(data => {
        // création du tableau des état ici pour pas devoir faire deux requettek
        creerTableauEtat(data, lastDataFromBdd)

        // on récupère la pmax de tous les onduleurs et on les parcours pour en faire la sommme
        let allPmax = 0
        for (let onduleur in data) {
            allPmax = allPmax + Number((data[onduleur]["pmax"] * 0.001).toFixed(1))
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
