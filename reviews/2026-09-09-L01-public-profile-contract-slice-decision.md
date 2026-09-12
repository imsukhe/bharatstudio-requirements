# Decision — L01 public profile contract slice

**Date:** 2026-09-09  
**State:** `Implemented and locally verified; independent review open`

The opt-in public profile search/lookup surface is client-facing and therefore
requires typed contract coverage. The published projection must remain exactly
the existing privacy-minimised response. This decision does not publish viewer
badges, support history, account visibility mutation, OAuth, or provider data.

The OpenAPI and fixture schema now encode the minimal public projection. A
hostile `netLifetimeAmountPaise` mutation fails validation, preventing the
contract from quietly widening to public financial history.
