function delete_course(id) {
    let response = confirm("Are you sure you want to delete this course from database?");
    if (response) {
        $.post("/ui/course/delete?id=" + id, function(data){},"json");
        setTimeout(refresh_page, 500);
    }
}

function archive(tag) {
    let response = confirm("Are you sure you want to archive this channel?");
    if (response) {
        console.log(tag)
        $.post("/ui/channel/archive?tag=" + tag.substr(1), function(data){},"json");
        setTimeout(refresh_page, 500);
    }
}

function unarchive(tag) {
    let response = confirm("Are you sure you want to unarchive this channel?");
    if (response) {
        console.log(tag)
        $.post("/ui/channel/unarchive?tag=" + tag.substr(1), function(data){},"json");
        setTimeout(refresh_page, 500);
    }
}

function refresh_page() {
    location.reload();
}