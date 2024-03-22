const tablePas = {
    heure: 3600,
    jour: 24 * 3600,
    mois: 24 * 3600 * 31,
    annee: 24 * 3600 * 31 * 12
}

const couleurAxePrimaire = "#0000ff"
const couleurAxePrimaireClaire = "#84abf4"
const couleurAxeSecondaire = "#027502"
const couleurAxeSecondaireClaire = "#aff7bd"

// variable donnant l'état des différents inputs
var checkboxChecked = []
var checkboxMasterUnchecked = []
var detailsOpen = []

function calculerMoyenneParIndice(objetListes) {
    // fonction qui prend une object contenant des listes de tailles différente et qui pour chaque indice de chaque listes fait une moyenne
    /* sous la forme {
        [1, 2, 3],
        [4, 2, 3, 5],
        ...
    }*/
    let moyenneParIndice = []
    let sommeParInd = []
    for (let liste in objetListes) {
        for (let i in objetListes[liste]) {
            if (moyenneParIndice[i] == undefined) {
                moyenneParIndice[i] = 0
                sommeParInd[i] = 0
            }
            moyenneParIndice[i] += objetListes[liste][i]
            sommeParInd[i]++
        }
    }
    moyenneParIndice.forEach((val, ind) => {
        moyenneParIndice[ind] = val/sommeParInd[ind]
    })
    // retourne une liste de valeur moyenne
    return moyenneParIndice;
}

function calcMoyenne(data, start, pas, calculSpecifiqueAlaDonnee) {
    // fonction qui parcours toutes les données remonter par la route /soe/site/getDataFromBdd/ et qui les répartis en fonction du PAS dans une liste ou chaque indice est réprésenter par un PAS (ex : PAS = jour, un indice = une journée)
    let donnees = []
    let debut = new Date(start*1000)
    let indCol = 0
    let res = {}
    for (let macOnduleur in data) {
        let indColInit = false
        indCol = 0
        let dateAvant = undefined
        let dateActuelle = undefined
        let reverseData = Object.keys(data[macOnduleur]).reverse()
        donnees = []
        for (let indice in reverseData) {
            if (dateAvant == undefined) {
                dateAvant = debut
            }
            dateActuelle = new Date(data[macOnduleur][reverseData[indice]]["time"])
            // premier tour de boucle init de l'indice en fonction du pas
            if (indCol == 0) {
                indColInit = true
                indCol += getPasDifferenceEntreDate(dateAvant, dateActuelle, pas)
            }
            if (donnees[indCol] == undefined) {
                donnees[indCol] = {}
                donnees[indCol].valeur = 0
                donnees[indCol].somme = 0
            }

            // fonction passée en paramètre qui fait une opération différente en fonction de chaque type de valeur
            calculSpecifiqueAlaDonnee(data, macOnduleur, reverseData, indice, donnees, indCol)
            donnees[indCol].somme += 1
            // console.log(indCol)
            
            let difference = getPasDifferenceEntreDate(dateAvant, dateActuelle, pas)
            
            // si il ya une différence c'est qu'il faut changer le indcol
            if (difference != 0) {
                if (donnees[indCol].valeur != undefined) {
                    // on calcul la moyenne pour cet indcol
                    donnees[indCol].valeur = parseFloat((donnees[indCol].valeur/donnees[indCol].somme).toFixed(2))
                }
                donnees[indCol].somme = 0
                if (!indColInit) {
                    // on change le indcol en lui ajoutant le nombre de col de différecnce entre la date actuelle et la date d'avant
                    indCol += difference
                }
            }
            indColInit = false
            dateAvant = new Date(data[macOnduleur][reverseData[indice]]["time"])
        }
        if (donnees[indCol].valeur != undefined) {
            donnees[indCol].somme += 1
            // il faut faire cette opération suplémentaire car la boucle fort va systématiquement omettre le dernier élément
            donnees[indCol].valeur = parseFloat((donnees[indCol].valeur/donnees[indCol].somme).toFixed(2))
        }
        // rangement de la liste de valeur dans un object contenant toutes les listes de valeurs moyenne de tous les sous apareil (ex: de toutes les string si on veut les données d'un onduleur)
        res[macOnduleur] = []
        for (let i in donnees) {
            res[macOnduleur][i] = donnees[i].valeur
        }
    }
    return res
}

