$(document).ready(function(){
    console.log($('#data'))
    var initScore = $('#data').data("score")
    if($('#data').data("uservote") == 1) {
        $("#upvote").attr("src", "../../../static/data/Upvoted.png")
    }
    if($('#data').data("uservote") == -1) {
        $("#downvote").attr("src", "../../../static/data/Downvoted.png")
    }
    $("#score").html("&nbsp;&nbsp;" + initScore)
    $("#upvote").click(function() {
        if($('#upvote').attr("src") == '../../../static/data/Upvoted.png') {
            $("#upvote").attr("src", "../../../static/data/Upvote.png")
            $("#score").html("&nbsp;&nbsp;" + (initScore -= 1))
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 0, "postid": $('#data').data("postid")})
        }
        else if($("#downvote").attr("src") == "../../../static/data/Downvoted.png"){
            $("#upvote").attr("src", '../../../static/data/Upvoted.png')
            $("#downvote").attr("src", "../../../static/data/Downvote.png")
            $("#score").html("&nbsp;&nbsp;" + (initScore += 2))
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 1, "postid": $('#data').data("postid")})
        }
        else{
            $("#upvote").attr("src", '../../../static/data/Upvoted.png')
            $("#score").html("&nbsp;&nbsp;" + (initScore += 1))
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 1, "postid": $('#data').data("postid")})
        }
    });
    $("#downvote").click(function() {
        if($('#downvote').attr("src") == '../../../static/data/Downvoted.png') {
            $("#downvote").attr("src", '../../../static/data/Downvote.png')
            $("#score").html("&nbsp;&nbsp;" + (initScore += 1))
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 0, "postid": $('#data').data("postid")})
        }
        else if($("#upvote").attr("src") == "../../../static/data/Upvoted.png"){
            $("#downvote").attr("src", '../../../static/data/Downvoted.png')
            $("#upvote").attr("src", '../../../static/data/Upvote.png')
            $("#score").html("&nbsp;&nbsp;" + (initScore -= 2))
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": -1, "postid": $('#data').data("postid")})
        }
        else{
            $("#downvote").attr("src", '../../../static/data/Downvoted.png')
            $("#score").html("&nbsp;&nbsp;" + (initScore -= 1))
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 1, "postid": $('#data').data("postid")})
        }
    });
});