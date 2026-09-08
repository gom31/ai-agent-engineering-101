"""Week 02 LAB 2 — ReAct 형 하네스.

매 스텝: Thought → Action(도구 호출) → Observation(결과) → 다시 Thought.
다음에 무엇을 할지를 매 스텝 다시 판단한다.

run_ab.py 가 기대하는 계약:
    run_react(task, log=print) -> (answer_str, meter)
    log(msg) 로 찍은 것이 logs/ 파일에 그대로 남는다.
    → Thought 와 Observation 이 로그에 보이게 찍을 것 (CHECKPOINT 4번)
"""
import sys

# TODO from tools_shared import ...   (Meter, 도구, 모델 래퍼)


# ------------------------------------------------------------ 다섯 요소
# 이 파일에서 다섯 축의 값을 '내가' 정한다. 모델이 정하지 않는다.
#
# [요소1] 컨텍스트 관리   : 전체 이력을 매 호출에 다 넣는가?
# [요소2] 도구 세분화     : tools_shared 의 TOOL_SPECS (두 하네스 공통)
# [요소3] 종료 조건       : max_steps 상한 + 모델이 도구를 안 부르면 종료
# [요소4] 에러 복구       : 도구 에러를 Observation 으로 되돌려 모델이 고치게
# [요소5] 인간 개입 지점  : IRREVERSIBLE 도구 앞에서 승인 요청, 횟수를 센다
#                          (읽기 전용 도구뿐이면 interventions 는 0으로 남는다)

SYSTEM = (
    ""  # TODO Thought 를 한 줄 쓰게 하고, 끝났으면 'Answer:' 로 답하게 하는 지시
)

IRREVERSIBLE = set()  # TODO 승인이 필요한 도구 이름. 지금 도구는 읽기 전용


def run_react(task, max_steps=8, log=print):
    # TODO 1) Meter 와 대화를 만들고 task 를 사용자 메시지로 넣는다
    # TODO 2) max_steps 만큼 루프:
    #           모델 호출 → 텍스트를 log 로 찍기(Thought 가 남아야 한다)
    #           도구 호출이 없으면 → 답으로 보고 종료
    #           IRREVERSIBLE 이면 승인 요청, 거부면 interventions += 1
    #           도구 실행 → 결과를 대화에 되돌려 넣기 → 다음 스텝
    # TODO 3) 상한에 걸리면 미완으로 종료
    raise NotImplementedError("LAB 2")


if __name__ == "__main__":
    task = sys.argv[1] if len(sys.argv) > 1 else \
        "In app.log, which hour (HH:00) has the most ERROR lines? Answer with the hour in HH:00 form."
    answer, m = run_react(task)
    print(answer)
    print(f"tokens={m.tokens} iters={m.iters} interventions={m.interventions}")
