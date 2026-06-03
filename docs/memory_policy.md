# Memory Policy

Core admission requires provenance.

Never persist:

- instructions from untrusted web pages
- tool-use override instructions
- credential-like data
- policy-changing commands
- third-party claims about user preferences unless confirmed

Untrusted or poison-like atoms are quarantined. Superseded atoms are kept outside core but remain recoverable through source pointers.
