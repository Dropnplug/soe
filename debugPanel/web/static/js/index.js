function createTab() {
    let tableau = document.getElementsByClassName("tab")[0]
    let models = JSON.parse(this.response)
    console.log(models)
    buildTab(tableau, models)
}

function buildTab(elemParent, models, chemin=[]) {
    if (models.constructor === Array) {
        // group
        for (let i in models) {
            if (models[i].constructor === Object && checkObjectKeys(["Content","ID","Name"], models[i])) {
                // model
                // on rentre dans un model donc le chemin est reset
                chemin=[]
                let elemEnfant = document.createElement("details")
                elemEnfant.classList.add("model")
                let summary = document.createElement("summary")
                summary.innerHTML = "[" + models[i]["ID"] + "] " + models[i]["Name"]
                elemEnfant.appendChild(summary)
                elemParent.appendChild(elemEnfant)
                chemin.push("" + models[i]["ID"])
                buildTab(elemEnfant, models[i]["Content"], chemin)
            } else {
                // curve
                let elemEnfant = document.createElement("details")
                let div = document.createElement("div")
                let summary = document.createElement("summary")
                summary.innerHTML = i
                div.classList.add("group", "point")
                div.appendChild(elemEnfant)
                elemEnfant.appendChild(summary)
                elemParent.appendChild(div)
                chemin.push(i)
                buildTab(elemEnfant, models[i], chemin)
            }
        }
    } else if (models.constructor === Object){
        // point
        for (let [key, value] of Object.entries(models)) {
            if (checkObjectKeys(["name", "value"], value)){
                // l'element est un point
                // il faut inclure joliement la description et un champ pour écrire la value si on peut avec un bouton submit
                if (typeof value["value"] == "number"){
                    if (value["value"] % 1 != 0){
                        value["value"] =  value["value"].toFixed(2)
                    }
                }
                let elem = document.createElement("p")
                elem.classList.add("point")
                let divKey = document.createElement("span")
                divKey.innerHTML = key
                elem.appendChild(divKey)
                if (checkObjectKeys(["label"], value)){
                    elem.innerHTML += " (" + value["label"] + ")"
                }
                if (value["mandatory"] != null){
                    let etoile = document.createElement("span")
                    etoile.innerHTML = "*"
                    etoile.style.color = "red"
                    elem.appendChild(etoile)
                }
                if (value["units"] != null){
                    let unit = document.createElement("span")
                    unit.innerHTML = " " + value["units"]
                    unit.style.color = "grey"
                    elem.appendChild(unit)
                }
                elem.innerHTML += " : "
                let valeurInput = false
                if (checkObjectKeys(["access"], value)){
                    if (value["access"] == "RW"){
                        valeurInput = true
                        let submit = document.createElement("button")
                        
                        if (value["type"].startsWith("enum") == true || value["type"].startsWith("bit") == true && value["symbols"] != null){
                            var input = document.createElement("select")
                            if (value["is_impl"] == false){
                                let optionELem = document.createElement("option")
                                optionELem.innerHTML = "Non implémenté"
                                input.appendChild(optionELem)
                            }
                            for (opt of value["symbols"]){
                                let optionELem = document.createElement("option")
                                if (opt["value"] == value["value"]){
                                    optionELem.setAttribute("selected", "selected")
                                }
                                optionELem.innerText = opt["name"]
                                optionELem.value = opt["value"]
                                input.appendChild(optionELem)
                            }
                        } else if (value["type"].startsWith("uint") == true || value["type"].startsWith("int") == true){
                            var input = document.createElement("input")
                            input.setAttribute("type", "number")
                        } else {
                            var input = document.createElement("input")
                            input.setAttribute("type", "text")
                        }
                        
                        chemin.push(key)
                        submit.setAttribute("onclick", "updateValue(this, " + JSON.stringify(chemin) + ")")
                        submit.innerText = "Valider"
                        chemin.pop()

                        input.setAttribute("value", value["value"])
                        input.classList.add("value")
                        if (value["is_impl"] == false){
                            input.setAttribute("disabled", "disabled")
                            submit.setAttribute("disabled", "disabled")
                        }

                        elem.appendChild(input)
                        elem.appendChild(submit)
                    } else {
                        valeurInput = false
                    }
                } else {
                    valeurInput = false
                }

                if (!valeurInput) {
                    let valeur = document.createElement("span")
                    valeur.classList.add("value")
                    if (value["is_impl"]){
                        if ((value["type"].startsWith("enum") == true || value["type"].startsWith("bit") == true) && value["symbols"] != null){
                            for (opt of value["symbols"]){
                                if (opt["value"] == value["value"]){
                                    valeur.innerText = opt["name"]
                                }
                            }
                        } else {
                            valeur.innerText = value["value"] 
                        }
                    } else {
                        valeur.innerText = "Non implémenté"
                        valeur.style.opacity = 0.5
                    }
                    elem.appendChild(valeur)
                }

                if (checkObjectKeys(["desc"], value)){
                    let desc = document.createElement("span")
                    desc.classList.add("description")
                    elem.innerHTML += " <br> "
                    desc.innerText = value["desc"]
                    elem.appendChild(desc)
                }

                elemParent.appendChild(elem)
            } else {
                // l'element est un group (curve)
                let elemEnfant = document.createElement("details")
                let summary = document.createElement("summary")
                let div = document.createElement("div")
                summary.innerHTML = key
                div.classList.add("group", "point")
                div.appendChild(elemEnfant)
                elemEnfant.appendChild(summary)
                elemParent.appendChild(div)
                chemin.push(key)
                buildTab(elemEnfant, value, chemin)
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

function updateValue(elem, pointRoute){
    elem.disabled = true
    let req = new XMLHttpRequest();
    req.open("POST", "/setPoint");
    let data = JSON.stringify({"pointRoute": pointRoute, "val": elem.previousSibling.value})
    req.boutonSubmit = elem
    req.addEventListener("load", notifyAction);
    req.send(data);
}

function notifyAction(event) {
    if (event.currentTarget.boutonSubmit.nextElementSibling.classList.contains("notifMaj")){
        event.currentTarget.boutonSubmit.nextElementSibling.remove()
    }
    let notif = document.createElement("span")
    notif.classList.add("notifMaj")
    if (this.status == 200){
        content = "Succès, la valeur a été mise à jour"
        color = "green"
    } else {
        content = "Erreur" + " " + this.status
        color = "red"
    }
    notif.style.color = color
    notif.innerText = content
    event.currentTarget.boutonSubmit.disabled = false
    event.currentTarget.boutonSubmit.parentElement.insertBefore(notif, event.currentTarget.boutonSubmit.nextSibling)
    setTimeout(function() {
        notif.remove()
    }, 10000);
}

addEventListener("DOMContentLoaded", requestModel)