import React, { useState } from 'react';
import './DeleteID.css'; // CSSファイルのインポート

// DeleteIDコンポーネントの定義
function DeleteID({ onComplete }) {
  // ユーザー入力とエラー状態を管理するstate
  const [formData, setFormData] = useState({
    fullName: ''
  });
  const [errors, setErrors] = useState({});

  // 入力フィールドの変更を監視してstateを更新する関数
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  // 入力データのバリデーションを行う関数
  const validateForm = () => {
    let newErrors = {};
    if (!formData.fullName.trim()) {
      newErrors.fullName = '名前を入力してください。';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0; // エラーがなければtrueを返す
  };

  // フォーム送信時の処理
  const handleSubmit = (e) => {
    e.preventDefault();
    if (validateForm()) {
      onComplete(formData); // フォームが有効な場合は次の処理を呼び出す
    }
  };

  // 戻るボタンの処理
  const handleBack = () => {
    window.location.href = '/';
  };

  return (
    <div className="DeleteID">
      <div className="DeleteID-header">
        <div className="delete-container">
          <p className="deleteIDform-title-jp">登録済みカード・デバイスの削除</p>
          <p className="deleteIDform-title-en">Deleting card/device</p>
          <form onSubmit={handleSubmit}>
            {/* 名前入力フィールド */}
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

            {/* ボタン群 */}
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

export default DeleteID; // コンポーネントのエクスポート