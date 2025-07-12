import React from 'react';
import './ContributionGraph.css'; // CSSファイルをインポート

interface ContributionGraphProps {
userName: string;
dailyData: { [date: string]: number } | null;
currentMonth: Date;
onPrevMonth: () => void;
onNextMonth: () => void;
}

// 時間に応じてセルの色を決定するヘルパー関数 (GitHub風の4段階)
const getColorForTime = (minutes: number): string => {
if (minutes === 0) return 'color-level-0';
if (minutes <= 60) return 'color-level-1';
if (minutes <= 180) return 'color-level-2';
if (minutes <= 360) return 'color-level-3';
return 'color-level-4';
};

// 曜日を英語の略称で取得する関数
const getDayAbbreviation = (date: Date): string => {
return date.toLocaleDateString('en-US', { weekday: 'short' });
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
const firstDayOfMonth = new Date(year, month, 1);
const startDayOfWeek = firstDayOfMonth.getDay(); // 0: Sunday, 1: Monday, ...

// 月の省略名を取得
const monthAbbreviation = currentMonth.toLocaleDateString('en-US', { month: 'short' });

// 週ごとの日付配列を生成
const weeks: Date[][] = [];
let currentWeek: Date[] = [];
let currentDate = new Date(year, month, 1 - startDayOfWeek + 1); // Adjust to start from the first Monday (or closest)

for (let i = 0; i < 7 * 7; i++) { // Maximum 7 weeks
    if (currentDate.getMonth() === month || (weeks.length === 0 && currentDate.getMonth() < month) || (currentWeek.length > 0 && currentDate.getMonth() > month)) {
    currentWeek.push(new Date(currentDate));
    } else {
    currentWeek.push(new Date(NaN)); // Placeholder for days outside the current month
    }

    if (currentWeek.length === 7) {
    weeks.push(currentWeek);
    currentWeek = [];
    }
    currentDate.setDate(currentDate.getDate() + 1);
    if (weeks.length > 0 && currentWeek.length === 0 && currentDate.getMonth() > month) {
    break; // Stop if we've moved to the next month and a new week hasn't started
    }
}

// 表示する曜日 (月、水、金)
const displayDays = ['Mon', 'Wed', 'Fri'];

return (
    <div className="contribution-graph-container-github">
    <div className="header">
        <h2>{userName} - {year} contributions</h2>
        <div className="month-navigator">
        <button onClick={onPrevMonth}>&lt; {new Date(year, month - 1, 1).toLocaleDateString('en-US', { month: 'short' })}</button>
        <span>{monthAbbreviation}, {year}</span>
        <button onClick={onNextMonth}>{new Date(year, month + 1, 1).toLocaleDateString('en-US', { month: 'short' })} &gt;</button>
        </div>
    </div>
    <div className="graph-area">
        <div className="weekday-labels">
        {displayDays.map(day => <div key={day}>{day}</div>)}
        </div>
        <div className="months-grid">
        {weeks.map((week, weekIndex) => (
            <div key={weekIndex} className="week">
            {week.map((date, dayIndex) => {
                const dayAbbr = getDayAbbreviation(date);
                if (!isNaN(date.getTime()) && displayDays.includes(dayAbbr)) {
                const dateString = `${year}-${String(month + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
                const minutes = dailyData?.[dateString] || 0;
                const colorClass = getColorForTime(minutes);
                const title = `${date.toLocaleDateString()}\n滞在時間: ${minutes}分`;
                return <div key={dayIndex} className={`day-cell-github ${colorClass}`} title={title}></div>;
                } else {
                return <div key={dayIndex} className="day-cell-github empty"></div>;
                }
            })}
            </div>
        ))}
        </div>
    </div>
    <div className="legend">
        <span>Less</span>
        <div className="colors">
        <div className="color-level-0"></div>
        <div className="color-level-1"></div>
        <div className="color-level-2"></div>
        <div className="color-level-3"></div>
        <div className="color-level-4"></div>
        </div>
        <span>More</span>
    </div>
    </div>
);
};

export default ContributionGraph;