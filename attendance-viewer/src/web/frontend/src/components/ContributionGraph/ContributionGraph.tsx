import React from 'react';
import './ContributionGraph.css';

interface ContributionGraphProps {
userName: string;
year: number;
dailyData: { [date: string]: number };
}

const MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const WEEKS_TO_SHOW = 53;

const getColorForTime = (minutes: number): string => {
if (minutes === 0) return 'color-level-0';
if (minutes <= 60) return 'color-level-1';
if (minutes <= 180) return 'color-level-2';
if (minutes <= 360) return 'color-level-3';
return 'color-level-4';
};

// タイムゾーン問題を回避して 'YYYY-MM-DD' 形式の文字列を生成する関数
const toISODateString = (date: Date): string => {
const y = date.getFullYear();
const m = String(date.getMonth() + 1).padStart(2, '0');
const d = String(date.getDate()).padStart(2, '0');
return `${y}-${m}-${d}`;
};

const ContributionGraph: React.FC<ContributionGraphProps> = ({ year, dailyData, userName }) => {
const getCalendarData = () => {
    const weeks: Date[][] = [];
    const monthLabelPositions: { label: string; index: number }[] = [];
    const firstDayOfYear = new Date(year, 0, 1);
    const dayOfWeek = firstDayOfYear.getDay();

    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() - dayOfWeek);

    let lastMonth = -1;
    let currentDate = new Date(startDate); // この日付オブジェクトを1日ずつ進めていく

    for (let weekIndex = 0; weekIndex < WEEKS_TO_SHOW; weekIndex++) {
    const currentWeek: Date[] = [];
    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
        currentWeek.push(new Date(currentDate)); // 現在の日付を週に追加

        if (currentDate.getFullYear() === year && currentDate.getMonth() !== lastMonth) {
        monthLabelPositions.push({ label: MONTH_LABELS[currentDate.getMonth()], index: weekIndex });
        lastMonth = currentDate.getMonth();
        }

        // 日付を1日進める
        currentDate.setDate(currentDate.getDate() + 1);
    }
    weeks.push(currentWeek);
    }
    return { weeks, monthLabelPositions };
};

const { weeks, monthLabelPositions } = getCalendarData();

return (
    <div className="graph-container-yearly">
    <h3 className="graph-title">{userName} - {year}年</h3>
    <div className="graph-grid">
        <div className="months-row">
        {monthLabelPositions.map(({ label, index }) => (
            <div key={label} className="month-label" style={{ gridColumnStart: index + 1 }}>
            {label}
            </div>
        ))}
        </div>
        <div className="days-and-cells">
        <div className="days-col">
            <span>Sun</span>
            <span>Mon</span>
            <span>Tue</span>
            <span>Wed</span>
            <span>Thu</span>
            <span>Fri</span>
            <span>Sat</span>
        </div>
        <div className="cells-grid">
            {weeks.map((week, weekIndex) => (
            <div key={weekIndex} className="week-col">
                {week.map((date, dayIndex) => {
                if (date.getFullYear() !== year) {
                    return <div key={dayIndex} className="cell empty" />;
                }

                // タイムゾーン問題を回避する関数を使用
                const dateString = toISODateString(date);
                const minutes = dailyData[dateString] || 0;
                const colorClass = getColorForTime(minutes);
                const title = `${dateString}\n滞在時間: ${minutes}分`;

                return <div key={dayIndex} className={`cell ${colorClass}`} title={title} />;
                })}
            </div>
            ))}
        </div>
        </div>
    </div>
    <div className="legend">
        {/* ... 凡例部分は変更なし ... */}
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