# book-api-bedrock-throttles

## Meaning
Amazon Bedrock rejected one or more `GET /books/{book_id}/summary` calls with HTTP 429 in the last minute.

## Impact
Readers who ask for a book summary get an error. The book list, details and edits still work.

## Diagnosis
1. Count throttles for every model, with no dimension filter. A non-zero Sum confirms throttling:
   `aws cloudwatch get-metric-statistics --namespace AWS/Bedrock --metric-name InvocationThrottles --statistics Sum --period 60 --start-time <15 minutes ago> --end-time <now>`
2. Read the model's tokens-per-minute quota in this account and Region:
   `aws service-quotas list-service-quotas --service-code bedrock --query "Quotas[?contains(QuotaName, 'tokens per minute')]"`
3. Search the app logs for `ThrottlingException`. Many calls at once: cause A, a burst.
   Steady calls near the quota: cause B, the quota is too low.

## Fix
- Cause A, a burst: confirm the SDK retries with backoff (`AWS_MAX_ATTEMPTS`, `AWS_RETRY_MODE=adaptive`), then lower the route's concurrency.
- Cause B, the quota is too low: request a quota increase for the model in this Region, with the measured peak tokens per minute.

## Verify
The alarm returns to `OK`, and `InvocationThrottles` Sum is 0 for 5 periods.
Then run `uv run scripts/smoke_test_cli.py --base-url <the app's URL>`. Every line must read `PASS`.

## Escalation
If the alarm is still in `ALARM` after 30 minutes, contact the delivery team's on-call engineer.
Send the alarm name, the time it fired, the Sum from diagnosis step 1 and the quota from step 2.
