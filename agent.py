import asyncio
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
)
from livekit.plugins import groq, silero, deepgram, cartesia
from livekit import rtc

# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")

# Get LiveKit credentials from environment
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET") 
LIVEKIT_URL = os.getenv("LIVEKIT_URL")

# Set LiveKit credentials in environment
if LIVEKIT_API_KEY:
    os.environ["LIVEKIT_API_KEY"] = LIVEKIT_API_KEY
if LIVEKIT_API_SECRET:
    os.environ["LIVEKIT_API_SECRET"] = LIVEKIT_API_SECRET
if LIVEKIT_URL:
    os.environ["LIVEKIT_URL"] = LIVEKIT_URL

# Set API keys in environment
if GROQ_API_KEY:
    os.environ["GROQ_API_KEY"] = GROQ_API_KEY
if DEEPGRAM_API_KEY:
    os.environ["DEEPGRAM_API_KEY"] = DEEPGRAM_API_KEY
if CARTESIA_API_KEY:
    os.environ["CARTESIA_API_KEY"] = CARTESIA_API_KEY

@function_tool
async def provide_mental_health_support(
    context: RunContext,
    user_concern: str,
    emotional_state: str = "neutral",
):
    """Provides mental health support and coping strategies for stress, anxiety, and emotional concerns."""
    
    # Define coping strategies based on concern type
    coping_strategies = {
        "anxiety": [
            "Try the 4-7-8 breathing technique: breathe in for 4, hold for 7, exhale for 8",
            "Practice grounding with the 5-4-3-2-1 technique: 5 things you see, 4 you touch, 3 you hear, 2 you smell, 1 you taste",
            "Consider progressive muscle relaxation starting from your toes and working up",
            "Remember that anxiety is temporary and this feeling will pass"
        ],
        "stress": [
            "Take a 5-minute break to do some deep breathing exercises",
            "Try breaking down overwhelming tasks into smaller, manageable steps",
            "Consider going for a short walk or doing light stretching",
            "Practice mindfulness by focusing on the present moment"
        ],
        "depression": [
            "Remember that you're not alone and these feelings are valid",
            "Try to engage in one small activity you usually enjoy",
            "Consider reaching out to a trusted friend or family member",
            "Gentle movement like a short walk can sometimes help improve mood"
        ],
        "overwhelm": [
            "List your priorities and focus on just one thing at a time",
            "Practice saying 'no' to additional commitments when possible",
            "Try the 'two-minute rule': if something takes less than 2 minutes, do it now",
            "Remember that it's okay to ask for help when you need it"
        ]
    }
    
    # Determine which strategies to suggest based on the concern
    concern_lower = user_concern.lower()
    relevant_strategies = []
    
    for concern_type, strategies in coping_strategies.items():
        if concern_type in concern_lower:
            relevant_strategies.extend(strategies[:2])  # Take first 2 strategies
    
    # If no specific match, provide general strategies
    if not relevant_strategies:
        relevant_strategies = [
            "Take a moment to breathe deeply and ground yourself",
            "Remember that it's okay to feel what you're feeling",
            "Consider talking to someone you trust about what you're experiencing"
        ]
    
    return {
        "support_type": "mental_health_guidance",
        "coping_strategies": relevant_strategies,
        "reminder": "These are general wellness suggestions. For persistent concerns, please consider speaking with a mental health professional.",
        "crisis_note": "If you're having thoughts of self-harm, please reach out to a crisis helpline immediately."
    }

