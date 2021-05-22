$(document).ready(function () {
    $("#TotalItem").text("0.00 €");
    $('#quatityitem').on('change keyup', function () {
        var quantity = $('#quatityitem').val();
        var price = $('#priceItem').val();
        var total = quantity * price;
        $("#TotalItem").text(total + " €");
    });

    var retrievedObject = localStorage.getItem('cartObject');
    console.log('retrievedObject: ', JSON.parse(retrievedObject));
    var cartObject = JSON.parse(retrievedObject);
    if (cartObject) {
        $('table#tableCart tr#defaultrow').remove();
        //add elements of arreglo
        var totalToPay = 0.00;
        for (var i = 0; i < cartObject.length; i++) {
            totalToPay = totalToPay + parseFloat((cartObject[i].price * cartObject[i].quantity));
        }
        $('#valueTot').text(totalToPay + " €");

        for (var i = 0; i < cartObject.length; i++) {
            var table = document.getElementById("tableCart");
            if (table) {
                var row = table.insertRow(-1); // -1 indica que los rows o filas se iran agregando al final de la tabla
                var ColName = row.insertCell(0); // posicion de columna 0 -> primera 1 -> segunda
                var ColDescription = row.insertCell(1);
                var ColQuantity = row.insertCell(2); // posicion de columna 0 -> primera 1 -> segunda
                var ColPrice = row.insertCell(3);
                var ColTotal = row.insertCell(4);
                var ColImage = row.insertCell(5);
                var ColAction = row.insertCell(6);
                ColName.innerHTML = cartObject[i].name; //seteando los valores a los nuevos rows
                ColDescription.innerHTML = cartObject[i].description;
                ColQuantity.innerHTML = cartObject[i].quantity;
                ColPrice.innerHTML = cartObject[i].price + " €";
                ColTotal.innerHTML = cartObject[i].total + " €";
                ColImage.innerHTML = '<img src=' + cartObject[i].pathImage + ' style="height:200px;width:200px">';
                ColAction.innerHTML = '<span style="height: 34px; width: 34px;" class="btn-ripple animate"></span> <i onclick="DeleteLine(this)" class="fa fa-trash" data-toggle="tooltip" title="" data-original-title="Delete item"></i>';
            }
        }
    }else{
        $('#valueTot').text(" 0.00€");
    }
});

let arrayObjectCart = [], objectCart = {};

function AddCartItem() {
    var retrievedObject = localStorage.getItem('cartObject');

    var quantity = $('#quatityitem').val();
    var price = $('#priceItem').val();
    var total = quantity * price;
    var name = $("#cartName").text();
    var pathImg = $('#pathImage').val();
    var id = $('#idItem').val();
    var description = $('#descriptionItem').val();
    objectCart = {
        id: id,
        description: description,
        quantity: quantity,
        price: price,
        total: total,
        name: name,
        pathImage: pathImg
    }
    if (retrievedObject) {
        arrayObjectCart = JSON.parse(retrievedObject);
        arrayObjectCart.push(objectCart);
        localStorage.setItem('cartObject', JSON.stringify(arrayObjectCart));
    } else {
        arrayObjectCart.push(objectCart);
        localStorage.setItem('cartObject', JSON.stringify(arrayObjectCart));
    }
    //add elements of array
    var totalToPay = 0.00;
    for (var i = 0; i < arrayObjectCart.length; i++) {
        totalToPay = totalToPay + parseFloat((arrayObjectCart[i].price * arrayObjectCart[i].quantity));
    }
    $('#valueTot').text(totalToPay + " €");
    $('#CartModalItem').modal('hide');
}


function OpenPreviewCart(id, price, name, pathImage, description) {
    $("#CartModalItem").modal("toggle");
    $('#priceItem').val(price);
    $("#priceItem").text(price);
    $("#cartName").text(name);
    $("#previewToCart").attr("src", pathImage);
    $('#pathImage').val(pathImage);
    $('#idItem').val(id);
    $('#descriptionItem').val(description);

}


function ClearCartAction() {
    window.localStorage.clear();
    location.reload();
}

function DeleteLine(element) {
    var retrievedObject = localStorage.getItem('cartObject');
    var Row = element.parentNode.parentNode.rowIndex; //method to get object to delete
    var name = "";
    var quantity = "";
    var index = 0;
    $('table tr:eq("' + Row + '") td').each(function () {
        if (index === 0) { // columna 1
            name = $(this).text();
        } else if (index === 2) { //columna 2
            quantity = $(this).text();
        }
        index++;
    });

    arrayObjectCart = JSON.parse(retrievedObject);

    //delete object in array
    arrayObjectCart.splice(arrayObjectCart.findIndex(matchesEl), 1);

    function matchesEl(el) { //search element in array
        return (el.name === name && el.quantity === quantity);
    }

    document.getElementById("tableCart").deleteRow(Row); // eliminacion de elemento de la tabla

    //knowing total
    //sum elements of array
    var totalToPay = 0.00;
    for (var i = 0; i < arrayObjectCart.length; i++) {
        totalToPay = totalToPay + parseFloat((arrayObjectCart[i].price * arrayObjectCart[i].quantity));
    }
    $('#valueTot').text(totalToPay + " €");

    //update  local storage
    localStorage.setItem('cartObject', JSON.stringify(arrayObjectCart));


    var TablaLineas = document.getElementById("tableCart");
    var rowCount = TablaLineas.rows.length;
    if (rowCount === 1) {
        $('#tableCart').append('<tr id="defaultrow"><td colspan="3"><span style="padding-left: 30%;">No items added to cart</span></td></tr>');
    }
}
