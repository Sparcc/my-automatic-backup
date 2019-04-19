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