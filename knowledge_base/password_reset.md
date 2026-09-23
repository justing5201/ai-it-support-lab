# Password Reset and Account Lockout

## Purpose

Use this procedure when a user reports:

- a forgotten organizational password;
- an account lockout;
- inability to authenticate with a known account;
- repeated authentication failures that may be related to the user's account.

This procedure does not define the organization's identity-verification process. Identity verification and administrative password resets must follow the organization's approved authentication and account-recovery procedures.

## Initial Information to Collect

Record:

- User-reported issue
- Exact error message
- Service or application affected
- Whether other organizational services are accessible
- Whether the user recently changed their password
- Whether the account appears locked, disabled, or simply rejects authentication
- Whether the user reports unexpected authentication activity

Never request:

- the user's current password;
- a new password chosen by the user;
- MFA verification codes;
- recovery codes;
- authenticator secrets.

## User-Safe Troubleshooting

1. Ask the user to stop repeated authentication attempts if the account appears to be locked.
2. Obtain the exact error message displayed.
3. Determine whether the issue affects one application or multiple organizational services.
4. If the organization provides Microsoft Entra Self-Service Password Reset (SSPR), direct the user to the organization's approved SSPR process.
5. Allow the approved authentication or recovery process to verify the user's identity. Do not substitute informal questions or personally known information for the approved process.

## Technician Troubleshooting

1. Follow the organization's approved identity-verification procedure before performing an administrative account recovery or password reset.
2. Using approved administrative tools, determine whether the account is locked, disabled, or otherwise restricted.
3. Review relevant authentication failures when available and authorized.
4. Determine whether the problem began after a password change.
5. Follow the organization's approved password-reset or account-unlock procedure if Tier 1 is authorized to perform the action.
6. Record the administrative action and outcome in the ticket.

## Security Review Conditions

Require additional review when:

- the user's identity cannot be verified using the approved process;
- the user reports authentication attempts they did not initiate;
- unexpected MFA prompts are reported;
- suspicious sign-in activity is identified;
- the account repeatedly becomes locked after access is restored;
- account recovery is required because the user has lost access to all registered authentication methods;
- the account appears disabled or restricted for a reason that Tier 1 cannot determine.

Do not bypass identity-verification controls to restore access.

## Escalation Criteria

Escalate when:

- identity verification cannot be completed;
- Tier 1 does not have authorization to perform the required account action;
- suspicious authentication activity is present;
- administrative systems indicate an account condition outside Tier 1 scope;
- the approved reset or unlock process fails;
- the issue remains unresolved after the documented procedure.

## Resolution Criteria

The incident may be considered resolved when:

- the approved authentication or recovery process has been completed;
- the user can successfully authenticate to the affected organizational service; and
- no unresolved security concern remains.

Document the action taken without recording passwords, MFA codes, or other authentication secrets.