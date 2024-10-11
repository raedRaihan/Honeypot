// Subreq.js
import React from 'react';
import './subreq.css';

const Subreq = ({ showModal, closeModal }) => {
  const handleModalClick = (event) => {
    if (event.target === event.currentTarget) {
      closeModal();
    }
  };

  return (
    showModal && (
      <div className="modal-background" onClick={handleModalClick}>
        <div className="modal-content">
          <span className="close" onClick={closeModal}>&times;</span>
          <h2>Request Fill Out</h2>
          <p>Thank you!</p>
          
          <div className="card-container">
            <form className="submit-request-form">
              <div className="form-group">
                <input type="text" id="userName" name="userName" className="form-input" placeholder="Name" />
              </div>
              
              <div className="form-group">
                <input type="email" id="userEmail" name="userEmail" className="form-input" placeholder="Email" />
              </div>
              
              <button type="submit" className="submit-button">Submit</button>  
            </form>
          </div>
          
        </div>
      </div>
    )
  );
};

export default Subreq;
