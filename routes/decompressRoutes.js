const express = require("express");
const router = express.Router();

router.get("/", (req, res) => {
  const input = req.headers.input;
  if (!input) return res.json({ msg: "nothing to decompress" });

  let decompress = "";
  for (let i = 0; i < input.length;) {
    let char = input[i++];
    let numStr = "";
    while (i < input.length && !isNaN(input[i])) {
      numStr += input[i++];
    }
    decompress += char.repeat(parseInt(numStr));
  }

  res.send(decompress);
});

module.exports = router;
