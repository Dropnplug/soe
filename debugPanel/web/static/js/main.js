function createTab() {
    let tableau = document.getElementsByClassName("tab")[0]
    let models = JSON.parse(this.response)
    console.log(models)
    buildTab(tableau, models)
}

function buildTab(elemParent, models) {
    if (models.constructor === Array) {
        for (let i in models) {
            if (models[i].constructor === Object && checkObjectKeys(["Content","ID","Name"], models[i])) {
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                summary.innerHTML = models[i]["ID"]
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                buildTab(elemEnfant, models[i]["Content"])
            } else {
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                summary.innerHTML = i
                elemEnfant.style.paddingLeft = "5em"
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                buildTab(elemEnfant, models[i], 1)
            }
        }
    } else if (models.constructor === Object){
        for (let [key, value] of Object.entries(models)) {
            if (checkObjectKeys(["name", "value"], value)){
                // il faut inclure joliement la description et un champ pour écrire la value si on peut avec un bouton submit
                let elem = document.createElement("p")
                elem.style.paddingLeft = "5em"
                let divKey = document.createElement("span")
                divKey.innerHTML = key
                elem.appendChild(divKey)
                if (checkObjectKeys(["label"], value)){
                    elem.innerHTML += " (" + value["label"] + ") : "
                } else {
                    elem.innerHTML += " : "
                }
                if (checkObjectKeys(["access"], value)){
                    if (value["access"] == "RW"){
                        let champ = document.createElement("input")
                        let submit = document.createElement("button")

                        submit.setAttribute("onclick", "updateValue(this)")
                        submit.innerText = "Valider"

                        champ.setAttribute("type", "text")
                        champ.setAttribute("value", value["value"])
                        if (value["value"] == null){
                            champ.setAttribute("disabled", "disabled")
                            submit.setAttribute("disabled", "disabled")
                        }

                        elem.appendChild(champ)
                        elem.appendChild(submit)
                    } else {
                        elem.innerHTML += value["value"]
                    }
                } else {
                    elem.innerHTML += value["value"]
                }

                if (checkObjectKeys(["desc"], value)){
                    elem.innerHTML += " <br> " + value["desc"]
                }

                elemParent.appendChild(elem)
            } else {
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                summary.innerHTML = key
                elemEnfant.style.paddingLeft = "5em"
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                buildTab(elemEnfant, value)
            }
        }
    }
}

// reagrde si une liste de clef est contenu dans un objet
function checkObjectKeys(listeKeys, obj){
    for (let elem of listeKeys){
        if (!Object.keys(obj).includes(elem)){
            return false
        }
    }
    return true
}

function requestModel() {
    let req = new XMLHttpRequest();
    req.addEventListener("load", createTab);
    req.open("GET", "/getModels");
    req.send();
}

function updateValue(butSubmitClicked){
    let pointRoute = []
    let elem = butSubmitClicked.parentElement
    while (elem.className != "tab") {
        pointRoute.push(elem.children[0].innerHTML)
        elem = elem.parentElement
    }
    let val = butSubmitClicked.previousSibling.value 
    pointRoute = pointRoute.reverse()

    let req = new XMLHttpRequest();
    req.open("POST", "/setPoint");
    let data = "pointRoute=" + pointRoute + "&val=" + val
    req.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    req.send(data);
    // req.send();
}

addEventListener("DOMContentLoaded", requestModel)