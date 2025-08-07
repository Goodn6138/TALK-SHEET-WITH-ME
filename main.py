
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import httpx
# import os
# from typing import Optional
# import logging
# import json
# from dotenv import load_dotenv


# load_dotenv()

# # Configure logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI(title="Excel AI Backend", version="1.0.0")

# # CORS configuration 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "https://talk-sheet-with-me-1.onrender.com",
#         "https://script.google.com",
#         "https://script.googleusercontent.com",
#         "https://docs.google.com",
#         "https://*.google.com",
#         "https://*.googleusercontent.com",
#         "http://localhost:3000",
#         "http://127.0.0.1:3000",
#         "http://localhost:8080",
#          "http://0.0.0.0:8000",
#         "null",
#     ],
#     allow_credentials=False,
#     allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

# # Pydantic models 
# class CommandRequest(BaseModel):
#     input: str
#     context: Optional[str] = None
#     sheet_info: Optional[dict] = None

# class CommandResponse(BaseModel):
#     script: str
#     explanation: Optional[str] = None
#     status: str = "success"

# class ErrorResponse(BaseModel):
#     error: str
#     status: str = "error"


# COHERE_API_KEY = os.getenv("COHERE_API_KEY")
# COHERE_API_URL = "https://api.cohere.ai/v1/chat"

# if not COHERE_API_KEY:
#     logger.warning("COHERE_API_KEY not found in environment variables")

# async def call_cohere_api(prompt: str) -> str:
#     """Call Cohere API to generate Google Apps Script code"""
#     headers = {
#         "Authorization": f"Bearer {COHERE_API_KEY}",
#         "Content-Type": "application/json"
#     }
    
#     payload = {
#         "model": "command-r",  
#         "message": prompt,  # 
#         "max_tokens": 500,
#         "temperature": 0.3,
#         "stop_sequences": ["```", "---"]
#     }
    
#     async with httpx.AsyncClient(timeout=30.0) as client:
#         try:
#             logger.info(f"Sending Cohere API request with payload: {json.dumps(payload, indent=2)}")
#             response = await client.post(COHERE_API_URL, headers=headers, json=payload)
#             response.raise_for_status()
            
#             result = response.json()
#             generated_text = result.get("text", "").strip()
            
#             if not generated_text:
#                 logger.warning("Cohere API returned empty text")
#                 raise HTTPException(status_code=502, detail="Cohere API returned empty response")
                
#             logger.info(f"Cohere API response: {generated_text[:100]}...")
#             return generated_text
            
#         except httpx.TimeoutException:
#             logger.error("Cohere API request timed out")
#             raise HTTPException(status_code=504, detail="Cohere API timeout")
#         except httpx.HTTPStatusError as e:
#             logger.error(f"Cohere API error: {e.response.status_code} - {e.response.text}")
#             raise HTTPException(status_code=502, detail=f"Cohere API error: {e.response.text}")
#         except Exception as e:
#             logger.error(f"Unexpected error calling Cohere: {str(e)}", exc_info=True)
#             raise HTTPException(status_code=500, detail="Internal server error")

# def create_cohere_prompt(user_command: str, context: str = None) -> str:
#     """Create a well-structured prompt for Cohere API"""
    
#     command = user_command.strip()
#     if not command:
#         raise ValueError("User command cannot be empty")
    
#     base_prompt = f"""
# You are an expert in Google Apps Script for Google Sheets. Convert the following natural language command into valid Google Apps Script code that can be executed in a Google Sheets environment. Return only the executable JavaScript code, without explanations, comments, or markdown formatting (e.g., no ```javascript or ```). Ensure the code is safe, functional, and uses SpreadsheetApp APIs. For summation commands, return code that calculates and returns the result.

# Command: "{command}"

# Context: {context if context else "Working with a Google Sheets spreadsheet"}

# Examples:
# Command: "Sort the first column in ascending order"
# Code: SpreadsheetApp.getActiveSpreadsheet().getActiveSheet().getRange('A:A').sort(1);

