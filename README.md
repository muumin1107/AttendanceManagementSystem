# 【Raspberry Pi】カードリーダー式在室確認システム

## システム概要図

![システム概要図](https://github.com/user-attachments/assets/b5f0f476-435f-4df4-8c25-18ee629812f1)

## クラウド環境

- AWS Cloud（クラウドサーバー）

| APIサーバー          | データベース | アクセス制限 | 監視       |
----                  |----         |----         |----
| API Gateway, Lambda | DynamoDB    | IAM, WAF    | CloudWatch |

## 運用方法

- ユーザー登録時のプルダウンに表示される名前を変更（追加・削除）したい時

```
// RaspberryPiにSSHで接続する（認証情報は別途資料参照）
$ cd ~/attendance_system/web/frontend/
$ sudo nano .env

REACT_APP_API_BASE_URL=http://XXX.XXX.XXX.XXX:XXX/XXX
REACT_APP_USER_NAMES=山田 太郎,佐藤 花子,田中 敬一郎 //←ここに追記・削除（カンマ後は半角スペース不要）
REACT_APP_GRADES=RS,M2,M1,B4,B3
// Ctrl+x → y で保存して終了

$ sudo reboot
```

- ユーザー登録に関する全ての情報は毎年4月1日00:00AMに削除されるため，在校生は再度ユーザー登録が必要となる
- 基本的には，再起動で解決する場合が多い