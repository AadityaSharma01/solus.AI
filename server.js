import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

const app = express();
const PORT = 5000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

app.use(express.json())
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

let currentVal = null;
let currentTime = null;
app.post("/api/runface", (req, res) => {
    const { time, value } = req.body;
    currentTime = time,
    currentVal = value;
    res.status(200).json({ status: "success" });
})

app.get("/api/runface", (__, res) => {
    res.json({ currentTime, currentVal });
})

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
