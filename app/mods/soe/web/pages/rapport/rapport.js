// TODO les fonctions des data doivent toutes retournée une liste de données affichable par le chart avec le bon interval de temps
const listeData = {
    "Puissance DC": (data) => {console.log(data)},
    "Tension DC": (data) => {console.log(data)},
    "Courant DC": (data) => {console.log(data)},
    "Puissance AC ": (data) => {console.log(data)},
    "Puissance AC L1": (data) => {console.log(data)},
    "Puissance AC L2": (data) => {console.log(data)},
    "Puissance AC L3": (data) => {console.log(data)},
    "Tension AC": (data) => {console.log(data)},
    "Tension AC L1": (data) => {console.log(data)},
    "Tension AC L2": (data) => {console.log(data)},
    "Tension AC L3": (data) => {console.log(data)},
    "Courant AC": (data) => {console.log(data)},
    "Courant AC L1": (data) => {console.log(data)},
    "Courant AC L2": (data) => {console.log(data)},
    "Courant AC L3": (data) => {console.log(data)},
    "Fréquence AC": (data) => {console.log(data)},
    "Fréquence AC L1": (data) => {console.log(data)},
    "Fréquence AC L2": (data) => {console.log(data)},
    "Fréquence AC L3": (data) => {console.log(data)},
    "Facteur de limitation de puissance": (data) => {console.log(data)},
    "Déphasage cos phi": (data) => {console.log(data)},
    "Température": (data) => {console.log(data)},
    "Puissance réactive": (data) => {console.log(data)},
    "Énergie": (data) => {console.log(data)},
}

function requestDataMultiChart(event, premiereFois=false) {
    // recup value des inputs
    let inputDateDebut = document.getElementById("inputDateDebut")
    let inputDateFin = document.getElementById("inputDateFin")

    let now = new Date()
    now.setHours(0, 0, 0, 0)
    let nowMoinsUnMois = new Date()
    nowMoinsUnMois.setMonth(nowMoinsUnMois.getMonth() - 1)
    nowMoinsUnMois.setHours(0, 0, 0, 0)
    nowMoinsUnMois.setDate(nowMoinsUnMois.getDate()+1)
    now.setDate(now.getDate()+1)
    
    let start = nowMoinsUnMois.getTime()
    let end = now.getTime()
    
    if (inputDateDebut.valueAsDate) {
        inputDateDebut.valueAsDate.setDate(inputDateDebut.valueAsDate.getDate()+1)
        start = inputDateDebut.valueAsDate.setHours(0, 0, 0, 0)
    }
    if (inputDateFin.valueAsDate) {
        inputDateFin.valueAsDate.setDate(inputDateFin.valueAsDate.getDate()+1)
        end = inputDateFin.valueAsDate.setHours(0, 0, 0, 0)
    }

    // on retire les millisecondes
    start = Math.floor(start / 1000)
    end = Math.floor(end / 1000)
    if (start > end) {
        console.log("erreur, la date de début est supérieur a la date de fin")
        return
    }

    request("POST", "/soe/site/getDataFromBdd/", {"start": start, "end": end}).then(data => {
        creerMultiChart(data, start, end, event)
    })
}

function repartirDonneesParOnudleurs(data) {
    let onduleursData = {}
    for (donnee in data) {
        if (onduleursData[data[donnee]["mac_onduleur"]+"_"+data[donnee]["slave_id"]] === undefined) {
            onduleursData[data[donnee]["mac_onduleur"]+"_"+data[donnee]["slave_id"]] = []
        }
        onduleursData[data[donnee]["mac_onduleur"]+"_"+data[donnee]["slave_id"]].push(data[donnee])
    }
    return onduleursData
}

function checkCheckbox(details) {
        let elems = details.getElementsByTagName("input")
        elems = [...elems]
        elems.shift()
        for (let elem in elems) {
            elems[elem].disabled = !elems[elem].disabled
        }
}

