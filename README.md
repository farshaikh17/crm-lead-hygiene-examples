# Clean CRM contacts before import

Examples for [CRM Lead Hygiene API](https://rapidapi.com/FarhanShaikh-Rh2lupsG6/api/crm-lead-hygiene-api).

Choose BASIC on the marketplace pricing page, review the subscription and bandwidth terms, and obtain your own RapidAPI application key. Do not use the Worker origin for customer POST calls. No key is included here. Keep your key on a server or in your automation platform's credential store; do not embed it in a public webpage or repository.

Set RAPIDAPI_KEY in your environment, then run `node normalize.mjs` or `python normalize.py`. From this directory, Unix users can run `sh normalize.sh`; Windows users can use curl.exe with the same URL, headers and `--data-binary @contact.json`.

The supplied contact normalizes to `Ana Maria`, `ana@example.com`, `+442079460018`, `GB`, and `https://example.com`. The complete response wraps the result in `{version,result}`; inspect `result.warnings`, `result.validity` and `result.changes` before writing to your CRM. This output is normalization, not proof the mailbox or phone can be reached.

## Routes and workflows

| Method / path | Input | Main output |
|---|---|---|
| POST /v1/contact/normalize | One contact object | result.original, normalized, validity, derived, warnings, changes |
| POST /v1/contact/fingerprint | One contact object | result.fingerprint_version, algorithm, fingerprints, weak_keys, contact |
| POST /v1/contacts/dedupe | {"contacts":[...]} | result.records, duplicates, summary, auto_merged |
| GET /health | None | Status and gateway configuration status |
| GET /v1 | None | Version and limits |
| GET /demo | None | Fixed synthetic example |

1. Export or receive contacts using your own authorized CRM access.
2. Map only relevant fields into the API contact schema: name, first_name, last_name, email, phone, country, website, domain, company, linkedin_url, social_urls.
3. Normalize each form submission before creating/updating a CRM contact. Retain your CRM record ID in your own workflow; unknown fields are preserved only in original and produce warnings.
4. For a supplied batch of 1–20 contacts, call dedupe with duplicates.json as a minimal example. Review pairs in result.duplicates; map each zero-based index back to the original records. Nothing is merged automatically.
5. For an index spanning many batches, call fingerprint per contact and store the versioned matching keys in your own controlled system. Review candidate matches before merging. A name_company key is weak; it does not generate dedupe pairs in the batch endpoint.

**Cross-batch warning:** splitting a CSV into batches does not detect matches across batches. The API never searches your CRM. It has no persistent contact index.

## Generic HTTP automation

In GoHighLevel, HubSpot, Salesforce, Zapier, Make or another system with an HTTP action, map the triggering contact into a JSON object. POST to the normalize route with Content-Type, X-RapidAPI-Key, and X-RapidAPI-Host headers. Store the key in platform credentials. Use a separate, authorized CRM action to write result.normalized only after reviewing validity/warnings. On 400/422 fix input; on 401 check the subscribed key; on 429 respect Retry-After and plan limits; on 5xx retry a small number of times with delay. Normalization is stateless, but your downstream CRM write needs its own duplicate/idempotency safeguards. These are generic patterns, not official native integrations or completed client workflows.

n8n: use Manual Trigger → Edit Fields (synthetic contact) → HTTP Request. Set method POST, URL above, JSON body `{{$json}}`, and use header credentials for X-RapidAPI-Key. Add X-RapidAPI-Host and Content-Type. Return JSON. This recipe has been reviewed against the HTTP contract; a live n8n installation was not available, so no workflow execution is claimed.

## Behavior and limits

Names preserve case and are not split. Email local-part case is preserved; only its domain is lowercased. National phone numbers require a country; valid numbers format as E.164. Recognized tracking parameters are removed from URLs. Duplicate candidates require exact valid normalized email or phone plus extension. Confidence is a fixed heuristic, not a probability. Role mailboxes and conflicting fields need human review. Maximum body 32 KiB; dedupe batch 1–20; field length 2,048; social_urls up to 10 strings; Worker limit 60 requests/minute/subscriber/edge location, with additional marketplace limits.

No application contact storage, external enrichment, deliverability checks, automatic merges, or CRM search. Fingerprints are deterministic matching identifiers, not anonymization. Marketplace/infrastructure metadata and customer retention practices are separate; avoid unnecessary personal fields.

As checked October 13, 2026: new BASIC 500 requests/month, PRO $5/10,000, ULTRA $15/100,000, hard request limits. A deprecated BASIC plan with 500,000 requests is visible for the owner; it is not the new-customer allowance. Separate bandwidth allowance 10,240 MB/month then $0.001/MB is displayed. Review live terms before subscribing. Full 20-contact batches imply theoretical maxima of 10,000/200,000/2,000,000 contact appearances respectively, if one batch call counts as one request; metering has not been independently measured. Batches can repeat contacts and cannot replace a global index.

## Validation status

Current owner Hub tests: normalize, fingerprint and 20-contact dedupe return 200. See the accompanying audit for exact results and remaining checks. Example client transport tests use a local adapter against the checkpoint bundle; these are separate from live customer gateway verification. Never treat owner tests as customer traction.

Original example code is MIT licensed. This repository should contain example files only; never publish the private evidence/checkpoint bundle or backend source.
