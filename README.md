# LiveKit Voice Agent with Metrics Logging

A sophisticated AI voice agent built with LiveKit that supports real-time voice conversations with comprehensive metrics logging and latency optimization.

## Features

🎙️ **Real-time Voice Pipeline**
- Speech-to-Text (STT) with Deepgram or Groq
- Large Language Model (LLM) with Groq (Llama 3.3)
- Text-to-Speech (TTS) with ElevenLabs or Groq
- Voice Activity Detection (VAD) with Silero

📊 **Comprehensive Metrics Logging**
- End-of-Utterance (EOU) delay tracking
- Time to First Token (TTFT) measurement
- Time to First Byte (TTFB) measurement
- Total latency monitoring
- Interruption counting
- Session summaries saved to Excel

🚀 **Performance Optimized**
- Target latency: < 2 seconds
- Optimized provider selection
- Real-time metrics monitoring
- Graceful interruption handling

## Quick Start

### 1. Setup Environment

```bash
# Install dependencies
python setup.py

# Or manually:
pip install -r requirements.txt
```

### 2. Configure API Keys

Create `.env.local` file with your API keys:

```env
# Required
GROQ_API_KEY=your-groq-api-key

# Optional (recommended for better quality)
DEEPGRAM_API_KEY=your-deepgram-api-key
ELEVENLABS_API_KEY=your-elevenlabs-api-key

# For deployment (optional)
LIVEKIT_URL=wss://your-livekit-url
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret
```

### 3. Get API Keys

#### Groq (Required - Free Tier)
1. Visit [Groq Console](https://console.groq.com/keys)
2. Sign up and create an API key
3. Add to `.env.local`: `GROQ_API_KEY=your-key`

#### Deepgram (Optional - Free Tier)
1. Visit [Deepgram Console](https://console.deepgram.com/)
2. Sign up and get API key
3. Add to `.env.local`: `DEEPGRAM_API_KEY=your-key`

#### ElevenLabs (Optional - Trial)
1. Visit [ElevenLabs](https://elevenlabs.io/)
2. Sign up and get API key
3. Add to `.env.local`: `ELEVENLABS_API_KEY=your-key`

### 4. Run the Agent

```bash
# Start the agent in development mode
python agent.py dev

# Or start with specific options
python agent.py start --room my-room --participant-name VoiceAgent
```

### 5. Test with Agent Playground

1. Open [LiveKit Agent Playground](https://agents-playground.livekit.io/)
2. Connect to your running agent
3. Start a voice conversation
4. Check `session_metrics.xlsx` for performance data

## Architecture

### Voice Pipeline Flow

```
User Speech → STT → LLM → TTS → Agent Speech
     ↓         ↓      ↓      ↓        ↓
  Metrics  Metrics Metrics Metrics Metrics
```

### Metrics Tracked

| Metric | Description | Target |
|--------|-------------|---------|
| EOU Delay | Time from user stops speaking to STT completion | < 200ms |
| TTFT | Time for LLM to generate first token | < 500ms |
| TTFB | Time from TTS start to audio playback | < 300ms |
| Total Latency | End-to-end response time | < 2000ms |
| Interruptions | User interruption count | Minimize |

### Provider Configuration

The agent automatically selects the best available providers:

**STT Priority:**
1. Deepgram Nova-2 (if API key available)
2. Groq STT (fallback)

**TTS Priority:**
1. ElevenLabs (if API key available)
2. Groq TTS (fallback)

**LLM:**
- Groq Llama-3.3-70b-versatile (optimized for speed)

## Usage Examples

### Basic Conversation
```
User: "Hello, how are you?"
Agent: "I'm doing well, thank you! How can I help you today?"
```

### Weather Lookup
```
User: "What's the weather like in New York?"
Agent: "Let me check the weather for you..." (uses lookup_weather tool)
```

### Handling Interruptions
```
User: "Can you tell me about..." [interrupts]
User: "Actually, never mind that. What about..."
Agent: [gracefully handles interruption and responds to new query]
```

## Metrics Analysis

After each session, check `session_metrics.xlsx`:

### Detailed Metrics Sheet
- Per-exchange timing data
- User input and agent responses
- Calculated latencies
- Interruption tracking

### Session Summary Sheet
- Overall session statistics
- Average latencies
- Performance benchmarks
- Quality metrics

### Performance Optimization Tips

1. **Reduce Latency:**
   - Use Deepgram for faster STT
   - Use ElevenLabs for concurrent TTS processing
   - Optimize LLM prompt length

2. **Monitor Metrics:**
   - Check total latency < 2s target
   - Minimize EOU delay
   - Track interruption patterns

3. **Improve Quality:**
   - Use ElevenLabs for better voice quality
   - Optimize agent instructions
   - Handle edge cases gracefully

## Development

### Testing Metrics
```bash
# Test metrics logging functionality
python test_metrics.py
```

### Custom Configuration
```python
# Modify agent.py for custom behavior
agent = Agent(
    instructions="Your custom instructions...",
    tools=[your_custom_tools],
)
```

### Adding New Providers
```python
# Add support for new STT/TTS/LLM providers
from livekit.plugins import your_provider

stt_provider = your_provider.STT(config="your-config")
```

## Troubleshooting

### Common Issues

1. **Agent doesn't start:**
   - Check API keys in `.env.local`
   - Verify dependencies installed
   - Check Python version (3.8+ required)

2. **High latency:**
   - Upgrade to premium API tiers
   - Check network connectivity
   - Monitor system resources

3. **Poor audio quality:**
   - Use ElevenLabs TTS
   - Check microphone/speaker setup
   - Verify audio codecs

### Debug Mode
```bash
# Run with verbose logging
LIVEKIT_LOG_LEVEL=debug python agent.py dev
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Add comprehensive metrics for new features
4. Test latency impact
5. Submit pull request

## License

MIT License - see LICENSE file for details.

## Support

- [LiveKit Documentation](https://docs.livekit.io/)
- [Agent Framework Guide](https://docs.livekit.io/agents/)
- [API References](https://docs.livekit.io/reference/)

---

Built with ❤️ using LiveKit Agents Framework
