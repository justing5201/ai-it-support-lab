# Suspected Phishing Email

## Purpose

Use this procedure when a user reports an unexpected or suspicious email, message, link, attachment, sign-in request, or request for sensitive information.

The purpose of Tier 1 handling is to reduce additional interaction with the message, collect relevant information, determine whether the user interacted with it, and route potential security incidents for appropriate review.

## Common Indicators

Reported indicators may include:

- unexpected links or attachments;
- requests for passwords, credentials, financial information, or other sensitive data;
- sender addresses that do not match the claimed organization;
- unexpected authentication requests;
- urgent or threatening language;
- messages designed to imitate a trusted organization or service.

The presence or absence of any single indicator does not by itself prove that a message is malicious.

## User-Safe Actions

1. Tell the user not to click links or open attachments in the suspicious message.
2. Tell the user not to reply to the sender.
3. Instruct the user to report the message using the organization's approved phishing-reporting method, if one exists.
4. Ask whether the user clicked a link.
5. Ask whether the user opened or executed an attachment.
6. Ask whether the user entered credentials or other sensitive information.
7. Ask whether the user approved an unexpected MFA or authentication request.
8. Advise the user not to continue interacting with the suspicious message.

Do not ask the user to send their password, MFA code, or other authentication secret as part of the investigation.

## Technician Actions

Record:

- sender address;
- message subject;
- approximate time received;
- recipient;
- whether a link was clicked;
- whether an attachment was opened or executed;
- whether credentials or sensitive information were entered;
- whether an unexpected MFA request was approved;
- whether similar messages have been reported by other users.

Follow the organization's approved security-reporting process for handling the reported message and collected information.

Do not independently perform containment or account-remediation actions unless those actions are explicitly authorized by organizational procedure.

## Human Review Required

Require security or designated human review when:

- the user clicked a suspicious link;
- an attachment was opened or executed;
- credentials or sensitive information were entered;
- an unexpected MFA request was approved;
- suspicious account activity is reported;
- multiple users received the same suspicious message;
- malware execution or device compromise is suspected;
- the message targets privileged, financial, or other sensitive access;
- the legitimacy of the message cannot be established through the approved process.

A suspected phishing report may still require review even when the user did not interact with the message, according to organizational policy.

## Resolution Criteria

Tier 1 handling is complete when:

- the user's interaction with the message has been established;
- required information has been recorded;
- the message has been reported through the approved process; and
- any required security escalation has been initiated.

Do not mark a suspected compromise as resolved solely because the suspicious email was deleted.