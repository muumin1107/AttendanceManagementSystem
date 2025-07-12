import React from 'react';
import './ContributionGraph.css';

interface ContributionGraphProps {
userName: string;
dailyData: { [date: string]: number } | null;
currentMonth: Date;
onPrevMonth: () => void;
onNextMonth: () => void;
}

// 時間に応じてセルの色を決定するヘルパー関数
const getColorForTime = (minutes: number): string => {
if (minutes === 0) return 'color-level-0';
if (minutes <= 60) return 'color-level-1';
if (minutes <= 180) return 'color-level-2';
if (minutes <= 360) return 'color-level-3';
return 'color-level-4';
};

const ContributionGraph: React.FC<ContributionGraphProps> = ({
userName,
dailyData,
currentMonth,
onPrevMonth,
onNextMonth,
}) => {
const year = currentMonth.getFullYear();
const month = currentMonth.getMonth();
const daysInMonth = new Date(year, month + 1, 0).getDate();

const dayHeaders = Array.from({ length: daysInMonth }, (_, i) => <th key={i + 1}>{i + 1}</th>);

const formatDateString = (day: number): string => {
    return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
};

return (
    <div className="contribution-graph-container">
    <div className="month-navigator">
        <button onClick={onPrevMonth}>&lt; 前の月</button>
        <h3>{userName} - {year}年 {month + 1}月</h3>
        <button onClick={onNextMonth}>次の月 &gt;</button>
    </div>
    <table className="contribution-table">
        <thead>
        <tr>{dayHeaders}</tr>
        </thead>
        <tbody>
        <tr>
            {Array.from({ length: daysInMonth }, (_, i) => {
            const day = i + 1;
            const dateString = formatDateString(day);
            const minutes = dailyData?.[dateString] || 0;
            const colorClass = getColorForTime(minutes);
            const title = `${dateString}\n在室時間: ${minutes}分`;

            return <td key={day} className={`day-cell ${colorClass}`} title={title}></td>;
            })}
        </tr>
        </tbody>
    </table>
    </div>
);
};

export default ContributionGraph;