# 🧠 Mental Health Support Voice Agent

A compassionate AI-powered voice assistant built with LiveKit that provides real-time mental health support, coping strategies, and emotional wellness guidance through natural voice conversations.

## ✨ Features

- **🎙️ Real-time Voice Interaction**: Natural conversation flow with advanced speech-to-text and text-to-speech
- **💚 Mental Health Support**: Specialized in providing coping strategies for anxiety, stress, depression, and overwhelm  
- **🔧 Multiple AI Provider Support**: Flexible configuration with Groq, Deepgram, and Cartesia
- **🛡️ Safe & Empathetic**: Non-judgmental, validating responses with crisis intervention guidance
- **🌐 Web-based Interface**: Easy access through LiveKit's agents playground
- **🔒 Secure**: Environment-based API key management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- API keys for at least one of the supported providers (see [API Keys Setup](#api-keys-setup))

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd VoiceAgent
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys (see below)
   ```

5. **Run the agent**
   ```bash
   python agent.py
   ```

6. **Connect to the agent**
   - Open [LiveKit Agents Playground](https://agents-playground.livekit.io/)
   - Connect to your local agent
   - Start a voice conversation!

## 🔑 API Keys Setup

Create a `.env` file in the project root with the following keys:

```env
# Required - At least one LLM provider
GROQ_API_KEY=your_groq_api_key_here

# Optional - For better STT quality
DEEPGRAM_API_KEY=your_deepgram_api_key_here

# Optional - For better TTS quality  
CARTESIA_API_KEY=your_cartesia_api_key_here

# LiveKit credentials (for production deployment)
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
LIVEKIT_URL=your_livekit_url
```

### Where to get API keys:

- **Groq** (Required): [console.groq.com/keys](https://console.groq.com/keys)
- **Deepgram** (Optional): [console.deepgram.com](https://console.deepgram.com)
- **Cartesia** (Optional): [cartesia.ai](https://cartesia.ai)
- **LiveKit** (For production): [livekit.io](https://livekit.io)

## 🏗️ Architecture

### AI Provider Stack
- **LLM**: Groq (Llama 3.3 70B) for fast, empathetic responses
- **STT**: Deepgram Nova-2 (fallback to Groq) for accurate speech recognition
- **TTS**: Cartesia (fallback to Groq) for natural voice synthesis
- **VAD**: Silero for voice activity detection

### Core Components
- **Agent Core**: LiveKit Agents framework for real-time communication
- **Mental Health Tools**: Specialized function tools for coping strategies
- **Session Management**: Handles voice conversations and context

## 🧰 Available Mental Health Tools

The agent includes a specialized `provide_mental_health_support` function that offers:

### Anxiety Support
- 4-7-8 breathing technique
- 5-4-3-2-1 grounding exercise
- Progressive muscle relaxation
- Reassurance and validation

### Stress Management
- Deep breathing exercises
- Task breakdown strategies
- Movement and mindfulness suggestions
- Present-moment focus techniques

### Depression Support
- Emotional validation
- Gentle activity suggestions
- Social connection encouragement
- Mood improvement strategies

### Overwhelm Relief
- Priority management
- Boundary setting guidance
- Two-minute rule implementation
- Help-seeking normalization

## 💬 Usage Examples

### Starting a Conversation
The agent greets users with warmth and creates a safe space for sharing:

> "Hello! I'm Ellie, and I'm here to provide a safe space where you can share how you're feeling. How can I support you today?"

### Example Interactions
- **User**: "I'm feeling really anxious about my presentation tomorrow"
- **Agent**: Provides breathing techniques, grounding exercises, and reassurance

- **User**: "I'm overwhelmed with everything I need to do"
- **Agent**: Offers task breakdown strategies and stress management techniques

## ⚠️ Important Disclaimers

- **Not a replacement for professional help**: This agent provides general wellness support
- **Crisis situations**: The agent will guide users to professional crisis resources
- **No medical advice**: No diagnosis or medical treatment recommendations are provided
- **Privacy**: Voice conversations are processed in real-time but not stored

## 🛠️ Development

### Project Structure
```
VoiceAgent/
├── agent.py              # Main agent implementation
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (not in git)
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

### Running in Development Mode
```bash
python agent.py dev
```
### Customization
- Modify the `instructions` in `agent.py` to adjust personality
- Add new coping strategies in the `provide_mental_health_support` function
- Configure different AI models by changing provider settings

## 🌐 Deployment

For production deployment:

1. Set up LiveKit Cloud credentials in `.env`
2. Deploy to your preferred platform (AWS, GCP, etc.)
3. Update the connection URL in your client application

### Technical Support
- [LiveKit Documentation](https://docs.livekit.io/)
- [Groq Documentation](https://console.groq.com/docs)
- [Deepgram Documentation](https://developers.deepgram.com/)


*Remember: This agent provides general wellness support. For persistent mental health concerns, please consult with a licensed mental health professional.*
