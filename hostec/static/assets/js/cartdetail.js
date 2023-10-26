function updateTotal() {
    var allSubCostElements = document.querySelectorAll('.allSubCost');
    var allSubQuantityElements = document.querySelectorAll('.allSubQuantity');
    var totalCostElement = document.getElementById('totalCost');
    var totalCost = 0;

    allSubCostElements.forEach(function(element, index) {
        var subCost = parseFloat(element.textContent || element.innerText);
        var quantity = parseInt(allSubQuantityElements[index].textContent || allSubQuantityElements[index].innerText);
        totalCost += (subCost * quantity);
    });

    totalCostElement.innerHTML = '€ ' + totalCost.toFixed(0); 
}


var buttonIncrease = document.getElementsByClassName('increaseCart');
for (var i = 0; i < buttonIncrease.length; i++) {
    buttonIncrease[i].addEventListener('click', function () {
        var cartId = this.getAttribute('data-cartid');
        var cart_token = this.getAttribute('data-csrf')
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', cart_token);
        formData.append('cartid', cartId);
        var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                if (responseData.status === 'success') {
                    var quantityElement = document.querySelector('#cartId-'+cartId);
                    quantityElement.innerHTML = responseData.new_quantity;
                    updateTotal()
                } else {
                    console.error('Error:', responseData.message);
                }
            }
        };
        xhr.open('POST', '/increaseCart/', true); 
        xhr.send(formData);
    });
}

var buttonDecrease = document.getElementsByClassName('decreaseCart');
for (var i = 0; i < buttonDecrease.length; i++) {
    buttonDecrease[i].addEventListener('click', function () {
        var cartId = this.getAttribute('data-cartid');
        var cart_token = this.getAttribute('data-csrf')
        var formData = new FormData();
        formData.append('csrfmiddlewaretoken', cart_token);
        formData.append('cartid', cartId);
        var xhr = new XMLHttpRequest();
        xhr.onload = function () {
            if (xhr.status === 200) {
                var responseData = JSON.parse(xhr.responseText);
                if (responseData.status === 'success') {
                    var quantityElement = document.querySelector('#cartId-'+cartId);
                    quantityElement.innerHTML = responseData.new_quantity;
                    updateTotal()
                } else {
                    console.error('Error:', responseData.message);
                }
            }
        };
        xhr.open('POST', '/decreaseCart/', true); 
        xhr.send(formData);
    });
}

var buttonRemove = document.getElementsByClassName('removeCart');
for (var i = 0; i < buttonRemove.length; i++) {
    buttonRemove[i].addEventListener('click', function () {
        if (window.confirm("Do you really want to remove this product?")) {
            var cartId = this.getAttribute('data-cartid');
            var cartToken = this.getAttribute('data-csrf');
            var formData = new FormData();
            formData.append('csrfmiddlewaretoken', cartToken);
            formData.append('cartid', cartId);
            var xhr = new XMLHttpRequest();
            xhr.onload = function () {
                if (xhr.status === 200) {
                    var responseData = JSON.parse(xhr.responseText);
                    if (responseData.status === 'success') {
                        alert("Remove Cart Success");
                        location.reload()
                    } else {
                        console.error('Error:', responseData.message);
                    }
                }
            };
            xhr.open('POST', '/removeCart/', true); 
            xhr.send(formData);
        }        
    });
}