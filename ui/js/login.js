
$(document).ready(function () {

    $("#btnSubmit").click(function (event) {

        //stop submit the form, we will post it manually.
        event.preventDefault();

        //get data
        var formData = {
            "username"              : $('input[name=student_id]').val(),
            "password"             : $('input[name=password]').val(),
        };

       // disabled the submit button
        $("#btnSubmit").prop("disabled", true);

        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/auth",
            data: formData,
            contentType: "application/json",
            crossDomain : true,
            success: function (data) {

                $("#output").text(data);
                console.log("SUCCESS : ", data);
                $("#btnSubmit").prop("disabled", false);

            },
            error: function (e) {

                $("#output").text(e.responseText);
                console.log("ERROR : ", e);
                $("#btnSubmit").prop("disabled", false);

            }
        });

    });

});