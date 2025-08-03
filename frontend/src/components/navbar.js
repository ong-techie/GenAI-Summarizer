import React from "react";
import { Link } from "react-router-dom";
import "./navbar.css";

const Navbar = () => {

  return (
    <nav className="navbar">
      <div className="nav-logo">GenAI Assistant</div>
      <ul className="nav-links">
        <li><Link to="/">Home</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
