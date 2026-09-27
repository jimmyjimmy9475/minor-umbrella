# Better coding practices

For the week 10 deliverable we modified out repository to follow better coding practices. A summary of those practices are provided below:

- Removal of unused files (namely the no code solution). It was not being used, nor did we intend to. It is always recoverable through the git history if needed.
- Clear separation of parts. The folder was restructured into code, data and output. Data should not be modified, output contains intermidate and final output. Both data(our dataset isn't huge and the licences allow for it) and code were both checked in, while outputs was not.
- Changing the filepaths relative to the repository root directory
- Moving file paths to the head of the document
- Adding a brief description to the top of the document
- Renamed files to be clear about their purpose and the order they are to be run in
- Added assert statements
- Added comments breaking up sections