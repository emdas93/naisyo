from konlpy.tag import Okt

def test_konlpy():
    try:
        # 형태소 분석기 초기화
        okt = Okt()
        
        # 테스트 문장
        sentence = "안녕하세요! KoNLPy가 잘 작동하는지 테스트 중입니다."
        
        # 형태소 분석
        morphs = okt.morphs(sentence)
        pos_tags = okt.pos(sentence)
        nouns = okt.nouns(sentence)
        
        # 결과 출력
        print("형태소:", morphs)
        print("품사 태깅:", pos_tags)
        print("명사 추출:", nouns)
        
        return True
    except Exception as e:
        print(f"KoNLPy 실행 중 오류 발생: {e}")
        return False

# 테스트 실행
if test_konlpy():
    print("KoNLPy가 정상적으로 실행되었습니다.")
else:
    print("KoNLPy 실행에 실패했습니다.")
