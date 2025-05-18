const express = require("express");
const router = express.Router();
const fs = require("fs");
const multer = require("multer");

const storage = multer.diskStorage({
  destination: (req, res, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => cb(null, Date.now() + "_" + file.originalname),
});
const upload = multer({ storage });

router.post("/upload", upload.single("file"), (req, res) => {
  const filepath = req.file.path;
  const originalname = req.file.originalname;

  fs.readFile(filepath, "utf-8", (err, data) => {
    if (err) return res.json({ message: "error reading a file" });

    let compressed = "";
    let count = 1;
    for (let i = 1; i <= data.length; i++) {
      if (data[i - 1] === data[i]) {
        count++;
      } else {
        compressed += data[i - 1] + count;
        count = 1;
      }
    }

    const filename = `${Date.now()}_compressed_${originalname}`;
    const outputPath = `compressed/${filename}`;
    fs.writeFile(outputPath, compressed, (err) => {
      if (err) return res.json({ message: "error saving compressed file" });

      res.json({
        message: "successful",
        downloadLink: `http://localhost:3000/${filename}`,
      });
    });
  });
});

router.get("/text", (req, res) => {
  const input = req.headers.input;
  if (!input) return res.json({ message: "file not found" });

  let compressed = "";
  let count = 1;
  for (let i = 1; i <= input.length; i++) {
    if (input[i - 1] === input[i]) {
      count++;
    } else {
      compressed += input[i - 1] + count;
      count = 1;
    }
  }
  res.send(compressed);
});

module.exports = router;
