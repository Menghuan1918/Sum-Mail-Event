# Sum-Mail-Event

English | [中文](README_CN.md)

This project aims to filter emails using local LLM to extract only events/notification/urgent emails that are relevant to the user (custom portrait). 

Currently in the start-up phase.

TODO:
- [x] Mail reading section
- [x] OCR section
- [x] Message Body Processing section
- [ ] LLM Processing Mail section
    - [x] LLM event classification (judgement) module
    - [x] LLM Summary Module
    - [ ] LLM Text Extraction Module
- [ ] Sending Reminder section
- [ ] Complete the entire workflow

## Planned processing flow

```mermaid
graph TD
    A[programme running] --> B[update mail]
    B --> C{mail format}
    C --> |Text format| D[Direct dumping]
    C --> |HTML format| E[Extract Plain Text]
    B --> F[Attachment/Inline Image Handling]
    F --> G{File Type}
    G --> |Image| H[OCR Recognition]
    H --> I[Recognise content to be added to text]
    G -->|Other| J[Not processed for now]
    A --> K[mail type judgement]
    K -->|Notification/Event Mail| L{Is relevant to user profile}
    L -->|Yes| M{Is it urgent}
    M -->|Yes| N[Extract key content]
    M -->|No| O[Extract Key Content]
    L -->|No| P[Ignore]
    K -->|spam| Q[Extract key content]
    A --> R[Notify User]
    R --> S{urgency}
    S -->|Urgent| T[Notify Immediately]
    S --> |non-urgent| U[aggregate notification]
    N --> V[store key content]
    O --> V
    Q --> V
    T -->|Read critical content| W[Send notification]
    U -->|by set rule| W
```

- Run the main programme every so often:

    - Updates messages (pulls the latest X messages)

    - Preprocess messages
        - Full text: dump directly if it is text, extract plain text if it is HTML.
        - Attachments and embedded images:
            - For images, add the recognised content to the dumped text after OCR.
            - For other documents, it will not be processed for the time being.

    - Determine the type of emails: notification emails/event emails/spam emails.

        - Notification mail/event mail:
            - Whether it is related to user-defined image
                - Related:
                    - Determine whether the email is urgent (need to reply/know in time).
                - Extract key contents of emails and store them locally
        - Spam:
            - Extracts the key content of the email and stores it locally (to prevent LLM from misjudging it, so it will still appear in the summary)

    - Notify users
        - Tentatively, this will be in the form of an email to a customised email address.
        - If the email is urgent, the key content of the email will be read and notified immediately.
        - If it is not urgent, it will be notified every X emails/period of time.