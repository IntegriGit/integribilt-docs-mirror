> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Role-Based Access Control

Available to [Enterprise Plan](https://www.getzep.com/pricing) customers only.

## Overview

Role-based access control (RBAC) lets you grant the right level of access to each teammate while keeping sensitive account actions limited to trusted users. RBAC grants permissions through roles, and every member can hold multiple assignments across the account and individual projects.

## Scopes and authorizations

RBAC permissions are evaluated at two scopes:

* **Account scope:** Covers organization-wide settings such as member management, billing, and account-level API keys, along with full access to every project.
* **Project scope:** Grants permissions for a single project, including its data plane, collaborators, and project-specific API keys, without exposing other projects or global settings.

Authorizations are grouped into the following capability areas. These appear in the dashboard when you review role details.

* `account.view.readonly` — View account-level configuration, billing status, and usage.
* `rbac.account.manage` — Create, update, or delete account-scoped role assignments, including promoting additional Account Owners.
* `rbac.project.manage` — Manage project-scoped assignments and project-level resources (API keys, data ingestion, deletion) for the projects a member administers.

## Roles

The role catalog includes account-wide roles and project-scoped roles. Assignments can be combined so that, for example, a teammate can be an Account Admin and a Project Viewer on a sensitive project.

### Account-level roles

| Role                | Scope   | Intended for                          | Key authorizations                                                                                                                                                                                                                                                                         |
| ------------------- | ------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Account Owner**   | Account | Founders, security administrators     | `account.view.readonly`, `rbac.account.manage`, `rbac.project.manage`<br />Manage billing and plan settings.<br />Create, update, and archive projects.<br />Rotate account and project API keys.<br />Assign or revoke any role, including other Account Owners.                          |
| **Account Admin**   | Account | Day-to-day operators who run projects | `account.view.readonly`, `rbac.project.manage`<br />Create and manage projects and API keys.<br />Ingest or delete context, documents, and graph data.<br />Assign and revoke project-scoped roles for any project.<br />Cannot remove the last Account Owner or change billing ownership. |
| **Billing Admin**   | Account | Finance or procurement partners       | `billing.manage`<br />View invoices and update payment details.<br />No access to project data or member management.                                                                                                                                                                       |
| **Account Viewer**  | Account | Compliance and audit reviewers        | `account.view.readonly`, `project.data.read`, `apikey.view`<br />Read account details, project metadata, and API keys.<br />Cannot make configuration changes.                                                                                                                             |
| **Project Creator** | Account | Builders who bootstrap new projects   | `project.create`<br />Create new projects from the dashboard.<br />No access to existing projects unless separately assigned.                                                                                                                                                              |

### Project-level roles

| Role               | Scope   | Intended for                                    | Key authorizations                                                                                                                                                                 |
| ------------------ | ------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Project Admin**  | Project | Team leads who manage a single project          | `rbac.project.manage` for the assigned project only.<br />Invite or remove project collaborators.<br />Create and rotate project API keys.<br />Ingest and delete project data.    |
| **Project Editor** | Project | Data engineers or agents that need write access | Read and write all project data, including context, documents, and graph content.<br />Use project API keys to ingest or delete data.<br />Cannot assign roles or manage API keys. |
| **Project Viewer** | Project | Analysts, auditors, or embedded stakeholders    | View project configuration, usage, threads, documents, and graph content.<br />Run read-only queries and exports.<br />Cannot ingest, delete, or manage API keys.                  |

## Managing role assignments

* Use the **Settings ▸ Members** page in the Zep Dashboard to add or remove roles. Search for an existing member or invite a new teammate, then assign any combination of account and project roles.
* Filter by project to focus on project-scoped roles, or view the full access matrix to understand overlapping assignments.
* Every member must have at least one Account Owner assigned. Attempts to delete the final Account Owner are rejected.
* The dashboard prevents duplicate assignments for the same member, scope, and project.
* Removing a role hides it from the active list but keeps the history available; you can restore access later by adding the role again.