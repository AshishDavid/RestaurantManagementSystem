$(document).ready(function () {
    $('#quatityitem').on('change keyup', function () {
        var cantidad = $('#quatityitem').val();
        var precio = $('#priceItem').val();
        var total = cantidad * precio;
        $("#TotalItem").text(total + " €");
    });

});




function AddCartItem(id, price, name, pathImage) {
    $("#CartModalItem").modal("toggle");
    $('#priceItem').val(price);
    $("#priceItem").text(price);
    $("#cartName").text(name);
}

