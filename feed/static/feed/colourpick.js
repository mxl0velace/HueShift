var colourPicker = new iro.ColorPicker('#picker', {
    layout: [
        {
            component: iro.ui.Wheel
        }
    ],
    width: 200
});

function sendColour(){
    target = document.getElementById("picker").parentNode.querySelector('.post_body');
    var form = document.getElementById("hiddenForm");
    form.pid.value = document.getElementById("picker").parentNode.dataset.postid;
    form.hue.value = colourPicker.color.hsl.h;
    var request = new XMLHttpRequest();
    request.open('POST', '/', true);
    request.send(new FormData(form));
    request.onload = function (){
        console.log(request.response);
        target.style.backgroundColor = "hsl(" + request.responseText + ",100%,50%)";
    }
}

colourPicker.on("input:end", sendColour);

function paintClick(button){
    var colourParent = document.getElementById("picker");
    button.closest('.post').appendChild(colourParent);
    colourPicker.reset();
    colourParent.style.display = "block";
}