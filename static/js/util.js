function getUserData(user) {
    if (user["is_student"] === true) {
        $.ajax({
            url: "/api/student/" + user["id"],
            type: "GET",
            headers: {
                Authorization: 'JWT ' + Cookies.get('access_token')
            },
            dataType: "json",
            contentType: "application/json",
            success: function (data) {
                $.extend(user, data);
                $("#user-name").text(user["student_name"] + " " + user["student_id"])
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    } else {
        $.ajax({
            url: "/api/faculty/" + user["id"],
            type: "GET",
            headers: {
                Authorization: 'JWT ' + Cookies.get('access_token')
            },
            dataType: "json",
            contentType: "application/json",
            success: function (data) {
                $.extend(user, data);
                $("#user-name").text(user["faculty_name"] + " " + user["faculty_id"])
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    }
    return user;
}
