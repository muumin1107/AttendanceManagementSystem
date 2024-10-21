import React, { useEffect, useState } from 'react';
import './BackgroundCycle.css';

const BackgroundCycle = () => {
    const [time, setTime] = useState(new Date());
    const [backgroundClass, setBackgroundClass] = useState('');
    const [celestialBody, setCelestialBody] = useState('sun');

    useEffect(() => {
        const timer = setInterval(() => {
            setTime(new Date());
        }, 1000);

        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        const updateBackground = () => {
            const hours = time.getHours();
            const minutes = time.getMinutes();
            const totalMinutes = hours * 60 + minutes;

            let newBackgroundClass = '';
            let newCelestialBody = 'sun';

            if (totalMinutes >= 180 && totalMinutes < 540) { // 3:00 - 9:00 (朝)
                newBackgroundClass = 'morning';
                newCelestialBody = 'sun';
            } else if (totalMinutes >= 540 && totalMinutes < 900) { // 9:00 - 15:00 (昼)
                newBackgroundClass = 'day';
                newCelestialBody = 'sun';
            } else if (totalMinutes >= 900 && totalMinutes < 1260) { // 15:00 - 21:00 (夕方)
                newBackgroundClass = 'evening';
                newCelestialBody = 'moon';
            } else { // 21:00 - 3:00 (夜)
                newBackgroundClass = 'night';
                newCelestialBody = 'moon';
            }

            setBackgroundClass(newBackgroundClass);
            setCelestialBody(newCelestialBody);
        };

        updateBackground();
        const intervalId = setInterval(updateBackground, 60000); // 毎分更新

        return () => clearInterval(intervalId);
    }, [time]);

    return (
        <div className={`background ${backgroundClass}`}>
            <div 
                className={`celestial-body ${celestialBody}`} 
            ></div>
        </div>
    );
};

export default BackgroundCycle;