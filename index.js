// index.js
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "react-oidc-context";

const cognitoAuthConfig = {
authority: "https://cognito-idp.ap-northeast-1.amazonaws.com/ap-northeast-1_ut9Rv6MVF",
client_id: "pitulldfmd72uemp676cgbhki",
redirect_uri: "https://main.d3hsg05q19yok9.amplifyapp.com/",
response_type: "code",
scope: "phone openid email",
};

const root = ReactDOM.createRoot(document.getElementById("root"));

// wrap the application with AuthProvider
root.render(
<React.StrictMode>
    <AuthProvider {...cognitoAuthConfig}>
    <App />
    </AuthProvider>
</React.StrictMode>
);