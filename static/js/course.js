let user;
let course;

$(document).ready(function () {
    $.ajax({
        url: "/api/user",
        type: "GET",
        headers: {
            Authorization: 'JWT ' + Cookies.get('access_token')
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            user = data;
            user = getUserData(user);
            getCourseData();
            getAttendanceData();
        },
        error: function (e) {
            console.log("ERROR : ", e.responseJSON["message"]);
        }
    });
})


function getAttendanceData() {
    $.ajax({
        url: "/api/attendance/" + course_id,
        type: "GET",
        headers: {
            Authorization: 'JWT ' + Cookies.get('access_token')
        },
        data: "user_id=" + user['id'],
        success: function (data) {
            course = data;
        },
        error: function (e) {
            console.log("ERROR : ", e.responseJSON["message"]);
        }
    });
}

function getCourseData() {
    $.ajax({
        url: "/api/course/" + course_id,
        type: "GET",
        headers: {
            Authorization: 'JWT ' + Cookies.get('access_token')
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            course = data;
            let courseBtn = $("#course-btn");
            if (user["is_student"] === true) {
                courseBtn.attr("disabled", course["is_ongoing"] === false)
                courseBtn.html("Attend ongoing class");
                courseBtn.click(attendClass);
            } else {
                courseBtn.click(changeCourseState);
                if (course["is_ongoing"] === false) {
                    courseBtn.html("Start class");
                } else {
                    courseBtn.html("Stop class");
                }
            }
        },
        error: function (e) {
            console.log("ERROR : ", e.responseJSON["message"]);
        }
    });
}

function changeCourseState() {
    $.ajax({
        url: "/api/attendance/" + course_id,
        type: "POST",
        data: "user_id=" + user['id'],
        headers: {
            Authorization: 'JWT ' + Cookies.get('access_token')
        },
        success: function (data) {
            let courseBtn = $("#course-btn");
            alert(data["message"]);
            if (course["is_ongoing"] === false) {
                courseBtn.html("Stop class");
            } else {
                courseBtn.html("Start class");
            }
            course["is_ongoing"] = !course["is_ongoing"]
        },
        error: function (e) {
            console.log("ERROR : ", e.responseJSON["message"]);
        }
    });
}

function attendClass() {
    console.log("attend class")
}