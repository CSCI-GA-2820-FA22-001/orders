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
    $("#create-btn").click(function(){
        let user_id = $("#create-order-id").val();
        let item_list = []
        for(var i = 1; i <= 3; i++){
            // console.log($(`#item_box_${i}`));
            // console.log($("#item-box-1").is(':checked'));
            if($(`#item-box-${i}`).is(':checked')){
                item_list.push(i);
            }
        }
        console.log(`User id: ${user_id}`);
        console.log(`Item list: ${item_list}`);
    })
})
