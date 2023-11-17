const listeCouleur = ["chartreuse", "DarkGreen", "blue", "green", "lime", "DarkCyan"]

request("GET", "/soe/dashboard/data/").then(data => {
    // création de la page à partir des données de la bdd
    creerAffichageACDC(data)
})

// construction du graph de l'historique
let now = new Date()
let start = new Date(now.getFullYear(), now.getMonth(), now.getDate() - 30).toISOString().slice(0, 10);
request("POST", "/soe/dashboard/dataHisto/", {"start":start, "end":"now"}).then(data => {
    console.log(data)
    creerAffichageHistoriqueDC(data)
})

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
                                console.log("qdlfkh")
                                return [dataset.label + " : " + dataset.data[ctx.dataIndex] + " kW"];
                            }
                        }
                    }
                }
            }
        })
    })
}

function creerAffichageHistoriqueDC(data){
    let datasets = {}
    for (onduleur in data) {
        console.log(data[onduleur])
        datasets["labels"]
        datasets[data[onduleur]["time"]]
    }

    let canvasHisto = document.getElementById("canvasHistoriqueAC");
    new Chart(canvasHisto, {
        type: 'bar',
        data: {
            labels:["a","a","a","a","a","a","a"],
            datasets: [{
                label: 'My First Dataset',
                data: [65, 59, 80, 81, 56, 55, 40],
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
        }
    })
}