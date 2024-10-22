import React, { useState } from 'react';
import './DeleteID.css';

function DeleteID({ onComplete }) {
  const [formData, setFormData] = useState({
    fullName: ''
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const validateForm = () => {
    let newErrors = {};
    if (!formData.fullName.trim()) {
      newErrors.fullName = '名前を入力してください。';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onComplete(formData);
    }
  };

  const handleBack = () => {
    window.location.href = '/';
  };

  return (
    <div className="DeleteID">
      <div className="DeleteID-header">
        <div className="delete-container">
          <p className="deleteIDform-title-jp">カード・デバイス削除</p>
          <p className="deleteIDform-title-en">Delete card/device</p>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="fullName">名前（Full Name）</label>
              <input
                type="text"
                id="fullName"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                placeholder="例：山田太郎（Taro Yamada）"
              />
              {errors.fullName && <span className="error">{errors.fullName}</span>}
            </div>
            <div className="button-group">
              <button type="button" className="back-button" onClick={handleBack}>
                戻る（Back）
              </button>
              <button type="submit" className="next-button">
                次へ（Next）
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default DeleteID;