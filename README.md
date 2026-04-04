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

1. Clone the repository and open a terminal in the project root.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Optionally configure an LLM provider.

For Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

Optional model override:

```powershell
$env:OPENAI_MODEL="gpt-5.4-mini"
```

If you want to use Anthropic instead:

```powershell
$env:ANTHROPIC_API_KEY="your_key_here"
```

If no API key is set, the app still runs using deterministic mock outputs for demo purposes.

## Run The App

Start Streamlit from the project root:

```bash
streamlit run app.py
```

After Streamlit starts, open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Quick Start

1. Run `streamlit run app.py`.
2. Leave the default `sample_inputs/legacy` and `sample_inputs/target` paths in place for a demo run.
3. Choose a model in the sidebar if needed.
4. Click `Run Modernization Analysis`.
5. Review the generated reverse-engineering, collation, and gap-analysis results in the UI.

## Usage

- Leave the default sample folders in place for an immediate demo run.
- Or point the sidebar inputs at your own legacy and target system folders.
- Click `Run Modernization Analysis`.

## Notes

- The app uses `gpt-5.4-mini` by default and can be overridden with `OPENAI_MODEL`.
- If no API key is present, the app uses deterministic mock outputs so the UI still works for demos and onboarding.