function moyenneString(data, macOnduleur, reverseData, indice, nomDonnees) {
    let somme = 0
    let valeur = 0
    let moy = 0
    // moyenne des string et on ingore les string à 0 pour qu'elles n'influencent pas la moyenne
    for (let pvString in data[macOnduleur][reverseData[indice]][nomDonnees]) {
        valeur += Number(data[macOnduleur][reverseData[indice]][nomDonnees][pvString])
        if (Number(data[macOnduleur][reverseData[indice]][nomDonnees][pvString]) != 0) {
            somme++
        }
    }
    if (somme != 0) {
        moy += valeur/somme
    } else { // si ya pas de somme ça veut dire que la string est vide et donc on la compte pas
        moy += 0
    }
    return moy
}

// TODO les fonctions des data doivent toutes retournée une liste de données affichable par le chart avec le bon interval de temps
const listeData = {
    "Puissance DC": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            // fonction de calcul spécifique de la donnée
            donnees[indCol].valeur += moyenneString(data, macOnduleur, reverseData, indice, "puissance_dc")
        })

        // toutes les infos spécifique à un dataset pour une données
        datasetAajouter = {
                // il faut un liste de données et non un object contenant des listes
                data: calculerMoyenneParIndice(res),
                unit:"W",
                id: checkboxId,
                label: "Puissance DC" + " " + label
            }
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Tension DC": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += moyenneString(data, macOnduleur, reverseData, indice, "tension_dc")
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"V",
            id: checkboxId,
            label: "Tension DC" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Courant DC": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += moyenneString(data, macOnduleur, reverseData, indice, "courant_dc")
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"A",
            id: checkboxId,
            label: "Courant DC" + " " + label
        }
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Puissance AC ": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["puissance_ac"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"W",
            id: checkboxId,
            label: "Puissance AC" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Puissance AC L1": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["puissance_ac_par_phase"][0])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"W",
            id: checkboxId,
            label: "Puissance AC L1" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Puissance AC L2": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["puissance_ac_par_phase"][1])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"W",
            id: checkboxId,
            label: "Puissance AC L2" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Puissance AC L3": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["puissance_ac_par_phase"][2])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"W",
            id: checkboxId,
            label: "Puissance AC L3" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Tension AC": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["tension_ac"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"V",
            id: checkboxId,
            label: "Tension AC" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Tension AC L1": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["tension_ac_par_phase"][0])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"V",
            id: checkboxId,
            label: "Tension AC L1" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Tension AC L2": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["tension_ac_par_phase"][1])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"V",
            id: checkboxId,
            label: "Tension AC L2" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Tension AC L3": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["tension_ac_par_phase"][2])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"V",
            id: checkboxId,
            label: "Tension AC L3" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Courant AC": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["courant_ac"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"A",
            id: checkboxId,
            label: "Courant AC" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Courant AC L1": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["courant_ac_par_phase"][0])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"A",
            id: checkboxId,
            label: "Courant AC L1" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Courant AC L2": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["courant_ac_par_phase"][1])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"A",
            id: checkboxId,
            label: "Courant AC L2" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Courant AC L3": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["courant_ac_par_phase"][2])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"A",
            id: checkboxId,
            label: "Courant AC L3" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Fréquence AC": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["frequence_ac"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"Hz",
            id: checkboxId,
            label: "Fréquence AC" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Fréquence AC L1": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["frequence_ac_par_phase"][0])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"Hz",
            id: checkboxId,
            label: "Fréquence AC L1" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Fréquence AC L2": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["frequence_ac_par_phase"][1])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"Hz",
            id: checkboxId,
            label: "Fréquence AC L1" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Fréquence AC L3": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["frequence_ac_par_phase"][2])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"Hz",
            id: checkboxId,
            label: "Fréquence AC L1" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Facteur de limitation de puissance": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["facteur_de_limitation_de_puissance"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"",
            id: checkboxId,
            label: "Facteur de limitation de puissance" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Déphasage cos phi": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["dephasage_cos_phi"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"",
            id: checkboxId,
            label: "Déphasage cos phi" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Température": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["temperature"])
        })

        datasetAajouter = {
                data: calculerMoyenneParIndice(res),
                unit:"°C",
                id: checkboxId,
                label: "Température" + " " + label
            }
        
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Puissance réactive": (data, start, end, pas, checkboxId, label) => {
        let res = calcMoyenne(data, start, pas, (data, macOnduleur, reverseData, indice, donnees, indCol) => {
            donnees[indCol].valeur += Number(data[macOnduleur][reverseData[indice]]["puissance_reactive"])
        })

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"",
            id: checkboxId,
            label: "Puissance réactive" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    },
    "Énergie": (data, start, end, pas, checkboxId, label) => {
        let donnees = []
        let debut = new Date(start*1000)
        let indCol = 0
        let res = {}
        for (let macOnduleur in data) {
            let indColInit = false
            indCol = 0
            let dateAvant = undefined
            let dateActuelle = undefined
            let reverseData = Object.keys(data[macOnduleur]).reverse()
            let premiereValeurDuPas = undefined
            let donneeDuDernierPas = 0
            donnees = []
            for (let indice in reverseData) {
                if (premiereValeurDuPas === undefined) {
                    premiereValeurDuPas = Number(data[macOnduleur][reverseData[indice]]["energie_totale"])
                }
                
                if (dateAvant == undefined) {
                    dateAvant = debut
                }
                dateActuelle = new Date(data[macOnduleur][reverseData[indice]]["time"])
                // premier tour de boucle init de l'indice en fonction du pas
                if (indCol == 0) {
                    indColInit = true
                    indCol += getPasDifferenceEntreDate(dateAvant, dateActuelle, pas)
                }
                if (donnees[indCol] == undefined) {
                    donnees[indCol] = {}
                    donnees[indCol].valeur = 0
                    donnees[indCol].somme = 0
                }

                // fonction passée en paramètre qui fait une opération différente en fonction de chaque type de valeur
                calculSpecifiqueAlaDonnee(data, macOnduleur, reverseData, indice, donnees, indCol)
                donnees[indCol].somme += 1
                
                let difference = getPasDifferenceEntreDate(dateAvant, dateActuelle, pas)
                
                // si il ya une différence c'est qu'il faut changer le indcol
                if (difference != 0) {
                    if (donnees[indCol].valeur != undefined) {
                        // on calcul la moyenne pour cet indcol
                        donnees[indCol].valeur = parseFloat((donnees[indCol].valeur/donnees[indCol].somme).toFixed(2))
                    }
                    donnees[indCol].somme = 0
                    if (!indColInit) {
                        // on change le indcol en lui ajoutant le nombre de col de différecnce entre la date actuelle et la date d'avant
                        indCol += difference
                    }
                }
                indColInit = false
                dateAvant = new Date(data[macOnduleur][reverseData[indice]]["time"])
            }
            if (donnees[indCol].valeur != undefined) {
                donnees[indCol].somme += 1
                // il faut faire cette opération suplémentaire car la boucle fort va systématiquement omettre le dernier élément
                donnees[indCol].valeur = parseFloat((donnees[indCol].valeur/donnees[indCol].somme).toFixed(2))
            }
            // rangement de la liste de valeur dans un object contenant toutes les listes de valeurs moyenne de tous les sous apareil (ex: de toutes les string si on veut les données d'un onduleur)
            res[macOnduleur] = []
            for (let i in donnees) {
                res[macOnduleur][i] = donnees[i].valeur
            }
        }

        datasetAajouter = {
            data: calculerMoyenneParIndice(res),
            unit:"",
            id: checkboxId,
            label: "Puissance réactive" + " " + label
        }
    
        initOrUpdateGraph("canvasMultiChart", undefined, datasetAajouter)
    }
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
            difference = dateActuelle.getHours() - dateAvant.getHours()
            // dateAvant = dateAvant.getTime() / 1000
            // dateActuelle = dateActuelle.getTime() / 1000
            // difference = Math.round(Math.abs(dateActuelle - dateAvant) / 3600)
            break
        case "jour":
            dateAvant = dateAvant.getTime() / 1000
            dateActuelle = dateActuelle.getTime() / 1000
            difference = Math.round(Math.abs((dateAvant - dateActuelle) / tablePas.jour))
            break
        case "mois":
            difference = dateActuelle.getMonth() - dateAvant.getMonth() + (12 * (dateActuelle.getFullYear() - dateAvant.getFullYear()))
            break
        case "annee":
            difference = dateActuelle.getFullYear() - dateAvant.getFullYear()
            break
    
        default:
            break
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
    // fonction qui active ou désactive toutes les checkbox d'un detail
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

