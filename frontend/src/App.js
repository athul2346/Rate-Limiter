import React, { useState } from 'react';
import RequestPanel from './components/RequestPanel';
import RateLimitIndicator from './components/RateLimitIndicator';
import ActivityLog from './components/ActivityLog';
import './App.css';

function App() {
  const [remainingRequests, setRemainingRequests] = useState(5);
  const [log, setLog] = useState([]);

  const handleNewRequest = (entry) => {
    setLog([entry, ...log]);
    if (entry.status === 'success' && remainingRequests > 0) {
      setRemainingRequests(remainingRequests - 1);
    }
  };

  return (
    <div className="App">
      <h1>Smart API Rate Limiter</h1>
      <RateLimitIndicator remainingRequests={remainingRequests} />
      <RequestPanel onNewRequest={handleNewRequest} />
      <ActivityLog log={log} />
    </div>
  );
}

export default App;
