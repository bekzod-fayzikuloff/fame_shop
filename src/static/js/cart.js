window.onload = function() {
    // function for update cookie can remove and sometimes reload page
    document.cookie = `cart=${localStorage.getItem("cart")}`
    if(!window.location.hash) {
        window.location = window.location + '#loaded';
        window.location.reload();
        document.cookie = `cart=${localStorage.getItem("cart")}`
    }
}

function itemDesc(productId, price) {
    /* Update selected items count and save changes in localStorage <also update cookies for backend> */
    let quantity = document.querySelector(`#cartItemQuantity_${productId}`)
    let totalPrice = document.querySelector(`#cartItemTotal_${productId}`)
    let totalCost = document.querySelector("#totalCost")
    if (!+quantity.innerHTML) {
        return
    }
    quantity.innerHTML = `${+quantity.innerHTML - 1}`
    totalPrice.innerHTML = `${+totalPrice.innerHTML - price}`
    totalCost.innerHTML = `${parseFloat(totalCost.innerHTML) - price}`

    let cart = JSON.parse(localStorage.getItem("cart"))

    let index = cart.findIndex(item => parseInt(item.productId) === productId)
    if (index !== -1) {
        cart[index].quantity -= 1
    }
    localStorage.removeItem("cart")
    localStorage.setItem("cart", JSON.stringify(cart))

}

function itemIncr(productId, price) {
    /* Update selected items count and save changes in localStorage <also update cookies for backend> */
    let quantity = document.querySelector(`#cartItemQuantity_${productId}`)
    let totalPrice = document.querySelector(`#cartItemTotal_${productId}`)
    let totalCost = document.querySelector("#totalCost")

    quantity.innerHTML = `${+quantity.innerHTML + 1}`
    totalPrice.innerHTML = `${parseFloat(totalPrice.innerHTML) + price}`
    totalCost.innerHTML = `${parseFloat(totalCost.innerHTML) + price}`

    let cart = JSON.parse(localStorage.getItem("cart"))

    let index = cart.findIndex(item => parseInt(item.productId) === productId)
    if (index !== -1) {
        cart[index].quantity += 1
    }
    localStorage.removeItem("cart")
    localStorage.setItem("cart", JSON.stringify(cart))
}
