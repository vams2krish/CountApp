"""CSS styles for MathBlitz - Modern Clean Design"""

# Store CSS as a string for easy access
CSS_CONTENT = """
<style>
/* ==================== FONTS ==================== */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ==================== BASE STYLES ==================== */
* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background: linear-gradient(135deg, #F5F7FA 0%, #E8ECF1 50%, #DEE2E8 100%);
    min-height: 100vh;
}

/* ==================== TYPOGRAPHY ==================== */
.main-title {
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #0066CC 0%, #004999 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: -0.02em;
}

.page-title {
    font-size: 1.75rem !important;
    font-weight: 700 !important;
    color: #1A1A2E !important;
    margin-bottom: 1.5rem !important;
}

.section-title {
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    color: #1A1A2E !important;
    margin-bottom: 1rem !important;
}

/* ==================== CARDS ==================== */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    border: 1px solid #E5E9F0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: box-shadow 0.3s ease, transform 0.2s ease;
}

.card:hover {
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.card-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #E5E9F0;
}

.card-icon {
    font-size: 1.5rem;
}

.card-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1A1A2E;
    margin: 0;
}

/* ==================== BUTTONS ==================== */
.stButton > button {
    border-radius: 12px !important;
    padding: 14px 28px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Primary Button */
.primary-btn > button,
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%) !important;
    color: white !important;
}

.primary-btn > button:hover,
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #0052A3 0%, #004999 100%) !important;
    box-shadow: 0 4px 16px rgba(0, 102, 204, 0.3) !important;
}

/* Secondary Button */
.secondary-btn > button {
    background: #FFFFFF !important;
    color: #0066CC !important;
    border: 2px solid #0066CC !important;
}

.secondary-btn > button:hover {
    background: #F0F7FF !important;
}

/* Success Button */
.success-btn > button {
    background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%) !important;
    color: white !important;
}

/* Danger Button */
.danger-btn > button {
    background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%) !important;
    color: white !important;
}

/* ==================== TASK DISPLAY ==================== */
.task-display {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin: 24px 0;
    border: 2px solid #E5E9F0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.task-display-correct {
    border-color: #22C55E !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #F0FDF4 100%) !important;
}

.task-display-incorrect {
    border-color: #EF4444 !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #FEF2F2 100%) !important;
}

.task-question {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1A1A2E;
    margin: 16px 0;
}

.task-question .highlight {
    color: #0066CC;
    font-weight: 700;
}

.task-question .accent {
    color: #FF6B6B;
    font-weight: 700;
}

.exercise-icon {
    font-size: 3.5rem;
    display: block;
    margin-bottom: 8px;
}

.exercise-name {
    font-size: 1.25rem;
    font-weight: 600;
    color: #64748B;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ==================== INPUTS ==================== */
.stNumberInput > div > div > input,
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #FFFFFF !important;
    border: 2px solid #E5E9F0 !important;
    border-radius: 12px !important;
    color: #1A1A2E !important;
    font-size: 1.1rem !important;
    padding: 12px 16px !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}

.stNumberInput > div > div > input:focus,
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #0066CC !important;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
    outline: none !important;
}

.stSelectbox > div > div > div {
    background: #FFFFFF !important;
    border: 2px solid #E5E9F0 !important;
    border-radius: 12px !important;
}

.stSelectbox > div > div > div:focus-within {
    border-color: #0066CC !important;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
}

/* ==================== STAT CARDS ==================== */
.stat-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    border: 1px solid #E5E9F0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.stat-card .stat-icon {
    font-size: 2rem;
    margin-bottom: 8px;
}

.stat-card .stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #1A1A2E;
    font-family: 'JetBrains Mono', monospace;
}

.stat-card .stat-label {
    font-size: 0.875rem;
    color: #64748B;
    font-weight: 500;
}

/* ==================== FORMULA BOX ==================== */
.formula-box {
    background: linear-gradient(135deg, #F0F7FF 0%, #E8F4FD 100%);
    border-radius: 16px;
    padding: 20px;
    margin: 16px 0;
    border-left: 4px solid #0066CC;
}

.formula-title {
    color: #0066CC;
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.formula-text {
    color: #1A1A2E;
    font-size: 1.25rem;
    font-weight: 600;
    font-family: 'JetBrains Mono', monospace;
    text-align: center;
    padding: 12px;
    background: rgba(255, 255, 255, 0.8);
    border-radius: 8px;
    margin: 8px 0;
}

.formula-example {
    color: #64748B;
    font-size: 0.9rem;
    margin-top: 8px;
}

.formula-tip {
    color: #FF6B6B;
    font-size: 0.875rem;
    font-weight: 500;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #D0E3F0;
}

/* ==================== TIMER ==================== */
.timer-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    background: #FFFFFF;
    border-radius: 16px;
    border: 2px solid #E5E9F0;
}

.timer-ring {
    width: 80px;
    height: 80px;
    position: relative;
}

.timer-ring svg {
    transform: rotate(-90deg);
}

.timer-ring-bg {
    fill: none;
    stroke: #E5E9F0;
    stroke-width: 6;
}

.timer-ring-progress {
    fill: none;
    stroke: #22C55E;
    stroke-width: 6;
    stroke-linecap: round;
    transition: stroke-dashoffset 0.5s ease;
}

.timer-ring-progress.warning {
    stroke: #F59E0B;
}

.timer-ring-progress.danger {
    stroke: #EF4444;
}

.timer-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.25rem;
    font-weight: 700;
    color: #1A1A2E;
    font-family: 'JetBrains Mono', monospace;
}

/* Simple Timer Display */
.timer-display {
    text-align: center;
    padding: 12px 20px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 1.1rem;
    font-family: 'JetBrains Mono', monospace;
}

.timer-easy {
    background: #DCFCE7;
    color: #16A34A;
}

.timer-medium {
    background: #FEF3C7;
    color: #D97706;
}

.timer-hard {
    background: #FEE2E2;
    color: #DC2626;
}

/* ==================== LEADERBOARD ==================== */
.leaderboard-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #E5E9F0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.leaderboard-title {
    color: #1A1A2E;
    font-size: 1rem;
    font-weight: 700;
    text-align: center;
    margin-bottom: 16px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.leaderboard-item {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    margin: 8px 0;
    border-radius: 12px;
    background: #F8FAFC;
    transition: background 0.2s ease;
}

.leaderboard-item:hover {
    background: #F1F5F9;
}

.leaderboard-item.top-1 {
    background: linear-gradient(135deg, #FEF9C3 0%, #FDE047 100%);
}

.leaderboard-item.top-2 {
    background: linear-gradient(135deg, #F1F5F9 0%, #E2E8F0 100%);
}

.leaderboard-item.top-3 {
    background: linear-gradient(135deg, #FEF3C7 0%, #FCD34D 100%);
}

.lb-rank {
    font-weight: 700;
    width: 32px;
    color: #64748B;
}

.lb-rank.gold {
    color: #D97706;
}

.lb-rank.silver {
    color: #64748B;
}

.lb-rank.bronze {
    color: #B45309;
}

.lb-name {
    flex: 1;
    color: #1A1A2E;
    font-weight: 500;
}

.lb-name.you {
    color: #0066CC;
    font-weight: 600;
}

.lb-score {
    font-weight: 700;
    color: #0066CC;
    font-family: 'JetBrains Mono', monospace;
}

/* ==================== SIDEBAR ==================== */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%) !important;
    border-right: none !important;
}

.sidebar-header {
    padding: 20px;
    text-align: center;
    border-bottom: 1px solid #334155;
    margin-bottom: 16px;
}

.sidebar-user {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px;
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    border-radius: 14px;
    margin-bottom: 16px;
    border: none;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
}

.sidebar-avatar {
    width: 56px;
    height: 56px;
    background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2563EB;
    font-size: 1.6rem;
    font-weight: 800;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.sidebar-username {
    font-weight: 700;
    color: #FFFFFF;
    font-size: 1.15rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.sidebar-score-container {
    display: flex;
    gap: 10px;
    margin: 16px 0;
    padding: 0 8px;
}

.sidebar-score-item {
    flex: 1;
    background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
    border-radius: 12px;
    padding: 14px 10px;
    text-align: center;
    border: 1px solid #475569;
}

.sidebar-score-value {
    font-size: 1.4rem;
    font-weight: 800;
    color: #FCD34D;
    font-family: 'JetBrains Mono', monospace;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

.sidebar-score-label {
    font-size: 0.65rem;
    color: #94A3B8;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 4px;
}

/* ==================== NAVIGATION SECTION ==================== */
.nav-section {
    padding: 8px 12px;
}

.nav-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 12px;
    padding-left: 6px;
}

/* Navigation button styling */
.nav-button {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 12px !important;
    padding: 14px 16px !important;
    margin-bottom: 6px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    transition: all 0.25s ease !important;
    border: none !important;
    text-align: left !important;
}

.nav-button:hover {
    transform: translateX(6px) !important;
}

/* Active nav button - Bright Blue */
.nav-button.active {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
}

/* Inactive nav button - Dark */
.nav-button:not(.active) {
    background: transparent !important;
    color: #CBD5E1 !important;
    border: 1px solid #334155 !important;
}

.nav-button:not(.active):hover {
    background: linear-gradient(135deg, #334155 0%, #475569 100%) !important;
    color: #FFFFFF !important;
    border-color: #475569 !important;
}

/* ==================== DANGER ZONE ==================== */
.danger-zone {
    background: linear-gradient(135deg, #450A0A 0%, #7F1D1D 100%);
    border-radius: 12px;
    padding: 16px;
    border: 1px solid #DC2626;
}

.danger-title {
    font-weight: 700;
    color: #FCA5A5;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.danger-text {
    color: #FECACA;
    font-size: 0.85rem;
    margin-bottom: 12px;
}

/* ==================== SIDEBAR FOOTER ==================== */
.sidebar-footer {
    padding: 16px;
    border-top: 1px solid #334155;
    margin-top: auto;
}

/* ==================== CALCULATION BREAKDOWN ==================== */
.calc-breakdown {
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
    border-radius: 16px;
    padding: 20px;
    margin: 16px 0;
    border: 1px solid #E5E9F0;
}

.calc-title {
    color: #1A1A2E;
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.calc-step {
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9rem;
    padding: 8px 0;
    border-bottom: 1px solid #E2E8F0;
}

.calc-step:last-of-type {
    border-bottom: none;
}

.calc-result {
    color: #22C55E;
    font-size: 1.1rem;
    font-weight: 700;
    margin-top: 12px;
    padding-top: 12px;
    border-top: 2px solid #22C55E;
}

/* ==================== SUCCESS/ERROR MESSAGES ==================== */
.success-message {
    background: linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%);
    padding: 20px 24px;
    border-radius: 16px;
    text-align: center;
    font-size: 1.25rem;
    font-weight: 600;
    color: #166534;
    border: 2px solid #22C55E;
}

.error-message {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%);
    padding: 20px 24px;
    border-radius: 16px;
    text-align: center;
    font-size: 1.25rem;
    font-weight: 600;
    color: #991B1B;
    border: 2px solid #EF4444;
}

/* ==================== DIFFICULTY SELECTOR ==================== */
.difficulty-container {
    display: flex;
    gap: 8px;
    justify-content: center;
    margin: 12px 0;
}

.difficulty-btn {
    padding: 10px 20px !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    border: 2px solid !important;
    cursor: pointer;
    transition: all 0.2s ease !important;
    opacity: 0.6;
}

.difficulty-btn.selected {
    opacity: 1;
}

.difficulty-btn.easy {
    background: #DCFCE7 !important;
    color: #16A34A !important;
    border-color: #22C55E !important;
}

.difficulty-btn.easy.selected {
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2) !important;
}

.difficulty-btn.medium {
    background: #FEF3C7 !important;
    color: #D97706 !important;
    border-color: #F59E0B !important;
}

.difficulty-btn.medium.selected {
    box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2) !important;
}

.difficulty-btn.hard {
    background: #FEE2E2 !important;
    color: #DC2626 !important;
    border-color: #EF4444 !important;
}

.difficulty-btn.hard.selected {
    box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2) !important;
}

/* ==================== SHARE BUTTONS ==================== */
.share-container {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin: 16px 0;
    flex-wrap: wrap;
}

.share-btn {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border-radius: 10px;
    color: white;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.875rem;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.share-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.share-x {
    background: #000000;
}

.share-fb {
    background: #1877F2;
}

.share-whatsapp {
    background: #25D366;
}

/* ==================== TIMES UP POPUP ==================== */
.times-up-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 9998;
    display: flex;
    justify-content: center;
    align-items: center;
    backdrop-filter: blur(4px);
}

.times-up-popup {
    background: #FFFFFF;
    border-radius: 24px;
    padding: 40px;
    border: 3px solid #EF4444;
    box-shadow: 0 20px 60px rgba(239, 68, 68, 0.3);
    text-align: center;
    max-width: 90%;
    max-width: 400px;
}

.times-up-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #EF4444;
    margin-bottom: 16px;
}

.times-up-message {
    color: #475569;
    font-size: 1.1rem;
    margin: 12px 0;
}

.times-up-buttons {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 24px;
    flex-wrap: wrap;
}

.times-up-btn {
    padding: 14px 28px !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border: none !important;
    cursor: pointer;
}

/* ==================== AUTH PAGES ==================== */
.auth-container {
    max-width: 420px;
    margin: 40px auto;
    padding: 32px;
    background: #FFFFFF;
    border-radius: 24px;
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
    border: 1px solid #E5E9F0;
}

.auth-tabs {
    display: flex;
    gap: 8px;
    margin-bottom: 24px;
    background: #F1F5F9;
    padding: 4px;
    border-radius: 12px;
}

.auth-tab {
    flex: 1;
    padding: 12px;
    border-radius: 10px;
    text-align: center;
    font-weight: 600;
    color: #64748B;
    cursor: pointer;
    transition: all 0.2s ease;
}

.auth-tab.active {
    background: #FFFFFF;
    color: #0066CC;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.auth-input {
    margin-bottom: 16px;
}

.auth-submit {
    margin-top: 8px;
}

.auth-footer {
    text-align: center;
    margin-top: 24px;
    padding-top: 24px;
    border-top: 1px solid #E5E9F0;
}

.auth-footer a {
    color: #0066CC;
    text-decoration: none;
    font-weight: 500;
}

.auth-footer a:hover {
    text-decoration: underline;
}

/* ==================== PROGRESS PAGE ==================== */
.progress-stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
}

.progress-chart {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #E5E9F0;
    margin-bottom: 16px;
}

.progress-chart-title {
    font-size: 1rem;
    font-weight: 600;
    color: #1A1A2E;
    margin-bottom: 16px;
}

.progress-table {
    background: #FFFFFF;
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid #E5E9F0;
}

.progress-table table {
    width: 100%;
    border-collapse: collapse;
}

.progress-table th {
    background: #F8FAFC;
    padding: 14px 16px;
    text-align: left;
    font-weight: 600;
    color: #475569;
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.progress-table td {
    padding: 14px 16px;
    color: #1A1A2E;
    border-bottom: 1px solid #F1F5F9;
}

.progress-table tr:last-child td {
    border-bottom: none;
}

.progress-table .status-correct {
    color: #22C55E;
    font-weight: 600;
}

.progress-table .status-incorrect {
    color: #EF4444;
    font-weight: 600;
}

.progress-table .status-timeout {
    color: #F59E0B;
    font-weight: 600;
}

/* ==================== SETTINGS PAGE ==================== */
.settings-section {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #E5E9F0;
    margin-bottom: 16px;
}

.settings-section-title {
    font-size: 1rem;
    font-weight: 600;
    color: #1A1A2E;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 1px solid #E5E9F0;
}

.settings-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
}

.settings-label {
    color: #475569;
    font-weight: 500;
}

.settings-toggle {
    position: relative;
    width: 52px;
    height: 28px;
}

.settings-toggle input {
    opacity: 0;
    width: 0;
    height: 0;
}

.settings-toggle-slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: #E2E8F0;
    border-radius: 28px;
    transition: 0.3s;
}

.settings-toggle-slider:before {
    position: absolute;
    content: "";
    height: 22px;
    width: 22px;
    left: 3px;
    bottom: 3px;
    background: white;
    border-radius: 50%;
    transition: 0.3s;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.settings-toggle input:checked + .settings-toggle-slider {
    background: #22C55E;
}

.settings-toggle input:checked + .settings-toggle-slider:before {
    transform: translateX(24px);
}

.settings-actions {
    display: flex;
    gap: 12px;
    margin-top: 16px;
}

/* ==================== TABS ==================== */
.stTabs [data-testid="stTabList"] {
    gap: 8px;
    background: #F1F5F9;
    padding: 4px;
    border-radius: 12px;
    width: fit-content;
}

.stTabs [data-testid="stTab"] {
    padding: 10px 20px;
    border-radius: 10px;
    font-weight: 500;
    color: #64748B;
    background: transparent;
    transition: all 0.2s ease;
}

.stTabs [data-testid="stTab"]:hover {
    color: #1A1A2E;
}

.stTabs [data-testid="stTab"][aria-selected="true"] {
    background: #FFFFFF;
    color: #0066CC;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* ==================== RADIO BUTTONS ==================== */
.stRadio [role="radiogroup"] {
    gap: 8px;
}

.stRadio [role="radio"] {
    padding: 10px 16px;
    border-radius: 10px;
    background: #F8FAFC;
    transition: all 0.2s ease;
}

.stRadio [role="radio"]:hover {
    background: #F1F5F9;
}

.stRadio [role="radio"][aria-checked="true"] {
    background: #E0F2FE;
    color: #0066CC;
}

/* ==================== ANIMATIONS ==================== */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-5px); }
    75% { transform: translateX(5px); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

.fade-in {
    animation: fadeIn 0.3s ease-out;
}

.fade-in-up {
    animation: fadeInUp 0.5s ease-out;
}

.slide-in {
    animation: slideIn 0.3s ease-out;
}

.slide-in-left {
    animation: slideInLeft 0.4s ease-out;
}

.slide-in-right {
    animation: slideInRight 0.4s ease-out;
}

.bounce {
    animation: bounce 1s infinite;
}

/* ==================== LEGAL PAGES ==================== */
.legal-page-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 40px;
    margin: 24px auto;
    max-width: 800px;
    border: 1px solid #E5E9F0;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
    animation: fadeInUp 0.5s ease-out;
}

.legal-page-header {
    text-align: center;
    margin-bottom: 32px;
    padding-bottom: 24px;
    border-bottom: 2px solid #E5E9F0;
}

.legal-page-title {
    font-size: 2rem !important;
    font-weight: 800 !important;
    color: #1A1A2E !important;
    margin-bottom: 8px !important;
}

.legal-last-updated {
    color: #64748B;
    font-size: 0.875rem;
    font-weight: 500;
}

.legal-section {
    margin-bottom: 28px;
    animation: fadeInUp 0.5s ease-out;
    animation-fill-mode: both;
}

.legal-section:nth-child(2) { animation-delay: 0.1s; }
.legal-section:nth-child(3) { animation-delay: 0.2s; }
.legal-section:nth-child(4) { animation-delay: 0.3s; }
.legal-section:nth-child(5) { animation-delay: 0.4s; }
.legal-section:nth-child(6) { animation-delay: 0.5s; }
.legal-section:nth-child(7) { animation-delay: 0.6s; }
.legal-section:nth-child(8) { animation-delay: 0.7s; }

.legal-section-title {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #1A1A2E !important;
    margin-bottom: 12px !important;
    padding-bottom: 8px;
    border-bottom: 1px solid #E5E9F0;
}

.legal-content {
    color: #475569;
    font-size: 1rem;
    line-height: 1.7;
}

.legal-content strong {
    color: #1A1A2E;
    font-weight: 600;
}

.legal-content ul {
    margin: 12px 0;
    padding-left: 20px;
}

.legal-content li {
    margin: 8px 0;
    line-height: 1.6;
}

.legal-back-btn {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    margin-top: 24px !important;
    padding: 14px 32px !important;
    background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
}

.legal-back-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 16px rgba(0, 102, 204, 0.3) !important;
}

.legal-footer {
    margin-top: 32px;
    padding-top: 24px;
    border-top: 2px solid #E5E9F0;
    text-align: center;
}

.legal-footer-text {
    color: #64748B;
    font-size: 0.875rem;
    line-height: 1.6;
}

/* ==================== ENHANCED CARD STYLES ==================== */
.card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    border: 1px solid #E5E9F0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
}

.card-gradient {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
}

.card-gradient:hover {
    background: linear-gradient(135deg, #F8FAFC 0%, #F1F5F9 100%);
}

.card-accent {
    border-left: 4px solid #0066CC;
}

.card-success {
    border-left: 4px solid #22C55E;
}

.card-warning {
    border-left: 4px solid #F59E0B;
}

.card-danger {
    border-left: 4px solid #EF4444;
}

/* ==================== ENHANCED TYPOGRAPHY ==================== */
.text-gradient {
    background: linear-gradient(135deg, #0066CC 0%, #7C3AED 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.text-muted {
    color: #64748B !important;
}

.text-success {
    color: #22C55E !important;
}

.text-warning {
    color: #F59E0B !important;
}

.text-danger {
    color: #EF4444 !important;
}

.text-mono {
    font-family: 'JetBrains Mono', monospace !important;
}

.text-sm {
    font-size: 0.875rem !important;
}

.text-lg {
    font-size: 1.125rem !important;
}

.text-xl {
    font-size: 1.25rem !important;
}

.font-light {
    font-weight: 300 !important;
}

.font-medium {
    font-weight: 500 !important;
}

.font-bold {
    font-weight: 700 !important;
}

.font-black {
    font-weight: 900 !important;
}

/* ==================== ENHANCED PROGRESS PAGE ==================== */
.progress-stat-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    border: 1px solid #E5E9F0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.progress-stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
}

.progress-stat-card .stat-icon {
    font-size: 2.5rem;
    margin-bottom: 12px;
    display: block;
}

.progress-stat-card .stat-value {
    font-size: 2.25rem;
    font-weight: 800;
    color: #1A1A2E;
    font-family: 'JetBrains Mono', monospace;
    display: block;
    margin-bottom: 4px;
}

.progress-stat-card .stat-label {
    font-size: 0.875rem;
    color: #64748B;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.progress-stat-card.accent-blue .stat-value { color: #0066CC; }
.progress-stat-card.accent-green .stat-value { color: #22C55E; }
.progress-stat-card.accent-purple .stat-value { color: #7C3AED; }
.progress-stat-card.accent-orange .stat-value { color: #F59E0B; }

.progress-chart-enhanced {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid #E5E9F0;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.progress-chart-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #E5E9F0;
}

.progress-chart-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1A1A2E;
}

.progress-chart-badge {
    background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.progress-activity-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.progress-activity-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1A1A2E;
}

/* ==================== ENHANCED SETTINGS PAGE ==================== */
.settings-section {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border-radius: 20px;
    padding: 28px;
    border: 1px solid #E5E9F0;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    transition: all 0.3s ease;
}

.settings-section:hover {
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.settings-section-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: #1A1A2E;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid #E5E9F0;
    display: flex;
    align-items: center;
    gap: 10px;
}

.settings-section-title .icon {
    font-size: 1.25rem;
}

.settings-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;
    border-bottom: 1px solid #F1F5F9;
}

.settings-row:last-child {
    border-bottom: none;
}

.settings-label {
    color: #475569;
    font-weight: 600;
    font-size: 1rem;
}

.settings-description {
    color: #64748B;
    font-size: 0.875rem;
    margin-top: 4px;
}

.settings-toggle-enhanced {
    position: relative;
    width: 56px;
    height: 30px;
}

.settings-toggle-enhanced input {
    opacity: 0;
    width: 0;
    height: 0;
}

.settings-toggle-slider-enhanced {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: #E2E8F0;
    border-radius: 30px;
    transition: all 0.3s ease;
}

.settings-toggle-slider-enhanced:before {
    position: absolute;
    content: "";
    height: 24px;
    width: 24px;
    left: 3px;
    bottom: 3px;
    background: white;
    border-radius: 50%;
    transition: all 0.3s ease;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

.settings-toggle-enhanced input:checked + .settings-toggle-slider-enhanced {
    background: linear-gradient(135deg, #22C55E 0%, #16A34A 100%);
}

.settings-toggle-enhanced input:checked + .settings-toggle-slider-enhanced:before {
    transform: translateX(26px);
}

.settings-toggle-enhanced:hover .settings-toggle-slider-enhanced {
    box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.2);
}

.settings-actions-enhanced {
    display: flex;
    gap: 16px;
    margin-top: 24px;
    flex-wrap: wrap;
}

.settings-btn {
    flex: 1;
    min-width: 200px;
    padding: 16px 24px !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
}

.settings-btn-save {
    background: linear-gradient(135deg, #0066CC 0%, #0052A3 100%) !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2) !important;
}

.settings-btn-save:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0, 102, 204, 0.3) !important;
}

.settings-btn-reset {
    background: linear-gradient(135deg, #FEE2E2 0%, #FECACA 100%) !important;
    color: #DC2626 !important;
    border: 2px solid #EF4444 !important;
}

.settings-btn-reset:hover {
    background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%) !important;
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2) !important;
}

.settings-account-card {
    background: linear-gradient(135deg, #F0F7FF 0%, #E8F4FD 100%);
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #BFDBFE;
}

.settings-account-header {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 20px;
}

.settings-account-avatar {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #0066CC 0%, #7C3AED 100%);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.5rem;
    font-weight: 800;
    box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3);
}

.settings-account-name {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1A1A2E;
}

.settings-account-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: 16px;
}

/* ==================== RESPONSIVE ==================== */
@media (max-width: 768px) {
    .stApp { padding: 8px; }
    .main-title { font-size: 2rem !important; }
    .page-title { font-size: 1.5rem !important; }
    
    .task-display { padding: 20px !important; border-radius: 16px !important; }
    .exercise-icon { font-size: 2.5rem !important; }
    .task-question { font-size: 1.2rem !important; }
    
    .stButton > button { 
        padding: 12px 20px !important; 
        font-size: 0.9rem !important; 
    }
    
    .card { padding: 16px !important; border-radius: 12px !important; }
    .stat-card { padding: 16px !important; }
    .stat-card .stat-value { font-size: 1.5rem !important; }
    
    .progress-stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .times-up-popup { padding: 24px; }
    .times-up-title { font-size: 1.75rem; }
    
    .difficulty-container { flex-wrap: wrap; }
    .share-container { flex-wrap: wrap; }
}

@media (max-width: 480px) {
    .main-title { font-size: 1.75rem !important; }
    .task-display { padding: 16px !important; }
    .exercise-icon { font-size: 2rem !important; }
    .task-question { font-size: 1rem !important; }
    
    .sidebar-score-container {
        flex-direction: column;
    }
    
    .auth-container {
        margin: 16px;
        padding: 20px;
    }
}

/* ==================== STREAMLIT OVERRIDES ==================== */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #E5E9F0;
}

div[data-testid="stMetricLabel"] {
    color: #64748B !important;
    font-size: 0.875rem !important;
}

div[data-testid="stMetricValue"] {
    color: #1A1A2E !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

.stDataFrame {
    border: 1px solid #E5E9F0 !important;
    border-radius: 12px !important;
    overflow: hidden;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: #E5E9F0;
    margin: 16px 0;
}

/* Info/Warning/Success messages */
.stSuccess {
    background: #DCFCE7 !important;
    color: #166534 !important;
    border: 1px solid #22C55E !important;
    border-radius: 12px !important;
}

.stError {
    background: #FEE2E2 !important;
    color: #991B1B !important;
    border: 1px solid #EF4444 !important;
    border-radius: 12px !important;
}

.stWarning {
    background: #FEF3C7 !important;
    color: #92400E !important;
    border: 1px solid #F59E0B !important;
    border-radius: 12px !important;
}

.stInfo {
    background: #E0F2FE !important;
    color: #075985 !important;
    border: 1px solid #0EA5E9 !important;
    border-radius: 12px !important;
}

/* ==================== DARK MODE SUPPORT ==================== */
@media (prefers-color-scheme: dark) {
    .stApp {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
    }
    
    .card,
    .task-display,
    .stat-card,
    .leaderboard-card,
    .formula-box,
    .calc-breakdown,
    .settings-section,
    .progress-chart,
    .progress-table,
    .auth-container {
        background: #1E293B;
        border-color: #334155;
    }
    
    .card-title,
    .page-title,
    .section-title,
    .task-question,
    .formula-text,
    .lb-name,
    .sidebar-username,
    .calc-title,
    .settings-section-title,
    .progress-chart-title {
        color: #F1F5F9;
    }
    
    .stat-card .stat-value,
    .lb-score,
    .sidebar-score-value {
        color: #38BDF8;
    }
    
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        background: #1E293B !important;
        border-color: #334155 !important;
        color: #F1F5F9 !important;
    }
    
    .main-title {
        background: linear-gradient(135deg, #38BDF8 0%, #818CF8 100%);
        -webkit-background-clip: text;
    }
}

/* ==================== SCROLLBAR ==================== */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #F1F5F9;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}
</style>
"""


def get_custom_css() -> str:
    """Get the custom CSS string"""
    return CSS_CONTENT


def custom_css() -> None:
    """Apply custom CSS to Streamlit"""
    import streamlit as st
    st.markdown(CSS_CONTENT, unsafe_allow_html=True)

