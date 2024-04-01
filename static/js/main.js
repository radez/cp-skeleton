$(document).ready(function() {
  // reload when session expires
  setTimeout(function(){
     location = '';
  }, 3601000) // 1 hour 10 seconds

  // Common Modal Event Handler
  $('#commonModal').bind('show.bs.modal', event => {
    // Set Modal Content to Loading
    mhead = $('<div class="modal-header"></div>');
    h1 = $('<h1 class="modal-title fs-5" id="commonModalTitle">Loading ...</h1>');
    close = $('<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>');
    mhead.append(h1);
    mhead.append(close);
    $("#modalContent").html(mhead).fadeIn('slow');
    mbody = $('<div class="modal-body"></div>');
    center = $('<div style="text-align: center;"></div>');
    mbody.append(center);
    loading = $('<img src="' + request_script_name + '/img/icons8-spinner.gif" alt="loading gif" size="72">');
    center.append(loading);
    $("#modalContent").append(mbody);

    // Button that triggered the modal
    const button = event.relatedTarget
    // Extract info from data-bs-* attributes
    const loadurl = button.getAttribute('data-bs-loadurl')
    $.ajax({
      url: loadurl,
      type: "GET",
      dataType: "html",
      success: function (res) {
        $("#modalContent").html(res).fadeIn('slow');
        //if (func) { func(); };
      },
      error: function (jqXHR, exception) {
        var msg = '';
        console.log(jqXHR);
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
        mhead = $('<div class="modal-header"></div>');
        h1 = $('<h1 class="modal-title fs-5" id="commonModalTitle">' + msg + '</h1>');
        close = $('<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>');
        mhead.append(h1);
        mhead.append(close);
        $("#modalContent").html(mhead).fadeIn('slow');
      }
    });
  })
});

function toggledisplay(elementID) {
 (function(style) {
	style.display = style.display === 'none' ? '' : 'none';
 })(document.getElementById(elementID).style);
}

function set_message(data, css_class='alert-success') {
    if (typeof data !== 'string' && data) {
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
  console.log(jqXHR);
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
    },
    error: ajaxErrorHandler
  });
   
}
