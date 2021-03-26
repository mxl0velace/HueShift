var colourPicker = new iro.ColorPicker('#picker', {
    layout: [
        {
            component: iro.ui.Wheel
        }
    ],
    width: 200
});

function sendColour(){
    console.log(document.getElementById("picker").parentNode.dataset.postid);
    console.log(colourPicker.color.hsl.h);
    var form = document.getElementById("hiddenForm");
    form.pid.value = document.getElementById("picker").parentNode.dataset.postid;
    form.hue.value = colourPicker.color.hsl.h;
    var request = new XMLHttpRequest();
    request.open('POST', '/', true);
    request.send(new FormData(form));
}

colourPicker.on("input:end", sendColour);

function paintClick(button){
    var colourParent = document.getElementById("picker");
    button.parentElement.appendChild(colourParent);
    colourPicker.reset();
    colourParent.style.display = "block";
}
  