# Command: "Sum all values in column A"
# Code: SpreadsheetApp.getActiveSheet().getRange('A:A').getValues().reduce((sum, [val]) => sum + (val || 0), 0);
# """
    
#     return base_prompt.strip()

# def sanitize_and_validate_script(script: str) -> str:
#     """Basic sanitization and validation of generated script"""
    
#     # Remove any markdown formatting
#     script = script.replace("```javascript", "").replace("```", "").strip()
    
#     # Basic security checks - prevent dangerous operations
#     dangerous_patterns = [
#         "eval(",
#         "Function(",
#         "setTimeout(",
#         "setInterval(",
#         "XMLHttpRequest",
#         "fetch(",
#         ".deleteSheet(",
#         ".deleteRange(",
#         "DriveApp.getFiles",
#         "GmailApp"
#     ]
    
#     for pattern in dangerous_patterns:
#         if pattern in script:
#             logger.warning(f"Potentially dangerous pattern detected: {pattern}")
#             # You might want to either block or sanitize further
    
#     return script

# @app.get("/")
# async def root():
#     """Health check endpoint"""
#     return {"message": "Excel AI Backend is running", "status": "healthy"}

# @app.post("/receive-data")
# async def receive_data(request: Request):
#     """Legacy endpoint - keeping for compatibility"""
#     data = await request.json()
#     logger.info(f"Received data: {data}")
#     return {"status": "success", "data": data}

# @app.options("/parse-command")
# async def parse_command_options():
#     """Handle CORS preflight requests"""
#     return {"message": "OK"}

# @app.post("/parse-command", response_model=CommandResponse)
# async def parse_command(request: CommandRequest):
#     """Main endpoint to process natural language commands"""
    
#     try:
#         logger.info(f"Processing command: {request.input}")
#         logger.info(f"Request context: {request.context}")
        
#         # Validate input
#         command = request.input.strip() if request.input else ""
#         if not command or len(command) < 3:
#             logger.warning(f"Invalid command: '{command}'")
#             raise HTTPException(status_code=400, detail="Command too short or empty (minimum 3 characters)")
        
#         if len(command) > 500:
#             logger.warning(f"Command too long: {len(command)} characters")
#             raise HTTPException(status_code=400, detail="Command too long (max 500 characters)")
        
#         # Create prompt for Cohere
#         prompt = create_cohere_prompt(command, request.context)
#         logger.info(f"Generated Cohere prompt: {prompt[:200]}...")
        
#         # Call Cohere API
#         if not COHERE_API_KEY:
#             logger.info("Using fallback mode (no Cohere API key)")
#             script = generate_fallback_script(command)
#         else:
#             logger.info("Calling Cohere API")
#             generated_script = await call_cohere_api(prompt)
#             script = sanitize_and_validate_script(generated_script)
        
#         if not script:
#             logger.error("Failed to generate valid script")
#             raise HTTPException(status_code=500, detail="Failed to generate valid script")
        
#         logger.info(f"Successfully generated script: {script[:100]}...")
        
#         return CommandResponse(
#             script=script,
#             explanation=f"Generated script for: {command}",
#             status="success"
#         )
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Error processing command: {str(e)}", exc_info=True)
#         raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# def generate_fallback_script(command: str) -> str:
#     """Generate basic scripts for testing when Cohere API is not available"""
    
#     command_lower = command.lower()
    
#     if "sum" in command_lower and "column" in command_lower:
#         return """
# try {
#   const sheet = SpreadsheetApp.getActiveSheet();
#   const range = sheet.getRange('A:A');
#   const values = range.getValues().flat().filter(val => typeof val === 'number');
#   const sum = values.reduce((a, b) => a + b, 0);
#   sheet.getRange('B1').setValue('Sum: ' + sum);
#   return 'Sum calculated: ' + sum;
# } catch (error) {
#   return 'Error: ' + error.message;
# }
# """
    
#     elif "hello" in command_lower or "test" in command_lower:
#         return """
# try {
#   const sheet = SpreadsheetApp.getActiveSheet();
#   sheet.getRange('A1').setValue('Hello from SHEET TALK! 😊');
#   return 'Hello message added to cell A1';
# } catch (error) {
#   return 'Error: ' + error.message;
# }
# """
    
