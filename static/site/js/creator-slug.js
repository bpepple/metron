function toSlug() {
    var e = document.getElementById("id_slug");
    var firstName = document.getElementById("id_first_name").value;
    var lastName = document.getElementById("id_last_name").value;
    var res = firstName + " " + lastName;
    if (!e._changed) { e.value = URLify(res, 255, false); }
  }

  document.getElementById("id_last_name").onkeyup = toSlug;