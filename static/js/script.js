var booklet_path ='';
function preview(){
    window.open('/static/pdf/booklet.pdf');
    $("#upload_form").load("/static/drag&drop.html");
}
function dragover_handler(ev) {
      ev.preventDefault();
      ev.dataTransfer.dropEffect = "move";
}
function drop_handler(ev) {
    ev.preventDefault();
    var file = ev.dataTransfer.items[0].getAsFile();
    console.log(file.name);
    booklet_path = '/static/output/booklet_'+file.name;
     
    var data = new FormData();
    data.append('file', file);

    fetch('/upload',{method:'POST', body:data}).then(
      response => {}
    ).then(
        json => {}
    ).catch(
        error => console.error(error)
    );

    $("#upload_form").load("/static/button.html");
}

window.onbeforeunload = function (event){
    event.preventDefault();
    fetch('/delete').then(response => {})
                    .then(json => {})
                    .catch(error => console.error(error));
}