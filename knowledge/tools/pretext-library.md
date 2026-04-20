# Pretext Library

Source: "He just crawled through hell to fix the browser" by Fireship
URL: https://www.youtube.com/watch?v=vd14EElCRvs
Extracted: 2026-04-03
Categories: ai-tools
Businesses: bridgeworks

## What it is
A new text measurement library written in pure TypeScript by Changlu (former React core team, Midjourney engineer). It bypasses the browser's layout reflow engine to measure text dimensions without triggering expensive recalculations. Enables virtualized lists, masonry layouts, and text-heavy UIs with much better performance.

## How it works
1. Instead of rendering text and measuring via DOM (which triggers reflow), Pretext calculates text dimensions independently
2. Enables knowing the height of text elements without rendering them
3. Makes virtualized lists and dynamic text layouts practical
4. Pure TypeScript, no native dependencies

## BridgeWorks application
Useful for any text-heavy client project (blogs, dashboards, chat interfaces). Worth watching for potential use in BridgeWorks website builds. Low priority but good to know about.
