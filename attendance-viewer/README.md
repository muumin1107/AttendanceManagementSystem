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
