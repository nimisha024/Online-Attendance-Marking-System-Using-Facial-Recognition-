function configure() {
    Webcam.set({
        width: 320,
        height: 240,
        image_format: 'jpeg',
        jpeg_quality: 90
    });
    Webcam.attach('#webcam');
}

function takeSnapshot() {
    $("#upload-button").attr("disabled", false);
    Webcam.snap(function (data_uri) {
        $('#result').html('<img id="image-prev" src="' + data_uri + '"/>')
    });

    Webcam.reset();
}

function uploadSnap() {
    $.post({
        url: "/api/attendance/" + course_id,
        data: {user_id: user.id, image: $("#image-prev").src},
        headers: {
            Authorization: 'JWT ' + Cookies.get('access_token')
        },
        success: function (data) {
            alert(data.message);
            $('#webcam-container').hide();
        },
        error: function (e) {
            console.log("ERROR : ", e);
        }
    });
}
