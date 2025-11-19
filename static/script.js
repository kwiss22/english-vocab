/**
 * 탭 전환 함수
 * @param {string} tabName - 표시할 탭 이름 ('words', 'add', 'quiz', 'stats')
 * @param {HTMLElement} buttonElement - 클릭된 탭 버튼 요소
 */
function showTab(tabName, buttonElement) {
    // 모든 탭 숨기기
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 모든 탭 버튼 비활성화
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 선택된 탭 보이기
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // 선택된 탭 버튼 활성화
    if (buttonElement) {
        buttonElement.classList.add('active');
    }
    
    // 탭별 데이터 로드
    if (tabName === 'words') {
        loadWords();
        loadCategories();
    } else if (tabName === 'stats') {
        loadStats();
    } else if (tabName === 'quiz') {
        loadCategories();
    } else if (tabName === 'add') {
        loadCategories();
    }
}

/**
 * 단어 목록을 서버에서 불러와 화면에 표시
 * @returns {Promise<void>}
 */
async function loadWords() {
    const wordsList = document.getElementById('words-list');
    wordsList.innerHTML = '<p class="loading">로딩 중...</p>';
    
    try {
        const response = await fetch('/api/words');
        const words = await response.json();
        
        if (words.length === 0) {
            wordsList.innerHTML = '<p class="empty-message">저장된 단어가 없습니다. 단어를 추가해보세요!</p>';
            return;
        }
        
        displayWords(words);
    } catch (error) {
        wordsList.innerHTML = '<p class="error-message">단어를 불러오는 중 오류가 발생했습니다.</p>';
        console.error('Error:', error);
    }
}

/**
 * 단어 목록을 화면에 표시하는 함수
 * @param {Array<{english: string, korean: string}>} words - 표시할 단어 배열
 */
function displayWords(words) {
    const wordsList = document.getElementById('words-list');
    
    if (words.length === 0) {
        wordsList.innerHTML = '<p class="empty-message">검색 결과가 없습니다.</p>';
        return;
    }
    
    wordsList.innerHTML = words.map(word => `
        <div class="word-item">
            <div class="word-content">
                <div class="word-english">${escapeHtml(word.english)}</div>
                <div class="word-korean">${escapeHtml(word.korean)}</div>
                ${word.category ? `<div class="word-category">🏷️ ${escapeHtml(word.category)}</div>` : ''}
            </div>
            <div class="word-actions">
                <button class="btn-edit" onclick="editWord('${escapeHtml(word.english)}', '${escapeHtml(word.korean)}', '${escapeHtml(word.category || '')}')">수정</button>
                <button class="btn-delete" onclick="deleteWord('${escapeHtml(word.english)}')">삭제</button>
            </div>
        </div>
    `).join('');
    
    // 단어 개수 업데이트
    document.getElementById('word-count').textContent = words.length;
}

/**
 * 단어 검색 함수 (실시간 검색)
 * 검색어가 없으면 전체 목록을 표시
 * @returns {Promise<void>}
 */
async function searchWords() {
    const searchInput = document.getElementById('search-input');
    const searchTerm = searchInput.value.trim().toLowerCase();
    const categoryFilter = document.getElementById('category-filter');
    const category = categoryFilter ? categoryFilter.value : '';
    const wordsList = document.getElementById('words-list');
    
    wordsList.innerHTML = '<p class="loading">검색 중...</p>';
    
    try {
        // 카테고리 필터 적용
        let url = '/api/words';
        if (category) {
            url += `?category=${encodeURIComponent(category)}`;
        }
        
        const response = await fetch(url);
        let words = await response.json();
        
        // 검색어로 필터링 (영어 또는 한글에 포함되는지 확인)
        if (searchTerm) {
            words = words.filter(word => 
                word.english.toLowerCase().includes(searchTerm) || 
                word.korean.includes(searchTerm)
            );
        }
        
        displayWords(words);
    } catch (error) {
        wordsList.innerHTML = '<p class="error-message">검색 중 오류가 발생했습니다.</p>';
        console.error('Error:', error);
    }
}

