var file = document.getElementById("id_image");
file.onchange = function(){
    if(file.files.length > 0)
    {
      document.getElementById('filename').innerHTML = file.files[0].name;
    }
};