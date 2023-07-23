import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import ReadMore from "./read_more";
import parse, { domToReact } from "html-react-parser";

const parse_options = {
    replace: ({ name, children }) => {
        if (name == 'a') {
            return <p>{domToReact(children, parse_options)}</p>;
        }
    }
};
  
const Record = (props) => [
  <div id={props.record._id}></div>,
  <tr className='row_header' key={props.record._id + 'info'}>
	<td><a target={"_blank"} href={props.record.job_info.link}>{props.record.job_info.title}</a></td>
	<td>{props.record.job_info.company}</td>
    <td>
      <Link className="btn btn-link" to={`/edit/${props.record._id}`}>Edit</Link> |
      <button className="btn btn-link"
        onClick={() => {
          props.deleteRecord(props.record._id);
        }}
      >
        Delete
      </button>
    </td>
  </tr>,
  <tr key={props.record._id + 'description'}>
    <td>
        <ReadMore lines={10} id={props.record._id}><div>{parse(props.record.job_info.description, parse_options)}</div></ReadMore>
    </td>
  </tr>
];
  
export default function RecordList() {
  const [records, setRecords] = useState([]);
  
  // This method fetches the records from the database.
  useEffect(() => {
    async function getRecords() {
      const response = await fetch(`http://localhost:5050/record/`, {
          method: 'POST',
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({num_records:50})
      });
  
      if (!response.ok) {
        const message = `An error occurred: ${response.statusText}`;
        window.alert(message);
        return;
      }
  
      const records = await response.json();
      setRecords(records);
    }
  
    getRecords();
  
    return;
  }, [records.length]);
  
  // This method will delete a record
  async function deleteRecord(id) {
    await fetch(`http://localhost:5050/record/${id}`, {
      method: "DELETE"
    });
  
    const newRecords = records.filter((el) => el._id !== id);
    setRecords(newRecords);
  }
  
  // This method will map out the records on the table
  function recordList() {
    return records.map((record) => {
      return (
        <Record key={record._id}
          record={record}
          deleteRecord={() => deleteRecord(record._id)}
          key={record._id}
        />
      );
    });
  }
  
  // This following section will display the table with the records of individuals.
  return (
    <div>
      <h3>Record List</h3>
      <table className="table table-striped" style={{ marginTop: 20 }}>
        <thead>
          <tr>
            <th>Title</th>
            <th>Company</th>
            <th>Options</th>
          </tr>
        </thead>
        <tbody>{recordList()}</tbody>
      </table>
    </div>
  );
}
