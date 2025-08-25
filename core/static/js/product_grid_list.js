const params = new URLSearchParams(window.location.search);
const title_q = document.getElementById("title_q");
const category = document.getElementById("product_category");
const min_price = document.getElementById("min_price");
const max_price = document.getElementById("max_price");
const paginated_by = document.getElementById("paginated_by");
const order_by = document.getElementById("order_by");
const form = document.getElementById("filter_form1");

title_q.value = params.get("title_q");
category.value = params.get("product_category");
min_price.value = params.get("min_price");
max_price.value = params.get("max_price");
paginated_by.value = params.get("paginated_by");
order_by.value = params.get("order_by");


document.addEventListener("DOMContentLoaded", function () {
    if (paginated_by) {
            paginated_by.addEventListener("change", function () {
            const value = this.value;
            const url = new URL(window.location.href);
            if (value) {
                url.searchParams.set("paginated_by", value);
                url.searchParams.delete("page");
            }
            window.location.href = url.toString();
            console.log(url.toString());
        });
    };
    if (order_by) {
            order_by.addEventListener("change", function () {
            const value = this.value;
            const url = new URL(window.location.href);
            if (value) {
                url.searchParams.set("order_by", value);
                url.searchParams.delete("page");
            }
            window.location.href = url.toString();
            console.log(url.toString());
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {

  form.addEventListener("submit", function (e) {
    e.preventDefault(); // stop normal submission

    // Get current URL
    const url = new URL(window.location.href);

    // Loop through all form fields
    const formData = new FormData(form);
    for (const [key, value] of formData.entries()) {
    url.searchParams.delete("page");
      if (value) {
        url.searchParams.set(key, value); // update or add parameter
      } else {
        url.searchParams.delete(key); // remove if empty
      }
    }

    // Navigate to the updated URL
    window.location.href = url.toString();
  });
});