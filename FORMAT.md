# Data format

- Offsets are zero-based byte offsets within each decoded registry value, except colorTableFileOffset, which is an offset in USER.EXE.
- All original registry scheme bytes are preserved losslessly in rawHex.
- Layout interpretation: 8-byte header; nonclient metrics and five 60-byte LOGFONTA records at offsets 8..343; 60-byte icon LOGFONTA at 344; 29 four-byte system-color entries at 404.
- Metric and font numbers are raw signed integers from the scheme, not converted to pixels or points.
- The meaning of both header DWORDs is deliberately left unassigned.
- LOGFONTA uses an ANSI 32-byte face-name buffer, decoded here as Windows-1252 up to the first NUL. Trailing bytes may be uninitialized data and are preserved.
- Color RGB bytes are red, green, blue in memory. The fourth byte is preserved separately; it is not alpha. Values such as 0x02 can indicate palette-related COLORREF flags.
- System-color index 25 is retained as ButtonAlternateFace, the name found in USER.EXE; it is not a standard documented GetSysColor index in current documentation.
- Gradient endpoints do not establish whether gradient captions are enabled; that setting is outside this Schemes export.
- The added Windows Standard (default) is explicitly reconstructed. Its original exported counterpart is retained unchanged.

Each file includes `schemaVersion`, source hashes, the original display name, provenance, byte length, SHA-256 of the scheme bytes, `rawHex`, `header`, `metrics`, `fonts`, and `colors`. Every original 520-byte payload is preserved. The JSON is an archival/decoded representation, not an installable Windows theme file.
