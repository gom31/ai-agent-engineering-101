"""Week 02 LAB 1 — 두 하네스가 공유하는 도구 / 모델 호출 / 측정 유틸.

Provider: OpenRouter (OpenAI 호환). 설정은 .env 에서 읽는다.
  OPENAI_BASE_URL=https://openrouter.ai/api/v1
  OPENAI_API_KEY=<키>
  AGENT_MODEL=google/gemma-4-31b-it:free

같은 도구 + 같은 모델을 두 하네스가 공유해야 A/B 가 '도구 비교'가 아닌
'하네스 비교'로 성립한다. 그래서 이 모듈이 하나뿐이다.

run_ab.py 와 두 하네스가 이 모듈에 기대하는 계약:
  - Meter 에 .tokens / .iters / .interventions 정수 속성
  - 모델 1회 호출 = iters 1 증가 + 사용 토큰을 tokens 에 적립
"""
import json
import os
import re


# ------------------------------------------------------------ .env loader
# (배선용. 학습 대상 아님 — 그대로 두면 된다.)
def _load_dotenv(path=".env"):
    """.env 의 KEY=VALUE 를 환경변수로. 실제 환경변수가 있으면 그쪽이 이긴다."""
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        return
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


_load_dotenv()

MODEL = os.environ.get("AGENT_MODEL", "google/gemma-4-31b-it:free")


# ============================================================ LAB 1-a. 도구 2개
# TODO read_file(path) -> str
#      작업 디렉터리 안의 텍스트 파일을 읽는다. 컨텍스트 보호용 길이 상한을 둔다.
#      (app.log 는 3082 바이트다. 상한을 어디에 두느냐가 실험 조건의 일부다.)
# TODO count_pattern(path, pattern) -> str
#      정규식에 맞는 줄 수를 센다.
# TODO TOOLS_IMPL = {"read_file": ..., "count_pattern": ...}
# TODO TOOL_SPECS = OpenAI tools 스키마 리스트
#      수업의 문장: "도구의 description 이 곧 인터페이스다."
#      모델은 이 설명문만 보고 도구를 고른다. 실험 조건이므로 REPORT.md 에 적을 것.


# ============================================================ LAB 1-b. Meter
# TODO class Meter
#      tokens / iters / interventions 를 한곳에서 센다.
#      add(n_in, n_out): 토큰 누적 + iters += 1  (모델 호출 1회 = 반복 1회)
#      interventions 는 하네스가 직접 올린다 (사람이 승인/거부한 횟수).


# ============================================================ LAB 1-c. 모델 호출
# TODO 대화 하나를 들고 있는 얇은 래퍼.
#      필요한 동작: 시스템/사용자 메시지 추가 → 1회 호출 → 도구 호출 실행 →
#                   도구 결과를 대화에 되돌려 넣기
#      OpenAI 호환 응답에서:
#        resp.choices[0].message            .content / .tool_calls
#        resp.usage.prompt_tokens / .completion_tokens  → Meter.add(...)
#      도구 결과 메시지 형식: {"role": "tool", "tool_call_id": ..., "content": ...}
#      [요소4] 도구가 예외를 던지면 에러 문자열을 결과로 되돌린다 (멈추지 않는다).
