import React from 'react';

const ActivityLog = ({ log }) => {
  return (
    <div>
      <h3>Activity Log</h3>
      <ul>
        {log.map((entry, index) => (
          <li key={index}>
            [{entry.time}] - {entry.status.toUpperCase()}: {entry.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ActivityLog;
