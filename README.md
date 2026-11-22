# Career Opportunity Tracker

**내가 중요하게 생각하는 기준으로 채용공고를 찾고, 지원 현황과 일정을 관리하는 Codex 스킬입니다.**

어떤 사람은 직무의 자율성과 성장 기회를, 다른 사람은 연봉·근무지·고용 안정성을 더 중요하게 봅니다. 이 스킬은 공통 조사 절차와 개인 프로필을 분리해, 같은 공고도 각자의 기준으로 비교하도록 돕습니다.

## 할 수 있는 일

- 개인의 경험·필수조건·선호에 맞는 채용공고 조사 및 비교
- 기업 공식 공고의 실제 업무·지원 조건·모집 상태·마감 확인
- 정성적 우선순위 또는 합의한 숫자 가중치로 추천 근거 설명
- 기존 공고와 대조해 플랫폼 중복을 합치고 신규·중요 변경 정리
- Notion에 공고·지원 여부·전형 단계·합불 결과 누적
- 지원 마감과 실제 과제·면접 일정을 연결된 캘린더에서 관리
- 요청받은 경우, 마감됐고 지원 이력이 없는 공고를 휴지통으로 정리

이 저장소는 에이전트가 읽는 **스킬 지침과 프로필 예시**를 제공합니다. 자체 크롤러나 채용 사이트 로그인 프로그램은 포함하지 않습니다. 사용할 수 있는 웹 검색·브라우저·Notion 연결 도구를 통해 작업합니다.

## 설치

Codex의 `$skill-installer`에 다음처럼 요청합니다.

```text
$skill-installer
https://github.com/sweeetpotatooo/career-opportunity-tracker/tree/main/skills/career-opportunity-tracker
이 경로의 스킬을 설치해줘.
```

설치된 스킬은 다음 턴부터 사용할 수 있습니다. 기본 설치 위치는 `$CODEX_HOME/skills/career-opportunity-tracker`이며, `CODEX_HOME`이 없으면 `~/.codex/skills/career-opportunity-tracker`입니다.

같은 이름의 스킬이 이미 설치돼 있다면 개인 프로필을 보존하면서 업데이트해 달라고 요청하세요. 기존 폴더를 통째로 지우면 개인 설정도 사라질 수 있습니다.

## 처음 사용하기

처음부터 YAML을 직접 작성할 필요는 없습니다. 원하는 일을 대화로 설명하면 프로필을 정리할 수 있습니다.

```text
$career-opportunity-tracker
내 경험과 채용공고 선택 기준을 프로필로 정리해줘.
필수조건은 서울 근무와 정규직이고, 연봉보다 배울 기회와 실제 제품 개선에 참여할 기회가 중요해.
아직 숫자 가중치는 정하지 않을게.
```

스킬의 `profiles/example.yaml`은 구조 설명용이며 실제 선호로 자동 적용하지 않습니다. 개인 프로필은 설치된 스킬 안의 `profiles/local/<이름>.yaml`에 저장하거나, 별도로 지정한 파일을 사용합니다.

다른 사람의 프로필을 만들 때는 해당 사람의 경험·기준·저장 위치를 별도로 설정합니다. 다른 사람의 지원 대시보드에 섞어 기록하지 않습니다.

## 사용 예시

### 공고 조사

```text
$career-opportunity-tracker
내 프로필 기준으로 현재 지원 가능한 공고를 찾아줘.
LinkedIn과 주요 채용 플랫폼에서 찾고 공식 공고를 확인해줘.
신규 후보는 최대 5개만, 적합성과 준비할 점을 나눠 정리해줘.
```

### 특정 공고 검토·등록

```text
$career-opportunity-tracker
이 공고가 내 기준에 맞는지 확인하고 Notion 대시보드에 추가해줘: <공고 URL>
```

### 전형 결과 반영

```text
$career-opportunity-tracker
A회사 B직무는 서류 탈락이야. 지원 기록에 반영해줘.
C회사 D직무 면접은 12월 3일 오후 2시야. 해당 공고에 연결해서 기록해줘.
```

### 마감 공고 정리

```text
$career-opportunity-tracker
지원 기록이 없고 지원기간이 지난 공고와 연결된 마감 일정을 정리해줘.
```

지원·합불 이력은 보존하며, 오늘 밤 마감 전인 공고나 상시·날짜 미상 공고를 추정 삭제하지 않습니다. 삭제는 복구 가능한 휴지통 이동으로 처리합니다.

## 내 기준과 가중치 설정

