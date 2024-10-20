import React from 'react';
import { motion } from 'framer-motion';
import { Wifi, X } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import './CardReading.css';

function CardReading({ formData, attendanceData, onCancel }) {
  // テスト用
  if (formData) {
    console.log('formData:', formData.fullName, formData.attribute, formData.description);
  } else if (attendanceData) {
    console.log('attendanceData:', attendanceData);
  } else {
    console.log('No data');
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

        <button className="cancel-button" onClick={onCancel}>
          <X className="cancel-icon" />
          <span className="cancel-text">中断<br />Cancel</span>
        </button>
      </header>
    </div>
  );
}

export default CardReading;