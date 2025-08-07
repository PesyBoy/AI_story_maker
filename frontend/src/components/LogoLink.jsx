import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import logo from '../assets/images/logo.png';

function LogoLink() {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogoClick = () => {
    if (location.pathname === '/') {
      // Already on homepage, scroll to #main
      const mainElement = document.getElementById('main');
      if (mainElement) {
        mainElement.scrollIntoView({ behavior: 'smooth' });
      }
    } else {
      // Navigate to homepage, then scroll after it loads
      navigate('/');
      setTimeout(() => {
        const mainElement = document.getElementById('main');
        if (mainElement) {
          mainElement.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    }
  };

  return (
    <div className="logo" onClick={handleLogoClick} style={{ cursor: 'pointer' }}>
      <img src={logo} alt="Logo" />
    </div>
  );
}

export default LogoLink;