**필수조건**과 **가점**은 별개입니다. 연봉 하한이나 근무지가 필수라면, 다른 항목의 높은 점수로 조건 차이를 덮지 않습니다. 사용자 경력과 공고의 필수 경력·학위·어학·기술 경험도 별도로 대조합니다.

| 방식 | 설정 | 적합한 상황 |
| --- | --- | --- |
| 정성 우선순위 | `ranking_mode: ordinal`, `priority` 지정, `weight: null` | 무엇이 더 중요한지는 알지만 숫자 비중은 아직 정하지 않았을 때 |
| 가중치 평가 | `ranking_mode: weighted`, 활성 항목마다 숫자 `weight` 지정 | 항목별 비중을 명시적으로 합의했을 때 |

숫자를 사용한다면 다음처럼 설정할 수 있습니다. **아래 비율은 설명용이며 추천 기본값이 아닙니다.**

```yaml
ranking_mode: "weighted"
criteria:
  - id: "growth"
    label: "학습과 성장 기회"
    priority: 1
    weight: 45
    evidence: "멘토링과 피드백, 새로운 책임을 맡을 기회"
  - id: "work_style"
    label: "근무 방식"
    priority: 2
    weight: 30
    evidence: "내가 원하는 출근 방식과 근무 시간"
  - id: "compensation"
    label: "보상"
    priority: 3
    weight: 25
    evidence: "공고에 확인되는 연봉·보상 조건"
```

항목은 연봉·성장·고용 안정성·산업·직무 자율성·기술·근무 방식 등으로 바꿀 수 있습니다. 가중치는 0 이상, 전체 합은 양수여야 합니다. 합이 100이 아니면 비율로 정규화합니다.

공고에 정보가 없으면 `미확인`으로 남깁니다. 미기재를 낮은 점수로 단정하지 않으며, 미확인 항목 때문에 순위가 달라질 수 있으면 이를 밝힙니다. 점수는 선택을 돕는 수단이며 합격 가능성 예측이 아닙니다. 상세 기준은 [평가 방식](skills/career-opportunity-tracker/references/ranking.md)을 참고하세요.

## Notion 연결

Notion 저장은 연결 도구와 사용자가 접근할 수 있는 데이터베이스가 필요합니다. 사용할 대시보드·공고 데이터 소스·일정 데이터 소스를 개인 프로필의 `notion`에 지정합니다. 저장 위치가 없으면 우선 채팅으로 결과를 제공합니다.

```yaml
notion:
  dashboard: "<내 대시보드 URL>"
  jobs_source: "collection://<내 공고 데이터 소스 ID>"
  jobs_database: "<내 공고 데이터베이스 ID>"
  calendar_source: "collection://<내 일정 데이터 소스 ID>"
  calendar_database: "<내 일정 데이터베이스 ID>"
  timezone: "Asia/Seoul"
```

쓰기 전 현재 스키마와 기존 행을 읽습니다. 기본 필드 예시와 기록 원칙은 [지원 기록 운영](skills/career-opportunity-tracker/references/notion-workflow.md)에 있습니다. 기존 대시보드가 없다면 먼저 필요한 필드와 캘린더 구성을 정하고, 생성해 달라고 요청할 수 있습니다.

새 후보의 개인 지원·합불 상태는 `미확인`입니다. 공개 공고 조사로 개인 지원일·면접일·결과를 추정하지 않으며, 사용자가 입력한 기록은 보존합니다.

## 매일 자동으로 조사하려면

스킬 설치만으로 예약 작업이 생성되지는 않습니다. 사용하는 환경의 자동화 기능에서 실행 시간·대상 프로필·저장 위치를 지정해 예약합니다.

```text
$career-opportunity-tracker로 <프로필명>의 기준에 맞는 공고를 조사해줘.
기존 지원 기록과 비교해 신규·중요 변경을 Notion에 저장하고,
이미 지원한 공고를 제외한 3일 이내 마감을 알려줘.
```

마감 공고 삭제는 별도 요청이 있을 때 수행합니다. 일일 조사는 개인 기록을 보존합니다.

## 저장소 구성

```text
skills/career-opportunity-tracker/
├── SKILL.md
├── agents/openai.yaml
├── profiles/example.yaml
└── references/
    ├── ranking.md
    └── notion-workflow.md
```

개인 프로필·실제 Notion 주소·지원 결과·인증정보는 공개 버전에 포함하지 않습니다. `profiles/local/`, `*.local.yaml`과 환경 파일은 `.gitignore`에서 제외합니다. 공개용 예시나 지침을 수정할 때도 개인 데이터가 포함되지 않았는지 확인해 주세요.
