const listeCouleur = ["chartreuse", "DarkGreen", "blue", "green", "lime", "DarkCyan"]
const anneMinHisto = 2022
const listeMois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

request("GET", "/soe/dashboard/data/").then(data => {
    // création de la page à partir des données de la bdd
    console.log(data)
    creerAffichageACDC(data)
})

function getMonthFromString(nom){
    return new Date(Date.parse(nom +" 1, 2012")).getMonth()+1
}

// construction du graph de l'historique
function requestHistoAC() {
    // recup value des inputs
    let inputHistoMois = document.getElementById("inputHistoMois")
    let inputHistoAnnee = document.getElementById("inputHistoAnnee")
    let mois = listeMois.indexOf(inputHistoMois.value)+1
    let annee = Number(inputHistoAnnee.value)
    let start = new Date(annee, mois-1, 1)
    let end = new Date(annee, mois-1, new Date(annee, mois, 0).getDate())
    request("POST", "/soe/dashboard/dataHisto/", {"start":start, "end":end}).then(data => {
        creerAffichageHistoriqueAC(data, new Date(annee, mois, 0).getDate())
    })
}

function creerAffichageACDC(data) {
    let dcPuissance = 0
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
    for (let onduleur in data) {
        acPuissance = acPuissance + data[onduleur]["puissance_ac"]
    }
    document.getElementById("puissanceAC").innerText = acPuissance + " kW"

    request("GET", "/soe/dashboard/onduleursInfo/").then(data => {
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
                                return dataset.label + " : " + dataset.data[ctx.dataIndex];
                            }
                        }
                    }
                }
            }
        })
    })
}

function creerAffichageHistoriqueAC(data, nbJourMois){
    sommePuissanceParJour = {}
    for (let i = 0; i < nbJourMois; i++) {
        sommePuissanceParJour[i+1] = 0
    }
    for (onduleur in data) {
        jour = new Date(data[onduleur]["time"]).getDay()
        sommePuissanceParJour[jour] = sommePuissanceParJour[jour] + data[onduleur]["puissance_ac"]
    }
    
    dataPuissanceMois = []
    labelPuissanceMois = []
    for(jour in sommePuissanceParJour) {
        dataPuissanceMois.push(sommePuissanceParJour[jour])
        labelPuissanceMois.push(jour)
    }

    let inputHistoMois = document.getElementById("inputHistoMois")

    // on vérifie que yai pas déjà un chart et si y en a un on update et on se casse
    let chart = Chart.getChart("canvasHistoriqueAC")
    if (chart) {
        chart.data.labels = labelPuissanceMois
        chart.data.datasets[0].data = dataPuissanceMois
        chart.data.datasets[0].labels = dataPuissanceMois
        chart.update()
        return
    }

    let canvasHisto = document.getElementById("canvasHistoriqueAC");
    new Chart(canvasHisto, {
        type: 'bar',
        data: {
            labels: labelPuissanceMois,
            datasets: [{
                label: 'Puissance AC kW par jour',
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
                            return value + ' kW';
                        }
                    },
                    title: {
                        color: 'black',
                        display: true,
                        text: 'Puissance'
                    }
                },
                x: {
                    ticks: {
                        callback: function(value, index, ticks) {
                            let mois = listeMois.indexOf(inputHistoMois.value)+1
                            if (String(mois).length == 1) {
                                mois = "0" + mois
                            }
                            if (String(value+1).length == 1) {
                                return "0" + (value+1) + "/" + mois;
                            }
                            return (value+1) + "/" + mois;
                        }
                    },
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
                            console.log("dalur")
                            return [dataset.label + " : " + dataset.data[ctx.dataIndex] + " kW"];
                        }
                    }
                }
            }
        }
    })
}