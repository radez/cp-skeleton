$(document).ready(function() {
    // reload when session expires
    setTimeout(function(){
       location = '';
    }, 3601000) // 1 hour 10 seconds
});

function toggledisplay(elementID) {
 (function(style) {
	style.display = style.display === 'none' ? '' : 'none';
 })(document.getElementById(elementID).style);
}

function set_message(data, css_class='alert-success') {
    if (typeof data !== 'string') {
        if ("css_class" in data) { css_class = data['css_class'] };
        message = data['msg'];
    } else {
        message = data;
    };

    let msgDiv = document.createElement("div");
    msgDiv.classList.add('alert');
    msgDiv.classList.add(css_class);
    msgDiv.classList.add('w-50');
    msgDiv.classList.add('mx-auto');
    msgDiv.innerHTML = "<strong>" + message + "</strong>";
    document.getElementById("message").appendChild(msgDiv);
    setTimeout(function() { msgDiv.remove(); }, 5000);
}

function loadResults(url, target) {
  var div = document.getElementById(target);
  $.ajax({
    url: url,
    success: function(data) {
      div.innerHTML = data;
    }
  });
   
}

function loadFilterResults(url, target) {
  var input, div;
  input = document.getElementById(target + "Input");
  div = document.getElementById(target + "Results");
  $.ajax({
    type: "POST",
    url: url,
    data: { value: input.value },
    success: function(data) {
      div.innerHTML = data;
    }
  });
   
}
