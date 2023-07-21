import express from "express";
import cors from "cors";
import "./load_environment.mjs";
import router from "./routes/record.mjs";

const PORT = process.env.PORT || 5050;
const app = express();

app.use(cors());
app.use(express.json());

app.use("/record", router);
app.use("/update_jobdb_exec", router);

app.listen(PORT, () => {
    console.log(`Server is running on port: ${PORT}`);
})