function creerDetail(elemParent, nomDetail, listeEtatCheckbox, typeAppareil) {
    // fonction qui créer un elem detail dans un elemparent
    let detail = document.createElement("details")
    let summary = document.createElement("summary")
    let label = document.createElement("label")
    let checkbox = document.createElement("input")
    label.setAttribute("for", nomDetail)
    label.innerText = nomDetail
    detail.id = "detail_"+nomDetail
    detail.ontoggle = () => {
        // on veut se souvenir de quelles sont les checkboc cochées ou non
        if (detail.open && detailsOpen.indexOf(detail.id) == -1) {
            detailsOpen.push(detail.id)
        } else if (detail.open == false) {
            let index = detailsOpen.indexOf(detail.id)
            if (index > -1) {
                detailsOpen.splice(index, 1)
            }
        }
    }
    checkbox.onchange = () => checkCheckbox(detail)
    checkbox.id = nomDetail
    checkbox.style.transform = "scale(1.3)"
    checkbox.type = "checkbox"
    checkbox.checked = true
    let checkboxMaster = checkbox
    summary.innerText = typeAppareil
    summary.style.fontSize = "1.2em"

    label.appendChild(checkbox)
    summary.appendChild(label)
    detail.appendChild(summary)
    elemParent.appendChild(detail)

    if (listeEtatCheckbox.includes(checkboxMaster.id)) {
        checkboxMaster.click()
    }
    if (detailsOpen.includes(detail.id)) {
        detail.open = true
    }

    return detail
}

