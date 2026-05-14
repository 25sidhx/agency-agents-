# Hermes Automation Context

**User:** Siddhant (Digital Marketing, Opus agency)
**VM:** Azure (20.244.40.133)
**Platform:** Telegram

---

## Active Projects

### Trend Monitoring (Twitter API)
- **API:** twitterapi.io
- **Key:** `new1_d5a9e99808f3459cb280f3e16c1edcdc` (in `.env`)
- **Schedule:** every 6h (configurable)
- **Output:** 5-item digest sent to Telegram
- **Status:** pending implementation

---

## Telegram Integration
- **Chat ID:** (to be supplied)
- **Delivery:** via `messaging` toolset
- **Home channel:** default

---

## Hermes Config Notes
- **Provider:** stepfun-ai/step-3.5-flash (Nvidia)
- **Gateway:** running
- **Memory:** enabled
- **Toolsets:** web, terminal, file, browser, messaging

---

## API Keys Stored
```
TWITTER_API_KEY=new1_d5a9e99808f3459cb280f3e16c1edcdc
# add others as we go
```

---

## Cron Jobs
List created jobs via `hermes cron list`

---

## Next Steps
1. Confirm keywords/niches for trend monitoring
2. Provide Telegram chat ID (if not home channel)
3. Test Twitter API script
4. Create cron job with 6h schedule
5. Add additional automations (competitor scan, weekly digest, etc.)

---

*Auto-updated by Hermes*