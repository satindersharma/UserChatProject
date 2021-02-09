window.addEventListener("load", () => {

// // image on error
// $("img").on("error", function () {  
//   // $(this).attr("src", "broken.gif");
//   console.log('image errrorr')
// });

  // navigate to edit tab on edit profile link click
  $("#edit-my-profile").on("click", function (e) {
    e.preventDefault();
    $('#v-pills-tab a[href="#v-pills-profile"]').tab("show");
  });

  // trigger submit the form on image change
  $("#id_profile-image").change(function (e) {
    e.preventDefault();
    $("#profile-edit-form").trigger("submit");

    // console.log(this)
  });
  // adding the image for user profile to html img element
  function addtheimage(input, image_id) {
    let reader = new FileReader();
    reader.onload = function (e) {
      $(image_id).attr("src", "");
      $(image_id).attr("src", `${e.target.result}`);
    };
    reader.readAsDataURL(input, image_id);
  }

  /* ----- profile form ajax ----- */

  let profile_form = $("#profile-edit-form");
  profile_form.submit(function (e) {
    e.preventDefault();
    let serializedData = new FormData(this);
    // console.log("serr", serializedData.get("profile-image"));
    // // Display the key/value pairs
    // for(var pair of serializedData.entries()) {
    //   console.log(pair[0]+ ', '+ pair[1]);
    // }

    $.ajax({
      type: profile_form.attr("method"),
      url: profile_form.attr("action"),
      data: serializedData,
      cache: false,
      contentType: false,
      processData: false,
      success: function (data) {
        $.confirm({
          title: "Success!",
          content: data.content,
          theme: "modern",
          autoClose: "ok|1000",
          escapeKey: true,
          draggable: true,
          onClose: function () {
            return true;
          },
          backgroundDismiss: function () {
            return true;
          },
          buttons: {
            ok: function () {
              return true;
            },
          },
        });
        // updating image on success
        image_input = serializedData.get("profile-image");

        addtheimage(image_input, ".profile-pic, .profile-pic-icon");
        $("#profile-image-delete").removeClass("disabled");
      },
      error: function (error_data) {
        let jsonData = error_data.responseJSON;
        let msg = "";
        $.each(jsonData, function (k, v) {
          msg += k + ": " + v[0].message + "<br/>";
        });
        $.confirm({
          title: "Error!",
          content: msg,
          theme: "modern",
          escapeKey: true,
          backgroundDismiss: true,
          onClose: function () {
            return true;
          },
          buttons: {
            ok: function () {
              return true;
            },
          },
        });
      },
    });
  });

  /* ---- profile image delete button ajax call --- */

  let img_delete_btn = $("#profile-image-delete");
  let is_disabled = img_delete_btn.hasClass("disabled");
  let default_img = img_delete_btn.data("defaultimage");
  img_delete_btn.on("click", function (e) {
    e.preventDefault();
    $.ajax({
      type: "post",
      url: "/delete-image/",
      data: { disabled: is_disabled },
      success: function (data) {
        $.confirm({
          title: "Success!",
          content: data.content,
          theme: "modern",
          autoClose: "ok|1000",
          escapeKey: true,
          draggable: true,
          backgroundDismiss: true,
          onClose: function () {
            return true;
          },
          buttons: {
            ok: function () {
              return true;
            },
          },
        });
        $(".profile-pic, .profile-pic-icon").attr("src", `${default_img}`);
        $("#profile-image-delete").addClass("disabled");
      },
      error: function (error_data) {
        let json_data = error_data.responseJSON;
        let msg = "";
        $.each(json_data, function (k, v) {
          msg += k + ": " + v[0].message + "<br/>";
        });
        $.confirm({
          title: "Error!",
          content: msg,
          theme: "modern",
          autoClose: "ok|1000",
          escapeKey: true,
          draggable: true,
          backgroundDismiss: true,
          onClose: function () {
            return true;
          },
          buttons: {
            ok: function () {
              return true;
            },
          },
        });
      },
    });
  });
});
