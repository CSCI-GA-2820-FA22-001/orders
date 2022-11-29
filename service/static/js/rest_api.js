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
        
        let user_id = parseInt($("#create-user-id").val());
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
    // Read an order by order id
    // ****************************************

    $("#read-btn").click(function () {
        let order_id = parseInt($("#read-order-id").val());
        console.log(`Order id: ${order_id}`);
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
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
    // Read an order by item id
    // ****************************************

    $("#read-by-item-id-btn").click(function () {
        let item_id = parseInt($("#read-item-id").val());
        console.log(`item id: ${item_id}`);
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/items/" + item_id,
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
    // Read an order by order status
    // ****************************************

    $("#read-by-order-status-btn").click(function () {
        let order_status = parseInt($("#read-order-status").val());
        let user_id = parseInt($("#read-user-id").val());
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/user/" + user_id + "/status/" + order_status
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
    // Update an order by order id
    // ****************************************

    $("#update-btn").click(function () {
        let order_id = parseInt($("#update-order-id").val());
        let user_id = parseInt($("#update-user-id").val());
        let create_time = Math.floor(Date.now() / 1000);
        let order_status = $("#update-order-status").val();
        console.log(`Order id: ${user_id}`);

        $("#flash_message").empty();
        
        let data = {
            "user_id": user_id,
            "create_time": create_time,
            "status": order_status
        };

        let ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id,
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
    // Delete an order by order id
    // ****************************************

    $("#delete-btn").click(function () {
        let order_id = parseInt($("#delete-order-id").val());
        console.log(`Order id: ${user_id}`);
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
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
    // switch to read page
    // ****************************************
    function hideAllPages() {
        $("#create-page").hide();
        $("#read-page").hide();
        $("#read-by-item-id-page").hide();
        $("#read-by-order-status-page").hide();
        $("#update-page").hide();
        $("#delete-page").hide();
    }

    function resetAllBtns() {
        document.querySelector('#to-create-page-btn').disabled = false;
        document.querySelector('#to-read-page-btn').disabled = false;
        document.querySelector('#to-read-by-item-id-page-btn').disabled = false;
        document.querySelector('#to-read-by-order-status-page-btn').disabled = false;
        document.querySelector('#to-update-page-btn').disabled = false;
        document.querySelector('#to-delete-page-btn').disabled = false;
    }

    function resetAll() {
        hideAllPages();
        resetAllBtns();
    }
    
    $("#to-create-page-btn").click(function(){
        resetAll();

        // disable the button
        document.querySelector('#to-create-page-btn').disabled = true;
        // show the page
        $("#create-page").show();
    })

    $("#to-read-page-btn").click(function(){
        resetAll();
        // disable the button
        document.querySelector('#to-read-page-btn').disabled = true;
        // show the page
        $("#read-page").show();
    });

    $("#to-update-page-btn").click(function(){
        resetAll();
        // disable the button
        document.querySelector('#to-update-page-btn').disabled = true;
        // show the page
        $("#update-page").show();
    });

    $("#to-delete-page-btn").click(function(){
        resetAll();
        // disable the button
        document.querySelector('#to-delete-page-btn').disabled = true;
        // show the page
        $("#delete-page").show();
    });

    $("#to-read-by-item-id-page-btn").click(function(){
        resetAll();
        // disable the button
        document.querySelector('#to-read-by-item-id-page-btn').disabled = true;
        // show the page
        $("#read-by-item-id-page").show();
    });

    $("#to-read-by-order-status-page-btn").click(function(){
        resetAll();
        // disable the button
        document.querySelector('#to-read-by-order-status-page-btn').disabled = true;
        // show the page
        $("#read-by-order-status-page").show();
    });
})