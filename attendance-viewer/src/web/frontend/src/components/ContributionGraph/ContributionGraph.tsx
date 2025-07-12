import React from 'react';
import './ContributionGraph.css';

interface ContributionGraphProps {
userName: string;
year: number;
dailyData: { [date: string]: number };
}

const WEEKS_TO_SHOW = 53;
const DAYS_IN_WEEK = 7;
const MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const getColorForTime = (minutes: number): string => {
if (minutes === 0) return 'color-level-0';
if (minutes <= 60) return 'color-level-1';
if (minutes <= 180) return 'color-level-2';
if (minutes <= 360) return 'color-level-3';
return 'color-level-4';
};

const ContributionGraph: React.FC<ContributionGraphProps> = ({ year, dailyData, userName }) => {
const getCalendarDays = () => {
    const calendarDays = [];
    const firstDayOfYear = new Date(year, 0, 1);
    const dayOfWeek = firstDayOfYear.getDay(); // 0=Sun, 1=Mon...
    
    // グリッドの開始日を、1月1日が含まれる週の日曜日に設定
    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() - dayOfWeek);

    for (let i = 0; i < WEEKS_TO_SHOW * DAYS_IN_WEEK; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    calendarDays.push(date);
    }
    return calendarDays;
};

const calendarDays = getCalendarDays();
const monthLabels = MONTH_LABELS.map((month, index) => {
    const firstDayOfMonth = new Date(year, index, 1);
    const firstDayOfYear = new Date(year, 0, 1);
    const diff = Math.floor((firstDayOfMonth.getTime() - firstDayOfYear.getTime()) / (1000 * 60 * 60 * 24));
    const weekIndex = Math.floor((diff + firstDayOfYear.getDay()) / DAYS_IN_WEEK);
    return { label: month, weekIndex };
});

return (
    <div className="graph-container-yearly">
    <h3 className="graph-title">{userName} - {year}年</h3>
    <div className="graph-grid">
        <div className="months-row">
        {monthLabels.map(({ label, weekIndex }) => (
            <div key={label} className="month-label" style={{ gridColumnStart: weekIndex + 1 }}>
            {label}
            </div>
        ))}
        </div>
        <div className="days-and-cells">
        <div className="days-col">
            <span>Mon</span>
            <span>Wed</span>
            <span>Fri</span>
        </div>
        <div className="cells-grid">
            {calendarDays.map((date, i) => {
            const isDateInCurrentYear = date.getFullYear() === year;
            const dateString = date.toISOString().split('T')[0];
            // 今年の日付でなければデータは0として扱う
            const minutes = isDateInCurrentYear ? (dailyData[dateString] || 0) : 0;
            const colorClass = getColorForTime(minutes);
            const title = `${dateString}\n滞在時間: ${minutes}分`;
            
            // 今年の日付でないセルは非表示（または薄く）する
            if (!isDateInCurrentYear) {
                return <div key={i} className="cell empty" />;
            }

            return <div key={i} className={`cell ${colorClass}`} title={title} />;
            })}
        </div>
        </div>
    </div>
    <div className="legend">
        <span>Less</span>
        <div className="cell color-level-0"></div>
        <div className="cell color-level-1"></div>
        <div className="cell color-level-2"></div>
        <div className="cell color-level-3"></div>
        <div className="cell color-level-4"></div>
        <span>More</span>
    </div>
    </div>
);
};

export default ContributionGraph;