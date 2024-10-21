// import React, { useEffect, useState } from 'react';
// import './BackgroundCycle.css';

// const BackgroundCycle = () => {
//     const [time, setTime] = useState(new Date());
//     const [backgroundClass, setBackgroundClass] = useState('');
//     const [celestialBody, setCelestialBody] = useState('sun');

//     useEffect(() => {
//         const timer = setInterval(() => {
//             setTime(new Date());
//         }, 1000);

//         return () => clearInterval(timer);
//     }, []);

//     useEffect(() => {
//         const updateBackground = () => {
//             const hours = time.getHours();
//             const minutes = time.getMinutes();
//             const totalMinutes = hours * 60 + minutes;

//             let newBackgroundClass = '';
//             let newCelestialBody = 'sun';

//             if (totalMinutes >= 180 && totalMinutes < 540) { // 3:00 - 9:00 (朝)
//                 newBackgroundClass = 'morning';
//                 newCelestialBody = 'sun';
//             } else if (totalMinutes >= 540 && totalMinutes < 900) { // 9:00 - 15:00 (昼)
//                 newBackgroundClass = 'day';
//                 newCelestialBody = 'sun';
//             } else if (totalMinutes >= 900 && totalMinutes < 1260) { // 15:00 - 21:00 (夕方)
//                 newBackgroundClass = 'evening';
//                 newCelestialBody = 'moon';
//             } else { // 21:00 - 3:00 (夜)
//                 newBackgroundClass = 'night';
//                 newCelestialBody = 'moon';
//             }

//             setBackgroundClass(newBackgroundClass);
//             setCelestialBody(newCelestialBody);
//         };

//         updateBackground();
//         const intervalId = setInterval(updateBackground, 60000); // 毎分更新

//         return () => clearInterval(intervalId);
//     }, [time]);

//     return (
//         <div className={`background ${backgroundClass}`}>
//             <div 
//                 className={`celestial-body ${celestialBody}`} 
//             ></div>
//         </div>
//     );
// };

// export default BackgroundCycle;

import React, { useEffect, useState } from 'react';
import './BackgroundCycle.css';

const BackgroundCycle = () => {
    const [cycleMinutes, setCycleMinutes] = useState(0); // Represents time in a 1-minute cycle
    const [backgroundClass, setBackgroundClass] = useState('');
    const [celestialBody, setCelestialBody] = useState('sun');

    useEffect(() => {
        const updateCycle = () => {
            setCycleMinutes((prevCycleMinutes) => (prevCycleMinutes + 1) % 60); // Update cycle time every second, reset after 60
        };

        const timer = setInterval(updateCycle, 1000); // Update every second

        return () => clearInterval(timer);
    }, []);

    useEffect(() => {
        const updateBackground = () => {
            let newBackgroundClass = '';
            let newCelestialBody = 'sun';

            if (cycleMinutes < 15) { // 0-14 seconds -> Morning
                newBackgroundClass = 'morning';
                newCelestialBody = 'sun';
            } else if (cycleMinutes < 30) { // 15-29 seconds -> Day
                newBackgroundClass = 'day';
                newCelestialBody = 'sun';
            } else if (cycleMinutes < 45) { // 30-44 seconds -> Evening
                newBackgroundClass = 'evening';
                newCelestialBody = 'moon';
            } else { // 45-59 seconds -> Night
                newBackgroundClass = 'night';
                newCelestialBody = 'moon';
            }

            setBackgroundClass(newBackgroundClass);
            setCelestialBody(newCelestialBody);
        };

        updateBackground();
    }, [cycleMinutes]);

    return (
        <div className={`background ${backgroundClass}`}>
            <div className={`celestial-body ${celestialBody}`}></div>
        </div>
    );
};

export default BackgroundCycle;