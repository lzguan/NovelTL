images = document.querySelectorAll('img');
console.log(window.location.href);
for (let i = 0; i < images.length; i++) 
{
    fetch(window.location.protocol + "//" + window.location.host + "/novel/img/" + images[i].id)
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to fetch image');
        }
        return response.blob()
    })
    .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        images[i].src = imageUrl;
    })
    .catch(error => {
        console.error('Error loading image:' + error)
    })
}
nextbtn = document.querySelectorAll('button.next')
for (let i = 0; i < nextbtn.length; i++) {
    nextbtn[i].addEventListener('click', () => {
        const curUrl = new URL(window.location.href)
        console.log(curUrl)
        path = curUrl.pathname.split('/').filter(Boolean)
        last = path.pop()
        newlast = parseInt(last, 10) + 1
        path.push(newlast)
        console.log(path.join('/'))
        console.log(window.location.host)
        const newUrl = new URL(path.join('/'), window.location.protocol + "//" + window.location.host)
        window.location.href = newUrl
    })
}    

prevbtn = document.querySelectorAll('button.previous')
for (let i = 0; i < prevbtn.length; i++) {
    prevbtn[i].addEventListener('click', () => {
        const curUrl = new URL(window.location.href)
        console.log(curUrl)
        path = curUrl.pathname.split('/').filter(Boolean)
        last = path.pop()
        newlast = parseInt(last, 10) - 1
        path.push(newlast)
        console.log(path.join('/'))
        console.log(window.location.host)
        const newUrl = new URL(path.join('/'), window.location.protocol + "//" + window.location.host)
        window.location.href = newUrl
    })
}    