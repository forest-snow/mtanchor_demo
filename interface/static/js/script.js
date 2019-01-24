$(function(){
    // template html elements
    var closeButton = "<i class='fa fa-times fa-large close'></i>"
    var emptyTopic = "<div class='row mb-4 topic template'></div>"
    var anchors = "<div class='col-2 p-3 ml-auto anchors'></div>"
    var blank1 = "<div class='col-3 p-3 bg-white'></div>"
    var blank2 = "<div class='col-3 p-3 ml-auto bg-white'></div>"
    var emptyWord = "<span class='btn btn-sm m-1 word'></span>"

    // hide loader
    $(".load").hide()

    // load ID
    $.get("/uid").done(function(data) {
        var uid = data["uid"];
        $("#uid").text("User ID: "+uid);
    });

    // enable sortable anchor words
    $(".l1.anchors").sortable({connectWith:".l1.anchors"});
    $(".l2.anchors").sortable({connectWith:".l2.anchors"});

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
    var addAnchor = function(e, ui){
        var newClone = $(ui.draggable).clone();
        newClone.removeClass("word");
        newClone.addClass("anchor");
        newClone.append(closeButton);
        $(this).append(newClone);

    };

    var dropOptions1 = {
        accept: ".l1.word",
        drop: addAnchor
    };
    $(".l1.anchors").droppable(dropOptions1);

    var dropOptions2 = {
        accept: ".l2.word",
        drop: addAnchor
    };
    $(".l2.anchors").droppable(dropOptions2);

    // dynamically triggering close buttons
    $("#topics").on("click", ".close", function(){
        $(this).parent().remove();
    });
    
    // add topic onto interface
    $("#add").click( function() {
        var topic = $(emptyTopic).clone();
        var l1anchors = $(anchors).clone()
            .addClass("l1").droppable(dropOptions1)
            .sortable({connectWith:".l1.anchors"});
        var l2anchors = $(anchors).clone()
            .addClass("l2").droppable(dropOptions2)
            .sortable({connectWith:".l2.anchors"});

        $(topic).append(closeButton);
        $(blank1).clone().appendTo(topic)
        $(topic).append(l1anchors);
        $(topic).append(l2anchors);
        $(blank2).clone().appendTo(topic)
        $("#topics").append(topic);

    });


    // helper functions for updating topics
    function pushText(array, textArray){
        $.each(array, function(i, anchors) {
            var texts = [];
            $(anchors).children(".anchor").each( function(j, anchor) {
                texts.push($(anchor).text());
            });
            textArray.push(texts);
        });
        return textArray;
    };

    function checkEmptyTopics(){
        var anchorArray = $(".anchors").get();
        var empty = false;
        $.each(anchorArray, function() {
            if(($(this).children().length) == 0) {
                empty = true;
            }
        });
        return empty;
    };

    // updating topics 
    $("#update").click( function(){
        if(checkEmptyTopics()) {
            alert("No topic update: make sure each topic has at least one anchor in each language.")
            return false;
        }
        console.log("here")

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
            type: 'POST',
            beforeSend: function() {
                $("#topics").hide(); 
                $(".load").show();
            },
            complete: function(){
                $(".load").hide();
                $("#topics").show();
            },
            success: function(result) {
                if (result == "success") {
                    location.reload()
                }
            }

        });
        
    });



    // translating words on mouseover
    // var mouseOver = function(ev) {
    //    var text = $(ev.target).text();

    //     get translation
    //     $.get("/translate", {text: text, in_corpus:false})
    //         .done(function(data) {
    //             var translation = data['translation'];
    //             if (translation !== 'N/A') {
    //                 $("#translation").text("Translation: "+translation);

    //             } else {
    //                 $("#translation").text("Translation: ");
    //             }
    //         });
    // };

    // $("#topics").on("mouseover", ".anchor, .word", mouseOver)


    // highlight ocurrences of word and its translation once clicked
    var highlight = function (ev) {
        var text = $(ev.target).text();
        console.log(text)

        // unhighlight previous words
        $(".highlight").removeClass("highlight");

        // highlight words with same text
        $(".word, .anchor").filter( function() { 
            return ($(this).text() === text)
        })
            .addClass("highlight");

        // highlight translations

        // $.get("/translate", {text: text, in_corpus:false})
        //     .done(function(data) {
        //         var translation = data['translation'];
        //         if (translation !== 'N/A') {
        //             $(".word, .anchor").filter( function() { 
        //                 return ($(this).text() === translation)
        //             })
        //                 .addClass("highlight");


        //         };
        //     });

    };
    
    $("#topics").on("click", ".anchor, .word", highlight);


    // autocomplete
    $("#search").autocomplete({
        minLength: 3,
        delay: 500,
        position: {my: "left bottom", at: "left top"},
        // callback to get word choices 
        source: function(request, response) {
            $.get("/autocomplete", {
                query: request.term
            }, function(data) {
                var choices = data["choices"];
                response(choices);
            });
        },
        // produce new word element and translation element (if exists in corpus)
        select: function(event, ui) {
            var text = ui.item.label
            var word = $(emptyWord).clone();
            word.text(text).draggable(dragOptions);

            if(ui.item.language=="l1") {
                word.addClass("l1")
            } else {
                word.addClass("l2")
            }

            // empty out previous searches
            $("#new-word").empty();
            
            $("#new-word").append(word);

            $.get("/translate", {text: text, in_corpus:true})
                .done(function(data) {
                    var translation = data['translation'];
                    if (translation !== 'N/A') {
                        var word = $(emptyWord).clone();
                        word.text(translation).draggable(dragOptions)
                            if(ui.item.language=="l1") {
                                word.addClass("l2")
                            } else {
                                word.addClass("l1")
                            };
                        $("#new-word").append(word);

                };
            });

        }
    });



});



