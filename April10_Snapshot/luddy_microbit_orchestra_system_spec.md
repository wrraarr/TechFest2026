
# Luddy Micro:bit Orchestra — Full System Specification and Implementation Plan

## 1. Purpose

Create a browser-based orchestral instrument for outreach in which multiple students use assigned micro:bits as physical musical roles. A single USB-connected hub micro:bit forwards radio messages to a web app. The web app converts those messages into quantized, harmonically constrained string performance using Tone.js sample playback.

This document assumes the following are already working:

- Tone.js sample playback for violin
- Tone.js sample playback for viola
- Tone.js sample playback for cello
- Tone.js sample playback for double bass

## 2. Design Intent

The system should feel magical, legible, and forgiving:

- every student can make a meaningful contribution immediately
- the ensemble should sound musical even with imperfect timing
- “weirdness” should be controllable without collapsing into noise
- setup and reset should be simple enough for a live demo environment

## 3. High-Level Architecture

### 3.1 Topology

- **12 satellite micro:bits** act as controllers
- **1 hub micro:bit** receives radio packets and forwards them over USB serial
- **1 laptop/browser host** runs the Tone.js orchestra engine and dashboard

### 3.2 Roles

#### Conductors
- **Tempo Baton (`T`)**
- **Key Controller (`K`)**
- **Dissonance Dial (`D`)**

#### Players
- **Violins**: `V1`, `V2`, `V3`, `V4`
- **Violas**: `VA1`, `VA2`
- **Cellos**: `C1`, `C2`
- **Double Bass**: `B1`

## 4. System Goals

### Functional goals
- connect browser to hub micro:bit over USB serial
- receive and parse all controller messages in real time
- maintain global musical state: key, tempo, dissonance
- quantize player events to the transport grid
- resolve player actions into harmonic string notes
- play notes through four sampled instrument families
- display an easy-to-read live dashboard for outreach

### Non-functional goals
- no page reloads required during normal operation
- resilient to brief packet bursts and over-enthusiastic students
- easy to explain to middle-school audiences
- degraded behavior should still sound musical

## 5. Recommended Message Strategy

## 5.1 Recommended split protocol

### Radio layer (micro:bit → hub)
Use `radio.sendValue(name, value)`.

Why:
- name/value pairs map directly to controller logic
- no custom parsing is needed on the hub
- names remain short and readable

### Serial layer (hub → browser)
Emit one ASCII line per event in this form:

`ID:VALUE`

Examples:
- `T:1`
- `K:2`
- `D:4`
- `V1:1`
- `VA2:1`
- `B1:1`

## 5.2 ID definitions

| ID | Sender | Value | Meaning |
|---|---|---:|---|
| `T` | Tempo baton | `1` | a detected beat tap/shake that creates accents and dynamic changes|
| `T` | Tempo baton (optional alt mode) | `40..200` | explicit BPM |
| `K` | Key controller | `0..3` | key index |
| `D` | Dissonance controller | `0..5` | dissonance bucket |
| `V1..V4` | violin players | `1` | trigger a one-shot event |
| `VA1..VA2` | viola players | `1` | trigger a one-shot event |
| `C1..C2` | cello players | `1` | trigger a one-shot event |
| `B1` | bass player | `1` | trigger a one-shot event |

## 5.3 Key index map

Recommended v1:

| Index | Key |
|---:|---|
| 0 | C major |
| 1 | G major |
| 2 | D major |
| 3 | A major |

This is intentionally simple for outreach. Minor keys can be added later.


## 5.4 Default interaction model

Use **one-shot triggers**, not sustained note-on/note-off behavior.

Why:
- simpler for kids
- avoids shared-sampler release collisions
- more reliable when several players share one instrument family
- works naturally with quantization and fixed note lengths

Optional advanced mode:
- `1` = note on
- `0` = note off

But that should be considered a later enhancement.

## 6. Micro:bit Firmware Specification

## 6.1 Shared rules for all satellites

