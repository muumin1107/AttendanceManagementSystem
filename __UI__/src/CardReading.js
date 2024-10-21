import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Wifi, X } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import './CardReading.css';

const CardReading = ({ formData, attendanceData, onCancel }) => {
  const [isCardDetected, setIsCardDetected] = useState(false);

  const handleCardDetection = useCallback(() => {
    console.log('Card detected!');
    setIsCardDetected(true);

    if (formData) {
      console.log('Form Data:', formData.fullName, formData.attribute, formData.description);
    } else if (attendanceData) {
      console.log('Attendance Data:', attendanceData);
    } else {
      console.log('No data available');
    }

    setTimeout(() => {
      setIsCardDetected(false);
    }, 3000);
  }, [formData, attendanceData]);

  useEffect(() => {
    const cardDetectionTimeout = setTimeout(() => {
      handleCardDetection();
    }, 5000);

    return () => clearTimeout(cardDetectionTimeout);
  }, [handleCardDetection]);

  return (
    <div className="CardReading">
      <header className="CardReading-header">
        <CurrentDateTime />
        <motion.div
          className={`icon-container ${isCardDetected ? 'card-detected' : ''}`}
          animate={{
            scale: [1, 1.1, 1],
            opacity: [0.5, 1, 0.5]
          }}
          transition={{
            duration: 2,
            repeat: Infinity,
            ease: 'easeInOut'
          }}
        >
          <Wifi className="wifi-icon" />
        </motion.div>
        <p className="touch-message-jp">カード・デバイスをかざしてください</p>
        <p className="touch-message-en">Please tap your card or device</p>

        <button className="cancel-button" onClick={onCancel}>
          <X className="cancel-icon" />
          <span className="cancel-text">中断<br />Cancel</span>
        </button>
      </header>
    </div>
  );
};

export default CardReading;