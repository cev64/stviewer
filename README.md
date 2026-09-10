# Sunday Wall

A drag-and-drop planner for the NFL Sunday TV wall — three screens stacked on one
mount, planned separately for the 1:00 ET and 4:00 ET windows of every week of the
2026 regular season.

Open `index.html` in a browser. No build step, no server, no dependencies.

## The wall

| Screen | Layouts |
| --- | --- |
| Top 40″ | 1 up, or 2 up |
| Main 65″ | Quad box (always four) |
| Bottom 40″ | 1 up, or 2 up |

Six to eight streams depending on how the 40″ sets are split. NFL RedZone sits at
the top of the rack and can take any of those slots in either window.

## Using it

Every week and window opens the same way: **RedZone on the top 40″, every other
screen blank.** Build from there.

- **Drag** a game from the rack onto a screen. Drag between screens to swap them,
  or drag one back to the rack to pull it. On a touchscreen, press and hold
  briefly to pick a game up — a quick swipe still scrolls the page.
- **Or tap** a game, then tap a screen.
- **Keyboard:** tab to a game or a screen, `Enter` to pick up or place, `Delete`
  to clear a screen, `Esc` to cancel.
- **Auto-fill** seats the unassigned games starting with the 65″ quad, and
  **Reset wall** puts the window back to RedZone-on-top.

Every week × window is saved independently, so Week 4's 4:00 wall does not
disturb Week 4's 1:00 wall.

## Schedule data

`index.html` embeds the full 2026 regular-season schedule — 205 games across
18 weeks — pulled from ESPN's public scoreboard API and filtered to the Sunday
1:00 ET and 4:00 ET (4:05/4:25) windows. Thursday, Sunday night, Monday,
international and holiday games are deliberately excluded.

Kickoffs the league has not set yet come through as **Flex** and appear in both
windows: four in Week 16, four in Week 17, and all sixteen in Week 18, which the
NFL schedules only after Week 17 finishes. Networks shown are the producing
broadcast; Sunday Ticket carries every game listed.

To refresh the data after the league moves games, re-run the extraction against
`https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=2026&seasontype=2&week=N`
and replace the JSON in the `#sked` script tag.

## Files

- `index.html` — the standalone page, everything embedded.
- `sunday-wall.html` — the same page as a Claude Artifact body (no `<html>`
  wrapper), which additionally syncs saved lineups across devices through the
  artifact `db` capability. The standalone page falls back to `localStorage`.
