var colourPicker = new iro.ColorPicker('#picker', {
    layout: [
        {
            component: iro.ui.Wheel
        }
    ],
    width: 200
});

function sendColour(){
    var post = document.getElementById("picker").closest('.post');
    if(post != null){
        target = post.querySelector('.post_body');
        var form = document.getElementById("hiddenForm");
        form.pid.value = post.dataset.postid;
        form.hue.value = colourPicker.color.hsl.h;
        form.action.value = 'shift';
        var request = new XMLHttpRequest();
        request.open('POST', '/', true);
        request.send(new FormData(form));
        request.onload = function (){
            console.log(request.response);
            target.style.backgroundColor = "hsl(" + request.responseText + ",100%,50%)";
        }
    } else{
        window.location.href = "/search?h="+colourPicker.color.hsl.h;
    }
}

colourPicker.on("input:end", sendColour);

function paintClick(button){
    var colourParent = document.getElementById("picker");
    button.closest('.post').querySelector('.post_shift').appendChild(colourParent);
    colourPicker.reset();
    colourParent.style.display = "block";
}

function deletePost(button){
    var form = document.getElementById("hiddenForm");
    form.pid.value = button.closest('.post').dataset.postid;
    form.action.value = 'delete';
    var request = new XMLHttpRequest();
    request.open('POST', '/', true);
    request.send(new FormData(form));
    request.onload = function(){
        if(request.status == 204){
            var post = button.closest('.post');
            var picker = document.getElementById('picker');
            if(picker.closest('.post') == post){
                picker.style.display = "none";
                document.body.appendChild(picker);
            }
            post.classList.add('post_deleted');
            post.addEventListener('transitionend', function(){
                post.remove();
            })
        }
    }

}

var vis = false;

function visClick(event){
    console.log("vissed!");
    vis = !vis;
    var drop = document.getElementById("dropdown-content");
    if(vis){
        drop.style.display = "block";
        var picker = document.getElementById('picker');
        drop.appendChild(picker);
         picker.style.display = "block";
    } else{
        drop.style.display = "none";
    }
}

document.addEventListener("click", (evt) => {
    if(evt.target.closest('#picker') == null){
        if(evt.target.closest('.clickWheel') == null){
            document.getElementById("picker").style.display = "none";
        }
        if(evt.target.closest('.dropWheel') == null){
            vis = false;
            document.getElementById("dropdown-content").style.display = "none";
        }
    }
})

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("dropdown-control").addEventListener("click", visClick, false);
});
