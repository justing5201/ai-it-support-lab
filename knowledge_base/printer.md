# Windows Printer and Printing Issues

## Purpose

Use this procedure when a Windows user reports that:

- a printer appears offline;
- documents remain in the print queue;
- printing does not start;
- Windows cannot communicate with a known printer;
- printing works for other users but not the affected workstation.

This procedure covers initial workstation and printer troubleshooting. Printer-server, network, access-control, and hardware procedures depend on the organization's environment.

## Initial Information to Collect

Record:

- Printer name or identifier
- User and affected workstation
- Reported printer status
- Exact error message, if present
- Whether the problem affects one user or multiple users
- Whether other users can print to the same printer
- Whether the user can print to another available printer
- Whether the issue affects one application or all applications

## User-Safe Troubleshooting

1. Confirm that the intended printer is selected in the application.
2. Confirm that the printer is powered on.
3. Check the printer display for visible error conditions such as offline status, paper problems, or other warnings.
4. Ask whether other users can currently print to the same printer.
5. Ask the user to close and reopen the application from which they are attempting to print.
6. If appropriate, have the user save their work and restart the workstation.
7. Test printing again and record any error displayed.

Do not instruct the user to modify Windows services, drivers, system files, or printer-server configuration unless the organization explicitly permits that action.

## Technician Troubleshooting

1. Determine whether the issue is isolated to the workstation or affects multiple users.
2. Verify that Windows is using the intended printer.
3. Open the Windows print queue and check for failed or stuck jobs.
4. Verify the status of the Windows Print Spooler service.
5. Restart the Print Spooler when appropriate and authorized.
6. Verify that the workstation can communicate with the printer or print service using the organization's approved diagnostic method.
7. Check for printer-driver errors or incompatible/outdated drivers.
8. Remove and reinstall the printer only when appropriate and permitted by organizational procedure.
9. Record errors and actions taken in the ticket.

## Escalation Criteria

Escalate when:

- multiple users cannot print to the same printer;
- the printer or print service is unreachable from multiple workstations;
- a printer-server or network infrastructure problem is suspected;
- a driver or configuration change requires privileges outside Tier 1 authority;
- the physical printer reports a hardware condition that cannot be resolved through approved basic troubleshooting;
- the issue repeatedly returns after documented remediation;
- the documented Tier 1 procedure does not resolve the problem.

## Resolution Criteria

The incident may be considered resolved when:

- the user can successfully submit a print job;
- the expected document is produced by the intended printer; and
- no related error remains.

Document the successful test and the action that resolved the incident.