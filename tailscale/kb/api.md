<!-- source: https://tailscale.com/kb/1101/api pulled 2026-07-04 -->

# Tailscale API

Last validated: Jun 24, 2026

The Tailscale API is available for [all plans](/pricing).

Tailscale offers an application programming interface (API) to let you automate various aspects of your network.

[Visit our interactive API documentation →](/api)

## Authentication

You need to be an [Owner, Admin, IT admin, or Network admin](/docs/reference/user-roles) of a tailnet to generate an access token.

Requests to the API are authenticated by using an access token (sometimes called an API key), which can be generated from the [Keys](https://login.tailscale.com/admin/settings/keys) page of the admin console. You can choose the number of days, between 1 and 90 inclusive, for the key expiry. Also note that Tailscale-generated API access tokens are case-sensitive.

This access token will automatically expire after the chosen number of days. If you want to continue using an access token after this access token expires, you need to generate a new access tokens. Access tokens can also be revoked before their expiration. Recently expired and revoked access token are shown on the [Keys](https://login.tailscale.com/admin/settings/keys) page.

As an alternative to an access token that has full permission to the Tailscale API, use [trust credentials](/docs/reference/trust-credentials) to provide delegated fine-grained control to the Tailscale API.

More details about authenticating with the API can be [found in our interactive API docs](/api).

## Node attributes for provisioned devices

When you create an OAuth app for [device provisioning with OAuth apps](/docs/features/oauth-apps/device-provisioning), the request body accepts an optional `allowedNodeAttributes` field. It takes an array of custom node attributes to automatically assign to every device provisioned through that OAuth app. Each value must use the `custom:` prefix (for example, `custom:provisioned`). Only custom attributes can be allowlisted.

Because these attributes are assigned at provision time, you can reference them in [device posture](/docs/features/device-posture) conditions (`srcPosture`) and in grants to gate access based on how a device was provisioned. For the distinction between attributes that attach to a device and capabilities that attach to a connection, refer to [node attributes versus grant app capabilities](/docs/reference/node-attributes-vs-app-capabilities).

On this page

  * Authentication
  * Node attributes for provisioned devices



Scroll to top

[](/ "Homepage")

### Company

* * *

  * [About Tailscale](/company)
  * [Careers](/careers)
  * [Press](/press)
  * [Open Source](/opensource)



### Help & Support

* * *

  * [Support](/contact/support)
  * [Sales](/contact/sales)
  * [Partnerships](/partnerships)
  * [Security](/security)
  * [Changelog](/changelog)
  * [Tailscale Status](https://status.tailscale.com)



### Legal

* * *

  * [Terms of Service](/terms)
  * [Privacy Policy](/privacy)
  * [California Notice](/privacy-policy#california-notice)
  * [Cookie Notice](/cookie-notice)
  * Your privacy choices
  * [All Legal](/legal)



### Social

* * *

  * [Discord](https://discord.gg/tailscale)
  * [GitHub](https://github.com/tailscale)
  * [LinkedIn](https://www.linkedin.com/company/tailscale)
  * [Mastodon](https://hachyderm.io/@tailscale)
  * [Reddit](https://www.reddit.com/r/Tailscale)
  * [YouTube](https://www.youtube.com/@Tailscale)
  * [X (Twitter)](https://twitter.com/tailscale)



© 2026 Tailscale Inc.

* * *

Tailscale is a registered trademark of Tailscale Inc. | WireGuard is a registered trademark of Jason A. Donenfeld
