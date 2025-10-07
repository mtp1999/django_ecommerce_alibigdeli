async function deleteProfileImage(url, csrf_token) {
    const formData = new FormData();
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
        window.location.reload();
    } catch (error) {
        console.log(error);
    }
};
