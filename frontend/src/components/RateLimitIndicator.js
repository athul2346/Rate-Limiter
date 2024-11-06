import React from 'react';

const RateLimitIndicator = ({ remainingRequests }) => {
  return (
    <div>
      <p>Remaining Requests: {remainingRequests}</p>
      <progress value={remainingRequests} max="5"></progress>
    </div>
  );
};

export default RateLimitIndicator;
