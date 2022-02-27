# Hackwest iOS forensics
![frontend](doc/imgs/fdcdeb541d1a297e6580b44319ff9f22.png)

**JPEG**
```
JPEG image data, JFIF standard 1.01, aspect ratio, density 72x72, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=2, orientation=upper-left], baseline, precision 8, 200x154, components 3
```
**PNG**
```
PNG image data, 96 x 96, 8-bit/color RGBA, non-interlaced
```
**PDF**
```
PDF document, version 1.4, 14 pages
```
**MP4**
```
ISO Media, MP4 Base Media v1 [ISO 14496-12:2003]
```

**SQLite**
```
SQLite Write-Ahead Log, version 3007000
```
**XML**
```
XML 1.0 document, ASCII text
```
**RTF**
```
RIFF (little-endian) data, Web/P image
```
**M4a**
```
ISO Media, Apple iTunes ALAC/AAC-LC (.M4A) Audio
```

- Calculate the size of data by filetype
- Find Contacts
- Find Networks

### Steps to finding address book
- Find manifest.db

- Seach manifest.db for Library/AddressBook/AddressBook.sqlite.db
```sql
SELECT fileID FROM Files WHERE relativePath = 'Library/AddressBook/AddressBook.sqlitedb';
```
- Search your indexed database for this fileID


```sql
    SELECT 
    ABPerson.ROWID,
    c16Phone,
    FIRST,
    MIDDLE,
    LAST,
    c17Email,
    DATETIME(CREATIONDATE+978307200,'UNIXEPOCH'),
    DATETIME(MODIFICATIONDATE+978307200,'UNIXEPOCH'),
    NAME
    FROM ABPerson
    LEFT OUTER JOIN ABStore ON ABPerson.STOREID = ABStore.ROWID
    LEFT OUTER JOIN ABPersonFullTextSearch_content on ABPerson.ROWID = ABPersonFullTextSearch_content.ROWID
```