Every satellite firmware should:
- set the same radio group at startup
- debounce its primary action
- show a short LED confirmation when a message is sent
- avoid flooding radio by sending only on meaningful change
- use a local cooldown timer to suppress repeated accidental sends

### Recommended cooldowns
- button/touch triggers: 120–180 ms
- shake / beat detection: 250 ms minimum
- tilt-derived continuous controls: send only on bucket change

## 6.2 Hub firmware

### Responsibilities
- join orchestra radio group
- receive all `name,value` messages
- forward them over USB serial as `name:value`
- optionally show a heartbeat LED when data is flowing

### Hub pseudocode

```text
on start:
  radio.setGroup(GROUP_ID)

on radio received value(name, value):
  serial.writeLine(name + ":" + value)
```

No musical logic belongs on the hub.

## 6.3 Tempo Baton (`T`)

### Recommended v1 behavior
- student shakes or taps the baton in time
- each valid beat sends `T:1`
- browser computes BPM from recent taps

### Baton firmware rules
- detect a shake or acceleration threshold crossing
- ignore re-triggers inside cooldown window
- optionally light a center LED on every sent beat

### Why this is best
Tap tempo is intuitive and performative. It makes “conducting” visible and social.

### Optional v2 behavior
Buttons A/B increment or decrement BPM directly and send explicit BPM:
- `T:110`
- `T:124`

## 6.4 Key Controller (`K`)

### Interaction
- Button A cycles backward
- Button B cycles forward
- display current key letter or number briefly
- send updated key index whenever it changes

### State
Store an integer `0..3`.

## 6.5 Dissonance Controller (`D`)

### Interaction
- map pitch or roll angle to six buckets: `0..5`
- only transmit when bucket changes
- LED bar or icon reflects current bucket

### Behavior
- `0` = diatonic / stable
- `5` = maximum tension / chromatic disruption

## 6.6 Players (`V1..B1`)

### Interaction options
Choose one primary gesture per device:
- button A
- capacitive touch logo
- shake
- pin touch using alligator clip pad

For outreach, use whichever is most physically expressive and robust.

### Event rule
On trigger:
- if cooldown expired, send `ID:1`

### Device labels
Every player micro:bit should be visibly labeled with:
- instrument family
- player ID
- one-line instruction (“Press to play”)

## 7. Browser Host Specification

## 7.1 Browser and hosting assumptions

Run in a Chromium-based browser and serve from a secure context (HTTPS or localhost). The app must not assume Firefox or Safari support for Web Serial.

## 7.2 App state machine

```text
BOOT
  -> AUDIO_READY
  -> SERIAL_READY
  -> LIVE
  -> ERROR / RECOVER
```

### BOOT
- load UI shell
- create state store
- prepare sample manifests

### AUDIO_READY
- user presses “Start Audio”
- call `Tone.start()`
- create transport and audio graph
- preload samplers

### SERIAL_READY
- user chooses hub via Web Serial
- open serial port
- start line reader
- show connection status

### LIVE
- incoming events update state and trigger scheduling

### ERROR / RECOVER
- serial disconnect
- sample load failure
- malformed line
- user can reconnect without reloading page

## 7.3 JavaScript module layout

Recommended file structure:

```text
/orchestra
  index.html
  /css
    app.css
  /js
    app.js
    serialBridge.js
    parser.js
    stateStore.js
    scheduler.js
    scoreEngine.js
    audioEngine.js
    ui.js
    diagnostics.js
  /data
    violinManifest.js
    violaManifest.js
    celloManifest.js
    bassManifest.js
```

## 7.4 SerialBridge module

Responsibilities:
- request port
- open port at configured baud rate
- read UTF-8 text lines
- split on newline
- emit parsed messages to the app

### Parsed event shape

```js
{
  id: "V1",
  value: 1,
  receivedAt: performance.now(),
  raw: "V1:1"
}
```

### Parser rules
- trim whitespace
- require exactly one colon
- ignore malformed lines
- parse `value` as integer
- log parse errors in diagnostics panel

