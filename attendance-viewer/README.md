# 【Raspberry Pi】カードリーダー式在籍確認システム（attendance-viewer）

## システム環境

- AWS

| サービス名   | 用途                          |
----          |----
| Amplify     | Webホスティング               |
| API Gateway | APIルーティング・WebSocket接続 |
| Lambda      | API処理実行                   |

## プロジェクト構成

```
src/web/frontend/
├── public/
│   └── ...                   # 静的ファイル（favicon, index.html等）
│
├── src/
│   ├── hooks/                # カスタムフック
│   │   ├── useAttendanceSocket.ts
│   │   └── useGetAttendance.ts
│   │
│   ├── pages/                # ページごとのコンポーネント
│   │   ├── ErrorPage/
│   │   │   ├── ErrorPage.tsx
│   │   │   └── ErrorPage.css
│   │   ├── HomePage/
│   │   │   ├── HomePage.tsx
│   │   │   └── HomePage.css
│   │   └── LoadingPage/
│   │       ├── LoadingPage.tsx
│   │       └── LoadingPage.css
│   │
│   ├── types/                # 型定義
│   │   └── attendance.ts
│   │
│   ├── App.css
│   ├── App.tsx
│   ├── index.css
│   └── index.tsx             # エントリーポイント
│
├── package.json
└── tsconfig.json
```

## 開発言語

- React（フロントエンド）

## 表示部の設定

- 自動起動用の設定ファイルを作成

```
$ mkdir -p ~/.config/autostart
$ nano ~/.config/autostart/kiosk.desktop

// 以下を記入
[Desktop Entry]
Type=Application
Name=Kiosk
Comment=Kiosk mode browser
Exec=chromium-browser --kiosk --noerrdialogs --disable-infobars --disable-extensions https://XXX

$ sudo reboot
```

- スクリーンセーバーと省電力設定の無効化

```
$ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

// 末尾に以下を追記
@xset s noblank
@xset s off
@xset -dpms
```

- マウスカーソルを非表示にする

```
$ sudo raspi-config

// カーソルキーで「6 Advanced Options」を選択
// 「A6 Wayland or X11」を選択
// 「W1 X11」を選択

$ sudo apt update
$ sudo apt install unclutter -y
$ sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

// 末尾に以下を追記
@unclutter -idle 1 -root

$ sudo reboot
```
