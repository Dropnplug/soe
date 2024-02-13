function requestDataMultiChart() {
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
        // start = inputDateDebut.valueAsNumber
    }
    if (inputDateFin.valueAsDate) {
        inputDateFin.valueAsDate.setDate(inputDateFin.valueAsDate.getDate()+1)
        end = inputDateFin.valueAsDate.setHours(0, 0, 0, 0)
        // end = inputDateFin.valueAsNumber
    }

    // on retire les millisecondes
    start = Math.floor(start / 1000)
    end = Math.floor(end / 1000)

    request("POST", "/soe/site/getDataFromBdd/", {"start": start, "end": end}).then(data => {
        creerMultiChart(data, start, end)
    })
}

function creerMultiChart(data, start, end) {
    console.log(data, start, end)
    
}

function prout(params) {
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