let filename = "";

function ElementWithAttList(element_name, list){
    let new_element = document.createElement(element_name);
    const length = list.length;
    for(let i = 0; i < length; i++){
        let attribute = list[i];
        new_element.setAttribute(attribute[0],attribute[1]);
    }
    return new_element;
}

function dragover_handler(ev) {
      ev.preventDefault();
      ev.dataTransfer.dropEffect = "move";
}

function drop_handler(ev) {
    ev.preventDefault();
    document.getElementById("message").innerHTML="アップロード中...";


    const file = ev.dataTransfer.items[0].getAsFile();
    filename = file.name;
     
    let data = new FormData();
    data.append('file', file);

    fetch('/upload',{method:'POST', body:data})
    .then(
      response => response.blob()
    ).then(
        blob => {
            //レスポンスが返ってきた後のhtmlを作成 
            
            let url = URL.createObjectURL(blob);//アップロードしたPDFの一枚目のURL

            let EmbedPDF = ElementWithAttList("embed",[
                ["src", url], ["type", "application/pdf"],["width", "100%"],["height","80%"]
            ]);

            let BackButton = ElementWithAttList("a", [
                ["class", "btn btn-light"], 
                ["style", "margin-top:5%;"],
                ["onclick", "back();"]
            ]);
            let BackButton_image = ElementWithAttList("img", [
                ["src", "/static/turnback.png"], 
                ["height", "20"], ["width", "30"]
            ]);
            BackButton.appendChild(BackButton_image);

            let DownloadButton = ElementWithAttList("a", [
                ["class", "btn btn-outline-secondary btn-sm"], 
                ["style", "position:absolute; transform:translate(-50%,0%); left:50%; margin-top:5%; "], 
                ["href", "/static/pdf/booklet_" + filename],
                ["download",""],
                ["onclick", "back();"]
            ]);               
            DownloadButton.appendChild(document.createTextNode("小冊子をダウンロード"));

            let form = document.getElementById("upload_form");
            form.innerHTML = "";
            form.appendChild(EmbedPDF);
            form.appendChild(BackButton);
            form.appendChild(DownloadButton);
        }
        
    ).catch(
        //error => console.error(error);
    );
    
}

function back(){
    $("#upload_form").load("/static/drag&drop.html")
}

function preview(){
    let download_name = new FormData();
    download_name.set('filename', filename);

    let messageForm = ElementWithAttList("div", [["class", "messageForm"]]);
    let message = ElementWithAttList("p", [["style", "font-size:30px; font-weight:300"],["id","message"]]);
    message.appendChild(document.createTextNode("ダウンロード中..."));
    messageForm.appendChild(message);

    let form = document.getElementById("upload_form");
    form.innerHTML = "";
    form.appendChild(messageForm);

    fetch('/download',{method:'POST', body: download_name})
    .then(
        response => response.blob()
    ).then(
        blob => {
            url = URL.createObjectURL(blob);
            window.open(url);
            document.getElementById("message").innerHTML = "PDFをドラッグ&ドロップ";
        }
    )
}

window.onbeforeunload = function (event){
    event.preventDefault();
    let download_name = new FormData();
    download_name.set('filename', filename);

    fetch('/download',{method:'POST', body: download_name})
}