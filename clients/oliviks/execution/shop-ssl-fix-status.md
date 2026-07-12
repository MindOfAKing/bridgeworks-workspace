# Shop SSL fix — status

**Problem:** shop.oliviks.com serves the shared-server cert (CN=*.web-hosting.com),
not a cert for the domain, so every visitor gets a browser security warning. Because
oliviks.com carries a manually-installed cert (expires Oct 9 2026) that only covers
oliviks.com + www, cPanel AutoSSL stands down account-wide ("will not renew via
AutoSSL because it was not issued via AutoSSL") and never issues one for the shop
subdomain.

**Why it must go through Namecheap:** cPanel shared hosting has NO "Run AutoSSL"
button (Namecheap removed it), the SSL Wizard has no products available, and the
Namecheap SSL plugin only auto-installs PAID certs. The only fix is Namecheap forcing
AutoSSL server-side (or deleting the blocking manual cert, which risks an HTTPS gap on
oliviks.com and can't be self-triggered).

**Action taken 2026-07-12:** Opened Namecheap Live Chat (logged in as Oliviks
Kitchen, cPanel user olivoilt, server72.web-hosting.com) and lodged the request.

**ACTUAL ROOT CAUSE (found by Namecheap agent Mykyta K.):** shop.oliviks.com was
added to cPanel as an ALIAS domain. Alias domains cannot receive their own AutoSSL
certificate — that is why it never got one, regardless of the manual oliviks.com
cert. This is NOT a "run AutoSSL" problem.

**Fix in progress (Namecheap doing it server-side):** convert shop.oliviks.com from
an alias to an ADD-ON domain, "Share Document Root" unchecked, document root kept
identical so WooCommerce keeps serving, then run AutoSSL. Emmanuel authorized cPanel
access and ~1 min downtime. Agent handed off Mykyta K. -> Kateryna B., who is
performing it. Ref: namecheap.com KB 897/29 (how to create an add-on domain).

**If it must be redone manually later:** Domains section in cPanel, remove the
shop.oliviks.com alias, re-add as add-on domain with the SAME document root as the
main site (WooCommerce lives there), Share Document Root unchecked, then AutoSSL.
Do it at low traffic; expect a brief outage.

**Verify when done:** re-pull the cert and confirm it names the domain, not
*.web-hosting.com:
```
echo | openssl s_client -connect shop.oliviks.com:443 -servername shop.oliviks.com 2>/dev/null | openssl x509 -noout -subject -ext subjectAltName
curl -sI https://shop.oliviks.com/  # expect 200/301 without -k, not 000
```

**Blocks:** domain flip ([[oliviks-domain-flip-plan]]) should wait until this is green.
