import React from "react";
import ReactDOM from "react-dom";
import App from "./App";  // Import App.js

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById("root")  // Connects React to index.html
);