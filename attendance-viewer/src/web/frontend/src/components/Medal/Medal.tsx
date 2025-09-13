import React from 'react';
import './Medal.css';

interface MedalProps {
    rank: 1 | 2 | 3;
    className?: string;
}

const Medal: React.FC<MedalProps> = ({ rank, className = '' }) => {
    const getMedalColor = () => {
        switch (rank) {
            case 1: return { primary: '#FFD700', secondary: '#FFA500', tertiary: '#FF8C00' }; // 金
            case 2: return { primary: '#C0C0C0', secondary: '#A8A8A8', tertiary: '#808080' }; // 銀
            case 3: return { primary: '#CD7F32', secondary: '#B8860B', tertiary: '#8B4513' }; // 銅
        }
    };

    const colors = getMedalColor();
    const rankText = rank.toString();

    return (
        <div className={`medal medal-${rank} ${className}`} title={`過去7日間で在室時間${rank}位のユーザー`}>
            <svg 
                width="60" 
                height="80" 
                viewBox="0 0 120 150" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
            >
                {/* メダルの紐 */}
                <path 
                    d="M45 10 Q50 5 60 5 Q70 5 75 10 L70 30 Q65 25 60 25 Q55 25 50 30 Z" 
                    fill={`url(#ribbonGradient${rank})`}
                    stroke={colors.tertiary}
                    strokeWidth="1"
                />
                <path 
                    d="M50 30 Q55 35 60 35 Q65 35 70 30 L75 50 Q70 45 60 45 Q50 45 45 50 Z" 
                    fill={`url(#ribbonGradient${rank})`}
                    stroke={colors.tertiary}
                    strokeWidth="1"
                />
                
                {/* メダルの外枠 */}
                <circle 
                    cx="60" 
                    cy="90" 
                    r="55" 
                    fill={`url(#medalGradient${rank})`}
                    stroke={colors.secondary}
                    strokeWidth="3"
                />
                
                {/* メダルの内側 */}
                <circle 
                    cx="60" 
                    cy="90" 
                    r="45" 
                    fill={`url(#innerGradient${rank})`}
                    stroke={colors.tertiary}
                    strokeWidth="2"
                />
                
                {/* 順位の数字（大きくした） */}
                <text 
                    x="60" 
                    y="110" 
                    textAnchor="middle" 
                    fontSize="48" 
                    fontWeight="bold" 
                    fill="white"
                    stroke="#333"
                    strokeWidth="2"
                    fontFamily="Arial, sans-serif"
                >
                    {rankText}
                </text>
                
                {/* 強化されたキラキラエフェクト */}
                <g fill="white" opacity="0.9">
                    {/* 大きなキラキラ */}
                    <circle cx="25" cy="65" r="4">
                        <animate attributeName="opacity" values="0.2;1;0.2" dur="1.2s" repeatCount="indefinite" />
                        <animate attributeName="r" values="3;5;3" dur="1.2s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="95" cy="70" r="3.5">
                        <animate attributeName="opacity" values="1;0.2;1" dur="1.8s" repeatCount="indefinite" />
                        <animate attributeName="r" values="2.5;4.5;2.5" dur="1.8s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="30" cy="115" r="3">
                        <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite" />
                        <animate attributeName="r" values="2;4;2" dur="1.5s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="90" cy="110" r="3.5">
                        <animate attributeName="opacity" values="1;0.3;1" dur="2.1s" repeatCount="indefinite" />
                        <animate attributeName="r" values="3;5;3" dur="2.1s" repeatCount="indefinite" />
                    </circle>
                    
                    {/* 中サイズのキラキラ */}
                    <circle cx="40" cy="50" r="2.5">
                        <animate attributeName="opacity" values="0.6;1;0.6" dur="1.7s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="80" cy="55" r="2">
                        <animate attributeName="opacity" values="1;0.4;1" dur="2.3s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="35" cy="130" r="2.5">
                        <animate attributeName="opacity" values="0.5;1;0.5" dur="1.9s" repeatCount="indefinite" />
                    </circle>
                    <circle cx="85" cy="125" r="2">
                        <animate attributeName="opacity" values="1;0.5;1" dur="2.5s" repeatCount="indefinite" />
                    </circle>
                    
                    {/* 星型のキラキラ */}
                    <g>
                        <path d="M20 80 L22 85 L27 85 L23 88 L25 93 L20 90 L15 93 L17 88 L13 85 L18 85 Z">
                            <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite" />
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="0 20 88;360 20 88" 
                                dur="4s" 
                                repeatCount="indefinite"
                            />
                        </path>
                        <path d="M100 85 L102 90 L107 90 L103 93 L105 98 L100 95 L95 98 L97 93 L93 90 L98 90 Z">
                            <animate attributeName="opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite" />
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="180 100 93;540 100 93" 
                                dur="3.5s" 
                                repeatCount="indefinite"
                            />
                        </path>
                    </g>
                    
                    {/* 十字のキラキラ（拡張） */}
                    <g>
                        <path d="M110 35 L113 32 L116 35 L113 38 Z">
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="0 113 35;360 113 35" 
                                dur="2.8s" 
                                repeatCount="indefinite"
                            />
                            <animate attributeName="opacity" values="0.5;1;0.5" dur="1.4s" repeatCount="indefinite" />
                        </path>
                        <path d="M10 120 L13 117 L16 120 L13 123 Z">
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="180 13 120;540 13 120" 
                                dur="2.2s" 
                                repeatCount="indefinite"
                            />
                            <animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite" />
                        </path>
                        <path d="M105 140 L108 137 L111 140 L108 143 Z">
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="0 108 140;360 108 140" 
                                dur="3.2s" 
                                repeatCount="indefinite"
                            />
                            <animate attributeName="opacity" values="0.7;1;0.7" dur="1.6s" repeatCount="indefinite" />
                        </path>
                    </g>
                </g>
                
                {/* グラデーション定義 */}
                <defs>
                    <radialGradient id={`medalGradient${rank}`} cx="50%" cy="30%" r="70%">
                        <stop offset="0%" stopColor={colors.primary} />
                        <stop offset="70%" stopColor={colors.secondary} />
                        <stop offset="100%" stopColor={colors.tertiary} />
                    </radialGradient>
                    <radialGradient id={`innerGradient${rank}`} cx="50%" cy="40%" r="60%">
                        <stop offset="0%" stopColor={colors.secondary} />
                        <stop offset="100%" stopColor={colors.tertiary} />
                    </radialGradient>
                    <linearGradient id={`ribbonGradient${rank}`} x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor={colors.primary} />
                        <stop offset="50%" stopColor={colors.secondary} />
                        <stop offset="100%" stopColor={colors.primary} />
                    </linearGradient>
                </defs>
            </svg>
        </div>
    );
};

export default Medal;