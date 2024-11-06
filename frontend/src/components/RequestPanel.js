import React, { useState } from 'react';
import axios from 'axios';

const RequestPanel = ({ onNewRequest }) => {
  const [responseMessage, setResponseMessage] = useState('');

  const makeApiRequest = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/resource');
      setResponseMessage(response.data.message);
      onNewRequest({ status: 'success', message: response.data.message, time: new Date().toLocaleTimeString() });
    } catch (error) {
      if (error.response && error.response.status === 429) {
        setResponseMessage("Rate limit exceeded. Please wait and try again.");
        onNewRequest({ status: 'error', message: "Rate limit exceeded", time: new Date().toLocaleTimeString() });
      } else {
        setResponseMessage("An error occurred. Please try again.");
      }
    }
  };

  return (
    <div>
      <button onClick={makeApiRequest}>Make API Request</button>
      <p>{responseMessage}</p>
    </div>
  );
};

export default RequestPanel;
