import React, { useState, useEffect } from 'react';
import logo from '../assets/images/logo.png';
import { Link as RouterLink } from 'react-router-dom';
import LogoLink from './LogoLink';

function Navbar() {
  const [nav, setNav] = useState(false);

  const changeBackground = () => {
    if (window.scrollY >= 50) {
      setNav(true);
    } else {
      setNav(false);
    }
  };

  useEffect(() => {
    window.addEventListener('scroll', changeBackground);
    return () => window.removeEventListener('scroll', changeBackground);
  }, []);

  return (
    <nav className={nav ? 'nav active' : 'nav'}>
      {/* Logo scrolls to #main section on home page */}
      <LogoLink />

      {/* Mobile menu toggle */}
      <input className="menu-btn" type="checkbox" id="menu-btn" />
      <label className="menu-icon" htmlFor="menu-btn">
        <span className="nav-icon"></span>
      </label>

      {/* Page routes using React Router */}
      <ul className="menu">
        <li><RouterLink to="/">Home</RouterLink></li>
        <li><RouterLink to="/generate">Generate</RouterLink></li>
        <li><RouterLink to="/about">About</RouterLink></li>
        <li><RouterLink to="/contact">Contact</RouterLink></li>
      </ul>
    </nav>
  );
}

export default Navbar;
