# Professor presentation pack

- ATSA_Gold_Presentation.pptx: 30 slides with embedded speaker notes.
- ATSA_Gold_Presentation.pdf: portable slide version.
- FULL_PROJECT_WALKTHROUGH.pdf / .docx / .md: methodology, code, decisions, demo, and 42 viva answers.
- SPEAKER_SCRIPT.md: slide-by-slide spoken guidance.
- ACTUAL_25_ARIMA_RESULTS.csv: recorded notebook model scores.
- ALL_72_MODEL_ORDERS.csv: every app order and deterministic-trend rule.
- ALL_209664_APP_COMBINATIONS.csv.gz: exhaustive finite settings catalogue, not batch-tested fits.
- DEMO_AND_EDGE_CASE_MATRIX.csv: 26 operational cases with evidence status.
- presentation_content.json: slide content snapshot.

Main slides: 1-26; backups 27-29; references 30. Results are from October 26, 2026.
Live app values can change with data/history/order/FX. User confirmed Streamlit deployment on October 27, 2026; no production URL is invented.
Rebuild: python scripts/build_professor_pack.py (python-pptx, python-docx, reportlab required).
