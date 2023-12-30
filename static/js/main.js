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

function ajaxErrorHandler(jqXHR, exception) {
  var msg = '';
  if (jqXHR.status === 0) {
      msg = 'Not connect.\n Verify Network.';
  } else if (jqXHR.status == 404) {
      msg = 'Requested page not found. [404]';
  } else if (jqXHR.status == 500) {
      msg = 'Internal Server Error [500].';
  } else if (exception === 'parsererror') {
      msg = 'Requested JSON parse failed.';
  } else if (exception === 'timeout') {
      msg = 'Time out error.';
  } else if (exception === 'abort') {
      msg = 'Ajax request aborted.';
  } else {
      msg = 'Uncaught Error.\n' + jqXHR.responseText;
  }
  set_message(msg, css_class='alert-danger');
}

function loadResults(url, target) {
  var div = document.getElementById(target);
  $.ajax({
    url: url,
    success: function(data) {
      div.innerHTML = data;
    },
    error: ajaxErrorHandler
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
