function setSlug(){
    const inputTitle = document.getElementById('id_title');
    const inputSlug = document.getElementById('id_slug');
    inputSlug.value = slugify(inputTitle.value)
}

const inputElements = document.getElementsByTagName('input');
inputElements.forEach(element => {
    element.classList.add('mt-1');
});

document.addEventListener('DOMContentLoaded', function() {
    const quillContainer = document.querySelector('#quill-editor');
    const hiddenInput = document.querySelector('#description');

    // Get the already initialized Quill instance
    const quill = Quill.find(quillContainer);

    // If editing an existing object, set initial content
    quill.root.innerHTML = hiddenInput.value || quillContainer.textContent.trim();

    // Sync content before form submission
    quillContainer.closest('form').addEventListener('submit', function() {
      hiddenInput.value = quill.root.innerHTML;
    });
});