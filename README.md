# 【ラズパイ】カードリーダー式勤怠管理システム

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![システム概要図](https://github.com/user-attachments/assets/68536d9d-3d55-40ca-b80d-ccf64a32d61e)

## ユーザーインターフェース（一部）
- **確認画面**

![UIイメージ](https://github.com/user-attachments/assets/dcf3c998-1461-49b9-8bcf-6be652ccdd0f)

![image](https://github.com/user-attachments/assets/da1da3da-157a-421f-b71a-b26e224a4ee9)

- **勤怠画面**

![スクリーンショット 2024-10-21 113408](https://github.com/user-attachments/assets/b42a4a17-4704-49aa-8b9f-da681d2f5fba)

![入力フォーム](https://github.com/user-attachments/assets/254fab70-aec4-468a-b115-f822b46bf780)

![カード読み込み画面](https://github.com/user-attachments/assets/efbf70c6-7fd6-48c0-8cf9-7a5c4332f5f1)

## RaspberryPiのセットアップ

- RaspberryPi 4 Model B

| Raspberry Pi Imager | OS            | Kernel |
----|----|----
| v1.8.5              | Raspbian 11.9 | 6.1.21 |

```
$ sudo apt update
$ cd ~/
$ mkdir .ssh
$ touch .ssh/authorized_keys
$ nano .ssh/authorized_keys

// 自身の公開鍵（.pub）をコピペ

$ sudo reboot
```

## カードリーダー接続

Raspberry Pi 4 Model BにRC-S380/Sを接続する．
- RC-S380/S

```
$ lsusb

// Sony Corp. RC-S380/Sが認識されていることを確認

$ sudo pip install nfcpy

// nfcが適切にインストールされているかを確認
$ git clone https://github.com/nfcpy/nfcpy.git
$ sudo python3 nfcpy/examples/tagtool.py show

// NFCカードを近づけて情報が表示されればOK

$ python3 -m nfc

// better assign ... と記載されている下の行に提示されたコマンドを入力
$ sudo sh -c 'echo SUBSYSTEM==\"usb\", ACTION==\"add\", ATTRS{idVendor}==\"054c\", ATTRS{idProduct}==\"06c1\", GROUP=\"plugdev\" >> /etc/udev/rules.d/nfcdev.rules'
$ sudo udevadm control -R # then re-attach device
```

以下は、あなたが提供したコードを基に作成したAPI仕様書です。

---

# API仕様書

## 基本URL
**`/`** - APIのルートパス

---

## エンドポイント一覧

| メソッド | URL                    | 概要                              |
| -------- | ---------------------- | --------------------------------- |
| `GET`    | `/`                    | APIのウェルカムメッセージを返す    |
| `GET`    | `/health`              | サービスの稼働状況を確認する       |
| `GET`    | `/get_uid`             | UIDを取得して暗号化する            |
| `POST`   | `/register_id`         | IDを登録する                      |
| `POST`   | `/register_attendance` | 勤怠状態を登録する                 |
| `DELETE` | `/remove_id`           | IDを削除する                      |
| `DELETE` | `/remove_attendance`   | 勤怠データを削除する               |

---

## エンドポイント詳細

### 1. ルートエンドポイント
- **メソッド**: `GET`
- **URL**: `/`
- **概要**: APIからのウェルカムメッセージを返します。
- **レスポンス**:  
  - **200 OK**
    ```json
    {
        "message": "Hello API Server!"
    }
    ```

---

### 2. ヘルスチェックエンドポイント
- **メソッド**: `GET`
- **URL**: `/health`
- **概要**: サービスの稼働状況を確認するためのエンドポイントです。
- **レスポンス**:  
  - **200 OK**
    ```json
    {
        "message": "Service is up and running"
    }
    ```

---

### 3. UID取得エンドポイント
- **メソッド**: `GET`
- **URL**: `/get_uid`
- **概要**: カードリーダーからUIDを取得し、暗号化して返します。
- **レスポンス**:  
  - **200 OK** - 成功時
    ```json
    {
        "message": "UID successfully read",
        "uid": "<encrypted_uid>"
    }
    ```
  - **400 Bad Request** - 失敗時
    ```json
    {
        "message": "Failed to read and encrypt UID"
    }
    ```
  - **500 Internal Server Error** - エラー発生時
    ```json
    {
        "code": 500,
        "message": "<error_message>"
    }
    ```

---

### 4. ID登録エンドポイント
- **メソッド**: `POST`
- **URL**: `/register_id`
- **概要**: IDを登録します。
- **リクエストボディ**:
    ```json
    {
        "id": "string",
        "name": "string",
        "attribute": "string",
        "description": "string"
    }
    ```
- **レスポンス**:  
  - **200 OK** - 登録成功時
    ```json
    {
        "code": 200,
        "message": "ID registration successful"
    }
    ```
  - **400 Bad Request** - 登録失敗時
    ```json
    {
        "code": 400,
        "message": "<error_message>"
    }
    ```
  - **500 Internal Server Error** - エラー発生時
    ```json
    {
        "code": 500,
        "message": "<error_message>"
    }
    ```

---

### 5. 勤怠登録エンドポイント
- **メソッド**: `POST`
- **URL**: `/register_attendance`
- **概要**: 勤怠状態を登録します。
- **リクエストボディ**:
    ```json
    {
        "id": "string",
        "next_state": "string"
    }
    ```
- **レスポンス**:  
  - **200 OK** - 登録成功時
    ```json
    {
        "code": 200,
        "message": "Attendance registration successful"
    }
    ```
  - **400 Bad Request** - 登録失敗時
    ```json
    {
        "code": 400,
        "message": "<error_message>"
    }
    ```
  - **500 Internal Server Error** - エラー発生時
    ```json
    {
        "code": 500,
        "message": "<error_message>"
    }
    ```

---

### 6. ID削除エンドポイント
- **メソッド**: `DELETE`
- **URL**: `/remove_id`
- **概要**: IDを削除します。
- **リクエストボディ**:
    ```json
    {
        "id": "string",
        "name": "string"
    }
    ```
- **レスポンス**:  
  - **200 OK** - 削除成功時
    ```json
    {
        "code": 200,
        "message": "ID removal successful"
    }
    ```
  - **400 Bad Request** - 削除失敗時
    ```json
    {
        "code": 400,
        "message": "<error_message>"
    }
    ```
  - **500 Internal Server Error** - エラー発生時
    ```json
    {
        "code": 500,
        "message": "<error_message>"
    }
    ```

---

### 7. 勤怠削除エンドポイント
- **メソッド**: `DELETE`
- **URL**: `/remove_attendance`
- **概要**: 勤怠データを削除します。
- **リクエストボディ**:
    ```json
    {
        "id": "string",
        "name": "string"
    }
    ```
- **レスポンス**:  
  - **200 OK** - 削除成功時
    ```json
    {
        "code": 200,
        "message": "Attendance removal successful"
    }
    ```
  - **400 Bad Request** - 削除失敗時
    ```json
    {
        "code": 400,
        "message": "<error_message>"
    }
    ```
  - **500 Internal Server Error** - エラー発生時
    ```json
    {
        "code": 500,
        "message": "<error_message>"
    }
    ```

---

## リクエスト/レスポンスボディ

### モデル

| モデル名               | 内容                                    |
| ---------------------- | --------------------------------------- |
| **RegisterIdRequest**   | ID登録リクエスト用                     |
| **RemoveIdRequest**     | ID削除リクエスト用                     |
| **RegisterAttendanceRequest** | 勤怠登録リクエスト用              |
| **RemoveAttendanceRequest**   | 勤怠削除リクエスト用              |
| **Response**            | 一般的なレスポンスフォーマット         |

---

### 1. `RegisterIdRequest`
```json
{
    "id": "string",
    "name": "string",
    "attribute": "string",
    "description": "string"
}
```

### 2. `RemoveIdRequest`
```json
{
    "id": "string",
    "name": "string"
}
```

### 3. `RegisterAttendanceRequest`
```json
{
    "id": "string",
    "next_state": "string"
}
```

### 4. `RemoveAttendanceRequest`
```json
{
    "id": "string",
    "name": "string"
}
```

### 5. `Response`
```json
{
    "code": 200,
    "message": "string"
}
```

---

この仕様書は、エンドポイントごとのリクエストとレスポンスの構造を説明しています。また、各モデルのリクエストボディとレスポンスボディも併せて記載しています。