// 단어 추가
document.getElementById('add-word-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const english = document.getElementById('english-input').value.trim().toLowerCase();
    const korean = document.getElementById('korean-input').value.trim();
    const category = document.getElementById('category-input').value.trim();
    const messageDiv = document.getElementById('add-message');
    
    if (!english || !korean) {
        messageDiv.innerHTML = '<p class="message error">단어와 뜻을 모두 입력해주세요.</p>';
        return;
    }
    
    try {
        const response = await fetch('/api/words', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ english, korean, category })
        });
        
        const result = await response.json();
        
        if (result.success) {
            messageDiv.innerHTML = `<p class="message success">${result.message}</p>`;
            document.getElementById('add-word-form').reset();
            
            // 카테고리 목록 새로고침
            loadCategories();
            
            // 단어 목록 탭이 활성화되어 있으면 새로고침
            if (document.getElementById('words-tab').classList.contains('active')) {
                loadWords();
            }
            
            // 검색창 초기화
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                searchInput.value = '';
            }
        } else {
            messageDiv.innerHTML = `<p class="message error">${result.message}</p>`;
        }
    } catch (error) {
        messageDiv.innerHTML = '<p class="message error">단어 추가 중 오류가 발생했습니다.</p>';
        console.error('Error:', error);
    }
});

// 단어 수정
function editWord(english, korean, category = '') {
    const newEnglish = prompt('영어 단어를 수정하세요:', english);
    if (newEnglish === null) return; // 취소 버튼 클릭
    
    const newKorean = prompt('한국어 뜻을 수정하세요:', korean);
    if (newKorean === null) return; // 취소 버튼 클릭
    
    const newCategory = prompt('카테고리를 수정하세요 (선택사항):', category || '');
    if (newCategory === null) return; // 취소 버튼 클릭
    
    if (!newEnglish.trim() || !newKorean.trim()) {
        alert('단어와 뜻을 모두 입력해주세요.');
        return;
    }
    
    updateWord(english, newEnglish.trim().toLowerCase(), newKorean.trim(), newCategory.trim());
}

