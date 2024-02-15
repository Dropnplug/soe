const listeData = {
    "Puissance DC": (data) => {console.log(data)},
    "Tension DC": (event) => {console.log(event)},
    "Courant DC": (event) => {console.log(event)},
    "Puissance AC ": (event) => {console.log(event)},
    "Puissance AC L1": (event) => {console.log(event)},
    "Puissance AC L2": (event) => {console.log(event)},
    "Puissance AC L3": (event) => {console.log(event)},
    "Tension AC": (event) => {console.log(event)},
    "Tension AC L1": (event) => {console.log(event)},
    "Tension AC L2": (event) => {console.log(event)},
    "Tension AC L3": (event) => {console.log(event)},
    "Courant AC": (event) => {console.log(event)},
    "Courant AC L1": (event) => {console.log(event)},
    "Courant AC L2": (event) => {console.log(event)},
    "Courant AC L3": (event) => {console.log(event)},
    "Fréquence AC": (event) => {console.log(event)},
    "Fréquence AC L1": (event) => {console.log(event)},
    "Fréquence AC L2": (event) => {console.log(event)},
    "Fréquence AC L3": (event) => {console.log(event)},
    "Facteur de limitation de puissance": (event) => {console.log(event)},
    "Déphasage cos phi": (event) => {console.log(event)},
    "Température": (event) => {console.log(event)},
    "Puissance réactive": (event) => {console.log(event)},
    "Énergie": (event) => {console.log(event)},
}

function requestDataMultiChart(premiereFois=false) {
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

    request("POST", "/soe/site/getDataFromBdd/", {"start": start, "end": end}).then(data => {
        creerMultiChart(data, start, end)
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

function creerMultiChart(data, start, end) {
    let onduleursData = repartirDonneesParOnudleurs(data)
    creerInputs(onduleursData)

    // update l'abscice donc le temps pck cette fonction est appellée à chaque changement de delta temps

    // resolve les inputs qui sont checkés pour qu'ils se raclculent

    let chart = Chart.getChart("canvasMultiChart")
    if (!chart) {
        let canvasMultiChart = document.getElementById("canvasMultiChart")
        new Chart(canvasMultiChart, {
            data: {
                datasets: [{
                    type: 'bar',
                    label: 'Bar Dataset',
                    data: []
                }],
                labels: []
            },
            options: {
                plugins: {
                    legend: {
                        display: false,
                    }
                }
            }
        })
    } else {
        chart.update()
    }
}