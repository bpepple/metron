document.getElementById("id_name").onkeyup = function() {
    var e = document.getElementById("id_slug");
    var seriesName = document.getElementById("id_name").value;
    var seriesYear = document.getElementById("id_year_began").value;
    var res = seriesName + ' ' + seriesYear;
    if (!e._changed) { e.value = URLify(res, 255, false); }
}

document.getElementById("id_year_began").onkeyup = function() {
    var e = document.getElementById("id_slug");
    var seriesName = document.getElementById("id_name").value;
    var seriesYear = document.getElementById("id_year_began").value;
    var res = seriesName + ' ' + seriesYear;
    if (!e._changed) { e.value = URLify(res, 255, false); }
}