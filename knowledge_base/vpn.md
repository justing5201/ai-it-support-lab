# VPN Connection and Authentication Troubleshooting

## Purpose

Use this procedure for support requests involving an inability to connect to the corporate VPN, repeated authentication failures, unexpected disconnects, or other GlobalProtect connection errors.

This procedure covers initial Tier 1 troubleshooting only. VPN access policies, authentication configuration, and authorization requirements are organization-specific and must not be assumed.

## Initial Information to Collect

Record:

- User-reported issue
- Exact error message
- When the issue began
- Whether the issue previously worked
- Whether general internet access is working
- Whether the user can sign in to other organizational services
- Whether the problem occurs on another network, if one is safely available
- Whether other users are reporting similar symptoms

Do not request the user's password, MFA code, recovery code, or other authentication secret.

## User-Safe Troubleshooting

1. Confirm the device has a working internet connection before troubleshooting the VPN.
2. Completely close the GlobalProtect application and reopen it.
3. Ask the user to attempt the connection again and provide the exact error message displayed.
4. Confirm whether the user can authenticate normally to other organizational services using their work account.
5. If practical, determine whether the same problem occurs from another trusted internet connection.
6. If the VPN client or device has not recently been restarted, have the user save their work and restart the device before testing again.

## Technician Troubleshooting

1. Review the information collected from the user and determine whether the failure appears related to connectivity, authentication, or the VPN client.
2. Verify that the endpoint has normal network connectivity before investigating the VPN service.
3. Check the organization's approved service-health or incident source for known VPN or authentication outages, if available.
4. Determine whether the issue affects one user or multiple users.
5. Review GlobalProtect troubleshooting or diagnostic logs when available and permitted by organizational procedure.
6. Verify account, VPN authorization, device-compliance, or access requirements only through the organization's approved administrative systems and procedures.
7. Record relevant error messages and diagnostic findings in the ticket.

## Escalation Criteria

Escalate for further investigation when:

- multiple users report the same VPN failure;
- the VPN service or authentication infrastructure may be unavailable;
- the user's account or VPN authorization requires an administrative change outside Tier 1 authority;
- device access or compliance requirements cannot be verified or corrected by Tier 1;
- GlobalProtect logs indicate a problem outside Tier 1 scope;
- the issue continues after the documented Tier 1 troubleshooting steps;
- the available documentation does not adequately address the observed error.

## Resolution Criteria

The incident may be considered resolved when:

- the user can successfully establish the required VPN connection; and
- the user confirms the required corporate resource is accessible.

Document the troubleshooting performed and the final outcome before closing the ticket.