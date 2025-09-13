import React from 'react';
import './Crown.css';

interface CrownProps {
    className?: string;
}

const Crown: React.FC<CrownProps> = ({ className = '' }) => {
    return (
        <div className={`crown ${className}`} title="過去7日間で最も在室時間が長いユーザー">
            <svg 
                width="28" 
                height="24" 
                viewBox="0 0 24 19" 
                fill="none" 
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"
                    fill="#FFD700"
                    stroke="#FFA500"
                    strokeWidth="1"
                />
                <path
                    d="M12 5L13.5 9H18L14.5 12L16 16L12 13L8 16L9.5 12L6 9H10.5L12 5Z"
                    fill="#FFF8DC"
                />
                {/* 王冠の装飾的な点 */}
                <circle cx="12" cy="8" r="1" fill="#FF6347" />
                <circle cx="9" cy="10" r="0.8" fill="#FF6347" />
                <circle cx="15" cy="10" r="0.8" fill="#FF6347" />
            </svg>
        </div>
    );
};

export default Crown;