// 단어 업데이트 API 호출
async function updateWord(oldEnglish, newEnglish, newKorean, newCategory = '') {
    try {
        const response = await fetch(`/api/words/${encodeURIComponent(oldEnglish)}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                english: newEnglish,
                korean: newKorean,
                category: newCategory
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            loadCategories(); // 카테고리 목록 새로고침
            loadWords(); // 단어 목록 새로고침
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert('단어 수정 중 오류가 발생했습니다.');
        console.error('Error:', error);
    }
}

// 단어 삭제
async function deleteWord(word) {
    if (!confirm(`'${word}' 단어를 삭제하시겠습니까?`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/words/${encodeURIComponent(word)}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            alert(result.message);
            loadCategories(); // 카테고리 목록 새로고침
            loadWords(); // 단어 목록 새로고침
        } else {
            alert(result.message);
        }
    } catch (error) {
        alert('단어 삭제 중 오류가 발생했습니다.');
        console.error('Error:', error);
    }
}

// 퀴즈 시작
let currentQuiz = null;

async function startQuiz() {
    const quizType = document.getElementById('quiz-type').value;
    const quizMode = document.getElementById('quiz-mode').value;
    const quizCategory = document.getElementById('quiz-category').value;
    const focusMode = document.getElementById('focus-mode').checked;
    const quizArea = document.getElementById('quiz-area');
    const quizResult = document.getElementById('quiz-result');
    
    quizResult.innerHTML = '';
    quizArea.innerHTML = '<p class="loading">문제를 불러오는 중...</p>';
    
    try {
        const response = await fetch('/api/quiz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                type: quizType, 
                mode: quizMode, 
                category: quizCategory,
                focus_mode: focusMode 
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            currentQuiz = result;
            
            let questionHtml = '';
            
            // 객관식 문제
            if (result.mode === 'multiple') {
                questionHtml = `
                    <div class="quiz-question">${result.question}</div>
                    <div class="quiz-word">${escapeHtml(result.word)}</div>
                    <div class="quiz-choices" id="quiz-choices">
                        ${result.choices.map((choice, index) => `
                            <button class="quiz-choice-btn" onclick="selectChoice(${index})" data-index="${index}">
                                ${index + 1}. ${escapeHtml(choice)}
                            </button>
                        `).join('')}
                    </div>
                `;
            } else {
                // 주관식 문제
                if (quizType === 'english_to_korean') {
                    questionHtml = `
                        <div class="quiz-question">${result.question}</div>
                        <div class="quiz-word">${escapeHtml(result.word)}</div>
                        <input type="text" id="quiz-answer" class="quiz-input" placeholder="한국어 뜻을 입력하세요" autofocus>
                    `;
                } else {
                    questionHtml = `
                        <div class="quiz-question">${result.question}</div>
                        <div class="quiz-word">${escapeHtml(result.correct_answer)}</div>
                        <input type="text" id="quiz-answer" class="quiz-input" placeholder="영어 단어를 입력하세요" autofocus>
                    `;
                }
            }
            
            quizArea.innerHTML = questionHtml + `
                <div class="quiz-buttons">
                    ${result.mode === 'multiple' ? '' : '<button class="btn-primary" onclick="checkAnswer()">정답 확인</button>'}
                    <button class="btn-refresh" onclick="startQuiz()">다음 문제</button>
                </div>
            `;
            
            // 주관식인 경우에만 Enter 키 이벤트 추가
            if (result.mode === 'text') {
                const answerInput = document.getElementById('quiz-answer');
                if (answerInput) {
                    answerInput.addEventListener('keypress', (e) => {
                        if (e.key === 'Enter') {
                            checkAnswer();
                        }
                    });
                }
            }
        } else {
            quizArea.innerHTML = `<p class="error-message">${result.message}</p>`;
        }
    } catch (error) {
        quizArea.innerHTML = '<p class="error-message">문제를 불러오는 중 오류가 발생했습니다.</p>';
        console.error('Error:', error);
    }
}

// 객관식 선택지 선택
function selectChoice(index) {
    // 모든 선택지 버튼에서 선택 상태 제거
    document.querySelectorAll('.quiz-choice-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    
    // 선택한 버튼에 선택 상태 추가
    const selectedBtn = document.querySelector(`[data-index="${index}"]`);
    if (selectedBtn) {
        selectedBtn.classList.add('selected');
    }
    
    // 정답 확인
    checkAnswer(index);
}

// 정답 확인
async function checkAnswer(selectedIndex = null) {
    if (!currentQuiz) {
        return;
    }
    
    const quizResult = document.getElementById('quiz-result');
    let userAnswer;
    
    // 객관식인 경우
    if (currentQuiz.mode === 'multiple') {
        if (selectedIndex === null) {
            return; // 선택지가 선택되지 않음
        }
        userAnswer = selectedIndex;
    } else {
        // 주관식인 경우
        const answerInput = document.getElementById('quiz-answer');
        if (!answerInput) {
            return;
        }
        userAnswer = answerInput.value.trim();
        
        if (!userAnswer) {
            alert('답을 입력해주세요.');
            return;
        }
    }
    
    try {
        const requestBody = {
            word: currentQuiz.word,
            answer: userAnswer,
            type: currentQuiz.type,
            mode: currentQuiz.mode
        };
        
        // 객관식인 경우 정답 인덱스 추가
        if (currentQuiz.mode === 'multiple') {
            requestBody.correct_index = currentQuiz.correct_index;
        }
        
        const response = await fetch('/api/quiz/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // 객관식인 경우 선택지 버튼 스타일 업데이트
            if (currentQuiz.mode === 'multiple') {
                document.querySelectorAll('.quiz-choice-btn').forEach((btn, index) => {
                    btn.disabled = true;
                    if (index === currentQuiz.correct_index) {
                        btn.classList.add('correct-choice');
                    } else if (index === selectedIndex && !result.is_correct) {
                        btn.classList.add('wrong-choice');
                    }
                });
            }
            
            if (result.is_correct) {
                quizResult.innerHTML = `
                    <div class="quiz-result correct">
                        ✓ 정답입니다! (정답: ${escapeHtml(result.correct_answer)})<br>
                        <small>맞춘 횟수: ${result.stats[0]}회 | 틀린 횟수: ${result.stats[1]}회</small>
                    </div>
                `;
            } else {
                quizResult.innerHTML = `
                    <div class="quiz-result wrong">
                        ✗ 틀렸습니다. 정답은 "${escapeHtml(result.correct_answer)}" 입니다.<br>
                        <small>맞춘 횟수: ${result.stats[0]}회 | 틀린 횟수: ${result.stats[1]}회</small>
                    </div>
                `;
            }
            
            // 통계 업데이트
            if (document.getElementById('stats-tab').classList.contains('active')) {
                loadStats();
            }
        }
    } catch (error) {
        quizResult.innerHTML = '<div class="quiz-result error">정답 확인 중 오류가 발생했습니다.</div>';
        console.error('Error:', error);
    }
}

// 차트 인스턴스 저장
let accuracyChart = null;
let summaryChart = null;

// 통계 로드
async function loadStats() {
    const statsList = document.getElementById('stats-list');
    statsList.innerHTML = '<p class="loading">로딩 중...</p>';
    
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        
        if (stats.length === 0) {
            statsList.innerHTML = '<p class="empty-message">퀴즈 통계가 없습니다. 먼저 퀴즈를 해보세요!</p>';
            // 차트도 숨기기
            document.querySelector('.charts-container').style.display = 'none';
            return;
        }
        
        // 차트 영역 표시
        document.querySelector('.charts-container').style.display = 'grid';
        
        // 차트 생성
        createCharts(stats);
        
        // 통계 목록 표시
        statsList.innerHTML = stats.map(stat => `
            <div class="stat-item">
                <div class="stat-word">
                    <div class="stat-word-english">${escapeHtml(stat.word)}</div>
                    <div class="stat-word-korean">${escapeHtml(stat.korean)}</div>
                </div>
                <div class="stat-numbers">
                    <div class="stat-accuracy">${stat.accuracy}%</div>
                    <div class="stat-details">${stat.correct}정 / ${stat.wrong}오 (총 ${stat.total}회)</div>
                </div>
            </div>
        `).join('');
    } catch (error) {
        statsList.innerHTML = '<p class="error-message">통계를 불러오는 중 오류가 발생했습니다.</p>';
        console.error('Error:', error);
    }
}

// 차트 생성 함수
function createCharts(stats) {
    const isDark = document.body.classList.contains('dark');
    const textColor = isDark ? '#e0e0e0' : '#333';
    const gridColor = isDark ? '#3a3a4e' : '#e0e0e0';
    
    // 정답률 상위 10개 단어 차트
    const topStats = [...stats].sort((a, b) => b.accuracy - a.accuracy).slice(0, 10);
    const accuracyCtx = document.getElementById('accuracy-chart').getContext('2d');
    
    // 기존 차트가 있으면 파괴
    if (accuracyChart) {
        accuracyChart.destroy();
    }
    
    accuracyChart = new Chart(accuracyCtx, {
        type: 'bar',
        data: {
            labels: topStats.map(s => s.word.length > 10 ? s.word.substring(0, 10) + '...' : s.word),
            datasets: [{
                label: '정답률 (%)',
                data: topStats.map(s => s.accuracy),
                backgroundColor: isDark ? 'rgba(139, 154, 255, 0.6)' : 'rgba(102, 126, 234, 0.6)',
                borderColor: isDark ? '#8b9aff' : '#667eea',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const stat = topStats[context.dataIndex];
                            return `정답률: ${stat.accuracy}% (${stat.correct}정 / ${stat.wrong}오)`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        color: textColor
                    },
                    grid: {
                        color: gridColor
                    }
                },
                x: {
                    ticks: {
                        color: textColor
                    },
                    grid: {
                        color: gridColor
                    }
                }
            }
        }
    });
    
    // 전체 통계 요약 차트 (파이 차트)
    const totalCorrect = stats.reduce((sum, s) => sum + s.correct, 0);
    const totalWrong = stats.reduce((sum, s) => sum + s.wrong, 0);
    const summaryCtx = document.getElementById('summary-chart').getContext('2d');
    
    // 기존 차트가 있으면 파괴
    if (summaryChart) {
        summaryChart.destroy();
    }
    
    summaryChart = new Chart(summaryCtx, {
        type: 'doughnut',
        data: {
            labels: ['정답', '오답'],
            datasets: [{
                data: [totalCorrect, totalWrong],
                backgroundColor: [
                    isDark ? 'rgba(144, 238, 144, 0.6)' : 'rgba(40, 167, 69, 0.6)',
                    isDark ? 'rgba(255, 107, 107, 0.6)' : 'rgba(220, 53, 69, 0.6)'
                ],
                borderColor: [
                    isDark ? '#90ee90' : '#28a745',
                    isDark ? '#ff6b6b' : '#dc3545'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: textColor,
                        padding: 15,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = totalCorrect + totalWrong;
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                            return `${label}: ${value}회 (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// HTML 이스케이프 함수
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// 다크 모드 토글
function toggleDarkMode() {
    const body = document.body;
    const isDark = body.classList.toggle('dark');
    
    // localStorage에 저장
    localStorage.setItem('darkMode', isDark ? 'enabled' : 'disabled');
    
    // 아이콘 업데이트
    updateDarkModeIcon(isDark);
    
    // 차트가 있으면 다시 생성 (다크 모드 색상 적용)
    if (document.getElementById('stats-tab').classList.contains('active')) {
        loadStats();
    }
}

// 다크 모드 아이콘 업데이트
function updateDarkModeIcon(isDark) {
    const toggleBtn = document.getElementById('dark-mode-toggle');
    if (toggleBtn) {
        toggleBtn.innerHTML = isDark ? '☀️ 라이트 모드' : '🌙 다크 모드';
    }
}

// 저장된 다크 모드 설정 불러오기
function loadDarkMode() {
    const savedMode = localStorage.getItem('darkMode');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // 저장된 설정이 있으면 사용, 없으면 시스템 설정 사용
    const shouldBeDark = savedMode === 'enabled' || (!savedMode && prefersDark);
    
    if (shouldBeDark) {
        document.body.classList.add('dark');
    }
    
    updateDarkModeIcon(shouldBeDark);
}

// 카테고리 목록 로드
async function loadCategories() {
    try {
        const response = await fetch('/api/categories');
        const categories = await response.json();
        
        // 카테고리 필터 드롭다운 업데이트
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            const currentValue = categoryFilter.value;
            categoryFilter.innerHTML = '<option value="">전체</option>' + 
                categories.map(cat => `<option value="${escapeHtml(cat)}">${escapeHtml(cat)}</option>`).join('');
            categoryFilter.value = currentValue;
        }
        
        // 퀴즈 카테고리 선택 업데이트
        const quizCategory = document.getElementById('quiz-category');
        if (quizCategory) {
            const currentValue = quizCategory.value;
            quizCategory.innerHTML = '<option value="">전체 카테고리</option>' + 
                categories.map(cat => `<option value="${escapeHtml(cat)}">${escapeHtml(cat)}</option>`).join('');
            quizCategory.value = currentValue;
        }
        
        // 단어 추가 폼의 datalist 업데이트
        const categoryList = document.getElementById('category-list');
        if (categoryList) {
            categoryList.innerHTML = categories.map(cat => `<option value="${escapeHtml(cat)}">`).join('');
        }
    } catch (error) {
        console.error('카테고리 로드 오류:', error);
    }
}

// 카테고리별 필터링
async function filterByCategory() {
    const category = document.getElementById('category-filter').value;
    const searchInput = document.getElementById('search-input');
    const searchTerm = searchInput ? searchInput.value.trim().toLowerCase() : '';
    
    try {
        let url = '/api/words';
        if (category) {
            url += `?category=${encodeURIComponent(category)}`;
        }
        
        const response = await fetch(url);
        let words = await response.json();
        
        // 검색어가 있으면 추가 필터링
        if (searchTerm) {
            words = words.filter(word => 
                word.english.toLowerCase().includes(searchTerm) || 
                word.korean.includes(searchTerm)
            );
        }
        
        displayWords(words);
    } catch (error) {
        console.error('필터링 오류:', error);
    }
}

// 페이지 로드 시 단어 목록 자동 로드 및 다크 모드 설정 불러오기
window.addEventListener('DOMContentLoaded', () => {
    loadWords();
    loadDarkMode();
    loadCategories();
});

