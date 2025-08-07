import React, {useState} from 'react'
import logo from '../assets/images/logo.png'
import {Link, linkl} from 'react-scroll'


function Navbar() {

  const [nav, setnav] = useState(false)

  const changeBackground = () => {
    if (window.scrollY >= 50){
      setnav(true)
    }
    else{
      setnav(false)
    }
  }
  window.addEventListener('scroll', changeBackground)
 

  return (
    <nav className={nav? "nav active":"nav"}>
        <Link to = 'main' smooth={true} duration={800} className='logo'>
          <img src = {logo} alt=''/>
        </Link>
        <input className='menu-btn' type='checkbox' id='menu-btn'/>
        <label className='menu-icon' for='menu-btn'>
          <span className='nav-icon'></span>
        </label>
        <ul className='menu'>
          <li><Link to='/' smooth={true} duration={800}>Home</Link></li>
          <li><Link to='/generate' smooth={true} duration={800}>Generate </Link></li>
          <li><Link to='/about' smooth={true} duration={800}>About</Link></li>
          <li><Link to='/contact' smooth={true} duration={800}>Contact</Link></li>
        </ul>

    </nav>
  )
}

export default Navbar