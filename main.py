import os
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse # <-- IMPORTED HTML RESPONSE
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# Import our Google Cloud SQL database setup
from database import SessionLocal, PatientIncident

load_dotenv()

app = FastAPI(title="TriageOS API", description="Multi-Agent Emergency Dispatch System")

# --- CORS CONFIGURATION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

system_instruction = """
You are the Primary Orchestrator Agent for TriageOS, a hospital emergency dispatch system.
Your job is to read raw emergency reports from paramedics and extract the necessary actions for your sub-agents.
You must return your analysis STRICTLY as a JSON object with this exact structure:
{
    "patient_details": "Brief summary of patient",
    "severity_level": "CRITICAL, HIGH, or MODERATE",
    "eta_minutes": integer representing minutes,
    "database_action": "What needs to be logged in the hospital database",
    "task_manager_action": "Specific task for nurses/staff to prepare",
    "calendar_action": "Who needs to be scheduled and for what"
}
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=system_instruction,
    generation_config={"response_mime_type": "application/json"}
)

class EmergencyRequest(BaseModel):
    message: str

# --- SUB-AGENT 1: Database Memory ---
def execute_database_agent(plan):
    print("\n[AGENT 1: DATABASE] Waking up...")
    db = SessionLocal()
    try:
        new_incident = PatientIncident(
            patient_details=plan["patient_details"],
            eta_minutes=plan["eta_minutes"],
            priority_level=plan["severity_level"],
            assigned_resources=plan["database_action"]
        )
        db.add(new_incident)
        db.commit()
        print("  -> SUCCESS: Emergency logged securely in Google Cloud SQL.")
        return "Logged to Cloud SQL successfully"
    except Exception as e:
        print(f"  -> FAILED: {e}")
        db.rollback()
        return f"Database error: {e}"
    finally:
        db.close()

# --- SUB-AGENT 2: Task Manager (MCP Integration) ---
def execute_task_agent(plan):
    print("\n[AGENT 2: TASK MANAGER] Waking up...")
    print("  -> Connecting to Hospital Jira/Trello via MCP...")
    time.sleep(1) # Simulating network delay
    
    mock_ticket = {
        "board": "ER_Trauma_Ward",
        "ticket_title": f"URGENT PREP: {plan['severity_level']} inbound",
        "description": plan['task_manager_action'],
        "assignee": "On-Duty Shift Lead",
        "status": "TODO"
    }
    
    print(f"  -> SUCCESS: Created urgent ticket: '{mock_ticket['ticket_title']}'")
    return {"status": "Ticket Created", "ticket_details": mock_ticket}

# --- SUB-AGENT 3: Calendar & Notes (MCP Integration) ---
def execute_calendar_agent(plan):
    print("\n[AGENT 3: CALENDAR & NOTES] Waking up...")
    print("  -> Connecting to Google Workspace via MCP...")
    time.sleep(1) # Simulating network delay
    
    mock_event = {
        "calendar": "Orthopedic_OnCall",
        "event_title": "EMERGENCY SURGERY STANDBY",
        "start_time": f"In {plan['eta_minutes']} minutes",
        "notes_attached": plan['calendar_action']
    }
    
    print(f"  -> SUCCESS: Scheduled '{mock_event['event_title']}' for {mock_event['start_time']}")
    return {"status": "Event Scheduled", "event_details": mock_event}

# --- API Endpoints ---

# FIXED FOR CLOUD RUN: This tells the cloud to show your HTML page!
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open("index.html", "r") as f:
        return f.read()

@app.post("/api/dispatch")
def handle_dispatch(request: EmergencyRequest):
    print(f"\n=========================================")
    print(f"[INCOMING EMERGENCY]: {request.message}")
    print(f"=========================================")
    
    try:
        print("\n[BOSS AGENT] Analyzing situation and delegating tasks...")
        response = model.generate_content(request.message)
        
        # FIXED: Robust JSON cleaning so Gemini doesn't crash the server
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        orchestrator_plan = json.loads(clean_json)
        
        db_status = execute_database_agent(orchestrator_plan)
        task_status = execute_task_agent(orchestrator_plan)
        calendar_status = execute_calendar_agent(orchestrator_plan)
        
        print("\n[SYSTEM] All tasks executed successfully.")
        
        return {
            "status": "success",
            "message": "Multi-Agent sequence executed autonomously.",
            "database_sub_agent": db_status,
            "mcp_task_agent": task_status,
            "mcp_calendar_agent": calendar_status,
            "execution_plan": orchestrator_plan
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)