import React from 'react';
import './ContributionGraph.css';

interface ContributionGraphProps {
userName: string;
year: number;
dailyData: { [date: string]: number };
}

const WEEKS_TO_SHOW = 53;
const DAYS_IN_WEEK = 7;

const getColorForTime = (minutes: number): string => {
if (minutes === 0) return 'color-level-0';
if (minutes <= 60) return 'color-level-1';
if (minutes <= 180) return 'color-level-2';
if (minutes <= 360) return 'color-level-3';
return 'color-level-4';
};

const ContributionGraph: React.FC<ContributionGraphProps> = ({ year, dailyData, userName }) => {
const today = new Date();
const endDate = new Date(year, today.getMonth(), today.getDate());
if (year < today.getFullYear()) {
    endDate.setFullYear(year, 11, 31);
} else {
    endDate.setFullYear(year);
}

const daysToShow = WEEKS_TO_SHOW * DAYS_IN_WEEK;
const startDate = new Date(endDate);
startDate.setDate(endDate.getDate() - daysToShow + 1);

const dates: Date[] = [];
for (let i = 0; i < daysToShow; i++) {
    const date = new Date(startDate);
    date.setDate(startDate.getDate() + i);
    dates.push(date);
}

const monthLabels = dates.reduce((acc, date, i) => {
    const month = date.toLocaleString('en-US', { month: 'short' });
    const prevMonth = i > 0 ? dates[i - 1].toLocaleString('en-US', { month: 'short' }) : '';
    if (month !== prevMonth) {
    acc.push({ month, index: Math.floor(i / DAYS_IN_WEEK) });
    }
    return acc;
}, [] as { month: string; index: number }[]);

return (
    <div className="graph-container-yearly">
    <h3 className="graph-title">{userName} - {year}年</h3>
    <div className="graph-grid">
        <div className="months-row">
        {monthLabels.map(({ month, index }) => (
            <div key={month} className="month-label" style={{ gridColumnStart: index + 1 }}>
            {month}
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
            {dates.map((date, i) => {
            const dateString = date.toISOString().split('T')[0];
            const minutes = dailyData[dateString] || 0;
            const colorClass = getColorForTime(minutes);
            const title = `${dateString}\n滞在時間: ${minutes}分`;

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