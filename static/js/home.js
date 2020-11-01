let user;

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
            getCourseData(user);
        },
        error: function (e) {
            console.log("ERROR : ", e);
        }
    });
})

function getCourseData(user) {
    if (user.is_student) {
        $.ajax({
            url: "/api/student/" + user.id + "/courses",
            type: "GET",
            headers: {
                Authorization: 'JWT ' + Cookies.get('access_token')
            },
            dataType: "json",
            contentType: "application/json",
            success: function (data) {
                addCourses(data)
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    } else {
        $.ajax({
            url: "/api/faculty/" + user.id + "/courses",
            type: "GET",
            headers: {
                Authorization: 'JWT ' + Cookies.get('access_token')
            },
            dataType: "json",
            contentType: "application/json",
            success: function (data) {
                addCourses(data)
            },
            error: function (e) {
                console.log("ERROR : ", e);
            }
        });
    }
}

function addCourses(courses) {
    let courseList = $('#course-list');
    let dummyCourse = $('#dummy-course');
    for (let course of courses) {
        let clone = dummyCourse.clone();
        clone.attr("id", course.course_code);
        courseList.append(clone);

        $("#" + course.course_code + " #course-name").text(course.course_name);
        $("#" + course.course_code + " #view-course").attr("href", "/course/" + course.course_code);
    }
    dummyCourse.remove();
}