const {spawn, ChildProcess} = require('child_process');
const bodyParser = require('body-parser')
const express = require('express');
const path = require('path');
const fs = require('fs')
const app = express();
const PORT = 5000;

app.use(bodyParser.urlencoded({ extended: false }))
app.use(bodyParser.json())
app.use('/', express.static('site'))

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, './index.html'));
});

app.get('/api/importarcoches', (req, res) => {
    const url = req.body.url
    var pythonResult;

    if (!url) {
        return res.status(400).send({
            error: "Bad request"
        })
    }
    const pythonJSON = spawn(
        'python3', 
        [
            'pythonScripts/pyScraper.py', 
            '"' + url + '"'
        ]);

    pythonJSON.stdout.on('data', (data) => {
        pythonResult = JSON.parse(data.toString())
    });
    pythonJSON.on('close', (code) => {
        console.log(`\nPython script exited with code ${code}`);
        
        if (code == 0) {
            try {
                const pythonPDF = spawn(
                    'python', 
                    [
                        'pythonScripts/htmlToPDF.py', 
                        '"' + pythonResult.pdf + '"'
                    ], {
                        detached: true,
                        stdio: ['ignore']
                    });
                pythonPDF.unref();
        
                pythonResult.pdf = path.basename(pythonResult.pdf).replace('.html', '.pdf') 
                res.status(200).send({
                    "result": 1,
                    "err": "",
                    "data": pythonResult,
                })
            } catch (TypeError) {
            }
        } else if (code == 1) {
            res.status(200).send({
                "result": 0,
                "err": "Pagina no encontrada",
                "data": null,
            })
        } 
    });
});

app.get('/api/downloadpdf', (req, res) => {
    const name = req.body.filename
    const file_path = path.join('files', name)
    console.log("\nDownloading file...")

    if (fs.existsSync(file_path)) {
        res.status(200).download(file_path, name);        
    } else {
        res.status(404).send({"Error": "File not found"})
    }
    
});

app.listen(
    PORT,
    () => console.log('http://localhost:5000')
)