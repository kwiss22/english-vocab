"""
영어 단어장 웹 애플리케이션 (Flask)
기존 vocab_book.py의 모든 기능을 웹 버전으로 구현

주요 기능:
- 단어 추가/수정/삭제/검색
- 영어 ↔ 한글 퀴즈
- 퀴즈 통계 및 시각화
- 다크 모드 지원
"""

from flask import Flask, render_template, request, jsonify
import json
import random
import os
import logging
from typing import Dict, List, Tuple, Optional

# Flask 앱 초기화
app = Flask(__name__)

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 상수 정의
VOCAB_FILE = "vocabulary.json"
STATS_FILE = "quiz_stats.json"
DEFAULT_PORT = 5000
FALLBACK_PORT = 5001

# 전역 변수
vocabulary: Dict[str, Dict] = {}  # {word: {"korean": meaning, "category": category}}
quiz_stats: Dict[str, List[int]] = {}  # {word: [correct_count, wrong_count]}
CATEGORIES_FILE = "categories.json"

def load_data() -> None:
    """
    파일에서 단어장 및 통계 데이터 불러오기
    
    Returns:
        None
    """
    global vocabulary, quiz_stats
    vocabulary = {}
    quiz_stats = {}
    
    # 단어장 데이터 로드
    try:
        if os.path.exists(VOCAB_FILE):
            with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 기존 형식({word: meaning})과 새 형식({word: {korean, category}}) 호환
                for word, value in data.items():
                    if isinstance(value, str):
                        # 기존 형식: {word: meaning} -> {word: {korean: meaning, category: ""}}
                        vocabulary[word] = {"korean": value, "category": ""}
                    elif isinstance(value, dict):
                        # 새 형식: {word: {korean: meaning, category: category}}
                        vocabulary[word] = {
                            "korean": value.get("korean", ""),
                            "category": value.get("category", "")
                        }
            logger.info(f"단어장 불러오기 성공: {len(vocabulary)}개 단어")
        else:
            logger.info("단어장 파일이 없습니다. 새로 생성합니다.")
    except json.JSONDecodeError as e:
        logger.error(f"단어장 JSON 파싱 오류: {e}")
        vocabulary = {}
    except Exception as e:
        logger.error(f"단어장 불러오기 실패: {e}")
        vocabulary = {}
    
    # 통계 데이터 로드
    try:
        if os.path.exists(STATS_FILE):
            with open(STATS_FILE, 'r', encoding='utf-8') as f:
                quiz_stats = json.load(f)
            logger.info(f"통계 불러오기 성공: {len(quiz_stats)}개 기록")
        else:
            logger.info("통계 파일이 없습니다. 새로 생성합니다.")
    except json.JSONDecodeError as e:
        logger.error(f"통계 JSON 파싱 오류: {e}")
        quiz_stats = {}
    except Exception as e:
        logger.error(f"통계 불러오기 실패: {e}")
        quiz_stats = {}

def save_data() -> bool:
    """
    단어장 및 통계 데이터를 파일에 저장
    
    Returns:
        bool: 저장 성공 여부
    """
    try:
        # 단어장 저장
        with open(VOCAB_FILE, 'w', encoding='utf-8') as f:
            json.dump(vocabulary, f, ensure_ascii=False, indent=2)
        
        # 통계 저장
        with open(STATS_FILE, 'w', encoding='utf-8') as f:
            json.dump(quiz_stats, f, ensure_ascii=False, indent=2)
        
        logger.debug("데이터 저장 성공")
        return True
    except IOError as e:
        logger.error(f"파일 저장 IO 오류: {e}")
        return False
    except Exception as e:
        logger.error(f"파일 저장 실패: {e}")
        return False

# 메인 페이지
@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html', 
                         word_count=len(vocabulary),
                         stats_count=len(quiz_stats))

# 단어 목록 API
@app.route('/api/words', methods=['GET'])
def get_words():
    """모든 단어 가져오기"""
    category = request.args.get('category', None)
    words_list = []
    
    for eng, data in vocabulary.items():
        word_data = {
            "english": eng,
            "korean": data.get("korean", ""),
            "category": data.get("category", "")
        }
        # 카테고리 필터링
        if category is None or category == "" or word_data["category"] == category:
            words_list.append(word_data)
    
    return jsonify(words_list)

