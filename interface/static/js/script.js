$(function(){
    var closeButton = "<i class='fa fa-times fa-large close'></i>"
    var emptyTopic = "<div class='row mb-4 topic template'></div>"
    var anchors = "<div class='col-2 p-3 ml-auto anchors'></div>"
    var blank1 = "<div class='col-3 p-3 bg-white'></div>"
    var blank2 = "<div class='col-3 p-3 ml-auto bg-white'></div>"


    // enable sortable anchor words
    $(".anchors").sortable({connectWith:".anchors"});

    // enable draggable words
    var dragOptions = {
        revert:true,
        helper:"clone",
        drag: function(e, ui){
            $(ui.helper).css("z-index",2)
        }
    };

    $(".word").draggable(dragOptions);


    // enable words to be dropped in anchor containers
    var dropOptions = {
        accept: ".word",
        drop: function (e, ui){
            var newClone = $(ui.draggable).clone();
            newClone.removeClass("word");
            newClone.addClass("anchor");
            newClone.append(closeButton);
            $(this).append(newClone);
        }
    };
    $(".anchors").droppable(dropOptions);

    // triggering close buttons
    $("#topics").on("click", ".close", function(){
        $(this).parent().remove();
    });
    


    $("#add").click( function() {
        var topic = $(emptyTopic).clone();
        var l1anchors = $(anchors).clone().addClass("l1").droppable(dropOptions).sortable({connectWith:".anchors"});
        var l2anchors = $(anchors).clone().addClass("l2").droppable(dropOptions).sortable({connectWith:".anchors"});
        $(topic).append(closeButton);
        $(blank1).clone().appendTo(topic)
        $(topic).append(l1anchors);
        $(topic).append(l2anchors);
        $(blank2).clone().appendTo(topic)
        $("#topics").append(topic);
    });



    function pushText(array, textArray){
        $.each(array, function(i, anchors) {
            var texts = [];
            $(anchors).children(".anchor").each( function(j, anchor) {
                texts.push($(anchor).text());
            });
            textArray.push(texts);
        });
        console.log(textArray)
        return textArray;
    }

    // updating topics 
    $("#update").click( function(){
        var l1anchors = []
        var l2anchors = []
        pushText($(".l1.anchors").get(), l1anchors)
        pushText($(".l2.anchors").get(), l2anchors)

        var data = {
            "l1":l1anchors,
            "l2":l2anchors
        };

        $.ajax({
            url: "/update",
            contentType: 'application/json',
            data: JSON.stringify(data),
            type: 'POST'
        })
        
    });

});



