function createTab() {
    let tableau = document.getElementsByClassName("tab")[0]
    let models = JSON.parse(this.response)
    console.log(tableau, models)
    buildTab(tableau, models)
}

function buildTab(elemParent, models) {
    if (models.constructor === Array) {
        for (let i in models) {
            if (models[i].constructor === Object && checkObjectKeys(["Content","ID","Name"], models[i])) {
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                summary.innerHTML = "[" + models[i]["ID"] + "] " + models[i]["Name"]
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                buildTab(elemEnfant, models[i]["Content"])
            } else {
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                summary.innerHTML = i
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                buildTab(elemEnfant, models[i])
            }
        }
    } else if (models.constructor === Object){
        for (let [key, value] of Object.entries(models)) {
            if (checkObjectKeys(["name", "value"], value)){
                // il faut inclure joliement la description et un champ pour écrire la value si on peut avec un bouton submit
                let elem = document.createElement("p")
                elem.innerHTML = value["name"] + " : " + value["value"]
                elemParent.appendChild(elem)
            } else {
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                summary.innerHTML = key
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                buildTab(elemEnfant, value)
            }
        }
    }
}

function checkObjectKeys(listeKeys, obj){
    for (let elem of listeKeys){
        if (!Object.keys(obj).includes(elem)){
            return false
        }
    }
    return true
}

function requestModel() {
    const req = new XMLHttpRequest();
    req.addEventListener("load", createTab);
    req.open("GET", "/getModels");
    req.send();
}

addEventListener("DOMContentLoaded", requestModel)