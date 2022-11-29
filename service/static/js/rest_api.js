$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function update_form_data(res) {
        $("#pet_id").val(res.id);
        $("#pet_name").val(res.name);
        $("#pet_category").val(res.category);
        if (res.available == true) {
            $("#pet_available").val("true");
        } else {
            $("#pet_available").val("false");
        }
        $("#pet_gender").val(res.gender);
        $("#pet_birthday").val(res.birthday);
    }

    /// Clears all form fields
    function clear_form_data() {
        $("#pet_name").val("");
        $("#pet_category").val("");
        $("#pet_available").val("");
        $("#pet_gender").val("");
        $("#pet_birthday").val("");
    }

    // Updates the flash message area
    function flash_message(message) {
        $("#flash_message").empty();
        $("#flash_message").append(message);
    }

    // ****************************************
    // Create a Order
    // ****************************************

    $("#create-btn").click(function () {

        
        let user_id = parseInt($("#create-order-id").val());
        let create_time = Math.floor(Date.now() / 1000);

        let items = []
        for(var i = 1; i <= 3; i++){
            // console.log($(`#item_box_${i}`));
            // console.log($("#item-box-1").is(':checked'));
            if($(`#item-box-${i}`).is(':checked')){
                items.push(i);
            }
        }
        console.log(`User id: ${user_id}`);
        console.log(`Item list: ${items}`);
        let data = {
            "user_id": user_id,
            "create_time": create_time,
            "items": items,
            "status": 1
        };

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });


    // ****************************************
    // Order team code starts here
    // ****************************************
    
    // ****************************************
    // switch to retrieve page
    // ****************************************
    $("#to-retrieve-btn").click(function(){
        $("#create-page").hide();
        $("#to-retrieve-btn").hide();
        $("#to-create-btn").show();
        $("#retrieve-page").show();
    });
    $("#to-create-btn").click(function(){
        $("#create-page").show();
        $("#to-retrieve-btn").show();
        $("#to-create-btn").hide();
        $("#retrieve-page").hide();
    })

})