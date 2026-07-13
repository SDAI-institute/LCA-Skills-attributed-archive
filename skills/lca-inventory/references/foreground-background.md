# Foreground/background construction

## Foreground

Processes directly controlled, redesigned, measured, or decision-sensitive. Preserve engineering parameters and site/technology specificity.

## Background

Generic supply chains outside direct control, represented by databases or established models. Background selection still requires geography, technology, time, and system-model fit.

## Interface rules

- Each foreground exchange maps to one clearly defined product/service.
- Record provider dataset and mapping rationale.
- Avoid double counting upstream production already embedded in an external model.
- Do not replace a decision-sensitive process with a generic market average merely for convenience.
- Use market datasets when a consumption mix is intended; use production/transformation datasets when the producer technology is intended.
- Preserve losses and transport between foreground and background handoffs.

## Nested models

When importing results from GREET, process simulation, EPD, or supplier PCF:

1. document included stages and elementary flows;
2. identify overlap with the host database;
3. decide whether to import an inventory, aggregated process, or indicator result;
4. avoid mixing LCIA results into an inventory model unless explicitly doing result-level aggregation;
5. retain source model/version and uncertainty.