function creerCheckbox(elemParent, data, idAppareil, onduleursData, nom, start, end, pas) {
    // fonction qui créer une checkbox
    let checkbox = document.createElement("input")
    let label = document.createElement("label")
    // TODO trouver le nom de l'onduleur
    label.innerText = data
    label.setAttribute("for", idAppareil+data)
    checkbox.type = "checkbox"
    checkbox.name = data
    checkbox.id = idAppareil+data
    checkbox.onchange = () => {
        if (checkbox.checked) {
            if (!checkboxChecked.includes(checkbox.id)) {
                checkboxChecked.push(checkbox.id)
            }
            // appelle à la bonne fonction grâce au nom de la donnée
            listeData[data](onduleursData, start, end, pas, checkbox.id, nom)
        } else {
            supprimerDatasetsFromChart("canvasMultiChart", checkbox.id)
            let index = checkboxChecked.indexOf(checkbox.id)
            if (index > -1) {
                checkboxChecked.splice(index, 1)
            }
        }
    }
    label.appendChild(checkbox)
    elemParent.appendChild(label)
    if (checkboxChecked.includes(checkbox.id)) {
        checkbox.click()
    }
}

function creerInputs(onduleursData, start, end, pas) {
    let spanInputs = document.getElementsByClassName("inputsData")[0]
    // on supprime tout
    spanInputs.innerHTML = ""
    // TODO trouver le nom du site
    const nomSite = "Site"
    
    // le site
    if (Object.keys(onduleursData).length != 0) {
        let detail = creerDetail(spanInputs, nomSite, checkboxMasterUnchecked, nomSite)
        // les inputs de données du site
        for (let data in listeData) {
            creerCheckbox(detail, data, "", onduleursData, nomSite, start, end, pas)
        }
    } else {
        let h2 = document.createElement("h2")
        h2.innerText = "Pas de données pour la période sélectionnée."
        spanInputs.appendChild(h2)
    }

    // les onduleurs
    for (let macOnduleur in onduleursData) {
        let detail = creerDetail(spanInputs, macOnduleur, checkboxMasterUnchecked, "Onduleur")
        // un onduleur
        for (let data in listeData) {
            let object = {}
            object[macOnduleur] = onduleursData[macOnduleur]
            creerCheckbox(detail, data, macOnduleur+"_", object, macOnduleur, start, end, pas)
        }
        // TODO ajouter les string de panneau
    }
}