function creerInputs(onduleursData) {
    let spanInputs = document.getElementsByClassName("inputsData")[0]
    spanInputs.innerHTML = ""
    const nomSite = "Site"

    // le site
    if (Object.keys(onduleursData).length != 0) {
        let detail = document.createElement("details")
        let summary = document.createElement("summary")
        let label = document.createElement("label")
        let checkbox = document.createElement("input")
        label.setAttribute("for", nomSite)
        label.innerText = nomSite
        checkbox.onchange = () => checkCheckbox(detail)
        checkbox.id = nomSite
        checkbox.style.transform = "scale(1.3)"
        checkbox.type = "checkbox"
        checkbox.checked = true
        summary.innerText = nomSite
        summary.style.fontSize = "1.2em"
    
        label.appendChild(checkbox)
        summary.appendChild(label)
        detail.appendChild(summary)
        for (let data in listeData) {
            let checkbox = document.createElement("input")
            let label = document.createElement("label")
            label.innerText = data
            label.setAttribute("for", data)
            checkbox.type = "checkbox"
            checkbox.name = data
            checkbox.id = data
            checkbox.onclick = () => listeData[data](onduleursData)
            label.appendChild(checkbox)
            detail.appendChild(label)
        }
        spanInputs.appendChild(detail)
    } else {
        let h2 = document.createElement("h2")
        h2.innerText = "Pas de données pour la période sélèctionnée."
        spanInputs.appendChild(h2)
    }

    // les onduleurs
    for (let macOnduleur in onduleursData) {
        let detail = document.createElement("details")
        let summary = document.createElement("summary")
        let label = document.createElement("label")
        let checkbox = document.createElement("input")
        let span = document.createElement("span")

        span.classList.add("spanLabelInput")
        label.setAttribute("for", macOnduleur)
        label.innerText = macOnduleur
        checkbox.onchange = () => checkCheckbox(detail)
        checkbox.id = macOnduleur
        checkbox.style.transform = "scale(1.3)"
        checkbox.type = "checkbox"
        checkbox.checked = true
        summary.innerText = "Onduleur"
        summary.style.fontSize = "1.2em"

        label.appendChild(checkbox)
        summary.appendChild(label)
        detail.appendChild(summary)
        
        // un onduleur
        for (let data in listeData) {
            let checkbox = document.createElement("input")
            let label = document.createElement("label")
            label.innerText = data
            label.setAttribute("for", macOnduleur + "_" + data)
            checkbox.type = "checkbox"
            checkbox.name = data
            checkbox.id = macOnduleur + "_" + data
            checkbox.onclick = () => listeData[data](onduleursData[macOnduleur])
            label.appendChild(checkbox)
            detail.appendChild(label)
        }
        spanInputs.appendChild(detail)
    }
}

// TODO fonction qui est appelée quand on clique sur une checkbox de details pour ajouter ou éffacer des datasets du graphique
function invertDrawedState() {
    // TODO appeler les fonctions qui retourne les data
}

function initOrUpdateGraph(nomCanvas, tableauAbscisse, listeDatasets) {
    // génération des datasets
    // TODO lors de la génération des datasets il faut ajouter un champs custom qui sert à identifier le dataset 

    let chart = Chart.getChart(nomCanvas)
    if (!chart) {
        let canvasMultiChart = document.getElementById(nomCanvas)
        new Chart(canvasMultiChart, {
            data: {
                // TODO générer les dataset en fonction des input coché par le user
                datasets: [
                    {
                        type: 'bar',
                        // TODO ça doit être le nom et l'id de l'onduleur ou bien le site
                        label: 'Bar Dataset',
                        // TODO couleur en fonction d'une liste de couleur avec une version plus clair de  chaque couleur pour les lignes du chart
                        yAxisID: 'Primaire',
                        backgroundColor: "#C8DBFE",
                        borderColor: "green",
                        // TODO en fonction du type de graphique les lines doivent être au dessus
                        order: 2,
                        data: [5700, 6300, 8200]
                    },
                    {
                        type: 'line',
                        label: 'Bar Dataset',
                        yAxisID: 'Secondaire',
                        backgroundColor: "#ccffcc",
                        borderColor: "green",
                        order: 1,
                        cubicInterpolationMode: "monotone",
                        data: [11, 3.6, 7.3, 8.1]
                    }
                ],
                labels: tableauAbscisse
            },
            options: {
                responsive: true,
                // plugins: {
                //     legend: {
                //         display: false,
                //     }
                // },
                scales: {
                    Primaire: {
                        type: 'linear',
                        position: 'left',
                        ticks: { beginAtZero: true, color: 'blue' },
                        grid: {
                            color: function(context) {
                                return '#C8DBFE';
                            },
                        },
                    },
                    // TODO enlever cet axe quand on en a pas besoins
                    Secondaire: {
                        type: 'linear',
                        position: 'right',
                        ticks: { beginAtZero: true, color: '#0c5b4f' },
                        grid: {
                            color: function(context) {
                                return '#a1dbcd';
                            },
                        },
                    }
                }
            }
        })
    } else {
        // TODO modifier les data, labels, couleur, type axes
        chart.data.labels = tableauAbscisse
        chart.update()
    }
}

