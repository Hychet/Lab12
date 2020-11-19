$(document).ready(function(){
    if($('#data').data("uservote") == 1) {
        $("#upvote").attr("src", "{{ url_for('static', filename='data/Upvoted.png') }}")
    }
    if($('#data').data("uservote") == -1) {
        $("#downvote").attr("src", "{{ url_for('static', filename='data/Downvoted.png') }}")
    }
    $("#upvote").click(function() {
        if($('#upvote').attr("src") == "{{ url_for('static', filename='data/Upvoted.png') }}") {
            $("#upvote").attr("src", "{{ url_for('static', filename='data/Upvote.png') }}")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 0, "postid": $('#data').data("postid")})
        }
        else {
            $("#upvote").attr("src", "{{ url_for('static', filename='data/Upvoted.png') }}")
            $("#downvote").attr("src", "{{ url_for('static', filename='data/Downvote.png') }}")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 1, "postid": $('#data').data("postid")})
        }
    });
    $("#downvote").click(function() {
        if($('#downvote').attr("src") == "{{ url_for('static', filename='data/Downvoted.png') }}") {
            $("#downvote").attr("src", "{{ url_for('static', filename='data/Downvote.png') }}")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 0, "postid": $('#data').data("postid")})
        }
        else {
            $("#downvote").attr("src", "{{ url_for('static', filename='data/Downvoted.png') }}")
            $("#upvote").attr("src", "{{ url_for('static', filename='data/Upvote.png') }}")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": -1, "postid": $('#data').data("postid")})
        }
    });
});