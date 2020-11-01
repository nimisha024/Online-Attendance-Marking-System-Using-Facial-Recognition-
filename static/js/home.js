$(document).ready(function () {
    let user;
    let courseData;
    $.ajax({
        url: "/api/user",
        type: "GET",
        headers: {
            Authorization: 'JWT ' + Cookies.get('access_token')
        },
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            user = $.parseJSON(data);
            user = getUserData(user);
            courseData = getCourseData(user);
            console.log("SUCCESS : ", user);
        },
        error: function (e) {
            console.log("ERROR : ", e.responseJSON["description"]);
        }
    });
})

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
                console.log("DATA : ", data);
                $.extend(user, data);
                console.log("SUCCESS : ", user);

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
                console.log("DONE", data);
                $.extend(user, data);
                console.log("SUCCESS : ", user);

                $("#user-name").text(user["faculty_name"] + " " + user["faculty_id"])
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    }
    return user;
}

function getCourseData(user) {
    let courseList = $('#course-list');
    let dummyCourse = $('#dummy-course');

    if (user["is_student"] === true) {
        $.ajax({
            url: "/api/student/" + user["id"] + "/courses",
            type: "GET",
            headers: {
                Authorization: 'JWT ' + Cookies.get('access_token')
            },
            dataType: "json",
            contentType: "application/json",
            success: function (data) {
                for (let i in data) {
                    let course = data[i];
                    let clone = dummyCourse.clone();
                    clone.attr("id", course["course_id"]);
                    courseList.append(clone);

                    $("#" + course["course_id"] + " h3").text(course["course_name"]);
                    $("#" + course["course_id"] + " a").attr("href", "/course/" + course["course_id"]);
                }
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    } else {
        $.ajax({
            url: "/api/faculty/" + user["id"] + "/courses",
            type: "GET",
            headers: {
                Authorization: 'JWT ' + Cookies.get('access_token')
            },
            dataType: "json",
            contentType: "application/json",
             success: function (data) {
                for (let i in data) {
                    let course = data[i];
                    let clone = dummyCourse.clone();
                    clone.attr("id", course["course_id"]);
                    courseList.append(clone);

                    $("#" + course["course_id"] + " h3").text(course["course_name"]);
                    $("#" + course["course_id"] + " a").attr("href", "/course/" + course["course_id"]);
                }
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    }
    dummyCourse.remove();
}