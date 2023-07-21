import { MongoClient } from "mongodb";

const connectionString = process.env.JOBDB_URI || "";

const client = new MongoClient(connectionString);

let conn;
try {
  conn = await client.connect();
} catch(e) {
  console.error(e)
}

let job_db = conn.db(process.env.JOBDB_NAME);

// create the job_postings collection if it doesn't exist
job_db.listCollections().toArray(function (err, collectionNames) {
  if (err) {
    console.error(err);
    return;
  }
  if (!collectionNames.includes(process.env.COLLECTION_NAME)) {
    job_db.createCollection(process.env.COLLECTION_NAME, function (err, res) {
      if (err) {
        console.error(err);
        return;
      }
      console.log("Created " + process.env.COLLECTION_NAME + " collection.");
    });
  }
});

export default job_db;
