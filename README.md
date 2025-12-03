# ai-twitter-bot

An automated Twitter (X) bot that fetches top news in a specified niche, summarizes them into 24 unique tweets, and posts one every hour using free services. Built for autonomy, ensuring operation without user intervention.

## Features
- **News Fetching**: Pulls top headlines from APIs or RSS feeds.
- **AI Summarization**: Uses Hugging Face models for concise, accurate summaries.
- **Unique Tweet Generation**: Ensures 24 diverse tweets per cycle to avoid repetition.
- **Automated Posting**: Hourly posts via cron scheduling on free hosting.
- **Error Handling**: Retries, logging, and alerts for reliability.
- **Free Hosting**: Runs on GitHub Actions with no costs.

## Prerequisites
- Python 3.8+
- GitHub account (for hosting)
- Twitter Developer account (for API access)
- NewsAPI account (free tier)
- Basic knowledge of Python and Git

## Project Structure
ai-twitter-bot/
├── .env  # Environment variables (add to .gitignore)
├── .github/workflows/tweet.yml  # GitHub Actions workflow
├── config.py  # Configuration settings
├── main.py  # Entry point script
├── fetcher.py  # News fetching module
├── summarizer.py  # Summarization module
├── generator.py  # Tweet generation module
├── poster.py  # Posting module
├── queue.py  # Tweet queue management
├── requirements.txt  # Dependencies
├── Dockerfile  # For containerization
└── README.md  # As provided earlier

## Installation
1. Clone the repo: `git clone https://github.com/yourusername/twitter-news-bot.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment: Create a `.env` file with:
    NEWS_API_KEY=your_newsapi_key 
    TWITTER_API_KEY=your_twitter_key 
    TWITTER_API_SECRET=your_twitter_secret 
    TWITTER_ACCESS_TOKEN=your_access_token 
    TWITTER_ACCESS_SECRET=your_access_secret
4. Configure niche: Edit `config.py` for your field (e.g., 'ai').

## Usage
- **Local Testing**: Run `python main.py` to generate and post a test tweet.
- **Deployment**: Push to GitHub; Actions will handle hourly runs.
- **Customization**: Modify `niche` in config for different topics.

## Project Roadmap
### Phase 1: Setup and Research (1-2 days)
- Research and select niche/sources.
- Set up accounts and test APIs manually.
- Install tools and create config files.
- **Details**: Ensure sources are reliable (e.g., no paywalls). Test summarization for accuracy.

### Phase 2: Core Development (3-5 days)
- Build fetcher, summarizer, generator, and poster modules.
- Implement uniqueness checks and error handling.
- **Details**: Use BART model for summaries (max 100 words). Generate tweets with templates like "Latest in [niche]: [summary] #Hashtag". Test for diversity.

### Phase 3: Automation and Hosting (2-3 days)
- Containerize with Docker.
- Set up GitHub Actions workflow with cron (e.g., `0 * * * *`).
- Integrate queue for tweet cycling.
- **Details**: Workflow runs hourly, fetching news if queue empty. Use secrets for keys. Monitor logs in Actions tab.

### Phase 4: Testing and Iteration (1-2 days)
- Run end-to-end tests over 24 hours.
- Fix issues like API errors or duplicates.
- **Details**: Use a test Twitter account. Check logs for failures; iterate on prompts for better uniqueness.

### Phase 5: Maintenance and Expansion (Ongoing)
- Monitor performance and update dependencies.
- Add features like multi-niche support.
- **Details**: Weekly reviews; expand to images or replies if needed.

## Challenges and Mitigations
- API limits: Cycle tweets to stay under 500/day.
- Uniqueness: Similarity thresholds prevent repeats.
- Hosting: Free tiers may throttle; switch to Render if needed.
- Security: Keys in secrets; no logging of sensitive data.

## Contributing
Fork and submit PRs. Ensure tests pass.

## License
MIT License.