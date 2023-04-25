document.addEventListener("DOMContentLoaded", () => {
    setupListeners()
});

function setupListeners() {
    /*
    * Handling item count increment and decrement
    * */
    const decrementBtn = document.querySelector("#decrementItem")
    const incrementBtn = document.querySelector("#incrementItem")

    incrementBtn.addEventListener("click", () => {
        let quantity = document.querySelector("#quantity")
        if (isNaN(+quantity.value)) {
            quantity.value = 1
        } else {
            quantity.value = +quantity.value + 1
        }
    })

    decrementBtn.addEventListener("click", () => {
        let quantity = document.querySelector("#quantity")
        if (isNaN(+quantity.value) || +quantity.value <= 1) {
            quantity.value = 1
        } else {
            quantity.value = +quantity.value - 1
        }
    })

    document.querySelector("#addToCart").addEventListener("click", () => {
        /*
        * Cart items add handling
        * Add Items and items quantity to localStorage
        * */
        let productId = document.querySelector("#productId").innerHTML
        let quantity = document.querySelector("#quantity").value

        if (localStorage.getItem("cart")) {
            let cart = JSON.parse(localStorage.getItem("cart"))
            if (!cart.filter(item => item.productId === productId).length) {
                cart = [{productId, quantity: +quantity}, ...cart]
                alert("Товар был добавлен в корзину")
            } else {
                let index = cart.findIndex(item => item.productId === productId)
                if (index !== -1) {
                    cart[index].quantity += +quantity
                    alert("Количество товара в корзине было успешно изменено!")
                }
            }
            localStorage.removeItem("cart")
            localStorage.setItem("cart", JSON.stringify(cart))
        } else {
            localStorage.setItem("cart", JSON.stringify([{productId, quantity: +quantity}]))
            alert("Товар был добавлен в корзину")
        }
    })
}
