my-automatic-backup
# Reminders
- Backup any important .ini files and merge manually after pulling new .ini files

# Usage
- Configure with backup.ini
- Add '(encrypted)' to a destination name to trigger file archival and encryption
  - Destination will contain:
      - python code to encrypt and decrypt
      - click the decrypt.bat file to extract archive, after which you will be prompted for a password that was used to encrypt this
- Standard backup destinations will simply backup each of the sources to each destination and create a sub directory corresponding to the root directory of each source.
    - e.g. source-->'C:\asd\fgh' --TO--> destination-->'F:\xcv\z\' will create a 'fgh' directory in destination 

# Components
Uses the standard Python 3 library. Base implementation was built for windows machines although the implementation can be modified in `BackupTools.py`. Minor changes may be needed in the parent files: `backup.py` and `BackupUtils.py` for a linux or mac implementation.

Encrypted backup functionality implements the 7z command. Documentation: https://sevenzip.osdn.jp/chm/cmdline/syntax.htm