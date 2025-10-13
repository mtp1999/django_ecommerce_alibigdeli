async function addToCart(product_id, url, csrf_token, reload_page=false) {
    const formData = new FormData();
    formData.append("product_id", product_id);
    formData.append("csrfmiddlewaretoken", csrf_token);
    try {
        const res = await fetch(url, {
            method: "POST",
            body: formData,
        });

        if (!res.ok) {
            throw new Error(`Error, Http status code: ${res.status}`)
        }
        const response_data = await res.json();
        const quantity_element = document.getElementById("cart_total_quantity");
        quantity_element.innerText = response_data.quantity;
        if (reload_page) {
            window.location.reload();
        }
    } catch (error) {
        console.log(error);
    }
};

async function removeProductFromCart(product_id, url, csrf_token) {
    const formData = new FormData();
    formData.append("product_id", product_id);
    formData.append("csrfmiddlewaretoken", csrf_token);
    try {
        const res = await fetch(url, {
            method: "POST",
            body: formData,
        });

        if (!res.ok) {
            throw new Error(`Error, Http status code: ${res.status}`)
        }
        window.location.reload();

    } catch (error) {
        console.log(error);
    }
};

async function ChangeProductQuantityInCart(product_id, quantity, url, csrf_token) {
    const formData = new FormData();
    formData.append("product_id", product_id);
    formData.append("quantity", quantity);
    formData.append("csrfmiddlewaretoken", csrf_token);
    try {
        const res = await fetch(url, {
            method: "POST",
            body: formData,
        });

        if (!res.ok) {
            throw new Error(`Error, Http status code: ${res.status}`)
        }
        window.location.reload();

    } catch (error) {
        console.log(error);
    }
};