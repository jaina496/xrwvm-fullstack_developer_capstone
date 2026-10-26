import React, { useState } from 'react';
import "../assets/style.css";
import "../assets/bootstrap.min.css";

const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const currUser = sessionStorage.getItem('username');

  const logout = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('/djangoapp/logout');
      const json = await res.json();
      if (res.ok && json) {
        sessionStorage.removeItem('username');
        window.location.href = '/';
      } else {
        alert('Unable to log out. Please try again.');
      }
    } catch (error) {
      console.error('Logout failed:', error);
      alert('Unable to log out. Please try again.');
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light" style={{ backgroundColor: 'darkturquoise', minHeight: '1in' }}>
      <div className="container-fluid">
        <h2 style={{ paddingRight: '5%' }}>Dealerships</h2>
        <button
          type="button"
          className="navbar-toggler"
          aria-controls="navbarText"
          aria-expanded={menuOpen}
          aria-label="Toggle navigation"
          onClick={() => setMenuOpen(!menuOpen)}
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div id="navbarText" className={`navbar-collapse ${menuOpen ? 'show' : 'collapse'}`}>
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            <li className="nav-item"><a className="nav-link" href="/" onClick={() => setMenuOpen(false)}>Home</a></li>
            <li className="nav-item"><a className="nav-link" href="/about" onClick={() => setMenuOpen(false)}>About Us</a></li>
            <li className="nav-item"><a className="nav-link" href="/contact" onClick={() => setMenuOpen(false)}>Contact Us</a></li>
            {!currUser && <li className="nav-item"><a className="nav-link" href="/login" onClick={() => setMenuOpen(false)}>Login</a></li>}
            {!currUser && <li className="nav-item"><a className="nav-link" href="/register" onClick={() => setMenuOpen(false)}>Register</a></li>}
            {currUser && <li className="nav-item"><span className="nav-link">{currUser}</span></li>}
            {currUser && <li className="nav-item"><a className="nav-link" href="/djangoapp/logout" onClick={logout}>Logout</a></li>}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Header;
