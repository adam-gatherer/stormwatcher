# stormwatcher
Weather Risk Pipeline

## 1. Problem Statement

Build a **cloud-native replacement** for a classic Autosys-style batch workflow using AWS services.

The concrete use case:

> Every morning at 06:00, the system fetches today's weather forecast for Edinburgh from a public API.  
> The raw JSON is written to S3 (simulating a file-drop landing zone, like Autosys file transfers).  
> The arrival of that file triggers processing which calculates a simple “weather risk” score and stores it in DynamoDB.  
> A notification is sent to confirm success/failure.  
> A small website reads from DynamoDB and shows today’s risk plus the last 7 days of history.

This doc is the **high-level overview** of that system, suitable for README context, interviews, and further design work.

---