def validate_word_input(english: str, korean: str) -> Tuple[bool, Optional[str]]:
    """
    단어 입력값 검증
    
    Args:
        english: 영어 단어
        korean: 한국어 뜻
        
    Returns:
        Tuple[bool, Optional[str]]: (검증 성공 여부, 에러 메시지)
    """
    if not english or not english.strip():
        return False, "영어 단어를 입력해주세요."
    if not korean or not korean.strip():
        return False, "한국어 뜻을 입력해주세요."
    if len(english) > 100:
        return False, "영어 단어는 100자 이하여야 합니다."
    if len(korean) > 200:
        return False, "한국어 뜻은 200자 이하여야 합니다."
    return True, None

@app.route('/api/words', methods=['POST'])
def add_word():
    """
    단어 추가 API
    
    Request Body:
        {
            "english": "단어",
            "korean": "뜻"
        }
        
    Returns:
        JSON: 성공/실패 메시지
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "요청 데이터가 없습니다."}), 400
        
        english = data.get('english', '').strip().lower()
        korean = data.get('korean', '').strip()
        category = data.get('category', '').strip()
        
        # 입력 검증
        is_valid, error_message = validate_word_input(english, korean)
        if not is_valid:
            return jsonify({"success": False, "message": error_message}), 400
        
        # 중복 확인
        if english in vocabulary:
            return jsonify({"success": False, "message": f"'{english}' 단어가 이미 존재합니다."}), 409
        
        # 단어 추가
        vocabulary[english] = {
            "korean": korean,
            "category": category
        }
        if save_data():
            logger.info(f"단어 추가 성공: {english}")
            return jsonify({"success": True, "message": f"'{english}' 단어가 추가되었습니다!"})
        else:
            return jsonify({"success": False, "message": "파일 저장에 실패했습니다."}), 500
            
    except Exception as e:
        logger.error(f"단어 추가 오류: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500

@app.route('/api/words/<word>', methods=['DELETE'])
def delete_word(word: str):
    """
    단어 삭제 API
    
    Args:
        word: 삭제할 영어 단어
        
    Returns:
        JSON: 성공/실패 메시지
    """
    try:
        word = word.lower().strip()
        
        if not word:
            return jsonify({"success": False, "message": "단어를 입력해주세요."}), 400
        
        if word not in vocabulary:
            return jsonify({"success": False, "message": "단어를 찾을 수 없습니다."}), 404
        
        # 단어 삭제
        del vocabulary[word]
        
        # 통계도 함께 삭제
        if word in quiz_stats:
            del quiz_stats[word]
        
        if save_data():
            logger.info(f"단어 삭제 성공: {word}")
            return jsonify({"success": True, "message": f"'{word}' 단어가 삭제되었습니다!"})
        else:
            return jsonify({"success": False, "message": "파일 저장에 실패했습니다."}), 500
            
    except Exception as e:
        logger.error(f"단어 삭제 오류: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500

@app.route('/api/words/<word>', methods=['PUT'])
def update_word(word: str):
    """
    단어 수정 API
    
    Args:
        word: 수정할 영어 단어
        
    Request Body:
        {
            "english": "새 단어",
            "korean": "새 뜻"
        }
        
    Returns:
        JSON: 성공/실패 메시지
    """
    try:
        word = word.lower().strip()
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "message": "요청 데이터가 없습니다."}), 400
        
        new_english = data.get('english', '').strip().lower()
        new_korean = data.get('korean', '').strip()
        new_category = data.get('category', '').strip()
        
        # 입력 검증
        is_valid, error_message = validate_word_input(new_english, new_korean)
        if not is_valid:
            return jsonify({"success": False, "message": error_message}), 400
        
        if word not in vocabulary:
            return jsonify({"success": False, "message": "단어를 찾을 수 없습니다."}), 404
        
        # 기존 카테고리 유지 (카테고리가 제공되지 않은 경우)
        if not new_category:
            new_category = vocabulary[word].get("category", "")
        
        # 단어가 변경된 경우
        if new_english != word:
            # 새 단어가 이미 존재하는지 확인
            if new_english in vocabulary and new_english != word:
                return jsonify({"success": False, "message": f"'{new_english}' 단어가 이미 존재합니다."}), 409
            
            # 기존 단어 삭제
            del vocabulary[word]
            
            # 통계 이전
            if word in quiz_stats:
                quiz_stats[new_english] = quiz_stats.pop(word)
            
            # 새 단어 추가
            vocabulary[new_english] = {
                "korean": new_korean,
                "category": new_category
            }
        else:
            # 단어는 같고 뜻/카테고리만 변경
            vocabulary[word] = {
                "korean": new_korean,
                "category": new_category
            }
        
        if save_data():
            logger.info(f"단어 수정 성공: {word} -> {new_english}")
            return jsonify({"success": True, "message": f"단어가 수정되었습니다!"})
        else:
            return jsonify({"success": False, "message": "파일 저장에 실패했습니다."}), 500
            
    except Exception as e:
        logger.error(f"단어 수정 오류: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500

# 단어 검색 API
@app.route('/api/words/<word>', methods=['GET'])
def search_word(word):
    """단어 검색"""
    word = word.lower()
    if word in vocabulary:
        data = vocabulary[word]
        return jsonify({
            "success": True, 
            "english": word, 
            "korean": data.get("korean", ""),
            "category": data.get("category", "")
        })
    else:
        return jsonify({"success": False, "message": "단어를 찾을 수 없습니다."}), 404

# 퀴즈 문제 가져오기 API
@app.route('/api/quiz', methods=['POST'])
def get_quiz():
    """퀴즈 문제 생성"""
    data = request.get_json()
    quiz_type = data.get('type', 'english_to_korean')  # 'english_to_korean' or 'korean_to_english'
    quiz_mode = data.get('mode', 'text')  # 'text' (주관식) or 'multiple' (객관식)
    focus_mode = data.get('focus_mode', False)  # True면 틀린 단어만 선택
    
    if not vocabulary:
        return jsonify({"success": False, "message": "퀴즈를 하려면 먼저 단어를 추가해주세요."}), 400
    
    # 단어 선택
    words = list(vocabulary.keys())
    
    # 카테고리 필터링
    quiz_category = data.get('category', None)
    if quiz_category and quiz_category != "":
        words = [w for w in words if vocabulary[w].get("category", "") == quiz_category]
        if not words:
            return jsonify({"success": False, "message": f"'{quiz_category}' 카테고리에 단어가 없습니다."}), 400
    
    # 틀린 단어 집중 학습 모드
    if focus_mode:
        # 정답률이 낮은 단어 우선 선택 (틀린 횟수가 많은 단어)
        words_with_stats = []
        for word in words:
            if word in quiz_stats:
                correct, wrong = quiz_stats[word]
                total = correct + wrong
                if total > 0:
                    accuracy = (correct / total) * 100
                    # 정답률이 낮거나 틀린 횟수가 많은 단어 우선
                    words_with_stats.append((word, accuracy, wrong))
        
        if words_with_stats:
            # 정답률 낮은 순으로 정렬 (같으면 틀린 횟수 많은 순)
            words_with_stats.sort(key=lambda x: (x[1], -x[2]))
            # 하위 50% 중에서 랜덤 선택 (너무 제한적이지 않게)
            bottom_half = words_with_stats[:max(1, len(words_with_stats) // 2)]
            word = random.choice(bottom_half)[0]
        else:
            # 통계가 없는 단어 중에서 선택
            word = random.choice(words)
    else:
        # 일반 모드: 랜덤 선택
        word = random.choice(words)
    
    # 객관식 문제 생성
    if quiz_mode == 'multiple':
        return get_multiple_choice_quiz(word, quiz_type)
    
    # 주관식 문제 생성
    word_data = vocabulary[word]
    korean = word_data.get("korean", "")
    
    if quiz_type == 'english_to_korean':
        return jsonify({
            "success": True,
            "type": "english_to_korean",
            "mode": "text",
            "word": word,
            "question": f"'{word}'의 한국어 뜻은?",
            "correct_answer": korean
        })
    else:  # korean_to_english
        return jsonify({
            "success": True,
            "type": "korean_to_english",
            "mode": "text",
            "word": word,
            "question": f"'{korean}'의 영어 단어는?",
            "correct_answer": word
        })

def get_multiple_choice_quiz(correct_word: str, quiz_type: str) -> Dict:
    """
    4지선다 객관식 문제 생성
    
    Args:
        correct_word: 정답 단어
        quiz_type: 'english_to_korean' or 'korean_to_english'
        
    Returns:
        JSON 응답 데이터
    """
    words = list(vocabulary.keys())
    
    # 정답 1개 + 오답 3개 선택
    wrong_words = [w for w in words if w != correct_word]
    if len(wrong_words) < 3:
        # 단어가 4개 미만이면 오답을 반복 사용
        while len(wrong_words) < 3:
            wrong_words.append(random.choice(words))
    
    wrong_choices = random.sample(wrong_words, min(3, len(wrong_words)))
    
    # 선택지 생성
    correct_word_data = vocabulary[correct_word]
    correct_korean = correct_word_data.get("korean", "")
    
    if quiz_type == 'english_to_korean':
        # 영어 → 한글: 정답은 correct_word의 뜻, 오답은 다른 단어들의 뜻
        correct_answer = correct_korean
        wrong_answers = [vocabulary[w].get("korean", "") for w in wrong_choices]
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)  # 선택지 섞기
        
        return jsonify({
            "success": True,
            "type": "english_to_korean",
            "mode": "multiple",
            "word": correct_word,
            "question": f"'{correct_word}'의 한국어 뜻은?",
            "correct_answer": correct_answer,
            "choices": choices,
            "correct_index": choices.index(correct_answer)
        })
    else:  # korean_to_english
        # 한글 → 영어: 정답은 correct_word, 오답은 다른 단어들
        correct_answer = correct_word
        wrong_answers = wrong_choices
        choices = [correct_answer] + wrong_answers
        random.shuffle(choices)  # 선택지 섞기
        
        return jsonify({
            "success": True,
            "type": "korean_to_english",
            "mode": "multiple",
            "word": correct_word,
            "question": f"'{correct_korean}'의 영어 단어는?",
            "correct_answer": correct_answer,
            "choices": choices,
            "correct_index": choices.index(correct_answer)
        })

@app.route('/api/quiz/check', methods=['POST'])
def check_quiz():
    """
    퀴즈 정답 확인 API
    
    Request Body:
        {
            "word": "단어",
            "answer": "사용자 답" (주관식) or 선택한 인덱스 (객관식),
            "type": "english_to_korean" or "korean_to_english",
            "mode": "text" (주관식) or "multiple" (객관식),
            "correct_index": 정답 인덱스 (객관식인 경우)
        }
        
    Returns:
        JSON: 정답 여부 및 통계
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "요청 데이터가 없습니다."}), 400
        
        word = data.get('word', '').lower().strip()
        user_answer = data.get('answer', '')
        quiz_type = data.get('type', 'english_to_korean')
        quiz_mode = data.get('mode', 'text')
        correct_index = data.get('correct_index', None)
        
        if not word:
            return jsonify({"success": False, "message": "단어를 입력해주세요."}), 400
        
        if word not in vocabulary:
            return jsonify({"success": False, "message": "단어를 찾을 수 없습니다."}), 404
        
        # 객관식 정답 확인
        if quiz_mode == 'multiple':
            if correct_index is None:
                return jsonify({"success": False, "message": "정답 인덱스가 없습니다."}), 400
            
            try:
                user_index = int(user_answer)
                is_correct = user_index == correct_index
            except (ValueError, TypeError):
                return jsonify({"success": False, "message": "잘못된 답안입니다."}), 400
        else:
            # 주관식 정답 확인
            if not user_answer:
                return jsonify({"success": False, "message": "답을 입력해주세요."}), 400
            
            word_data = vocabulary[word]
            if quiz_type == 'english_to_korean':
                correct_answer = word_data.get("korean", "")
                is_correct = user_answer.strip() == correct_answer
            else:  # korean_to_english
                correct_answer = word
                is_correct = user_answer.lower().strip() == correct_answer.lower()
        
        # 통계 초기화 (없는 경우)
        if word not in quiz_stats:
            quiz_stats[word] = [0, 0]
        
        # 통계 업데이트
        if is_correct:
            quiz_stats[word][0] += 1  # 맞춘 횟수
            logger.debug(f"퀴즈 정답: {word}")
        else:
            quiz_stats[word][1] += 1  # 틀린 횟수
            logger.debug(f"퀴즈 오답: {word}")
        
        save_data()
        
        # 정답 정보 반환
        word_data = vocabulary[word]
        if quiz_type == 'english_to_korean':
            correct_answer = word_data.get("korean", "")
        else:
            correct_answer = word
        
        return jsonify({
            "success": True,
            "is_correct": is_correct,
            "correct_answer": correct_answer,
            "stats": quiz_stats[word]
        })
        
    except Exception as e:
        logger.error(f"퀴즈 정답 확인 오류: {e}")
        return jsonify({"success": False, "message": "서버 오류가 발생했습니다."}), 500

