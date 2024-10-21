import React, { useState } from 'react';
import CurrentDateTime from './CurrentDateTime';
import RegisterID from './RegisterID';
import CardReading from './CardReading';
import BackgroundCycle from './BackgroundCycle';
import { UserPlus } from 'lucide-react';
import './App.css';

function App() {
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const [attendanceType, setAttendanceType] = useState(null);
  const [registrationData, setRegistrationData] = useState(null);
  const [attendanceData, setAttendanceData] = useState(null);

  const handleStartRegistration = () => {
    setShowRegisterForm(true);
    setAttendanceData(null);
  };

  const handleAttendanceClick = (type) => {
    setAttendanceType(type);
    setAttendanceData(type);
    setShowRegisterForm(false);
    setRegistrationData(null);
  };

  const handleRegistrationComplete = (formData) => {
    setRegistrationData(formData);
    setAttendanceType('登録');
    setAttendanceData(null);
    setShowRegisterForm(false);
  };

  const handleCancel = () => {
    setAttendanceType(null);
    setRegistrationData(null);
    setAttendanceData(null);
  };

  if (showRegisterForm) {
    return <RegisterID onComplete={handleRegistrationComplete} />;
  }

  if (attendanceType) {
    return (
      <CardReading
        type={attendanceType}
        formData={registrationData}
        attendanceData={attendanceData}
        onCancel={handleCancel}
      />
    );
  }

  return (
    <div className="App">
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
            <strong>新規カード・デバイス登録（New card/device registration）</strong>
          </span>
        </button>
      </header>
    </div>
  );
}

export default App;