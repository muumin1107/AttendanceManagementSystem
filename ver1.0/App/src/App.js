import React, { useState } from 'react';
import CurrentDateTime from './CurrentDateTime';
import RegisterID from './RegisterID';
import DeleteID from './DeleteID';
import CardReading from './CardReading';
import BackgroundCycle from './BackgroundCycle';
import { UserPlus, UserMinus, CircleAlert, CircleCheck } from 'lucide-react';
import './App.css';

function App() {
  // 各フォームの表示フラグとデータ管理用のstate
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [showDeleteForm, setShowDeleteForm] = useState(false);
  const [attendanceType, setAttendanceType] = useState(null);
  const [registrationData, setRegistrationData] = useState(null);
  const [deleteData, setDeleteData] = useState(null);
  const [attendanceData, setAttendanceData] = useState(null);
  const [processResult, setProcessResult] = useState(null);
  const [showPopup, setShowPopup] = useState(false);
  const [popupMessage, setPopupMessage] = useState({ jp: '', en: '' });
  const [popupType, setPopupType] = useState('success');

  // 新規登録フォームの表示
  const handleStartRegistration = () => {
    setShowRegisterForm(true);
    setAttendanceData(null);
  };

  // 削除フォームの表示
  const handleStartDelete = () => {
    setShowDeleteForm(true);
    setAttendanceData(null);
  };

  // 勤怠ボタンがクリックされた時の処理
  const handleAttendanceClick = (type) => {
    setAttendanceType(type);
    setRegistrationData(null);
    setDeleteData(null);
    setAttendanceData(type);
    setShowRegisterForm(false);
    setShowDeleteForm(false);
  };

  // 登録処理が完了したときの処理
  const handleRegistrationComplete = (register_formData) => {
    setRegistrationData(register_formData);
    setAttendanceType('登録');
    setAttendanceData(null);
    setShowRegisterForm(false);
  };

  // 削除処理が完了したときの処理
  const handleDeleteComplete = (delete_formData) => {
    setDeleteData(delete_formData);
    setAttendanceType('削除');
    setAttendanceData(null);
    setShowDeleteForm(false);
  };

  // キャンセルボタンが押された時の処理
  const handleCancel = () => {
    setAttendanceType(null);
    setRegistrationData(null);
    setAttendanceData(null);
  };

  // 処理結果に応じてポップアップを表示
  const handleProcessResult = (result) => {
    if (result === 'success') {
      setPopupMessage({ jp: '完了しました', en: 'Success' });
      setPopupType('success');
    } else if (result === 'client_error') {
      setPopupMessage({ jp: '入力内容が不正です', en: 'The input is invalid' });
      setPopupType('error');
    } else if (result === 'network_error') {
      setPopupMessage({ jp: 'ネットワークエラーが発生しました', en: 'An unexpected error has occurred' });
      setPopupType('error');
    } else if (result === 'reader_error') {
      setPopupMessage({ jp: 'カード読み取りに失敗しました', en: 'Card reading failed' });
      setPopupType('error');
    }

    setShowPopup(true);
    setTimeout(() => {
      setShowPopup(false);
    }, 3000);

    // フォームのリセット
    setAttendanceType(null);
    setRegistrationData(null);
    setAttendanceData(null);
    setShowRegisterForm(false);
    setShowDeleteForm(false);
  };

  // フォーム表示処理
  if (showRegisterForm) {
    return <RegisterID onComplete={handleRegistrationComplete} />;
  }

  if (showDeleteForm) {
    return <DeleteID onComplete={handleDeleteComplete} />;
  }

  if (attendanceType) {
    return (
      <CardReading
        type={attendanceType}
        register_formData={registrationData}
        delete_formData={deleteData}
        attendanceData={attendanceData}
        onCancel={handleCancel}
        onProcessResult={handleProcessResult}
      />
    );
  }

  return (
    <div className="App">
      {/* 成功やエラーのポップアップ表示 */}
      {showPopup && (
        <div className={`popup ${popupType}`}>
          {popupType === 'success' ? <CircleCheck className="popup-icon" /> : <CircleAlert className="popup-icon" />}
          <div>
            <strong>{popupMessage.jp}</strong><br />
            {popupMessage.en}
          </div>
        </div>
      )}
      <BackgroundCycle />
      <header className="App-header">
        <CurrentDateTime />
        <div className="attendance-buttons">
          <button
            className="attendance-button clock-in"
            onClick={() => handleAttendanceClick('出勤')}
          >
            出勤<br />Clock In
          </button>
          <button
            className="attendance-button break-start"
            onClick={() => handleAttendanceClick('休入')}
          >
            休入<br />Break Start
          </button>
          <button
            className="attendance-button break-end"
            onClick={() => handleAttendanceClick('休出')}
          >
            休出<br />Break End
          </button>
          <button
            className="attendance-button clock-out"
            onClick={() => handleAttendanceClick('退勤')}
          >
            退勤<br />Clock Out
          </button>
        </div>
        <button className="register-link" onClick={handleStartRegistration}>
          <UserPlus className="register-icon" />
          <span>
            <strong>新規カード・デバイスの登録（Registering card/device）</strong>
          </span>
        </button>
        <button className="delete-link" onClick={handleStartDelete}>
          <UserMinus className="delete-icon" />
          <span>
            <strong>登録済みカード・デバイスの削除（Deleting card/device）</strong>
          </span>
        </button>
      </header>
    </div>
  );
}

export default App; // Appコンポーネントをエクスポート
