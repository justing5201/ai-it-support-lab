# Windows Workstation Performance Issues

## Purpose

Use this procedure when a user reports that a Windows workstation is unusually slow, applications take significantly longer than expected to open, the system frequently becomes unresponsive, or overall performance has noticeably degraded.

Performance problems can have many causes. Avoid assuming hardware failure without diagnostic evidence.

## Initial Information to Collect

Record:

- User and workstation
- When the performance problem began
- Whether the entire system or one application is affected
- Whether the issue is constant or intermittent
- Any displayed error messages
- Whether the issue began after a software installation, update, or other known change
- Whether a restart temporarily improves the problem
- Whether other users or devices report similar symptoms

## User-Safe Troubleshooting

1. Ask the user to save all current work.
2. Close applications and browser tabs that are not needed.
3. Restart the workstation.
4. After restart, determine whether the performance issue remains.
5. Determine whether the entire workstation is slow or only one application.
6. Record any error messages or application failures.
7. Ask whether the issue began after a recent known change.

Do not instruct the user to disable security software, remove system files, modify Windows services, or make administrative configuration changes.

## Technician Troubleshooting

1. Open Task Manager and review CPU, memory, disk, and application resource utilization.
2. Identify processes consistently consuming unusually high system resources.
3. Check available disk space.
4. Review startup applications when startup or persistent background activity appears relevant.
5. Check Windows Update status and relevant optional driver updates.
6. Review recently installed applications or updates when the reported timeline suggests a relationship.
7. Review relevant system or application errors when available.
8. Follow the organization's approved endpoint-security procedure if malware or unwanted software is suspected.
9. Determine whether the device hardware and available resources are adequate for the required workload.
10. Record significant diagnostic findings in the ticket.

Do not terminate unfamiliar security, management, or business-critical processes without determining their purpose and following organizational procedure.

## Escalation Criteria

Escalate when:

- hardware failure is suspected;
- persistent resource exhaustion cannot be explained or corrected by Tier 1;
- storage health or other hardware diagnostics indicate a potential failure;
- malware or endpoint compromise is suspected;
- operating-system corruption is suspected;
- administrative remediation exceeds Tier 1 authority;
- multiple devices show the same performance problem;
- the issue continues after documented Tier 1 troubleshooting.

## Resolution Criteria

The incident may be considered resolved when:

- the identified cause has been addressed using an approved action;
- the workstation returns to acceptable performance for the user's normal workload; and
- the user confirms that the original performance problem is no longer occurring.

Document the identified cause when known, actions performed, and the user's confirmation.