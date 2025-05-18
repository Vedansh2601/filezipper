const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

app.use(cors());
app.use(bodyParser.text());
app.use(express.static("uploads"));
app.use(express.static("compressed"));

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

// Use Routes
const rleRoutes = require("./routes/rleRoutes");
const lzwRoutes = require("./routes/lzwRoutes");
const decompressRoutes = require("./routes/decompressRoutes");

app.use("/rle", rleRoutes);              // e.g., POST /rle/upload
app.use("/lzw", lzwRoutes);              // e.g., POST /lzw/upload
app.use("/decompress", decompressRoutes); // e.g., GET /decompress

app.listen(3000, () => {
  console.log("Server running on http://localhost:3000");
});