const newShade = (hexColor, magnitude) => {
    // fonction qui prend une couleur et la transforme dans une couleur un peut plus rouge
    // merci stackoverflow
    hexColor = hexColor.replace(`#`, ``)
    if (hexColor.length === 6) {
        const decimalColor = parseInt(hexColor, 16)
        let r = (decimalColor >> 16) + magnitude
        r > 255 && (r = 255)
        r < 0 && (r = 0)
        let g = (decimalColor & 0x0000ff)
        g > 255 && (g = 255)
        g < 0 && (g = 0)
        let b = ((decimalColor >> 8) & 0x00ff)
        b > 255 && (b = 255)
        b < 0 && (b = 0)
        return `#${(g | (b << 8) | (r << 16)).toString(16)}`
    } else {
        return hexColor
    }
}

function addOrRemoveAxes(nomCanvas) {
    // fonction qui regarde quels sont les unitées présentent dans le graph et suprime ou ajoute des axes en fonction de ça
    let chart = Chart.getChart(nomCanvas)
    let primaire = undefined
    let secondaire = undefined
    
    for (let unit in chart.data.units) {
        if (chart.data.units[unit].yAxisID == "Primaire") {
            primaire = unit
        }
        if (chart.data.units[unit].yAxisID == "Secondaire") {
            secondaire = unit
        }
    }

    if (primaire || !secondaire) {
        chart.options.scales["Primaire"] = {
            type: 'linear',
            position: 'left',
            title: {
                display: true,
                text: primaire,
                color: couleurAxePrimaire
            },
            ticks: { beginAtZero: true, color: couleurAxePrimaire },
            grid: {
                color: function(context) {
                    return couleurAxePrimaireClaire
                },
            },
        }
    } else if (secondaire) {
        delete chart.options.scales["Primaire"]
    }

    if (secondaire) {
        chart.options.scales["Secondaire"] = {
            type: 'linear',
            position: 'right',
            title: {
                display: true,
                text: secondaire,
                color: couleurAxeSecondaire
            },
            ticks: { beginAtZero: true, color: couleurAxeSecondaire },
            grid: {
                color: function(context) {
                    return couleurAxeSecondaireClaire
                }
            }
        }
    } else {
        delete chart.options.scales["Secondaire"]
    }

    chart.update()
}

function supprimerDatasetsFromChart(nomCanvas, idDataset) {
    let chart = Chart.getChart(nomCanvas)
    let trouve = false
    let i = 0
    while (!trouve && i < chart.data.datasets.length) {
        if (chart.data.datasets[i].id == idDataset) {
            let nbDonnees = compterNombreDonneePourUnite(chart.data.datasets[i].unit, nomCanvas)
            if (nbDonnees == 1) {
                delete chart.data.units[chart.data.datasets[i].unit]
            }
            chart.data.datasets.splice(i, 1)
            trouve = true
        }
        i += 1
    }

    if (trouve) {
        addOrRemoveAxes(nomCanvas)
        chart.update()
    }
    return trouve
}

function supprimerTousLesDatasets(nomCanvas) {
    let chart = Chart.getChart(nomCanvas)
    if (chart) {
        chart.data.datasets = []
        chart.data.units = {}
        addOrRemoveAxes(nomCanvas)
        chart.update()
    }
}

function compterNombreDonneePourUnite(unite, nomCanvas) {
    let chart = Chart.getChart(nomCanvas)
    let somme = 0
    if (chart) {
        for (let dataset in chart.data.datasets) {
            if (chart.data.datasets[dataset].unit == unite) {
                somme += 1
            }
        }
    }
    return somme
}