# 통계 API
@app.route('/api/stats', methods=['GET'])
def get_stats():
    """퀴즈 통계 가져오기"""
    stats_list = []
    
    for word, stats in quiz_stats.items():
        if word not in vocabulary:
            continue  # 단어가 삭제된 경우 스킵
        
        correct, wrong = stats
        total = correct + wrong
        accuracy = (correct / total * 100) if total > 0 else 0
        
        word_data = vocabulary[word]
        stats_list.append({
            "word": word,
            "korean": word_data.get("korean", "?"),
            "category": word_data.get("category", ""),
            "correct": correct,
            "wrong": wrong,
            "total": total,
            "accuracy": round(accuracy, 1)
        })
    
    # 정답률 순으로 정렬
    stats_list.sort(key=lambda x: x['accuracy'], reverse=True)
    
    return jsonify(stats_list)

# 카테고리 목록 API
@app.route('/api/categories', methods=['GET'])
def get_categories():
    """모든 카테고리 목록 가져오기"""
    categories = set()
    for word_data in vocabulary.values():
        category = word_data.get("category", "").strip()
        if category:
            categories.add(category)
    
    # 빈 카테고리도 포함 (카테고리 없음)
    categories_list = sorted(list(categories))
    return jsonify(categories_list)

def start_server(port: int = None) -> None:
    """
    Flask 서버 시작
    
    Args:
        port: 서버 포트 번호 (None이면 환경 변수 또는 기본값 사용)
    """
    # 프로덕션 환경에서는 PORT 환경 변수 사용 (Railway, Render 등)
    if port is None:
        port = int(os.environ.get('PORT', DEFAULT_PORT))
    
    # 프로덕션 환경 확인
    is_production = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('ENV') == 'production'
    debug_mode = not is_production
    
    # 호스트 설정 (프로덕션에서는 0.0.0.0)
    host = '0.0.0.0' if is_production else '127.0.0.1'
    
    logger.info("="*60)
    logger.info("영어 단어장 웹 애플리케이션 시작!")
    logger.info("="*60)
    logger.info(f"단어 개수: {len(vocabulary)}개")
    logger.info(f"통계 기록: {len(quiz_stats)}개")
    logger.info(f"모드: {'프로덕션' if is_production else '개발'}")
    logger.info(f"접속 주소: http://{host}:{port}")
    logger.info("="*60)
    
    app.run(debug=debug_mode, host=host, port=port, use_reloader=False)

if __name__ == '__main__':
    # 프로그램 시작 시 데이터 로드
    load_data()
    
    try:
        start_server(DEFAULT_PORT)
    except OSError as e:
        if "Address already in use" in str(e):
            logger.warning(f"포트 {DEFAULT_PORT}이 사용 중입니다. {FALLBACK_PORT} 포트로 시도합니다.")
            start_server(FALLBACK_PORT)
        else:
            logger.error(f"서버 시작 실패: {e}")
            raise
    except Exception as e:
        logger.error(f"서버 시작 실패: {e}")
        raise

