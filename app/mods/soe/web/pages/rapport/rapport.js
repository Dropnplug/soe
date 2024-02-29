const tablePas = {
    heure: 3600,
    jour: 24 * 3600,
    mois: 24 * 3600 * 31,
    annee: 24 * 3600 * 31 * 12
}

const variationCouleur = 2

var checkboxChecked = []
var checkboxMasterUnchecked = []
var detailsOpen = []

// TODO les fonctions des data doivent toutes retournée une liste de données affichable par le chart avec le bon interval de temps
const listeData = {
    "Puissance DC": (data, start, end, pas, checkboxId, label) => {
        let donnees = []
        let debut = new Date(start*1000)
        
        let indCol = 0
        for (let macOnduleur in data) {
            indCol = 0
            let dateAvant = undefined
            let dateActuelle = undefined
            let reverseData = Object.keys(data[macOnduleur]).reverse()
            let nombreDeData = 0
            for (let indice in reverseData) {
                nombreDeData += 1
                if (dateAvant == undefined) {
                    dateAvant = debut
                }
                dateActuelle = new Date(data[macOnduleur][reverseData[indice]]["time"])
                let difference = getPasDifferenceEntreDate(dateAvant, dateActuelle, pas)
                if (difference != 0) {
                    if (donnees[indCol] != undefined) {
                        donnees[indCol] = Math.round((donnees[indCol]/nombreDeData)/1000)
                    }
                    nombreDeData = 0
                    indCol += difference
                }
                dateAvant = new Date(data[macOnduleur][reverseData[indice]]["time"])
                for (let pvString in data[macOnduleur][reverseData[indice]]["puissance_dc"]) {
                    if (donnees[indCol] == undefined) {
                        donnees[indCol] = 0
                    }
                    donnees[indCol] += Number(data[macOnduleur][reverseData[indice]]["puissance_dc"][pvString])
                }
            }
        }

        datasetAajouter = {
                data: donnees,
                unit:"kw",
                id: checkboxId,
                label: "Puissance DC" + " " + label
            }
        
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Tension DC": (data, start, end, pas, checkboxId, label) => {
        datasetAajouter = {
            data: [100],
            unit:"V",
            id: checkboxId,
            label: "Tension DC" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Courant DC": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Puissance AC ": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Puissance AC L1": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Puissance AC L2": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Puissance AC L3": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Tension AC": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Tension AC L1": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Tension AC L2": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Tension AC L3": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Courant AC": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Courant AC L1": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Courant AC L2": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Courant AC L3": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Fréquence AC": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Fréquence AC L1": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Fréquence AC L2": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Fréquence AC L3": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Facteur de limitation de puissance": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Déphasage cos phi": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Température": (data, start, end, pas, checkboxId, label) => {
        let donnees = []
        let debut = new Date(start*1000)
        
        let indCol = 0
        for (let macOnduleur in data) {
            indCol = 0
            let dateAvant = undefined
            let dateActuelle = undefined
            let reverseData = Object.keys(data[macOnduleur]).reverse()
            let nombreDeData = 0
            for (let indice in reverseData) {
                nombreDeData += 1
                if (dateAvant == undefined) {
                    dateAvant = debut
                }
                dateActuelle = new Date(data[macOnduleur][reverseData[indice]]["time"])
                let difference = getPasDifferenceEntreDate(dateAvant, dateActuelle, pas)
                if (difference != 0) {
                    if (donnees[indCol] != undefined) {
                        donnees[indCol] = Math.round((donnees[indCol]/nombreDeData)/1000)
                    }
                    nombreDeData = 0
                    indCol += difference
                }
                dateAvant = new Date(data[macOnduleur][reverseData[indice]]["time"])
                for (let pvString in data[macOnduleur][reverseData[indice]]["puissance_dc"]) {
                    if (donnees[indCol] == undefined) {
                        donnees[indCol] = 0
                    }
                    donnees[indCol] += Number(data[macOnduleur][reverseData[indice]]["puissance_dc"][pvString])
                }
            }
        }

        datasetAajouter = {
                data: donnees,
                unit:"°C",
                id: checkboxId,
                label: "Température" + " " + label
            }
        
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Puissance réactive": (data, start, end, pas) => {console.log(data, start, end, pas)},
    "Énergie": (data, start, end, pas) => {console.log(data, start, end, pas)},
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

function getPasDifferenceEntreDate(dateAvant, dateActuelle, pas) {
    // soustraire les dates sur le pas
    let difference = 0
    switch (pas) {
        case "heure":
            dateAvant = dateAvant.getTime() / 1000
            dateActuelle = dateActuelle.getTime() / 1000
            difference = Math.round(Math.abs(dateActuelle - dateAvant) / 3600)
            break;
        case "jour":
            dateAvant = dateAvant.getTime() / 1000
            dateActuelle = dateActuelle.getTime() / 1000
            difference = Math.round(Math.abs((dateAvant - dateActuelle) / tablePas.jour))
            break;
        case "mois":
            difference = dateActuelle.getMonth() - dateAvant.getMonth() + (12 * (dateActuelle.getFullYear() - dateAvant.getFullYear()))
            break;
        case "annee":
            difference = dateActuelle.getFullYear() - dateAvant.getFullYear()
            break;
    
        default:
            break;
    }
    return difference
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
        let masterCheckbox = elems.shift()
        
        if (masterCheckbox.checked == false) {
            if (!checkboxMasterUnchecked.includes(masterCheckbox.id)) {
                checkboxMasterUnchecked.push(masterCheckbox.id)
            }
        } else {
            let index = checkboxMasterUnchecked.indexOf(masterCheckbox.id)
            if (index > -1) {
                checkboxMasterUnchecked.splice(index, 1)
            }
        }

        for (let elem in elems) {
            elems[elem].disabled = !elems[elem].disabled
            if (elems[elem].disabled == false && elems[elem].checked) {
                // deux appels pour décocher puis recocher et fire l'envent onchange
                elems[elem].click()
                elems[elem].click()
            } else {
                supprimerDatasetsFromChart("canvasMultiChart", elems[elem].id)
            }
        }
}

// TODO découper cette fonction en sous fonction pour pas dupliquer le code
function creerInputs(onduleursData, start, end, pas, tableauAbscisse) {
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
        detail.id = "detail_"+nomSite
        detail.ontoggle = () => {
            if (detail.open) {
                detailsOpen.push(detail.id)
            } else {
                let index = detailsOpen.indexOf(detail.id)
                if (index > -1) {
                    detailsOpen.splice(index, 1)
                }
            }
        }
        checkbox.onchange = () => checkCheckbox(detail)
        checkbox.id = nomSite
        checkbox.style.transform = "scale(1.3)"
        checkbox.type = "checkbox"
        checkbox.checked = true
        let checkboxMaster = checkbox
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
            checkbox.onchange = () => {
                if (checkbox.checked) {
                    // appelle à la bonne fonction grâce au nom de la donnée
                    if (!checkboxChecked.includes(checkbox.id)) {
                        checkboxChecked.push(checkbox.id)
                    }
                    listeData[data](onduleursData, start, end, pas, checkbox.id, nomSite)
                } else {
                    supprimerDatasetsFromChart("canvasMultiChart", checkbox.id)
                    let index = checkboxChecked.indexOf(checkbox.id)
                    if (index > -1) {
                        checkboxChecked.splice(index, 1)
                    }
                }
            }
            label.appendChild(checkbox)
            detail.appendChild(label)
            if (checkboxChecked.includes(checkbox.id)) {
                checkbox.click()
            }
        }
        spanInputs.appendChild(detail)
        
        if (checkboxMasterUnchecked.includes(checkboxMaster.id)) {
            checkboxMaster.click()
        }

        if (detailsOpen.includes(detail.id)) {
            detail.open = true
        }
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

        detail.id = "detail_"+macOnduleur
        detail.ontoggle = () => {
            if (detail.open) {
                detailsOpen.push(detail.id)
            } else {
                let index = detailsOpen.indexOf(detail.id)
                if (index > -1) {
                    detailsOpen.splice(index, 1)
                }
            }
        }
        span.classList.add("spanLabelInput")
        label.setAttribute("for", macOnduleur)
        label.innerText = macOnduleur
        checkbox.onchange = () => checkCheckbox(detail)
        checkbox.id = macOnduleur
        checkbox.style.transform = "scale(1.3)"
        checkbox.type = "checkbox"
        checkbox.checked = true
        let checkboxMaster = checkbox
        summary.innerText = "Onduleur"
        summary.style.fontSize = "1.2em"

        label.appendChild(checkbox)
        summary.appendChild(label)
        detail.appendChild(summary)

        if (checkboxChecked.includes(checkbox.id)) {
            checkbox.click()
        }
        
        // un onduleur
        for (let data in listeData) {
            let checkbox = document.createElement("input")
            let label = document.createElement("label")
            // TODO trouver le nom de l'onduleur
            label.innerText = data
            label.setAttribute("for", macOnduleur + "_" + data)
            checkbox.type = "checkbox"
            checkbox.name = data
            checkbox.id = macOnduleur + "_" + data
            checkbox.onchange = () => {
                if (checkbox.checked) {
                    let object = {}
                    object[macOnduleur] = onduleursData[macOnduleur]
                    // appelle à la bonne fonction grâce au nom de la donnée
                    if (!checkboxChecked.includes(checkbox.id)) {
                        checkboxChecked.push(checkbox.id)
                    }
                    listeData[data](object, start, end, pas, checkbox.id, macOnduleur)
                } else {
                    supprimerDatasetsFromChart("canvasMultiChart", checkbox.id)
                    let index = checkboxChecked.indexOf(checkbox.id)
                    if (index > -1) {
                        checkboxChecked.splice(index, 1)
                    }
                }
            }
            label.appendChild(checkbox)
            detail.appendChild(label)
            if (checkboxChecked.includes(checkbox.id)) {
                checkbox.click()
            }
        }
        spanInputs.appendChild(detail)
        if (checkboxMasterUnchecked.includes(checkboxMaster.id)) {
            checkboxMaster.click()
        }
        if (detailsOpen.includes(detail.id)) {
            detail.open = true
        }
    }
}

function shadeColor(color, percent) {
    var R = parseInt(color.substring(1,3),16);
    var G = parseInt(color.substring(3,5),16);
    var B = parseInt(color.substring(5,7),16);

    R = parseInt((R + percent)%255);
    G = parseInt((G + percent)%255);
    B = parseInt((B + percent)%255);
    console.log(R, G, B)

    R = (R<255)?R:255;
    G = (G<255)?G:255;
    B = (B<255)?B:255;

    R = Math.round(R)
    G = Math.round(G)
    B = Math.round(B)

    var RR = ((R.toString(16).length==1)?"0"+R.toString(16):R.toString(16));
    var GG = ((G.toString(16).length==1)?"0"+G.toString(16):G.toString(16));
    var BB = ((B.toString(16).length==1)?"0"+B.toString(16):B.toString(16));

    return "#"+RR+GG+BB;
}

function addOrRemoveAxeSecondaire(nomCanvas) {
    let chart = Chart.getChart(nomCanvas)
    let units = {}
    
    let trouve = false
    let i = 0
    while (!trouve && i < chart.data.datasets.length) {
        units[chart.data.datasets[i].unit] = 1
        if (Object.keys(units).length > 1) {
            trouve = true
        }
        i += 1
    }

    if (trouve) {
        chart.options.scales["Secondaire"] = {
            type: 'linear',
            position: 'right',
            ticks: { beginAtZero: true, color: '#0c5b4f' },
            grid: {
                color: function(context) {
                    return '#a1dbcd'
                }
            }
        }
    } else {
        if (chart.options.scales["Secondaire"] != undefined) {
            delete chart.options.scales["Secondaire"]
        }
    }

    chart.update()
}

function supprimerDatasetsFromChart(nomCanvas, idDataset) {
    let chart = Chart.getChart(nomCanvas)
    
    let trouve = false
    let i = 0
    while (!trouve && i < chart.data.datasets.length) {
        if (chart.data.datasets[i].id == idDataset) {
            // chart.data.units[chart.data.datasets[i].unit].backgroundColor = shadeColor(chart.data.units[chart.data.datasets[i].unit].backgroundColor, variationCouleur)
            // chart.data.units[chart.data.datasets[i].unit].borderColor = shadeColor(chart.data.units[chart.data.datasets[i].unit].borderColor, variationCouleur)
            // chart.data.units[chart.data.datasets[i].unit]["nombre"] += 1
            chart.data.datasets.splice(i, 1)
            trouve = true
        }
        i += 1
    }

    if (trouve) {
        addOrRemoveAxeSecondaire("canvasMultiChart")
        chart.update()
    }
}

function supprimerTousLesDatasets(nomCanvas) {
    let chart = Chart.getChart(nomCanvas)
    chart.data.datasets = []
    addOrRemoveAxeSecondaire("canvasMultiChart")
    chart.update()
}

function initOrUpdateGraph(nomCanvas, tableauAbscisse=undefined, datasetAajouter) {
    let chart = Chart.getChart(nomCanvas)
    if (!chart) {
        let canvasMultiChart = document.getElementById(nomCanvas)
        new Chart(canvasMultiChart, {
            data: {
                units: {},
                datasets: [],
                labels: tableauAbscisse
            },
            options: {
                responsive: true,
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
                }
            }
        })
    } else {
        // modifier les data, labels, couleur, type axes
        if (tableauAbscisse != undefined) {
            chart.data.labels = tableauAbscisse
        } else {
            supprimerDatasetsFromChart(nomCanvas, datasetAajouter.id)
            // il y a déjà un dataset avec l'unité du dataset à ajouter
            if (Object.keys(chart.data.units).includes(datasetAajouter.unit)) {
                datasetAajouter.yAxisID = chart.data.units[datasetAajouter.unit]["yAxisID"]
                datasetAajouter.backgroundColor = shadeColor(chart.data.units[datasetAajouter.unit].backgroundColor, variationCouleur)
                datasetAajouter.borderColor = shadeColor(chart.data.units[datasetAajouter.unit].borderColor, variationCouleur)
            } else { // il n'y en a pas
                if (chart.data.datasets.length == 0 || (chart.data.datasets.length == 1 && chart.data.units[Object.keys(chart.data.units)[0]]["yAxisID"] == "Secondaire")) {
                    datasetAajouter.yAxisID = "Primaire"
                    datasetAajouter.backgroundColor = "#c8dbfe"
                    datasetAajouter.borderColor = "#0000ff"
                } else if (chart.data.datasets.length == 1) {
                    datasetAajouter.yAxisID = "Secondaire"
                    datasetAajouter.backgroundColor = "#ccffcc"
                    datasetAajouter.borderColor = "#00ff00"
                } else {
                    console.log("on peut pas ajouter de donnée le graphique est déjà plein")
                    document.getElementById(datasetAajouter.id).click()
                    console.log(checkboxChecked)
                    console.log(chart.data.units)
                    chart.update()
                    return
                }
            }
            
            chart.data.units[datasetAajouter.unit] = {
                yAxisID: datasetAajouter.yAxisID,
                backgroundColor: datasetAajouter.backgroundColor,
                borderColor: datasetAajouter.borderColor,
                // nombre: nombre
            }
            
            datasetAajouter.type = "line"
            datasetAajouter.cubicInterpolationMode = "monotone"
            // TODO ajouter l'unité sur les axes
            chart.data.datasets.push(datasetAajouter)
        }
        chart.update()
        addOrRemoveAxeSecondaire(nomCanvas)
    }
}

function genAbscisse(start, end) {
    // choix du pas en fonction de la taille de l'interval et de l'input user
    let intervalTimeStamp = end - start
    let maxCol = 62
    
    
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

    let tableauAbscisse = repartirTemps(start, end, pas)
    return [tableauAbscisse, pas]
}

function repartirTemps(start, end, pas) {
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

function creerMultiChart(data, start, end, event) {
    let onduleursData = repartirDonneesParOnudleurs(data)
    
    // update l'abscice donc le temps pck cette fonction est appellée à chaque changement de delta temps
    let [tableauAbscisse, pas] = genAbscisse(start, end)
    
    // création et mise à jour des checkbox d'affichage de données
    creerInputs(onduleursData, start, end, pas, tableauAbscisse)

    let listeDatasets = {}

    // initialistaion ou mise à jour du chart avec les nouveaux datasets et interval de temps
    initOrUpdateGraph("canvasMultiChart", tableauAbscisse=tableauAbscisse, listeDatasets)
}