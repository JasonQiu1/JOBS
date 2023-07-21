import express from "express";
import job_db from "../connect.mjs";
import { ObjectId } from "mongodb";
import { spawnSync } from "child_process";
import { resolve } from "path";

const router = express.Router();

// This section will help you get a list of all the records.
router.get("/", async (req, res) => {
    let collection = await job_db.collection(process.env.COLLECTION_NAME);
    let results = await collection.find({}).limit(req.body.num_records).toArray();
    res.send(results).status(200);
});

// This section will help you get a single record by id
router.get("/:id", async (req, res) => {
    let collection = await job_db.collection(process.env.COLLECTION_NAME);
    let query = {_id: new ObjectId(req.params.id)};
    let result = await collection.findOne(query);

    if (!result) res.send("Not found").status(404);
    else res.send(result).status(200);
});

// This section will help you create a new record.
router.post("/", async (req, res) => {
    if (req.body.hasOwnProperty("update_jobdb")) {
        console.log("Updating local job database...");
        const update_jobdb_proc = spawnSync('cmd', ['/s','/c','cd .. & python ./update_jobsdb.py'], {encoding:'utf-8',windowsVerbatimArguments:true,shell:true})
        console.log(update_jobdb_proc.stdout); 
        console.log(update_jobdb_proc.stderr); 

        // TODO reply with how many new postings found
        res.send("Finished updating database!").status(204);
    } else if (req.body.hasOwnProperty("num_records")) {
        console.log("Fetching " + req.body.num_records + " records...")
        let collection = await job_db.collection(process.env.COLLECTION_NAME);
        let results = await collection.find({}).limit(req.body.num_records).toArray();
        console.log("Done!")
        res.send(results).status(200);
    }else {
        let newDocument = {
            name: req.body.name,
            position: req.body.position,
            level: req.body.level,
        };
        let collection = await job_db.collection(process.env.COLLECTION_NAME);
        let result = await collection.insertOne(newDocument);
        res.send(result).status(204);
    }
});

// This section will help you update a record by id.
router.patch("/:id", async (req, res) => {
    const query = { _id: new ObjectId(req.params.id) };
    const updates =    {
        $set: {
            name: req.body.name,
            position: req.body.position,
            level: req.body.level
        }
    };

    let collection = await job_db.collection(process.env.COLLECTION_NAME);
    let result = await collection.updateOne(query, updates);

    res.send(result).status(200);
});

// This section will help you delete a record
router.delete("/:id", async (req, res) => {
    const query = { _id: new ObjectId(req.params.id) };

    const collection = job_db.collection(process.env.COLLECTION_NAME);
    let result = await collection.deleteOne(query);

    res.send(result).status(200);
});

export default router;
