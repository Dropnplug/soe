function enable_hotspot() {
    request("GET", "/dropnwifi/config/enable_hotspot/").then(data => {})
}

function disable_hotspot() {
    request("GET", "/dropnwifi/config/disable_hotspot/").then(data => {})
}