## 7.5 StateStore module

Global state:

```js
{
  tempo: 96,
  keyIndex: 0,
  dissonance: 0,
  transportStarted: false,
  lastTempoTapMs: null,
  tempoTapHistory: [],
  players: {
    V1: { lastSeen: 0, pending: false, lastNote: null, flash: 0 },
    ...
  }
}
```

## 8. Audio Engine Specification

## 8.1 Reuse your existing sample-loader pattern

Your current sampler prototype already demonstrates a useful pattern:
- build note maps from sample file names
- group them by dynamic
- create `Tone.Sampler` instances from those maps
- enable/disable notes based on available samples

That pattern should be turned into a reusable loader per instrument family.

## 8.2 Recommended orchestra loading strategy

### v1
Preload **one stable dynamic layer** per instrument family:
- violin
- viola
- cello
- bass

Recommended default: `mezzo-forte` or `forte`

### v2
Support dynamic banks and switching later.

### Important implementation choice
Do **not** dispose and recreate samplers during live outreach performance when a conductor control changes. Preload what you need before going live.

## 8.3 Logical voices

Use one-shot `triggerAttackRelease()` calls.

Suggested default durations:
- `B1`: `2n`
- `C1`, `C2`: `4n`
- `VA1`, `VA2`: `4n`
- `V1..V4`: `8n`

This keeps the lower strings foundational and the upper strings agile.

## 8.4 Audio graph

Recommended signal path:

```text
Instrument sampler(s)
  -> section gain
  -> master compressor
  -> limiter
  -> destination
```

Optional:
- very small room reverb send on violas/violins only
- keep it subtle to preserve rhythmic clarity

### Starting mix
- bass: +4 dB
- cello: +2 dB
- viola: 0 dB
- violin: -3 dB

## 8.5 Missing sample handling

Every instrument descriptor should expose:
- available note list
- minimum note
- maximum note

When score logic resolves a note:
1. compute desired pitch
2. clamp to instrument range
3. if exact note missing, choose nearest available note

This is more robust than assuming complete chromatic coverage.

## 9. Quantization and Scheduling

## 9.1 Why quantization is mandatory

Without quantization, the experience becomes a timing contest and quickly sounds chaotic. Quantization turns messy human timing into a coordinated ensemble texture.

## 9.2 Default quantization

Use:
- **grid:** next `8n`
- **transport:** `Tone.Transport`
- **scheduling policy:** place every player event on the next grid boundary

## 9.3 Event scheduling flow

```text
incoming player event
  -> validate cooldown
  -> mark player active in UI
  -> compute next quantized transport time
  -> resolve note
  -> schedule sample trigger
```

## 9.4 Tempo estimation from baton taps

Use a rolling window of recent tap timestamps.

Recommended algorithm:
1. keep last 4–6 beat times
2. compute inter-tap intervals
3. drop obvious outliers
4. average remaining intervals
5. convert to BPM
6. clamp to allowed range, e.g. 50–180 BPM
7. smooth transport BPM changes with a short ramp

This avoids wild tempo jumps from accidental double-shakes.

## 9.5 Device cooldown rules inside browser

In addition to firmware cooldown, enforce browser-side cooldown per device:
- ignore duplicate triggers from the same player inside a short window
- collapse multiple triggers from the same device into one scheduled note per quantization slot

That keeps one excited student from dominating the ensemble.

## 10. Score Engine Specification

## 10.1 Guiding idea

A player should not choose an exact pitch directly.

Instead, each player selects a **musical role**, and the score engine translates that role into a note based on:
- current key
- current dissonance
- the player’s lane
- recent section history

## 10.2 Harmonic role table

Recommended v1 player lanes:

