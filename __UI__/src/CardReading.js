import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Wifi, X } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import './CardReading.css';

const CardReading = ({ formData, attendanceData, onCancel }) => {
  const [isCardDetected, setIsCardDetected] = useState(false);
  const [message, setMessage] = useState(null); // フィードバックメッセージ

  // API呼び出しの共通関数
  const callApi = async (url, data) => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const result = await response.json();
      console.log('API呼び出し成功:', result);
      setMessage('登録が成功しました！');
    } catch (error) {
      console.error('APIエラー:', error);
      setMessage('エラーが発生しました。もう一度お試しください。');
    }
  };

  const handleCardDetection = useCallback(async () => {
    console.log('Card detected!');
    setIsCardDetected(true);

    const test_id = 'test'; // 実際のカードIDをここで取得

    if (formData) {
      const { fullName, attribute, description } = formData;
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_id', {
        id: test_id, name: fullName, attribute, description
      });
    } else if (attendanceData) {
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_attendance', {
        id: test_id, next_state: attendanceData
      });
    } else {
      alert('No data available');
    }

    setTimeout(() => {
      setIsCardDetected(false);
      setMessage(null); // メッセージをリセット
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

        {message && <p className="message">{message}</p>} {/* フィードバックメッセージの表示 */}

        <button className="cancel-button" onClick={onCancel}>
          <X className="cancel-icon" />
          <span className="cancel-text">中断<br />Cancel</span>
        </button>
      </header>
    </div>
  );
};

export default CardReading;