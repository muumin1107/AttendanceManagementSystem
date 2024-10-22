import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Wifi, X } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import Loading from './Loading';
import './CardReading.css';

const CardReading = ({register_formData, delete_formData, attendanceData, onCancel, onProcessResult }) => {
  const [isCardDetected, setIsCardDetected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isCancelled, setIsCancelled] = useState(false); // 中断を示すフラグ

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
      if (!isCancelled) {
        onProcessResult('network_error');
      }
    } finally {
      setIsLoading(false);
      onCancel();
    }
  };

  // UIDを取得するAPI呼び出し
  const fetchCardUid = async () => {
    if (isCancelled) return null; // 中断されていたらUID取得しない
    try {
      const response = await fetch('http://127.0.0.1:8000/get_uid');
      if (response.status === 200) {
        const data = await response.json();
        return data.uid;
      } else {
        if (!isCancelled) {
          onProcessResult('reader_error'); // 読み取りエラー時に処理結果を返却
        }
        return null;
      }
    } catch (error) {
      if (!isCancelled) {
        onProcessResult('network_error'); // ネットワークエラー時も処理結果を返却
      }
      return null;
    }
  };

  const handleCardDetection = useCallback(async () => {
    setIsCardDetected(true);

    const uid = await fetchCardUid(); // APIからUIDを取得

    if (!uid || isCancelled) {
      return; // エラーが発生した場合や中断時は処理を中断
    }

    if (register_formData) {
      const { fullName, attribute, description } = register_formData;
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_id', 'POST', {
        id: uid, name: fullName, attribute, description
      });
    } else if (delete_formData) {
      const { fullName } = delete_formData;
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/remove_id', 'DELETE', {
        id: uid, name: fullName
      });
    } else if (attendanceData) {
      await callApi('https://fast-gnni-shizuokauniversity-8f675ed2.koyeb.app/register_attendance', 'POST', {
        id: uid, next_state: attendanceData
      });
    } else {
      alert('データがありません');
    }

    setTimeout(() => {
      setIsCardDetected(false);
    }, 3000);
  }, [register_formData, delete_formData, attendanceData, isCancelled]); // isCancelledを依存に追加

  useEffect(() => {
    const cardDetectionTimeout = setTimeout(() => {
      handleCardDetection();
    }, 1000);

    return () => clearTimeout(cardDetectionTimeout);
  }, [handleCardDetection]);

  const handleCancelClick = () => {
    setIsCancelled(true); // 中断フラグを立てる
    onCancel();
  };

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

        <button className="cancel-button" onClick={handleCancelClick}>
          <X className="cancel-icon" />
          <span className="cancel-text">中断<br />Cancel</span>
        </button>
      </header>
    </div>
  );
};

export default CardReading;
