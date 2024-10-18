import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Wifi } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import Loading from './Loading';
import './CardReading.css';

function CardReading() {
  const [isLoading, setIsLoading] = useState(false);

  const handleStartLoading = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  };

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="CardReading">
      <header className="CardReading-header">
        <CurrentDateTime />
        <motion.div
          className="icon-container"
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          <Wifi className="wifi-icon" />
        </motion.div>
        <p className="touch-message-jp">カード・デバイスをかざしてください</p>
        <p className="touch-message-en">Please tap your card or device</p>
        <button className="start-button" onClick={handleStartLoading}>Start Loading</button>
      </header>
    </div>
  );
}

export default CardReading;