| Player | Family | Register | Base degrees |
|---|---|---|---|
| `B1` | bass | low | `1` |
| `C1` | cello | low-mid | `1,5` |
| `C2` | cello | low-mid | `5,1` |
| `VA1` | viola | mid | `3,5` |
| `VA2` | viola | mid | `5,3` |
| `V1` | violin | high | `1,3,5` |
| `V2` | violin | high | `3,5,6` |
| `V3` | violin | high | `5,6,8` |
| `V4` | violin | high | `2,7,8` |

Use `8` to mean the octave above the root.

## 10.3 Selection method

For v1, use deterministic cycling instead of pure randomness.

Each player keeps a local step index:
- trigger 1 -> first degree
- trigger 2 -> next degree
- wrap around

Why:
- repeated actions feel learnable
- students can hear cause/effect
- ensemble sounds more coherent

## 10.4 Register map

Define a target octave for each family in each key. Example only:

- bass root around octave 2–3
- cellos around octave 3–4
- violas around octave 4
- violins around octave 5–6

Implementation should clamp against actual sample availability.

## 10.5 Dissonance model

Do **not** apply dissonance equally to all sections.

Recommended section weights:
- bass: very low
- cello: low
- viola: medium
- violin: high

This preserves harmonic grounding while letting upper voices create color.

### Dissonance levels

#### `D = 0`
- exact diatonic degree
- no chromatic displacement

#### `D = 1`
- occasional neighbor-tone displacement in violins only

#### `D = 2`
- low chance of ±1 semitone on violins/violas

#### `D = 3`
- moderate chance of chromatic shift
- occasional borrowed color tones

#### `D = 4`
- frequent chromatic alteration in upper strings
- cellos may occasionally alter by ±1 semitone

#### `D = 5`
- high chance of chromatic or non-scale tone in violins
- viola more adventurous
- bass remains mostly root/fifth anchored

## 10.6 Note resolution pseudocode

```js
function resolveNote(playerId, state) {
  const lane = PLAYER_LANES[playerId];
  const degree = lane.degrees[lane.stepIndex++ % lane.degrees.length];
  let midi = degreeToMidi(state.keyIndex, degree, lane.register);

  midi = applyDissonance({
    midi,
    dissonance: state.dissonance,
    section: lane.family
  });

  midi = clampToInstrumentRange(midi, lane.family);
  midi = snapToNearestAvailableSample(midi, lane.family);

  return Tone.Frequency(midi, "midi").toNote();
}
```

## 11. UI / Dashboard Specification

## 11.1 Primary controls

Top bar:
- Start Audio
- Connect Hub
- Reset Orchestra
- Demo Mode
- Fullscreen

## 11.2 Conductor panel

Three large cards:
- Tempo
- Key
- Dissonance

Each card shows:
- current value
- last update time
- animated visual state

### Tempo card
- live BPM
- tap indicator pulse
- metronome swing bar or pendulum

### Key card
- large key name
- optional circle-of-fifths mini display

### Dissonance card
- level `0..5`
- color ramp from calm to chaotic

## 11.3 Player panel

Nine large player cards:
- instrument label
- ID
- glow on trigger
- last note played
- small “alive” indicator if data recently received

Suggested grouping:
- Bass row
- Cello row
- Viola row
- Violin row

## 11.4 Diagnostics panel

Hidden by default or collapsible:
- serial connected/disconnected
- malformed packet count
- last 20 raw lines
- event counters per device
- sample load status

## 11.5 Visual feedback goals

A student should be able to tell:
- whether their micro:bit is connected and doing something
- whether the orchestra is fast or slow
- whether the music is getting stranger
- which section they belong to

## 12. Demo Mode Specification

A full fake-input mode is essential.

Demo Mode should:
- simulate serial messages without a hub micro:bit
- provide on-screen buttons for all 12 devices
- support automated random ensemble playback
- allow testing in classrooms before hardware distribution

This becomes your best debugging tool.

## 13. Error Handling and Safeguards

## 13.1 Serial disconnect
- detect disconnection
- show reconnection prompt
- retain app state
- allow reconnect without page reload

## 13.2 Audio not started
- block performance actions until user gesture starts audio
- display clear instruction

