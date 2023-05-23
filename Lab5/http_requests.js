window.post = function(data) {
    return fetch('/api/tests/', {method: "POST", headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
}

window.patch = function(id, data) {
    return fetch('/api/tests/'+id, {method: "PATCH",
    headers: {
        "Content-type": "application/json",
        "accept": "application/json"}, body: JSON.stringify(data)});
}
window.del = function(id, data) {
    return fetch('/api/tests/'+id, {method: "DELETE", headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data)});
}