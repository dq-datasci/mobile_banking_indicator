#!/usr/bin/env python
import os
import json
import argparse
from datetime import datetime

def format_log(jsonl_path, topic, author="Antigravity", date=None):
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")

    if not os.path.exists(jsonl_path):
        print(f"Error: No se encontró el log en {jsonl_path}")
        return False

    markdown_lines = []
    
    header = f"""
# ====================================================================================================
# FECHA: {date} | AUTOR: {author}
# SESIÓN: N/A | TEMA: {topic}
# ====================================================================================================

# Chat Conversation

Note: _This is an auto-generated export of the chat conversation._
"""
    markdown_lines.append(header)

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            try:
                data = json.loads(line)
            except:
                continue

            # Procesar entrada del usuario
            if data.get("source") == "USER_EXPLICIT" and data.get("type") in ["USER_INPUT", "VIEW_FILE"]:
                content = data.get("content", "").strip()
                
                # Limpiar tags del sistema
                if "<USER_REQUEST>" in content:
                    content = content.split("<USER_REQUEST>")[-1].split("</USER_REQUEST>")[0].strip()
                if "<ADDITIONAL_METADATA>" in content:
                    content = content.split("<ADDITIONAL_METADATA>")[0].strip()
                
                if content:
                    markdown_lines.append(f"### User Input\n\n{content}\n")

            # Procesar respuesta del modelo (Antigravity)
            elif data.get("source") == "MODEL" and data.get("type") == "PLANNER_RESPONSE":
                content = data.get("content", "").strip()
                tool_calls = data.get("tool_calls", [])
                
                tool_texts = []
                for tc in tool_calls:
                    # Extraer el resumen o acción de la herramienta, o el nombre de la herramienta
                    args = tc.get("args", {})
                    action = args.get("toolSummary", args.get("toolAction", tc.get("name")))
                    action = action.strip('"') # limpiar comillas si vienen
                    tool_texts.append(f"*{action}*")
                
                if content or tool_texts:
                    markdown_lines.append(f"### Planner Response\n")
                    if content:
                        markdown_lines.append(f"{content}\n")
                    if tool_texts:
                        markdown_lines.append("\n".join(tool_texts) + "\n")

    output_content = "\n".join(markdown_lines)
    
    target_path = "docs/NOTEBOOKLM_LOGS/Antigravity_Logs_David.md"
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    with open(target_path, "a", encoding="utf-8") as out_f:
        out_f.write(output_content + "\n")
        
    print(f"✅ Log exportado exitosamente a {target_path}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exporta el log de la sesión de Antigravity")
    parser.add_argument("--session-id", required=True, help="El ID de la conversación (conversation-id)")
    parser.add_argument("--topic", required=True, help="El tema de la conversación")
    parser.add_argument("--base-dir", default=os.path.expanduser("~/.gemini/antigravity-ide/brain/"), help="Directorio base de logs")
    
    args = parser.parse_args()
    
    jsonl_path = os.path.join(args.base_dir, args.session_id, ".system_generated", "logs", "transcript.jsonl")
    
    format_log(jsonl_path, args.topic)
