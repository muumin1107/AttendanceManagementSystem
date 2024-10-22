import React, { useEffect, useState } from 'react';
import './CurrentDateTime.css';

function CurrentDateTime() {
    const [dateTime, setDateTime] = useState(new Date());

    useEffect(() => {
    const timer = setInterval(() => setDateTime(new Date()), 1000);
    return () => clearInterval(timer);
    }, []);

    const formatDate = (date) => {
    return date.toLocaleDateString('ja-JP', { year: 'numeric', month: '2-digit', day: '2-digit' });
    };

    const formatTime = (date) => {
    return date.toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    };

    return (
    <div className="current-datetime">
        <div className="date">{formatDate(dateTime)}</div>
        <div className="time">{formatTime(dateTime)}</div>
    </div>
    );
}

export default CurrentDateTime;