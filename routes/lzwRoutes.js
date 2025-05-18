const express = require("express");
const router = express.Router();
const multer = require("multer");
const { exec } = require("child_process");
const fs = require("fs");

const storage = multer.diskStorage({
  destination: (req, res, cb) => cb(null, "uploads/"),
  filename: (req, file, cb) => cb(null, Date.now() + "_" + file.originalname),
});
const upload = multer({ storage });

router.post("/upload", upload.single("file"), (req, res) => {
  const filepath = req.file.path;
  const pythonScriptPath = "lzw_utils1.py";

  const command = `python3 ${pythonScriptPath} ${filepath}`;

  exec(command, (error, stdout, stderr) => {
    if (error) return res.status(500).json({ message: "Compression failed" });

    try {
      const result = JSON.parse(stdout);

      if (result.error) {
        return res.status(400).json({ message: result.error });
      }

      const filename = `${Date.now()}_compressed.txt`;
      const outputPath = `compressed/${filename}`;

      fs.writeFile(outputPath, result.compressed, (err) => {
        if (err)
          return res.status(500).json({ message: "Failed to save compressed file" });

        res.json({
          message: "Compression successful",
          bitLength: result.bit_length,
          downloadLink: `http://localhost:3000/${filename}`,
        });
      });
    } catch (e) {
      res.status(500).json({ message: "Invalid Python output" });
    }
  });
});

module.exports = router;
