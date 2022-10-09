const axios = require("axios");
const cheerio = require("cheerio");
const express = require("express");

const PORT = 8000;

const app = express();

app.listen(PORT, () => console.log(`server running on PORT ${PORT}`));
