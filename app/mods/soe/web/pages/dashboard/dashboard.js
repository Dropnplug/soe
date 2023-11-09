request("GET", "/soe/dashboard/data/").then(data => {
    creerAffichageAC(data)
})

function creerAffichageAC(data) {
    console.log(data)
    
}