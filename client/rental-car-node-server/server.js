const express = require('express');
const path = require('path');

const app = express();
const PORT = process.PORT || '3000';
const HOST = '0.0.0.0';

const dirRentalCarApp = 'build/rental_car_app'

app.use(express.static(path.join(__dirname), dirRentalCarApp))

app.get('*', (req, res) => {
    res.sendFile(path.join(__dirname, dirRentalCarApp, 'index.html'))
})

app.listen(PORT, HOST, () => {
    console.log(`Node server started, addresses: `);
    console.log(`- local address: http://localhost:${PORT}`);
    console.log(`- lan address: http://${HOST}:${PORT}`);
})
