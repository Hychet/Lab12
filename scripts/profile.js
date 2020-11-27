$(document).ready(function(){
    $("img.upvote").each(function () {
        if($('#data').data("posts")[parseInt($(this).attr('id').substring(1)) - 1]['userVote'] == 1) {
            $(this).attr("src", "../../../static/data/Upvoted.png")
        }
    });
    $("img.downvote").each(function () {
        if($('#data').data("posts")[parseInt($(this).attr('id').substring(1)) - 1]['userVote'] == -1) {
            $(this).attr("src", "../../../static/data/Downvoted.png")
        }
    });
    $("span.score").each(function () {
        $(this).html("&nbsp;&nbsp;" + $('#data').data("posts")[parseInt($(this).attr('id').substring(1)) - 1]['score'])
    });
    $("img.upvote").click(function() {
        var elid = $(this).attr('id').substring(1)
        if($(this).attr("src") == '../../../static/data/Upvoted.png') {
            $(this).attr("src", "../../../static/data/Upvote.png")
            console.log(elid)
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 0, "postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
            $("#s" + elid).html("&nbsp;&nbsp;" + ($('#data').data("posts")[parseInt(elid) - 1]['score'] -= 1))
        }
        else if($("#d" + $(this).attr('id').substring(1)).attr("src") == "../../../static/data/Downvoted.png"){
            $(this).attr("src", "../../../static/data/Upvoted.png")
            $("#d" + $(this).attr('id').substring(1)).attr("src", "../../../static/data/Downvote.png")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 1, "postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
            $("#s" + elid).html("&nbsp;&nbsp;" + ($('#data').data("posts")[parseInt(elid) - 1]['score'] += 2))
        }
        else{
            $(this).attr("src", "../../../static/data/Upvoted.png")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 1, "postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
            $("#s" + elid).html("&nbsp;&nbsp;" + ($('#data').data("posts")[parseInt(elid) - 1]['score'] += 1))
        }
    });
    $("img.downvote").click(function() {
        var elid = $(this).attr('id').substring(1)
        if($(this).attr("src") == '../../../static/data/Downvoted.png') {
            $(this).attr("src", "../../../static/data/Downvote.png")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": 0, "postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
            $("#s" + elid).html("&nbsp;&nbsp;" + ($('#data').data("posts")[parseInt(elid) - 1]['score'] += 1))
        }
        else if($("#u" + $(this).attr('id').substring(1)).attr("src") == "../../../static/data/Upvoted.png"){
            $(this).attr("src", '../../../static/data/Downvoted.png')
            $("#u" + elid).attr("src", "../../../static/data/Upvote.png")
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": -1, "postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
            $("#s" + elid).html("&nbsp;&nbsp;" + ($('#data').data("posts")[parseInt(elid) - 1]['score'] -= 2))
        }
        else{
            $(this).attr("src", '../../../static/data/Downvoted.png')
            $.post("/vote", {"voterHash": $('#data').data("userhash"), "vote": -1, "postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
            $("#s" + elid).html("&nbsp;&nbsp;" + ($('#data').data("posts")[parseInt(elid) - 1]['score'] -= 1))
        }
        console.log($('#data').data("posts"))
    });

    $("a.delete").click(function() {
        if (confirm("Are you sure you want to delete this post?")) {
            var elid = $(this).attr('id').substring(6)
            $(this.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement).html("");
            $.post("/delete", {"postid": $('#data').data("posts")[parseInt(elid) - 1]['id']})
        }
    });
});