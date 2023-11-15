const { exec } = require('child_process');

let sensorValue = '';

// exec('python MQTT_Connection.py', (error, stdout, stderr) => {
//     sensorValue = stdout;
// });

//
// hosting a web-based front-end and respond requests with sensor data
// based on example code on https://expressjs.com/
//
const express = require('express')
const app = express()
const port = 3001

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    res.render('index')
})

app.post('/', (req, res) => {
    res.writeHead(200, {
        'Content-Type': 'application/json'
    });
    exec('python MQTT_Connection.py', (error, stdout, stderr) => {
        sensorValue = stdout;
    });
    res.end(JSON.stringify({
        sensorValue: sensorValue
    }));
})

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})