#     else:
#         return f"""
# try {{
#   const sheet = SpreadsheetApp.getActiveSheet();
#   sheet.getRange('A1').setValue('Command received: {command}');
#   return 'Command processed (fallback mode)';
# }} catch (error) {{
#   return 'Error: ' + error.message;
# }}
# """

# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     """Global exception handler for unhandled errors"""
#     logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
#     return {"error": "Internal server error", "status": "error"}


# if __name__ == "__main__":
#     import uvicorn
#     import os
#     port = int(os.getenv("PORT", 8000)) 
#     host = os.getenv("HOST", "0.0.0.0")  
#     print(f"🚀 Starting Excel AI Backend on http://{host}:{port}")
#     print(f"🩺 Health check: http://{host}:{port}/")
#     print(f"📝 API docs: http://{host}:{port}/docs")
#     uvicorn.run(app, host=host, port=port, reload=True)

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from typing import Optional
import logging
import json
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Excel AI Backend", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://talk-sheet-with-me-1.onrender.com",
        "https://script.google.com",
        "https://script.googleusercontent.com",
        "https://*.google.com",
        "https://*.googleusercontent.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8080",
        "http://0.0.0.0:8000",
        "https://api.cohere.ai/v1/chat",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class CommandRequest(BaseModel):
    input: str
    context: Optional[str] = None
    sheet_info: Optional[dict] = None

class CommandResponse(BaseModel):
    script: str
    explanation: Optional[str] = None
    status: str = "success"

class ErrorResponse(BaseModel):
    error: str
    status: str = "error"

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_API_URL = "https://api.cohere.ai/v1/chat"

if not COHERE_API_KEY:
    logger.warning("COHERE_API_KEY not found in environment variables")

