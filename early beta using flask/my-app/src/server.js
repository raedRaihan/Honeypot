require("dotenv").config();
const express = require("express");

const app = express();

app.use(express.json());
app.use(express.static("public"));

// Routes go here
app.get('/', function (req, res) {
    res.status(200).send('VERIFIED')
   

});
app.listen(process.env.PORT || 3000 , () => console.log('Welcome'));