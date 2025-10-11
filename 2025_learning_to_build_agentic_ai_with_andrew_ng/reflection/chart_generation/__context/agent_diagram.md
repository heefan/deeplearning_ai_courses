# Agent Call Diagram - Chart Generation with Reflection Pattern

This diagram shows the complete agent interaction flow for the reflection-based chart generation system.

## System Architecture (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REFLECTION PATTERN FLOW                          │
└─────────────────────────────────────────────────────────────────────────────┘

    User Query
         │
         ▼
┌─────────────────┐
│   Orchestrator  │ ◄─── Controls the reflection loop
│   (Reflection   │      (max 3 iterations)
│    Manager)     │
└─────────────────┘
         │
         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Generator     │───▶│   LMStudio      │───▶│   Generated     │
│   Agent         │    │   gpt-oss-20b   │    │   Code          │
│                 │    │                 │    │                 │
│ • Creates code  │    │ • Local model   │    │ • Python code  │
│ • Uses schema   │    │ • Structured    │    │ • <execute_     │
│ • Gets context  │    │   output        │    │   python> tags  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                           │
         │                                           ▼
         │                                  ┌─────────────────┐
         │                                  │   Critic        │
         │                                  │   Agent         │
         │                                  │                 │
         │                                  │ • Reviews code  │
         │                                  │ • Checks logic  │
         │                                  │ • Validates req │
         │                                  └─────────────────┘
         │                                           │
         │                                           ▼
         │                                  ┌─────────────────┐
         │                                  │   LMStudio      │
         │                                  │   gpt-oss-20b   │
         │                                  │                 │
         │                                  │ • Code review   │
         │                                  │ • Feedback      │
         │                                  │ • Approval      │
         │                                  └─────────────────┘
         │                                           │
         │                                           ▼
         │                                  ┌─────────────────┐
         │                                  │   Decision      │
         │                                  │   Point         │
         │                                  │                 │
         │                                  │ Approved?       │
         │                                  │ ┌─────────────┐ │
         │                                  │ │    YES      │ │
         │                                  │ └─────────────┘ │
         │                                  │ ┌─────────────┐ │
         │                                  │ │     NO      │ │
         │                                  │ └─────────────┘ │
         │                                  └─────────────────┘
         │                                           │
         │                    ┌──────────────────────┼──────────────────────┐
         │                    │                      │                      │
         │                    ▼                      ▼                      ▼
         │            ┌─────────────┐        ┌─────────────┐        ┌─────────────┐
         │            │   Code      │        │ Improvement │        │   Code      │
         │            │ Executor   │        │ Feedback    │        │ Executor    │
         │            │            │        │             │        │             │
         │            │ • Extract  │        │ • Specific  │        │ • Extract   │
         │            │   code     │        │   issues    │        │   code      │
         │            │ • Validate │        │ • Improve  │        │ • Validate  │
         │            │   imports  │        │   suggestions│       │   imports   │
         │            │ • Execute│        │ • Context    │        │ • Execute    │
         │            │   safely   │        │   update    │        │   safely    │
         │            └─────────────┘        └─────────────┘        └─────────────┘
         │                    │                      │                      │
         │                    ▼                      │                      ▼
         │            ┌─────────────┐                │              ┌─────────────┐
         │            │ Generated  │                │              │ Generated  │
         │            │ Charts     │                │              │ Charts     │
         │            │            │                │              │            │
         │            │ • PNG/SVG  │                │              │ • PNG/SVG  │
         │            │ • Files   │                │              │ • Files    │
         │            │ • Results │                │              │ • Results  │
         │            └─────────────┘                │              └─────────────┘
         │                    │                      │                      │
         │                    ▼                      │                      ▼
         │            ┌─────────────┐                │              ┌─────────────┐
         │            │   User      │                │              │   User     │
         │            │  Results   │                │              │  Results   │
         │            │            │                │              │            │
         │            │ • Code     │                │              │ • Code     │
         │            │ • Charts  │                │              │ • Charts   │
         │            │ • History │                │              │ • History  │
         │            └─────────────┘                │              └─────────────┘
         │                                           │
         │                                           │
         └───────────────────────────────────────────┘
                    (Continue to next iteration)
