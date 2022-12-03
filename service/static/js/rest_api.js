$(function () {

    // ****************************************
    //  U T I L I T Y   F U N C T I O N S
    // ****************************************

    // Updates the form with data from the response
    function status2int(status) {
        if (status == "created")  {
            return 1;
        }
        if (status == "completed") {
            return 2;
        }
        if (status == "cancelled") {
            return 3;
        }
        return 0;
    }

    function int2status(status) {
        if (status == 1) {
            return "created";
        }
        if (status == 2) {
            return "completed";
        }
        if (status == 3) {
            return "cancelled";
        }
        return "unknown";
    }
    
    function update_form_data_order(res) {
        console.log(`res:` + res)
        $("#order_id").val(res.id)
        $("#user_id").val(res.user_id);
        $("#create_time").val(res.create_time);
        $("#items").val(res.items);
        $("#status").val(int2status(res.status));
    }

    /// Clears all form fields
    function clear_form_data_order() {
        $("#order_id").val("");
        $("#user_id").val("");
        $("#create_time").val("");
        $("#items").val("");
        $("#status").val("");
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
        console.log(`data:` + JSON.stringify(data));
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data_order(res)
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
    // Create a Order
    // ****************************************

    $("#create-order-btn").click(function () {
        let user_id = parseInt($("#user_id").val());
        let create_time = Math.floor(Date.now() / 1000);
        let items = [];
        if ($("#items").val().length > 0) {
            items = $("#items").val().split(",");
        }

        let data = {
            "user_id": user_id,
            "create_time": create_time,
            "items": items,
            "status": 1
        };
        console.log(`data:` + JSON.stringify(data));

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "POST",
            url: "/orders",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data_order(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Read an order by order id
    // ****************************************

    $("#retrieve-order-btn").click(function () {
        let order_id = parseInt($("#order_id").val());
        console.log(`Order ID: ${order_id}`);
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id,
        });

        ajax.done(function(res){
            update_form_data_order(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Update an order by order id
    // ****************************************

    $("#update-order-btn").click(function () {
        let order_id = parseInt($("#order_id").val());
        let user_id = parseInt($("#user_id").val());
        let status = status2int($("#status").val());
        let create_time = Math.floor(Date.now() / 1000);
        let items = [];
        if ($("#items").val().length > 0) {
            items = $("#items").val().split(",");
        }

        $("#flash_message").empty();
        
        let data = {
            "user_id": user_id,
            "create_time": create_time,
            "status": status,
            "items": items
        };
        console.log(`status:` + $("#status").val());
        console.log(`data:` + JSON.stringify(data));

        let ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id,
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            update_form_data_order(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Delete an order by order id
    // ****************************************

    $("#delete-order-btn").click(function () {
        let order_id = parseInt($("#order_id").val());
        console.log(`Order ID: ${order_id}`);
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id,
        });

        ajax.done(function(res){
            clear_form_data_order()
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });
})