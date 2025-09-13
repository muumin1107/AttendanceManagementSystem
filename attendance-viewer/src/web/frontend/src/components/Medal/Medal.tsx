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
                width="50" 
                height="50" 
                viewBox="0 0 120 120" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
            >
                {/* メダルの外枠 */}
                <circle 
                    cx="60" 
                    cy="60" 
                    r="55" 
                    fill={`url(#medalGradient${rank})`}
                    stroke={colors.secondary}
                    strokeWidth="3"
                />
                
                {/* メダルの内側 */}
                <circle 
                    cx="60" 
                    cy="60" 
                    r="45" 
                    fill={`url(#innerGradient${rank})`}
                    stroke={colors.tertiary}
                    strokeWidth="2"
                />
                
                {/* 順位の数字 */}
                <text 
                    x="60" 
                    y="75" 
                    textAnchor="middle" 
                    fontSize="36" 
                    fontWeight="bold" 
                    fill="white"
                    stroke="#333"
                    strokeWidth="1"
                >
                    {rankText}
                </text>
                
                {/* キラキラエフェクト（1位のみ） */}
                {rank === 1 && (
                    <g fill="white" opacity="0.8">
                        <circle cx="35" cy="35" r="3">
                            <animate attributeName="opacity" values="0.3;1;0.3" dur="1.5s" repeatCount="indefinite" />
                        </circle>
                        <circle cx="85" cy="40" r="2.5">
                            <animate attributeName="opacity" values="1;0.3;1" dur="2s" repeatCount="indefinite" />
                        </circle>
                        <circle cx="30" cy="85" r="2">
                            <animate attributeName="opacity" values="0.5;1;0.5" dur="1.8s" repeatCount="indefinite" />
                        </circle>
                        <circle cx="90" cy="80" r="2.5">
                            <animate attributeName="opacity" values="1;0.2;1" dur="2.2s" repeatCount="indefinite" />
                        </circle>
                        
                        {/* 十字のキラキラ */}
                        <path d="M100 25 L102 23 L104 25 L102 27 Z">
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="0 102 25;360 102 25" 
                                dur="3s" 
                                repeatCount="indefinite"
                            />
                        </path>
                        <path d="M20 95 L22 93 L24 95 L22 97 Z">
                            <animateTransform 
                                attributeName="transform" 
                                type="rotate" 
                                values="180 22 95;540 22 95" 
                                dur="2.5s" 
                                repeatCount="indefinite"
                            />
                        </path>
                    </g>
                )}
                
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
                </defs>
            </svg>
        </div>
    );
};

export default Medal;