```

## Detailed Reflection Loop (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        REFLECTION LOOP SEQUENCE                           │
└─────────────────────────────────────────────────────────────────────────────┘

User Query: "Create Q1 sales comparison chart"
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ITERATION 1                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Data      │    │ Generator   │    │ LMStudio    │    │ Generated   │
│  Schema     │───▶│   Agent    │───▶│ gpt-oss-20b │───▶│   Code      │
│             │    │             │    │             │    │             │
│ • Parse CSV │    │ • Build     │    │ • Generate  │    │ • Python    │
│ • Extract   │    │   prompt    │    │   code      │    │   code      │
│   schema    │    │ • Include   │    │ • Return    │    │ • <execute_ │
│ • Get       │    │   context   │    │   structured │    │   python>   │
│   samples   │    │ • Send to   │    │   response  │    │   tags      │
│             │    │   LMStudio  │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                    │
                                                                    ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Critic    │    │ LMStudio    │    │ Critique    │    │ Decision    │
│   Agent     │◄───│ gpt-oss-20b │◄───│ Response   │◄───│ Point       │
│             │    │             │    │             │    │             │
│ • Review    │    │ • Analyze   │    │ • Result:   │    │ Approved?   │
│   code      │    │   code      │    │   approved/ │    │ ┌─────────┐ │
│ • Check     │    │ • Check     │    │   needs     │    │ │  YES    │ │
│   logic     │    │   logic     │    │   improve   │    │ └─────────┘ │
│ • Validate  │    │ • Validate  │    │ • Feedback  │    │ ┌─────────┐ │
│   reqs      │    │   reqs      │    │ • Issues    │    │ │   NO    │ │
│             │    │             │    │ • Suggestions│    │ └─────────┘ │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                                                    │
                                                                    ▼
                                                           ┌─────────────┐
                                                           │   Branch    │
                                                           │             │
                                                           │  ┌─────────┐│
                                                           │  │Approved ││
                                                           │  └─────────┘│
                                                           │  ┌─────────┐│
                                                           │  │Needs    ││
                                                           │  │Improve  ││
                                                           │  └─────────┘│
                                                           └─────────────┘
                                                                    │
                                                                    ▼
                                                           ┌─────────────┐
                                                           │   Action    │
                                                           │             │
                                                           │ ┌─────────┐ │
                                                           │ │Execute  │ │
                                                           │ │Code     │ │
                                                           │ └─────────┘ │
                                                           │ ┌─────────┐ │
                                                           │ │Update   │ │
                                                           │ │Context  │ │
                                                           │ │& Retry  │ │
                                                           │ └─────────┘ │
                                                           └─────────────┘
```

## Code Execution Flow (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CODE EXECUTION SAFETY FLOW                         │
└─────────────────────────────────────────────────────────────────────────────┘

Generated Code with <execute_python> tags
         │
         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CODE EXECUTOR                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Extract   │    │  Validate   │    │  Execute    │    │   Capture   │
│   Code      │    │  Imports    │    │  Safely     │    │  Results    │
│             │    │             │    │             │    │             │
│ • Parse     │    │ • Check     │    │ • Sandbox   │    │ • Output    │
│   tags      │    │   allowed   │    │   env       │    │   files     │
│ • Extract   │    │   imports   │    │ • Timeout   │    │ • Charts    │
│   Python     │    │ • matplotlib│    │   protect  │    │ • PNG/SVG   │
│   code      │    │ • pandas    │    │ • Error     │    │ • Results   │
│             │    │ • numpy     │    │   handling  │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
         │                 │                 │                 │
         ▼                 ▼                 ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Clean     │    │   Reject    │    │   Success   │    │   Return    │
