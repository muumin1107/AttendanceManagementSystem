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
// 注: minutes === 0 の場合に色を付けたい場合は、この条件を変更してください
if (minutes === 0) return 'color-level-0';
if (minutes <= 60) return 'color-level-1';
if (minutes <= 180) return 'color-level-2';
if (minutes <= 360) return 'color-level-3';
return 'color-level-4';
};


const ContributionGraph: React.FC<ContributionGraphProps> = ({ year, dailyData, userName }) => {

const getCalendarData = () => {
    const weeks: Date[][] = [];
    const monthLabelPositions: { label: string; index: number }[] = [];
    const firstDayOfYear = new Date(year, 0, 1);
    const dayOfWeek = firstDayOfYear.getDay(); // 0=Sun, 1=Mon...

    const startDate = new Date(firstDayOfYear);
    startDate.setDate(firstDayOfYear.getDate() - dayOfWeek);

    let lastMonth = -1;

    // 53週分のデータを生成
    for (let weekIndex = 0; weekIndex < WEEKS_TO_SHOW; weekIndex++) {
    const currentWeek: Date[] = [];
    // 1週間（7日分）のデータを生成
    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
        // --- ★★★ ここからが修正箇所 ★★★ ---
        // 毎回新しいDateオブジェクトを作るのではなく、一つのDateオブジェクトを使い回して日付を1日ずつ進める
        const date = new Date(
        startDate.getFullYear(),
        startDate.getMonth(),
        startDate.getDate() + (weekIndex * 7) + dayIndex
        );
        // --- ★★★ ここまでが修正箇所 ★★★ ---
        
        currentWeek.push(date);

        // 月のラベル位置を計算
        if (date.getFullYear() === year && date.getMonth() !== lastMonth) {
        monthLabelPositions.push({ label: MONTH_LABELS[date.getMonth()], index: weekIndex });
        lastMonth = date.getMonth();
        }
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

                const dateString = date.toISOString().split('T')[0];
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