import React, { useState } from 'react';
import CurrentDateTime from './CurrentDateTime';
import RegisterID from './RegisterID';
import DeleteID from './DeleteID';
import CardReading from './CardReading';
import BackgroundCycle from './BackgroundCycle';
import { UserPlus, UserMinus, CircleAlert, CircleCheck } from 'lucide-react';
import './App.css';

function App() {
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

  const handleStartRegistration = () => {
    setShowRegisterForm(true);
    setAttendanceData(null);
  };

  const handleStartDelete = () => {
    setShowDeleteForm(true);
    setAttendanceData(null);
  };

  const handleAttendanceClick = (type) => {
    setAttendanceType(type);
    setRegistrationData(null);
    setDeleteData(null);
    setAttendanceData(type);
    setShowRegisterForm(false);
    setShowDeleteForm(false);
  };

  const handleRegistrationComplete = (register_formData) => {
    setRegistrationData(register_formData);
    setAttendanceType('登録');
    setAttendanceData(null);
    setShowRegisterForm(false);
  };

  const handleDeleteComplete = (delete_formData) => {
    setDeleteData(delete_formData);
    setAttendanceType('削除');
    setAttendanceData(null);
    setShowDeleteForm(false);
  };

  const handleCancel = () => {
    setAttendanceType(null);
    setRegistrationData(null);
    setAttendanceData(null);
  };

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

    setAttendanceType(null);
    setRegistrationData(null);
    setAttendanceData(null);
    setShowRegisterForm(false);
    setShowDeleteForm(false);
  };

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

export default App;