async def entrypoint(ctx: JobContext):
    print("🧠 LiveKit Mental Health Support Agent Starting...")
    print("🔧 Development Mode - No Cloud Connection Required")
    print("🌐 Connect via: https://agents-playground.livekit.io/")
    print("📊 Agent URL: http://localhost:60931/debug")
    print("💚 Providing empathetic support for emotional wellness")
    print("=" * 60)
    
    await ctx.connect()
    
    # Configure providers based on available API keys
    print("\n🔧 Configuring providers...")
    
    # STT Configuration (prefer Deepgram for better performance)
    if DEEPGRAM_API_KEY:
        stt_provider = deepgram.STT(model="nova-2")
        print("   ✅ Using Deepgram for STT")
    else:
        stt_provider = groq.STT()
        print("   ✅ Using Groq for STT")
    
    # TTS Configuration (prefer Cartesia for better quality, then Groq)
    if CARTESIA_API_KEY:
        tts_provider = cartesia.TTS()  # Use default voice
        print("   ✅ Using Cartesia for TTS")
    else:
        tts_provider = groq.TTS(model="playai-tts")
        print("   ✅ Using Groq for TTS")
    
    # LLM Configuration (Groq for fast inference)
    llm_provider = groq.LLM(model="llama-3.3-70b-versatile")
    print("   ✅ Using Groq for LLM")

    agent = Agent(
        instructions="""
            You are Ellie a compassionate and empathetic mental health support voice assistant.
            
            Your primary role is to:
            - Listen actively and respond with empathy to users experiencing stress, anxiety, or emotional difficulties
            - Provide emotional validation and normalize feelings
            - Offer practical coping strategies and grounding techniques
            - Encourage self-care and professional help when appropriate
            - Maintain a warm, non-judgmental, and supportive tone
            
            Key guidelines:
            - Always validate the user's feelings and experiences
            - Use active listening phrases like "I hear that you're feeling..." or "That sounds really difficult"
            - Keep responses concise but meaningful for voice interaction
            - Offer specific, actionable coping strategies when appropriate
            - Remind users that seeking professional help is a sign of strength
            - Never provide medical advice or attempt to diagnose
            - If someone mentions self-harm or crisis, gently guide them to professional resources
            - Use the provide_mental_health_support tool when users express stress, anxiety, or emotional concerns
            
            Communication style:
            - Speak in a calm, soothing voice
            - Use person-first language
            - Be present and focused on the user's immediate needs
            - Ask gentle follow-up questions to better understand their situation
            - Offer hope and remind them that feelings are temporary
            
            Start by greeting the user warmly and letting them know this is a safe space to share how they're feeling.
            """,
        tools=[provide_mental_health_support],
    )
    
    session = AgentSession(
        vad=silero.VAD.load(
            min_speech_duration=0.1,
            min_silence_duration=0.5,
        ),
        stt=stt_provider,
        llm=llm_provider,
        tts=tts_provider,
    )

    print("\n🚀 Agent ready! Waiting for connections...")
    print("🌐 Connect via: https://agents-playground.livekit.io/")
    print("📊 Debug info: http://localhost:60931/debug")
    
    await session.start(agent=agent, room=ctx.room)
    
    # Generate initial greeting
    await session.generate_reply(
        instructions="Greet the user warmly and let them know this is a safe space where they can share how they're feeling. Ask gently how you can support them today. Keep it brief, compassionate, and welcoming."
    )


if __name__ == "__main__":
    print("🧠 LiveKit Mental Health Support Agent - Local Development Mode")
    print("=" * 60)
    print("🔧 Running in local mode (loading from .env file)")
    print("🌐 Connect via: https://agents-playground.livekit.io/")
    print(" Providing empathetic support for stress, anxiety, and emotional wellness")
    print("")
    
    # Validate API keys
    if not GROQ_API_KEY:
        print("⚠️  ERROR: GROQ_API_KEY not found in .env file!")
        print("   Please add your Groq API key to the .env file")
        print("   Get one at: https://console.groq.com/keys")
        exit(1)
    
    if not DEEPGRAM_API_KEY:
        print("ℹ️  INFO: DEEPGRAM_API_KEY not set - will use Groq for STT")
    
    if not CARTESIA_API_KEY:
        print("ℹ️  INFO: CARTESIA_API_KEY not set - will use Groq for TTS")
    
    print("")
    print("🚀 Starting mental health support agent...")
    print("💡 Remember: This agent provides general wellness support.")
    print("   For professional help, please consult a licensed mental health provider.")
    
    # Check if dev command was provided, if not, add it
    import sys
    if len(sys.argv) == 1:
        # No command provided, add 'dev' automatically
        sys.argv.append('dev')
        print("📝 Auto-adding 'dev' command for development mode")
    
    # Use the standard LiveKit CLI
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))