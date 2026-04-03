# AI Modernization Platform

Production-style demo app for reverse engineering a legacy insurance system and a target modernization implementation, then surfacing rule-level migration gaps in a polished Streamlit UI.

## Stack

- Python
- Streamlit
- LangGraph
- OpenAI API with `gpt-5.4-mini`

## Features

- Reverse engineers legacy and target folders into structured specs
- LangGraph orchestration across modular agents
- Agent-level caching under `outputs/cache/`
- Safe JSON parsing and normalized outputs
- Error-tolerant file reading with encoding recovery
- Gap analysis with rule comparison table and confidence scoring
- Execution log visibility in the UI
- Sample legacy and target insurance inputs included
- Local mock fallback when `OPENAI_API_KEY` is not set

## Project Structure

```text
app.py
graph.py
config.py
agents/
utils/
prompts/
sample_inputs/
outputs/cache/
```

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Optionally set your OpenAI key:

```bash
set OPENAI_API_KEY=your_key_here
```

4. Run the app:

```bash
streamlit run app.py
```

## Usage

- Leave the default sample folders in place for an immediate demo run.
- Or point the sidebar inputs at your own legacy and target system folders.
- Click `Run Modernization Analysis`.

## Notes

- The app uses `gpt-5.4-mini` by default and can be overridden with `OPENAI_MODEL`.
- If no API key is present, the app uses deterministic mock outputs so the UI still works for demos and onboarding.
