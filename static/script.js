function remove_task(event) {
    const id = event.target.parentNode.parentNode.id
    fetch('/remove/' + id).then(response => window.location.reload())
}

function toggleModal(event) {
    const el = document.getElementsByTagName('form')[0]
    if (el.style.display == 'block') {
        el.style.display = 'none'
    } else {
        el.style.display = 'block'
    }
    }
    
    const a = document.getElementById('form-toggler')
    a.addEventListener('click', toggleModal)
    // .then(response => console.log(response))