function initOrUpdateGraph(nomCanvas, tableauAbscisse=undefined, datasetAajouter) {
    let chart = Chart.getChart(nomCanvas)
    if (!chart) {
        // création du graph
        let canvasMultiChart = document.getElementById(nomCanvas)
        let chartNew = new Chart(canvasMultiChart, {
            data: {
                units: {},
                datasets: [],
                labels: tableauAbscisse
            },
            options: {
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                responsive: true,
                tooltips: {
                    axis: 'x'
                },
                scales: {
                    Primaire: {
                        type: 'linear',
                        position: 'left',
                        ticks: { beginAtZero: true, color: 'blue' },
                        grid: {
                            color: function(context) {
                                return '#C8DBFE'
                            }
                        }
                    }
                }
            },
            plugins: [{
                afterDraw: (chart) => {
                    if (chart.tooltip?._active?.length) {
                        let x = chart.tooltip._active[0].element.x
                        let yAxis = undefined
                        if (chart.scales.Primaire) {
                            yAxis = chart.scales.Primaire
                        } else if (chart.scales.Secondaire) {
                            yAxis = chart.scales.Secondaire
                        }
                        let ctx = chart.ctx
                        ctx.save()
                        ctx.beginPath()
                        ctx.moveTo(x, yAxis.top)
                        ctx.lineTo(x, yAxis.bottom)
                        ctx.lineWidth = 1
                        ctx.strokeStyle = '#ff0000'
                        ctx.globalCompositeOperation = "destination-over"
                        ctx.stroke()
                        ctx.restore()
                    }
                }
            }]
        })
    } else {
        // modifier les data, labels, couleur, type axes
        if (tableauAbscisse != undefined) {
            chart.data.labels = tableauAbscisse
        }
        if (Object.keys(datasetAajouter).length == 0) {
            chart.update()
            return
        }
        supprimerDatasetsFromChart(nomCanvas, datasetAajouter.id)
        // il y a pas déjà un dataset avec l'unité du dataset à ajouter
        if (chart.data.units[datasetAajouter.unit] == undefined) {
            if (Object.keys(chart.data.units).length == 0 || (Object.keys(chart.data.units).length == 1 && chart.data.units[Object.keys(chart.data.units)[0]].yAxisID == "Secondaire")) {
                datasetAajouter.yAxisID = "Primaire"
                datasetAajouter.backgroundColor = couleurAxePrimaireClaire
                datasetAajouter.borderColor = couleurAxePrimaire
            } else if (Object.keys(chart.data.units).length == 1) {
                datasetAajouter.yAxisID = "Secondaire"
                datasetAajouter.backgroundColor = couleurAxeSecondaireClaire
                datasetAajouter.borderColor = couleurAxeSecondaire
            } else {
                // TODO ajouter un popup de msg d'erreur
                if (document.getElementById(datasetAajouter.id)) {
                    document.getElementById(datasetAajouter.id).click()
                }
                console.log("on peut pas ajouter de donnée le graphique est déjà plein")
                chart.update()
                return
            }
            chart.data.units[datasetAajouter.unit] = {
                yAxisID: datasetAajouter.yAxisID,
                backgroundColor: datasetAajouter.backgroundColor,
                borderColor: datasetAajouter.borderColor,
            }
        } else {
            datasetAajouter.yAxisID = chart.data.units[datasetAajouter.unit].yAxisID
            datasetAajouter.backgroundColor = newShade(chart.data.units[datasetAajouter.unit].backgroundColor, (compterNombreDonneePourUnite(datasetAajouter.unit, nomCanvas)*40)%200)
            datasetAajouter.borderColor = newShade(chart.data.units[datasetAajouter.unit].borderColor, (compterNombreDonneePourUnite(datasetAajouter.unit, nomCanvas)*60)%200)
        }
        
        chart.data.units[datasetAajouter.unit].yAxisID = datasetAajouter.yAxisID
        
        datasetAajouter.type = "line"
        datasetAajouter.cubicInterpolationMode = "monotone"
        chart.data.datasets.push(datasetAajouter)
        chart.update()
        addOrRemoveAxes(nomCanvas)
        // centrage des donnée sur l'axe des abscice
        if (chart.options.scales.x.offset == false) {
            chart.options.scales.x.offset = true
            chart.update()
        }
    }
}

function genAbscisse(start, end) {
    // choix du pas en fonction de la taille de l'interval et de l'input user 
    let intervalTimeStamp = end - start
    let maxCol = 62
    let pas = ""
    let inputPas = document.getElementById("pas")
    if (intervalTimeStamp / tablePas[inputPas.value] > maxCol) {
        // TODO affiché une popup d'erreur
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
    // génération du tableau de date à mettre en abscice du graphique en fonction du pas
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

    supprimerTousLesDatasets("canvasMultiChart")
    
    // création et mise à jour des checkbox d'affichage de données
    creerInputs(onduleursData, start, end, pas)
    
    let listeDatasets = {}
    // initialistaion ou mise à jour du chart avec les nouveaux datasets et interval de temps
    initOrUpdateGraph("canvasMultiChart", tableauAbscisse=tableauAbscisse, listeDatasets)
}