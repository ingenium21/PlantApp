// JavaScript source code
// **********************************************************************************
// Shopping Cart Functions
var PA_shoppingCart = {};

PA_shoppingCart.cart = [name, 0, 0]; //the cart array

// will display name, price, and count
PA_shoppingCart.Item = function (name, price, count) {
    this.name = name;
    this.price = price;
    this.count = count;
};

// addItemToCart Function
PA_shoppingCart.addItemToCart = function (name, price, count) { // add item to cart
    for (var i in this.cart) {
        if (this.cart[i].name === name) {
            this.cart[i].count += count;
            PA_shoppingCart.saveCart();
            return;
        }
    }
    var item = new PA_shoppingCart.Item(name, price, count);
    PA_shoppingCart.cart.push(item);
    this.saveCart();
};

// setCountForItem Function
PA_shoppingCart.setCountForItem = function (name, count) {
    for (var i in this.cart) {
        if (this.cart[i].name === name) {
            this.cart[i].count = count;
            break;
        }
    }
    this.saveCart();
};

// removeItemFromCart Function
PA_shoppingCart.removeItemFromCart = function (name) { // removes one item
    for (var i in this.cart) {
        if (this.cart[i].name === name) {
            this.cart[i].count--; //removes 1 of said item from cart
            if (this.cart[i].count === 0) {
                this.cart.splice(i, 1);
            }

            break;
        }
    }
    this.saveCart();
};
// removeItemFromCartAll(name) -> removes all particular item name
PA_shoppingCart.removeItemFromCartAll = function (name) {
    for (var i in this.cart) {
        if (this.cart[i].name === name) {
            this.cart.splice(i, 1);
            break;
        }
    }
    this.saveCart();
};

// clearCart() -> clears the entire cart
PA_shoppingCart.clearCart = function () {
    this.cart = [];
    this.saveCart();
};

// countCart() -> return total count
PA_shoppingCart.countCart = function () {
    var totalCount = 0;
    for (var i in this.cart) {
        totalCount += this.cart[i].count;
    }
    return totalCount;
};

// totalCart() -> return total cost
PA_shoppingCart.totalCart = function () {
    var totalCost = 0;
    for (var i in this.cart) {
        totalCost += this.cart[i].price * this.cart[i].count;
    }
    return totalCost.toFixed(2);
};

// listCart() -> return array of Item
PA_shoppingCart.listCart = function () {
    var cartCopy = [];
    for (var i in this.cart) {
        var item = this.cart[i];
        var itemCopy = {};
        for (var p in item) {
            itemCopy[p] = item[p];   //this copies name, price, and count
        }
        itemCopy.total = (item.price * item.count).toFixed(2);
        cartCopy.push(itemCopy);
    }
    return cartCopy;
};

// saveCart() -> saves user's cart
PA_shoppingCart.saveCart = function () {
    localStorage.setItem("shoppingCart", JSON.stringify(this.cart));
};

// loadCart() -> loads saved cart

PA_shoppingCart.loadCart = function () {
    this.cart = JSON.parse(localStorage.getItem("shoppingCart"));
    if (this.cart === null) {
        this.cart = [];
    }
};

PA_shoppingCart.loadCart();