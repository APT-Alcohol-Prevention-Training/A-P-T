import csv
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional
from config import current_config


class SessionLogger:
    """Logger that tracks conversations by session and saves them as CSV files."""
    
    def __init__(self):
        self.config = current_config()
        self.sessions: Dict[str, List[Dict]] = {}
        # Directories are created by config.create_directories()
    
    
    def _get_status_dir(self, status: str) -> str:
        """Get the directory path for a given status."""
        if status == "active":
            return str(self.config.ACTIVE_SESSION_DIR)
        elif status == "completed":
            return str(self.config.COMPLETED_SESSION_DIR)
        else:
            return str(self.config.SESSION_LOG_DIR / status)
    
    def _get_csv_path(self, session_id: str, status: str) -> str:
        """Get the CSV file path for a session."""
        return os.path.join(self._get_status_dir(status), f"{session_id}.csv")
    
    def _get_metadata_path(self, session_id: str, status: str) -> str:
        """Get the metadata file path for a session."""
        return os.path.join(self._get_status_dir(status), f"{session_id}_metadata.json")
    
    def create_session(self, user_ip: str) -> str:
        """Create a new session for a user and return the session ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        
        # Create initial session metadata
        metadata = {
            "session_id": session_id,
            "user_ip": user_ip,
            "start_time": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Save metadata
        metadata_path = self._get_metadata_path(session_id, "active")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        
        return session_id
    
    def log_conversation(self, session_id: str, chatbot_type: str, user_message: str, 
                        bot_response: str, user_ip: str, risk_score: Optional[int] = None,
                        conversation_context: Optional[Dict] = None) -> bool:
        """Log a conversation entry for a specific session."""
        if session_id not in self.sessions:
            # Try to load existing session
            if not self._load_session(session_id):
                return False
        
        # Extract assessment answers and chat history from context
        assessment_answers = ""
        chat_history = ""
        if conversation_context:
            if "assessment_answers" in conversation_context:
                # Convert assessment answers to JSON string
                assessment_answers = json.dumps(conversation_context["assessment_answers"], ensure_ascii=False)
            if "chat_history" in conversation_context:
                # Convert chat history to JSON string
                chat_history = json.dumps(conversation_context["chat_history"], ensure_ascii=False)
        
        entry = {
            "timestamp": datetime.now().strftime(self.config.LOG_DATE_FORMAT),
            "conversation_number": len(self.sessions[session_id]) + 1,
            "chatbot_type": chatbot_type,
            "user_message": user_message,
            "bot_response": bot_response,
            "user_ip": user_ip,
            "risk_score": risk_score if risk_score is not None else "",
            "scenario": conversation_context.get("party_scenario", "") if conversation_context else "",
            "assessment_answers": assessment_answers,
            "chat_history": chat_history,
            "full_context": json.dumps(conversation_context, ensure_ascii=False) if conversation_context else ""
        }
        
        self.sessions[session_id].append(entry)
        
        self._save_session_csv(session_id)
        
        return True
    
    def _load_session(self, session_id: str) -> bool:
        """Load an existing session from disk."""
        csv_path = self._get_csv_path(session_id, "active")
        if os.path.exists(csv_path):
            self.sessions[session_id] = []
            with open(csv_path, "r", encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.sessions[session_id].append(row)
            return True
        return False
    
    def _save_session_csv(self, session_id: str):
        """Save session data to CSV file."""
        if session_id not in self.sessions or not self.sessions[session_id]:
            return
        
        csv_path = self._get_csv_path(session_id, "active")
        
        fieldnames = ["timestamp", "conversation_number", "chatbot_type", 
                     "user_message", "bot_response", "user_ip", "risk_score", "scenario",
                     "assessment_answers", "chat_history", "full_context"]
        
        with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.sessions[session_id])
    
    def end_session(self, session_id: str):
        """Mark a session as completed and move it to completed folder."""
        if session_id not in self.sessions:
            return
        
        # Update metadata
        metadata_path = self._get_metadata_path(session_id, "active")
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            metadata["end_time"] = datetime.now().isoformat()
            metadata["status"] = "completed"
            metadata["total_conversations"] = len(self.sessions[session_id])
            
            # Move files to completed folder
            new_metadata_path = self._get_metadata_path(session_id, "completed")
            with open(new_metadata_path, "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2)
            os.remove(metadata_path)
        
        # Move CSV file
        old_csv = self._get_csv_path(session_id, "active")
        new_csv = self._get_csv_path(session_id, "completed")
        if os.path.exists(old_csv):
            os.rename(old_csv, new_csv)
        
        # Remove from memory
        del self.sessions[session_id]
    
    def get_session_csv_path(self, session_id: str) -> Optional[str]:
        """Get the path to a session's CSV file."""
        # Check both active and completed sessions
        for status in ["active", "completed"]:
            csv_path = self._get_csv_path(session_id, status)
            if os.path.exists(csv_path):
                return csv_path
        
        return None
    
    def _list_sessions_in_dir(self, status: str) -> List[str]:
        """List all session IDs in a specific directory."""
        sessions = []
        dir_path = self._get_status_dir(status)
        if os.path.exists(dir_path):
            for file in os.listdir(dir_path):
                if file.endswith(".csv"):
                    sessions.append(file.replace(".csv", ""))
        return sessions
    
    def get_all_sessions(self) -> Dict[str, List[str]]:
        """Get all session IDs organized by status."""
        return {
            "active": self._list_sessions_in_dir("active"),
            "completed": self._list_sessions_in_dir("completed")
        }
    
    def export_all_sessions_to_csv(self, output_path: str):
        """Export all sessions (active and completed) to a single CSV file."""
        # Only proceed if session export feature is enabled
        if not self.config.FEATURE_SESSION_EXPORT:
            return 0
            
        all_data = []
        
        # Collect data from all sessions
        for status in ["active", "completed"]:
            session_ids = self._list_sessions_in_dir(status)
            for session_id in session_ids:
                csv_path = self._get_csv_path(session_id, status)
                if os.path.exists(csv_path):
                    with open(csv_path, "r", encoding="utf-8-sig") as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            row["session_id"] = session_id
                            row["session_status"] = status
                            all_data.append(row)
        
        # Sort by timestamp
        all_data.sort(key=lambda x: x.get("timestamp", ""))
        
        # Write to output CSV
        if all_data:
            fieldnames = ["session_id", "session_status", "timestamp", "conversation_number", 
                         "chatbot_type", "user_message", "bot_response", "user_ip", 
                         "risk_score", "scenario", "assessment_answers", "chat_history", "full_context"]
            
            with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(all_data)
        
        return len(all_data)

# Global instance
session_logger = SessionLogger()