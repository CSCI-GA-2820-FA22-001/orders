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

    function update_form_data_item(res) {
        console.log(`res:` + res)
        $("#order_id_for_item").val(res.order_id);
        $("#item_id").val(res.item_id);
    }

    /// Clears all order form fields
    function clear_form_data_order() {
        $("#order_id").val("");
        $("#user_id").val("");
        $("#create_time").val("");
        $("#items").val("");
        // $("#status").val("Created");
    }

    /// Clears all item form fields
    function clear_form_data_item() {            
        $("#order_id_for_item").val("");
        $("#item_id").val("");
        $("#item_detail").val("");
    }

    // Updates rows in order table
    function update_order_table(orders) {
        $("#search_results").empty();
        let table = `<table class="table table-striped">`
        table += `<thead>`
        table += `<tr>`
        table += `<th class="col-md-1">Order ID</th>`
        table += `<th class="col-md-4">User ID</th>`
        table += `<th class="col-md-4">Create Time</th>`
        table += `<th class="col-md-3">Status</th>`
        table += `</tr>`
        table += `</thead>`
        table += `<tbody>`

        let firstOrder = ""
        for (let i = 0; i < orders.length; i++) {
            let order = orders[i];
            table += `<tr id="row=${i}"> <td>${order.id}</td>` 
            table += `<td>${order.user_id}</td>`
            table += `<td> ${order.create_time} </td>`
            table += `<td> ${order.status} </td>`
            table += `</tr>`
            if (i == 0) {
                firstOrder = order;
            }
        }
        table += '</tbody></table>'
        $("#search_results").append(table);

        if (firstOrder != "") {
            update_form_data_order(firstOrder)
        }
    }

    // Updates items in item table
    function update_item_table(items) {
        $("#search_results_item").empty();
        let table = `<table class="table table-striped">`
        table += `<thead>`
        table += `<tr>`
        table += `<th class="col-md-1">Order ID</th>`
        table += `<th class="col-md-4">Item ID</th>`
        table += `</tr>`
        table += `</thead>`
        table += `<tbody>`

        let firstItem = ""
        for (let i = 0; i < items.length; i++) {
            let item = items[i];
            table += `<tr id="row=${i}"> <td>${item.order_id}</td>` 
            table += `<td>${item.item_id}</td>`
            table += `</tr>`
            if (i == 0) {
                firstItem = item;
            }
        }
        table += '</tbody></table>'
        $("#search_results_item").append(table);

        if (firstItem != "") {
            update_form_data_item(firstItem)
        }
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
            update_form_data_order(res);
            flash_message("Success");
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
    // Listing Orders
    // ****************************************

    $("#list-order-btn").click(function () {
        let user_id = parseInt($("#user_id").val());

        $("#flash_message").empty();

        let ajax = $.ajax({
            type: "GET",
            url: "/orders?user_id=" + user_id,
            contentType: "application/json",
            // data: JSON.stringify(data),
        });

        ajax.done(function(res){
            console.log(res)
            update_order_table(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    })

    // ****************************************
    // Read an order by status and user id
    // ****************************************

    $("#search-order-by-status-btn").click(function () {
        let order_status = parseInt($("#status").val());
        let user_id = parseInt($("#user_id").val());
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/" + user_id + "/" + status,
        });

        ajax.done(function(res){
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // List all items id an order by order id
    // ****************************************

    $("#get-item-btn").click(function () {
        let order_id = parseInt($("#order_id_for_item").val());

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id + "/items",
        });

        ajax.done(function(res){
            update_item_table(res)
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Read an order by status and user id
    // ****************************************

    $("#search-order-by-status-btn").click(function () {
        let order_status = parseInt($("#status").val());
        let user_id = parseInt($("#user_id").val());
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/" + user_id + "/" + order_status,
        });

        ajax.done(function(res){
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // List all items id an order by order id
    // ****************************************

    $("#get-item-btn").click(function () {
        let order_id = parseInt($("#order_id_for_item").val());

        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "GET",
            url: "/orders/" + order_id + "/items",
        });

        ajax.done(function(res){
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
    // Update an item in an order by order id and item id
    // ****************************************

    $("#update-item-btn").click(function () {
        let item_id = parseInt($("#item_id").val());
        let order_id = parseInt($("#order_id_for_item").val());
        let item_json = $("#item_detail").val()
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "PUT",
            url: "/orders/" + order_id+ "/items/" + item_id,
            data: JSON.stringify(item_json),
        });

        ajax.done(function(res){
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    // ****************************************
    // Cancel an order
    // ****************************************

    $("#cancel-order-btn").click(function () {
        let order_id = parseInt($("#order_id").val());
        let status = status2int($("#status").val());
        $("#flash_message").empty();

        let status_json = {
            "status": status
        }

        let ajax = $.ajax({
            type: "POST",
            url: "/orders/" + order_id+ "/cancel",
            data: JSON.stringify(status_json),
        });

        ajax.done(function(res){
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

    // ****************************************
    // Add an item to order
    // ****************************************

    $("#add-item-btn").click(function () {
        let order_id = parseInt($("#order_id").val());
        let item_id = parseInt($("#item_id").val());
        console.log(`Order ID: ${order_id} ; Item ID: ${item_id} `);
        $("#flash_message").empty();
        
        let data = {
            "order_id": order_id,
            "item_id": item_id
        };
        console.log(`data:` + JSON.stringify(data));

        let ajax = $.ajax({
            type: "POST",
            url: "/orders/" + order_id + "/items",
            contentType: "application/json",
            data: JSON.stringify(data),
        });

        ajax.done(function(res){
            clear_form_data_order()
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    $("#clear-order-btn").click(function () {
        clear_form_data_order()
    });

    $("#clear-item-btn").click(function () {
        clear_form_data_item()
    });

    // ****************************************
    // Delete an item in and order by order id and item id
    // ****************************************

    $("#delete-item-btn").click(function () {
        let item_id = parseInt($("#item_id").val());
        let order_id = parseInt($("#order_id_for_item").val());
        $("#flash_message").empty();
        
        let ajax = $.ajax({
            type: "DELETE",
            url: "/orders/" + order_id+ "/items/" + item_id
        });

        ajax.done(function(res){
            flash_message("Success")
        });

        ajax.fail(function(res){
            flash_message(res.responseJSON.message)
        });
    });

    
})

