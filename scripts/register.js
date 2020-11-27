$(document).ready(function(){
    var option1 = 0;
    var option2 = 0;
    var option3 = 0;
    var option4 = 0;
    var optionTotal = 0;

    if (document.getElementById('option1Input').checked) {
        option1 = 1;
        $("#option1").css("border", "4px solid black");
    }
    else if (document.getElementById('option2Input').checked) {
        option2 = 1;
        $("#option2").css("border", "4px solid black");
    }
    else if (document.getElementById('option3Input').checked) {
        option3 = 1;
        $("#option3").css("border", "4px solid black");
    }
    else if (document.getElementById('option4Input').checked) {
        option4 = 1;
        $("#option4").css("border", "4px solid black");
    }


	$("img").click(function(){
        if (this.id == "option1") {
            $("img#option2").css("border", "");
            $("img#option3").css("border", "");
            $("img#option4").css("border", "");
            $(this).css("border", "4px solid black");
            option1 = 1;
            option2 = 0;
            option3 = 0;
            option4 = 0;
        }
        else if (this.id == "option2") {
            $("img#option1").css("border", "");
            $("img#option3").css("border", "");
            $("img#option4").css("border", "");
            $(this).css("border", "4px solid black");
            option1 = 0;
            option2 = 1;
            option3 = 0;
            option4 = 0;
        }
        else if (this.id == "option3") {
            $("img#option1").css("border", "");
            $("img#option2").css("border", "");
            $("img#option4").css("border", "");
            $(this).css("border", "4px solid black");
            option1 = 0;
            option2 = 0;
            option3 = 1;
            option4 = 0;
        }
        else if (this.id == "option4") {
            $("img#option1").css("border", "");
            $("img#option2").css("border", "");
            $("img#option3").css("border", "");
            $(this).css("border", "4px solid black");
            option1 = 0;
            option2 = 0;
            option3 = 0;
            option4 = 1;
        }
	});
});