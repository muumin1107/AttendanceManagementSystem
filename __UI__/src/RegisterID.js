import React, { useState } from 'react';
import './RegisterID.css';

function RegisterID({ onComplete }) {
  const [formData, setFormData] = useState({
    fullName: '',
    attribute: '',
    description: ''
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
    if (!formData.attribute) {
      newErrors.attribute = '属性を選択してください。';
    }
    if (!formData.description.trim()) {
      newErrors.description = '説明を入力してください。';
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
    <div className="RegisterID">
      <div className="RegisterID-header">
        <div className="register-container">
          <p className="registerIDform-title-jp">カード・デバイス登録</p>
          <p className="registerIDform-title-en">Card/Device registration</p>
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
            <div className="form-group">
              <label htmlFor="attribute">属性（Attribute）</label>
              <select
                id="attribute"
                name="attribute"
                value={formData.attribute}
                onChange={handleChange}
              >
                <option value="">選択してください</option>
                <option value="ICカード">ICカード（IC cards）</option>
                <option value="スマートフォン">スマートフォン（Smartphone）</option>
                <option value="その他">その他（Others）</option>
              </select>
              {errors.attribute && <span className="error">{errors.attribute}</span>}
            </div>
            <div className="form-group">
              <label htmlFor="description">説明（Description）</label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="例：学生証（Student ID card）"
              />
              {errors.description && <span className="error">{errors.description}</span>}
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

export default RegisterID;