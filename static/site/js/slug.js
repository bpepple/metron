document.getElementById("id_name").onkeyup = function() {
    var e = document.getElementById("id_slug");
    if (!e._changed) { e.value = URLify(document.getElementById("id_name").value, 255, false); }
}