## 13.3 Packet flood
- enforce per-device browser cooldown
- collapse duplicate events inside the same beat window

## 13.4 Missing samples
- fallback to nearest available pitch
- mark issue in diagnostics log

## 13.5 Tempo instability
- smooth BPM updates
- ignore implausible double-taps
- keep last stable BPM if baton goes silent

## 13.6 Bad messages
- ignore malformed lines
- never crash parser on unexpected input

## 14. Implementation Plan

## Phase 1 — Refactor the sampler code into reusable instrument banks

Deliverables:
- one shared loader factory for violin/viola/cello/bass
- one stable default dynamic per family
- note availability metadata per instrument

Success criteria:
- each family can trigger arbitrary valid test notes from code
- no runtime sample reloads needed during play

## Phase 2 — Build browser shell + serial bridge + demo mode

Deliverables:
- Start Audio button
- Connect Hub button
- serial line reader
- packet parser
- demo mode event injector

Success criteria:
- raw `ID:VALUE` lines appear in UI log
- manual and simulated events reach application state

## Phase 3 — Hub firmware + single-device smoke test

Deliverables:
- hub MakeCode program
- one player micro:bit firmware
- one conductor micro:bit firmware

Success criteria:
- a real micro:bit trigger reaches browser reliably
- no manual intervention required after initial connect

## Phase 4 — Musical state + quantized scheduler

Deliverables:
- Tone.Transport setup
- tempo state
- key state
- dissonance state
- next-grid scheduling

Success criteria:
- one player trigger schedules a note on the next beat division
- baton taps update transport BPM smoothly

## Phase 5 — Score engine and section mapping

Deliverables:
- harmonic lane map
- deterministic player cycling
- range clamp
- dissonance transform

Success criteria:
- the same player sounds role-consistent across repeated triggers
- dissonance affects upper strings more than lower strings

## Phase 6 — Full UI dashboard

Deliverables:
- conductor cards
- player cards
- metronome
- diagnostics panel
- fullscreen-friendly layout

Success criteria:
- a middle-school audience can visually connect physical action to system behavior

## Phase 7 — Full ensemble rehearsal and outreach hardening

Deliverables:
- all 12 micro:bits programmed and labeled
- mix balancing
- cooldown tuning
- reset workflow
- printed facilitator instructions

Success criteria:
- complete orchestra can run through repeated demos
- restart sequence is simple and dependable

## 15. Acceptance Checklist

A v1 is ready when all of the following are true:

- browser connects to hub successfully
- all satellites send readable events
- all player actions create audible notes
- notes are quantized
- key changes affect harmony globally
- dissonance changes upper-voice behavior clearly
- baton meaningfully controls tempo
- the UI reflects current state
- system can recover from serial disconnect
- repeated enthusiastic input does not collapse the mix

## 16. Recommended MVP Build Order

If you want the shortest path to a compelling prototype, build in this order:

1. browser shell
2. serial bridge
3. demo mode
4. one violin player
5. one bass player
6. tempo baton
7. quantization
8. key controller
9. dissonance controller
10. remaining players
11. final dashboard polish

That path gets you to “physically playable and musically convincing” quickly.

## 17. Best v1 Decisions

These are the decisions I would lock in now:

- use `radio.sendValue(name, value)` on the micro:bits
- use `ID:VALUE` text lines over serial
- default to one-shot quantized notes
- preload one dynamic layer per instrument for reliability
- use deterministic player lanes before adding randomness
- keep bass mostly consonant even when dissonance is high
- treat demo mode as a first-class feature, not an afterthought

## 18. Suggested Next Technical Step

The immediate next code task is:

**replace your current single-instrument page with a modular orchestra shell that can:**
1. start Tone,
2. preload all four instrument families,
3. simulate `T`, `K`, `D`, `V1`, and `B1`,
4. quantize those events on the transport,
5. display conductor + player cards.

Once that exists, the micro:bits become just event sources.
