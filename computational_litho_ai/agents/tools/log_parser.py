# agents/tools/log_parser.py

def suggest_fix_from_logs(log_data: str) -> str:
    if "stitch error" in log_data.lower():
        return "Detected stitch error. Try aligning pattern boundaries at 45° overlap."
    elif "dose mismatch" in log_data.lower():
        return "Dose mismatch found. Recalibrate the EBL system and update OPC table."
    return "No critical issues found. Try increasing resist thickness slightly."
