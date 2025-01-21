const express = require('express')
const path = require('path')
const app = express()
const port = 3000;

app.use(express.json())

app.get("/novel/chapter/:id", (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'html', 'chapter_' + req.params.id + '.html'))
})

app.get("/novel/img/:id", (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'img', req.params.id))
})

app.get("/src/js/src.js", (req, res) => {
    res.sendFile(path.join(__dirname, 'src', 'js', 'src.js'))
})

app.listen(3000, () => {
    console.log("Server is running on port 3000")
})