const express = require('express');
const {spawn} = require('child_process');
const bodyParser = require('body-parser')
const app = express();
const PORT = 5000;

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())

app.get('/', (req, res) => {
    res.status(200).send(`
        test
    `);
});

app.get('/api/importarcoches', (req, res) => {
    console.log("----------------------------") 
    const url = req.body.url
    const path = req.body.PDFpath
    var test;
    if (!url) {
        return res.status(400).send({
            error: "Bad request"
        })
    }
    const python = spawn(
        'python', 
        [
            'pythonScripts/pyScraper.py', 
            '"' + url + '"',
            path
        ]);
    python.stdout.on('data', (data) => {
        test = JSON.parse(data.toString())
    });

    python.on('close', (code) => {
        console.log(`Python script exited with code ${code}`);
        res.status(200).send({
            data: test
        })
    });
});

app.get('/downloadpdf', (req, res) => {
    res.status(200).download('test.py');
});



app.listen(
    PORT,
    () => console.log('http://localhost:5000')
)