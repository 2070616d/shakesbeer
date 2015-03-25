this.imagePreview = function(){
    /* CONFIG */

        xOffset = 50;
        yOffset = 10;

        // these 2 variable determine popup's distance from the cursor

    /* END CONFIG */
    $("a.recipeImg").hover(function(e){
        this.t = this.title;
        this.title = "";
        var c = (this.t != "") ? "<br/>" + this.t : "";
        $("body").append("<p id='recipeImg'><img src='"+ this.rel +"' alt='image preview' style=\"height:auto; width:auto; max-width:300px; max-height:300px;\"/>"+ c +"</p>");
        $("#recipeImg")
            .css("top",(e.pageY - xOffset) + "px")
            .css("left",(e.pageX + yOffset) + "px")
            .fadeIn("fast");
    },
    function(){
        this.title = this.t;
        $("#recipeImg").remove();
    });
    $("a.recipeImg").mousemove(function(e){
        var posY;
        if (e.pageY - $(window).scrollTop() + $('#recipeImg').height() >= $(window).height() ) {
            posY = $(window).height() + $(window).scrollTop() - $('#recipeImg').height() - 50;
        } else {
            posY = e.pageY - yOffset;
        }
        $("#recipeImg")
            .css("top",(posY) + "px")
            .css("left",(e.pageX + xOffset) + "px");
    });
};


// starting the script on page load
$(document).ready(function(){
    imagePreview();
});