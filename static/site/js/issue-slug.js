function getSelectedOption(sel) {
    var opt;
    for ( var i = 0, len = sel.options.length; i < len; i++ ) {
        opt = sel.options[i];
        if ( opt.selected === true ) {
            break;
        }
    }
    return opt;
}

document.getElementById("id_series").onclick = function() {
    var e = document.getElementById("id_slug");
    var sel = document.getElementById("id_series");
    var seriesName = getSelectedOption(sel);
    var issueNumber = document.getElementById("id_number").value;
    var res = seriesName.text + " " + issueNumber;
    if (!e._changed) { e.value = URLify(res, 255, false); }
}

document.getElementById("id_number").onkeyup = function() {
    var e = document.getElementById("id_slug");
    var sel = document.getElementById("id_series");
    var seriesName = getSelectedOption(sel);
    var issueNumber = document.getElementById("id_number").value;
    var res = seriesName.text + " " + issueNumber;
    if (!e._changed) { e.value = URLify(res, 255, false); }
}