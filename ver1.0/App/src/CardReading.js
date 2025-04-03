import React, { useState, useEffect, useCallback } from 'react';
import { motion } from 'framer-motion';
import { Wifi, X } from 'lucide-react';
import CurrentDateTime from './CurrentDateTime';
import Loading from './Loading';
import './CardReading.css';

// CardReadingコンポーネントを定義
const CardReading = ({ register_formData, delete_formData, attendanceData, onCancel, onProcessResult }) => {
  const [isCardDetected, setIsCardDetected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [isCancelled, setIsCancelled] = useState(false); // 中断を示すフラグ

  // API呼び出しを共通化する関数
  const callApi = async (url, method, data) => {
    setIsLoading(true);
    try {
      const response = await fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });
      if (response.status === 200) {
        onProcessResult('success'); // 成功時
      } else {
        onProcessResult('client_error'); // クライアントエラー時
      }
    } catch (error) {
      if (!isCancelled) {
        onProcessResult('network_error'); // ネットワークエラー時
      }
    } finally {
      setIsLoading(false);
      onCancel(); // 処理が終わったらキャンセルを実行
    }
  };

  // UIDを取得するAPI呼び出し
  const fetchCardUid = async () => {
    if (isCancelled) return null; // 中断されていたらUID取得しない
    try {
      const response = await fetch('{APIサーバーIP:ポート番号}/get_uid');
      if (response.status === 200) {
        const data = await response.json();
        return data.uid;
      } else {
        if (!isCancelled) {
          onProcessResult('reader_error'); // 読み取りエラー
        }
        return null;
      }
    } catch (error) {
      if (!isCancelled) {
        onProcessResult('network_error'); // ネットワークエラー
      }
      return null;
    }
  };

  // カードが検出された際の処理
  const handleCardDetection = useCallback(async () => {
    setIsCardDetected(true);

    const uid = await fetchCardUid(); // UIDをAPIから取得

    if (!uid || isCancelled) {
      return; // エラーまたは中断時に処理を中止
    }

    // 登録処理
    if (register_formData) {
      const { fullName, attribute, description } = register_formData;
      await callApi('{APIサーバーIP:ポート番号}/register_id', 'POST', {
        id: uid, name: fullName, attribute: attribute, description: description
      });
    } else if (delete_formData) {
      const { fullName } = delete_formData;
      await callApi('{APIサーバーIP:ポート番号}/remove_id', 'DELETE', {
        id: uid, name: fullName
      });
    } else if (attendanceData) {
      await callApi('{APIサーバーIP:ポート番号}/register_attendance', 'POST', {
        id: uid, next_state: attendanceData
      });
    } else {
      alert('データがありません');
    }

    // カード検出を3秒後にリセット
    setTimeout(() => {
      setIsCardDetected(false);
    }, 3000);
  }, [register_formData, delete_formData, attendanceData, isCancelled]);

  // コンポーネントがマウントされた際にカード検出処理を開始
  useEffect(() => {
    const cardDetectionTimeout = setTimeout(() => {
      handleCardDetection();
    }, 1000);

    return () => clearTimeout(cardDetectionTimeout); // クリーンアップ
  }, [handleCardDetection]);

  // キャンセルボタンのクリック処理
  const handleCancelClick = () => {
    setIsCancelled(true); // 中断フラグを立てる
    onCancel();
  };

  if (isLoading) {
    return <Loading />; // ローディング中の表示
  }

  return (
    <div className="CardReading">
      <header className="CardReading-header">
        <CurrentDateTime /> {/* 現在の日時を表示 */}
        <motion.div
          className={`icon-container ${isCardDetected ? 'card-detected' : ''}`}
          animate={{ scale: [1, 1.1, 1], opacity: [0.5, 1, 0.5] }}
          transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
        >
          <Wifi className="wifi-icon" /> {/* Wi-Fiアイコン */}
        </motion.div>
        <p className="touch-message-jp">カード・デバイスをかざしてください</p> {/* 日本語メッセージ */}
        <p className="touch-message-en">Please tap your card or device</p> {/* 英語メッセージ */}

        <button className="cancel-button" onClick={handleCancelClick}>
          <X className="cancel-icon" />
          <span className="cancel-text">中断<br />Cancel</span>
        </button>
      </header>
    </div>
  );
};

export default CardReading; // コンポーネントをエクスポート