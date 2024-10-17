# 【ラズパイ】カードリーダー式勤怠管理システム

RaspberryPiを使ったカードリーダー式の勤怠管理システムを作成します．

## システム概要図

![システム概要図](https://github.com/user-attachments/assets/68536d9d-3d55-40ca-b80d-ccf64a32d61e)

## ユーザーインターフェース（一部）
- **確認画面**

![UIイメージ](https://github.com/user-attachments/assets/dcf3c998-1461-49b9-8bcf-6be652ccdd0f)

![image](https://github.com/user-attachments/assets/da1da3da-157a-421f-b71a-b26e224a4ee9)

- **勤怠画面**

![スクリーンショット 2024-10-08 020253](https://github.com/user-attachments/assets/df8d716a-8ead-415f-86ed-de99af2e30f1)

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

## API 使用説明書

### 概要
このAPIは、Notion APIを使用して勤怠管理システムのIDと勤怠データを管理します。以下の機能を提供し、IDの登録・削除、勤怠状態の登録・削除、システムのヘルスチェックを行います。APIはFastAPIを使用して実装されており、リクエストとレスポンスはJSON形式で行われます。

APIは、Notion API経由でデータベース操作を行い、各操作に対してデータの検証や重複チェックなどが行われます。

---

### エンドポイント一覧

| エンドポイント               | メソッド  | 機能                                         |
|-----------------------------|-----------|----------------------------------------------|
| `/`                         | `GET`     | APIのルートエンドポイント。ウェルカムメッセージを返します。 |
| `/docs`                     | `GET`     | 各APIのドキュメントを返却（表示）します。 |
| `/health`                   | `GET`     | サービスのヘルスチェックを行います。                  |
| `/register_id`              | `POST`    | IDを登録します。                             |
| `/remove_id`                | `DELETE`  | 登録されたIDを削除します。                   |
| `/register_attendance`      | `POST`    | 勤怠情報を登録します。                       |
| `/remove_attendance`        | `DELETE`  | 勤怠情報を削除します。                       |


---

### エンドポイント詳細

#### 1. ルートエンドポイント

**エンドポイント:**  
`GET /`

**説明:**  
APIのルートエンドポイントです。システムにアクセスする際にウェルカムメッセージを返します。

**レスポンス例:**  
```json
{
  "message": "Welcome to the Attendance System API"
}
```

---

#### 2. ヘルスチェックエンドポイント

**エンドポイント:**  
`GET /health`

**説明:**  
サービスの稼働状況を確認するためのエンドポイントです。正常に稼働している場合は、稼働中のメッセージを返します。

**レスポンス例:**  
```json
{
  "message": "Service is up and running"
}
```

---

#### 3. ID登録エンドポイント

**エンドポイント:**  
`POST /register_id`

**説明:**  
Notion APIを通じてID管理データベースに新しいIDを登録します。

**リクエストパラメータ:**

| パラメータ      | 型     | 説明                              |
|----------------|--------|-----------------------------------|
| `id`           | `str`  | 登録するユーザーのID                 |
| `name`         | `str`  | 登録するユーザーの名前               |
| `attribute`    | `str`  | 属性（例: ICカード, スマートフォン） |
| `description`  | `str`  | 備考                              |

**処理の流れ:**
1. データの検証（Notion APIを使用して、データが有効であるか確認）。
2. IDの重複チェック（すでに登録済みのIDか確認）。
3. 登録処理（重複していない場合、IDを登録）。

**レスポンス例:**  
- 成功時:
```json
{
  "code": 200,
  "message": "ID registration successful"
}
```
- 失敗時:
```json
{
  "code": 400,
  "message": "Duplicate ID"
}
```

---

#### 4. ID削除エンドポイント

**エンドポイント:**  
`DELETE /remove_id`

**説明:**  
Notion APIを通じて、ID管理データベースから指定されたIDを削除します。

**リクエストパラメータ:**

| パラメータ      | 型     | 説明               |
|----------------|--------|--------------------|
| `id`           | `str`  | 削除するユーザーのID   |
| `name`         | `str`  | 削除対象のユーザー名   |

**処理の流れ:**
1. IDと名前の照合（IDと名前が一致するか確認）。
2. 一致した場合に削除処理を行う。

**レスポンス例:**  
- 成功時:
```json
{
  "code": 200,
  "message": "ID removal successful"
}
```
- 失敗時:
```json
{
  "code": 400,
  "message": "ID not found"
}
```

---

#### 5. 勤怠登録エンドポイント

**エンドポイント:**  
`POST /register_attendance`

**説明:**  
Notion APIを通じて勤怠管理データベースに勤怠情報を登録します。

**リクエストパラメータ:**

| パラメータ      | 型     | 説明               |
|----------------|--------|--------------------|
| `id`           | `str`  | 勤怠情報を登録するユーザーのID |
| `next_state`   | `str`  | 次の勤怠状態（例: 出勤, 退勤）  |

**処理の流れ:**
1. IDに基づいて名前を取得（IDが存在するか確認）。
2. 勤怠状態の検証（次の状態が有効であるかを確認）。
3. 勤怠情報の登録（時間情報も含めて登録）。

**レスポンス例:**  
- 成功時:
```json
{
  "code": 200,
  "message": "Attendance registration successful"
}
```
- 失敗時:
```json
{
  "code": 400,
  "message": "Invalid state transition"
}
```

---

#### 6. 勤怠削除エンドポイント

**エンドポイント:**  
`DELETE /remove_attendance`

**説明:**  
Notion APIを通じて勤怠管理データベースから指定された勤怠データを削除します。

**リクエストパラメータ:**

| パラメータ      | 型     | 説明                 |
|----------------|--------|----------------------|
| `id`           | `str`  | 削除する勤怠データのID  |
| `name`         | `str`  | 削除対象のユーザー名     |

**処理の流れ:**
1. IDと名前の照合（IDと名前が一致するか確認）。
2. 一致した場合に勤怠データを削除。

**レスポンス例:**  
- 成功時:
```json
{
  "code": 200,
  "message": "Attendance removal successful"
}
```
- 失敗時:
```json
{
  "code": 400,
  "message": "Attendance data not found"
}
```

---

### 内部機能

APIの実装は、`AttendanceSystemOperation` クラスによって操作が管理されています。このクラスは、Notion APIを介してデータの追加、削除、検証を行います。以下は主要な内部関数です。

1. **`_verify_id_and_name(id: str, name: str)`**
   - 指定されたIDと名前が一致するかを検証します。
   - 一致しない場合、エラーメッセージを返します。

2. **`register_id(id: str, name: str, attribute: str, description: str)`**
   - IDをNotionデータベースに登録します。
   - データの検証や重複チェックを行います。

3. **`remove_id(id: str, name: str)`**
   - 指定されたIDをNotionデータベースから削除します。
   - IDと名前が一致することを確認後、削除処理を実行します。

4. **`register_attendance(id: str, next_state: str)`**
   - 勤怠データベースに新しい勤怠情報を登録します。
   - 勤怠状態が正しいかを検証し、データをNotionに追加します。

5. **`remove_attendance(id: str, name: str)`**
   - 勤怠データベースから指定された勤怠情報を削除します。

---

### エラーレスポンス
各エンドポイントでエラーが発生した場合、適切なHTTPステータスコードとともにエラーメッセージが返されます。

**エラーレスポンス例:**  
```json
{
  "code": 500,
  "message": "Internal server error"
}
```

---

### 備考
APIは、Notion APIと連携してデータベース操作を行います。運用環境では、必要に応じて認証機構（例: OAuth2, JWT）やパフォーマンス最適化を考慮してください。また、データベース構造やデータの管理方法に応じて適切なエラーハンドリングを行うことを推奨します。
