
  Essential Starter Commands for 
  edge-assistant

  🚀 Quick Setup & Help

  # Get help and see all available commands
  edge-assistant --help

  # Get help for specific commands
  edge-assistant analyze --help
  edge-assistant research --help

  🎯 Unified Multimodal Analysis 
  (Recommended)

  # Simple text analysis
  edge-assistant analyze "Explain the key 
  principles of clean code"

  # Analyze an image
  edge-assistant analyze "What do you see in
   this image?" --file screenshot.png

  # Analyze a PDF document  
  edge-assistant analyze "Summarize the key 
  findings" --file report.pdf

  # Start a threaded conversation (maintains
   context)
  edge-assistant analyze "What are 
  microservices?" --thread learning
  edge-assistant analyze "What are their 
  pros and cons?" --thread learning

  🔍 Web Research

  # Research current topics with citations
  edge-assistant research "latest AI 
    developments 2025"
  edge-assistant research "best practices 
  for API design"
  edge-assistant research "Python 
  performance optimization techniques"

  💬 Interactive Conversations

  # Simple chat with threading
  edge-assistant ask "Explain REST vs 
  GraphQL" --thread api-design
  edge-assistant ask "Which should I choose 
  for my project?" --thread api-design

  # With custom system instructions
  edge-assistant ask "Review this code 
  architecture" --system "You are a senior 
  software architect"

  📚 Knowledge Base Management

  # Index your local documentation
  edge-assistant kb-index ./docs ./README.md
   ./notes

  # Search your indexed knowledge
  edge-assistant kb-research "How to 
  implement authentication?"
  edge-assistant kb-research "deployment 
  best practices"

  ✏️ Safe File Editing

  # Preview changes first (dry-run by 
  default)
  edge-assistant edit README.md "Add a 
  troubleshooting section"

  # Apply changes after reviewing the diff
  edge-assistant edit README.md "Add 
  installation instructions" --apply

  🛠️ Agent Mode with Tools

  # Tool-calling AI with approval workflow
  edge-assistant agent "Create a Python 
  script to process CSV files" --approve
  edge-assistant agent "Analyze my project 
  structure and suggest improvements"

  🎨 Advanced Multimodal Workflows

  # Mixed content analysis with threading
  edge-assistant analyze "What safety issues
   do you see?" --file facility.jpg --thread
   safety-review --system "You are a safety 
  inspector"
  edge-assistant analyze "Review this safety
   report" --file safety-report.pdf --thread
   safety-review
  edge-assistant analyze "What are your 
  final recommendations?" --thread
  safety-review

  # Document + image analysis
  edge-assistant analyze "Extract key data 
  from this chart" --file chart.png --thread
   data-analysis
  edge-assistant analyze "How does this 
  relate to the research paper?" --file
  paper.pdf --thread data-analysis

  📊 Thread Management

  # Check thread status and content 
  breakdown
  edge-assistant analyze "Status check"
  --thread my-session

  # Clear a specific thread
  edge-assistant analyze --clear-thread
  --thread my-session

  # Set custom interaction limits
  edge-assistant analyze "Question" --thread
   long-session --max-interactions 50

  🔧 Testing & Verification

  # Test the installation
  edge-assistant analyze "Hello! Is 
  everything working?"

  # Test file analysis
  edge-assistant analyze "What type of file 
  is this?" --file ./README.md

  # Test web research
  edge-assistant research "current weather 
  OpenAI API"

  💡 Pro Tips Commands

  # Force specific content type
  edge-assistant analyze "Analyze as image"
  --file diagram.pdf --type image

  # Use specific model
  edge-assistant analyze "Complex reasoning 
  task" --model gpt-4o

  # Combine system prompt with threading
  edge-assistant analyze "Review this code"
  --file app.py --thread code-review
  --system "You are a senior developer 
  focusing on security and performance"