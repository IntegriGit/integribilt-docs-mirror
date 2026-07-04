> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://help.getzep.com/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://help.getzep.com/_mcp/server.

# Configuring authentication

Available to [Enterprise Plan](https://www.getzep.com/pricing) customers only.

This page is for administrators. It covers connecting a project's Memory MCP Server to your identity provider so end users can sign in and reach their own memory. For the end-user side, see [Connecting a client](/memory-mcp-server/connect).

## Before you start

* The Memory MCP Server must be enabled for your account. Contact [sales](mailto:sales@getzep.com) if it is not yet available.
* You need the `mcp.connection.manage` capability on the project. This is a dedicated capability, separate from member OIDC configuration — see [Role-Based Access Control](/role-based-access-control).
* Register an OIDC application (a confidential client) in your identity provider so Zep can sign users in. You will need its client ID and client secret, and the provider's issuer URL.

Zep sends users to your identity provider to log in; it never stores end-user credentials. Each project has one active connection — one identity provider.

## Configure the connection

You configure the connection in the Zep Dashboard under your project's **Settings ▸ MCP** page.

Register a confidential OIDC client. Set its redirect URI to Zep's OAuth callback, shown on the MCP settings page when you create the connection. Note the client ID, client secret, and issuer URL.

On **Settings ▸ MCP**, create a connection and enter your identity provider's issuer URL and client credentials. Zep validates the issuer and finds its signing keys automatically. The client secret is stored securely and is never displayed again.

Choose the claim that maps to a Zep user and configure any admission restrictions. See the field reference below.

Leave the connection read-only or opt into writes, and decide whether new users are provisioned automatically. See [Writes](#writes) and [Provisioning new users](#provisioning-new-users).

Enable the connection. Until you enable it, clients cannot connect to the project's MCP endpoint.

## Connection settings

| Setting                         | Description                                                                                                                                                                                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identity provider issuer URL    | The OIDC issuer for your provider. Validated when you create the connection.                                                                                                                                                        |
| JWKS URL                        | The provider's signing-key endpoint. Found automatically from the issuer if you leave it blank.                                                                                                                                     |
| Client ID and client secret     | The credentials for the OIDC application you registered. The secret is write-only — Zep never displays it again.                                                                                                                    |
| User ID claim                   | The claim mapped to the Zep user. Defaults to `sub`. Confirm your chosen claim is a stable identifier for each user, and set it before users connect — changing it later breaks the mapping, and existing users return as new ones. |
| Email claim                     | Optional claim used to populate the user's email.                                                                                                                                                                                   |
| Allowed domains                 | Optional list restricting access to users whose email is in these domains.                                                                                                                                                          |
| Groups claim and allowed groups | Optional claim and list restricting access to members of specific groups.                                                                                                                                                           |
| Just-in-time provisioning       | Whether a new user is created on first sign-in. Off by default.                                                                                                                                                                     |
| Allow writes                    | Whether connected clients may write to memory. Off by default.                                                                                                                                                                      |
| Access token lifetime           | How long an issued token stays valid, from 60 seconds to 24 hours. Defaults to about five minutes.                                                                                                                                  |

### Admission gates

Allowed domains and allowed groups are **admission** gates, checked at login. Group membership comes from the OIDC `groups` claim, which is only as fresh as the user's last login — treat these gates as coarse admission control, not live revocation. To stop access immediately, revoke the user's session or disable the connection (see [Revoking access](#revoking-access)).

Widening an admission gate — adding domains or groups — requires an explicit re-confirmation step in the dashboard.

### Writes

A connection is read-only by default: connected clients can read memory but not change it, and the write tools are hidden. Enabling writes exposes the `add_memory` tool so clients can add to a user's memory.

An account-level **writes kill switch** overrides every connection's write setting. It is off by default; when you engage it for incident response, all writes are blocked regardless of per-connection configuration.

### Provisioning new users

Just-in-time provisioning is off by default. When it is off, only existing Zep users can connect, and an unknown user is turned away. When it is on, a user who signs in successfully and passes the admission gates is created on first connect. Provisioning is rate-limited per account.

## Revoking access

* **One user:** revoke the user's session. They cannot obtain a new token; a token already issued keeps working until it expires (about five minutes by default).
* **Everyone:** disable the connection. New sign-ins are refused immediately, and tokens already issued stop working within a few minutes.
* **All writes:** engage the account-level writes kill switch.

Lower the connection's access token lifetime to shorten how long a revoked token can linger.

## Auditing

Every connection change — create, update, enable, disable, delete — is recorded in an audit log with the member who made it and a before-and-after snapshot. Review it on the MCP settings page. Changes to writes, provisioning, and the admission gates are the ones to watch.