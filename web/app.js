const express = require('express')
const path = require('path')
const app = express()
const port = 3000;

app.use(express.json())

app.get("/novel/:name/chapter/:id", (req, res) => {
    res.sendFile(path.join(__dirname, '..', '..', 'Database', req.params.name, 'html', 'chapter_' + req.params.id + '.html'))
})

app.get("/novel/:name/img/:fname", (req, res) => {
    res.sendFile(path.join(__dirname, '..', '..', 'Database', req.params.name, 'img', req.params.fname))
})

app.get("/src/js/src.js", (req, res) => {
    res.sendFile(path.join(__dirname, 'javascript', 'src.js'))
})

app.listen(3000, () => {
    console.log("Server is running on port 3000")
})