│   Code      │    │   Unsafe    │    │   Result    │    │   Files    │
│             │    │   Code      │    │             │    │             │
│ • Remove    │    │ • Block     │    │ • Generated │    │ • Chart     │
│   tags      │    │   dangerous │    │   charts    │    │   paths     │
│ • Prepare   │    │   imports   │    │ • Execution │    │ • Metadata  │
│   for exec  │    │ • Log       │    │   time      │    │             │
│             │    │   attempt   │    │ • Return    │    │             │
│             │    │             │    │   code      │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Error Handling Flow (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ERROR HANDLING FLOW                              │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Agent    │    │   Retry     │    │   Max       │    │  Graceful   │
│   Call     │    │   Logic     │    │  Retries    │    │  Failure    │
│            │    │            │    │            │    │            │
│ • Success? │───▶│ • Retry    │───▶│ • Reached  │───▶│ • Log      │
│ • Error?   │    │   count    │    │   limit?   │    │   error    │
│            │    │ • Wait     │    │            │    │ • Return   │
│            │    │   time     │    │            │    │   message  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
         │                 │                 │                 │
         ▼                 ▼                 ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Continue   │    │   Retry     │    │   Stop     │    │   User      │
│   Flow     │    │   Agent     │    │   Process  │    │  Notified   │
│            │    │   Call     │    │            │    │            │
│ • Success  │    │ • Network  │    │ • Log      │    │ • Error    │
│   result   │    │   error    │    │   failure  │    │   message  │
│ • Generated │    │ • Timeout  │    │ • Cleanup  │    │ • Fallback │
│   code     │    │ • LMStudio │    │   resources│    │   response │
│            │    │   down     │    │            │    │            │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        EXECUTION ERROR HANDLING                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Code      │    │   Timeout  │    │   Syntax    │    │   Runtime   │
│ Execution   │    │   Error    │    │   Error     │    │   Error    │
│            │    │            │    │            │    │            │
│ • Success? │───▶│ • Timeout  │───▶│ • Invalid  │───▶│ • Name     │
│ • Error?   │    │   after    │    │   syntax    │    │   error    │
│            │    │   30s      │    │            │    │ • Import   │
│            │    │            │    │            │    │   error    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
         │                 │                 │                 │
         ▼                 ▼                 ▼                 ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Return    │    │   Log       │    │   Log       │    │   Log       │
│   Results   │    │   Timeout   │    │   Syntax    │    │   Runtime   │
│            │    │   Error     │    │   Error     │    │   Error     │
│ • Charts   │    │ • Return   │    │ • Return   │    │ • Return   │
│ • Files    │    │   -1 code   │    │   error    │    │   error    │
│ • Success  │    │ • Error    │    │   message  │    │   message  │
│   status   │    │   message  │    │            │    │            │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

## Component Interaction Map (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        COMPONENT INTERACTION MAP                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ADK Agents    │    │ Core Components  │    │ External        │
│                 │    │                 │    │ Services        │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Generator   │ │    │ │Orchestrator │ │    │ │ LMStudio    │ │
│ │ Agent       │ │◄───┤ │             │ │    │ │ gpt-oss-20b │ │
│ │             │ │    │ │ • Controls  │ │    │ │             │ │
│ │ • Creates   │ │    │ │   loop       │ │    │ │ • Local     │ │
│ │   code      │ │    │ │ • Manages   │ │    │ │   model     │ │
│ │ • Uses      │ │    │ │   context   │ │    │ │ • Structured│ │
│ │   schema    │ │    │ │ • Handles   │ │    │ │   output    │ │
│ │ • Gets      │ │    │ │   errors    │ │    │ │ • Fast      │ │
│ │   context   │ │    │ │             │ │    │ │   response  │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
│ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
│ │ Critic      │ │    │ │ Code        │ │    │ │ File        │ │
│ │ Agent       │ │◄───┤ │ Executor    │ │    │ │ System      │ │
│ │             │ │    │ │             │ │    │ │             │ │
│ │ • Reviews   │ │    │ │ • Extract   │ │    │ │ • Save      │ │
│ │   code      │ │    │ │   code      │ │    │ │   charts    │ │
│ │ • Checks    │ │    │ │ • Validate  │ │    │ │ • PNG/SVG   │ │
│ │   logic     │ │    │ │   imports   │ │    │ │ • Results  │ │
│ │ • Validates │ │    │ │ • Execute   │ │    │ │             │ │
│ │   reqs      │ │    │ │   safely    │ │    │ │             │ │
│ └─────────────┘     │ │    │ └─────────────┘ │    │ └─────────────┘ │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Data Flow       │    │ Data Flow       │    │ Data Flow       │
│                 │    │                 │    │                 │
│ • CSV Schema    │    │ • Generated     │    │ • Chart Files  │
│ • Sample Data   │    │   Code          │    │ • Results       │
│ • Date Range    │    │ • <execute_     │    │ • Metadata      │
│ • Coffee Types  │    │   python> tags  │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Key Features Summary (ASCII)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           KEY FEATURES SUMMARY                             │
└─────────────────────────────────────────────────────────────────────────────┘

🔄 REFLECTION LOOP                    🔒 SAFETY & SECURITY
┌─────────────────┐                  ┌─────────────────┐
│ • Generator     │                  │ • Code extract  │
│   creates code  │                  │   from tags     │
│ • Critic        │                  │ • Import        │
│   reviews       │                  │   validation    │
│ • Iterative     │                  │ • Sandboxed     │
│   improvement   │                  │   execution     │
│ • Context       │                  │ • Timeout       │
│   awareness     │                  │   protection    │
└─────────────────┘                  └─────────────────┘

📊 DATA INTEGRATION                  🧪 TESTING STRATEGY
┌─────────────────┐                  ┌─────────────────┐
│ • CSV schema    │                  │ • Unit tests    │
│   parsing       │                  │   (mocked)      │
│ • Sample data   │                  │ • E2E tests     │
│   extraction    │                  │   (real LMStudio│
│ • Date range    │                  │ • Performance   │
│   analysis      │                  │   benchmarks    │
│ • Coffee type   │                  │ • Error        │
│   enumeration   │                  │   scenarios     │
└─────────────────┘                  └─────────────────┘

⚡ PERFORMANCE                       🛠️ MODERN TOOLING
┌─────────────────┐                  ┌─────────────────┐
│ • Async/await   │                  │ • UV dependency │
│   for I/O       │                  │   management    │
│ • Connection    │                  │ • Pytest        │
│   pooling       │                  │   testing       │
│ • Cached        │                  │ • Black/isort  │
│   schema        │                  │   formatting    │
│ • Optimized     │                  │ • Ruff linting  │
│   prompts       │                  │ • MyPy type     │
└─────────────────┘                  └─────────────────┘
```

This ASCII diagram provides a comprehensive visual representation of the reflection-based chart generation system, showing all the key components, data flows, error handling, and safety measures in a clear, text-based format.