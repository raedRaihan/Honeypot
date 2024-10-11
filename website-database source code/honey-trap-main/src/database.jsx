import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getDatabase, ref, get, child, onValue } from 'firebase/database';

import app from './firebase'; // Importing the initialized Firebase app
import './style.css';

const Database = () => {
  const [activeButton, setActiveButton] = useState('home');
  const [navActive, setNavActive] = useState(false);
  const navigate = useNavigate();
  const [profiles, setProfiles] = useState([]);

  const handleButtonClick = (buttonId) => {
    setActiveButton(buttonId);
  };

  useEffect(() => {

    const db = getDatabase(app);
    const userProfilesRef = ref(db, 'user_profiles');
    onValue(userProfilesRef, (snapshot) => {
      const data = snapshot.val();
      console.log(data);
    });
    get(ref(getDatabase(app), 'user_profiles')).then((snapshot) => {
      if (snapshot.exists()) {
        console.log(snapshot.val());
        const data = [];
        snapshot.forEach((childSnapshot) => {
          const profile = childSnapshot.val();
          // Only add profile to data if "scam" field is equal to "True"
          if (profile.scam === true) {
            data.push(profile);
          }
        });
        console.log(data);
        setProfiles(data);
      } else {
        console.log("No data available");
      }
    }).catch((error) => {
      console.error(error);
    });
    // Get the database instance
    //const db = getDatabase();
    //const db = database;
    // Reference to the "user_profiles" table in Firebase
    //const profilesRef = ref(db, 'user_profiles');

    // Fetch data from Firebase and filter based on "scam" field
    // get(child(profilesRef, '/')) // <-- Correct child path
    // .then((snapshot) => {
    //   const data = [];
    //   if (snapshot.exists()) {
    //     snapshot.forEach((childSnapshot) => {
    //       const profile = childSnapshot.val();
    //       // Only add profile to data if "scam" field is equal to "True"
    //       if (profile.scam === 'true') {
    //         data.push(profile);
    //       }
    //     });
    //   }
    //   console.log(data);
    //   setProfiles(data);
    // })
    // .catch((error) => {
    //   console.error('Error fetching data:', error);
    // });
}, []); // Empty dependency array ensures useEffect runs only once
  

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
              onClick={() => navigate('/')}
            />
          )}

          {/* Navigation items */}
          <div className={`nav-items-container ${navActive ? 'nav-active' : ''}`}>
            <Link
              to="/"
              className={`nav-item ${activeButton === 'home' ? 'active' : ''}`}
              onClick={() => handleButtonClick('home')}
            >
              Home
            </Link>
            <Link
              to="/"
              className={`nav-item ${activeButton === 'about' ? 'active' : ''}`}
              onClick={() => handleButtonClick('about')}
            >
              About
            </Link>
            <Link
              to="/"
              className={`nav-item ${activeButton === 'disclaimer' ? 'active' : ''}`}
              onClick={() => handleButtonClick('disclaimer')}
            >
              Disclaimer
            </Link>
            <Link
              to="/"
              className={`nav-item ${activeButton === 'database' ? 'active' : ''}`}
              onClick={() => handleButtonClick('database')}
            >
              Database
            </Link>
            <Link
              to="/"
              className={`nav-item ${activeButton === 'contact' ? 'active' : ''}`}
              onClick={() => handleButtonClick('contact')}
            >
              Contact Us
            </Link>
          </div>
        </nav>
      </div>

      {/* database page */}
      <div className="database-inner-page" id="database-info">
        <h2>Database</h2>
        <table className="database-table">
          <thead>
            <tr>
              <th>Profile Name</th>
              <th>Link</th>
            </tr>
          </thead>
          <tbody>
            {profiles.map((profile, index) => (
              <tr key={index}>
                <td>{profile.name}</td>
                <td><a href={profile.profile_link}>{profile.profile_link}</a></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* contact us page */}
      <footer className="contact-us-page" id="contact-info">
        <div className="container">
          <div className="row">
            {/* footer column 1 */}
            <div className="footer-col">
              <h4>Quick Links</h4>
              <ul>
                <li>
                  <button
                    id="about"
                    className={`link-button ${activeButton === 'about' ? 'active' : ''}`}
                    onClick={() => handleButtonClick('about')}
                  >
                    About
                  </button>
                </li>
                <li>
                  <button
                    id="disclaimer"
                    className={`link-button ${activeButton === 'disclaimer' ? 'active' : ''}`}
                    onClick={() => handleButtonClick('disclaimer')}
                  >
                    Disclaimer
                  </button>
                </li>
                <li>
                  <button
                    id="database"
                    className={`link-button ${activeButton === 'database' ? 'active' : ''}`}
                    onClick={() => handleButtonClick('database')}
                  >
                    Database
                  </button>
                </li>
                <li>
                  <button
                    id="submit-requests"
                    className={`link-button ${activeButton === 'submit-requests' ? 'active' : ''}`}
                    onClick={() => handleButtonClick('submit-requests')}
                  >
                    Submit Requests
                  </button>
                </li>
              </ul>
            </div>
            {/* footer column 2 */}
            <div className="footer-col">
            </div>
            <div className="footer-col">
              <h4>Contact us</h4>
              <div className="social-links">
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

export default Database;
