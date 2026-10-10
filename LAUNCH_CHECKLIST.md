# Launch checklist

**Status: NOT READY TO LAUNCH.** The project is an educational tourism chatbot, not live travel information or a booking service.

- [x] Add Karnataka tourism persona, separate sourced knowledge file, interface, course report, and evaluation set.
- [x] Warn that timings, closures, entry rules, prices, and fees may change.
- [x] Add favicon and sample privacy and terms pages.
- [x] Configure Render for public access with its default hostname and no shared-password gate.
- [ ] Connect this private GitHub repository to Render, set `OPENAI_API_KEY` through Render secrets, and deploy.
- [ ] Verify the public URL, HTTPS, API health, chat, legal pages, mobile layout, and provider error handling.
- [ ] Add API spend alerts/limits and abuse controls before broad public promotion.
- [ ] Human-review evaluation responses and source details.
- [ ] Obtain legal, privacy, and security review before production use; establish retention and deletion controls.

The repo being created does not make the service live. Anyone with the eventual public URL can use the service and incur API usage. Do not share a launch URL until deploy and checks succeed.
