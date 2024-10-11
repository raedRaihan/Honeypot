import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';


import Database from './database';
import Subreq from './subreq';
import './style.css';



const HoneyTrap = () => {
  
  const [activeButton, setActiveButton] = useState('home'); 
  const [navActive, setNavActive] = useState(false);

  //modal handling
  const [showModal, setShowModal] = useState(false);

  const openModal = () => {
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
  };


  //handles navbar toggling
  const toggleNav = () => {
    setNavActive(!navActive);
  };



  const handleButtonClick = (buttonId) => {
    setActiveButton(buttonId);

    // Smooth scrolling to sections(tabs)
    const scrollToSection = (sectionId) => {
      document.getElementById(sectionId).scrollIntoView({ 
        behavior: 'smooth',
        block: 'start'
      });
    };

    switch(buttonId) {
      case 'home':
        scrollToSection('home-info');
        break;
      case 'about':
        scrollToSection('about-us-info');
        break;
      case 'disclaimer':
        scrollToSection('disclaimer-info');
        break;
      case 'database':
        scrollToSection('database-info');
        break;
      case 'submit-requests':
        scrollToSection('submit-request-form');
        break;
      case 'contact':
        scrollToSection('contact-info');
        break;  
      default:
        break;
    }
    
  };


  

  return (
    <div>
      {/* navbar */}
      <div id="navbar-root">
        <nav className="navbar">


          {/* Conditionally render the logo based on navActive state */}
          {!navActive && (
            <img 
              id="logo" 
              src="logo1.png" 
              alt="Honey Trap Logo" 
              onClick={() => handleButtonClick('home')} 
            />
          )}

          {/* Hamburger menu icon (appears when screen is < 770px wide) */}
          <label className="hamburger">
            <input 
              type="checkbox" 
              id="burger" 
              checked={navActive} 
              onChange={toggleNav} 
            />
            <span></span>
            <span></span>
            <span></span>
          </label>



          {/* Navigation items */}
          <div className={`nav-items-container ${navActive ? 'nav-active' : ''}`}>
            <button id="home" className={`nav-item ${activeButton === 'home' ? 'active' : ''}`} onClick={() => handleButtonClick('home')}>Home</button>
            <button id="about" className={`nav-item ${activeButton === 'about' ? 'active' : ''}`} onClick={() => handleButtonClick('about')}>About</button>
            <button id="disclaimer" className={`nav-item ${activeButton === 'disclaimer' ? 'active' : ''}`} onClick={() => handleButtonClick('disclaimer')}>Disclaimer</button>
            <Link
  to="/database"
  className={`nav-item ${activeButton === 'database' ? 'active' : ''}`}
  onClick={() => handleButtonClick('database')}
>
  Database
</Link>
            <button id="contact" className={`nav-item ${activeButton === 'contact' ? 'active' : ''}`} onClick={() => handleButtonClick('contact')}>Contact us</button>
          </div>

        </nav>
      </div>



  
       {/* home page */}
      <div className="home-page" id="home-info">
        <div className='card'>
        <h1>HoneyTrap</h1>
        <button className="get-started-bt" onClick={() => handleButtonClick('about')}>Get Started  &#10132;</button>
        </div>
      </div>



      {/* about page */}
      <div className="about-page" id="about-us-info">
        <h2>About HoneyTrap</h2>
        <p> This website's initiative is to combat online scams, specifically those targeting vulnerable individuals such as the elderly. The project aims to create a comprehensive defense tool against scammers by employing advanced AI technology and strategic engagement techniques. Through the creation of a simulated online persona, the system will infiltrate scammers, engaging them in conversations while gathering valuable intelligence. The primary purpose of this initiative is to disrupt scammer operations, delay their fraudulent activities, and provide critical data to law enforcement agencies. Users of this system, including ethical hackers, cybersecurity experts, and individuals passionate about online security, will employ the tool to actively counteract scams. This product will be a useful tool by helping vulnerable families to not be swindled by online thieves.</p>
      </div>




      {/* disclaimer page */}
      <div className="disclaimer-page" id="disclaimer-info">
        <h2>Disclaimer</h2>
        <p>The primary objective is to identify potential scammers by engaging with them. Any accounts suspected of engaging in fraudulent activities will be documented in a scammer database. It is essential to recognize that engaging with scammers carries inherent risks, including potential exposure to deceptive or harmful content. Users are advised to exercise caution and discretion when interacting with unknown individuals online. This project is conducted for research and educational purposes only, and users engage with it at their own discretion and risk.</p>
      </div>





     {/* database page */}
      <div className="database-page" id="database-info">
        <h2>Database</h2>
        <p>Discover peace of mind with our Scammer Alert Database. Seamlessly integrated into our platform, this database features a comprehensive compilation of Facebook usernames associated with known scammers. Stay informed and protect yourself from fraudulent activities lurking in online spaces. Empower yourself to navigate the digital realm with confidence, armed with valuable insights into potential threats.</p>
        <Link to="/database"><button type="button" className="redirect-button">Check</button></Link>
      </div>





       {/* submit requests page */}
      <div className="submit-requests-page" id="submit-request-form">
        <h2>Submit a Request</h2>
        <p>We acknowledge that sometimes errors can occur, and names added to our database might be inaccurate. If you find that your name has been listed incorrectly or without justification, this is the place where you can request its removal. </p>
        <button className="redirect-button" onClick={openModal}>Make Claim</button>
        <Subreq showModal={showModal} closeModal={closeModal} />
      </div>





   {/* contact us page */}
    <footer class="contact-us-page" id = "contact-info">
     <div class="container">
      <div class="row">
       


        {/* footer column 1 */}
        <div class="footer-col">
          <h4>Quick Links</h4>
          <ul>
             <li><button id="about" className={`link-button ${activeButton === 'about' ? 'active' : ''}`} onClick={() => handleButtonClick('about')}>About</button></li> 
            <li><button id="disclaimer" className={`link-button ${activeButton === 'disclaimer' ? 'active' : ''}`} onClick={() => handleButtonClick('disclaimer')}>Disclaimer</button></li> 
            <li><button id="database" className={`link-button ${activeButton === 'database' ? 'active' : ''}`} onClick={() => handleButtonClick('database')}>Database</button></li> 
            <li><button id="submit-requests" className={`link-button ${activeButton === 'submit-requests' ? 'active' : ''}`} onClick={() => handleButtonClick('submit-requests')}>Submit Requests</button></li> 
          </ul>
        </div>
       


       {/* footer column 2 */}
        <div class="footer-col">
        </div>
        <div class="footer-col">
          <h4>Contact us</h4>
          <div class="social-links">
          <a href="mailto:honeypot4316@example.com">
           <img src="email.png" alt="Email the creators" />
          </a>

          
          </div>
        </div>
      </div>
     </div>
  </footer>

    </div>

  );
};

const rootDiv = document.createElement('div');
document.body.appendChild(rootDiv);

const root = ReactDOM.createRoot(rootDiv);
root.render(
  <Router>
    <Routes>
      <Route exact path="/" element={<HoneyTrap />} />
      <Route path="/database" element={<Database />} />
      <Route path="/subreq" element={<Subreq />} />
    </Routes>
  </Router>
);