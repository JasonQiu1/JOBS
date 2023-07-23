import React, { useEffect } from "react";
  
// We use Route in order to define the different routes of our application
import { Route, Routes } from "react-router-dom";
  
// We import all the components we need in our app
import Navbar from "./components/navbar";
import RecordList from "./components/record_list";
//import Edit from "./components/edit";
import Create from "./components/create";
import UpdateDB from "./components/update_jobdb";

import './styles.css'
  
const App = () => {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route exact path="/" element={<RecordList />} />
        <Route path="/create" element={<Create />} />
        <Route path="/updatedb" element={<UpdateDB />} />
      </Routes>
    </div>
  );
};
  
export default App;