function genAbscisse(start, end) {
    // choix du pas en fonction de la taille de l'interval et de l'input user
    let intervalTimeStamp = end - start
    let maxCol = 62
    let tablePas = {
        heure: 3600,
        jour: 24 * 3600,
        mois: 24 * 3600 * 31,
        annee: 24 * 3600 * 31 * 12
    }
    
    let pas = ""
    let inputPas = document.getElementById("pas")
    if (intervalTimeStamp / tablePas[inputPas.value] > maxCol) {
        console.log("erreur, prendre un interval plus petit")
    } else {
        pas = inputPas.value
    }

    if (pas == "") {
        if (intervalTimeStamp < 2*tablePas.jour) {
            pas = "heure"
        } else if (intervalTimeStamp < 2*tablePas.mois) {
            pas = "jour"
        } else if (intervalTimeStamp < 2*tablePas.annee) {
            pas = "mois"
        } else {
            pas = "annee"
        }
    }
    inputPas.value = pas

    let chaineAPush = undefined
    let tableauAbscisse = []
    let debut = new Date(start*1000)
    let fin = new Date(end*1000)
    let date = debut
    let premierTour = true
    while (date <= fin) {
        let jour = "0" + date.getDate()
        jour = jour.substring(jour.length - 2)
        let mois = "0" + Number(date.getMonth() + 1)
        mois = mois.substring(mois.length - 2)
        let annee = date.getFullYear()
        
        chaineAPush = ""
        if (pas == "heure") {
            let heure = "0" + Number(date.getHours())
            heure = heure.substring(heure.length - 2)
            let min = "0" + Number(date.getMinutes())
            min = min.substring(min.length - 2)

            chaineAPush = [jour + "/" + mois, " " +heure + ":" + min]
            date.setHours(date.getHours()+1)
        } else if (pas == "jour") {
            chaineAPush = jour + "/" + mois
            date.setDate(date.getDate()+1)
        } else if (pas == "mois") {
            chaineAPush = mois + " / " + annee
            date.setMonth(date.getMonth()+1)
            if (premierTour) {
                fin.setMonth(fin.getMonth()+1)
                fin.setDate(0)
                premierTour = false
            }
        } else {
            chaineAPush = annee
            date.setFullYear(date.getFullYear()+1)
            if (premierTour) {
                fin.setFullYear(fin.getFullYear(), 11, 31)
                premierTour = false
            }
        }
        tableauAbscisse.push(chaineAPush)
    }
    return tableauAbscisse
}

function genListeDatas(start, end) {
    
}

function creerMultiChart(data, start, end, event) {
    let onduleursData = repartirDonneesParOnudleurs(data)

    // création et mise à jour des checkbox d'affichage de données
    creerInputs(onduleursData)

    // update l'abscice donc le temps pck cette fonction est appellée à chaque changement de delta temps
    let tableauAbscisse = genAbscisse(start, end)

    // TODO resolve les inputs qui sont checkés pour qu'ils se raclculent
    let listeDatasets = []

    // initialistaion ou mise à jour du chart avec les nouveaux datasets et interval de temps
    initOrUpdateGraph("canvasMultiChart", tableauAbscisse, listeDatasets)
}