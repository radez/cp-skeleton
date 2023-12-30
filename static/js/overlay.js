function overlay_close(e) {
    e.preventDefault();
    $("#overlay, .inner-overlay, .overlay-content").removeClass("active");
    $('#overlay-content').html('<div style="text-align: center;"><img src="' + request_script_name + '/img/icons8-spinner.gif" alt="loading gif"></div>');
};
function overlay_refresh(url, func=null) {
    $.ajax({
      url: url,
      type: "GET",
      dataType: "html",
      success: function (res) {
           $("#overlay-content").html(res).fadeIn('slow');
           if (func) { func(); };
      }
    });
};
function overlay_open(url, func=null) {
    $("#overlay, .inner-overlay, .overlay-content").addClass("active");
    overlay_refresh(url, func); 
};
