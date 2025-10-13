function setSlug(){
    const inputTitle = document.getElementById('id_title');
    const inputSlug = document.getElementById('id_slug');
    inputSlug.value = slugify(inputTitle.value)
}

const inputElements = document.getElementsByTagName('input');
inputElements.forEach(element => {
    element.classList.add('mt-1');
});