async def call_cohere_api(prompt: str) -> str:
    """Call Cohere API to generate Google Apps Script code"""
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "command-r",
        "message": prompt,
        "max_tokens": 500,
        "temperature": 0.3,
        "stop_sequences": ["```", "---"]
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            logger.info(f"Sending Cohere API request with payload: {json.dumps(payload, indent=2)}")
            response = await client.post(COHERE_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            generated_text = result.get("text", "").strip()
            
            if not generated_text:
                logger.warning("Cohere API returned empty text")
                raise HTTPException(status_code=502, detail="Cohere API returned empty response")
                
            logger.info(f"Cohere API response: {generated_text[:100]}...")
            return generated_text
            
        except httpx.TimeoutException:
            logger.error("Cohere API request timed out")
            raise HTTPException(status_code=504, detail="Cohere API timeout")
        except httpx.HTTPStatusError as e:
            logger.error(f"Cohere API error: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=502, detail=f"Cohere API error: {e.response.text}")
        except Exception as e:
            logger.error(f"Unexpected error calling Cohere: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")

def create_cohere_prompt(user_command: str, context: str = None) -> str:
    """Create a well-structured prompt for Cohere API"""
    command = user_command.strip()
    if not command:
        raise ValueError("User command cannot be empty")
    
    base_prompt = f"""
You are an expert in Google Apps Script for Google Sheets. Convert the following natural language command into valid Google Apps Script code that can be executed in a Google Sheets environment. Return only the executable JavaScript code, without explanations, comments, or markdown formatting (e.g., no ```javascript

Command: "{command}"

Context: {context if context else "Working with a Google Sheets spreadsheet"}

Examples:
Command: "Sort the first column in ascending order"
Code: SpreadsheetApp.getActiveSpreadsheet().getActiveSheet().getRange('A:A').sort(1);

Command: "Sum all values in column A"
Code: const sheet = SpreadsheetApp.getActiveSheet(); const rangeA = sheet.getRange('A:A'); const values = rangeA.getValues().flat(); const sum = values.reduce((sum, val) => sum + (val || 0), 0); sheet.getRange('B1').setValue(sum);
"""
    
    return base_prompt.strip()

def sanitize_and_validate_script(script: str) -> str:
    """Basic sanitization and validation of generated script"""
    script = script.replace("```javascript", "").replace("```", "").strip()
    dangerous_patterns = [
        "eval(",
        "Function(",
        "setTimeout(",
        "setInterval(",
        "XMLHttpRequest",
        "fetch(",
        ".deleteSheet(",
        ".deleteRange(",
        "DriveApp.getFiles",
        "GmailApp"
    ]
    for pattern in dangerous_patterns:
        if pattern in script:
            logger.warning(f"Potentially dangerous pattern detected: {pattern}")
    return script

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Excel AI Backend is running", "status": "healthy"}

@app.post("/receive-data")
async def receive_data(request: Request):
    """Legacy endpoint - keeping for compatibility"""
    data = await request.json()
    logger.info(f"Received data: {data}")
    return {"status": "success", "data": data}

@app.options("/parse-command")
async def parse_command_options():
    """Handle CORS preflight requests for /parse-command"""
    return JSONResponse(content={"message": "CORS preflight OK"}, status_code=200)

@app.post("/parse-command", response_model=CommandResponse)
async def parse_command(request: CommandRequest):
    """Main endpoint to process natural language commands"""
    try:
        logger.info(f"Processing command: {request.input}")
        logger.info(f"Request context: {request.context}")
        command = request.input.strip() if request.input else ""
        if not command or len(command) < 3:
            logger.warning(f"Invalid command: '{command}'")
            raise HTTPException(status_code=400, detail="Command too short or empty (minimum 3 characters)")
        if len(command) > 500:
            logger.warning(f"Command too long: {len(command)} characters")
            raise HTTPException(status_code=400, detail="Command too long (max 500 characters)")
        prompt = create_cohere_prompt(command, request.context)
        logger.info(f"Generated Cohere prompt: {prompt[:200]}...")
        if not COHERE_API_KEY:
            logger.info("Using fallback mode (no Cohere API key)")
            script = generate_fallback_script(command)
        else:
            logger.info("Calling Cohere API")
            generated_script = await call_cohere_api(prompt)
            script = sanitize_and_validate_script(generated_script)
        if not script:
            logger.error("Failed to generate valid script")
            raise HTTPException(status_code=500, detail="Failed to generate valid script")
        logger.info(f"Successfully generated script: {script[:100]}...")
        return CommandResponse(
            script=script,
            explanation=f"Generated script for: {command}",
            status="success"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

def generate_fallback_script(command: str) -> str:
    """Generate basic scripts for testing when Cohere API is not available"""
    command_lower = command.lower()
    if "sum" in command_lower and "column" in command_lower:
        return """
try {
  const sheet = SpreadsheetApp.getActiveSheet();
  const range = sheet.getRange('A:A');
  const values = range.getValues().flat().filter(val => typeof val === 'number');
  const sum = values.reduce((a, b) => a + b, 0);
  sheet.getRange('B1').setValue('Sum: ' + sum);
  return 'Sum calculated: ' + sum;
} catch (error) {
  return 'Error: ' + error.message;
}
"""
    elif "hello" in command_lower or "test" in command_lower:
        return """
try {
  const sheet = SpreadsheetApp.getActiveSheet();
  sheet.getRange('A1').setValue('Hello from SHEET TALK! 😊');
  return 'Hello message added to cell A1';
} catch (error) {
  return 'Error: ' + error.message;
}
"""
    else:
        return f"""
try {{
  const sheet = SpreadsheetApp.getActiveSheet();
  sheet.getRange('A1').setValue('Command received: {command}');
  return 'Command processed (fallback mode)';
}} catch (error) {{
  return 'Error: ' + error.message;
}}
"""

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled error: {str(exc)}", exc_info=True)
    return {"error": "Internal server error", "status": "error"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    print(f"🚀 Starting Excel AI Backend on http://{host}:{port}")
    print(f"🩺 Health check: http://{host}:{port}/")
    print(f"📝 API docs: http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port, reload=True)
