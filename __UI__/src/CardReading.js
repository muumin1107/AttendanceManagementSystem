import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Wifi, X } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import Loading from './Loading';
import './CardReading.css';

const CardReading = ({register_formData, delete_formData, attendanceData, onCancel, onProcessResult }) => {
  const [isCardDetected, setIsCardDetected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // API呼び出しの共通関数
  const callApi = async (url, method, data) => {
    setIsLoading(true);
    try {
      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (response.status === 200) {
        onProcessResult('success');
      } else {
        onProcessResult('client_error');
      }
    } catch (error) {
      onProcessResult('network_error');
    } finally {
      setIsLoading(false);
      onCancel();
    }
  };

  const handleCardDetection = useCallback(async () => {
    setIsCardDetected(true);

    const test_id = 'test'; // 実際のカードIDをここで取得

    if (register_formData) {
      const { fullName, attribute, description } = register_formData;
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_id', 'POST', {
        id: test_id, name: fullName, attribute, description
      });
    } else if (delete_formData) {
      const { fullName } = delete_formData;
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/remove_id', 'DELETE', {
        id: test_id, name: fullName
      });
    } else if (attendanceData) {
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_attendance', 'POST', {
        id: test_id, next_state: attendanceData
      });
    } else {
      alert('データがありません');
    }

    setTimeout(() => {
      setIsCardDetected(false);
    }, 3000);
  }, [register_formData, delete_formData, attendanceData]);

  useEffect(() => {
    const cardDetectionTimeout = setTimeout(() => {
      handleCardDetection();
    }, 1000);

    return () => clearTimeout(cardDetectionTimeout);
  }, [handleCardDetection]);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <div className="CardReading">
      <header className="CardReading-header">
        <CurrentDateTime />
        <motion.div
          className={`icon-container ${isCardDetected ? 'card-detected' : ''}`}
          animate={{ scale: [1, 1.1, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
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