import React, { useEffect } from "react";
  
// We use Route in order to define the different routes of our application
import { Route, Routes, Switch, useLocation } from "react-router-dom";
  
// We import all the components we need in our app
import Navbar from "./components/navbar";
import RecordList from "./components/record_list";
//import Edit from "./components/edit";
import Create from "./components/create";
import UpdateDB from "./components/update_jobdb";

import './styles.css'
  
const App = () => {
	const { pathname, hash, key } = useLocation();

	useEffect(() => {
        console.log(hash);
		// if not a hash link, scroll to top
		if (hash === '') {
			window.scrollTo(0, 0);
		}
		// else scroll to id
		else {
			setTimeout(() => {
				const id = hash.replace('#', '');
				const element = document.getElementById(id);
				if (element) {
					element.scrollIntoView();
				}
			}, 0);
		}
	}, [pathname, hash, key]); // do this on route change

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
