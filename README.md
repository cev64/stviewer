# Sunday Wall

A drag-and-drop planner for the NFL Sunday TV wall — three screens stacked on one
mount, planned separately for the 1:00 ET and 4:00 ET windows of every week of the
2026 regular season.

Open `index.html` in a browser. No build step, no server, no dependencies.

## The wall

| Screen | Layouts |
| --- | --- |
| Top 40″ | 1 up, or 2 up |
| Main 65″ | 1 up, 2 up, or quad box |
| Bottom 40″ | 1 up, or 2 up |
| Laptop | 1 up (off by default) |

Three to nine streams depending on how the sets are split. The laptop is added
per window with **Add laptop** and sits on the table to the right of the mount;
removing it returns its game to the rack. Its panel is 15″, but it is drawn at
21″ because it sits closer than the TVs, so the wall shows how big it actually
looks from the couch. Panel widths across the whole room are true to their
diagonals — a 40″ is 61.54% the width of the 65″, the laptop 32.31%. NFL RedZone sits at
the top of the rack and can take any of those slots in either window. Dropping to
a smaller layout sends the games on the screens it loses back to the rack.

### Pictures are drawn at true size

A 16:9 source shown on half of a 16:9 screen does not fill that half — it
letterboxes, taking the full width and half the height, with black above and
below. The wall draws it that way, so what you see is the size the picture will
actually be. That is also why the quad box is the efficient layout: quartering a
16:9 screen gives four cells that are themselves exactly 16:9, so four games fill
the panel with no black bars at all, while 2 up on the same panel wastes half of
it.

## Using it

Every week and window opens the same way: **RedZone on the top 40″, every other
screen blank.** Build from there.

- **Drag** a game from the rack onto a screen. Drag between screens to swap them,
  or drag one back to the rack to pull it. On a touchscreen, press and hold for
  about half a second to pick a game up — it buzzes and lifts so you can tell.
  Anything shorter stays a scroll.
- **Or tap** a game, then tap a screen.
- **Tap a game already on a screen** to cover it with a red ✕. The ✕ removes it,
  the red around the ✕ backs out, and tapping a different screen swaps the two.
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
