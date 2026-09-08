"""Week 02 LAB 3 — Plan-then-Execute 형 하네스.

1차 호출로 전체 계획(단계 리스트)을 한 번에 받고, 2차부터 각 단계를 순서대로
실행한다. 계획을 미리 굳히므로 토큰이 적고 흐름이 예측 가능하지만, 중간
Observation 이 계획과 어긋나면 방향을 틀기 어렵다.

run_ab.py 가 기대하는 계약:
    run_plan_execute(task, log=print) -> (answer_str, meter, replans)
    세 번째 값 replans 가 results.csv 의 note 칸에 들어간다.
"""
import json
import sys

# TODO from tools_shared import ...


# ------------------------------------------------------------ ReAct 와 다르게 잡는 축
# [요소1] 컨텍스트 : 계획 대화와 실행 대화를 분리한다 (ReAct 는 단일 이력)
# [요소3] 종료     : 계획의 단계를 다 소진하면 종료 (+ 단계당 도구 호출 예산)
# [요소4] 에러 복구: 어긋나면 재계획 — 단 max_replan=1 로 유연성 상한을 명시
#
# REPORT.md (1) 변형 정의는 바로 이 대비를 쓰는 것이다.

SYSTEM_PLAN = ""  # TODO "JSON 리스트로만 답하라" 류의 계획 전용 지시
SYSTEM_EXEC = ""  # TODO 한 단계씩 실행, 어긋나면 'OFF_PLAN:', 최종은 'Answer:'


def parse_plan(text):
    """계획 텍스트 → 단계 문자열 리스트, 실패하면 None.

    파싱 실패는 버그가 아니라 이 하네스의 실패 모드 하나다. results.csv 의
    X 행이자 REPORT.md 의 finding 이 된다. 코드 펜스(```json)를 붙여 오는
    모델이 많다.
    """
    raise NotImplementedError("LAB 3")


def run_plan_execute(task, max_replan=1, max_tool_rounds=3, log=print):
    # TODO 1) PLAN: 도구 없이 1회 호출 → parse_plan. None 이면 실패로 반환
    # TODO 2) EXECUTE: 계획을 순서대로. 한 단계 안에서 도구 호출은
    #           max_tool_rounds 까지만 (예산을 넘으면 OFF_PLAN 취급)
    # TODO 3) OFF_PLAN 이고 replans < max_replan 이면 남은 단계만 재계획
    # TODO 4) 마지막에 최종 답을 'Answer:' 로 요청
    raise NotImplementedError("LAB 3")


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else \
        "In app.log, which hour (HH:00) has the most ERROR lines? Answer with the hour in HH:00 form."
    answer, m, replans = run_plan_execute(task)
    print(answer)
    print(f"tokens={m.tokens} iters={m.iters} interventions={m.interventions} replans={replans}")
